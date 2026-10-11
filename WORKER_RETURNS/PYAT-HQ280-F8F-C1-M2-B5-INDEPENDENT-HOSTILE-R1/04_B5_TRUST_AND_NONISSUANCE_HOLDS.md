# HQ280 F8F — B5 trust boundary and non-issuance holds

## 1. The residual, stated precisely

**Finding (owner-level, reproduced by actual invocation):** `pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor` treats the caller-supplied `LearnedProductLifecycleSubject` as **trusted input**. Its publication gate verifies the *shape* of a replay-closure claim and then publishes; it does **not** verify the provenance or authority of any identity on the subject.

Evidence (four real invocations; no static assertions):

| probe | subject mutation | actual outcome |
|---|---|---|
| K4 | `replay_state = "REPLAY_COMPLETE"` forged | **PUBLISHED** |
| K5a | honest `replay_state`, fake `ProducerPermissionCeiling("urn:reviewer:PRODUCTION_GRANT")` | refused — **reason is the replay closure**, not the ceiling |
| K5b | forged `replay_state` **+** fake production ceiling | **PUBLISHED**; the executor stores the fake ceiling verbatim |
| K5c | forged `replay_state` + fake `build_or_release_receipt_refs` + fake `replay_root_ref` | **PUBLISHED** |

**Therefore:** B5's publication gate is a **well-formedness** gate, not a **provenance** gate. Any caller who can construct a `LearnedProductLifecycleSubject` — which is a plain frozen dataclass — can publish a "product" whose closure, receipts, replay root and permission ceiling are entirely fabricated.

**Why this is not a defect in F8E's repair:** F8E disclosed it, did not claim to fix it, and the candidate never asserts otherwise. It is a **pre-existing, correctly-recorded limitation of an accepted owner**, and it is out of the candidate's declared source-free scope to fix (fixing it would require a producer-issued subject credential — a new authority, not a repair).

**Why it nevertheless blocks adoption beyond development grade:** the moment any publication, CURRENT selection, serving or operative use is trusted on the strength of a B5 receipt, this boundary becomes a live forgery path. It must be closed **before** the candidate is promoted past development scope.

## 2. What F8E's candidate *does* correctly hold

Re-verified at runtime, unchanged by this review:

- `DEVELOPMENT_GRADE = "SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD"`, `authorizing=False`, `grant=None`, `external_issuer=None`.
- `requested_replay_grade` must equal the historical M2 grade; `FRESH_PROCESS_REPLAY` is refused (K8, `REPLAY_GRADE_OVERCLAIM`).
- Native nonpositive C1 cannot mint an M2 product (K7, `C1_NATIVE_NONPOSITIVE`).
- Publication and CURRENT selection still fail for the candidate's own subject (`p04`), and no selected-service path exists (`n10`, I4 M1-only) — the candidate mints **no** selected T1 service.
- `REPLAY_BLOCKED_MISSING_AUTHORITY` and `REBUILD_BLOCKED` remain the honest typed states.

## 3. Non-issuance holds (unchanged, and NOT granted by this PASS)

1. **Competent producer issuer** — still absent. The candidate issues no `AuthoritySnapshot` and is not a producer-origin credential.
2. **Operative G0b model use** — HELD. The H04 repair records *consumed* model/walkback authorities as closure members; recording a consumed authority is not issuing model use.
3. **B5 provenance** — HELD pending a producer-issued subject credential (see §1).
4. **G1 selected-service / serving** — HELD. No authenticated ingress path is exercised or created here.
5. **CURRENT / currentness / replay currentness** — HELD; historical explanation only.
6. **Source-scientific and raw-source use** — not granted. No raw survey, no `SAV`/`DTA`, no source re-read was executed in this review.
7. **World / N9 / N10W / V3 / actor** — untouched.
8. **Production / canonical / PRE-MAIN / root-manifest mutation** — none.

## 4. Adoption recommendation (technical only)

**The candidate qualifies for narrow, staged, DEVELOPMENT-LEVEL technical adoption** at its declared source-free scope: all five repairs are independently confirmed at owner level and 280/280 independently executed tests pass.

Adoption should be recorded **with the B5 provenance limitation as an explicit condition of grade**, so that no downstream consumer reads a development-grade B5 publication as provenance-bearing. Any promotion beyond development scope requires, at minimum: (a) a producer-issued subject credential closing §1, (b) a competent producer issuer, and (c) the separate G0b/G1/CURRENT decisions listed in §3.

**Terminal:** `HQ280_F8F_INDEPENDENT_C1_M2_B5_HOSTILE_RUNTIME_RETURNED__NONISSUING__GITHUB_PUSHED`.
