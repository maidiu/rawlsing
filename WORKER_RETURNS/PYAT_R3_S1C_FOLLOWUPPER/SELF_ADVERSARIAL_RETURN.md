# PYAT R3 S1-C — Independent follow-upper adversarial construction

**Packet:** S1-C / P1-04. **Not G5.** **Draft additive PR:** https://github.com/maidiu/rawlsing/pull/959. **Exclusive branch:** `agent/pyat-r3-s1c-followupper-projection-adversarial-20261112-r1`.
**Common code lineage:** A #950 `5a6eb73158479a3bf4cead70b0d36cca43d902b6` → B #955 implementation/test `e15ccaedaa54155fc3855f821565e2794c946a68` → additive repair. Other B branch was not modified. #948 `7064daa14d93109211629e72d08f3a6e705a0d57` is unmerged; protected cut `6a5c12f04323d74001f9632063ec907f4fc4468e`. Authority: TEST_ONLY_SOURCEFREE, no original35/host/science/actor/protected merge.

## Original contract and adversarial approach

Independently read P1-04 #918 and R3/R3C/R3S #909, adopted PROGRAMMA/MCR-lite, the real R61 `enumerate_frontier` constructor, `ScientificFrontier`, existing R03 `compile_governed_frontier`/issued I05 reader and A/B source/tests/returns. G1/G3 require *all declared source and science fates*, not mere counts or same-owner hashes. A established valid operation set anti-joins; B correctly detected three previously omitted negative/occurrence surfaces and froze them. B's author CI reports 14 new/current tests plus 22 inherited and real Batch/C11/I05 results at sourcefree fixture grade.

## A material further defect, not a speculative improvement

B's `verify_frozen_inputs` compared `FrozenInputCensus.unknown_scope_records` to `frontier.unknown`, `excluded_scope_records` to `frontier.excluded`, and the inventory ledger to a copy of `frontier.inventory_ledger`. **If the caller forged both the frontier and its separately rehashed frozen packet, the checks accepted fictitious records.** B's own initial new test deliberately constructed an extra `ROUTING_UNKNOWN` for an unrepresented source item X and an extra exclusion for unrepresented Y and asserted that this falsified frontier was valid. The original R61 `enumerate_frontier` defines `unknown` as EXACTLY `op.material()` for UNKNOWN operations; `excluded` as the exact projection of PROHIBITED/INAPPLICABLE_PROVED operations; `inventory_ledger` as `inventory_ledger(inventory, policy)`. A sourcefree fake external negative record is not one of those outputs.

Consequence: a hash-consistent, fabricated UNKNOWN/EXCLUDED/administration-fate record could be returned as *conserved sourcefree evidence* even though there was no corresponding typed original R61 operation/inventory. A second hash does not prove an independent source.

## Implemented replacement

At the same existing adapter entry point, before opening a source or invoking the compiler, check:
- exact `frontier.unknown` and `frontier.excluded` projections from operation rows;
- exact occurrence ledger derivation from frozen `SourceInventory` and `GrammarPolicy`;
- per-operation class, scientific disposition, execution and result counters, not just total count.

Retain B's independent frozen-census equality guards and all of A's real issued execution/anti-joins. No new compiler, source permit, persistence or scientific issuer. New typed refusals are `UNKNOWN_PROJECTION_DRIFT`, `EXCLUDED_PROJECTION_DRIFT`, `INVENTORY_LEDGER_SOURCE_DRIFT`, and per-axis `*_COUNTS_DRIFT`. Tests explicitly rehash fabricated frontier and census, exercise a legitimate R61 UNKNOWN from a missing risk set (rather than unrelated routing HELD), reject a rehashed altered per-occurrence disposition, reject count-preserving execution histogram substitution and preserve B's existing restoration/first-reader tests.

**Code/test cut:** `b120cfc449415a17c7469c26329a8e9ea4e1a48c`.
- Adapter blob: `ae66477721eff01185872fba1e1f9453ac7ec655`.
- Tests blob: `f0e7f5980a54f70a5bc172a8d628074e317f246a`.
- Predecessor B adapter blob: `e97c3727d7798fedca4cd5c9b621e335ff50ebb7`.

## Proof integrity — explicitly NOT green

**Verified by source inspection**: B's frozen-vs-frontier equality cannot detect a shared edit on both sides; R61's authentic `enumerate_frontier` projection identities prove the additional consistency check is directly applicable. Native `lower_operation` already rejects noncanonical eligible operation IDs, so that suspected separate bug was **refuted**, not claimed as a new finding.

**Actual executable verification at this exact new head: NOT_RUN.** The PR runs `43279326500`, `43279674997` and `43280002352` failed before a job runner/steps were assigned; job listings showed no runner or executed test steps, and decoded logs were unavailable. Their `failure` states are **not** converted to either passing tests or reproduced code failures. The parallel stacked integration workflows failed in the same pre-step condition. A's and B's earlier CI PASS receipts apply only to their respective immutable tested cuts and do not prove this descendant.

## Self-adversarial assessment and next challenge

I caught and corrected one test weakness: a second `_fixture(tmp_path)` overwrote the same source fixture while testing count-preserving status drift; it now calls `enumerate_frontier(inventory,policy,budget=5)` on the *same* frozen source. I caught another: routing UNKNOWN yields HELD under current R61, whereas missing risk-set proof yields real UNKNOWN; the test now uses a genuinely UNKNOWN operation.

Remaining limits: No real runtime or fresh-process tests at this exact patch cut; the sourcefree projection check enforces **internal R61 consistency**, not independent original35 completeness or authentic third-party entitlement. If future science requires source-negative items not represented as R61 operations, they need a separately typed source-qualified surface rather than laundering an extra mapping into R61 `frontier.unknown`. Cost is linear in already declared operations and inventory rows, but no host measurement on this delta has occurred. Do not reopen A/B's valid sourcefree operation/reader work or claim an external issuer.

**Agent A's strongest counterattack:** first rerun the focused and inherited suites at this exact patch code cut on an actual authorized runner. Then try (1) jointly rehashed invented UNKNOWN/EXCLUDED rows, (2) rehashed false occurrence-level disposition, (3) equal-total execution status substitution, (4) legitimately sourced UNKNOWN risk-set and optional-weight RAW, (5) exact native Batch/C11/I05 changed-input output and restoration, (6) whether R61's expected projections are unconditionally valid for this declared SOURCEFREE frontier. Repair only a real failed original-contract test. After A's counter and clean G1–G4, a distinct nonauthor decides G5. No hardening loop.

**Disposition:** MATERIAL_SOURCE_GROUNDED_REPAIR_COMMITTED__NEW_S2_TESTS_NOT_RUN__A_COUNTERATTACK_REQUIRED__G5_NOT_RUN.
