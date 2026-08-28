# A09 — Current-Line Runtime Target

The worker branch is the HQ return/control branch:

- `agent/verkhovod-a09-lmq013-response35-runtime-r1`
- start `c68b1ea88aba402ce3670e620cb98a126b662dba`

The live G8 implementation line required by the command is PR #27:

- PR: `#27 Source/wave identity repair campaign`
- current head observed by A09: `75aac98e0280289a717e2b49f8d2066ab1c926db`
- state: open / draft
- G8 closure: still open.

## Material code-line difference

At the A09 starting ref:
- smoke blob: `446196773920cd0296c9d78ecaae4e5dbef93d4c`
- facet-ready deployment blob: `9c595b9f08e4c2a89ed541f7cd68bd8669e8f9f4`
- no `ddm_source_wave_identity.py` is present;
- no PG8-009/010 tests are present.

At PR #27 head:
- smoke blob: `9ae08618d08cfce8e1270067c727ea13f6aac709`
- facet-ready deployment blob: `060191e4447c794c658552c7018ce7e5ce5be5bc`
- SWID identity kernel blob: `f58fb511d633c1d63632242c98733ed89fdb6cb7`
- PG8-009 blob: `1236cd3f60061b6c96c2b7b93c2c1931cae7b58a`
- PG8-010 blob: `c761f2ace7ddbaba4a90d314333698c8b2a049cb`.

Therefore a fresh G8 court must execute the PR #27 current line (or its exact accepted successor), while writing the resulting court receipt back to this A09 return branch.
