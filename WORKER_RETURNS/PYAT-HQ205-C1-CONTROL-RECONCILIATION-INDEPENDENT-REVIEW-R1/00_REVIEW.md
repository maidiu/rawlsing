# PYAT HQ205 — accepted analytical/C1 control reconciliation independent review — R1

- Repository: `maidiu/rawlsing`
- Branch: `agent/reviewer-pyat-hq205-c1-r1`
- Commissioned startup SHA: `e639fe446392ff12e85ec8c5beffe44c11286334`
- Commission base: `0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646`
- Candidate under review: `88f262b94bbe94cd3e2a8113c8b17d0872c5089c`
- HQ168 accepted integration: `149c3d2636160d8de9b5a8be0c8b87195158077d`
- HQ168 accepted result: `063ee8b77fc4e05c37456ff0168e946247f919ef`
- HQ168 court-verified code: `933a3d31aa961719c73e6ce7eebcfe40bc8cd45e`
- Final prior independent review: `c8ce0ea81a2165f37d566f37de788fecedf85051`
- Model: DeepSeek V4.1 Flash — DeepSeek Harness
- **No code was modified.** No source access, no self-adoption.

## Disposition

`C1_RECONCILIATION_PARTIAL__OVERIMPORT_REPAIR_REQUIRED`

Substance verified in full; the import set must be pruned.

## 0. The two findings that decide this review

**Finding 1 — over-import (drives the disposition).** Of the candidate's 84 imports, only **30 are
required**. The other **54 authority-material files are never opened by the accepted court**. I
proved this three ways: a static scan (no directory enumeration anywhere), a dynamic `io.open` audit
of a full 454-test run (9 of 68 imported `WORKER_RETURNS` paths opened), and a **removal
experiment** — in a scratch worktree at the candidate commit, deleting all 54 still gives
**454 passed, exit 0**. A sensitivity control (deleting all 9 required files) collapses the court to
108 failed / 336 passed / 10 errors, so the experiment discriminates.

**Finding 2 — the "unreconstructed record" claim is false (drives a required correction).** The
candidate states the exact 15 court file *names* "were never recorded by either authority" and that
it reconstructed the court by residual arithmetic. **Both authorities record the exact 15 names** in
machine-readable per-file maps the candidate overlooked:
`063ee8b7:.../08_EXECUTION_RECEIPT.json` (`per_file`) and
`c8ce0ea8:.../05_TEST_AND_REPLAY_REVIEW.json`
(`section8_count_audit.per_file_independently_collected`). The candidate's reconstruction happens to
match them **file-for-file**, so the integrated artifact is right — but its justification is wrong,
and it understates the evidence available.

Everything else the candidate claims is confirmed.

## 1. Method

Two independent sparse worktrees: the review worktree at the commission head, and a candidate
worktree at `88f262b94`. I verified first that control advanced only through two **documentation**
commits after the candidate's base, and that `git diff ff4f06954 e639fe44 -- rawlsing_next` is
**empty** — so the candidate reconciled onto a code state identical to current control, and my two
worktrees are an exact before/after pair.

## 2. A — accepted-grain reconstruction

`ACCEPTED_OWNER_SET_CONFIRMED`.

Two independent authority instruments declare the **same five** production owner blobs: the HQ168
adoption document (`149c3d26`, section "Production owner conservation") and the final prior review
(`c8ce0ea8`, `section2_blob_conservation`). I resolved all five with `git rev-parse` at the accepted
result `063ee8b7` and at the court-verified code `933a3d31` **before** reading the candidate's
reconstruction: both match exactly, and the candidate carries the same blobs.

| owner | blob |
|---|---|
| `pre553_analytical_state_and_route.py` | `3a5e3db8a0897900d0b2606813bda7c3f586d46e` |
| `pre553_empirical_possibility_provider.py` | `23167aa25291fb148b1e3cf210ac33fe7769b783` |
| `pre553_authority_maintenance.py` | `547e6bf20354f38179a0e2600de64c7cb2260ea0` |
| `pre553_analytical_replay_dependency.py` | `47e65aad5e0a8df7af6fda72fc8807a002e556ce` |
| `pre553_analytical_composition.py` | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` |

**The fifth owner question.** The mission named four analytical modules; HQ168 accepted **five**.
`pre553_authority_maintenance.py` is genuinely the fifth: it is named in the adopting instrument
itself, not inferred. `CONFIRMED_FIFTH_ACCEPTED_OWNER`.

Acceptance was never inferred from branch presence; the side branch also carries the historical R8
spine and the historical failed court (434 passed / 1 failed), which remain **historical-only** and
which the candidate correctly did not import into `rawlsing_next`.

## 3. B — 89-path necessity

Population: 89 changed files = **84 imports** (all byte-exact to the accepted result) + **5
candidate return documents**. Relative to control: 87 additions, 2 restorations.

| class | count |
|---|---|
| `REQUIRED_ACCEPTED_DEPENDENCY` | **30** (5 owners + 7 accepted-grain test files + 9 test-support + 9 authority files) |
| `UNNECESSARY_OVERIMPORT` | **54** |
| `REQUIRED_ONLY_FOR_HISTORICAL_COURT` | 0 |
| `CURRENT_CONTROL_ALREADY_HAS_LAWFUL_SUCCESSOR` | 0 |

The 54 by directory: AT07 freeze **38**, R2 **4**, R3 **6**, R8 **6**. The 9 that are genuinely read:
`R2/02_VALUE_RELATION_ORACLE.json`, `R2/03_SYNTHETIC_AUTHORITY_FREEZE.json`,
`R2/04_SLICE_PROJECTION.json`, `R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json`,
`R8/04_CURRENT_AT07_IDENTITY_SPINE.json`, and the four AT07
`FORWARD|REVERSE_(SUCCESSOR|HISTORICAL)_CANONICAL.json`.

Mitigating: the candidate **disclosed** directory-granularity import (its receipt lists
`authority_material_added` as four *directories* with file counts), and every imported file is a
byte-exact accepted blob. Aggravating: the AT07 freeze's `INPUTS/` directory contains **historical
copies of production owner source**, which is a lineage-hygiene hazard here — and the candidate's
own `HISTORICAL_ONLY__NOT_PART_OF_ACCEPTED_GRAIN` category is applied inconsistently, since
`INPUTS/r8_spine.json`, `INPUTS/r8_test_law.py` and `INPUTS/historical_owner.py` are historical R8
material that travelled inside the package.

## 4. C — `pre553_authority_maintenance` collision test

**`SAME_OWNER_STRICT_SUCCESSOR`.** The lineage is decisive:

- both versions descend from `215932d08` (W35);
- **control's blob `ac7f3a013129bc148debf8f011597971a2c99442` is byte-identical to the common-ancestor version** — control never touched this owner after the split;
- the accepted blob is that same ancestor plus exactly three coherent C1-03R commits
  (`eb02332c9`, `7f6449375`, `c690bb0b1`), all descendants of the ancestor;
- `__all__` is identical (17 names, none removed); exactly one internal class is added.

The invariant change is a strict extension: control enforced
`set(recompilation_pairs) == affected_keys`; the accepted version requires replacements and
noncurrent outcomes to be **disjoint and to cover the affected set exactly**, adds duplicate-row,
new-ref, single-outcome and unknown-source refusals, and keeps the unaffected-disjointness guard.
Exact coverage is preserved and error paths stay fail-closed.

One precision note: the candidate's "control is a functional subset" is right for the *guarantee*
surface and inverted for the *input* surface (the accepted version admits a grounded noncurrent
outcome where control demanded a replacement). Wording only; the verdict stands.

## 5. D — consumer boundary

**`PRODUCER_UPSTREAM_CONSUMER_DOWNSTREAM__NO_DUPLICATION`.** The consumer
`source_backed_positioned_subject_possibility.py` is blob `62e5eced47b64512f47b004e3e13a6ef3fe21de7` at control, at the
accepted result, at the candidate and at my head — untouched. The restored producer imports six of
its symbols and **delegates** to `evaluate_positioned_subject_possibility` at its public entry point.
The two modules share **zero** exported names and **zero** module-level class/def names.

## 6. E — court reconstruction

`COURT_RECONSTRUCTION_LEGITIMATE_AND_NOW_PROVABLY_EXACT`.

The commission's premise (and the candidate's claim) that the exact 15 filenames were not preserved
is **false**. Both authorities record them. The recorded set, which the candidate reproduced
exactly:

| file | collected |
|---|---|
| `test_pre553_analytical_state_and_route.py` | 92 |
| `test_pre553_authority_maintenance.py` | 57 |
| `test_pre553_replay_audit.py` | 54 |
| `test_pre553_analytical_replay_dependency.py` | 43 |
| `test_pre553_empirical_possibility_provider.py` | 43 |
| `test_pre553_analytical_composition_higher_order.py` | 35 |
| `test_pre553_empirical_query.py` | 32 |
| `test_pre553_c1_03_join.py` | 28 |
| `test_pre553_structural_admission.py` | 17 |
| `test_pre553_discovery_exact.py` | 14 |
| `test_pre553_analytical_composition.py` | 13 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| `test_pre553_discovery_adaptive.py` | 8 |
| `test_pre553_discovery_adaptive_admission.py` | 3 |
| `test_pre553_recursive_handoff.py` | 2 |
| **total** | **454** |

Seven of the fifteen are accepted-grain tests (311 tests); eight are control-resident
dependency-closure tests (143 tests); 311 + 143 = 454. My independent per-file collection matches
every count, and my independent re-run gives **454 passed, exit 0** (twice).

The "alternate 15-file set" question is therefore moot: there is no inference to attack, because
the true set is recorded. The candidate's residual-arithmetic story is unnecessary and its
"unreconstructed record" caveat must be withdrawn.

## 7. F — regression

`ZERO_REGRESSION_CONFIRMED_INDEPENDENTLY`. I ran the full suite in both trees.

| | failed | passed | skipped | errors | failure/error IDs |
|---|---|---|---|---|---|
| before (control) | 227 | 2276 | 1 | 53 | 280 |
| after (candidate) | 227 | 2566 | 1 | 53 | 280 |

New failure IDs: **0**. Fixed failure IDs: **0**. The ID sets are
byte-identical. Passed delta **+290** reconciles exactly:
254 from the six newly imported analytical courts (92+43+43+35+28+13) plus 36 from
`test_pre553_authority_maintenance` growing 21 → 57. Five collection errors exist in **both** trees
and `--continue-on-collection-errors` was used in both, so no failure hides behind an aborted
collection.

## 8. G — H-D capability

`CURRENT_CONTROL_CAPABILITY__AT_DECLARED_ACCEPTED_GRAIN` — **truthful and correctly bounded**. The
five owners are on control at byte-exact accepted blobs, the accepted court reproduces, regression
is nil, and the producer delegates to rather than duplicates the consumer. The receipt explicitly
withholds C4/live execution, the HQ168 single-owner-contract limitation, H-A, H-C and F8. H-D stays
PARTIAL. The claim survives the over-import finding, because none of the 54 unnecessary files
contributes to it.

## 9. Required repairs

1. **OVERIMPORT-01** (blocking for acceptance) — prune the 54 never-opened authority files, keeping
   the 9 the accepted court opens.
2. **COURT-RECORD-01** (documentation) — replace the "unreconstructed record" caveat with a citation
   of the two recorded per-file maps.
3. **NECESSITY-WORDING-01** (documentation) — state necessity at file granularity.

## 10. Scope

No source access, no locator discovery, no warrant issuance, no live C4, no C7, no actor/person
work, no self-adoption. No code modified. Synthetic and documentary material only.
