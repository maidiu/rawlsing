# B05 — LiTS Current Exact Local Oracle Producer Contract

Producer:

`python -m rawlsing_next.fiabc_final_oracle_freeze_producers produce-lits ...`

This command is intentionally local-source-capable but was not executed by this browser/GitHub worker.

## Governing path

The producer performs:

exact LiTS DTA SHA verification
→ existing `decode_dta(..., encoding="latin1")`
→ existing governed LiTS projection materializer
→ existing current LiTS runtime package/authority set
→ `build_source_backed_c11_repository()`
→ `CarrierNeutralResearchExecutor.execute_i05()`
→ exact constituent-I03 reruns through the T5 closure helper
→ observation-shaped current material
→ accepted ASTRA identity checks
→ `build_lits_i_oracle()`
→ inherited existing `freeze_oracle()`
→ `verify_frozen_oracle()`.

No `compose_p2r1_binding`, candidate provider, Candidate A/B/C process, candidate cache, or candidate root participates.

## Exact invariants

- source SHA: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows: 29002
- variables: 1198
- runtime catalog: `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`
- active binding: `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`
- runtime release: `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`
- candidates: 50
- query roles: 77
- accepted learned product: `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`
- accepted semantic replay: `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`

The historical ASTRA product and source/replay receipt are read by exact path from accepted commit `e631de162c582423639b7067a4f36b29f8aa4d89`; they are not substituted by new history.

## Required outputs surfaced in producer receipt

- `current_standardized_constituent_i03_fact_refs`
- `current_constituent_i03_closure_identity`
- `current_observation_shaped_exact_ref_manifest`

The oracle document itself is the existing standard schema `RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0`.

## Candidate-root law

The producer uses `WORK_ROOT/court/oracle_producers/LITS_I` for neutral temporary material and rejects source/oracle producer paths beneath `WORK_ROOT/cells`.
