# Execution receipt

Candidate executed: YES.

- Ordinary invocation: exit 97, fail-closed isolation barrier.
- Direct shebang: exit 97, fail-closed isolation barrier.
- `python3 -I -S`: flags `isolated=1, ignore_environment=1, no_user_site=1, no_site=1, safe_path=1`.
- Sibling-shadow authoritative executions: 0 malicious imports.
- PYTHONPATH authoritative execution: 0 malicious imports.
- sitecustomize/usercustomize authoritative execution: 0 hook imports.
- Injected repository path: exit 98, `FAIL_CANDIDATE_CONTROLLED_IMPORT_PATH_PRESENT`.

The nonzero authoritative full-validator result is attributable to unavailable canonical dependencies and does not negate the measured interpreter-isolation barrier result.

