# sys.path audit

Observed under `python3 -I -S`:

```
['/Library/Frameworks/Python.framework/Versions/3.11/lib/python311.zip',
 '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11',
 '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/lib-dynload']
```

Repository entries: 0. Script-directory entries: 0. CWD entries: 0. PYTHONPATH attacker entries: 0.

A controlled trusted-host invocation inserted the attack-worktree path before executing the gate. The gate exited 98 with `FAIL_CANDIDATE_CONTROLLED_IMPORT_PATH_PRESENT`, before `argparse` import.

