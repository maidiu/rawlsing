# A08 — LMQ-010 COMPLETE QSR LOWER-LEVEL PRODUCER DEPENDENCY / REPLAY CLOSURE R1

Status: `PASS__LMQ010_COMPLETE_QSR_LOWER_LEVEL_PRODUCER_DEPENDENCY_AND_DESTRUCTIVE_REPLAY_CLOSED`

Repository: `maidiu/rawlsing`  
Worker branch: `agent/verkhovod-a08-lmq010-qsr-replay-r1`  
Mandated start: `0df921b4b45f8f6539cfabe498581ae66caf7206`

## Governing predecessor state

Authority 41 authorizes A08 specifically to close `LMQ-010`. Required predecessor Z03 final is `0c0e0704be91a5e19c9c524e3f29cd081495b721`. Z03 closed `LMQ-011` only at QSR carrier/manual-source-structure succession grain and left `LMQ-010` explicitly `OPEN_PARTIAL`, because complete lower-level primary-source/audit dependency identity plus destructive replay had not been proved. A08 consumes that exact open debt and does not reopen the already-closed succession court.

## Holding

`LMQ-010` closes at the exact QSR lower-level producer/replay grain. The recovered 18,792-row Register C carrier is no longer supported only by carrier checksum/manual-core succession: a fresh QSR was generated in a destructive replay tree from the recovered canonical audit-owner boundary and exact historical builder inputs, with the reference QSR absent from the production input set. The reference was opened only after generation for parity comparison.

Fresh output and current recovered carrier are byte-identical:

- rows: `18,792`
- columns: `69`
- fresh SHA-256: `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219`
- reference SHA-256: `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219`
- differing rows: `0`
- differing cells: `0`
- ordered row-identity root: `ac9f897b782f467e777f881e8d251d6f3b85a0dd0acdfc0c6f6482bd356e8569`

The replay also preserves the historically unresolved/review surface rather than laundering it away:

- `needs_manual_review=yes`: `562` rows
- `source_structure_review_required=true`: `937` rows
- `source_structure_classification=unknown`: `377` rows

## Complete replay producer boundary

Six exact core inputs were hash-verified before execution:

| Producer | SHA-256 |
|---|---|
| `build_question_structure_register.py` | `3cabb94b84e7e498cfc56c4d579d58047744ef545faae2e03586a7d5f0856175` |
| `ddm_v550_source_structure.py` | `609a02e1615ba3c028d284b5f11e198df1eda26e53bae2a0b50d6609d749a0e0` |
| `ddm_survey_identity.py` | `18333b59b82f8faef7459b873f819e2cf4a38312bdd0ec68b1cdc7c172297158` |
| `source_structure_validation_manifest.csv` | `7e9899151530740517f0b2e054164ff9a761dc8c2fae4bb8fcc32728ac34344e` |
| `question_type_taxonomy.yaml` | `3612c6b400008467471b71cc38d811b8c5349bac0617e974a72e76e584e86b27` |
| `questions_master_drivers.csv` (`d62`) | `d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011` |

The declared CLOSED_35 producer census contains exactly `35/35` canonical audit CSVs and exactly `18,792` audit rows. Every audit byte hash is preserved in `QSR_PRODUCER_DEPENDENCY_LEDGER.csv` / `QSR_REPLAY_DEPENDENCY_MANIFEST.json`; every one also carries the recovered primary-source file SHA lineage. Asian Barometer W6 is explicitly excluded.

The historical validation manifest was not semantically edited for replay. Only its audit transport paths were rewritten into the fresh temporary tree; all non-path cells were mechanically checked identical. The deterministic replay transport-manifest SHA-256 is `74d7c9fbd43bf9cd207806cc5a387908278e7a85ce9b241fc458ddf69b982bd2`.

## Executed proof

`DESTRUCTIVE_REPLAY_RECEIPT.json` records the real replay. `qsr_lower_level_replay.py` is the reusable fail-closed verifier. It verifies all producer hashes and CLOSED_35 identities, stages only declared producers, requires the reference carrier only after generation, and fails on output parity drift.

Focused hostile tests: `6/6 PASS`. They cover missing producers, producer hash mutation, excluded Asian Barometer W6 contamination, semantic manifest mutation during transport rewrite, reference-carrier tampering, and exact 35-producer census acceptance.

## Negative ceiling

This closure is deliberately narrower than several adjacent authorities:

- `CURRENT_QSR_IS_REFERENCE_ONLY_AND_MUST_NOT_BE_A_REPLAY_INPUT`.
- Primary-source hashes establish lineage behind all 35 audit owners; A08 does **not** claim a fresh raw-source→audit re-execution.
- Mechanical consumption of `d62` reproduces the historical builder result; it does **not** convert `d62` into blanket semantic authority or re-adjudicate its mixed assertion-grain history.
- Audit/QSR structure does **not** create routing authority.
- A08 does not reopen `LMQ-011`, does not perform `LMQ-013`, and does not adjudicate product-wide V550J/routing debts.

## Disposition

`LMQ-010 = CLOSED__EXACT_35_AUDIT_PRODUCERS_AND_PRIMARY_SOURCE_HASH_LINEAGE_RECOVERED__DESTRUCTIVE_QSR_REPLAY_BYTE_PARITY_PROVED`

Terminal: `A08_LMQ010_QSR_REPLAY_R1_COMPLETE`
