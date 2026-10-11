# 01 — Producer → B5 caller graph and the actual trust boundary

Traced by reading the accepted owners in this worktree at HEAD
`c6e986dfa02b80887ded5f4d0da2e2413e676172`, and confirmed by **actual invocations**
(`repro/repro_f8f_k4_k5_boundary.py`, log `repro/c02_boundary_repro.log`). Every line
number below is from that exact tree.

---

## 1. The owners that exist

| owner | file | what it owns | what it explicitly does **not** own |
|---|---|---|---|
| **B5 lifecycle** | `pre553_learned_product_lifecycle.py` | registration, publication, selection, supersession, withdrawal, replay, rebuild, GC | *"producer semantics, M2 release-core semantics, AuthoritySnapshot maintenance, consumer permission, source/carrier retirement…"* (module docstring, lines 11–13) |
| **M2 release** | `pre553_learned_product_release.py` | producer-owned subject → immutable `ReleaseCore` → publication binding → exact `ResolutionReceipt` | *"lifecycle publication/currentness, semantic adjudication, consumer permission…"* (lines 10–11) |

These two owners are **adjacent but not connected**. There is no adapter, no registry and
no credential binding them anywhere in the repository. That gap is the whole finding.

## 2. The real caller graph into B5 (traced, not assumed)

```
   WHOEVER CALLS B5 — any holder of a constructed object
        │
        ├─ LearnedProductLifecycleSubject(...)          line 320   ← FROZEN DATACLASS, PUBLIC CTOR
        │      .__post_init__()                         line 345   shape validation ONLY
        │
        ├─ LearnedProductLifecycleSubject.from_protocol()line 405   duck-typed attribute read
        │      (LearnedProductReleaseProtocol is runtime_checkable → attribute PRESENCE only,
        │       per the code's own comment at line 407; and `**overrides` is caller-supplied)
        │
        ├─ LearnedProductLifecycleSubject.from_dict()   line 454   ← REHYDRATION BYPASS
        │      (a plain mapping is a complete subject)
        │
        ▼
   executor.stage_release(subject)                     line 1468  ← NO AUTHENTICITY CHECK
        │      isinstance(subject, LearnedProductLifecycleSubject)   ← the ONLY gate
        │      + same-release-idempotence / product-hash conflict
        ▼
   executor.register_product(release_ref, ...)          line 1570
        │      event_authority_ref / event_rule_ref are bare caller-supplied ExactRefs
        ▼
   executor.publish_product(release_ref, ...)          line 1632
        │      line 1644: if subject.replay_state != "REPLAY_COMPLETE": refuse
        │      line 1646: if not subject.authority_snapshot_refs: refuse   ← UNREACHABLE
        │      line 1648: if not subject.determinant_refs:         refuse   ← UNREACHABLE
        │      (both are already guaranteed by __post_init__ at lines 363–366 and 372–374,
        │       and the state defaults to "REPLAY_COMPLETE" at line 341)
        ▼
   executor.select_current(selection_key_ref, release_ref, ...)  line 1760
        │      _selection_subject_ok() line 1742 — checks PUBLISHED + VALID + family/scope only
        ▼
   CURRENT_SELECTED receipt
```

## 3. Where each claimed identity is actually sourced

This is the decisive table. **Not one** of these is bound to anything a producer issued:

| subject field | consumed by B5 at | sourced from | verified against anything the producer issued? |
|---|---|---|---|
| `replay_state` | 1644, 2307, 2483 | caller literal (default `"REPLAY_COMPLETE"`, line 341) | **NO** |
| `authority_snapshot_refs` | 1646 | caller literal | **NO** — no issuer exists in the repo |
| `determinant_refs` / `determinant_set_hash` | 1648 | caller literal (only self-consistency, 375–380) | **NO** |
| `replay_root_ref` | 1657 (event payload) | caller literal | **NO** |
| `build_or_release_receipt_refs` | 1599 (event payload) | caller literal | **NO** |
| `producer_permission_ceiling_ref` | 1662 (event payload) | caller literal | **NO** |
| `producer_contract_ref` | 1589 | caller literal — **never checked against the M2 owner** | **NO** |
| `event_authority_ref`, `event_rule_ref` | 1581, 1637 | caller literal, every call | **NO** — no authority registry is consulted |

Verified independently by grep: `producer_permission_ceiling_ref` appears **only as a
consumed field** across `rawlsing_next/` (in B5 and in `pre553_learned_world_composition.py`);
there is no issuer for it, and no registry that could authenticate it.

## 4. Actual outcome, measured

```
C02 OBSERVED: 4/5 caller-constructed subjects reached PUBLISHED and 4/5 reached CURRENT_SELECTED.
```

Including one whose closure, receipts and replay root were entirely fabricated, and one
whose forged `urn:reviewer:PRODUCTION_GRANT` permission ceiling was stored **verbatim**
into the committed `PRODUCT_PUBLISHED` event payload.

## 5. Root cause, stated precisely

The B5 publication gate is a **well-formedness gate, not a provenance gate**. F8F said
this. C02 confirms it and names the mechanism: the three checks at lines 1644/1646/1648
are either (a) satisfied by `__post_init__` before they run, or (b) defaulted-on by the
dataclass field default at line 341. **They are not checks on caller input; they are
restatements of the constructor.**

## 6. Where enforcement belongs, and why not inside B5

Three candidate placements were considered:

1. **Inside `LearnedProductLifecycleExecutor.publish_product`.** *Rejected.* B5's module
   contract disclaims producer and M2 semantics. An authenticity gate there would either
   (a) invent a producer-credential authority inside a semantic owner, or (b) couple B5 to
   M2 across a jurisdiction boundary the adopted contracts deliberately separate. Both are
   canonical semantic owner mutations, which this commission forbids.

2. **A new registrar / credential / signature scheme.** *Rejected.* None is granted; F8F
   itself recorded that closing this needs "a producer-issued subject credential — a new
   authority, not a repair."

3. **A candidate-only owner-controlled perimeter in front of B5, whose trust edge is the
   EXISTING accepted M2 owner.** *Adopted.* The M2 owner already content-verifies its own
   releases (`_verify_release_core`, line 743), resolves exact closures out of a real
   repository, and refuses foreign bindings and re-ownership. It is the smallest trusted
   ingress that already exists.

**Consequence for the semantic owner: zero. `pre553_learned_product_lifecycle.py` and
`pre553_learned_product_release.py` are byte-identical to the sealed startup.** Both are
imported and called, never edited (H28, H29 spy on the real owners to prove it).

## 7. The custody graph C02 actually installs

```
 OWNER (trusted harness, construction-time only)
   │
   ├─ M2Repository ──►  M2.resolve_release_exact(release_ref)     [ACCEPTED OWNER, unmodified]
   │        │                       content-verified ReleaseCore
   │        ├─ release_ref                     ← M2-issued
   │        ├─ producer_contract_ref           ← M2-issued
   │        ├─ semantic_projection_hash        ← ProducerSubject.semantic_anatomy_ref
   │        ├─ replay_root_ref                 ← M2 REPLAY_RECONSTRUCTION closure ref
   │        ├─ determinant_refs                ← M2 DETERMINANT closure ∪
   │        │                                     consumed model/walkback authorities ∪
   │        │                                     semantic-authority determinants ∪ custody
   │        └─ direct_dependency_refs          ← M2 DEPENDENCY closure ∪ custody
   │
   ├─ ProducerCustodyMaterial (frozen)     product/family/owner/scope, semantic AuthoritySnapshot
   │                                     refs (R1), receipts, PERMISSION CEILING,
   │                                     consumed authority refs, required replay grade,
   │                                     replay state (R2), COMPLETE expected identity
   │
   ├─ RevocationLedger (frozen)           revoked release keys / authority keys /
   │                                     replay-closure keys
   │
   ▼
 publish(PublicationRequest(slot))   ← the ONLY public surface; data-only, one str field
   │
   ├─ 1 M2 resolution            2 revocation gate      3 replay-grade gate
   ├─ 4 determinant derivation   5 OWNER BUILDS subject 6 DEEP AUTHENTICATION
   │                                                                  │
   └─────────────────────── only now ────────────────────────────────┘
                                    ▼
              B5.stage_release → register_product → publish_product
                                    ▼
              receipt: authorizing=False, grant=None, g0b=None, g1_service=None,
                      current_selection_performed=False, scientific_competence_claim=NONE
```

Nothing on the left of the deep-authentication step is reachable from the public surface.
That is the structural fix: the caller cannot express a forgery, so there is nothing to
validate on their behalf.

## 8. F8E / F8F carry-forward, and where C02 differs

* F8E H04's lesson (**consumed model and walkback authorities must be real determinant
  edges**) is adopted directly: C02 derives them into `determinant_refs` *and* lists them
  in `consumed_authority_refs`, so a walkback revocation reaches this product (H10).
* F8E H05's lesson (**every determinant is a real graph edge**) is preserved: the determinant
  set C02 hands B5 is exactly what B5's `from_subjects` turns into edges (line 1243).
* F8E's **four-XOR source-free-only** scope, `grant=None`, `authorizing=False`,
  `external_issuer=None`, `DEVELOPMENT_GRADE`, G0b/G1/CURRENT holds are all preserved. C02
  adds no scientific content and reads no source.
* **C02 differs from F8F in one respect of substance:** F8F recorded the boundary at
  *publication*. C02 reproduces it at publication **and** current selection, and additionally
  probes (K7) a subject fabricated purely from caller dictionaries with no producer input
  whatsoever.
* F8E's candidate module `pre553_c1_immutable_release_binding.py` is **absent from this
  worktree's HEAD** (it exists only on the F8E line, branched from `6a8c91d99…`). C02
  therefore builds its own genuine M2 fixture rather than depending on an unavailable
  sibling artifact. Recorded so nobody reads this as a silent omission.