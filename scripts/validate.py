#!/usr/bin/env python3
"""Offline structural checks. No Codex invocation or API charges."""
import argparse
import json
from pathlib import Path
import re
import sys
import tomllib

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {'codex-token-saver', 'api-and-interface-design', 'graphify', 'debugging-and-error-recovery', 'code-simplification', 'smart-test-selection', 'using-agent-skills', 'context-engineering', 'security-and-hardening', 'code-review-and-quality', 'git-workflow-and-versioning', 'browser-testing-with-devtools', 'planning-and-task-breakdown', 'observability-and-instrumentation', 'deprecation-and-migration', 'doubt-driven-development', 'source-driven-development', 'test-driven-development', 'solid-pragmatic', 'interview-me', 'constraint-driven-development', 'documentation-and-adrs', 'spec-driven-development', 'frontend-ui-engineering', 'change-impact-analyzer', 'performance-optimization', 'shipping-and-launch', 'ci-cd-and-automation', 'incremental-implementation', 'idea-refine', 'project-memory'}
REQUIRED={"explorer","implementer","tester","reviewer","architect","security_reviewer"}
def check(root=ROOT):
    errors=[]; warnings=[]; roles={}
    skills=list((root/".agents/skills").glob("*/SKILL.md"))
    names=set()
    missing = EXPECTED_SKILLS - {f.parent.name for f in skills}
    if missing: errors.append(f"missing skill directories: {sorted(missing)}")
    for f in skills:
        content=f.read_text(encoding="utf-8")
        match=re.match(r"\A---\s*\n(.*?)\n---\s*\n",content,re.S)
        if not match:
            errors.append(f"{f}: missing YAML frontmatter");continue
        fm=match.group(1)
        fields={}
        for line in fm.splitlines():
            if ":" in line and not line.startswith((" ","\t")):
                k,v=line.split(":",1);fields[k.strip()]=v.strip().strip('"\'')
        for k in ("name","description"):
            if not fields.get(k):errors.append(f"{f}: missing {k}")
        name=fields.get("name")
        if name:
            if name in names:errors.append(f"duplicate skill {name}")
            names.add(name)
            if name != f.parent.name: errors.append(f"{f}: skill name differs from folder")
        if len(fields.get("description",""))>300:
            warnings.append(f"{f}: description >300 chars")
    for f in (root/".codex").rglob("*.toml"):
        try: data=tomllib.loads(f.read_text(encoding="utf-8"))
        except Exception as e:errors.append(f"{f}: invalid TOML: {e}");continue
        if f.parent.name=="agents":
            roles[f.stem]=data.get("model")
            if not data.get("developer_instructions"):errors.append(f"{f}: missing instructions")
    if not REQUIRED.issubset(roles):errors.append(f"missing agent roles: {sorted(REQUIRED-set(roles))}")
    for r in ("explorer","tester","implementer"):
        if "sol" in str(roles.get(r,"")).lower():errors.append(f"{r} unexpectedly uses expensive Sol")
    config=tomllib.loads((root/".codex/config.toml").read_text())
    if config.get("agents",{}).get("max_concurrent_threads_per_session",99)>2:
        warnings.append("concurrency above recommended 2")
    return {"ok":not errors,"skills":len(skills),"skill_names":sorted(names),"missing_skills":sorted(missing),"roles":roles,"errors":errors,"warnings":warnings}
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    result=check()
    if args.json:print(json.dumps(result,indent=2))
    else:
        print(f"Skills: {result['skills']} | Agent roles: {len(result['roles'])}")
        for item in result["errors"]:print("ERROR:",item)
        for item in result["warnings"]:print("WARN:",item)
        print("PASS" if result["ok"] else "FAIL")
    sys.exit(0 if result["ok"] else 1)
