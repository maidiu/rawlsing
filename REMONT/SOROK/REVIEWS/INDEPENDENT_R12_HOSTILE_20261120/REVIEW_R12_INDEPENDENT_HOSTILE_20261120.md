# SOROK REMONT #1199 — independent hostile R12 receiving

**Verdict: `REVISE_EXACT_DEFECT`** for exact immutable candidate `9db0e6f64bf568409e638ff2215af8b8a414487f` (PR #1199, draft/unmerged). **This review is independently executed by a distinct assistant session on exact code, but uses the same connected GitHub principal (`maidiu`), is not credential-independent G5, and does not accredit the original P070/P071 source patch whose earlier reviewer was its author.**

## Specific first fault — project reorganization bypasses trial-before-motive

R12's `um_sorok_organism/development.py::admit` (source Git blob `64b11e6d719d45ecb3e2ebb9a6be77a9cee532fe`) refuses `ADD_PROJECT` and a same-end `TAKE_UP_POSSIBLE_END` during an `issued_trial`; the sibling `REORGANIZE_PROJECT` ingress is not covered. `_admit_in_place` subsequently accepts `REORGANIZE_PROJECT` fields `object`, `motive`, and `priority` without checking that the very same runtime-issued trial is not being promoted into an established durable motive. The existing project's `origin` preserves its earlier event, falsely implying the mature rewritten motive has earlier provenance; its `history` does record the current event, so the contradiction is visible but not prohibited.

Actual connected reproducer in `TEST_R12_HOSTILE_RECEIVING_NEW.py`:

1. Initialize one world and Nadia, age by `background(280)`; create an unrelated durable family-routine project through an actual earlier **nontrial WAIT event** and typed `ADD_PROJECT` admission.
2. In a **different** actual SING event, allow the sourcefree heuristic to produce a provisional possible end.
3. Immediately choose the runtime-issued *SING trial ID*, not an externally injected operation, through a callback.
4. In the corresponding **same-event development callback**, propose `REORGANIZE_PROJECT` addressed to the preexisting project's real ID, replacing `object` with the current possible end and `motive` with `MATURE_END_FROM_THIS_TRIAL` and priority 15.
5. On frozen R12 the step **succeeds and commits**. The existing project now has a promoted mature trial motive while its end remains `POSSIBLE_NOT_ACQUIRED_MOTIVE` and the event chain verifies `valid=True`. The hostile test requires rejection and no world-clock/actor mutation, so it correctly fails: `AssertionError: InvalidDevelopment not raised`.

This is not a forged event, malformed actor, hostile in-process direct mutation, invented project ID, nor an invalid `ADD_PROJECT` candidate. It uses the live callback and actual issued trial in R12's own functional path.

**Minimal bounded repair:** in `development.admit`, for current runtime `issued_trial`, prohibit `REORGANIZE_PROJECT` writes to durable purpose-defining `object` or `motive` (and examine `status`/`priority` promotion claims) as well as `ADD_PROJECT`, without forbidding ordinary separate-event reorganization or actor-owned valid trial history. More generally enforce purpose-genesis provenance for *every* semantically equivalent project ingress, not merely the explicit new-project kind. A sibling R11 repair #1198 already attempted the object/motive route, but it was not inherited by R12; adapt with independent inspection rather than claiming unreviewed branch is accepted.

## Independent execution and custody

Source ZIP: ChatGPT Library `/Rawlsing/SOROK-REMONT/REMONTATHON_R12_20261120/SOROK_REMONT_R12_INDEPENDENT_REVIEW_REPAIRS_246_TESTS.zip`; local independently checked SHA-256 `2aeb7fc0075124ce0107bf48087ed1bb2b967cb52846135a18559ac00b83b460`.

- Frozen recovered suite using **Python 3.13.5**: normal unittest `246/246 PASS`, `python -O` `246/246 PASS`, `python -m pytest` `246 passed + 14 subtests`. These results are **this review's local execution**, separate from reported Python 3.11.3 clean-worktree PASS (PR #1199 comment `7051205213`), which this review did not repeat.
- Independently added six test functions: **five PASS, one substantive RED**, normal and optimized. Combined suite `252 tests = 251 PASS, 1 FAIL` normal, `251 PASS / 1 FAIL` optimized, `python -m pytest` **251 passed, 1 failed + 20 subtests**. All logs preserved in this review packet.
- The independent five passing tests cover (a) canonical stored world/actor byte and singleton world-roster rejection (P070); (b) NaN, positive and negative infinity sensor rejection (P071); (c) current trial's `ADD_PROJECT` rollback; (d) legitimate trial's actor-owned history with no motive promotion; (e) a nontrial separate-event project reorganization. Passing these first-fault probes **does not accredit P070/P071 source-science or any native owner**.
- Independently computed 42/42 Python file byte size, SHA-256 and Git blob SHA-1 exact matches to the R12 manifest; independently compared all 42 blob identities with the actual immutable #1199 GitHub tree. No missing or extra Python files in the two target subtrees.
- Original #1171 source-register `REMONT/SOROK/OPEN_DEFECTS.json` `c0b7cd0589a7aa0ca5bd9f53c42f07ab03933ef7`: **all 71 P records byte-semantically identical in ordered serialized JSON** to R12. 53 original scoped first-fault independent review fields unchanged; T=0; E=6. R12 adds only its R12 candidate metadata key, not a novel register. P070/P071 remain author-repaired / independent review pending. Remaining eight OPEN, eight PARTIAL retained.

## Receiving boundaries

No sourcefree whole-person scientific acceptance, native P2–P6/CAN/ADP/PFF or PYAT source legitimacy, external LLM validation, credential-independent G5, or protected merge. The exact code was read and tests were executed independently of the author evidence; test source remains distinct. Any formal `APPROVE` or `REQUEST_CHANGES` from the same authenticated GitHub account must not be represented as credential-independent review. Use a `COMMENT` review and preserve the explicit `REVISE_EXACT_DEFECT` verdict.

**Shortest next operation:** repair purpose-reorganization route in source owner; add this six-function review module unchanged to repaired test court; prove RED→GREEN with source/clock/actor-world rollback and both positive branches under normal/-O/pytest; reacquire fresh immutable HEAD review by a different reviewer for the repaired R12 cut. P070/P071 need a nonauthor reviewer. Protected PROGRAMMA and paired CURRENT_PROGRESS should only be updated through competent authorized receiving; `HQ_CURRENTNESS_HOLD` pending writer/receiving authority.
