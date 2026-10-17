# 03 — ALTERNATIVES COMPARATIVE CALIBRATION AND LEAK HOSTILES

All executed with real Python against pinned, blob-verified native bytes.
**28/28 frozen tests pass.** Nothing xfailed, skipped or relabelled.

## 1. Method comparison at matched evidence

All three methods consume the identical admissible wave set; only the estimation
rule differs. Evidence reads, retrieval calls and compute units are identical.

| Method | Rule | TC1 interior | TC2 null | Uncertainty class |
|---|---|---|---|---|
| **M0 piecewise hold** | nearest prior admissible anchor | 0.20 | 0.50 | `HELD_NO_INTERPOLATION` |
| **M1 linear interpolation** | inherited `_interp` between anchors | **0.40** | 0.50 | `INTERPOLATED_NOT_OBSERVED` |
| **M2 uncertainty-aware backoff** | nearest anchor + gap-dependent uncertainty | 0.20 | 0.50 | `BACKOFF_*` |

**Adjudication.** M1 is the only method that extracts real information from a gap,
and it is the only one that must be refused in three situations (rupture bracket,
no support, non-harmonizable geometry). M2 is the only method that is *safe
everywhere*, and it differs from M0 exactly where the gap is too wide to hold
silently (`BACKOFF_WIDE_GAP_UNCERTAIN` when the next anchor is >2 years away).

**Recommendation: keep all three, and require the caller to state which clock
question and which method produced a value.** Neither M0 nor M2 is universally
correct; they trade resolution for safety, and the choice is semantic, not technical.

## 2. Leak hostiles

| Hostile | Observed |
|---|---|
| **Unauthorized future publication** | wave observed 2010, published 2015, queried at 2012 → `NO_TEMPORAL_SUPPORT`, `BLOCKED_TEMPORAL_KEY`. The value never enters an AS_OF read. |
| **Retrospective read of the same wave** | succeeds but is flagged `PUBLICATION_LAG:W0` and carries "published AFTER the query clock" in its detail. It is never presented as knowable in 2012. |
| **Contradictory causal clock** (query before every observation, AS_OF) | `NO_TEMPORAL_SUPPORT`, blocked |
| Same query, archival mode | `PROBE_ONLY_TEMPORAL_KEY` + `NO_PRIOR_KNOWN_AT_WAVE` — never a guessed value |
| **Stale source / revocation** | revoked wave excluded in **both** clock modes (a real engine bug found and fixed during this pass) |
| **Archival non-renewal** | excluded in both modes → `NO_TEMPORAL_SUPPORT` |
| **Wrong instrument** | excluded → `NO_TEMPORAL_SUPPORT` |
| **Wrong cohort** | excluded → `NO_TEMPORAL_SUPPORT` |
| **Wrong geography, explicit harmonization** | `NON_HARMONIZABLE_GEOMETRY`, refused; **never pooled or averaged** |
| **No support at all** | `NO_TEMPORAL_SUPPORT`; consumer emits `ROUTE_BLOCKED_NO_SUPPORT`, a real nonpositive route, not a fabricated opportunity |
| **Changed temporal source, same structural world** | `structurally_identical()` still true while opportunities change — proves the movement is temporal, not structural |
| **Ambient import shadowing** | `test_imports_land_inside_this_return` and `test_temporal_primitives_are_inherited_verbatim_not_reimplemented` both assert `module.__file__` and object identity against the staged tree |

## 3. Sensitivity to target clock and support

Quantified rather than asserted: on TC1, M0/M1/M2 at clock 1980 yield **no
support**; at 1990 they yield the 1990 anchor; at 1995 only M1-retrospective moves
off the anchor; at 2000 all converge on the terminal anchor. The step-function shape
of M0/M2 against the piecewise-linear shape of M1 is the entire trade-off, and it is
visible directly in the numbers.

## 4. No fake high-resolution signal

- Interpolated values are always classed `INTERPOLATED_NOT_OBSERVED` and carry
  `PROBE_ONLY_TEMPORAL_KEY` — they are **not** authorized product values.
- `_bounded_score` clamps to [0, 1]; `_pressure_band` maps to a finite band. No
  value can exceed the observed anchor range by construction.
- The null case TC2 returns exactly 0.50 under both M0 and M1: no trend is invented
  from a flat series.

## 5. Custody and calibration honesty

- Native closure **1259/1259** git blob SHA-1 verified.
- Temporal primitives are **inherited by identity**, asserted with `is` — not
  reimplemented, so no silent divergence is possible.
- Every consumer value carries world, institution, grain, source family, instrument,
  cohort, country, edition, query clock, clock question, publication-lag flags, plus
  `synthetic: true` and `observed_temporal_calibration: false`.
- **No performance, latency, cost or calibration extrapolation beyond this synthetic
  grain is claimed.**
