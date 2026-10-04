# HQ204 — C1 accepted-lineage surgical reconciliation — R1

**Disposition: `ACCEPTED_C1_OWNER_SET_RECONCILED_ON_CURRENT_CONTROL__AT_DECLARED_ACCEPTED_GRAIN__C4_STILL_UNAUTHORIZED`**
**Terminal: `HQ204_ANALYTICAL_CONTROL_RECONCILIATION_RETURNED__HQ_REVIEW_REQUIRED`**

Bounded integration lane. No raw-source access, no live C4, no C7, no actor/person
implementation, no self-adoption, **no wholesale merge of the accepted branch**.

## Identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq204-c1-r1` |
| Startup SHA (exact, verified) | `50fdc737deeb21c88f6f07a326e76680481dc753` |
| Current-control base | `ff4f06954824a3a5699bc5c1c9bd68cb3c5b4146` |
| HQ168 accepted integration | `149c3d2636160d8de9b5a8be0c8b87195158077d` |
| HQ168 accepted result | `063ee8b77fc4e05c37456ff0168e946247f919ef` |
| Tested code ref | `933a3d31aa961719c73e6ce7eebcfe40bc8cd45e` |
| Final independent review | `c8ce0ea81a2165f37d566f37de788fecedf85051` |

Only the exact governed branch ref was fetched. All five commissioned reference SHAs
were confirmed present.

**Divergence measured:** merge base `87029d349` (HQ163), **183 C1-only** vs **256
control-only** commits. Neither is an ancestor of the other — genuinely diverged, as
HQ204 stated.

## Method: acceptance was never inferred from side-branch presence

The HQ168 adoption document and the final independent review **independently declare
the same five production owner blob SHAs**. Every one was verified against
`git ls-tree` at the accepted result *before* classification.

### Production owner classification

| Path | HQ168 blob | Control before | Classification |
|---|---|---|---|
| `pre553_analytical_composition.py` | `604c8d59…` | absent | `ABSENT__MUST_IMPORT` |
| `pre553_empirical_possibility_provider.py` | `23167aa2…` | absent | `ABSENT__MUST_IMPORT` |
| `pre553_analytical_state_and_route.py` | `3a5e3db8…` | absent | `ABSENT__MUST_IMPORT` |
| `pre553_analytical_replay_dependency.py` | `47e65aad…` | absent | `ABSENT__MUST_IMPORT` |
| `pre553_authority_maintenance.py` | `547e6bf2…` | `ac7f3a01…` | `COMPATIBLE_CURRENT_SUCCESSOR` |

> **The mission named four analytical modules. HQ168 accepted five.** The fifth is
> `pre553_authority_maintenance.py`. Importing only the four named would have left
> the accepted owner set incomplete.

### Dependencies: nine already present, byte-identical

`pre553_c11_repository`, `pre553_discovery_adaptive`, `pre553_discovery_exact`,
`pre553_empirical_authority`, `pre553_empirical_objects`, `pre553_empirical_query`,
`pre553_recursive_handoff`, `pre553_structural_admission`, and
`source_backed_positioned_subject_possibility` — all `SAME_BLOB_ALREADY_PRESENT`,
none touched by this lane. This is why the accepted owners import cleanly with no
source-specific adaptation.

### No owner collision — STOP condition not triggered

`ACCEPTED_OWNER_COLLISION__HQ_ADJUDICATION_REQUIRED` was **not** triggered, on two
specific findings:

**1. `pre553_authority_maintenance.py` is a weaker earlier variant of the *same*
owner, not a competitor.** Both sides descend from commit `215932d08`; the accepted
side then applied three coherent C1-03R commits. Control took a different path and
holds 437 fewer lines.

The one substantive difference is a **generalization, not a conflict**. Control
enforces `set(recompilation_pairs) == affected_keys`, forcing *every* affected
dependent to carry a recompilation pair. The accepted version replaces this with a
strictly stronger outcome-based invariant: every affected dependent requires exactly
one **outcome**, may not receive both a replacement and a noncurrent disposition, and
an outcome naming a dependent outside the affected set is refused. Exact coverage is
still enforced; the disjointness guard is preserved. Control is a functional
**subset**, so the restoration is same-grain, not a conflict I had to adjudicate.

Restored capability absent from control: `NO_CURRENT_NO_LAWFUL_REPLACEMENT`,
`CURRENT`/`EXPLICIT_NONCURRENT`/`NOT_GOVERNED`, the noncurrent receipt schema, and
`NoncurrentDependentOutcome`.

**2. `source_backed_positioned_subject_possibility.py` is the upstream consumer, not
a rival.** This was the highest-risk collision candidate. The accepted provider's own
ownership law names it as the accepted public possibility consumer, and the provider
imports it. Producer-upstream, consumer-downstream.

### `HISTORICAL_ONLY__NOT_PART_OF_ACCEPTED_GRAIN`

Historical R8 spine, the historical failed court (`434 passed / 1 failed`), and no
historical-R8 production or test file — none absent from control, none imported.

## What was integrated

84 paths, all at byte-exact accepted blobs: **82 additions, 2 modifications**.

- 5 production owners (4 added, 1 restored)
- 6 test files added, 1 test file restored
- 9 test-support files added
- 63 authority-material files across 4 directories

Integration used `git checkout <accepted-sha> -- <exact paths>`, which writes
byte-identical blobs **without importing any side-branch history**. Zero side-branch
commits imported; current-control ancestry preserved.

### Authority material that was also missing

Three `PYAT-C1-00-CONTRACT-CORRECTION-R{2,3,8}` directories and the
`PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1` freeze were absent from control.
Without them the courts fail closed. The AT07 forward/reverse identities inside the
imported fixture match the HQ168 adoption exactly — an independent cross-check.

## Court: exact reproduction

The exact 15 court **file names** were not recorded by either authority — only
per-file counts. The court was reconstructed to an **exact multiset match** and
**exact total**:

```
declared : 92 57 54 43 43 35 32 28 17 14 13 13 8 3 2   = 454
rebuilt  : 92 57 54 43 43 35 32 28 17 14 13 13 8 3 2   = 454
```

The residual `143` resolved because the accepted dependency closure's control-resident
tests sum to exactly `32+17+14+13+8+54+3+2 = 143`.

**Result: 454 collected, 454 passed, 0 failed, 0 errors, 0 skipped — twice**
(69.76s, 68.00s). This matches HQ168's accepted court exactly. Execution was
available here, so the committed court was **re-run**, not accepted documentarily.

### One shared test file had also diverged

Control's `test_pre553_authority_maintenance.py` carried **zero** references to the
noncurrent lifecycle layer the restored owner introduces. Restoring only the module
would have left the accepted owner uncovered. The accepted test blob carries 94 such
references and collects **57** versus control's 21.

## Eight accepted-grain properties proved

| Property | Evidence |
|---|---|
| Direct exact analytical route | `compose_positioned_subject_possibility`, `build_state_route_result`, `assert_route_not_laundered` |
| I05 / discovery route | `classify_discovery_receipt_state`, `classify_adaptive_coverage`; 3 discovery courts green |
| Higher-order / recursive route | higher-order court 35 green; `pre553_recursive_handoff` SAME_BLOB |
| Ordered joint targets | positioned-subject court 13 green; `SEMANTIC_ORDERED`, `joint_component_count 1` |
| Complete cell geometry | `classify_empirical_cells`; r7 geometry-cell hostile cases |
| Negative / refusal preservation | `FAIL_CLOSED`, `NONCOMPARABLE`, `VALID_EMPTY`, `UNRESOLVED`; `NOT_GOVERNED`; r6 stale-ref fail-closed |
| Replay / dependency / currentness | `assert_replay_claim`, `resolve_current_analytical_product`; `CURRENT`/`EXPLICIT_NONCURRENT`/`NOT_GOVERNED` |
| Positioned-subject consumer linkage | provider imports and delegates to the control-resident consumer, per its own ownership law |

## Regression: zero new failures

A **manifest-identical detached worktree at the startup SHA** gave a true baseline.

| | before | after |
|---|---|---|
| failed | 227 | **227** |
| passed | 2276 | **2566** |
| errors | 53 | **53** |
| failure/error IDs | 280 | **280** |

**New: 0. Fixed: 0.** The failure set is byte-identical. `passed +290` reconciles
exactly: 254 from the six new analytical courts plus 36 from `authority_maintenance`
growing 21→57. The baseline worktree was removed afterwards.

## H-D receipt

**Broader analytical composition is `CURRENT_CONTROL_CAPABILITY` at the declared
accepted grain — with two qualifications.** It is **not** established beyond that
grain, and it does not close H-D.

This lane satisfies H-D's third precondition (the accepted C1 chain is now on
governed control). H-A temporal directionality and H-C service-source applicability
remain open, so H-D stays PARTIAL. `F8_DOES_NOT_TRANSFORM_POSSIBILITY_GEOMETRY` is
unchanged: the integrated composition adds no geometry- or distribution-transformer
operation. C4/live/raw-source execution remains unauthorized pending Omega-1
production-readiness adjudication and a separate raw-source warrant.

## Holds preserved

- No wholesale merge; **0** side-branch commits imported; current-control ancestry intact
- Byte-exact conservation of all 5 production owners and all 15 test/support files
- No raw-source access, live C4, C7, actor/person implementation, or warrant issuance
- No self-adoption: this reconciles an accepted lineage, it does not adopt or authorize

## Environment divergence disclosed

The SECOND-MAC STORE LAW names an authorized shared store at
`/Users/matthewsmith/Desktop/as2b-lits1-DiSDJn/repository`. **It does not exist on
this machine**, and `/Users/matthewsmith/Desktop/Rawlsing` here is a valid git working
tree, not the large non-Git directory the law warns about. I created **no new clone**,
performed no initialization, overwrite, move or absorption, and placed the sparse
worktree in the designated `Rawlsing_Worktrees`.

## Unreconstructed record

The exact 15 court file *names* were never recorded. The total, the multiset, and the
accepted-grain-vs-dependency-closure classification of all 15 files are exact; the
identity of the 8 dependency-closure files is inferred from an exact residual sum of
143 and is corroborated by each being the direct test of a SAME_BLOB dependency.

## Terminal

`HQ204_ANALYTICAL_CONTROL_RECONCILIATION_RETURNED__HQ_REVIEW_REQUIRED`