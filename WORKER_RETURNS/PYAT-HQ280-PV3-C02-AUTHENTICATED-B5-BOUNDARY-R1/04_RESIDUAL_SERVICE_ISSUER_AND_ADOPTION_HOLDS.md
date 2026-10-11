# 04 — Residual service, issuer and adoption holds

**Scope of this document:** everything C02 explicitly does **not** establish, and the exact
conditions under which anything here could later change. Nothing below is granted, implied
or self-adopted by this commission.

---

## 1. What the C02 candidate establishes (narrow, and only this)

At a **development, source-free, non-authorizing** grade, over an owner-controlled
perimeter whose trust edge is the already-accepted M2 ReleaseCore owner:

> A `LearnedProductLifecycleSubject` that reaches B5 publication through this ingress
> corresponds, field-by-field, to material the accepted M2 owner actually issued, and
> matches a frozen, complete, closed owner expectation for its slot.

That is a **technical authenticity** statement. It is not a competence statement, an
authority statement, a currency statement or a permission statement.

## 2. Residual R1 — competent producer issuer (STILL ABSENT)

* **Status:** absent. C02 invents no issuer, key registry or signature scheme, and grants
  none.
* **What C02 does:** `semantic_authority_snapshot_refs` are **owner-held**, deeply frozen
  and expectation-bound. That is an *internal owner-setup completeness invariant*, not proof
  that any competent authority issued them.
* **Why it matters:** F8F's hold (a) "a producer-issued subject credential" and (b) "a
  competent producer issuer" are separate. C02 addresses the *structural* half — a caller
  can no longer assert a subject — but **not** the *issuance* half. Nobody has been shown to
  be competent to issue a learned product at all.
* **To close:** an accepted, separately authorised AuthoritySnapshot / producer-issuer
  owner. Not granted here. Not invented here.

## 3. Residual R2 — replay is an authenticated claim, not an independent re-execution

* **Status:** `REPLAY_COMPLETE` remains an **owner-held claim**. C02 binds it to the M2
  replay reconstruction closure's own `replay_grade` and to the closed expectation, and
  refuses a grade outside the accepted vocabulary (H06/H07) or an explicitly incomplete
  closure (H08). It does **not** re-run the replay.
* **Explicit warning carried on the receipt:** `HISTORICAL_EXPLANATION_ONLY` is a permitted
  grade and is **labelled as such** on every receipt that uses it (P06). It must never be
  read as serving-grade or current-grade replay.
* **To close:** an accepted replay executor owner that re-derives the closure from source
  material. Not granted here.

## 4. Residual R3 — the expectation is not an independent preimage

* **Status:** the expected-identity map is authored from the same owner construction it
  authenticates. It is a **drift guard and a tamper detector**, not an independently
  authored preimage.
* **Consequence:** an in-process principal able to rewrite **both** custody and expectation
  consistently would produce an authenticating but fictitious subject. This is explicitly
  **UNPROVED and out of scope**, not claimed closed.
* **Partial mitigation that does hold:** every M2-owned field is re-read from the accepted
  M2 owner at publish time and cross-checked against the expectation, so tampering with the
  **custody** alone (without the expectation) is caught (H14, H25). Tampering with **both**
  is not covered.

## 5. Residual R4 — not deployed security

* **Threat model covered:** the bounded **data-only external caller** of F8F K4–K5, widened
  to "a caller that may reach the C02 public surface".
* **Not covered:** an attacker executing arbitrary Python inside the owner process. C02 is a
  **trusted-harness** design, in the same sense as the accepted HQ266 G01 ingress. It is not
  a custody root, not a trust root, and not a substitute for an independent credential.

## 6. Frozen vs unfrozen custody (exact statement)

| frozen, deeply | not frozen |
|---|---|
| the expected-identity map | the `M2Repository` object |
| the slot table (`MappingProxyType`) | the `ExactRef` / `AuthorityRef` objects inside custody |
| `owner_custody_projection()` | nested objects of the M2 repository |
| `accepted_expected_identity(slot)` | |

Item assignment, deletion and the mutating mapping methods are refused on every frozen
container (H27). Deep-converting the unfrozen objects would change the semantic ref objects
the accepted M2/B5 owners consume, which is out of scope. **A caller cannot reach them
through the public surface; an in-process holder of one can still mutate it.**

## 7. Holds that remain exactly where F8F/F8E left them — UNCHANGED

| # | hold | C02 status |
|---|---|---|
| 1 | **G0b operative model/use** | **HELD.** No grant, no request, no fabrication. `g0b=None` on every receipt. |
| 2 | **G1 selected-service / serving** | **HELD.** C02 mints no selected service. `g1_service=None` on every receipt. |
| 3 | **CURRENT / currentness** | **HELD.** C02 never performs selection; `current_selection_performed=False`; runtime assert proves no `CURRENT_*` event exists (P04); a counterfeit claim has no field (H02). |
| 4 | **B5 publication trust root** | **Still not a trust root.** C02 is the *development-grade* answer to F8F hold (a) — a bound perimeter — not a production credential. |
| 5 | **Source-scientific / raw-source use** | **Not granted.** No SAV/DTA, no raw survey, no source read. |
| 6 | **Respondent lineage** | **Not republished.** |
| 7 | **World / N9 / N10W / V3 / actor** | **Untouched.** |
| 8 | **Semantic / canonical / PRE-MAIN / root manifest** | **Unmutated.** |
| 9 | **Self-adoption** | **None.** This candidate adopts nothing, including itself. |

## 8. F8E invariants carried forward and re-verified

| F8E/F8F invariant | C02 status |
|---|---|
| four-XOR source-free-only, `grant=None`, `authorizing=False`, `external_issuer=None` | preserved |
| `DEVELOPMENT_GRADE` nonissuing ceiling | preserved and extended (`G1_HELD`, `CURRENT_HELD` added explicitly) |
| `requested_replay_grade` must equal the historical M2 grade; `FRESH_PROCESS_REPLAY` refused (K8) | preserved (H07), now enforced by both the accepted M2 owner and the ingress |
| native nonpositive C1 cannot mint an M2 product (K7) | unchanged — C02 depends on the accepted M2 owner for this and adds no relaxation |
| publication and CURRENT selection fail for the candidate's own F8E subject | **C02 does not weaken this.** C02 requires the positive path to keep working; it does not grant the F8E candidate any publication or selection it did not have. |
| I4 M1-only, no selected T1 service | preserved |

## 9. Adoption holds — what HQ would have to decide, and C02 does not decide it

1. Whether a **perimeter** is the correct enforcement point versus a producer-issued
   credential. C02 argues for the perimeter at development grade and shows its limits (R3);
   it does not settle the question.
2. Whether the **candidate perimeter** may ever be adopted into the canonical tree. C02
   proposes nothing for adoption and produced no `PROPOSED_UNADOPTED` diff, because no
   correction to an existing owner proved indispensable.
3. Whether **R1** (owner-held AuthoritySnapshot refs) is acceptable at any grade above
   development. C02's honest answer is that it is not, without a real issuer.
4. Whether **R2** (authenticated replay claim) is acceptable for anything but historical
   explanation.
5. **Independent hostile re-review.** C02 has not been independently reviewed. F8F's
   standard was independent re-execution with adversarial inputs; C02 has run mutation
   testing but **no independent reviewer**. Recommend a C03-style independent hostile pass
   before any grade above development is considered.

## 10. Scientific invariants — explicitly untouched

All 35 waves remain in scope and unmodified. 18,276 historical implementation IDs are not
the original administered-item count. 78,037 WGA annotations are not issued executable
jobs. 46 WVS candidates / 58 UNAVAILABLE fact states are not measured discoveries. Afro R5
19,210 common risk and CONTEXT permission do not grant material causality or G0b. No
present authority, missing respondent meaning, joint exposure, weighted design, wave
comparability, model use, authenticated B5 publication or V3 actor state was manufactured.

**Terminal:** `HQ280_PV3_C02_B5_TRUST_BOUNDARY_SOURCEFREE_CANDIDATE_AND_HOSTILES_PUSHED__NO_OPERATIVE_PUBLICATION`