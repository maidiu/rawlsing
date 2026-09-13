# W4-F05 — bounded-evidence replay provenance collision repair return

Status: `PASS__EXACT_REPLAY_PROVENANCE_COLLISION_REPAIRED__NOT_INDEPENDENTLY_QUALIFIED`

Branch: `agent/rabochii-prev3-w4-f05-bounded-evidence-replay-repair-r1`

Commission/start tip: `abd63d4340d5c296d3ae483b98473a747e6b75db`

Executed grain: `PREV3_BOUNDED_EVIDENCE_REPLAY_PROVENANCE_COLLISION_REPAIR_R1_ONLY`

Exact repaired blocker:
`E07_BLOCKER__D07_RECEIPT_REPLAY_COLLISION__OMISSION_REASON_AND_SELECTED_INPUT_AUTHORITY_REFS_NOT_PROVENANCE_BEARING`

## Repair

The D07 receipt projection now makes both missing provenance dimensions canonical replay/hash-bearing material:

1. every unavailable required or optional input contributes its exact `(input_id, omission_reason)` association to `unavailable_input_omission_reasons`;
2. every selected empirical input contributes its exact `(input_id, authority_refs)` association to `selected_input_authority_refs`.

Both structures are emitted by `Receipt.as_dict()` and included in the receipt hash core. Input ordering remains canonical by `input_id`; `PolicyInput.authority_refs` remains canonicalized by the pre-existing sorted/deduplicated `ExactRef` tuple. Therefore input order or authority-ref order does not perturb identity, while changing an omission reason, changing a selected authority dependency, or swapping the same provenance values between different input identities changes the replay receipt/hash.

No decision-state law, claim ceiling, partial-loss law, alternate-source authority law, nonempirical-prior law, renormalization prohibition, or OC03/OC04/OC05 applicability posture was changed.

## Exact implementation identities

- production: `rawlsing_next/objective_consumer_bounded_evidence.py` — blob `f30fca20e7b56e00348e82765d95f974b4b6a195`
- targeted/regression test: `rawlsing_next/tests/test_objective_consumer_bounded_evidence_d07.py` — blob `75df736d118ffff7e8803606ca29e05047395ee9`
- inherited D07 harness, unchanged: `rawlsing_next/tests/d07_bounded_loss_harness.py` — blob `74a393f11d986e89a21d192495dc1bf985ace0e4`
- inherited E07 independent qualification script reused as a regression oracle: `.../THIRD_WAVE_WORKER_RETURNS/E07/02_INDEPENDENT_HOSTILE_QUALIFICATION.py` — blob `42823511fe532546ce24af77468c0eca4816f3a8`

## Courts executed

- inherited D07 bounded-loss harness: `12 PASS / 0 FAIL / 12 total`;
- targeted pytest file after repair: `6 passed`;
- inherited E07 qualification cases replayed against the repair: `7 PASS / 0 FAIL / 7 total`, including former collision probes E07-H02 and E07-H03;
- F05 targeted collision/canonicalization controls: `5 PASS / 0 FAIL / 5 total`.

The targeted controls prove:

- omission-reason change => different serialized receipt and hash;
- selected-input authority-ref change => different serialized receipt and hash;
- input/ref ordering only => identical canonical receipt and hash;
- authority values swapped between input identities => different receipt/hash;
- omission reasons swapped between unavailable input identities => different receipt/hash.

Exact run details and sample receipt identities are frozen in `02_COLLISION_AND_TAMPER_TEST_RESULTS.json`.

## PASS / successor gate

The commissioned repair grain **PASSES**. The proved replay collision is eliminated without weakening inherited bounded-evidence behavior.

This return is **not** an independent qualification of its own repair.

`SUCCESSOR_GATE = GATE-DEGRADED-REQUALIFICATION__OPEN_TO_SEPARATE_INDEPENDENT_WORKER_ONLY`

## Boundary confirmation

- MAIN mutated: `NO`
- PRE-MAIN mutated: `NO`
- library used: `NO`
- consumer scope broadened: `NO`
- decision semantics changed: `NO`
- OC03/OC04/OC05 promoted: `NO`
- omission treated as zero/false/default: `NO`
- quarantined OBL063 driver/type/person-terminal semantics revived: `NO`
- PRE-V3 objective-world boundary preserved: `YES`
