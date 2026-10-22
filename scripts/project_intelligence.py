#!/usr/bin/env python3
"""Local project memory, reverse-dependency impact, and conservative test hints.
No external dependencies, execution of tests, or network calls.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

# Reuse the bundled graph; avoid duplicating its parsing and import resolution.
import importlib.util
GRAPH=Path(__file__).resolve().parents[1]/'.agents/skills/graphify/scripts/graph.py'
spec=importlib.util.spec_from_file_location('local_graphify',GRAPH)
graph=importlib.util.module_from_spec(spec);spec.loader.exec_module(graph)

def store(root):return root/'.graphify/memory.json'
def load_memory(root):
 p=store(root)
 if not p.exists():return {'version':1,'entries':[]}
 data=json.loads(p.read_text(encoding='utf-8'))
 if not isinstance(data,dict) or not isinstance(data.get('entries'),list):raise ValueError('Invalid memory schema')
 return data

def write_json(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,prefix='.tmp-',delete=False,encoding='utf-8') as f:
  json.dump(data,f,ensure_ascii=False,indent=2);temp=f.name
 os.replace(temp,path)

def valid_path(root,name):
 if not name or Path(name).is_absolute():raise ValueError('Use a non-empty relative path')
 path=(root/name).resolve()
 if not path.is_relative_to(root):raise ValueError('Path escapes project root')
 return path.relative_to(root).as_posix()

def remember(root,kind,summary,paths,source):
 if kind not in ('decision','pitfall','convention','failure','constraint'):raise ValueError('Invalid kind')
 if not summary.strip() or len(summary)>1200:raise ValueError('Summary required (<=1200 chars)')
 if len(paths)>20:raise ValueError('Too many paths')
 paths=sorted(set(valid_path(root,p) for p in paths))
 if source not in ('user','verified-code','verified-test','reviewed-decision'):raise ValueError('Unverified source')
 data=load_memory(root)
 import hashlib
 key=hashlib.sha256((kind+'\n'+summary.strip()+'\n'+','.join(paths)).encode()).hexdigest()[:16]
 for entry in data['entries']:
  if entry['id']==key:return entry
 entry={'id':key,'kind':kind,'summary':summary.strip(),'paths':paths,'source':source,'created_at':datetime.now(timezone.utc).isoformat()}
 data['entries'].append(entry);write_json(store(root),data)
 return entry

def recall(root,term='',paths=(),limit=10):
 entries=load_memory(root)['entries'];term=term.lower().strip();paths=set(paths)
 result=[]
 for e in entries:
  matches_path=not paths or any(p==q or p.startswith(q+'/') or q.startswith(p+'/') for p in e['paths'] for q in paths)
  matches_term=not term or term in (e['summary']+' '+' '.join(e['paths'])).lower()
  if matches_path and matches_term:result.append(e)
 return result[-limit:]

def changed_files(root,base=None):
 cmd=['git','diff','--name-only','--diff-filter=ACMR']
 if base:cmd+= [base]
 result=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=15)
 if result.returncode:raise RuntimeError(result.stderr.strip() or 'git diff failed')
 staged=subprocess.run(['git','diff','--cached','--name-only','--diff-filter=ACMR'],cwd=root,capture_output=True,text=True,timeout=15)
 untracked=subprocess.run(['git','ls-files','--others','--exclude-standard'],cwd=root,capture_output=True,text=True,timeout=15)
 paths=set(result.stdout.splitlines())|set(staged.stdout.splitlines())|set(untracked.stdout.splitlines())
 return sorted(p for p in paths if (root/p).is_file())

def impact(g,changed,depth=3):
 # Edge source imports target; reverse traversal discovers importers affected by changes.
 reverse={}
 for e in g['edges']:reverse.setdefault(e['target'],set()).add(e['source'])
 known={n['id'] for n in g['nodes']};seeds={p for p in changed if p in known}
 visited=set(seeds);front=set(seeds);levels=[]
 for _ in range(depth):
  nxt=set().union(*(reverse.get(p,set()) for p in front)) -visited if front else set()
  if not nxt:break
  levels.append(sorted(nxt));visited|=nxt;front=nxt
 return {'changed':sorted(changed),'indexed_changed':sorted(seeds),'affected':sorted(visited-seeds),'levels':levels,'unindexed':sorted(set(changed)-known),'note':'Static Python import edges only; dynamic imports, external callers, JS/TS and runtime behavior may be missing.'}

def test_candidates(root,g,report,limit=30):
 impacted=set(report['changed'])|set(report['affected']); candidates=[]
 for n in g['nodes']:
  p=n['id']; name=Path(p).name
  if not (name.startswith('test_') and name.endswith('.py') or name.endswith('_test.py')):continue
  if p in impacted:candidates.append({'file':p,'reason':'dependency-graph'})
  else:
   # Heuristic only; label accordingly and do not claim comprehensive coverage.
   stems={Path(x).stem.replace('test_','').replace('_test','') for x in impacted}
   if any(len(s)>=4 and s in name for s in stems):candidates.append({'file':p,'reason':'filename-heuristic'})
 candidates=sorted(candidates,key=lambda x:(x['reason']!='dependency-graph',x['file']))[:limit]
 return {'suggested_tests':candidates,'example_command':('python -m pytest '+' '.join(x['file'] for x in candidates)) if candidates else None,'run_full_suite_when':'security, payments, migrations, API contracts, release, incomplete graph, or high-risk changes','warning':'Suggestions are not proof of coverage. Review and run tests explicitly; this tool never executes tests.'}

def main(argv=None):
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['remember','recall','impact','tests','sync']);ap.add_argument('--root',default='.');ap.add_argument('--kind');ap.add_argument('--summary');ap.add_argument('--path',action='append',default=[]);ap.add_argument('--source',default='verified-code');ap.add_argument('--term',default='');ap.add_argument('--base');ap.add_argument('--limit',type=int,default=20)
 args=ap.parse_args(argv);root=Path(args.root).resolve()
 if args.command=='remember':
  if not args.kind or not args.summary:ap.error('remember requires --kind and --summary')
  result=remember(root,args.kind,args.summary,args.path,args.source)
 elif args.command=='recall':result=recall(root,args.term,[valid_path(root,p) for p in args.path],min(max(args.limit,1),100))
 else:
  g,count=graph.sync(root)
  if args.command=='sync':result={'indexed_files':len(g['nodes']),'reindexed_files':count,'edges':len(g['edges'])}
  else:
   paths=[valid_path(root,p) for p in args.path] if args.path else changed_files(root,args.base)
   report=impact(g,paths)
   result=report if args.command=='impact' else test_candidates(root,g,report,min(max(args.limit,1),100))
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
