#!/usr/bin/env python3
"""Safe, dependency-free installer. Dry-run by default."""
import argparse
from pathlib import Path
import shutil
import sys

SOURCE=Path(__file__).resolve().parents[1]
FILES=[Path("AGENTS.md"),Path(".codex/config.toml")]
FILES+=sorted(p.relative_to(SOURCE) for base in (".agents/skills",".codex/agents","references")
              for p in (SOURCE/base).rglob("*") if p.is_file())
def install(destination,apply=False,overwrite=False):
    destination=Path(destination).expanduser().resolve()
    if destination==SOURCE:raise ValueError("destination must differ from source")
    created=skipped=[]
    created=0;skipped=0
    for rel in FILES:
        src=SOURCE/rel;target=destination/rel
        if target.exists() and not overwrite:
            print("SKIP existing",rel);skipped+=1;continue
        print("COPY" if apply else "WOULD COPY",rel)
        if apply:
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():
                backup=target.with_name(target.name+".bak")
                if backup.exists():raise FileExistsError(f"Backup already exists: {backup}")
                shutil.copy2(target,backup)
            shutil.copy2(src,target)
        created+=1
    print(f"{'Installed' if apply else 'Planned'} {created} files; skipped {skipped}.")
    if skipped:print("Merge existing AGENTS.md / .codex/config.toml manually.")
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--target",required=True,help="Target project root")
    ap.add_argument("--apply",action="store_true",help="Actually copy files")
    ap.add_argument("--overwrite",action="store_true",help="Back up and replace existing files")
    args=ap.parse_args()
    install(args.target,args.apply,args.overwrite)
