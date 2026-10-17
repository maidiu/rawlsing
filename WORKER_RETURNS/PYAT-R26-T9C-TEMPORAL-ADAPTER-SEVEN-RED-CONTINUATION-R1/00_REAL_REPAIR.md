# 00 — real repair: seven defect classes, ten independent temporal REDs (PYAT R26 T9C)

**Role.** Original T9B sourcefree temporal adapter owner, continuation repair.
**Not** the independent T9I reviewer, **not** HQ, **not** an EE12 issuer.

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (verified PRIVATE) |
| Branch | `agent/rabochii-pyat-r26-t9c-temporal-adapter-seven-red-repair-r1` |
| Sealed startup | `79cf24ee615ec24bee2dc8584b31fb6b240fd3cf` |
| Original author | `edf3494b1b11cb71a78540aba950aa15da900c8a` |
| Independent T9I court | `a2a7bdeda76aa008b3d620b01af71f7fd6efaaae` |
| Commission | `WORKER_COMMISSIONS/PYAT-R26-T9C-TEMPORAL-ADAPTER-SEVEN-RED-CONTINUATION-R1/00_COMMISSION.md` |
| Write scope | `WORKER_RETURNS/PYAT-R26-T9C-TEMPORAL-ADAPTER-SEVEN-RED-CONTINUATION-R1/` **only** |
| Grain | `SOURCEFREE_SYNTHETIC` |

---

## 1. What was actually broken

The independent T9I court returned
`RED_SOURCEFREE_TEMPORAL_CLOCK_CUSTODY_AND_CONSUMER`. Its own tally was 38 passed /
10 failed assertions across seven defect classes. The ten are reproduced exactly by
this return's counterexample runner against the original adapter
(`02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json`):

```
R1 false native authorization            1 assertion   original 0/1   ->  repaired 1/1
R2 missing-as-zero                       3 assertions  original 0/3   ->  repaired 3/3
R3 excluded-source provenance            1 assertion   original 0/1   ->  repaired 1/1
R4 incomplete structural equality        1 assertion   original 0/1   ->  repaired 1/1
R5 PROBE-based opportunity authorization 1 assertion   original 0/1   ->  repaired 1/1
R6 post-rupture carry                    2 assertions  original 0/2   ->  repaired 2/2
R7 nonbasis publication lag              1 assertion   original 0/1   ->  repaired 1/1
                                        -----------
                                         10 total       0/10          ->  10/10
```

The arithmetic of the adapter was never in dispute. T9I confirmed it reproduces.
The failures were **contract** failures: what the adapter was allowed to *claim*.

---

## 2. The seven repairs

### R1 — false native authorization

**Defect.** The adapter imported `AUTHORIZED_SPARSE_TEMPORAL_KEY` from the pinned
V553 module and stamped it onto adapter results. It never called
`_authorize_v553_multi_wave_key`, which is the function that actually decides, and
which requires a harmonized key plus **two** qualified anchors. A single synthetic
`Wave(.20)` therefore claimed an inherited native grant it never received.

**Repair.** `temporal_key` is now **returned by the original
`_authorize_v553_multi_wave_key`**, called on the qualified anchor group at the
clock with the harmonized-key, packet-provenance, resolved-dimension and
probe-readiness inputs that function genuinely consumes. The adapter supplies those
inputs as the caller's declarations and forwards them verbatim; it does not decide
the status. Native may only ever **downgrade** a result.

| Anchor group at the clock | Native result |
|---|---|
| 0 eligible | `BLOCKED_TEMPORAL_KEY` |
| 1 eligible | `PROBE_ONLY_TEMPORAL_KEY` — reason `insufficient_distinct_waves` |
| 2+ eligible | `AUTHORIZED_SPARSE_TEMPORAL_KEY` — reason `at_least_two_probe_ready_resolved_structural_anchors` |

**The second clause of R1 is the important one.** The native gap-segment index
preserves `unknown_gap_preserved` with `interpolation_allowed=false` even when the
caller passes `allow_interpolation=True`. So a stand-in for an unobserved year can
never be upgraded by a two-anchor native grant: an `INTERPOLATED_NOT_OBSERVED`
result is capped at `PROBE_ONLY_TEMPORAL_KEY` no matter what the anchor count says.
Verified directly against `_build_v553_interpolation_segment_index` with
`allow_interpolation=True`.

### R2 — missing is not zero

**Defect.** A floating-point `NaN` wave produced `value=0.0`, `band="none"`,
`AUTHORIZED`, and no refusal under all three methods, because `_bounded_score` was
called on an unsupported observation.

**Repair.** Upstream native support validation runs **before any numeric use**.
`None`, non-numeric, `NaN`, `inf`, and an explicitly declared
`support_status="MISSING"` are all typed UNKNOWN: `value=None`,
`refused_code=MISSING_OBSERVATION_NOT_ZERO`, `temporal_key=BLOCKED_TEMPORAL_KEY`,
`band=None`. An observed `0.0` remains a real observed zero with `band="none"` and
`refused_code=None`. Mixed support drops the unsupported anchor and names it in a
`MISSING_SUPPORT_EXCLUDED:` uncertainty segment.

This is an adapter-contract repair only. The accepted original V553
`_bounded_score` default-to-0.0 behaviour is untouched and is covered by its own
control (`test_r2_native_bounded_score_default_is_untouched`).

### R3 — excluded-source provenance

**Defect.** Consumer provenance named `case.waves[0].source_family` and `.edition`
even when that first wave had been filtered out as `WRONG_SOURCE`/`WRONG_EDITION`.
An excluded source was reported as the supported consumer provenance while the
numeric filtering was correct.

**Repair.** `source_family` / `edition` / `source_families` / `editions` are bound
to the waves actually named in `basis_wave_ids`. If the basis waves disagree on
`(source_family, edition)` the read is refused with `BASIS_SOURCE_CONFLICT` rather
than silently narrowed to one source.

### R4 — incomplete structural equality

**Defect.** `structurally_identical` compared `world_id`, `access_grants`,
`institution` and `grain` but ignored `structural_routes`. Removing
`ROUTE_PARTICIPATION` from the supplied world at the same clock changed the output
while the certificate still returned `True`.

**Repair.** The complete structural/access world identity travels with every read in
`provenance.structural_world_fields` (`world_id`, `structural_routes`,
`access_grants`, `institution`), and `structurally_identical` compares it in full.
Route removal, institution change and access-grant change are all detected; the
original two-clock positive fixture still certifies identical.

### R5 — PROBE-based opportunity authorization

**Defect.** At retrospective 1995 the honest `.40` estimate was correctly labelled
`PROBE_ONLY` / `NOT_OBSERVED`, yet `read_selected_world` emitted
`ROUTE_DEFERRED_REVIEW` with no refusal and described the result as a
permission-valid open route. An exploratory estimate was opening authorized world
options.

**Repair.** Only a natively `AUTHORIZED` observation may present an open,
permission-valid route. A `PROBE_ONLY`/exploratory read reports
`opportunity_ids = ("ROUTE_BLOCKED_NO_SUPPORT",)` and `authorized_opportunity=False`,
and lists the band-implied routes **separately** in `exploratory_route_ids`. A
refused read opens nothing.

### R6 — post-rupture carry

**Defect.** Query 1997 across the declared 1995 population break carried the
pre-break `.20` as `AUTHORIZED` with no rupture caveat, implying the post-break
cohort estimand.

**Repair.** A carry that crosses a registered rupture is kept as a **typed bounded
hypothetical**: the value is preserved and `refused_code` stays `None` (so the
accepted author positive that a hold still works across a rupture survives
unchanged at `0.30`), but the result is explicitly qualified
(`POST_RUPTURE_CARRY_HYPOTHETICAL:R1995|IDENTIFIED_SET_UNBOUNDED:STABILITY_NOT_ASSUMED`),
`rupture_qualified=True`, and `temporal_key` is downgraded to `PROBE_ONLY` so no
route is opened. The detail states that the post-break cohort estimand is **not**
identified and that **no stability is assumed**. R1's interpolation bracket refusal
is unchanged.

### R7 — archive context versus basis publication lag

**Defect.** Retrospective M0 used only `W0` yet flagged future `W1` as a
publication lag *on that value*. Over-inclusive, ambiguous provenance.

**Repair.** `publication_lag_wave_ids` and `pub_lag_of()` are computed over the
**basis waves only**, so lag provenance can never name a wave the method did not
use. The unused post-clock archive inventory is published **separately** as
`archive_context_wave_ids`, and is never presented as product publication basis.
`AS_OF` reads carry no archive context at all. A genuinely late-published basis wave
is still flagged.

---

## 3. What was preserved

| Requirement | Status |
|---|---|
| Original V553 code | **Unmodified.** 22/22 staged files byte-identical to repo blobs at `79cf24ee`. `git status` clean on the accepted native tree. |
| 28 author positives | **Preserved.** Court 4: 28/28, run in the original author return against its original 1,259-file tree. |
| 8 inherited native tests | **Preserved.** Court 3: 8/8, unmodified source. |
| Original `_interp` / `_pressure_band` / `_bounded_score` | Inherited **by identity**, not reimplemented. |
| Original `_authorize_v553_multi_wave_key` | Called, not copied, not patched. |
| Historically honest AS_OF vs RETROSPECTIVE | **Preserved.** AS_OF still refuses a wave published after the clock and still cannot interpolate; RETROSPECTIVE still flags publication lag rather than pretending. |
| Reviewer assertions | **Unmodified.** Frozen T9I test is byte-identical to git blob `f624177d4980f524781c84956eb23a45bfa52a78`. |
| source35, N9, OC05, N11/N12, Sorok V3 | **Untouched.** |

### Arithmetic, stated honestly

Commission-mandated values are preserved and were **not** falsified by the frozen
expected-output contract in `01_SEVEN_DEFECT_CONTRACTS.json` (frozen before the
adapted suite ran):

* AS_OF 1995, all three methods: **0.20**, using `W0` alone
* RETROSPECTIVE 1995, M1: **0.40**, `INTERPOLATED_NOT_OBSERVED`, `PROBE_ONLY`
* RETROSPECTIVE 1995, M0 / M2: **0.20**
* endpoints 1990 / 2000: **0.20 / 0.60**, sourcefree

Interpretation limits, unchanged from the independent court and not weakened here:

* linear slope `1/25` per year, midpoint `2/5` — **a model, not an identified observation**
* unconditioned identification set `[0, 1]`, maximum absolute error `3/5`
* under explicitly imposed monotonicity: `[1/5, 3/5]`, maximum absolute error `1/5`
* neither bound is a sampling confidence interval; sampling error is
  **UNIDENTIFIED** — no sample design, calibration error, variance or national
  inference is supplied

No original source or actor exposure inference is made. `provenance` carries
`synthetic=true` and `observed_temporal_calibration=false`, and contains no
`memory`, `remembered` or `exposure` key. There is no independent archival known-at
upper bound, no effective/discovered-at revocation timestamps, and no
historical-entitlement versus current-computation grant pair; a supplied
retrospective archive is a caller precondition, not an authenticated dated snapshot.

---

## 4. Execution

`python3 -B run_all.py` — real pytest, pinned imports, `-B`, plugin autoload
disabled, explicit `--rootdir` and `-c` on every court. Full logs in `logs/`,
machine-readable assembly in `evidence/t9c_four_court_execution.json`.

| Court | Cases | Passed | Failed | Errors | Exit |
|---|---:|---:|---:|---:|---:|
| Frozen independent T9I suite | 48 | 47 | 1 | 0 | 1 |
| Own T9C repair suite | 52 | 52 | 0 | 0 | 0 |
| Inherited original V553 native suite | 8 | 8 | 0 | 0 | 0 |
| Unchanged original T9B author suite | 28 | 28 | 0 | 0 | 0 |

Crosswalk against the independent court's own JUnit
(`evidence/03_T9I_RED_TO_GREEN_CROSSWALK.json`):

```
T9I independent court : 38 pass  10 fail
T9C repaired adapter  : 47 pass   1 fail
red -> green          : 10
newly red             :  1
```

Module custody for the frozen court (`evidence/t9c_frozen_t9i_module_receipts.json`):
16 loaded project modules, **16/16 inside this return, 0 ambient leaks**.

---

## 5. The one residual failure, disclosed

`test_two_time_original_consumer_and_numerical_products_reproduced` compares the
repaired consumer output against the **original T9B published two-time artifact**.
Repairing R5 requires a `PROBE_ONLY` read to stop presenting a route as a
permission-valid open opportunity; that artifact records
`opportunity_ids = ["ROUTE_DEFERRED_REVIEW"]` for the 1990 `PROBE_ONLY` read. The
two cannot both hold. The repair takes precedence and the deviation is disclosed.

Exactly **one semantic field** changes: `1990.opportunity_ids`.
Everything the independent court endorsed is unchanged — 0.20 / 0.60 values, bands,
`basis_wave_ids`, `uncertainty`, `temporal_key`, `refused_code`, and the entire
`provenance` block. All other differences are purely additive disclosure fields
introduced by the repairs themselves (`structural_world_fields`, `source_families`,
`editions`, `archive_context_wave_ids`, `native_multi_wave_authorization_*`,
`authorized_opportunity`, `exploratory_route_ids`, `not_observed`,
`rupture_qualified`).

Full field-level diff: `03_NATIVE_JUNIT_AND_IMPORT_LEDGER.md` §5 and
`02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json`.

This residual is a **required consequence of repairing R5**, not an undisclosed
regression. It is the only new red in the frozen transport, and it is red precisely
because the rejected artifact exhibited R5.

---

## 6. Prohibitions — none of these is granted

No real EE12 source pair. No national statistical inference. No OC05. No N11. No
N12. No V3. No method adoption. No N8E/N8S/N9 execution. No actor exposure or
remembered-exposure evidence. No observed temporal calibration. No longitudinal
cohort estimand.

**Independent T9R review is required before HQ method acceptance.** This return is
a repaired adapter contract and its evidence. It is not a method accession.

---

## 7. Artifacts

| Path | Contents |
|---|---|
| `00_REAL_REPAIR.md` | this document |
| `01_SEVEN_DEFECT_CONTRACTS.json` | frozen seven-defect contracts and frozen expected outputs (frozen before execution) |
| `02_ACTUAL_ORIGINAL_V553_AND_CONSUMER.json` | actual native controls, side-by-side counterexamples, full corrected consumer outputs |
| `02_counterexamples.py` | generates the above; loads original T9B adapter by exact path without modifying it |
| `03_NATIVE_JUNIT_AND_IMPORT_LEDGER.md` | four-court JUnit ledger, native import ledger, module receipts, residual diff |
| `04_T9R_REVIEW_WAKE.md` | independent T9R review wake |
| `t9b_temporal.py` | corrected adapter (module name retained for frozen-court transport compatibility) |
| `test_t9c_repair.py` | 52 own repair checks |
| `guarded_runner.py` | pinned-import, preimage-guarded frozen-court runner |
| `run_pinned_v553_suite_t9c.py` | inherited original V553 8-test runner |
| `run_all.py` | four-court runner |
| `frozen_t9i_court/test_independent_clock_custody.py` | byte-identical frozen independent transport (blob `f624177d…`) |
| `native/data/ddm_build_copy/` | minimal 22-source byte-verified pinned closure |
| `pinned_candidate/evidence/02_real_temporal_to_selected_world_two_times.json` | frozen original T9B published artifact used by the transport |
| `junit/`, `logs/`, `evidence/`, `environment_passport.json`, `05_REMOTE_VERIFICATION.json` | execution, custody and publication receipts |
