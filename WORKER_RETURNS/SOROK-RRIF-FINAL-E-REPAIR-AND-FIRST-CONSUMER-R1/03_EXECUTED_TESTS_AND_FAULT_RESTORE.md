# RRIF-E — executed tests, fault/restore and cold replay

## Commands and real results

All commands used local S2 Python 3.11.3, pytest 9.1.1, SQLite and a real Git
worktree. R2/R3 suites were run in separate processes to preserve their vendored
import closure.

| Court | Command | Result |
|---|---|---|
| R2 original | `PYTHONPATH="$R2:$REPO" python3 -m pytest -o addopts='' -q -p no:cacheprovider "$R2/tests/test_join.py" "$R2/tests/test_rrif_r2_c12.py"` | **20 passed** in 11.83 s |
| R3 extension | `PYTHONPATH="$R2:$R2/rrif_r3_extension:$REPO" python3 -m pytest ... "$R2/rrif_r3_extension/tests/test_rrif_r3_extension.py"` | **9 passed** in 7.73 s |
| RRIF-E repair | same, `"$R2/tests/test_rrif_e_repair.py"` | **6 passed** in 3.47 s |
| Receiving patch | clean R2 base copy + `patch -p1` + R2/repair tests | **26 passed** in 14.52 s |
| First consumer | `python3 first_consumer_cli.py --root ...` | exit 0; receipt written |

Evidence:

- `candidate/evidence/court_results.json`
- `candidate/evidence/r2_original_20.xml`
- `candidate/evidence/r3_extension_9.xml`
- `candidate/evidence/rrif_e_repair_6.xml`
- `candidate/evidence/first_consumer_receipt.json`
- `candidate/receiving_packet/PATCH_APPLY_TEST.md`

## T1 fault/restore

`test_repaired_independent_c12_verifier_green_intact_red_tamper_restore`:

1. intact root: vendored verifier RED (`episode:0/1:body_hash_mismatch`), repaired
   verifier GREEN;
2. forged episode body: repaired verifier RED with `body_hash_mismatch`;
3. exact DB byte restore: repaired verifier GREEN.

The original vendored failure is preserved as a known source defect, not
rewritten or hidden.

## C1 coordinated tamper/restore

`test_coordinated_column_branch_and_perception_tamper_is_guarded_red_then_restore`:

- rewrite episode body `branch_id`, recompute body/column hash, and change a
  perception `actor_id` in raw SQLite;
- `QualifiedC12Store` remains GREEN;
- `GuardedC12Store` RED with branch-origin and actor-membership errors;
- classification `SELF_HASH_ONLY__TRUST_CUSTODY_HOLD`;
- external owner anchor `OWNER_ANCHOR_REQUIRED`;
- exact SQLite restore -> both GREEN, no authenticity claim.

## Same-root first consumer

`run_first_consumer` executed:

```text
JoinedSession.start(perform="omit")
  -> SHARE_TOOL material event / C9 target
  -> say RECIPROCATE / do_help HELP_ACCEPT / attend NO_CHANGE
  -> wait(30) clock 40
  -> fork alt / close
  -> JoinedSession.open cold / return_session scene open
  -> repaired C12 root+alt GREEN
  -> R3 C12 cold read root GREEN
  -> C9 actor C9_SOURCE_MISSING
  -> legacy first_session LEGACY_HELD
  -> separate CP-A5 PASS RETAIN_TOOL, market UNKNOWN, ask UNKNOWN
```

The exact receipt is `candidate/evidence/first_consumer_receipt.json`.

## Original negatives preserved

Not rerun in this bounded commission and not repaired by implication:

- C9 R3B 14 passed / 1 failed;
- BP4R 7 passed / 2 failed;
- B3 ghost writes, F1CI3, G17I, CAN3 9, OC5E 49, M04 unjournaled ADP017;
- original F1CR patched bytes absent;
- original V3 ZIP container mismatch;
- R6/R7 source-present/unadopted exceptions.

These remain owner/court evidence and are not converted into green by this
packet.

## NOT_RUN

- 294/97 historical inventory, new branch census, Programma/Pyat work.
- Native source/actor, CAN/ADP/SCI05, C11, human A5, provider calls.
- Production DB, PRE-MAIN merge, PR or other-worker worktree mutation.
- Independent hostile review of this exact return.
