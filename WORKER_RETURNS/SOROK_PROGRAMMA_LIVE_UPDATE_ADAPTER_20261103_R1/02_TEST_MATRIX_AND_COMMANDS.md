# LIVE-02 — adversarial test matrix, exact commands and evidence grades

## Test status

**S0–S1 private-GitHub source checks: PERFORMED. Python/pytest/S2: NOT_RUN.** The code and tests are committed for an authorized S2 runner. Nothing here is a pytest result. The commission references 62 original P0/P1 author tests at the repaired base; they were neither performed nor independently certified in this session.

### S2 runner preflight (must be observed, not inferred)

Use a clean local Git worktree at the branch SHA published in the terminal return. It must contain exact objects for `a9ebf71e` W8-R, `7bf2da30` JOIN-E, `4387dc81` JOIN-V, `b65c75a9` S35/P1, `598d9e9e` RRIF R2, and `8090a1ea` independent RED. Before testing:

```sh
git -C /path/to/rawlsing status --porcelain
git -C /path/to/rawlsing cat-file -t a9ebf71e62d84e5dcc599662e976eca7fcd0e623
git -C /path/to/rawlsing cat-file -t 7bf2da302996491ddf34b9a039fea47ac982d135
git -C /path/to/rawlsing cat-file -t 4387dc818a96fda2d5271672505fbd9da1059703
git -C /path/to/rawlsing cat-file -t b65c75a9e62618690f7d02265bc9e850af549161
git -C /path/to/rawlsing cat-file -t 598d9e9eaba5143950c63317705fd09104fbf463
git -C /path/to/rawlsing cat-file -t 8090a1ea308ab17f302f55bb2639c3e4cd774c7a
cd /path/to/rawlsing/SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q test_live_update_adapter.py
```

If any object is missing locally, fetch that exact commit from the authorized private origin, recheck its object/blob and rerun. **Never** silently fall back to a mutable branch tip or substitute a different review subject. Run the existing repaired engine regression suite (including `test_repair_r1.py` and `test_p0_trust_repair.py`) afterward; do not rename prior results as fresh execution.

### Exact temporary GENESIS / CLI cold readback

The first entry must have a canonical journal, not merely a stale `state.json`. From the above directory:

```sh
mkdir -p /tmp/sorok-live02/evidence
PYTHONDONTWRITEBYTECODE=1 python3 -c 'import living_reference as lr; from pathlib import Path; lr.commit_event(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}), journal_path=Path("/tmp/sorok-live02/evidence/journal.jsonl"), state_path=Path("/tmp/sorok-live02/state.json"))'
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json freshness
# Read the exact current journal_head from the JSON response. Replace HEAD_1:
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json intake fixtures/join_e_scoped_review.json --expected-head HEAD_1
# Read new current journal head from the intake output. Replace HEAD_2:
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json intake fixtures/s35_authored_sourcefree.json --expected-head HEAD_2
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json work-now
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json goal C9@INTEGRATE
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json focus C12@INTEGRATE
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json changes-since a9ebf71e62d84e5dcc599662e976eca7fcd0e623
python3 live_update_adapter.py --state /tmp/sorok-live02/state.json candidate-patch
python3 living_reference.py --state /tmp/sorok-live02/state.json verify-journal
```

These commands have been written/checked against the Python functions as text but **not executed here**. Inspect the real outputs and correct any sourcefree defect before requesting independent review.

## Adversarial sourcefree acceptance matrix (tests written, NOT_RUN)

| Scenario | Target test | Required result |
|---|---|---|
| Real JOIN-E scoped review → authored S35 intake | `test_real_join_e_then_s35_cold_replay_and_one_entry_work_now` | Two distinct exact receipt records; E021 at 7bf scoped; S35 attached to CAN011 source only, first consumer NONE, O05 still unissued; cold journal digest exactly equals rebuilt digest |
| Exact duplicate re-ingestion | `test_duplicate_event_idempotent_no_new_journal_or_state_revision` | No second event or revision; explicit idempotent return even with stale caller head for exactly same payload |
| Same ID, mutated content | `test_duplicate_transition_id_different_body_is_refused` | Reject collision without journal write |
| Order inversion | `test_exact_order_inversion_same_claims_not_different_science` | Same phase/membership/readiness grade after S35/JOIN order swap; chronological event audit retains different order |
| Missing overnight transition | `test_missing_transition_is_not_inferred` | Exactly zero changes after last event, no imaginary source ingestion, C9 mode unselected |
| Actual R2 independent RED after 7bf | `test_independent_negative_exact_cut_preserves_unrelated_join_acceptance` | 598d/8090 RED in C12 source view; E021 scoped 7bf remains present; C12 native/verify unissued |
| Forged source blob/altered SHA | `test_forgery_and_cross_cut_refusals_do_not_append` parameterized | Reject mismatched blob, guide cut, code SHA and review object before append |
| Ghost native rule or fabricated owner | same parameterized test | Reject `NATIVE`, `caller_verified`, wrong owner, positive selected Rule mode |
| Old review on new root | same parameterized test | Refuse c784/new-root reinterpretation of 7bf JOIN-V acceptance |
| Absent first reader | same parameterized test | Scoped positive review cannot claim verified first consumer without code symbol. S35 candidate may expressly declare NONE |
| Concurrent/stale CAS | `test_strict_cas_rejects_concurrent_writer_but_preserves_original_append_path` | Strict delta stale head refused without appending; original P0/P1 general append semantics unchanged |
| Positive learned practice false equivalence | `test_source_free_author_fixture_never_implies_positive_acquisition` | O05@ACCEPT not satisfied; G-C9-T-ANY MODE_UNSELECTED_HOLD, no native issuance |
| Existing qualified P0/P1 withdrawal and restore | `test_original_qualified_withdraw_restore_and_negative_independence` | Node-scoped source availability and downstream consumer recomputed while unrelated accepted 7bf source remains scoped; cold rebuild equal |
| Unqualified withdrawal | `test_existing_p0_p1_withdrawal_engine_is_reused_not_replaced` | Existing P0/P1 qualified-withdrawal requirement refuses caller-only transition |
| Attempted event-chain erasure | `test_unverified_event_erasure_of_delta_refused_and_replay_fail_closed` | Refuse a text-only HQ claim that tries to erase PROGRAMMA_DELTA event; direct low-level journal spoof cannot suppress source view |
| Real but unrelated Git blob | `test_unrelated_real_git_source_cannot_manufacture_node_claim` | Node must already be tied to same exact source_ref, not any real valid Git object |
| Fresh entering agent with zero new returns | `test_first_entry_without_new_delta_discloses_unprocessed_work` | Explicit historical-only state; cannot assume overnight work was imported |
| ALL/ANY/IF recursive no false readiness | Phase projection and above tests; inspect `G-C9-NATIVE-INTEGRATE`, `G-C9-T-ANY`, `G-A5-RUN-COMMON`, `G-C12-SF-VERIFY` | All same-target constraints preserved; inactive IF = MODE_UNSELECTED_HOLD; a single positive leaf does not complete multi-member target or override independent negative |

## Source-qualified facts already verified without running code

GitHub actually returned/verified the named JOIN-E return blob `9a185f7c...`, its `JoinedSession` source blob `dc089428...`, JOIN-V review blob `52dfc715...`, S35 source blob `02d65686...`, RRIF return blob `9d7eeb09...`, independent R2 review blob `38c20119...`, and P0/P1 base source files. W8-R at `a9ebf71...` carries the declared gate/seam member IDs. The returned PDF and product/person studies are not needed for this narrowly mechanical delta adapter.

## Qualification of test outcome

No author of LIVE-02 may write `PASS`, `INDEPENDENTLY_REVIEWED`, `OWNER_ADOPTED`, `NATIVE_C12` or `HUMAN_A5` merely because a test is declared or this GitHub commit exists. A qualified S2 run must record exact command, actual environment, test count, failures, sourcecut, and cold-rebuild effects. A **different** independent I3 reviewer must examine it at that exact returned implementation SHA. If any tests fail, make only the smallest sourcecut-correct repair within the allowlist; do not commission a new controller or rewrite the guide.
