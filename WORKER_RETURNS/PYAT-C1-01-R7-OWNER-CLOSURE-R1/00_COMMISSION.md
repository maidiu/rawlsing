# PYAT C1-01 — R7 CLOSED-WITNESS OWNER + PACKET + HOSTILE COURT CLOSURE — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Browser/GitHub implementation + documentary correction worker, GPT-5.6 Sol High

Branch:
`agent/rabochii-pyat-hq135-c1-01-r7-owner-closure-r1`

Exact base:
`458f839845fc149874e5a64af5eda41bbd52c4e1`

This base contains:
- the R6 normative fixture patch at `663379caa7c9b8a80bca889d8d5b59d0486ff901`;
- the independent R6 review return at this exact head;
- no accepted C1-01 execution qualification.

Read first:
`WORKER_RETURNS/PYAT-C1-01-R6-INDEPENDENT-REVIEW-R1/00_REVIEW.md`
and all four associated review artifacts.

The governing review disposition is:
`ESCALATE_WITH_COUNTEREXAMPLE`.

HQ accepts that counterexample and authorizes exactly the bounded owner repair described below.

## Mission

Close only the three defects identified by the R6 independent review:

1. enforce the already-frozen CLOSED 16-key witness law in the existing analytical adapter;
2. serialize the complete literal R7/R6-equivalent 16-field witness preimages and immutable dependency locators so future readers never need to rediscover them from tests/implementation;
3. restore the missing mandatory hostile/reidentification tests.

Do not broaden C1 semantics.
Do not begin C1-02.
Do not change the R6 normative caller-defined query fields.
Do not change the accepted forward/reverse arithmetic.
Do not create real-source authority.

## Exact owner repair authorized

File:
`rawlsing_next/pre553_analytical_composition.py`

Current accepted/banked R6 production blob before repair:
`5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`

The only production-owner semantic repair authorized is inside `_verify_witness(...)`:

Current law is effectively:
`required.issubset(identity)`

Replace that permissive check with exact key-set equality enforcing:

`set(identity) == required`

The witness identity material must contain exactly the already-frozen 16 keys and no extras.

Use a typed fail-closed `ConditionValueRelationMismatch` message for either missing or extra keys.

Do not alter:
- the 16-key set itself;
- field comparison semantics;
- witness hashing law;
- producer/consumer APIs;
- evidence construction;
- arithmetic;
- source/release/risk/measure/provenance behavior.

No other production code edit is authorized unless this exact repair is mechanically impossible. If another owner change appears necessary, stop and return `EXISTING_OWNER_CHANGE_REQUIRED` with the exact reason.

## Full witness preimage freeze

Repair:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R6/02_NORMATIVE_WITNESS_MATERIALS.json`

or, if historical R6 packet immutability within this branch would be clearer, create an R7 correction packet and update the active C1 packet to point to it. Do not rewrite historical R2/R3/R4/R5 evidence.

The current governing packet after your return MUST serialize, literally, for both forward and reverse:

- exact full CLOSED 16-key `identity_material`;
- witness_ref;
- consumer query ref;
- consumer binding material;
- consumer binding fingerprint;
- subject condition preimage ref/material;
- producer query ref;
- producer predicate ref/hash;
- producer predicate leaf ref/projection;
- pairing ground-truth ref;
- pairing authority ref;
- source universe ref;
- release ref;
- effective_time_or_interval = null;
- binding_mode.

Also freeze immutable dependency locators sufficient to reconstruct and audit those materials without test-code archaeology.

At minimum bind these accepted dependencies by exact path + blob:

1. R2 value relation oracle:
   path:
   `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json`
   blob:
   `c6acafae820c065215fdbe7a703480a8b19fbc57`

2. R2 synthetic authority freeze:
   path:
   `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json`
   blob:
   `333989fa7b57c221d6aa5ebfc25d9d76e0acad32`

3. R3 evidence identity preimage:
   path:
   `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/04_EVIDENCE_IDENTITY_PREIMAGE.json`
   blob:
   `1d1e9eddeebf7e1f26189355dc06e71bf70a367f`

Preserve the independently recomputed current R6 identities unless the exact CLOSED-key owner repair itself lawfully changes them (it should not):

- forward query:
  `8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`
- reverse query:
  `2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`
- forward witness:
  `f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`
- reverse witness:
  `a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`
- forward evidence:
  `c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`
- reverse evidence:
  `0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

If any of these change, stop and return the exact counterexample rather than silently superseding them.

## Mandatory test restoration

File:
`rawlsing_next/tests/test_pre553_analytical_composition.py`

Retain all existing R6 positive and hostile coverage.

Add/restore exact tests for:

### H1 — CLOSED 16-key no extras

Take an otherwise-valid current witness identity material.

Add a 17th field.

Recompute a matching witness ref/hash for the 17-key map.

The adapter MUST reject it because the identity key set is not exactly the frozen 16-key set.

This test must prove the exact owner counterexample is closed; a stale-hash failure is not sufficient.

### H2 — AT19 valid determinant reidentification

Create a newly identified, internally valid mutation of the relation/witness determinant while holding unrelated determinants fixed as far as the frozen contract requires.

Prove:
- the mutated witness has a newly valid identity;
- the composed direct result identity reidentifies;
- unrelated producer/source/release/risk/measure/target/model determinants remain unchanged.

Do not satisfy AT19 merely by creating an invalid stale-ref witness that fails closed.

### H3 — denominator-member identity hostile

Change an exact denominator member while preserving the same visible 54/60 arithmetic.

Prove the evidence identity changes.

### H4 — geometry-cell identity hostile

Change an exact geometry cell determinant.

Prove the evidence identity changes.

### H5 — relation/pairing-authority identity hostile

Change the fixture-only pairing/comparability authority through the lawful witness/provenance/authority material.

Prove evidence/composed identity reidentifies as required.

Do not create or infer real-source comparability authority.

## Exact write allowlist

You may edit/create only:

1. `rawlsing_next/pre553_analytical_composition.py`
2. `rawlsing_next/tests/test_pre553_analytical_composition.py`
3. `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R6/02_NORMATIVE_WITNESS_MATERIALS.json`
4. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md`
5. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json`
6. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/worker_return.json`
7. `WORKER_RETURNS/PYAT-C1-01-VERTICAL-SLICE-R4/**`
8. `WORKER_RETURNS/PYAT-C1-01-R7-OWNER-CLOSURE-R1/**`

If you decide historical clarity requires a dedicated R7 contract-correction directory, you may additionally create:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R7/**`
but do not mutate R2/R3/R4/R5.

No other files.

## Source-free execution

Browser runtime may be absent. Do not fake execution.

If an exact repository pytest runtime is available, run:

`python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

If unavailable, return patch-ready and explicitly state that execution remains required.

The previous execution attempt at:
`a92f977e9ce4615326b09ad9e3407b3b02684788`
returned:
`BLOCKED_EXECUTION_CAPABILITY`

because its isolated runtime could not materialize an exact Git worktree.

Do not repeat that absence proof at length; just record whether this worker had a competent exact runtime.

## Prohibitions

Do not access or materialize raw survey files.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not run real-source C11.
Do not create semantic/comparability/model/actor authority.
Do not begin C1-02.

## Required returns

Under:
`WORKER_RETURNS/PYAT-C1-01-R7-OWNER-CLOSURE-R1/**`

Required:

- `00_RETURN.md`
- `01_SCOPE_AND_OWNER_DIFF.json`
- `02_FULL_WITNESS_PREIMAGE_AUDIT.json`
- `03_HOSTILE_COURT_MATRIX.json`
- `04_EXECUTION_STATUS.json`
- `05_FINAL_DISPOSITION.json`

Allowed dispositions:

- `PATCH_READY__REVIEW_AND_EXECUTION_REQUIRED`
- `PASS_SOURCE_FREE_IF_EXECUTION_ACTUALLY_RUN`
- `EXISTING_OWNER_CHANGE_REQUIRED`
- `COUNTEREXAMPLE_TO_R7_CLOSURE`

Terminal:

`C1_01_R7_OWNER_CLOSURE_RETURNED__HQ_ADJUDICATION_REQUIRED`
