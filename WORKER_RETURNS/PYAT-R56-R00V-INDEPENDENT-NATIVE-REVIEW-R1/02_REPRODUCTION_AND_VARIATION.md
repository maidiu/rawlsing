# Independent reproduction and schema-conforming variation

## 36 cases

`tools/reviewer_replay.py` independently reads the five R2 policy files at the exact commit, recomputes their Git blob SHA-1s, builds each case from the independent baseline+overlay and materializes the pinned expected operation objects. It calls the public evaluator with the author’s handle only after verifying the handle’s blobs equal the independent pin.

Actual: **36/36 pass**, exact decisions, ceilings, reason lists, counts, missing/extra diffs, renamed `ARC1_BIJECTIVE_Q301_LOCAL`, and typed identity. Receipt: `evidence/reviewer_replay.json`.

## Independent variations

- valid subset cardinalities 1, 5 and 17 with `claims_scope_is_full_universe=false` → local ALLOW;
- full reconstructed multiset in reverse order → local ALLOW (no declared ordering of the operation set);
- complete frozen ARC1 renamed variant → local ALLOW;
- count-preserving replacement with an alien operation ID → REFUSE_FRONTIER;
- duplicate ID with extra count → REFUSE_FRONTIER;
- noninjective candidate rename → REFUSE_FRONTIER;
- typed identity distinguishes bool vs integer, null vs missing object, and ordered arrays;
- policy dependency substitution → REFUSE_FRONTIER; cold reload → local ALLOW.

The gate does not hardcode 18 operations: a 17-operation subset is accepted when the claim explicitly scopes itself, and an 18-record policy is treated as data. No C00–C35 case switch or literal q301 label blacklist exists in gate source.

## Limits

The pinned 18-operation policy is test material, not a native execution. The six author tests and the reviewer tests are policy fixtures; they do not qualify any survey or decoder.
