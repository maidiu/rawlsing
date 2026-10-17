# PYAT R23 F6C — native F6 comparative continuation: result and method verdict

**Verdict: `F6_SOURCEFREE_NATIVE_COMPARATIVE_CONTINUATION_EXECUTED__METHOD_EVIDENCE_REQUIRES_INDEPENDENT_COURT`**

**Role:** original R18 F6B implementation owner continuing the *same coherent
scientific outcome* after HOLD. **Not** HQ, **not** source authority, **not** an
independent reviewer.

- Repository `maidiu/rawlsing` (private).
- Branch `agent/rabochii-pyat-r23-f6b-native-comparative-continuation-r1`.
- Sealed startup **`11f5fd5710cf974dd1a2a399f3d1254011189b4b`** (direct remote verified before work).
- Write terrain: `WORKER_RETURNS/PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1/` only.
- Zero new provider/model calls, zero network attempts, zero raw survey reads,
  zero original respondent reads.

**Execution: 92 tests, 0 failures.**

| Court | Result |
|---|---|
| Inherited S03/S03R/S03FR/S03FO no-drop + canonical-order | **24/24 PASS, 11 subtests PASS** |
| F6C frozen court (this return) | **57/57 PASS** |

---

## 1. The custody correction, done first and done honestly

The addendum's control point was that the previously reported source identity is
wrong. It is wrong, and I verified it before importing anything.

| | Blob | Bytes |
|---|---|---|
| Actual pinned file at `1428c2e92…` | **`fc5e37fa5b2f0eb689593b42d95479d1327cb94c`** | 22257 |
| Previously reported `182cc797…` | `182cc7970d7624f6614015f5a51d0602e1630d52` | 20443 |

Confirmed two independent ways: recomputing
`sha1(b"blob "+len+b"\0"+bytes)` from the actual bytes, and `git ls-tree` at that
exact commit. The two objects are **not** byte-identical — 250 differing lines.
The HQ correction is correct; the original R22/R23 text is historically
unmodified but **superseded at this one source pin**.

I did **not** transplant the older blob into the later commit, and I did **not**
suppress any negative completeness test.

Four scientific invariants exist **only** in the corrected blob, now recorded in
`native_source_identity.json`: the complete-native-joint-domain refusal, the
declared (insertion-order) category order, the outcome-as-predicate tautology
flag, and the ordered `_cells` helper.

### A finding the commission did not anticipate

**The inherited 24-test suite passes on *both* blobs.** I ran it against the
superseded `182cc797…` preimage and it went 24/24 as well. So the inherited suite
is **not** a discriminator for the custody delta — the correction changes which
source is authoritative without changing any inherited test outcome.

I therefore added the discriminating negative the addendum calls for:
`test_delta_omitted_native_category_is_refused_as_manufactured_zero`. It drops one
native cell (keeping denominator conservation exact, so only the completeness
check can fire) and requires `SynthesisError: incomplete native joint domain …
cannot be silently manufactured as zero`. That test passes on `fc5e37fa…` and
cannot pass on `182cc797…`. This is the single most important thing for G14 to
re-check.

## 2. Recovered input contracts — the prior smoke was not a PASS

The earlier F6B repro was correctly never called a PASS. Both reported causes were
real and are now fixed at the fixture level, not in the native code:

- **`SynthesisError` on a float** — `_q` accepts only `int` or rational strings.
  A `0.0` radius raises `numeric inputs must be integers or rational strings`.
- **`KeyError` on `target_id`** — `_target_check` requires `target_id`, plus
  `geography`, `boundary_ref`, `population`, `unit`, `strata_ref`, integer `year`,
  and target shares summing to one.

Two further contract requirements surfaced only on real execution, both of which
I got wrong first and corrected in **my** fixture builder:

- joint cells must be the **complete cross-product** of the two axes' native
  category codes (I used `zip`, producing 2 cells per stratum);
- `design_variance` must be keyed by **mapped** labels, not native codes — the
  producer's own comment says variances must already be for the mapped cell
  probabilities.

## 3. The science actually executed

Two separately indexed, **nonoverlapping** synthetic universes per world, with
predeclared strata/clock and an **independently predeclared** target estimand.

### World A — legitimate overlapping-stratum standardization

| Quantity | Native producer | Naive pooled mixture (my analysis) | Predeclared truth |
|---|---|---|---|
| `[secure, formal]` | **13/25** | 2/5 | 13/25 |
| `[secure, informal]` | **1/10** | 1/10 | 1/10 |
| `[insecure, formal]` | **1/10** | 1/10 | 1/10 |
| `[insecure, informal]` | **7/25** | 2/5 | 7/25 |
| L1 error vs truth | **0** | **6/25** | — |
| P(formal \| secure) | **26/31** | 4/5 | 26/31 |

Both universes have *identical pooled* joints, so pooling reports a stable
`P(formal|secure) = 4/5`. Stratum conditioning to the target's own shares recovers
the truth **exactly**. Standardization genuinely improves target prediction here,
by an exact and checkable margin.

### World B — positivity violation, honest bounds over a false point

Target declares `remote_territory` (share 1/5) covered by **neither** source.

- `candidate.distribution` → **`null`**
- `uncovered_target_mass` → **`1/5`**
- covered subprobability → **8/25, 2/25, 2/25, 8/25** — sums to **4/5, deliberately not renormalised to 1**
- `conditional()` → **`UNAVAILABLE` / `NO_COMPLETE_TARGET_JOINT`**
- source-disagreement bounds → `[2/25, 19/25]`, `[2/25, 7/25]`, `[2/25, 7/25]`, `[2/25, 19/25]`
- bias-sensitivity bounds (radius 3/50) → `[1/50, 41/50]`, `[1/50, 17/50]`, `[1/50, 17/50]`, `[1/50, 41/50]`
- `complementary_binary_bounds(2/5, 2/5)` → lower **0**, upper **2/5**, independence scenario **4/25**, `scenario_is_measured: false`

The missing stratum widens every upper bound and produces **no point estimate**.
Minority strata stay visible in both worlds, with native cell counts preserved
verbatim.

With source-specific fields varied alone, the intended world option changes and
all unrelated fields are unchanged — verified directly.

## 4. Negatives exercised (all refuse or back off; none fabricates)

Denominator/conservation; exclusion counts; proxy-as-measured
(`INDEPENDENT_MARGINALS`); suppressed table status; unweighted mass ≠ raw count;
float numeric input; missing `target_id`; target shares ≠ 1; grain/unit;
geography; boundary; time clock; false overlap claim; overlap review without a
review ref; duplicate sample behind distinct labels; zero weight; weights that do
not name every source; version/mapping preimage mismatch; unqualified mapping;
blocked scale; empty strata; empty source list; duplicate source id;
complementary constructs; hidden nonmodal design-variance coverage; missing design
variance → `UNKNOWN_DESIGN` not a fabricated number; real source without
admission; refusing admission → typed refusal; conditional outside topology;
category outside support; mutated bundle → replay-hash mismatch; joint budget;
support threshold as diagnostic not pruner; duplicate joint cell; unmapped native
category; incomplete native joint domain.

## 5. What I got wrong and disclosed

1. **Frozen World B upper bounds were wrong** (14/25 → corrected 19/25; bias upper
   31/50 → 41/50/17/50). I had omitted the uncovered stratum's share from every
   cell's upper bound. **The producer was right and I was wrong.** No producer
   change, no relaxed test; only my own arithmetic was corrected and disclosed in
   `01_…json` and `02_…json`.
2. Two fixture-builder bugs (cross-product; mapped variance keys), both mine,
   both disclosed.

## 6. Honest limits

This is **sourcefree synthetic method evidence**. It is self-adopted by the same
implementation owner that wrote the producer, so it carries **no independent
authority**. It establishes nothing about any real survey, wave, respondent,
calibrated posterior, acceptance rate, population frequency, or confidence
interval — none of which exist anywhere in this return.

**The original-source gate is unchanged and closed.** No raw SAV/DTA, no
original respondent data, no F6 issuer, no N9/OC05, no N11/N12, no Sorok V3, no
protected branch or previous-worker source touched.

**A genuinely separate independent court is required before HQ adoption.** HQ owns
the final method selection, the World B decision-string hole, the equiweight
policy default, and any quantitative person-world consequence assessment.

---

**Deliverables:** [native_source_identity.json](native_source_identity.json) ·
[01 frozen worlds](01_FROZEN_SOURCEFREE_STUDY_WORLDS.json) ·
[02 actual native output + consumer](02_ACTUAL_INHERITED_F6_OWNER_OUTPUT_AND_NATIVE_CONSUMER.json) ·
[03 holes](03_ALTERNATIVE_ERROR_SENSITIVITY_HOLES.md) ·
[04 HQ decision + source gate](04_HQ_F6_DECISION_AND_ORIGINAL_SOURCE_GATE.md) ·
[05 execution receipt](05_EXECUTION_RECEIPT.json) ·
`02_TESTS/` (worlds + frozen court), `03_JUNIT/`, `04_LOGS/`,
`05_NATIVE_STAGE/` (imported pinned module),
`01_STAGED_NATIVE/REPORTED_VS_ACTUAL_BLOB_DELTA.diff`.