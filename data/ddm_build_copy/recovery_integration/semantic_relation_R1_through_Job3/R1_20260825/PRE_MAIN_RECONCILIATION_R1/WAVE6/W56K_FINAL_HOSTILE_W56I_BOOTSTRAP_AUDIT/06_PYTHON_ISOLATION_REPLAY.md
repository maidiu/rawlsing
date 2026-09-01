# Python isolation replay

## G7 — PASS for Python import/process isolation

Preserved exact-candidate W56J execution findings:
- ordinary invocation exited 97 before shadowable imports;
- direct shebang exited 97;
- `python3 -I -S` produced `isolated=1`, `ignore_environment=1`, `no_user_site=1`, `no_site=1`, `safe_path=1`;
- sibling stdlib-name shadows executed zero times;
- PYTHONPATH injection executed zero malicious imports;
- sitecustomize/usercustomize executed zero hooks;
- injected repository `sys.path` exited 98.

W56K independently replayed the process-resolution premise relevant to the newly found seam. With all five Python isolation flags true under `python3 -I -S`, a PATH-prepended hostile executable named `git` was executed successfully by `subprocess.run(['git', ...])`.

Observed equivalent replay:
`flags 1 1 1 1 True`
`returncode 0`
`stdout MALICIOUS_GIT_EXECUTED`

Conclusion: the Python import boundary is real and W56J's positive findings stand. It does not isolate subprocess executable resolution.