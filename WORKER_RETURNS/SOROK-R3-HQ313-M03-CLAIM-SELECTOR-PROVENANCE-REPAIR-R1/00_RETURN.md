# M03 — canonical claim selection and response-as-of repair

**Verdict: SOURCEFREE_CLAIM_PROVENANCE_REPAIR_CANDIDATE_ONLY.** Both unchanged M02 REDs now PASS. The final candidate passes all **513 literal tests** (M01/inherited 413 + M02 100), plus **74 new author controls**. The nine historical CAN3 REDs remain nine literal FAILs in a separate execution. No skips or errors enter those totals.

This is an implementation author return. This chat previously authored the M02 review; it is not independent acceptance of M03. HQ's distinct M04 science court remains required. No helper agents, model switches, external model calls, semantic issuance or production adoption were performed.

## Exact custody

The direct remote assigned branch tip was verified at sealed startup `92b9fa8b29f85ad77576da39a8765a666a5ab37f`. M01 candidate `02187a14e75ff30dd953d3c7185d689b80e62304`, its preregistration `845edf5d7c9c48b192b631dacf295afa6f587137`, M02 review `0216d9036a87e2f60f42fd5b2870556027808419` and expectation freeze `0c875790fd7341402d7eeee4a515ca67dc43ee65` are the input authorities. The adopted CAN008_R2, ADP016 and ADP017 blobs were read and verified; their imported fixture implementations were preserved.

The local sparse worktree uses the existing authenticated Git object store. Static sources were reused only after marker, checksum and actual file verification. Each test constructs actual synthetic native owner state in a fresh execution. There is no claim that mutable owner state survived from an earlier process, nor that a saved source-free receipt grants original actor/source custody.

All writes and changes from the seal are inside this assigned return. Original tests, frozen expectations, owner modules, adopted law, production registry, canonical control and respondent/source data are unchanged. The candidate is installed as an explicit source overlay at this return's original M01 runtime import location. No response monkeypatch or replacement oracle is used. [Exact source/import audit](07_SOURCE_AND_IMPORT_AUDIT.json) distinguishes patched source from pinned original blobs.

## Before and after

| Execution | Before implementation | Final candidate |
| --- | ---: | ---: |
| M01 literal controls | 94 PASS | 94 PASS |
| CAN3 inherited controls | 97 PASS | 97 PASS |
| CAN2 inherited controls | 89 PASS | 89 PASS |
| Relevant owner controls | 133 PASS | 133 PASS |
| M02 literal independent controls | 98 PASS / 2 RED | 100 PASS |
| New M03 author controls | — | 74 PASS |
| Historical CAN3 REDs, separate | historical nine | 9 FAIL |

Baseline evidence was completed and committed before candidate implementation (`77707a4ce789f497e67e6ad39cab68fe11505af1`). [All 513 literal case identities and outcomes](04_LITERAL_513_CASE_CLOSURE.json) match before and after. The two changed outcomes are:

- `test_checkpoint_claim_selector_cannot_downgrade_existing_belief_to_absence`: the prior unknown selector silently changed Ye REROUTE to AMPLIFY with identical owner state. It now refuses with `CLAIM_SELECTION_UNKNOWN`; no later event/read/history publication survives.
- `test_lawful_future_claim_cannot_condition_an_earlier_response`: the actual admitted January 20, 1999 event and native BELIEF transition still exist. Selecting that future claim for November 20, 1998 now refuses with `CLAIM_SELECTION_AFTER_RESPONSE`. The owner transition is not relabeled invalid merely because it cannot condition an earlier response.

Full portable stdout, JUnit, observations and function-source traces are in [before](evidence/before) and [after](evidence/after). Portable copies remove personal paths and hostname metadata; raw metadata remains only in ignored local runtime storage, with sanitization hashes recorded.

## Implemented boundary

`candidate/cell.py` retains the original response transfer function and native owner calls. The small overlay adds an explicit committed claim-selection binding, validated checkpoint restore, read-time provenance proof, helper source bytes in the existing rule grant, and exact internal rollback. [The diff](candidate/M01_TO_M03.patch) shows the M01 changes. `candidate/claim_provenance.py` implements the finite validator.

The first-event journal commitment binds the actual E1 event, permitted canonical claim, actor/world/as-of scope, owning rule identity and version/hash, actual first response receipt, response implementation source hash, first owner-state hash and journal-entry identity. The selected canonical claim is derived from the existing source contract, never from a requested later response. A rehashed outer selector/binding cannot substitute another source while leaving that actual first commitment intact.

Public restore checks the preserved commitment and reverts atomically on a malformed or mismatched binding. To preserve the literal M02 interface, an unknown outer selector hint can be restored in quarantine alongside the genuine binding. It is never trusted as absence: consumption resolves the actual selected claim and refuses an unknown, foreign, future or otherwise invalid selection before applying the response map.

Each read validates actual canonical claim, source emission, native effect/transition identities and authority, source parents, owning rule, current snapshot and current private permission at the response cut. Duplicate effects and stale permission material cannot be collapsed into an apparently lawful state. The read enforces the finite 1998–2000 rule scope and records actual effective times. The helper does not choose BUFFER/AMPLIFY/DEFLECT/REROUTE/BLOCK.

A genuine NONE arm remains lawful: the canonical E1 claim and its emission exist, with no applied stance, transition, state snapshot or private permission. It still produces Ye AMPLIFY. Native BELIEF addition, inaccessible supersession and withdrawal remain valid; the first-event commitment does not freeze the owner against legitimate later native operations.

This is integrity within the declared source-free checkpoint/event contract, not OS-resistant attestation or an independently issued production authority. A whole same-contract checkpoint can replay in a new Cell. A binding from a different first commit cannot be mixed into another checkpoint.

## Scientific preservation and counterexamples

The [36-arm comparison](05_FACTORIAL_AND_TEMPORAL_RECEIPTS.json) verifies the exact same actual owner-state bytes/hash, CAN008 history bytes, source events, Ym/Ye outputs and history delivery behavior before and after repair. The inherited factorial and the independent M02 factorial both execute. M02's stronger fixed-epistemic-state, same-memory-ID content intervention remains PASS; owner reads and native formations are observed in actual function traces.

[New author tests](repro/test_author.py) cover genuine NONE across twelve memory/history combinations; unknown/unhashable selectors; actual earlier and future alternative native claims; an unselected future claim that must not suppress legitimate NONE; thirteen source binding fields; first commit identity; missing/malformed binding; cross-cell mixing; lawful whole-checkpoint replay; coherent binding reissuance against the unchanged commitment; missing journal commit; five current permission corruptions; stale permission after native revision; native duplicate ADD; coherently altered effect material; invalid/earlier cuts; three valid read cuts; finite-scope overflow; actual helper-body mutation; native withdrawal; and failure-stage rollback.

The first author run found a real extra rollback failure (69 PASS / 1 FAIL). Calling public validated restore during transaction failure could reject the already corrupt pre-call receipt and retain E2 admission. Internal rollback now restores its own captured pre-call parts directly, preserving even quarantined corrupt metadata byte-for-byte while continuing to deny consumption. [The original failing evidence](evidence/author_initial_rollback_failure) remains; the unchanged counterexample and all final author cases pass. Preliminary passing runs are retained as interim evidence and excluded from final totals.

Three early harness/output-directory or XML-packaging faults are retained separately with correction receipts. They precede the clean baseline and are not scientific baseline outcomes. Source assertions and test expectations were not relaxed to fix them.

K3 access-unknown refusal and inaccessible BLOCK, K5 private/public noncollapse, source-body hash refusal, CAN3 history comparison and atomic rollback all remain covered by unchanged literal cases. The [admissibility/rollback audit](06_ADMISSIBILITY_AND_ROLLBACK.json) links typed denials to exact captured before/after checkpoints.

## Authority and return bounds

Production positive-authority registry blob `e0528d65215cb431196570c38bac4eae94217a1b` remains byte-identical and EMPTY. The separate historical replay executes only the original nine selected failing cases, not all CAN3 585, and does not invert their assertions.

Serial ADP016→ADP017 mediation remains **HOLD**. Actual finite parallel memory/epistemic-state conditioning is preserved; it establishes neither calibrated human psychology nor an operative actor-causal mechanism. Real competent issued production owner authority remains **HOLD**. No CURRENT/PRE-MAIN movement, V3 operation, source release or production adoption follows from this return.

[Reproduction instructions](08_REPRODUCTION.md), [executed totals](03_EXECUTED_RESULTS.json), [environment passport](environment_passport_delta.json) and [requirement audit](09_REQUIREMENT_AUDIT.md) accompany the candidate. The final direct remote verification is recorded after the return commit; this file cannot contain its own commit hash without changing that hash.
