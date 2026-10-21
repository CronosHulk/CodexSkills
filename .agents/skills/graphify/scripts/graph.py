#!/usr/bin/env python3
"""Dependency graph for local code; stdlib-only, incremental, no external calls."""
import argparse, ast, hashlib, json, os, re
from pathlib import Path
from collections import deque

EXCLUDE={'.git','.graphify','node_modules','.venv','venv','dist','build','__pycache__','.next','.tox'}
SUFFIX={'.py','.js','.jsx','.ts','.tsx','.go','.rs','.java','.pl','.pm'}
MAX_BYTES=500_000

def walk(root):
    for base,dirs,files in os.walk(root):
        dirs[:]=sorted(d for d in dirs if d not in EXCLUDE and not d.startswith('.git'))
        for f in sorted(files):
            p=Path(base)/f
            if p.suffix in SUFFIX and not p.is_symlink():
                try:
                    if p.stat().st_size<=MAX_BYTES:yield p
                except OSError:pass

def analyze(root,p):
    rel=p.relative_to(root).as_posix(); data=p.read_bytes(); digest=hashlib.sha256(data).hexdigest()
    node={'id':rel,'kind':'file','hash':digest,'symbols':[],'imports':[]}
    if p.suffix=='.py':
        try:
            tree=ast.parse(data.decode('utf-8-sig'),filename=rel)
            for n in ast.walk(tree):
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                    node['symbols'].append({'name':n.name,'line':n.lineno,'kind':type(n).__name__})
                elif isinstance(n,ast.Import):node['imports'].extend(a.name for a in n.names)
                elif isinstance(n,ast.ImportFrom):
                    if n.module:node['imports'].append('.'*n.level+n.module)
        except (SyntaxError,UnicodeError):node['parse_error']=True
    return node

def sync(root):
    root=Path(root).resolve(); out=root/'.graphify/graph.json'; old={}
    if out.exists():
        try:old={n['id']:n for n in json.loads(out.read_text())['nodes']}
        except (ValueError,KeyError,TypeError):pass
    nodes=[];changed=0
    for p in walk(root):
        rel=p.relative_to(root).as_posix();data=p.read_bytes();digest=hashlib.sha256(data).hexdigest()
        if rel in old and old[rel].get('hash')==digest:node=old[rel]
        else:node=analyze(root,p);changed+=1
        nodes.append(node)
    by_module={n['id'][:-3].replace('/','.') :n['id'] for n in nodes if n['id'].endswith('.py')}
    for n in nodes:
        if n['id'].endswith('/__init__.py'):
            by_module[n['id'][:-12].replace('/','.')]=n['id']
    edges=[]
    for n in nodes:
        for imp in n['imports']:
            if imp.startswith('.'):continue # relative import resolution requires package context
            target=by_module.get(imp)
            if not target:
                matches=[(k,v) for k,v in by_module.items() if imp.startswith(k+'.')]
                if matches:target=max(matches,key=lambda x:len(x[0]))[1]
            if target and target!=n['id']:edges.append({'source':n['id'],'target':target,'kind':'imports'})
    result={'schema_version':1,'root':str(root),'nodes':nodes,'edges':edges}
    out.parent.mkdir(exist_ok=True)
    tmp=out.with_suffix('.json.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(out)
    return result,changed

def query(g,term,limit=12):
    term=term.lower();matches=[]
    for n in g['nodes']:
        syms=[s for s in n['symbols'] if term in s['name'].lower()]
        if term in n['id'].lower() or syms:
            matches.append({'file':n['id'],'symbols':syms[:8]})
    return matches[:limit]

def neighbors(g,node):
    return [e for e in g['edges'] if node in (e['source'],e['target'])]

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['sync','query','neighbors','stats'])
    p.add_argument('--root',default='.');p.add_argument('--term');p.add_argument('--node');p.add_argument('--limit',type=int,default=12)
    args=p.parse_args();g,changed=sync(args.root)
    if args.command=='sync':value={'files':len(g['nodes']),'edges':len(g['edges']),'changed':changed}
    elif args.command=='query':
        if not args.term:p.error('query requires --term')
        value=query(g,args.term,max(1,min(args.limit,100)))
    elif args.command=='neighbors':
        if not args.node:p.error('neighbors requires --node')
        value=neighbors(g,args.node)[:max(1,min(args.limit,100))]
    else:value={'files':len(g['nodes']),'edges':len(g['edges'])}
    print(json.dumps(value,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
