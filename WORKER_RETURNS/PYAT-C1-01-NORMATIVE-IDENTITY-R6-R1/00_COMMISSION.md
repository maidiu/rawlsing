# PYAT C1-01 — NORMATIVE SYNTHETIC IDENTITY COMPLETION R6 + SOURCE-FREE EXECUTION — R1

Status: ISSUED__USER_MEDIATED_CODEX_LAUNCH_REQUIRED

Role: Codex implementation/execution worker. Use strongest available reasoning model; GPT-5.6-class preferred.

Branch:
`agent/codex-pyat-hq132-c1-01-normative-identity-r6-r1`

Exact base:
`73346b423616e9c18b25b110009ba6c8bb14c268`

The exact R5 finding at this base is:
`PREIMAGE_UNDERDETERMINED__CONTRACT_CORRECTION_REQUIRED`.

HQ accepts that finding.

This commission does NOT attempt to recover the old four historical query/witness hashes.

It explicitly supersedes those underdetermined fixture-only identities by freezing a new complete source-free AT07 identity convention now.

No real-source semantic, comparability, survey, model or actor authority is created.

## Frozen production implementation

Do not edit:

`rawlsing_next/pre553_analytical_composition.py`

Exact frozen blob:
`5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`

Do not edit the public producer or consumer owners.

## HQ normative synthetic query convention

For both directions, use the already accepted AT07 universe, release, target, condition preimage, empirical coordinate, pairing AuthorityRef, producer query/predicate and pairing-ground-truth materials from the accepted C1 packet.

The following caller-defined fields are now frozen.

### Forward query

`query_id`:

`c1-at07-forward-position-p1-to-answer`

Query-level synthetic subject material:

```json
{
  "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
  "fixture_id": "AT07_BIDIRECTIONAL_100",
  "role": "FORWARD_POSITION_P1",
  "real_subject": false
}
```

Construct its ExactRef as:

- kind: `C1_SYNTHETIC_POSITIONED_SUBJECT@1`
- object_id: `urn:test:c1:at07:positioned-subject:forward-position-p1`
- content_hash: `semantic_hash(the exact material above)`

Forward `requested_projection`:

```json
{
  "kind": "C1_AT07_CONDITIONAL_DISTRIBUTION",
  "direction": "POSITION_P1_TO_ANSWER",
  "target_role": "ANSWER"
}
```

Forward conditioner `effective_time_or_interval`:
`null`

### Reverse query

`query_id`:

`c1-at07-reverse-answer-yes-to-position`

Query-level synthetic subject material:

```json
{
  "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
  "fixture_id": "AT07_BIDIRECTIONAL_100",
  "role": "REVERSE_ANSWER_YES",
  "real_subject": false
}
```

Construct its ExactRef as:

- kind: `C1_SYNTHETIC_POSITIONED_SUBJECT@1`
- object_id: `urn:test:c1:at07:positioned-subject:reverse-answer-yes`
- content_hash: `semantic_hash(the exact material above)`

Reverse `requested_projection`:

```json
{
  "kind": "C1_AT07_CONDITIONAL_DISTRIBUTION",
  "direction": "ANSWER_YES_TO_POSITION",
  "target_role": "POSITION"
}
```

Reverse conditioner `effective_time_or_interval`:
`null`

## HQ normative witness identity convention

Continue using witness kind:

`C1_CONDITION_VALUE_BINDING_WITNESS@2`

The exact witness identity material is now a CLOSED mapping containing exactly these 16 keys and no extras:

1. `consumer_query_ref`
2. `consumer_binding_material`
3. `consumer_binding_fingerprint`
4. `subject_condition_preimage_ref`
5. `subject_condition_preimage_material`
6. `producer_query_ref`
7. `producer_predicate_ref`
8. `producer_predicate_hash`
9. `producer_predicate_leaf_ref`
10. `producer_predicate_leaf_projection`
11. `pairing_ground_truth_ref`
12. `pairing_authority_ref`
13. `source_universe_ref`
14. `release_ref`
15. `effective_time_or_interval`
16. `binding_mode`

Populate those fields exactly from the actual accepted fixture objects and current owner material.

Specific normative rules:

- `consumer_query_ref := consumer_query.ref`
- `consumer_binding_material := canonicalize(binding.material())`
- `consumer_binding_fingerprint := semantic_hash(binding.material())`
- `producer_query_ref := actual empirical_query.ref`
- `producer_predicate_ref := actual predicate.ref`
- `producer_predicate_hash := actual predicate.predicate_hash`
- `effective_time_or_interval := null`
- `binding_mode := EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE`

Use the already accepted exact subject-condition, predicate-leaf, pairing-ground-truth and pairing-authority objects for each direction.

Witness object IDs:

Forward:
`urn:test:c1:at07:condition-value-witness:r6-forward-p1`

Reverse:
`urn:test:c1:at07:condition-value-witness:r6-reverse-yes`

Witness content hash:
`semantic_hash(exact closed 16-field identity material)`

## Supersession law

The following old hashes remain historical evidence of the underdetermined R2/R3 fixture and MUST NOT be reverse-engineered:

- old forward query:
  `83727ca59eaf43085324ee7dc7db5ce4ecf4e4bf1f1284692cd3ad3f192df027`
- old reverse query:
  `cb2d085675c137848bb40f191ba8992100513eaa904a09cd54064f6ef51d3d8a`
- old forward witness:
  `c93e840c06da9ab8de9ca237863d52858fe6765d5bfd7c7efb42b879440663c9`
- old reverse witness:
  `e81c4e19144a749877a6f6e7e48a213e869bfe5d04ba81372ca5384b7cf5e700`

Because evidence identity includes the witness ref, recompute new forward/reverse evidence identities honestly.

If new hashes differ from historical hashes, that is EXPECTED and must be recorded as explicit R6 supersession, not failure.

The arithmetic/projection semantics remain unchanged:

- forward = 54/60;
- reverse = 54/62;
- raw_support = exact producer denominator;
- same accepted source/release/target/risk/measure/provenance law;
- same noncircular evidence preimage schema;
- same value-bearing condition relation;
- same hostile fail-closed timing before evidence construction/consumer call.

## Exact write allowlist

You may edit/create only:

1. `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R6/**`
2. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md`
3. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json`
4. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/worker_return.json`
5. `rawlsing_next/tests/test_pre553_analytical_composition.py`
6. `WORKER_RETURNS/PYAT-C1-01-VERTICAL-SLICE-R3/**`

Do not modify production code.

## Required implementation/test completion

Update the active current C1 packet to identify R6 as the current fixture identity authority while preserving R2/R3/R4/R5 historical records.

Update the C1 analytical test so it:

1. constructs both normative R6 queries from the exact HQ values above;
2. recomputes both query refs;
3. constructs both exact closed witness materials from actual owner/fixture objects;
4. recomputes both witness refs;
5. executes the actual public empirical query producer;
6. calls the frozen banked C1 analytical adapter;
7. derives, rather than supplies, the evidence slice;
8. invokes the actual public positioned-subject possibility consumer;
9. verifies forward 54/60 and reverse 54/62;
10. verifies exact new R6 forward/reverse evidence refs;
11. verifies all mandatory C1-01 hostile cases;
12. verifies a mutation of the witness/relation determinant reidentifies or fails closed as specified;
13. verifies no preconstructed final slice input exists.

The test must not preserve the old red assertion that historical R5 preimages should exist.

## Execution

This task is routed to Codex because Browser workers have already demonstrated the relevant source-free pytest execution gap.

Do not access raw survey files.
Do not materialize raw survey files.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not run real-source C11 materialization.

Use an isolated source-free runtime.

Do not use the user's Mac unless the user explicitly authorizes that in the actual Codex conversation.

Run at minimum:

`python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

Record exact Python/dependency environment, commands and pass/fail/error/skip totals.

## Required returns

R6:
- `00_RETURN.md`
- `01_NORMATIVE_QUERY_MATERIALS.json`
- `02_NORMATIVE_WITNESS_MATERIALS.json`
- `03_SUPERSESSION_MAP.json`
- `04_EVIDENCE_RECOMPUTATION.json`
- `05_CONTRACT_INTEGRITY_RECEIPT.json`

C1-01 R3:
- `00_RETURN.md`
- `01_SCOPE_AND_DIFF.json`
- `02_AT07_EXECUTED_ASSERTION_MATRIX.json`
- `03_HOSTILE_EXECUTED_MATRIX.json`
- `04_EXECUTION_RECEIPT.json`
- `05_FINAL_DISPOSITION.json`

Allowed dispositions:

- `PASS_AT_R6_NORMATIVE_SOURCE_FREE_GRAIN`
- `PATCH_READY__EXECUTION_CAPABILITY_BLOCKED`
- `NORMATIVE_MATERIAL_INCOMPATIBLE_WITH_CURRENT_OWNER`
- `EXISTING_OWNER_CHANGE_REQUIRED`
- `COUNTEREXAMPLE_TO_R6_FREEZE`

Do not begin C1-02.

Terminal:
`C1_01_R6_NORMATIVE_COMPLETION_RETURNED__HQ_ADJUDICATION_REQUIRED`
