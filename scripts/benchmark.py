#!/usr/bin/env python3
"""Summarize measured task runs from JSONL; no invented cost estimates."""
import argparse,csv,json,statistics
from collections import defaultdict
from pathlib import Path
def summarize(path):
    groups=defaultdict(list)
    for n,line in enumerate(Path(path).read_text().splitlines(),1):
        if not line.strip():continue
        r=json.loads(line)
        if r["mode"] not in ("baseline","optimized"):raise ValueError(f"line {n}: invalid mode")
        for field in ("task_id","mode","input_tokens","output_tokens","success"):
            if field not in r:raise ValueError(f"line {n}: missing {field}")
        if not isinstance(r["success"],bool):raise ValueError(f"line {n}: success must be boolean")
        groups[(r["task_id"],r["mode"])].append(r)
    for (task,mode),rows in sorted(groups.items()):
        mean=lambda key:round(statistics.mean(r[key] for r in rows),1)
        print(f"{task:24} {mode:10} n={len(rows)} "
              f"input={mean('input_tokens')} output={mean('output_tokens')} "
              f"success={sum(r['success'] for r in rows)}/{len(rows)}")
    for task in sorted({k[0] for k in groups}):
        b=groups.get((task,"baseline"),[]);o=groups.get((task,"optimized"),[])
        if b and o:
            tokens=lambda rs:statistics.mean(r["input_tokens"]+r["output_tokens"] for r in rs)
            before=tokens(b);after=tokens(o)
            if before:print(f"{task}: total-token change {(after/before-1)*100:+.1f}% (NOT dollar cost)")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("jsonl");args=p.parse_args()
    summarize(args.jsonl)
