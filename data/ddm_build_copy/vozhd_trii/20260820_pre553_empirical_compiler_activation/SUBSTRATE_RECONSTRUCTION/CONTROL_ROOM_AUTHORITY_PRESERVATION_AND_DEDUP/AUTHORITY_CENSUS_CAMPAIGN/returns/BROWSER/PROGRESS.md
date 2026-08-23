# Browser Authority Census — Post-HARVEST-003 Progress

Status: `BROWSER_CENSUS__HARVEST_003_ADJUDICATED__V525B_ACCEPTED_AUTHORITY_RECOVERED__D62_SHADOWING_PROVENANCE_UNRESOLVED__HARVEST_004_ISSUED`

Start SHA: `b824c7d2b618b8e0987f6774b302e875d90b8fdd`
Worker: `agent/vozhd-controlroom-authority-census-browser-r1`

## HARVEST-003 integrity

Browser inspected the actual uploaded ZIP and independently verified:

- packet SHA-256 `0ad166ec3da232f56a5a0c9612862e99b2091e8ba80626bc76417e7a4524e461`;
- size `20,844,038` bytes;
- ZIP integrity;
- all `252/252` internal checksum entries.

The worker correctly declined a raw old/new row diff because the available composite keys were non-unique. Browser did not collapse those rows. Instead, Browser recovered the historical consumer's exact lookup law and evaluated the effective carrier under that law.

## Accepted historical semantic/driver authority recovered

The V525b package positively identifies the 6,211-row masters as accepted authority:

- `questions_master_semantic.csv` SHA `6e76965c...`
- `questions_master_drivers.csv` SHA `53feb282...`

`canonical_driver_bundle_manifest.yaml` records `authority_status: accepted_structural_authority`, package status `green_driver_atlas_structural`, and identifies both masters as `canonical_structural_authority` with exact hashes. Green validation reports zero blank semantic-content IDs, zero blank final-driver IDs, complete driver-index coverage and no blockers.

These files are therefore preserved accepted historical authority, not disposable precursors.

## Later semantic carrier is generated, not a proved successor

The later 18,528-row semantic master SHA `171d399d...` is produced by recovered `build_semantic_questions_master.py` SHA `58b390c3...`.

The builder preserves exact existing semantic IDs where available but otherwise performs token/content-key scoring and emits `matched_content_key`, `soft_content_key`, or low-confidence `fallback_cluster` assignments. The later carrier is not byte-lossless against V525b and no explicit retirement/supersession bridge was recovered.

## `d62...` exactly explains Register B

The later driver master SHA `d62accad...` has 28,983 rows but only 18,519 distinct `(source,wave,var_name)` keys.

The historical question-structure builder constructs a dict keyed by `(source,wave,var_name)`. Duplicate keys therefore resolve mechanically to the last row encountered.

Using only that exact lookup projection:

- Register B has 18,262 matching effective `d62...` keys and 530 unmatched rows;
- all nine semantic/driver fields have zero mismatches for all 18,262 matches;
- applying the same effective lookup against Register A yields exactly the previously observed 2,148 changed rows and exactly 13,330 changed cells with identical per-column counts.

`d62...` is therefore the direct effective carrier behind the A→B semantic/driver transition.

## Duplicate-key shadowing is a preservation defect until provenance proves otherwise

Within the 2,148 changed keys:

- 2,056 have two rows in `d62...`;
- the last duplicate is always the Register B state;
- 1,228 still preserve the Register A state as the earlier duplicate;
- winning rows are overwhelmingly `accepted_context_only` or `accepted_block_child` structural/context rows;
- 1,870 winning rows have blank `status` and 1,864 have blank `final_driver_origin`;
- the effective transition includes thousands of nonblank→blank semantic-field changes.

No recovered authority object says that this duplicate-row precedence intentionally supersedes the accepted semantic state. Current classification:

`DUPLICATE_KEY_STRUCTURAL_ROW_SHADOWING__AUTHORITY_PROVENANCE_UNRESOLVED`

## Review evidence is narrow, not a global bridge

Recovered facet-deepening review files overlap only 68 of the 2,148 changed keys and do not provide a global acceptance bridge.

`gss1972_semantic_authority_review_notes.md` is positive narrow manual authority: a 216-row question-by-question review with 19 rows tightened while conservative boundaries were retained. It is preserved only for that scope.

## Current disposition

- `EXP-006 EARLY_SEMANTIC_MASTER`: positive accepted V525b authority recovered; later generated carrier does not prove lossless supersession.
- `EXP-007 DRIVER_FACET`: `d62...` positively identified as Register B's effective carrier; producer and duplicate-precedence authority unresolved.
- `EXP-030 SUPERSESSION_REGISTRY`: still open; H003 supplies explicit non-supersession evidence for this lineage.
- no expectation is `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`.

## Next local request

Issued:

`HARVEST-004 — D62 DRIVER-MASTER PRODUCER AND DUPLICATE-SHADOWING PROVENANCE`

This request is limited to the pre-`d62` master states, producer/updater scripts/configs, structural-enrichment row creation, and any explicit authority saying duplicate last-row precedence was intended or accepted. It forbids repair, deduplication, re-keying, regeneration, or semantic adjudication.
