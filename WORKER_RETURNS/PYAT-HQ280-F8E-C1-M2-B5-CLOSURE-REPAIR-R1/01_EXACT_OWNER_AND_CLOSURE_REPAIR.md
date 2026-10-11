# HQ280 F8E — Exact owner and closure repair

Authority: HQD-2026-10-10-280. Canonical observed `6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9`; PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (neither mutated). Sealed startup `6552be7b6e4a92654e98e5562d3e2b6f24d769bd`. Seed candidate `69bb0fc69175b2f6048b00cfa47dc852593798c0`.

Allowed tracked writes were limited to the F8D-new development candidate `rawlsing_next/pre553_c1_immutable_release_binding.py`, its test `rawlsing_next/tests/test_pre553_c1_immutable_release_binding.py`, and the files under this return directory. No adopted runtime owner, root manifest, raw survey, semantic law or canonical file was modified.

## Owners actually used at runtime

| Owner | Role | How it was exercised |
|---|---|---|
| `rawlsing_next/pre553_analytical_composition.py` (accepted blob `604c8d59…`) | produces the real `AnalyticalCompositionResult` and `PossibilitySliceEvidence` | every positive and every hostile object is a genuine composition built through the accepted owner path (`G1._compose` over the frozen XOR fixture) |
| `rawlsing_next/pre553_learned_product_release.py` (M2) | real repository, producer subject, five closures, release constitution | release/closure construction and the real M2 closure-completeness refusals in `n08` |
| `rawlsing_next/pre553_learned_product_lifecycle.py` (B5) | real lifecycle subject, stage/register/publish refusal | `p04` stages and registers, then shows publication and CURRENT selection still fail |
| `rawlsing_next/pre553_analytical_replay_dependency.py` + `pre553_authority_maintenance.py` | accepted `AnalyticalDependencyRegistry` / `SemanticDeterminantGraph` | registration, graph construction and `affected()` propagation |
| G1 fixture `test_pre553_ee14_c1_owner_authenticated_ingress_hq262` | real owner-side C1 cell plans and composition entry | supplies the honest q1/q2 identities used for pinning |

No mock, stub or monkeypatched owner substitutes for any of the above. The only monkeypatch in the suite is the original `n05` watchdog on `M2.register_producer_subject`, which asserts a call count of zero — it does not replace an owner.

## The five repairs

**H01 — cell identity from shape alone.** `_ALLOWED_CELLS` checked only conditioner count and denominator. A genuinely computed `q(C|A=0)` has arity 1 and denominator 2, identical to honest q1, and was accepted. Repair: per-cell pinned identity recorded from the accepted C1/query owner path — predicate hash, condition-binding witness hash, target ref, target domain identity and risk-set identity. An alien with the same shape now fails `CELL_PREDICATE_IDENTITY_MISMATCH`. These pins are **development preconditions describing the admitted native scope**, not an issued authority; no authority was manufactured, and where identity could not be proved the affected product is held.

**H02 — reversed numerator behind identical labels.** Honest q2 is `[('0',0),('1',1)]`; alien `q(C|A=1,B=1)` is `[('0',1),('1',0)]`. Both have denominator 1 and both sort to `[0,1]`, so the original sorted assertion could not distinguish them. Repair: an order-sensitive frozen numerator oracle (q1 `(1,1)`, q2 `(0,1)`) and pinned denominators (2 and 1). Defence in depth is intended: the predicate pin fires first, the numerator oracle is the independent second guard, and a dedicated test asserts the reversed profile `(1,0)` differs from the frozen oracle so the H02 guard cannot be vacuous.

**H03 — risk-set member cross-preimage.** `_verify` compared risk-set id and denominator member refs but never the member identities themselves, so a rehashed composition carrying substituted members passed. Repair: evidence-geometry `risk_set_member_refs` are cross-checked against `composition.risk_set_member_refs`, a coverage floor is added over the admitted denominator, and the per-cell risk-set identity is pinned. A rehashed alien now fails `RISK_MEMBER_PREIMAGE_MISMATCH`.

**H04 — consumed model and walkback authorities.** `PositionedSubjectPossibilityModelRule.model_authority_ref` and `.walkback_authority_ref` were represented only through the model-rule hash, so they were absent from the M2 AUTHORITY closure, the B5 snapshot and every authority edge. Repair: both are unioned into `auths` as separate exact `AuthorityRef` members. Measured effect: the AUTHORITY closure grew and the graph now carries 6 authority edges; `affected([model_authority_ref])` reaches the product while an unrelated authority does not.

**H05 — C1-03R graph under-projection.** Registration stored `determinant_exact_refs` (31) but declared `dependency_edges_from` (22); the accepted registry only emits edges from `dependency_edges_from`, so 9 determinant identities including the model-rule ref were never traversed. Repair: the full determinant closure is declared as the edge source, with explicit post-conditions asserting one edge per determinant and authority propagation. Measured effect: 31 dependency edges for 31 determinants, and every determinant is a real edge parent.

## Ceilings preserved

Nonissuing development family, `grant=None`, `external_issuer=None`, `authorizing=False`, `REPLAY_BLOCKED_MISSING_AUTHORITY`, `REBUILD_BLOCKED`, historical-only C1-03R replay, and I4 M1-only are all unchanged and re-verified. Publication, CURRENT selection, G1 serving and operative G0b still fail — proven by the still-passing original tests `p04`, `n09` and `n10`. No source-scientific or model-use expansion was made.
