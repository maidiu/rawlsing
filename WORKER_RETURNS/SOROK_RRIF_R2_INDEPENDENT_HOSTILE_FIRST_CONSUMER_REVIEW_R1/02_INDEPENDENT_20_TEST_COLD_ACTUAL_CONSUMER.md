# Independent 20-test rerun, cold first consumer and raw persistence inspection

Subject: `598d9e9eaba5143950c63317705fd09104fbf463` (content commit `1745fbb68dddfe150e93eb7789a02c4c0768bd66`).
Clean detached worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-r2-review` at the subject SHA, `git status --porcelain` empty before and after the test run.

## 1. Harness and model verification

Actual process argv observed with `ps`:

```text
opencode run --dir /Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-rrif-r2-real-code-independent-hostile-first-consumer-20261031 --model opencode-go/deepseek-v4.1-flash --variant max --agent build --title SOROK RRIF R2 independent hostile first consumer --auto --format json ...
```

Actual session row in `/Users/matthewsmith/.local/share/opencode/opencode.db`:

```json
{"id":"ses_e6c2f579affee1zDyF5CBUoD76","title":"SOROK RRIF R2 independent hostile first consumer","directory":"/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-rrif-r2-real-code-independent-hostile-first-consumer-20261031","version":"1.18.34","agent":"build","model":"{\"id\":\"deepseek-v4.1-flash\",\"providerID\":\"opencode-go\",\"variant\":\"max\"}"}
```

Result: `MAX` is actually active (`variant: max` in both argv and session DB row). No provider/model/host/account/editor switch or effort reduction occurred. No provider model call was made during this review.

## 2. Environment actually used

```text
host              mainMac.lan
OS                macOS 13.2.1 (Darwin 22.6.0) x86_64
Python            3.11.3 at /usr/local/bin/python3
pytest            9.0.2
Git               2.43.0
SQLite            3.39.5
OpenCode          1.18.34
timezone          EDT; run timestamp 2026-10-31T17:16:08-04:00
```

The author's receipt reported `oldMac.lan`, Python 3.11.3, pytest 9.1.1, git 2.39.1 and 28.60s. The independent host/toolchain differs; the observed test result did not.

## 3. Exact test command and result

```sh
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-r2-review
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2:$PWD" \
python3 -m pytest -o addopts='' -q -p no:cacheprovider \
  SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/tests/test_join.py \
  SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/tests/test_rrif_r2_c12.py \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-r2-review-evidence/independent_junit.xml
```

Actual stdout tail:

```text
....................                                                     [100%]
20 passed in 11.26s
```

Actual JUnit root:

```text
testsuite name="pytest" errors="0" failures="0" skipped="0" tests="20" time="11.256"
timestamp="2026-10-31T17:16:08.369243-04:00" hostname="mainMac.lan"
```

Exit code 0. `git status --porcelain` after the run was empty; no RRIF source was edited.

## 4. The 20 exact tests and outcomes

All PASS, in the independent clean worktree:

| # | Test |
|---|---|
| 1 | `test_import_closure_is_explicit_and_matches_source_manifest` |
| 2 | `test_material_omission_vs_e2_changes_help_without_patch` |
| 3 | `test_full_encounter_positive_and_cold_reentry` |
| 4 | `test_b_refusal_is_typed_no_target_and_does_not_manufacture_target` |
| 5 | `test_attention_excludes_actor_decision_and_preserves_occurrence` |
| 6 | `test_private_state_and_actor_ignorance_do_not_cross_surface` |
| 7 | `test_refusal_disagreement_departure_and_no_contact` |
| 8 | `test_cold_reopen_is_nonmutating_and_fork_diverges` |
| 9 | `test_c9_target_consumer_severance_cold_red_restore` |
| 10 | `test_cli_start_status_help_verify` |
| 11 | `test_b_source_edge_help_observable_and_targetless_no_target` |
| 12 | `test_foreign_and_r29p_roots_are_refused_without_donor_mutation` |
| 13 | `test_coordinated_sidecar_and_meta_source_substitution_rejected` |
| 14 | `test_branch_lineage_required_and_legitimate_fork_reopens` |
| 15 | `test_missing_orphan_and_relocated_roots_are_typed` |
| 16 | `test_targetless_provenance_lineage_and_fork` |
| 17 | `test_nested_forks_receipts_parent_isolation_and_tamper` |
| 18 | `test_fork_post_create_receipt_failure_rolls_back` |
| 19 | `test_c12_episode_preimage_tamper_is_detected_and_restores` |
| 20 | `test_independent_c12_verifier_rejects_forged_episode_hash` |

Tests 1–18 are copied JOIN-E tests with path adaptation; tests 19–20 are the only new R2 test logic. Test 20 is materially weak: see `03_C12_C9_B_SOURCE_TAMPER_AND_RESTORE.json`, section `verifier_comparison`.

## 5. Actual cold first consumer (separate processes, real SQLite)

All CLI commands were separate `python3 -m joined.cli` processes with `PYTHONPATH` set to the candidate + clean worktree. No in-process echo of author JSON was used as evidence.

### omit path

```text
start --perform omit   exit 0  source b_operation=SHARE_TOOL; b_event_hash=16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486; target=e86c98e3d813f7a4cb3f027d302796bb8ae4cc55d73b24431562b8b29e5dd7b1
status                 exit 0  scene_open=true; native=false; material_performance=omit
help                   exit 0  accepted=true; strategy=HELP_ACCEPT; tools_remaining=1 in source facts
wait --hours 30        exit 0  clock=40; scene_open=false
leave                  exit 0  NO_CHANGE
offscreen --hours 30   exit 0  clock=70; message=null (no contact granted)
return                 exit 0  NO_CHANGE; surface "You are already through the portal." (cold process opened and verified the state)
verify                 exit 0  session.ok=true; root.ok=true; closure.ok=true; manifest.ok=true (444 files)
```

The "You came back" cold surface was independently reproduced by `test_full_encounter_positive_and_cold_reentry` (PASS) in a legal contact-granted flow; the separate-process `return` above truthfully returned its NO_CHANGE terminal surface instead.

### e2 path

```text
start --perform e2     exit 0  source b_operation=SHARE_TOOL; target=fdd5a35255e3ebef48e76dca5227f71656b02b823e49cd5cb906233670cfffa4
help                   exit 0  accepted=false; strategy=HELP_REFUSE; fact MATERIAL_PRESSURE
status                 exit 0  material_performance=e2; native=false; scene_open=true
verify                 exit 0  session.ok=true; root.ok=true; closure.ok=true; manifest.ok=true
fork --branch alt      exit 0  alt created from first_session; fork_clock=70; root_hash=15ef9a01bc5b0ea76045dccae55ae52a2d9d7aa0f4c0779b62b9d984eed0feb2
say (cold alt process) exit 0  strategy=RECALL_WORK; clock=70
status (cold alt)      exit 0  branch_id=alt; native=false
```

### targetless refusal path

```text
RefusalSession.start  source b_operation=REFUSE_TOOL; target_id=""; targetless=true
do_help               accepted=false; strategy=HELP_REFUSE
probe c9              target_branch=NO_CHANGE; target_reason=NO_PROPOSAL; material_reason=NO_ELIGIBLE_MATERIAL_SOURCE
probe e1/e2           adp019_admission_receipt=ADP019_ADMISSION_RECEIPT_ABSENT; later_read_status=STATE_ABSENT
cold RefusalSession.open  verify.ok=true; do_help accepted=false
```

The refusal path does not manufacture a C9 target, E2 practice or native grant.

## 6. Independent raw persistence inspection

I did not trust `verify` JSON. I connected directly to the returned `product/c12.sqlite` with SQLite, read the rows, and recomputed the stored preimages.

After the actual CLI flow:

| DB fact | omit | e2 |
|---|---|---|
| counts by branch | root: ep 2/world 1/perc 2/ckpt 4; first_session: ep 18/world 8/perc 18/ckpt 16 | root: ep 2/world 1/perc 3/ckpt 4; first_session: ep 6/world 4/perc 10/ckpt 8 |
| actor A `tools_remaining` in latest checkpoint | 1 | 0 |
| C12 `GM01_SOURCE` = session meta = bp2 sidecar | true | true |
| `grade` in session meta | `TEST_ONLY_SOURCEFREE_NOT_NATIVE` | `TEST_ONLY_SOURCEFREE_NOT_NATIVE` |
| CLI status `native` | false | false |
| source `native` | false | false |

Recomputed from raw rows (episode/world_event/checkpoint):

```text
omit  episode 20/20 self-consistent; world_event 9/9; checkpoint 20/20; perception 20 rows (no hash column)
e2    episode  8/8  self-consistent; world_event 6/6; checkpoint 12/12; perception 13 rows (no hash column)
```

The `perception` table has no `hash` column; `QualifiedC12Store.verify` checks only contiguous `seq`. A direct update of perception `actor_id`, `clock` and `channel` leaves `verify` green (see 03). No external anchor is used by the CLI.

## 7. Tests NOT run

The two-file command above did not execute:

- 24 vendored `test_*.py` files, including `vendor/j/tests/test_r31j.py`, `vendor/e/tests/test_r31e_expression.py`, `vendor/e/vendor/r30a/tests/test_r30a_first_session.py`, R29P/R29M tests and the nested BP2/BP4 test suites;
- any C9 R3B original 14/1 court, C9C12-R2 6/6 court, BP4R 7/2 diagnostics, CP-A5, B-F1CR or V3CORE suite;
- any native C4/ADP/CAN008/CAN011/SCI05/Pyat N11/N12/C11 path, original survey/respondent data, production C9/C12 anchor/KMS/mirror/outbox, human A5 or PREMAIN merge;
- any provider/model/network call or browser.

The 20/20 result is a scoped sourcefree local test result, not native acceptance.

## 8. First-consumer conclusion

The actual first consumer is `joined.cli` / `JoinedSession.start/open` over `R31J -> BP3/C8 -> C9 -> R29P/R26E C12 -> R31E -> joined`; it reads the intended J/E source closure (`audit_loaded` green; J/E/LIVE class checks green). It is runnable and cold-reopenable. It is **not** promoted native: every status, checkpoint and C12 row carries TEST_ONLY/sourcefree/native=false grades.

The material obsolescence/repackaging finding is in `01_MANIFEST_ORIGINAL_JOIN_AND_NEW_DELTA.json`: production code is byte-identical JOIN-E; only `tests/test_rrif_r2_c12.py` is genuinely new logic.
