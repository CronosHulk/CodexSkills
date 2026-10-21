#!/usr/bin/env python3
"""Non-destructive Codex CLI probe; does not invoke a model."""
import shutil,subprocess,sys
exe=shutil.which("codex")
if not exe:
    print("Codex CLI not installed / not on PATH; static validation still available.")
    sys.exit(0)
for args in ([exe,"--version"],[exe,"--help"]):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=10)
        print(" ".join(args), "exit=",p.returncode)
        print((p.stdout or p.stderr)[:700])
    except Exception as e:print("Probe unavailable:",e)
print("IMPORTANT: CLI presence does NOT verify model availability, effective subagent models or routing.")
print("Use /model, /status and inspect subagent runs in a real trusted Codex session.")
