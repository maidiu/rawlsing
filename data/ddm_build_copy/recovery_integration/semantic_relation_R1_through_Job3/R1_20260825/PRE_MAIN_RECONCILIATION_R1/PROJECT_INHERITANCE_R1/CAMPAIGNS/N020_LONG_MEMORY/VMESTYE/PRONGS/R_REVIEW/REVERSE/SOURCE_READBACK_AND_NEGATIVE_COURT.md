# ZL-17 R1 — source readback, no-drop and false-green test ledger

## Immutable inputs
- Protected `256d46bf425cc37e114465cddbe3c60e535766ab`, base tree `2010d5a7e7d4cab4ef265a4e63e6b3f759598a39` verified via GitHub Branch API at dispatch.
- Candidate [PR #864](https://github.com/maidiu/rawlsing/pull/864) `6be7a62535f12e83628018b1942767371e842cac`, 37 changed files, draft and unmerged at read.
- Independent receiving [#813 R5](https://github.com/maidiu/rawlsing/issues/813) [PR #859](https://github.com/maidiu/rawlsing/pull/859) `449a97480dfa5c9f7f2042d688fe1ed1869ffe91`; the 13-prong SOURCE_PROOF_RECEIPTS.tsv was read from candidate R2, not treated as native truth.
- Direct Git blob SHA set:
  - FUNCTION_ATLAS `98df0d9642a3c3f5fa1ecbf7a9cf7251e32b9fa0`
  - RELATIONS `3a4d51819858e51d4abc1d9431b56c0727540e8e`
  - OPERATION_TRACES `4e903c2f3bc5ecae1b73c20982f30c27499af79d`
  - AUTHORITY_APPLICATIONS `cf6a61c30f60c0fbb450454d7933ca3a1aedabae`
  - EVIDENCE `c401cd18ebed7fec2d712e3798a092cf56f20607`
  - IMPLEMENTATIONS `d8caad082b23cef140a145abe144c7bdaea5b3bc`
  - CONSUMER_EDGES `03529cf44ff30aeb843e05651483c887b1be1309`
  - DECISION_EVENTS `377cd8a5d63caf4e7d0ce5e3dcad6a23da0608c0`
- Source G4 82 `CURRENT_SEAM_STATES.jsonl` at protected `256d46bf425cc37e114465cddbe3c60e535766ab` blob `5a951626c0dde91b682eb23216c88dbfc054808d`; Sorok W7 E001/E014 cut `37915a47ed3e33a71ad8334c0aa505f5d65796ca` blob `d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47`.

## Exact independent S0–S1 operations
1. Used GitHub Git blob readback for all eight canonical data tables; parsed literal TSV headers, direct IDs and row bodies in memory. Row counts and relation kinds reported in `00_RETURN.md`. These checks do not rerun ZL15's entire builder or native tests.
2. Parsed 82 source JSONL seams. Compared all 82 to source-specific records in candidate EVIDENCE and checked the RELATIONS applicability field has zero literal IF conditions. The accompanying `SOURCE_AUTHORITY_CONSUMER_PROVENANCE_EDGES.tsv` preserves **82 distinct** seam edge IDs from source, not 82 inferred executable graph edges.
3. Built exact ID sets from the normalized tables for consumer/producer/evidence references; counted valid target joins vs sentinels. Counts and important exceptions in R17-D02..D04.
4. Independently opened protected N10E producer, analytical composition imports, N10W progressive path, N9 publisher/missing import target, legacy F03 authority application and Sorok W7 E001/E014 historical source rows. No external test call or native authority issuance.
5. Repeated 8 terminal-first cold readings, each with a named stop/falsifier in `BACKWARD_TRACE_SAMPLES.tsv`. Old function F03 and Sorok E014 negatives remain specific; synthetic/requested replay not claimed to have been executed.

## Falsifier / negative probes for author repair (NOT EXECUTED by this S0–S1 review)
| Probe | Minimal perturbation | Required outcome |
| --- | --- | --- |
| N1 | Flip applicability of `ASTRA:IF:N0:N4:0` without changing the edge IDs | Reverse graph changes conditional obligation, does not count IF as MUST |
| N2 | Keep `ASTRA:REQ:N10W:N11` source while changing one F-gate conditional predicate | MUST remains independent; only IF/functional-IF branch changes |
| N3 | Match Sorok `C11@INTEGRATE` by text to Pyat empirical `C11` | Reject false first-reader join; E001 still owner-held |
| N4 | Supply F03 `row=None` status with all five QUC guards true vs one false | Preserve six coordinates in all-true case; clear on false; no invented current run |
| N5 | Supply E014 positive actor despite `BLOCKED_NAMED_AUTHORITY_REQUIRED` | Refuse positive actor; preserve scoped negative-only |
| N6 | Call absent N9 `prev3_objective_position_materializer` at same sourcecut | Preserve bounded import defect, do not generalize to all N9 absence |
| N7 | Strip a specific `negative_evidence_id` or `AUTHORITY_APPLICATIONS.evidence_ids` exact J-EV | Reference validator rejects or explicitly types missing; no generic marker green |
| N8 | Remove producer→composition ID link while keeping all labels/hashes | Bidirectional cold-use navigation fails despite intact source identity |

## Honesty of run grade
- **Direct source/doc/TSV/JSONL reading:** PERFORMED S0–S1; deterministic in-memory reference checks performed.
- **Project test runner, CI, controlled real source mutation, original respondent S2/S3, native N11/N12 or Sorok C11 import:** NOT_RUN. The negative probes above are **specified falsifiers**, not claimed passed tests.
- **First non-test reader verified:** ZERO by this reviewer; existing protected sourcefree callsite examples are S1 code/currentness and inherited bounded test receipts, not authorized native original35.
- **Authority/actor/source rights:** NOT_GRANTED. Protected branch and ZL15 branch untouched. No independent PR APPROVE or merge.
- **Receiving:** `REVISE`; four explicit bounded integrator repairs; same reviewer may cold-check corrected exact HEAD later.
