# Browser Authority Census — Post-HARVEST-002 Progress

Status: `BROWSER_CENSUS__HARVEST_002_ADJUDICATED__EXISTING_SCOPE_AUTHORITY_NOT_INHERITED__HARVEST_003_ISSUED`

Start SHA: `b824c7d2b618b8e0987f6774b302e875d90b8fdd`
Worker: `agent/vozhd-controlroom-authority-census-browser-r1`

## HARVEST-002 adjudicated

Browser inspected the actual returned ZIP and independently verified:

- packet SHA-256 `70789a6556f70c2c6be0771defe00fec918b7e64514e37d82744493431f1dc37`;
- size `89,531` bytes;
- ZIP integrity;
- all 25 `SHA256SUMS.txt` entries.

## Current-35 scope identity exists

The recovered audit binding is not a populated scope carrier. It is intentionally fail-closed:

`BLOCKED_REQUIRES_HASH_BOUND_AUDIT_REPUBLICATION`

with 35 expected UIDs, 0 observed UIDs and 0 hash-bound audit artifacts.

Separately, Browser recovered the accepted SWID identity authority on `agent/source-wave-identity-repair-integration`:

`source_wave_identity_registry_35wave_v1.json`

Git blob SHA-1 `ae09ab645d5d134c4462a012da57dbe02708b690`.

It declares exactly 35 production CLOSED_35 members, including EVS 1999 and explicitly recognizing Asian Barometer W6 as excluded.

HARVEST-002 also recovered `wave_authority_registry_35wave_v1.json` SHA-256 `3670d056c45c188843681535feb8543cf5a4ad20f2d0a067ce4f6b16b944888e`, with exactly 35 per-wave authority entries, EVS1999 present and Asian W6 absent.

Therefore current-35 identity/scope authority exists. No new scope authority is authorized for creation.

## Itinerary manual authority is preserved, not superseded

The historical itinerary remains one exact SHA:

`866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3`

Its 35 rows still contain Asian W6 and omit EVS1999. Its manual fields remain epistemic capital: review priority, manual designation requirement, primary/secondary documents and review notes.

The accepted SWID repair is positive preservation evidence. Its adjudicated W03-A repair was rejected once, then required to use governed UID itinerary/question-list joins. On the accepted repair branch, V550 resolves itinerary rows to `source_family_uid + wave_uid`, preserves the manual gate fields, and fails closed when duplicate UID-resolved rows carry divergent gate content.

Thus identity authority does not retire itinerary semantics.

## Current-control non-inheritance defect

At Browser/control HEAD `20e8edbd0c9f2b07d31d1292f2d5864420c1a7c0`:

- `source_wave_identity_registry_35wave_v1.json` is absent;
- `ddm_source_wave_identity.py` is absent;
- `ddm_v550_question_use.py` still literal-matches normalized `source + wave` against the historical itinerary and returns normal/false defaults for an unmatched row.

The accepted SWID integration line and current Browser/control line diverge from merge base `25a63e08b0fcf7ef3dfc9de0c7b03325d26d918a`.

The census therefore records:

`EXISTING_ACCEPTED_AUTHORITY_NOT_INHERITED__CURRENT_CONTROL_EXECUTION_DIVERGENCE`

not missing authority.

## EVS1999 bounded residual gap

EVS1999 has substantial positive authority:

- current respondent source registry;
- current respondent semantic registry;
- accepted PREP71 R04 source/documentary packet;
- 35-wave per-wave authority registry with a 513-row first-pass authority binding containing `manual_designation_required`, plus semantic/position/directionality overlays.

But EVS1999 has no historical wave-level itinerary row, while EVS 1981/1990/2008/2017 are all `critical` and `manual_designation_required=true` there.

No existing object yet proves that the absent EVS1999 wave-level itinerary judgment is losslessly encoded elsewhere. That remains a bounded preservation/supersession gap; no neighboring-wave or per-question inference is allowed.

## Audit republication remains separate

The source-structure audit binding's 0 observed artifacts is preserved as negative/fail-closed authority. It does not reopen the recovered question-structure/manual core and it does not erase current-35 identity authority.

## No missing-authority promotion

No expectation is classified `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`.

## Next local request

Issued:

`HARVEST-003 QUESTION_SEMANTIC_MASTER_AND_DRIVER_FACET_LINEAGE`

It is limited to the exact old/new `questions_master_semantic.csv` and `questions_master_drivers.csv` identities, the mechanically provable row/field deltas, and the narrow human triage/review/adjudication lineage that produced them.

It explicitly forbids semantic regeneration, canonical selection by recency/completeness, and any reopening of the already recovered `EXP-001` manual/source-topology authority.
