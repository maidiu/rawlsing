# ASTRA-D10-R1 — RETURN

## Terminal disposition

**PASS** — the existing M10-M01 concrete candidate envelope is assembled at the authorized D10 grain and passes the governed deterministic replay court.

This return does **not** issue rule currentness and does **not** create an actor/world application fact.

## Exact return artifacts

- component/ref inventory: `WORKER_RETURNS/ASTRA-D10-R1/01_COMPONENT_REF_INVENTORY.json`
- concrete candidate envelope: `WORKER_RETURNS/ASTRA-D10-R1/02_M10_M01_CANDIDATE_ENVELOPE.py`
- governed validation/replay receipt: `WORKER_RETURNS/ASTRA-D10-R1/03_VALIDATION_AND_REPLAY_RECEIPT.json`
- typed residuals and successor wake: `WORKER_RETURNS/ASTRA-D10-R1/04_TYPED_RESIDUALS_AND_SUCCESSOR.json`
- replay test: `rawlsing_next/tests/test_astra_d10_r1_candidate_envelope.py`
- governed court spec: `.rabochii/court_spec.json`

## Assembled D10 state

The candidate is exactly the inherited M10-M01 rule body/shape/authority/trace/qualification-temporal-portability envelope, with the accepted D09 disposition preserved:

- value mode: `NONNUMERIC`
- calibration authority: `NOT_APPLICABLE`
- calibration N/A basis content hash: `0a72c9453ad55f1934f1e9953c3557a56893083ec32efb8e9a7fc03d0bb6244e`
- rule currentness: `CANDIDATE_NOT_CURRENT`
- current-selection evidence refs: empty
- noncurrent-disposition refs: empty
- rule-owner authority: `BOUND`
- causal-use authority: `BOUND`
- measurement / estimand / identification authorities: explicit accepted `NOT_APPLICABLE` dispositions
- mechanism class: `P1 MATERIAL_ACCESS_DEPENDENCY`

The deterministic D10 output refs are:

- candidate row content hash: `d8888ed404b68b5679f9742a77e3e12a9af0a6d397e227a826afa48fe3dc3115`
- batch content hash: `90ff2bf3edfe955ebfd113ae77a0e8f04ac19d9dd96a1e04d370e0ff4dbb2546`
- runtime binding content hash: `f4094d73cc2f6e0c3a40d5f5eb94e86a69d32863026cb1844c1d18b854fcf370`
- candidate receipt content hash: `ce4aefa2e59975556b30d1c906538179b450b5fb7965ba2b358823386f9c55bb`
- batch receipt content hash: `5b1af74948c14bce32bd64d0ddeed1a8e01f80f08a9590289f1cc0f14299991c`

The adapter result is `ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT`, with current-selection state `ELIGIBLE_FOR_SEPARATE_SELECTION`.

## Governed replay evidence

The first court run exposed only a missing execution-surface dependency: the branch did not contain the already accepted generic S03 adapter. No candidate semantics were changed to address that execution issue.

The exact previously accepted adapter was restored at:

`rawlsing_next/sdtf_r4_generic_batch_adapter.py`

Its Git blob is exactly:

`f6427a42524086194ed6fca9ba2387561ff00891`

which is the accepted repaired-T02 implementation blob from commit:

`f02336187e50a443d929ff7abbe5dcd5f3950f70`

The restoration commit is:

`be4439f927afcfad8ed6aacd9d897ca647c9617d`

The governed replay then passed:

- workflow: `Rabochii Governed Bounded Court`
- run: `35155030203`
- job: `104992333233`
- result: `PASS`
- court receipt artifact: `10470468717`
- artifact digest: `sha256:9592a1483af3022a08e0d33b8216d9960690da745531a41b5e572e2b46236471`
- semantic candidate SHA: `a8740b5ad80f288d2f9dcf6dcc4c89ba232d5b75`
- evidence execution SHA: `be4439f927afcfad8ed6aacd9d897ca647c9617d`
- determinism mode: `EXACT`
- Python: `3.12.14` / CPython
- court spec SHA-256: `d6e2db661c11d72e531acd039c29604946d20d8643ef63e1d922a9bb76b2b4bd`

The replay test checks repeat identity, all 28 determinant states, all six package states, explicit D09 calibration N/A, `CANDIDATE_NOT_CURRENT`, empty current-selection/noncurrent refs, accepted authority dispositions, and a governed-change sensitivity case that fails closed on altered row material.

## Hard ceilings preserved

No new M10-M01 rule semantics were designed. No new value-mode judgment was made. No numeric calibration was inferred. No `CURRENT_ACCEPTED` decision was issued. No current actor/world application fact, occupant, witness, topology, V3 person state, or OBL063 use was created. No A/B/C carrier work was performed.

`MAIN` was not modified. Semantic PRE-MAIN was not modified.

## Typed residuals

There is no D10 blocker. The remaining typed residuals are deliberately separate successor gates:

1. `INDEPENDENT_CONCRETE_ENVELOPE_QUALIFICATION_PENDING` — owned by ASTRA-D10Q.
2. `RULE_CURRENT_SELECTION_NOT_PERFORMED` — owned by ASTRA-D11 only after accepted D10Q PASS.
3. `ACTOR_ENTITY_REALIZATION_NOT_SUPPLIED` — outside the D10 grain and reserved to the later application/realization path.

None of these residuals negates the D10 PASS.

## Authorized successor wake

Immediate successor:

`ASTRA-D10Q — PSC06_EXACT_M10_M01_CONCRETE_RULE_ENVELOPE_INDEPENDENT_QUALIFICATION_ONLY`

D10Q has zero repair authority at that qualification grain.

Only after an accepted D10Q PASS, the inherited chain permits:

`ASTRA-D11 — PSC06_EXACT_COMPLETE_QUALIFIED_RULE_INDEPENDENT_CURRENT_SELECTION_ONLY`

D10 itself stops before that current-selection boundary.
