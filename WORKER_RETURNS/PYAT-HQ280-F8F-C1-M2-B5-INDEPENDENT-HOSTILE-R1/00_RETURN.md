# PYAT HQ280 F8F — Independent hostile exact runtime review of F8E repaired source-free C1→M2/B5 R1

**TERMINAL:** `HQ280_F8F_INDEPENDENT_C1_M2_B5_HOSTILE_RUNTIME_RETURNED__NONISSUING__GITHUB_PUSHED`
**TECHNICAL GRADE:** `DEVELOPMENT_CANDIDATE_READY_FOR_NARROW_STAGED_HQ_TECHNICAL_ADOPTION__FIVE_REPAIRS_INDEPENDENTLY_CONFIRMED__ONE_RECORDED_RESIDUAL_TRUST_BOUNDARY__NONISSUING`
**Branch:** `agent/reviewer-pyat-hq280-f8f-c1-m2-b5-independent-hostile-r1` @ `f82bf8de50b5a76b71ff12063f5fff95efc33511`
**Candidate:** `agent/rabochii-pyat-hq280-f8e-c1-m2-b5-closure-repair-r1 @ 2a4a90ec76d3400f98ba6fd3fd306f6ff977d042`
**Authority:** HQD-2026-10-10-280 · canonical `6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated). **No self-adoption.**

## 1. Independent runtime — actual, not simulated

Executed in a real local Git worktree at the sealed tip with the pinned interpreter (Python 3.11.3, **pytest 9.1.1** — F8E reported 9.0.2; same tests, same outcome, so the result is not patch-version dependent).

| suite | collected | passed | failed | exit | F8E claim | match |
|---|---:|---:|---:|---:|---|---|
| F8E candidate suite | 23 | **23** | 0 | 0 | 23 passed | **EXACT** |
| adjacent 4 adopted owners | 123 | **123** | 0 | 0 | 123 passed | **EXACT** |
| C1-03R join + G1 ingress fixture | 124 | **124** | 0 | 0 | — | — |
| **reviewer-injected hostiles** | 10 | **10** | 0 | 0 | — | — |
| **total independently executed** | **280** | **280** | 0 | 0 | | |

Candidate bytes verified: module blob `36563ddee5b6c1fe44940712ec85ba7a3156fb5d` (sha256 `460547ad…`), test blob `1e972bf9199278c715deedce6a52dd2be1b3ec55` (sha256 `1af1289c…`) — both **exact** against the commission and against F8E's own `02_ACTUAL_TEST_RUN.json`.

**Terrain note (honesty):** the adjacent suites first errored here purely because sibling fixture artifacts (`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/-R3/-R8`) lay outside the sparse checkout. Materialising them restored 123/123. That is a **checkout-scope gap, not a candidate regression** — recorded so nobody reads the initial errors as a defect.

## 2. The five repairs — independently confirmed at owner level

Each was re-tested with my own adversarially mutated inputs against the real accepted owners, **not** by re-running F8E's assertions alone:

| repair | my independent probe | actual owner outcome |
|---|---|---|
| H01 cell identity from shape | recompute q1 from a **different** condition set (same arity, same denominator) and submit it as `q1` | **REFUSED** (`*_IDENTITY_MISMATCH`) — K6 |
| H02 reversed numerator | order-sensitive frozen oracle `q1 (1,1)` / `q2 (0,1)` with pinned denominators 2 / 1 | guard present and non-vacuous |
| H03 risk-member cross-preimage | substituted members with a valid rehash | **REFUSED** (`RISK_MEMBER_PREIMAGE_MISMATCH`) |
| H04 model/walkback authority closure | real `affected()` invocation | product **is** reached; **unrelated authority does NOT propagate** — K1/K2 |
| H05 C1-03R graph under-projection | edge-parent/child inspection over the live graph | **every determinant is an edge parent; every edge terminates at the product; no unsupported edge** — K3 |

## 3. Where F8E's own tests were weaker than they read (graded honestly)

F8E labels all eight additions "genuinely injected hostile regressions". On inspection they are a **mixture**:

- `h01`, `h02`, `h03` — genuine injections (an alien/mutated object is built and submitted to the owner); my K6 independently reproduces the class.
- `h04`, `h05`, `h05b` — predominantly **static membership assertions** over an already-built view, plus real `affected()` calls. `h02b` is a scope-equality check.
- **Not tested by F8E at all:** `affected()` **order invariance** and **subset mutation**, which the commission explicitly requested. I added them (K1, K2) — both pass.

This does not overturn F8E's GREEN result; it corrects the *description* of the evidence.

## 4. The one recorded residual — B5's caller-supplied lifecycle trust boundary (STILL OPEN)

This is a **real owner-level finding from actual invocations**, not a static assertion:

| probe | actual outcome |
|---|---|
| **K4** caller supplies `replay_state="REPLAY_COMPLETE"` on a rebuilt subject | **PUBLISHED** — B5 accepts the forged closure claim |
| **K5a** honest `replay_state` + fake production-looking `ProducerPermissionCeiling` | refused — but the reason is the **replay closure**, not the ceiling |
| **K5b** forged `replay_state` + fake production ceiling | **PUBLISHED**, and the executor stores the caller's fake ceiling verbatim |
| **K5c** forged `replay_state` + **fake `build_or_release_receipt_refs` and fake `replay_root_ref`** | **PUBLISHED** |

**Conclusion:** `LearnedProductLifecycleExecutor` treats the caller-supplied `LearnedProductLifecycleSubject` as trusted. It validates that a replay closure *claim* is present, and **never validates the authority of the subject's closure refs, receipt refs, replay root or permission ceiling**. F8E correctly disclosed this ("the B5 trust-boundary limitation recorded by F8D-R still stands"), but it is worth stating precisely: **the publication gate is a well-formedness gate, not a provenance gate.** At development/source-free scope this is acceptable and non-issuing; it is a hard blocker for any serving, CURRENT-selection or operative use until a producer-issued subject credential exists.

## 5. Item-by-item commission coverage

| # | requirement | result |
|---|---|---|
| 1 | actual worktree, blobs, versions, rerun 23 + adjacent | **DONE** — 280/280 |
| 2 | hostile-review the five repairs against real owners; distinguish owner rejection from static comparison | **DONE** — §2/§3 |
| 3 | source-free fixture numerator `(1,1)`/`(0,1)` and predicates genuinely restricted to four-XOR scope | **CONFIRMED** — `_ALLOWED_CELLS = {"q1":(1,2),"q2":(2,1)}`, `CELL_OUT_OF_SCOPE` refusal, per-cell pinned predicate/witness/target/risk identity; **no generic C1 binding and no model-use claim** is minted (K6/K7 prove refusal is by identity, not by shape) |
| 4 | B5 caller-supplied trust boundary | **GAP RECORDED** — §4, four actual invocations |
| 5 | authority closure AND affected propagation, subset mutation, order invariance | **DONE** — K1/K2/K3 |
| 6 | native unsupported/`VALID_EMPTY` cannot mint M2; q1/q2 alignment; I4 M1-only; historical replay ≠ CURRENT/G1 | **CONFIRMED** — K7 (`C1_NATIVE_NONPOSITIVE`), K8 (`REPLAY_GRADE_OVERCLAIM`), and the still-passing `p04/n09/n10` |
| 7 | exact technical grade + separate holds | **DONE** — §6 |

## 6. Grade, and the holds that remain

**Technical grade:** the repaired source-free C1→M2/B5 candidate is **ready for narrow, staged, development-level HQ technical adoption** at the declared source-free scope. All five F8E repairs are independently reproduced at owner level; 280/280 tests pass; the candidate's own non-issuing ceilings (`grant=None`, `authorizing=False`, `REPLAY_BLOCKED_MISSING_AUTHORITY`, `REBUILD_BLOCKED`, historical-only, I4 M1-only) are intact.

**Adoption of this candidate would still NOT grant, and must not be read as granting:**

1. **B5 provenance.** The caller-supplied subject boundary (§4) must be closed by a producer-issued subject credential before any publication/CURRENT serving is trusted.
2. **Competent producer-issuer.** Still missing; no `AuthoritySnapshot` is issued by the candidate.
3. **G0b operative model-use** — HELD.
4. **G1 selected-service / serving** — HELD; the candidate mints no selected T1 service.
5. **CURRENT / replay currentness** — HELD; historical explanation only.
6. **Source-scientific and raw-source use** — not granted; no raw survey was executed here.
7. **World / N9 / V3 / actor** — untouched.

**Terminal:** `HQ280_F8F_INDEPENDENT_C1_M2_B5_HOSTILE_RUNTIME_RETURNED__NONISSUING__GITHUB_PUSHED`.
