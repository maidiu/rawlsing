# PYAT HQ281 R02 — Independent hostile review: actual V2 and durable batch integration

**TERMINAL:** `HQ281_R02_BOUNDED_PRODUCT_OR_EXACT_HOLD__GITHUB_PUSHED`
**DISPOSITION:** `EXACT_HOLD__CANDIDATES_CANNOT_COMPOSE__NO_LAWFUL_INTEGRATION_TREE_EXISTS`
**Branch:** `agent/reviewer-pyat-hq281-r02-v2-batch-integration-hostile-r1` @ `eaf838ed42d924c3185f9e158b2da03c91eb3e40`
**B01E:** `92cb25340c49fb51e2b8d6e00d5a4f471296fc8f` · **A04TU:** `d6e766cd6ba7dc46b19cc61123d968a274015ddd`
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated). **ZERO code changes to candidates or accepted owners.**

## 1. What I actually reproduced

| suite | tree | collected | passed | failed | exit | wall |
|---|---|---|---|---|---|---|
| B01E governed-batch durable integration | `92cb2534` code | **29** | **29** | 0 | 0 | 73.85 s (includes the three real SIGKILL windows) |

Blobs verified: governed-batch `44807c6a287145507d7332138c944cd61da363bf`; its durable dependency `719c8d878bcfb3b6c61c844c9bf974ada8365929` — **byte-identical to the B01D fail-closed core I independently reviewed in B01DR**, so B01E genuinely builds on the repaired durable layer and inherits the closed `RERUN_SAFE` forge path.

A04TU's own suite was **not reproducible as a separate code candidate** — see §2: `d6e766cd` adds **no `rawlsing_next/` code at all** (return/evidence only).

## 2. THE EXACT HOLD — the two candidates cannot compose

I did not assume they live on one branch; I measured it. The cross-tree presence matrix is a clean **mutual exclusion**:

| module | B01E `92cb2534` | A04TU `d6e766cd` | reviewer HEAD `eaf838ed` |
|---|---|---|---|
| `pre553_governed_batch_checkpoint_integration_candidate.py` | **PRESENT** | **ABSENT** | **PRESENT** |
| `pre553_original_workload_v2_verifier_candidate.py` | **ABSENT** | **PRESENT** | **ABSENT** |
| `pre553_batch_durable_checkpoint_candidate.py` (B01E's dependency) | PRESENT | **ABSENT** | — |

Consequences, stated exactly:

- A04TU's tree **does not contain the durable batch candidate at all** — not merely the V2 verifier's counterpart, but the *dependency* — so nothing on `d6e766cd` can import the durable layer.
- B01E's tree **does not contain the V2 verifier**, so nothing on `92cb2534` can verify an expected universe.
- **No accepted branch carries both in one importable tree.** Composition would require an integration commit that does not exist.

**Exact owner-level missing join:** *no accepted owner supplies an integration module that binds `pre553_governed_batch_checkpoint_integration_candidate` (with its durable dependency) to `pre553_original_workload_v2_verifier_candidate` in a single importable tree.* Constructing one myself would be precisely the fabricated green run the commission forbids, so I did not.

Also noted: **A04TU is an evidence/return commit, not a code candidate.** The commission's "A04TU reports 44+29 clean tests" therefore describes the **A04T V2 verifier** suite (44, which I reviewed in A04TR) plus 29 of its own hostiles — not 73 tests of a composable second implementation.

## 3. Grades (kept separate, as ordered)

| dimension | grade |
|---|---|
| **V2 TECH** | **ACCEPTED (narrow)** — from A04TR: versioned native verifier, raw-field recomputation; one self-referential test defect |
| **BATCH DURABLE** | **ACCEPTED (narrow)** — B01E 29/29 on the B01D `RERUN_SAFE`-closed core |
| **COMPOSED RUN** | **FAIL / NOT AVAILABLE** — exact disjointness above |
| **INDEPENDENT E CUSTODY** | **NOT ESTABLISHED** — no external custodian seals the expected payload pre-execution |
| **SOURCE USE** | **NOT GRANTED** — no raw SAV/DTA read, no source warrant |
| **REAL CONSUMER** | **NOT ESTABLISHED** |
| **REAL_EXECUTION** | **NOT GRANTED** |
| **ALL35** | **NOT CLAIMED** — 35 waves / 63 temporal syntactic pairs and every HELD/DENIED/NA preserved and untouched |

## 4. Hostiles — what I ran, and what I decline to claim

**Ran:** B01E's full 29-test suite on its own exact committed tree, including its three real SIGKILL windows (74 s of genuine process work, not simulated); blob verification of both B01E modules; the cross-tree module presence matrix; verification that B01E's durable dependency is the B01D core I previously attacked.

**Not run, and recorded as blocked by the join rather than as PASS:** unified unknown-side-effect-before-COMMIT across the composed stack, head-blocking vs forbidden skip through a V2 expectation, failed/deferred pin against a V2 key, forged idempotence against the *composed* path, manifest/work-key mismatch across the two trees, foreign source/release authority through the V2 verifier, altered actual consumer, and producer-self-generated E. Every one of these requires both modules in one tree; that tree does not exist. **Naming them as unavailable is the honest result; marking them green would be fabrication.**

**Terminal:** `HQ281_R02_BOUNDED_PRODUCT_OR_EXACT_HOLD__GITHUB_PUSHED`.
