# R27 T9D — temporal authority and provenance repair result

**Status:** REPAIRED UNDER BOUNDED SOURCEFREE ADAPTER, RETURNED FOR INDEPENDENT
T9S REVIEW. This is the original T9B/T9C productive adapter continuation. It is
NOT an independent temporal reviewer, NOT HQ, and issues no source, actor,
method-adoption, N9, OC05, real EE12, N11/N12 or V3 grant.

- Repository: `maidiu/rawlsing` (PRIVATE, verified)
- Branch: `agent/rabochii-pyat-r27-t9d-native-authority-provenance-correction-r1`
- Exact sealed startup: `7603c47610c01937e48b07f7fc69531964182911`
- Commission: `WORKER_COMMISSIONS/PYAT-R27-T9D-TEMPORAL-AUTHORITY-PROVENANCE-REPAIR-R1/00_COMMISSION.md`
- Original T9C author: `9a33c2dcaa7ac0d50606416ab965488c9782934b` (repair payload
  `d6e062684ca34b99ee9713c8c0affa0ed5c27f25`)
- Independent T9R verdict: `299dbf0d3a54fa76e36e524c553662f60090fe72`
  (`RED / HOLD FOR METHOD ACCEPTANCE`)
- Repaired adapter: `t9b_temporal.py`, sha256
  `77a4d25d9a6338cf747ca89185790a6d51b0ecbc0c450697a2e30215d92073ef`,
  git blob SHA-1 (NUL preimage) `d6710868d72d73f0b711224f18c8792c8b666666`
- Real diff vs T9C adapter: `07_REAL_DIFF_T9C_TO_T9D.patch` (776 lines)

## What was preserved

Everything T9C fixed is preserved: all **ten original T9I RED assertions remain
green** (independent T9I frozen court 47 PASS / 1 FAIL, the single failure being
the stored two-time byte-artifact comparison that T9R already classified as the
expected safety-related historical comparison). The V553 originals stay
byte-identical (22 native files, all matching the T9C closure and the accepted
blobs) and the temporal primitives remain inherited **by identity**
(`_interp`, `_pressure_band`, `_bounded_score`, the three key constants,
`_authorize_v553_multi_wave_key`). The historically honest AS_OF versus
RETROSPECTIVE estimates are unchanged: AS_OF 1995 = 0.20 on W0 alone,
RETROSPECTIVE 1995 M1 = 0.40 `INTERPOLATED_NOT_OBSERVED`, endpoints 0.20/0.60.
No unsafe old opportunity behavior was restored to make historical
byte-comparison assertions green.

## What was repaired (T9R's remaining independent failures)

1. **Unused future data upgrading authorization (T9D-1).** Product
   authorization is now determined per the actually USED basis at the clock, not
   per all supplied archive context. A held estimate for an unobserved year is
   typed `HELD_ESTIMATE_NOT_OBSERVATION_AT_CLOCK` and can never carry the anchor
   group's AUTHORIZED status into a product authorization — "a held 1995
   estimate is not a 1995 observation". Adding W1 (2000) to a retrospective 1995
   hold on W0 (1990) no longer changes `temporal_key`, `authorized_opportunity`
   or `opportunity_ids`; W1 appears only in `archive_context_wave_ids`. An
   interpolated stand-in stays `INTERPOLATED_NOT_OBSERVED`. The native anchor
   group verdict remains disclosed verbatim as the SOURCE-side temporal grant
   (`native_authorization` / `provenance.native_multi_wave_authorization_status`),
   deliberately distinct from product authorization.

2. **Empty actor grants permitting routes (T9D-2).** Native temporal
   source-grant and actor opportunity entitlement are now separate typed
   concepts. No permission-valid route opens without a present current
   independently provided actor grant; `access_grants=()` yields
   `WITHHELD_NO_CURRENT_ACCESS_GRANT`, `opportunity_ids=[ROUTE_BLOCKED_NO_SUPPORT]`
   and `authorized_opportunity=false`, with band-implied routes listed only as
   explicitly exploratory.

3. **Malformed publication-lag basis identities (T9D-3).** Basis lag, archive
   context, rupture and missing-support identities are typed fields
   (`publication_lag_wave_ids`, `archive_context_wave_ids`,
   `rupture_crossed_year`, `missing_excluded_wave_ids`); `pub_lag_of` returns the
   typed basis-lag field and never parses a pipe-suffixed rupture caveat as a
   fake source-wave ID. Invariant: `set(pub_lag_of(x)) <= set(x.basis_wave_ids)`.

4. **Duplicate wave IDs corrupting source provenance (T9D-4).** A reused
   `wave_id` is refused BEFORE any source/country filtering with
   `DUPLICATE_WAVE_ID_REFUSED`, and basis provenance is bound to the exact
   selected wave objects (`basis_source_refs`), so a last-wins dictionary can
   never rebind product identity to an excluded `WRONG_SOURCE`/`WRONG_EDITION`
   input.

5. **Archival known-at and source-currentness capabilities (T9D-5).** Typed
   `archival_known_at_upper_year` (dated archive snapshot bound) and typed
   `SourceGrant` (source-family / owner / edition / currentness) are now
   expressible and ENFORCED. The presence of metadata is never itself a grant:
   it is checked against the used basis. A missing issuer returns explicit
   UNAVAILABLE/HOLD (`SOURCE_GRANT_UNAVAILABLE_*`,
   `ARCHIVAL_KNOWN_AT_BOUND_EXCEEDED`); the adapter never synthesizes a
   production original issuer or a faked clearance. The four previously
   unavailable precommitted gates D04/D16/D17/D17_WRONG_OWNER now execute real
   candidate calls and pass their frozen assertions.

## Executed courts (separate, never aggregated)

| Court | Tests | PASS | FAIL | ERROR | SKIP | Exit |
|---|---:|---:|---:|---:|---:|---:|
| Frozen independent T9I (unchanged) | 48 | 47 | 1 | 0 | 0 | 1 |
| T9C own repair suite (unchanged) | 52 | 52 | 0 | 0 | 0 | 0 |
| Original V553 native consumer (unchanged) | 8 | 8 | 0 | 0 | 0 | 0 |
| Original T9B author suite (unchanged) | 28 | 27 | 1 | 0 | 0 | 1 |
| T9R frozen delta50 + T9D capability bindings | 50 | 50 | 0 | 0 | 0 | 0 |
| T9R post-inspection hostiles (unchanged) | 7 | 7 | 0 | 0 | 0 | 0 |
| T9D own authority/provenance checks | 22 | 22 | 0 | 0 | 0 | 0 |

The two failures are exactly the two expected safety-related historical
compatibility comparisons, unchanged and unedited:

- `test_two_time_original_consumer_and_numerical_products_reproduced` (T9I) —
  the stored two-time byte artifact records the old open opportunity lists and
  none of the new typed disclosure fields. R5/R7 safety repair necessarily
  changes those fields. Reported as historical incompatibility, not restored.
- `test_hostile_changed_temporal_source_with_same_structural_world_only_moves_the_channel`
  (author28) — both retrospective interpolated outputs now correctly have
  blocked authorized-route lists (their exploratory lists differ). Preserved as
  historical compatibility evidence rather than reopening an unsafe route.

## Not granted

No original EE12 source pair, no real source bytes, no national inference, no
OC05, no N9, no N11, no N12, no Sorok actor, no V3, no method adoption, no
actor exposure or remembered-exposure claim. Downstream consumer negatives
(duplicate identity, edition mismatch, wrong owner, non-current grant, missing
issuer, empty entitlement, future publication, held-product authority) are
executed as real tests, not asserted.

## Return packet

- `00_RESULT.md` (this file)
- `01_BASIS_AUTHORITY_AND_GRANTS.json` — layer/tier contract of the repair
- `02_ARCHIVAL_SOURCE_KNOWN_AT.json` — archival known-at and source-currentness
  capability record with the four frozen gate results
- `03_FOUR_COURTS_AND_SOURCE_PROOF.md` — court transcripts and source proof
- `04_T9S_WAKE.md` — independent T9S review wake
- `05_REMOTE_VERIFICATION.json` — exact remote SHA readback
- `06_EVIDENCE_FILE_HASHES.json` — sha256 and git blob SHA-1 (NUL preimage) for
  every staged source/test, with byte-identity receipts
- `07_REAL_DIFF_T9C_TO_T9D.patch` — real diff of the adapter
- `evidence/`, `junit/`, `logs/` — raw observations, JUnit XML and stdout
