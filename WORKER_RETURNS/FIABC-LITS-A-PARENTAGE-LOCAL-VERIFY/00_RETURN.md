# FIABC LiTS-A Preserved Parentage Local Verification

## Terminal

`FIABC_LITS_A_LOCAL_PARENTAGE_VERIFY__HISTORICAL_ROOT_NOT_PRESENT__NO_REBUILD_PERFORMED`

## Scope

This worker performed only read-only artifact-location checks for the exact historical Candidate-A R5 root expected to identify as:

`e8f37557493b816e4562f5f47df110cf49b429e9ead54e5b624d6638ee07aa3d`

The prepared verifier was inspected before use. It was not executed because its required preserved R5 root input was not found.

## Bounded local finding

No `member_inventory.jsonl`, path containing the expected root prefix `e8f37557`, or Spotlight-indexed `root.json` was found in the searched local artifact surfaces:

- `/Users/matthewsmith/Desktop`
- `/Users/matthewsmith/Documents`
- `/Users/matthewsmith/Downloads`
- `/Users/matthewsmith/.Trash`
- `/Users/matthewsmith/Library/CloudStorage`
- `/tmp`
- `/private/tmp`
- `/Volumes`

The checked-out repository contains historical metadata naming the root, but not the preserved root itself. Repository metadata is not treated as proof of present filesystem existence.

## Prohibitions preserved

- Raw LiTS source bytes were not opened.
- R5 member payloads were not opened.
- Candidate A was not rebuilt or run.
- Candidate B/C, I03, I05, and measured P2X were not run.
- No preserved R5 root was mutated.
- No generic R35 parentage or currentness was inferred.

The commission requires stopping at the root-absent terminal. No rebuild was performed.
