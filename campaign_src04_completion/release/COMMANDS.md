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

For the pinned fixed-B v2 repaired input (178+3 only where source-qualified):

```sh
PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode primary \
  --grant campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json \
  --grant-sha256 <exact-sha256> \
  --repaired-config rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json \
  --repaired-config-sha256 5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5
```

Expected current output: `BLOCKED_MISSING_FULL_SOURCE_GRANT`; 163 complete
responses, 15 held responses, 2 initial coordinates, q701 held, 1,195,931 response
positions, all 181 slots accounted. No original SAV I/O and no native release.
