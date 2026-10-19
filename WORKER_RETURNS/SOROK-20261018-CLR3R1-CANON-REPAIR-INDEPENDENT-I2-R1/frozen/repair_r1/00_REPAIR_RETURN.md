# CLR3 — user-authorized repair of the two new I2 REDs

**Both frozen independent counterexamples now pass against the repair candidate.** This follow-up is author repair and executable regression evidence, not independent acceptance of these changes or native adoption.

Authorization: the user's follow-up, “okay, can you fix them please”, after the explanation of I2-F01 and I2-F02. This authorizes a bounded sourcefree repair inside the existing reviewer return. Original CLR3 at `4076dcc7c944723b8eea449c0753e535b79d1aa5`, the independent review at `0a5da3542f9bb5dd442a2cc1bd605d8958388f13`, their evidence, all frozen tests, accepted laws, PRE-MAIN, source branch and current actor remain unchanged.

The repaired implementation is `candidate/recursive_court.py`. It is a copy of the reviewed wrapper with an explicit import-path binding to the unchanged 65-file legacy closure. The patch changes validation and commit ordering only; numerical evolution, coefficients, event selection, probability policy, narrative grammar and native-owner HOLD are preserved.

## I2-F01: cross-entry canon consistency

Before accepting a new realization, the ledger compares it with already admitted realizations at the same clock in the same research-world ledger:

- The same lock ID must have the same physical location.
- For the same focal actor/time, the father-presence account must agree.

Conflicts raise `CANON_OBJECT_LOCATION_CONFLICT` or `CANON_ACTOR_FACT_CONFLICT`. `verify()` also checks these invariants over retained entries. Validation completes before either the source-preimage map or canon list changes. A refusal reserves no source ID, so a corrected compatible retry can succeed without rewriting earlier entries.

Compatible same-time particulars and alternative wording remain legal. Separate counterfactual-world ledgers may select different locations. A later observation does not retroactively replace an earlier location: both immutable records remain, with their own clocks and exact references. This bounded observation check does not create a general movement/correction authority or a native world-history consistency engine.

## I2-F02: encounter-source consistency

The repair chooses the small **ingress consistency-check** option rather than asserting a newly authenticated producer. Before admission, and on later verification, the source must consistently bind the existing fixture's:

- Boolean father-presence flag;
- presence or absence of exactly one `actual-shared-attention` selected event;
- that event's existing `relationship` kind and `care` offer;
- available-time/presence account when the optional material-response record is supplied.

An inconsistent account raises `SOURCE_ENCOUNTER_MISMATCH` before any canon/source write. Both false-to-true and true-to-false contradictions are exercised. Duplicate attention records, altered event kind, removed care offer and contradictory material time refuse as well. The material threshold is the original fixture's unchanged `>=10` predicate, not a new psychological coefficient or issued rule.

This fixes the reported contradiction between the narration's presence claim and the recorded encounter. It does not independently recompute every possible numerical transition, certify arbitrary producer data, authenticate an issuer, or validate human parenting/uptake. Those stronger claims remain outside this repair.

## Executed verification

| Suite | PASS | RED | Errors | Skips |
|---|---:|---:|---:|---:|
| Original unchanged CLR3 suite, bound to repaired wrapper | 38 | 0 | 0 | 0 |
| All six unchanged independent probes, bound to repaired wrapper | 6 | 0 | 0 | 0 |
| Additional repair controls | 11 | 0 | 0 | 0 |
| Original six historical assertions, on their frozen harness | 0 | 6 | 0 | 0 |

**55 PASS, six original REDs retained.** Before repair, the copied wrapper with only its source-path binding changed reproduced the same two independent REDs; `evidence/before_repair.*` retains that baseline. No expectation was edited, skipped or marked xfail. The explicit pytest plugin verifies that candidate tests import `repair_r1/candidate/recursive_court.py`; passing tests against the old wrapper are not misrepresented as repaired execution.

All four complete valid trajectory records remain equal to the published CLR3 JSON, including numerical snapshots, draws, canon records, later task and whole-trace hashes. Three workplace trajectories also replay identically in four cold processes with hash seeds 0, 1, 71 and 123. Every observed legacy import stays in the unchanged frozen closure and matches its recorded SHA-256. The complete previous review's file hashes are checked before and after testing.

The runner exits **1 deliberately** because it includes the preserved six-RED historical court. Actual per-suite exit codes, commands, logs and parseable JUnit are in `evidence/`. An initial runner failed while sanitizing paths into XML with angle-bracket placeholders; XML-safe placeholders fixed that packaging problem. The isolated historical court also required its frozen harness directory on its own Python path. Both harness diagnostics are retained; neither fix changed candidate behavior or test expectations.

## Remaining boundaries

The archive-container mismatch, the historical-admission limit on 49 extra dependencies, all six original RED dispositions and all native-owner implementation/grant holds remain unchanged. No production mathematics, native psychology, CAN008/CAN011/ADP issuance, B3/M2 integration, actor use or migration was performed.

HQ owns a distinct review/adoption decision for this repaired candidate. The same agent's repair tests do not constitute independent acceptance of its own changes. The earlier independent review remains a frozen historical result; this additive repair packet records the changed candidate and its evidence separately. Publication uses the existing commissioned branch, ordinary non-force push and direct remote SHA readback.
