# Astra independent deep system audit R1

**OVERALL SYSTEM DISPOSITION: ASTRA_AUDIT_COMPLETE__STOP_THE_LINE_DISPOSITION_REQUIRED**

Accepted anchor: `abd0b5ff2ffcf235b67140641f88cc61ca45c12c`. Active candidate inspected separately: `a1630969f8e0b1003e657a38f77abbc413f83f2e`. This is an audit disposition, not implementation PASS or project acceptance.

**SAFE TO CONTINUE CURRENT GT12 CLOSURE? YES_WITH_CONDITIONS.** Continue the bounded closure work, but do not close/adopt the audited E2B candidate until ASTRA-003 is disposed and the genuine ordinary current pair traverses the public entry. Use the scoped GT12 builders and governed CONTEXT-only wrapper; keep exact current query/fact/replay gates. The audit does not establish corruption of the banked current GT2 fact.

**SAFE TO BEGIN GT3/GT4 AFTER CURRENT GT12 CLOSURE? NO under the audited contracts if this enables positive V3 authority.** Closure alone does not resolve ASTRA-001/002/004 or answer ASTRA-006. Preliminary work to establish those preconditions is appropriate; the first positive event requires separately accepted authority and invocation/effect proofs.

**STOP_THE_LINE:** ASTRA-003, active candidate only. Its current-object checker normalizes component refs to `ExactRef` but compares them to ordinary query `dict` refs. The exact current query fails that comparison. The known pending current payload is not a separate audit finding.

**BEFORE_GT3_GT4:** ASTRA-001 (source immutability), ASTRA-002 (shared-boundary authority), ASTRA-004 (positive invocation binding), ASTRA-006 (dependency-role/reconstruction question).

| Top five, in HQ action order | Required disposition |
|---|---|
| ASTRA-003 — current E2B representation contradiction | Repair the comparison without changing identity; prove the real public entry. |
| ASTRA-001 — sealed source bodies remain writable | Enforce deep immutability or equivalent authenticated reads; preserve canonical bytes. |
| ASTRA-002 — wrapper-only authority fitness | Enforce exact family/source and relation-use law at shared operation boundaries. |
| ASTRA-004 — future delegation lacks source binding | Accept and test the per-invocation positive-owner contract before enabling positive V3. |
| ASTRA-005 — expanded provenance transport | After GT12, retain compact exact refs and avoid repeated expanded canonicalization. |

**SINGLE HIGHEST-VALUE CORRECTNESS ACTION:** ASTRA-001. Make an exact sealed source reference remain a truthful reference after ingestion. Do this before validation-by-ref caching.

**SINGLE HIGHEST-VALUE OPTIMIZATION:** ASTRA-005. Preserve all existing commitments while eliminating expanded reference materialization at the seal boundary. Inferred canonical document size is 47,238,068 bytes versus 3,108,906 compact bytes (15.194×); this is not a measured speedup.

**SINGLE MOST IMPORTANT FUTURE-RISK ACTION:** Require separately accepted, source/actor/operation-bound positive-owner invocation and observable runtime effects. A structural resolution or delegation receipt must not become authority by implication.

**MOST SURPRISING THING FOUND:** Public exported projections can alter nested records of a sealed C11 release. The isolated source then produces a different SUPPORTED joint table under the same release/event/query/provenance refs. The new fact hash does change, and a known expected current fact/replay hash would catch it.

**MOST IMPORTANT THING INVESTIGATED AND FOUND SOUND:** The production V3 guard cannot be made positive through caller-claimed authority or a registry override. Its public path uses an immutable empty accepted-positive registry and returns DENY_ZERO_EFFECT. The adopted typed GT12 wrapper also strictly preserves CONTEXT-only descent. These are real current protections, not proof of a future stateful owner.

Six ledger records: five HIGH and one MEDIUM; one STOP_THE_LINE, four BEFORE_GT3_GT4, one HIGH_VALUE_AFTER_GT12. The five substantive primary classes each have one record: IDENTITY_OR_PROVENANCE_RISK, AUTHORITY_RISK, CROSS_LAYER_CONTRADICTION, FUTURE_GT3_GT4_RISK, IDENTITY_PRESERVING_OPTIMIZATION; OPEN_QUESTION has one. No CRITICAL claim.

Validation: 298 focused accepted-anchor tests and 33 focused active-candidate tests passed. Isolated contract checks exposed the gaps those suites do not cover. The full current 19,210-member execution and actual fact rehydration were not repeated. Exact coverage, controls, and limits are in [01](01_SCOPE_AND_COVERAGE.md), [02](02_FINDINGS_LEDGER.jsonl), and [05](05_TEST_ADEQUACY.md).
