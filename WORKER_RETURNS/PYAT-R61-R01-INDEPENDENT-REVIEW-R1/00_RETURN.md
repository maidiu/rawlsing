# R01V independent review return — REVISE

**Verdict: `REVISE`.** Finite, evidence-backed. Not `ACCEPT_SCOPED_LOCAL`.
No source/science/adoption claim. The author's code and tests were not edited.

## Exact review target and separation

- Candidate/startup: `fcf9fe9f8662c9e98801e670d0d4357072d8d453` (matches
  `.r61/launch.json` `startup`).
- Code commit: `d6f41177b16711ec721a9782c9797131295db2b5`; base
  `a54893657ba65e44c1049f763208b0b4b6ed5eb9`.
- Author branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`, remote head
  `fcf9fe9f8662c9e98801e670d0d4357072d8d453` before this review.
- Reviewer branch/worktree:
  `agent/opencode-pyat-r61-r01v-independent-review-r1` at
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v`.
- Author session `ses_e98c905cbffekusoHURfKyEUKG` is distinct from this reviewer
  session. Same provider account (`opencode-go/deepseek-v4.1-flash`,
  variant max, existing Global account) is disclosed; this is not organizational
  scientific independence. Browser runtime remains unqualified.
- Changed-path check: candidate diff from base contains only the four R01
  allowlist files (`types.py`, `enumerate.py`, `native_map.py`,
  `test_universal_grammar.py`), the sealed commissions/INPUTS, and the author
  return. No unlisted code path. Manifest artifact SHA256s match the returned
  files; `manifest.json` explicitly excludes itself.
- EXPECTATIONS.md was committed (`acdf5fa66`) before any candidate
  implementation/report inspection.

## What was independently reached (actual consumer)

1. **Author suite replay with reviewer JUnit and actual imports:** exit `0`,
   `11 passed`, `0 failures/0 errors/0 skips`, 6.55 s. Log/JUnit:
   `replay/author_suite.log`, `replay/author_suite_junit.xml`.
2. **Own independent frontier oracle:** 20 collected probes, 10 pass / 10 fail.
   Exit `1` (the 10 failures are the contract defects below). JUnit/log:
   `replay/independent_probes_junit.xml`, `replay/independent_probes.log`.
3. Hand-computed ordered-pair oracle matched: 4 ordered target tuples x 5
   ordered condition tuples = 20 exact `(targets, conditions)` identities for
   J=2/K=1; all 13 ordered K=2 condition tuples over two int domains matched;
   order is semantic, not a set alias.
4. Duplicate qualified occurrence refused; `NOT_ADMINISTERED` held;
   administration `UNKNOWN` retained; administrative role prohibited; complete
   admin-only inventory = valid empty (`e_pre_count=0`, root present) versus
   incomplete inventory = `e_pre=None` with cause.
5. Budget `3` leaves the full operation set/E_pre intact and yields exact
   pending ids; bounds unchanged. Partition flattening and cold subprocess
   recomputation reproduce the same content hash, partition root, operation ids,
   disposition counts and pending ids. There is no serialized restore ingress
   (NOT_REACHED; see defects D14).
6. Count-preserving substitution is rejected by `conservation_report`.
7. Direction/role order is an explicit grant; reverse direction is prohibited
   until granted. Form/repeat keys remain distinct. Risk-set and measure-kind
   changes alter `op_id`.
8. **Actual I05 consumer reached:** real
   `execute_exact_bounded_discovery` with synthetic C11/I03 objects produced six
   supported rule receipts; baseline `native_receipt_anti_join` passed. A
   condition-atom semantic mutation that preserved `rule_id` still passed the
   anti-join (`no_drop_ok=True`) — see D6. This is mapping-level evidence only;
   it is not R03 issuance or original science.

## Blocking defects (full exact inputs in `defects.md`)

| ID | Defect | Probe |
|---|---|---|
| D1 | Bool and explicit-null condition domains rejected | `test_DEFECT_bool_condition_domain_is_representable`; `test_DEFECT_explicit_null_condition_value_is_representable` |
| D2 | Operation identity does not bind source wave/edition/digest | `test_DEFECT_operation_identity_binds_source_edition_and_digest` |
| D3 | Operation identity does not bind estimand/weight/design/variance | `test_DEFECT_operation_identity_binds_estimand_weight_and_design` |
| D4 | Operation type cannot represent clocks/currentness | `test_DEFECT_operation_type_carries_clocks_and_currentness` |
| D5 | Eligibility/execution/result axes collapsed into one enum | `test_DEFECT_eligibility_execution_result_axes_are_separate` |
| D6 | Receipt anti-join checks only `rule_id`/count, not condition semantics | `test_DEFECT_native_receipt_antijoin_binds_conditions_not_just_rule_id` |
| D7 | `LoweringRecord` lacks required R03 contract fields | `test_DEFECT_lowering_record_has_required_contract_fields` |
| D8 | Native target cells coerce int/bool to string (`1` and `"1"` collide) | `test_DEFECT_native_target_cells_preserve_typed_int_vs_string` |

Blocking reason: these prevent exact K conservation into the native boundary and
prevent R03 from relying on the compiler as a complete, typed, cold-stable
frontier. R03 must remain **not started** until a repaired R01 is independently
re-qualified. D9-D16 in `defects.md` are medium/low or declared-limitation
candidates and do not by themselves define the verdict.

## Actual consumer and NOT_REACHED edges

- **Reached:** G50-style symbolic enumeration and disposition ledger; exact
  ordered identity checks; conservation anti-join; partition/budget; cold
  recomputation; actual I05 `DiscoveryResultReceipt` rule-id anti-join for six
  selected rules.
- **NOT_REACHED:** R02 row/occasion projection or physical source-row
  permutation (only occurrence-tuple order was permuted); R03 total native
  workload/`IssueWorkloadRecord`/U43 admission; direct C11/I03/Route B/Batch
  construction or replay/dedup; full recursion/baseline enumeration; serialized
  cold restore; all 35/1,890 original obligations; original `U/E_pre`; F6/F7/F8;
  N11/N12; production/protected CI; J52/W52; Browser runtime.
- Seven selected author mappings do not define the independent oracle and do not
  establish full native R03 execution. The reviewer's six-rule I05 probe is also
  mapping-level only.

## Evidence index

- `EXPECTATIONS.md` — frozen independent oracle/falsifiers, committed first.
- `defects.md` — exact inputs, observed/required, contract links, rank.
- `probes/test_r01v_independent.py` — disposable independent probes.
- `replay/author_suite_junit.xml`, `replay/author_suite.log` — reviewer replay.
- `replay/independent_probes_junit.xml`, `replay/independent_probes.log` — own
  probes/outcomes.
- `proof_witness.json` — commands, exits, mutants, imports, limits.
- `evidence/startup_and_identity.txt` — startup/remote/allowlist/manifest/import
  blobs and versions.
- `evidence/junit_summary.txt` — JUnit counts and per-probe status.
- `evidence/remote_readback.txt` — non-force push/readback record.
- `SHA256manifest.json` — hashes of all report artifacts except itself.
- `RESUME.md` — exact reproduction commands.

## Boundary and disposition

This is a reviewer qualification only. It does not repair the candidate, adopt
it, issue source permission, original `U/E_pre`, empirical support, science,
N11/N12, production/CI, F6/F7/F8, or restart J52/W52. R03 remains conditional on
independently qualified R01 plus accepted R02. The author must not treat this
return as self-adoption; a fresh candidate repair requires its own independent
review.
