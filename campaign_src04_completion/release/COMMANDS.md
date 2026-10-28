# SRC04 full completion commands

Run from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/d1-src04-observed-tally`.

```sh
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode prepare
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode tests
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode replay
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode return \
  --artifact-commit <code-commit>
```

After the missing full grant is supplied:

```sh
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode primary \
  --grant campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json \
  --grant-sha256 <exact-sha256>
```

For a separately qualified lane-B repaired config:

```sh
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode primary \
  --grant campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json \
  --grant-sha256 <exact-sha256> \
  --repaired-config <immutable-config-path> \
  --repaired-config-sha256 <exact-sha256>
```

Expected current output: `BLOCKED_MISSING_FULL_SOURCE_GRANT`; 163 complete
responses, 15 held responses, 2 initial coordinates, q701 held, 1,195,931 response
positions, all 181 slots accounted. No original SAV I/O and no native release.
