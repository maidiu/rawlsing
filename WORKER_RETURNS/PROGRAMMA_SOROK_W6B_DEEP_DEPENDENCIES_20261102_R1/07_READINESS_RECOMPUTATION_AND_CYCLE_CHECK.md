# W6-B — reproducible dependency readiness, one-leaf change and cycle check

**Scope and source cut:** This is an in-memory **documentary graph calculation** over `05_EXECUTION_GATES_AND_READY_WORK_PACKAGES.jsonl` on this isolated W6-B branch, inheriting W5 `e3d5c77f455f6d53c8078c1c706c12f9a9ee4bde` and its 08 `E008/E021/D-C9/D-C12` cases. It is **not** a native code test, review or scientific issuance. Gates and work packages are nonadopted candidate guide additions. Requirements are attached to `target_id@stage`, not an undifferentiated component.

## 1. Exact deterministic evaluation procedure

For each `GATE` in 05, read `member_requirements[]` as `{source_id,required_stage,required_scope,ref}`; a member is true **only** where an `EVIDENCE_LEAF` for exactly that `ref` says `SATISFIED_AT_SCOPED_CUT` and the requested scope is no stronger than the evidence. A `SOURCEFREE_AUTHOR_REPORTED__NOT_NATIVE` member can only use a corresponding sourcefree author leaf; `JOIN_E_7BF_INDEPENDENT_SCOPED_ONLY` can use ONLY the exact independently scoped 7bf source. Source/knowledge presence, unreviewed PASS, an old accepted cut, owner grant and human participant proof are not interchangeable.

A gate with `ALL_OF` is ready to perform its target action when **all of its prerequisites are already satisfied**; `ANY_OF` when a legitimate alternative is satisfied. An `IF` gate participates only when its declared `predicate` is selected; **unselected IF does not create a blocker or a global waiver**. Satisfying the gate's *prerequisites* makes the corresponding task READY; **it does not automatically mark the target `@stage` completed**. A qualified new worker/owner receipt must first be attached to that exact target@stage and source/claim scope. If an unsatisfied member has its own gates, recurse; otherwise terminate in exact SOURCE_UNKNOWN, OWNER_HELD, or first actionable package. Same-stage mutual gates must be SCC-reduced before claiming executable status.

A work package reports `READY_TO_SPECIFY`, `READY_NOW_SOURCEFREE_SCOPED`, `READY_NOW_SOURCE_REUSE_RESEARCH`, `BLOCKED_UPSTREAM`, `OWNER_ACTION_READY_FOR_REQUEST_NOT_GRANT` or `IF_SCOPE_NOT_SELECTED` according to its gate prerequisites, phase and owner; these are *advisory readiness* categories, never adopted work authorization. Special SCC package `WP-W6B-06` is `JOINT_WAITING_ON_MATRIX` until a verified `E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY` receipt exists; after that it becomes `JOINT_READY_AFTER_MATRIX` **to resolve the joint C9/C12 contract**, not to mark either contract specified.

Implementation can reproduce this with a static JSONL parser, stage+scope exact-key lookups, reverse references and Tarjan/Kosaraju; no server/controller required. The calculation here traversed the retrieved records directly, not a manual guess. **No durations/owner capacity exist to calculate a measured critical path.**

## 2. Frozen-cut results and the real first work

At the retrieved branch cut: **97 evidence leaves, 77 gates and 39 work packages**; their evidence stages are explicit. The statuses below are computed, not completion findings.

**Native C12**: WP-W6B-01 `READY_TO_SPECIFY`; WP-W6B-02 `READY_NOW_SOURCEFREE_SCOPED`; WP-W6B-03 `READY_TO_SPECIFY`; WP-W6B-04 `READY_TO_SPECIFY`; WP-W6B-05 `READY_TO_SPECIFY`; WP-W6B-08 `READY_TO_SPECIFY`; WP-W6B-09 `OWNER_ACTION_READY_FOR_REQUEST_NOT_GRANT`; WP-W6B-10 `READY_TO_SPECIFY`; WP-W6B-11 `READY_TO_SPECIFY`; WP-W6B-24 `BLOCKED_UPSTREAM`.

**Early A5 and human**: WP-W6B-14 `READY_TO_SPECIFY`; WP-W6B-17 `READY_TO_SPECIFY`; WP-W6B-18 `READY_TO_SPECIFY`; WP-W6B-37 `READY_TO_SPECIFY`; WP-W6B-19 `BLOCKED_UPSTREAM`; WP-W6B-25 `BLOCKED_UPSTREAM`.

**Independently feasible**: WP-W6B-12 `READY_TO_SPECIFY`; WP-W6B-13 `READY_TO_SPECIFY`; WP-W6B-16 `READY_TO_SPECIFY`; WP-W6B-15 `READY_TO_SPECIFY`; WP-W6B-22 `READY_NOW_SOURCE_REUSE_RESEARCH`; WP-W6B-33 `READY_TO_SPECIFY`; WP-W6B-34 `READY_TO_SPECIFY`; WP-W6B-35 `READY_TO_SPECIFY`; WP-W6B-36 `READY_TO_SPECIFY`.

For the sought outcome `C12@INTEGRATE` at **native generated-person scope**, the root `G-C12-NATIVE-INTEGRATE` still requires `C11@INTEGRATE`, `C10@INTEGRATE`, `C9@INTEGRATE`, `C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE`, and `C12:LOCAL_GUIDE:EXTERNAL_ANCHOR@VERIFY`. The C9 branch expands to `O03@ACCEPT` plus `O05@ACCEPT` **OR** `O07@ACCEPT` with scope predicates, actual C8/C4 and an E2 reader; the C11 branch requires Pyat `C0@ACCEPT` and Sorok receiver. None of these are replaced by a sourcefree P1/M35 test. The **first independently feasible** work is the code/evidence matrix (`WP-01`), sourcefree access bridge (`WP-02`), science decision packets (`WP-03/04/05`), receive-only C11 spec (`WP-08`), C4/C8 source-contract specifications (`WP-10/11`), alongside **separate** Pyat-origin owner action (`WP-09`). The actual native C12 build (`WP-24`) is blocked.

For `A5@ACCEPT`, `G-A5-ALL-ACCEPT` has `S11@VERIFY`, `S14:LOCAL_GUIDE:OPERATED_CONTROLS@VERIFY`, `S15:LOCAL_GUIDE:HUMAN_PROTOCOL@ACCEPT`, `S5:LOCAL_GUIDE:PLURAL_EVALUATION@ACCEPT`, and actual `A5:LOCAL_GUIDE:GATE5_HUMAN@VERIFY` as independent conjuncts. The human **test** uses `G-A5-RUN-COMMON` plus one **chosen** mode `G-A5-EARLY-IF` or `G-A5-NATIVE-IF`; it does *not* need `A5@ACCEPT` before running. First work is S5/S14/S15 science/safety/protocol SPECIFY and S11 UX SPECIFY; a low-fidelity S11 prototype is blocked only on its own `S11@SPECIFY` stage, not on full native C12. Actual people cannot yet be tested under an accepted A5 claim. Conditional alpha 100 permits curated seeds for Gates 0–3, **not** substitution for A0 native claims, operational privacy or participant rights.

## 3. Recomputing one real original target after one hypothetical qualified receipt

The change test changes **one leaf only**: `E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY` from UNSATISFIED to `SATISFIED_AT_SCOPED_CUT` with an **illustrative independent source-matrix verification**. This is not an assertion that such a worker returned. It uses the actual W5-reported E008 writer/root/version/ACK/anchor mismatch.

| Selected source-derived work | Before, W5 frozen | After hypothetical matrix receipt | Why |
|---|---|---|---|
| `WP-W6B-01` matrix | READY_TO_SPECIFY (prerequisites met) | COMPLETED_AT_HYPOTHETICAL_SCOPED_CUT | New qualified matrix witness attaches to target; work no longer first missing leaf |
| `WP-W6B-06` joint writer/reader decision | JOINT_WAITING_ON_MATRIX | **JOINT_READY_AFTER_MATRIX** | The external `E008 MATRIX@SPECIFY` predecessor is now present; the two internal same-stage contract demands can be solved together |
| `WP-W6B-07` compatible C9→C12 implementation | BLOCKED_UPSTREAM | **BLOCKED_UPSTREAM** | Neither writer-schema nor reader-root is yet SPECIFIED; a matrix is not the negotiated contract |
| `WP-W6B-24` native C12 | BLOCKED_UPSTREAM | **BLOCKED_UPSTREAM** | CAN/ADP, C4/C8/C10/C11, external anchor and native source grants remain |
| `WP-W6B-25` human A5 | BLOCKED_UPSTREAM | **BLOCKED_UPSTREAM** | Privacy/UX/scientific/human gates remain; E008 alone cannot create a human participant |

**Actual computed change in the package classifier:** [{"id":"WP-W6B-06","status":"JOINT_READY_AFTER_MATRIX"}]. The table separately records `WP-01` as *completed* in the hypothetical leaf ledger, because an action can remain classified 'READY_TO_SPECIFY' by its prereq gate even after its output is complete unless the evaluator first checks the target's own evidence. Therefore the correct procedure is **completion before readiness**. Never count a completed prerequisite as both newly runnable and pending. A source or schema mismatch in the matrix instead yields `ALTERNATIVE_DECISION_REQUIRED`, not automatic resolution.

## 4. Directed cycle / SCC result

A Tarjan pass over all **phase-specific gate targets → required phase-specific prerequisites**, with non-blocking `CONTEXT_ONLY` excluded, found exactly **1 nontrivial SCC** at this source-derived *design model*: `C12:LOCAL_GUIDE:READER_ROOT@SPECIFY` ↔ `C9:LOCAL_GUIDE:WRITER_SCHEMA@SPECIFY`.

This is **joint interface co-specification**, not evidence of a native code circular import. W5 08 E008 and 10 expressly report incompatible candidate C9/C12 cuts and an unresolved owner selection of writer/root/schema/ACK/anchor. `G-E008-C9-COSPEC` and `G-E008-C12-COSPEC` model *reciprocal acceptance of one shared interface*: neither owner may unilaterally freeze an incompatible half as an accepted pair. **Joint package** `WP-W6B-06`: C9 writer owner + C12 reader owner + proportionate independent cut reviewer; first external action is the `E008@SPECIFY` matrix, then jointly agree a provisional writer-output/reader-readset contract, source version/root, mirror ACK, external custody requirements, migration behavior, negative cut, tests; C9 and C12 can separately implement against that *same agreed contract*; one independent actor performs same-root write/cold read/severance before any acceptance. The SCC is resolved as a coordinated `SPECIFY` bundle, not by declaring both already done.

**Limit:** sources prove a shared contract/selection issue, not that both source code implementations are locked in an unavoidable runtime dependency cycle. A source reread may find one fully compatible existing adapter; then the joint *decision* can select reuse and dissolve the modeled SCC. If the proposed bidirectional specification proves unjustified, mark `DESIGN_CYCLE_NEEDS_RESOLUTION` and replace with an owner-chosen one-directional interface dependency. Do not invent a second joint runtime for the sake of an SCC.

Time recursion `C10/C12` at successive events is **not** a same-stage dependency SCC; cyclical *human developmental causation* is not a cycle in the build graph. Nor does S12 optional social ecology block early A5; alpha 100 explicitly defers it.

## 5. Reproduction and negative assertions

- Exact success grades from inherited W5: `M25@KNOW`, `M29@KNOW` historical attributed functions; `E021@VERIFY` scoped independent JOIN-E 7bf evidence; `C4:LOCAL_GUIDE:COACTOR_B@BUILD` and `C8:LOCAL_GUIDE:ACTION_OMISSION@BUILD` sourcefree **author** proof. No receipt here says native or human.
- `O03:LOCAL_GUIDE:RULE_A_PREDICATE@KNOW` is S35's *candidate*, not native `O03@ACCEPT`.
- `O05:LOCAL_GUIDE:RULE_T_DISCRIMINATOR@KNOW` only documents the scientific controversy; neither `O05@ACCEPT` nor `O07@ACCEPT` is present.
- `C0:LOCAL_GUIDE:PYAT_RECEIPT@KNOW` means knowledge of the **need**, not Pyat `@ACCEPT`.
- No `A5:LOCAL_GUIDE:GATE5_HUMAN@VERIFY` record or positive current native importer was found in these frozen W5 references.
- Some W6-B graph source and scope choices are **researcher-proposed** and must be checked against W6-A/C and current HQ/source owners at fan-in. The graph is a **plan candidate**, not a logical proof that all scientific/ethical necessities are complete.

**Provenance:** In-memory JSONL evaluation of this worker's actual committed source, with `S0–S16` original requirements in Sorok `05_PROGRAM_MAP.md` @`865b5b01e1a27e99020cf2bb389af8cd4c874b57`; Sorok `00E/74/100/101` same cut; W5 `08/09/10/13` @`e3d5c77f455f6d53c8078c1c706c12f9a9ee4bde`; W1-B `5ab447a447620e65d441d2d2cfd745cb3d354a7c`; W1-C `12433b89e100d2c4b9b20a94c4ccca7d2af7529a`. No full local Sorok suite or human test was run.
