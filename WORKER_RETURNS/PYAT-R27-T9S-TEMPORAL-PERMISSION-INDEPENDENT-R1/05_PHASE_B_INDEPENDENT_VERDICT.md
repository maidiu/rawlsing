# T9S Phase B — independent temporal-authority verdict

**Verdict: `ACCEPT_SOURCEFREE_TEMPORAL_AUTHORITY_PROVENANCE_REPAIR`** — T9D
closes all six preregistered RED groups and the two formerly unavailable
capability gates, while the two remaining failures are exactly the documented
safety-related historical compatibility nodes (routes blocked, not reopened).
This is an independent sourcefree scientific review, not a source, actor,
method-adoption, N9, OC05, real EE12, N11/N12 or V3 grant.

**Candidate under review:** `agent/rabochii-pyat-r27-t9d-native-authority-provenance-correction-r1`
@ `d4969f513be0b3691f1bbf45813d17fc171a51a7` (repair payload
`5c76591bd`, sealed startup `7603c4761`). Direct remote readback verified.
The only source change is `t9b_temporal.py` (sha256
`77a4d25d9a6338cf747ca89185790a6d51b0ecbc0c450697a2e30215d92073ef`, Git NUL-blob
`d6710868d72d73f0b711224f18c8792c8b666666`); the staged native closure, frozen
T9I/T9C/author/delta/hostile files are byte-identical to their origin bytes
(`phase_b/SOURCE_MANIFEST.json`, 39 files re-hashed against the candidate commit).

## Independent courts physically executed against T9D

| Court | PASS | FAIL | ERROR | SKIP | Exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| **T9S frozen preregistered falsifiers (Phase A, 17)** | **17** | 0 | 0 | 0 | 0 |
| T9S additional post-inspection controls (12) | 12 | 0 | 0 | 0 | 0 |
| T9R frozen delta50 + capability bindings | 50 | 0 | 0 | 0 | 0 |
| T9R post-inspection hostiles (unchanged) | 7 | 0 | 0 | 0 | 0 |
| Frozen independent T9I (unchanged) | 47 | 1 | 0 | 0 | 1 |
| Unchanged original T9B author | 27 | 1 | 0 | 0 | 1 |
| T9C own repair suite (unchanged) | 52 | 0 | 0 | 0 | 0 |
| Original V553 native consumer (unchanged) | 8 | 0 | 0 | 0 | 0 |
| T9D own authority/provenance checks | 22 | 0 | 0 | 0 | 0 |

The Phase A preregistered suite went from **6 PASS / 11 FAIL (T9C)** to
**17 PASS / 0 FAIL (T9D)** — all six RED groups closed. The two failures are
exactly the two expected historical compatibility nodes, byte-identical and
un-edited (see below), and are NOT regressions.

## Preregistered RED groups — closed

* **F1 unused-future upgrade** (M0/M2) — adding post-clock `W1` to a held 1995
  product leaves `basis_wave_ids=("W0",)`, `temporal_key=PROBE_ONLY`,
  `authorized_opportunity=False`, `opportunity_ids=[ROUTE_BLOCKED_NO_SUPPORT]`,
  `product_observation_status=HELD_ESTIMATE_NOT_OBSERVATION_AT_CLOCK`, and `W1`
  appears only in `archive_context_wave_ids`. Also verified at the other held
  clock 2005 (post-inspection control).
* **F2 empty actor grants** (all three methods) — `access_grants=()` yields
  `WITHHELD_NO_CURRENT_ACCESS_GRANT`, `authorized_opportunity=False`, no open
  route. Native temporal source-grant and actor entitlement are distinct typed
  layers.
* **F3 lag-pipe/rupture suffix** — `pub_lag_of` reads the typed
  `publication_lag_wave_ids` field; `set(pub_lag_of(x)) <= set(basis_wave_ids)`
  holds even with rupture + missing-support qualifiers.
* **F4 duplicate wave id** — refused `DUPLICATE_WAVE_ID_REFUSED` before any
  source/country filter; provenance bound to the exact selected objects, never
  a last-wins `WRONG_SOURCE`/`WRONG_EDITION`.
* **F5 archive known-at** — `archival_known_at_upper_year=2020` excludes a
  2030-published wave in both clock modes (`ARCHIVAL_KNOWN_AT_BOUND_EXCEEDED`),
  so a retrospective read can never present unpublished support as observed.
* **F6 source grant** — typed `SourceGrant` is CHECKED against the used basis:
  wrong-edition → `SOURCE_GRANT_MISMATCH`, non-current → `SOURCE_GRANT_NOT_CURRENT`,
  wrong owner/empty family → `SOURCE_GRANT_WRONG_OWNER`, missing claim →
  `SOURCE_GRANT_MISSING`. No synthesized clearance.

## The two historical compatibility failures (safety-correct)

1. T9I `test_two_time_original_consumer_and_numerical_products_reproduced` —
   the stored 1990 two-time byte artifact records the old open
   `opportunity_ids=['ROUTE_DEFERRED_REVIEW']`; the repair correctly returns
   `ROUTE_BLOCKED_NO_SUPPORT`. This is the disclosed R5/R7 disclosure diff, not
   a reopened unsafe route.
2. author28 `test_hostile_changed_temporal_source_with_same_structural_world_only_moves_the_channel`
   — both retrospective interpolated outputs now correctly have blocked
   authorized-route lists (their exploratory lists differ). Preserved as
   historical evidence rather than reopening an unsafe route.

Neither was edited, xfailed or skipped.

## Layer-split observation (judged, not a RED)

T9D deliberately splits the native anchor-group verdict (`evaluate().temporal_key`
+ `native_authorization`, the SOURCE-side temporal grant over the whole qualified
anchor group, disclosed verbatim in provenance) from the consumer product key
(`read_selected_world().temporal_key` + `product_observation_status`, gated by
the actually used basis at the clock). For an OBSERVED anchor year the product
key may carry the group verdict; for HELD/INTERPOLATED years it is downgraded to
PROBE. This matches the T9C frozen contract ("native call over the whole
qualified anchor group") and the commission's "distinguish native temporal
source-key from actor opportunity" and "determine permission per actually used
basis/clock" for held/interpolated products. The held-product gate is what the
preregistered F1 falsifies, and it passes at every probed held clock.

## Arithmetic and V553 preservation

AS_OF 1995 = 0.20 (W0 alone); RETROSPECTIVE 1995 M1 = 0.40
`INTERPOLATED_NOT_OBSERVED` PROBE; endpoints 0.20/0.60; missing/NaN typed
`MISSING_OBSERVATION_NOT_ZERO` and observed zero stays a real zero. The original
V553 native suite passes 8/0 and the native closure is byte-identical to T9C.
No old open-route behaviour was restored.

## Disposition

The commission's ten original T9I REDs, the T9R delta capability gates and the
T9R seven hostiles are all green; the two historical failures are the preserved
safety-compatibility nodes. **No N9, OC05, real EE12, N11/N12, Sorok actor, V3,
source35 U/Epre or method adoption is granted.** HQ retains scientific adoption
authority.
