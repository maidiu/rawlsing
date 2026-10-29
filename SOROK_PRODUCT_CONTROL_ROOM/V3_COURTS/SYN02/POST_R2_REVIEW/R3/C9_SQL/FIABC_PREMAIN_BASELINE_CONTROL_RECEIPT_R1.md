# PRE-MAIN FIABC original-court baseline comparison — independently executed GitHub Actions

**Evidence run:** [40799996204](https://github.com/maidiu/rawlsing/actions/runs/40799996204). **Source execution head:** `5989fe083c67da27f4366968199e18792c24c74b` PR #514. **PRE-MAIN exact base:** `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.

This is a negative baseline/attribution proof, **not a positive FIABC acceptance** and not permission to change any Pyat/FIABC oracle or preflight binding. Original `.rabochii/court_spec.json`, Python 3.11, and `rawlsing_next.rabochii_bounded_court` are used for both revisions, with identical checkout directory, test environment and Python process model. The ephemeral CI runner first executed the staged C9 PR HEAD, detached to the exact PRE-MAIN base SHA, and executed the same court again. Git sourcefetch credentials were read-only as in existing governed CI; an earlier attempt without original Git fetch capability caused broad spurious errors and is **excluded from acceptance**.

| Comparison | Candidate C9 staging | Unchanged PRE-MAIN baseline |
|---|---:|---:|
| Total original FIABC pytest tests | 147 | 147 |
| PASS | 144 | 144 |
| FAIL | 3 | 3 |
| ERROR/SKIP | 0 | 0 |
| Identical named RED test nodes and failure summaries | YES | YES |
| Bounded court result | FAIL | FAIL |
| DIAGNOSTIC comparison CI result | PASS equality | PASS equality |

**Exactly the same three preexisting REDs in both cuts:**
1. `rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope` — existing sourcebacked Darwin stage backend blob expectation `b655d8b8...` versus `1bb84723...`.
2. `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state` — candidate-C binding blob expectation `c2451b1b...` versus `47893688...`.
3. `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law` — same candidate-C binding identity conflict.

The **C9 import/recovery PR did not cause these three named failures**, because those failures also reproduce unchanged on exact PRE-MAIN under the same execution method. Their resolution belongs to the competent Pyat/FIABC original source/authority and PRE-MAIN currentness owners, not a Sorok C9 repair agent. The currently failing *global* Rabochii Governed Bounded Court must remain RED, and the independently green C9 sourcefree workflows must not be used as substitutes for that project's own acceptance.

**Proof ceiling:** individual C9 tests, source SHA preconditions and C12 versioned negatives are independently supported elsewhere, but there is still no original CAN/ADP/Pyat native Rule A/T/C11, no performed native E2, no whole-person A0–A5 release and no active production writer. This comparison only adjudicates **regression attribution**, never scientific correctness or original source admissibility.
