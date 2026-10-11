# 02 — The authenticated ingress candidate

**File:** `rawlsing_next/pre553_authenticated_b5_ingress_candidate.py`
**Contract:** `HQ280_C02_AUTHENTICATED_B5_INGRESS_CANDIDATE@1`
**Grade:** `SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD__G1_HELD__CURRENT_HELD`
**Status:** development candidate on branch. **Not adopted. Not a trust root. Not deployed
security.**

---

## 1. Design in one paragraph

Give the caller a surface that **cannot express a forgery**, and bind every identity the
B5 owner will consume to material the **already-accepted M2 owner** actually issued. The
caller names an owner-registered slot; the ingress resolves the release itself, derives the
determinant/replay/dependency closures itself, builds the `LearnedProductLifecycleSubject`
itself, authenticates it field-by-field against a frozen closed expectation, and only then
calls B5. Every refusal happens before the first B5 call.

This mirrors the accepted HQ266 G01 ingress (`pre553_ee14_c1_owner_authenticated_ingress.py`),
which already established the pattern in this repository: data-only surface, owner-held
expectation, deep closed-set authentication before the downstream owner, typed errors
carrying the exact mismatched fields, and an explicitly stated bounded residual. C02 does
not invent a new discipline; it applies the existing one to the B5 perimeter.

## 2. The public surface

```python
@dataclass(frozen=True)
class PublicationRequest:
    slot: str
```

```python
ingress.publish(request) -> B5IngressReceipt
```

Enforced with **exact builtin types** (`type(x) is T`, never `isinstance`):

* a subclass of `PublicationRequest` is refused (H03);
* a subclass of `str` for `slot` is refused;
* any field beyond `slot` is refused (H01, H02);
* `None`, `str`, `int`, `tuple`, `object()` are refused (H03).

**There is no field through which a subject, release ref, authority, closure, receipt,
replay root, permission ceiling, currentness claim, hash or callback can arrive.** All
F8F/K4–K5 forgeries were *subject* forgeries; a data-only surface has no subject.

## 3. The closed expected-identity key set

`REQUIRED_EXPECTATION_KEYS` — 21 keys, exact, closed, all compared on every publish:

```
release_key                    release_content_hash         producer_subject_key
producer_contract_key          semantic_anatomy_key         semantic_projection_hash
product_key                    product_family_key           producer_owner_key
selection_scope_key            authority_snapshot_keys      direct_dependency_keys
determinant_keys               determinant_set_hash         consumed_authority_keys
replay_closure_key             replay_grade                 replay_root_key
receipt_keys                   permission_ceiling_key       m2_release_projection_hash
```

Fail-closed completeness, three times over:

1. **at ingress construction**, per slot — so an incomplete owner setup can never reach a
   request, let alone B5 (H20);
2. **immediately before the comparison** — so the gate cannot be skipped (same tests);
3. **as an explicit refusal for missing keys, extraneous keys, and wrong builtin types**
   (`type(v) is EXPECTATION_KEY_TYPES[k]`, so a `bool` cannot satisfy a `str` field, and no
   subclass can satisfy a scalar field — H22).

This is the same D1 defect class HQ268 found in the accepted G01 owner, deliberately closed
here rather than reproduced.

## 4. Ordering — refusal is strictly before B5

```
publish()
 ├─ _validate_request              → B5IngressRequestError        (b5_invoked=False)
 ├─ slot lookup                    → B5IngressRequestError        (b5_invoked=False)
 ├─ _resolve_m2   [ACCEPTED OWNER] → B5IngressM2Error             (b5_invoked=False)
 ├─ _revocation_check              → B5IngressRevocationError     (b5_invoked=False)
 ├─ _replay_gate                   → B5IngressReplayError         (b5_invoked=False)
 ├─ _determinant_refs              → B5IngressDeterminantError    (b5_invoked=False)
 ├─ BUILD subject (owner side)
 ├─ _authenticate  [CLOSED SET]    → B5IngressAuthenticationError (b5_invoked=False)
 ├─ ═══ first call into B5 happens here ═══
 ├─ B5.stage_release / register_product / publish_product
 └─ B5IngressReceipt
```

`b5_invoked` is a real attribute on every typed error, and **H28 proves it by spying on
`LearnedProductLifecycleExecutor.stage_release`**: on the positive path the spy fires
exactly once with the expected release key; on a hostile path it fires **zero** times.

## 5. Typed refusals (each provably reachable, each `b5_invoked=False`)

| class | `refusal_class` | reached by |
|---|---|---|
| `B5IngressRequestError` | `REQUEST_SURFACE_VIOLATION` | H01, H02, H03, H17 |
| `B5IngressCustodyError` | `CUSTODY_INCOMPLETE` | H26 |
| `B5IngressRevocationError` | `AUTHORITY_REVOKED` | H09, H10, H11, H12, H13 |
| `B5IngressM2Error` | `M2_RESOLUTION_REFUSED` | H23, H16 |
| `B5IngressAuthenticationError` | `IDENTITY_AUTHENTICATION_FAILED` | H04, H14, H18, H19, H25 |
| `B5IngressDeterminantError` | `DETERMINANT_CLOSURE_INCOMPLETE` | H24 |
| `B5IngressReplayError` | `REPLAY_CLOSURE_REFUSED` | H05, H06, H08 |

`B5IngressAuthenticationError` carries `mismatched_fields` (every failing key) and
`missing_keys` (only the absent subset), so **an incomplete owner setup stays
distinguishable from a complete expectation holding a different value.**

## 6. Trust-edge bindings

| B5 subject field | bound to | owner of the truth |
|---|---|---|
| `release_ref` | `M2.resolve_release_exact(...)` → `ReleaseCore.ref` | **ACCEPTED M2** (content-verified) |
| `producer_contract_ref` | `ReleaseCore.semantic_producer_contract_ref` | **ACCEPTED M2** |
| `semantic_projection_hash` | `ProducerSubject.semantic_anatomy_ref.content_hash` | **ACCEPTED M2** |
| `replay_root_ref` | M2 `REPLAY_RECONSTRUCTION` closure ref | **ACCEPTED M2** |
| `determinant_refs` / `determinant_set_hash` | M2 `DETERMINANT` closure ∪ consumed model+walkback authorities ∪ semantic-authority determinants ∪ custody — normalised to B5's own ordering, hashed by B5's own rule | **ACCEPTED M2** + frozen custody |
| `direct_dependency_refs` | M2 `DEPENDENCY` closure ∪ custody | **ACCEPTED M2** + frozen custody |
| `authority_snapshot_refs` | frozen owner custody | **owner** (residual R1) |
| `build_or_release_receipt_refs` | frozen owner custody | owner |
| `producer_permission_ceiling_ref` | frozen owner custody, **keyed by slot** — never derived, never taken from a subject | owner |
| `replay_state` | frozen owner custody, gated by the M2 replay closure's own `replay_grade` | owner (residual R2) |
| `product_ref`, `product_family_ref`, `producer_owner_ref`, `selection_scope_ref` | frozen owner custody | owner |

**Consumed model and walkback authorities are real determinant edges** (F8E H04 lesson) and
are separately revocation-checked (H09, H10). This is what makes a walkback revocation
*reach* this product rather than sitting inertly beside it.

## 7. Revocation

`RevocationLedger` holds exact **ref keys** — no wildcards, no fuzzy matching, no
`latest`-style tokens. Checked before anything is derived:

* `release_keys` → H12
* `authority_keys` against **semantic** snapshot identities → H11
* `authority_keys` against **consumed model/walkback** authorities → H09, H10
* `replay_closure_keys` → H13

## 8. The receipt

```python
B5IngressReceipt(
  contract="HQ280_C02_AUTHENTICATED_B5_INGRESS_CANDIDATE@1",
  development_grade="SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD__G1_HELD__CURRENT_HELD",
  slot, release_key, release_content_hash, producer_subject_key, producer_contract_key,
  semantic_anatomy_key, determinant_keys, determinant_set_hash, replay_closure_key,
  replay_grade, replay_root_key, receipt_keys, permission_ceiling_key,
  authority_snapshot_keys, consumed_authority_keys,
  registered_event_key, publication_event_key, ingress_authentication_hash,
  current_selection_performed=False, current_selection_receipt_ref=None,
  authorizing=False, grant=None, g0b=None, g1_service=None,
  scientific_competence_claim="NONE__TECHNICAL_PRODUCT_AUTHENTICITY_ONLY",
  technical_only_note="Technical product authenticity only. This is NOT a scientific, "
                      "model or use competence judgement, NOT a G0b grant, NOT a G1 "
                      "selected service, and NOT an operative CURRENT publication.",
)
```

`ingress_authentication_hash` is `semantic_hash` over the **full observed material, the full
expected material, and both B5 event refs** — a caller retaining only the published release
ref cannot reconstruct it. P05 proves it is content-addressed: two publishes over the same
owner material produce the identical hash; P07 proves two slots produce different hashes.

## 9. The boundary: technical authenticity ≠ scientific competence

This is enforced structurally, not just documented. C02 proves that a B5-published subject
**corresponds to material the accepted M2 owner actually issued**. It does **not** and
cannot decide whether the producer was competent to issue it. Every receipt is stamped
non-authorizing; `authorizing`, `grant`, `g0b`, `g1_service` are literally `False`/`None`
and asserted so (P02).

**C02 never performs current selection.** `publish()` asserts at runtime that no
`CURRENT_SELECTED` / `CURRENT_SUPERSEDED` / `CURRENT_CLEARED` event exists and that the
lifecycle state is exactly `PUBLISHED` (P04). A counterfeit CURRENT claim has no field to
arrive on (H02) and no code path to be honoured on.

## 10. What was deliberately NOT done

* No new G0b. No selected G1 service. No source authority. No operative CURRENT. No V3
  actor permission. No scientific/model/use issuance of any kind.
* No new registrar, credential, signature scheme or trust root.
* No modification to `pre553_learned_product_lifecycle.py` or
  `pre553_learned_product_release.py`. No `PROPOSED_UNADOPTED` diff is offered, because no
  correction to an existing owner proved indispensable — see `00_RETURN.md` §5.
* No raw source read, no SAV/DTA, no respondent-lineage republishing, no semantic or
  canonical mutation, no self-adoption.

## 11. Bounded residuals — stated, not buried

**Frozen (deeply, at every level):** the expected-identity map, the slot table, the custody
container, and the read-only projections returned by `owner_custody_projection()` /
`accepted_expected_identity()`. Item assignment, deletion and the mutating mapping methods
are refused (H27).

**Not frozen:** the `M2Repository` and the `ExactRef`/`AuthorityRef` objects inside custody
remain the owner's own shared objects. Deep-converting them would change the semantic ref
objects the accepted M2/B5 owners consume, which is out of scope here. A caller cannot reach
them through the public surface, but an in-process principal that already holds one can
still mutate it.

* **R1 — semantic `authority_snapshot_refs` are OWNER-HELD, not issuer-held.** No accepted
  AuthoritySnapshot issuer exists in the repository and C02 invents none. They are frozen
  and expectation-bound, which is an internal completeness invariant, **not** independent
  proof of authority issuance. A competent producer issuer remains the open prerequisite
  F8F recorded.
* **R2 — `REPLAY_COMPLETE` is an owner-held claim, not an independent replay
  re-execution.** C02 binds it to the M2 replay closure's own `replay_grade` and to the
  closed expectation, and refuses a grade outside the accepted vocabulary (H06, H07) or an
  incomplete closure (H08). `HISTORICAL_EXPLANATION_ONLY` remains permitted and is
  **labelled as such on the receipt** (P06); it must never be read as serving-grade replay.
* **R3 — the expectation is authored from the construction it authenticates.** It is a
  drift guard and a tamper detector, not an independent preimage. An in-process principal
  able to rewrite *both* custody and expectation is explicitly **UNPROVED**.
* **R4 — no defence against an attacker executing arbitrary Python inside the owner
  process.** The threat model is exactly the bounded data-only external caller of F8F
  K4–K5, widened to "a caller that may reach the C02 public surface". This is not deployed
  security and not a custody root.