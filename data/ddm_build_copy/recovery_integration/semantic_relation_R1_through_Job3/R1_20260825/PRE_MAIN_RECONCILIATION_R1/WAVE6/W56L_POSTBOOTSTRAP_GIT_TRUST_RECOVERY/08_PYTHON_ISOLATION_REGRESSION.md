# Python isolation regression

All W56J/W56K positive Python-process properties are preserved:

- built-in `sys` is the sole pre-barrier import;
- ordinary invocation fails at exit 97;
- direct shebang/non-isolated launch fails at the same barrier;
- authoritative execution requires `python3 -I -S`;
- `isolated`, `ignore_environment`, `no_user_site`, `no_site`, and `safe_path` must all be true;
- repository-root discovery no longer requires Git; the explicit root is checked before any Git subprocess;
- repository entries in active `sys.path` fail closed;
- zero Rawlsing/governance helper imports exist in the predecessor script.

Local hostile regression: a sibling `argparse.py` with an execution marker remained unexecuted under the repaired `-I -S` invocation.

The Git trust repair therefore narrows the subprocess boundary without reopening the Python import boundary.