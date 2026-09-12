# W2-D06 Commission — PREV3_M3_OBJECTIVE_RESULT_FIREWALL_IMPLEMENTATION_R1_ONLY

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w2-d06-m3-firewall-implementation-r1`

Frozen branch parent: `107fb80308dafb6dc2e9ba1dd15b8b2d9e7ac2d2`

Execute only:

`PREV3_M3_OBJECTIVE_RESULT_FIREWALL_IMPLEMENTATION_R1_ONLY`

## Read first

- HQ fan-in / dispatch authority.
- C07 governed return at `9ef74ff14dacf7dd3c224b5b4cab336ec1f6bf0e`.
- C07 `01_M3_FIREWALL_REPAIR_SPEC.md` blob `57c318fbc91470b5d6b1eb7e6c3247fde1c7f501`.
- C07 `02_ERROR_AND_CALLER_CONTRACT_DISPOSITION.tsv` and `03_HOSTILE_CASES.json`.
- Current M3, PRE553 source-relation and M4 relation-M1 binding code/tests named by C07.

## Mission

Implement the adopted M3 result-contract firewall: positive M3 output is lawful only under an exact competent current objective-world result contract; arbitrary lexical payloads may not self-certify. Preserve lawful objective actor-indexed facts and keep person-state semantics impossible in PRE-V3.

## Required implementation

- version affected M3 rule/object contract rather than silently reinterpret V1 `actor_independent`;
- exact result schema ref + content hash;
- exact semantic-owner/authority binding;
- `semantic_jurisdiction = PRE_V3_OBJECTIVE_WORLD`;
- explicit `actor_indexing_mode = NO_ACTOR_INDEX | OBJECTIVE_ACTOR_INDEXED` or exact equivalent;
- hard `person_state_semantics = FORBIDDEN` or equivalent;
- payload schema conformance before positive support;
- identity/replay material commits to rule + result schema + owner/authority + jurisdiction + indexing mode + canonical payload;
- no default/generic result schema fallback.

## Contract-drift repairs

- preserve exact-ref integrity behavior in PRE553 source relations; align stale tests rather than weaken production;
- preserve sealed relation-M1 producer-use boundary; positive test through governed wrapper, raw caller-selected use remains negative.

## Do not

- do not solve this with a larger forbidden-word list;
- do not categorically ban actor identifiers;
- do not weaken exact source relation or M4 use-authority guards;
- do not add psychological/person-state/driver/type semantics.

## Authorized write scope

The smallest production/schema/test surfaces allowed by C07 plus:

`.../HQ_FIRST_WAVE_FANIN_AND_SECOND_WAVE_DISPATCH_R1/SECOND_WAVE_WORKER_RETURNS/W2-D06/`

## Expected return

- `00_RETURN.md`
- exact modified production/test identities
- targeted regression results
- full relevant PRE-V3 regression results
- `01_FIREWALL_SCHEMA_AND_AUTHORITY_BINDING_RECEIPT.json`
- `02_HOSTILE_AND_OBJECTIVE_ACTOR_POSITIVE_RESULTS.json`

Library: `NO`.

PASS: all C07 hostile aliases fail closed, lawful objective actor-indexed controls pass under exact schema authority, stale contract tests are corrected without guard weakening, identity commits to semantic contract, and relevant regression is green.

This worker may self-PASS implementation only. Independent hostile qualification is a separate successor and remains required before broad M3 STOP is lifted.

Successor gate: `GATE-FIREWALL-HOSTILE-QUALIFICATION`.
