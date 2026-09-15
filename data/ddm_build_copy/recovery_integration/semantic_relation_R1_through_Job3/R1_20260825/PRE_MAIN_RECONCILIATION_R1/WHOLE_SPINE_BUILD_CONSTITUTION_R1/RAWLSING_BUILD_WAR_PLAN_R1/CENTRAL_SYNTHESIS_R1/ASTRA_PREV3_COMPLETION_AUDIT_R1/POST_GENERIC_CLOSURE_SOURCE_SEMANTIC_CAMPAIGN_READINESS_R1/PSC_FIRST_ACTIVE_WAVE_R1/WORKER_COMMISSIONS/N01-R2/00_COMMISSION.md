# N01-R2 — CURRENT 18,276 IMPLEMENTATION DENOMINATOR / REPO CARRIER R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-psc-w1r2-n01-current-denominator-exact-carrier-r1`

Commission base / HQ authority: `aea759b8b4234081e6348b0adb721c3c3f345f1f`

Library: `REQUIRED_BUT_EXACTLY_BOUNDED_TO_THE_NAMED_CURRENT_CARRIER`

Exact grain: `PREV3_CURRENT_ACTIVE_IMPLEMENTATION_DENOMINATOR_AND_REPO_ENUMERABLE_IDENTITY_CARRIER_R2_ONLY`

## Governing inputs

Read current `HQ_HANDOFF/LATEST.json`, then read:

`PSC_FIRST_ACTIVE_WAVE_R1/03_W1_RETURN_JOIN_AND_CURRENT_CARRIER_RESOLUTION_R1.md`

The only Library object whose membership content is authorized by this commission is the exact accepted catalog bundle:

- accepted name `LAYER1_GOVERNED_35WAVE_CATALOGS.zip`;
- Library-visible duplicate may be named `layer1_governed_35wave_catalogs(1).zip`;
- exact SHA-256 `b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d`;
- exact byte size `5,257,954`.

Do not consume a same-name object unless the bytes hash exactly to that SHA-256.

## Mission

Mechanically project the accepted current catalog bundle into a repo-enumerable exact membership/identity carrier for all 18,276 current active implementations.

At minimum preserve for each member:

- exact `question_implementation_id`;
- exact source family;
- exact wave/release;
- exact source-variable/question identity fields present in the source catalog where needed for stable identification;
- exact source catalog member identity and content hash;
- source row ordinal or another deterministic exact row locator;
- exact identity hash when carried by the source row.

Sharding by family is encouraged. Do not emit one needlessly giant monolith if exact family shards plus manifest are cleaner.

## Required proof

PASS requires:

- exactly 18,276 projected rows;
- exactly 18,276 unique `question_implementation_id` values;
- zero duplicate IDs;
- exactly nine current families and 35 active wave/release scopes;
- family and wave counts reconcile exactly to the accepted carrier;
- every projected row is mechanically traceable to one exact row of one exact accepted source catalog;
- a deterministic validator/receipt proves the above from committed artifacts;
- no FQRA/QSR/R7G/700-row substitution.

The repo carrier is identity/membership infrastructure only. It creates no semantic, routing, applicability, response, structural, causal, topology, currentness, person or V3 authority.

`CATALOG_MEMBERSHIP_IDENTITY != SEMANTIC_AUTHORITY != ROUTING_AUTHORITY`

## Write scope

Write only under:

`.../PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N01-R2/`

plus narrowly necessary validator code/tests if required. Do not mutate existing authority carriers.

## Boundaries

PRE-V3 objective-world only. OBL063 person/driver/type terminal semantics remain quarantined. No automatic semantic interpretation. No provisional sibling output. MAIN, semantic PRE-MAIN and HQ control branch untouched.

Work through PASS or the smallest exact proved blocker, commit the governed return, and report final tip plus exact artifact hashes.