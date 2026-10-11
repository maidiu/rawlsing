# PYAT HQ280 PV3 C02 — Producer-authenticated B5 lifecycle publication trust boundary

**TERMINAL:** `HQ280_PV3_C02_B5_TRUST_BOUNDARY_SOURCEFREE_CANDIDATE_AND_HOSTILES_PUSHED__NO_OPERATIVE_PUBLICATION`
**Agent:** Local independent OpenCode/Codex Python implementer.
**Branch:** `agent/rabochii-pyat-hq280-pv3-c02-authenticated-b5-boundary-r1`
**Sealed startup (verified, unchanged):** `c6e986dfa02b80887ded5f4d0da2e2413e676172`
**Authority:** HQD-2026-10-10-280 · parallel seal `908ee4e74849884b1d4c2f532209a0ca57538b67` · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated).
**Disposition:** source-free, non-authorizing **development candidate**. **No self-adoption.** No canonical, PRE-MAIN or semantic mutation.

---

## 1. What was actually done

Independently traced the real producer→B5 ingress and caller graph in this worktree,
re-reproduced HQ280 F8F's B5 publication boundary from actual owner invocations, and built
the smallest authenticated, owner-controlled perimeter in front of the accepted B5 owner.

**One new candidate module + one new candidate test module. Zero modifications to any
existing production owner.**

| file | state |
|---|---|
| `rawlsing_next/pre553_authenticated_b5_ingress_candidate.py` | NEW, candidate only |
| `rawlsing_next/tests/test_pre553_authenticated_b5_ingress_candidate.py` | NEW, candidate only |
| `rawlsing_next/pre553_learned_product_lifecycle.py` | **UNMODIFIED** |
| `rawlsing_next/pre553_learned_product_release.py` | **UNMODIFIED** |
| `WORKER_RETURNS/PYAT-HQ280-PV3-C02-AUTHENTICATED-B5-BOUNDARY-R1/` | NEW (this return) |

**Correction to existing `pre553_learned_product_lifecycle.py` proposed? NO.** See §5: the
defect is correctly located in the *absence of a perimeter*, not inside the B5 semantic
owner, so no correction was necessary and none is proposed as unadopted code.

## 2. The boundary, independently re-reproduced (not restated from F8F)

`repro/repro_f8f_k4_k5_boundary.py`, executed at HEAD `c6e986dfa…`, against the accepted
owners in this worktree:

| probe | F8F recorded | **C02 observed** |
|---|---|---|
| K4 forged `replay_state` | PUBLISHED | **PUBLISHED + CURRENT_SELECTED** |
| K5a honest state, forged ceiling | refused (on replay closure) | refused, `MISSING_REPLAY_CLOSURE` |
| K5b forged state + forged ceiling | PUBLISHED | **PUBLISHED + CURRENT_SELECTED**, ceiling stored verbatim as `urn:reviewer:PRODUCTION_GRANT` |
| K5c forged state + forged receipts + forged replay root | PUBLISHED | **PUBLISHED + CURRENT_SELECTED** |
| K7 fully forged subject built from caller dicts | *(not probed by F8F)* | **PUBLISHED + CURRENT_SELECTED** |

**Result: 4 of 5 caller-constructed subjects reached PUBLISHED and 4 of 5 reached
`CURRENT_SELECTED`.** F8F's finding is confirmed at owner level, and it is **one step
worse than recorded**: the boundary is not only a publication boundary, it is a
**current-selection** boundary. Log: `repro/c02_boundary_repro.log`.

## 3. The candidate

`pre553_authenticated_b5_ingress_candidate.py` — an owner-controlled, **data-only**
perimeter. Its public surface `publish(PublicationRequest(slot=<name>))` accepts one
closed builtin dataclass with one closed field. There is **no field through which a
subject, release ref, authority, closure, receipt, replay root, permission ceiling,
currentness claim, hash or callback can arrive.** All F8F/K4–K5 forgeries were *subject*
forgeries; a data-only surface has no subject.

The trust edge is the **existing accepted M2 owner** (`pre553_learned_product_release`),
not a new registrar and not cryptography. No new authority, issuer, key registry or
signature scheme was invented — none is granted by this commission.

Refusal happens **before the first accepted-B5 call**; every typed error carries
`b5_invoked=False`. See `02_AUTHENTICATED_INGRESS_CANDIDATE.md` for the full design.

## 4. Actual test evidence

| suite | result | log |
|---|---|---|
| C02 candidate suite (**37 tests: 7 positive, 30 hostile**) | **37 passed, 0 failed** | `repro/c02_candidate_suite.log` |
| 13 adjacent **accepted** owners (B5 lifecycle, M2 release, G1 ingress, EE14 as-of CURRENT, replay audit, repo-native CURRENT rehydration, applicability court, 3× F8 scope/binding courts, F8 receipt-permission identity, C1 query, learned-world composition) | **525 passed, 0 failed** | `repro/adjacent_adopted_owners.log` |
| pyflakes on both new files | clean (rc=0) | `repro/pyflakes.log` |
| **mutation testing — 6 mutants, 6 killed** | see below | `03_ACTUAL_POSITIVE_NEGATIVE_TESTS.json` |

The suite is **not all-refusal green**: P01–P07 are genuine positive paths (real M2
release construction, real B5 publication, content-addressed reproducibility, multi-slot
independence, historical replay grade accepted *and labelled*). H01–H30 are hostiles, each
invoking real owners with a mutated caller side and recording the actual typed outcome.

**Non-vacuity was proven, not asserted.** Six targeted mutants of the candidate's own
enforcement were each killed by the suite:

| mutant | tests that fail |
|---|---|
| deep authentication disabled | 5 (H04, H14, H18, H19, H25) |
| revocation gate disabled | 5 (H09–H13) |
| replay gate disabled | 3 (H05, H06, H28) |
| data-only request surface relaxed | 3 (H01, H02, H03, H17) |
| construction-time expectation completeness gate removed | 3 (H20, H21, H22) |
| M2 determinant derivation removed | 15 |

## 5. Enforcement placed at the correct perimeter — no semantic owner mutation

`LearnedProductLifecycleExecutor` is, by its own module contract (lines 11–13), an
owner-internal runtime that "deliberately does not own producer semantics, M2 release-core
semantics, AuthoritySnapshot maintenance, consumer permission…". Its publication gate is
**necessarily** a well-formedness gate over an opaque, caller-asserted subject, and that is
correct for its jurisdiction. Adding an authenticity gate *inside* it would be a semantic
owner mutation and a jurisdiction change.

**Decision: enforcement belongs in a new candidate-only perimeter in front of B5, bound to
the accepted M2 owner.** Full argument and the exact caller graph in
`01_PRODUCER_TO_B5_CALLGRAPH_AND_TRUST.md`.

## 6. Residual holds (unchanged, and NOT granted by this work)

1. **Competent producer issuer** — still absent. No `AuthoritySnapshot` is issued.
2. **Semantic AuthoritySnapshot refs are OWNER-HELD, not issuer-held** (residual R1). This
   is the one field class C02 cannot source from an accepted owner, and it is stated as an
   open prerequisite, not solved.
3. **`REPLAY_COMPLETE` remains an owner-held claim** (R2), gated by the M2 replay closure's
   own `replay_grade`; not an independent replay re-execution.
4. **The expectation is authored from the construction it authenticates** (R3) — a drift
   guard and tamper detector, not an independent preimage.
5. **G0b operative model/use** — HELD. **G1 selected-service / serving** — HELD.
   **CURRENT / currentness** — HELD; the candidate never performs selection.
6. **B5 publication still has no trust root beyond owner custody + the accepted M2 owner.**
   This candidate is the *development-grade* answer to F8F §4 hold (a), not a production
   credential. Nothing here is deployed security against an in-process attacker (R4).
7. **All 35 waves** remain in scope and untouched. 18,276 / 78,037 / 46 / 58 are not
   treated as implementation IDs, executable jobs, measured discoveries or positive
   statistical results. No raw SAV/DTA, no respondent-lineage republishing, no source read.
8. **Graft-from-another-release and tampered-release defences are the ACCEPTED M2 owner's**,
   demonstrated at runtime (H15, H16) — not new C02 authority.

## 7. Terminal

`HQ280_PV3_C02_B5_TRUST_BOUNDARY_SOURCEFREE_CANDIDATE_AND_HOSTILES_PUSHED__NO_OPERATIVE_PUBLICATION`