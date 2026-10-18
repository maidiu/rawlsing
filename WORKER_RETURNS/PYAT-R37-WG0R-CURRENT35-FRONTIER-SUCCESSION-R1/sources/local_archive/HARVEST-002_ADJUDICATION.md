# HARVEST-002 Adjudication — Current-35 Scope Identity and Audit-Binding Lineage

Status: `ADJUDICATED__EXISTING_AUTHORITY_NOT_INHERITED__FOLLOW_UP_REQUIRED`

Packet SHA-256: `70789a6556f70c2c6be0771defe00fec918b7e64514e37d82744493431f1dc37`

## Packet integrity

Browser independently verified the uploaded ZIP bytes and size (`89,531` bytes), ZIP integrity, and every one of the 25 entries in `SHA256SUMS.txt`. The packet reports 147 physical-manifest rows and 17 distinct packaged SHA identities.

## Holding 1 — the source-structure audit binding is a fail-closed publication gate, not a populated current-35 carrier

Exact recovered object:

- `source_structure_audit_binding_35wave_v1.json`
- SHA-256 `d8b73c0fc2498084c69adf0703313286c417c0170431613a024eec39412a68ce`
- schema `source_structure_audit_binding_35wave_v1`
- status `BLOCKED_REQUIRES_HASH_BOUND_AUDIT_REPUBLICATION`
- authority scope `CLOSED_35`
- expected wave UIDs: 35 distinct
- observed wave UIDs: 0
- artifacts: 0

Its expected UID set contains `wv_evs_1999_v1` and does not contain Asian Barometer W6. Its blockers explicitly require republication of hash-bound source-structure audits for exactly 35 UIDs before this binding can be green.

Therefore `observed=0` does **not** mean Rawlsing has zero current-35 identities. It means this particular audit-publication binding is intentionally fail-closed pending publication of its 35 hash-bound audit artifacts.

## Holding 2 — the governed current-35 source-wave identity authority already exists

HARVEST-002 recovered the exact identity kernel:

- `ddm_source_wave_identity.py`
- SHA-256 `4847f568d91ec7f94157e09c9a5d28052e85d7ff436877fb63bcd9343c24af7e`

It loads `data/ddm_build_copy/bindings/source_wave_identity_registry_35wave_v1.json`, requires declared versus actual CLOSED_35 count equality, resolves source family before wave, exposes governed UIDs, and fails closed when `require_closed_35` is requested for a recognized excluded identity.

Browser Git recovery then located that exact registry on the accepted SWID integration lineage `agent/source-wave-identity-repair-integration`:

`data/ddm_build_copy/bindings/source_wave_identity_registry_35wave_v1.json`

Git blob SHA-1: `ae09ab645d5d134c4462a012da57dbe02708b690`

The registry declares:

- `production_membership_set = CLOSED_35`
- `production_member_count = 35`
- authority basis: `question_relation_registry_35wave_active_v1.csv source_family/canonical_wave identities`
- recognized excluded: `Asian Barometer|W6`
- EVS 1999 UID `wv_evs_1999_v1` with `governance_state=CLOSED_35` and `closed_35_member=true`
- Asian Barometer W6 with `governance_state=RECOGNIZED_EXCLUDED` and `closed_35_member=false`

Current-35 scope identity authority therefore exists. No new current-35 identity wisdom is authorized for creation.

## Holding 3 — a 35-entry per-wave authority registry also exists

HARVEST-002 recovered:

- `wave_authority_registry_35wave_v1.json`
- SHA-256 `3670d056c45c188843681535feb8543cf5a4ad20f2d0a067ce4f6b16b944888e`
- scope `CLOSED_35_WAVES`
- 35 distinct source-family/canonical-wave entries
- EVS 1999 present; Asian Barometer W6 absent.

The EVS 1999 entry hash-binds a 513-row first-pass authority table and 513-row semantic, position-conditioning and directionality overlays. The first-pass schema explicitly contains `manual_designation_required`, `designation_confidence` and `rationale`.

This proves substantial EVS1999 manual/semantic authority exists. It does **not** prove lossless replacement of the separate wave-level itinerary fields.

## Holding 4 — the historical itinerary remains manual semantic capital

The only recovered `question_wave_itinerary.csv` identity remains:

`866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3`

It has 35 rows, includes Asian Barometer W6 and omits EVS 1999. Its manual fields are:

- `review_priority`
- `manual_designation_required`
- `primary_docs`
- `secondary_docs`
- `review_notes`

EVS 1981, 1990, 2008 and 2017 are all `critical` with `manual_designation_required=true`. EVS 1999 has no itinerary row.

No identity registry, source census or per-question authority table is permitted to silently invent the absent EVS1999 wave-level itinerary judgment.

## Holding 5 — accepted SWID work preserves itinerary semantics by re-keying; it does not retire them

Browser recovered the accepted SWID repair/adjudication lineage at `agent/source-wave-identity-repair-integration`.

`TERMINAL_RESOLUTIONS_W06D.json` records all 26 mandatory active issues terminally resolved at the static closure, including `SWID-016`, while explicitly not claiming a runtime pass.

`RESOLUTION_LEDGER.json` records that Vozhd rejected the first W03-A return, required V550-local UID itinerary and question-list joins, and accepted the amended architecture without identifying an unowned semantic behavior change.

On that repaired branch, `ddm_v550_question_use.py` resolves both the candidate record and itinerary rows to governed `source_family_uid + wave_uid`; divergent duplicate gate content fails closed; the returned gate still preserves the historical `review_priority`, `manual_designation_required`, `primary_docs`, `secondary_docs` and `review_notes`.

Thus the accepted SWID architecture is preservation/re-keying of the itinerary authority, not semantic supersession of it.

## Holding 6 — current Browser/control did not inherit the accepted SWID repair

At Browser/control HEAD `20e8edbd0c9f2b07d31d1292f2d5864420c1a7c0`:

- `data/ddm_build_copy/bindings/source_wave_identity_registry_35wave_v1.json` is absent;
- `data/ddm_build_copy/ddm_source_wave_identity.py` is absent;
- current `ddm_v550_question_use.py` Git blob `8d90a5116fd05b5db17e9b4645638a3aa6fc1131` still selects itinerary rows by literal normalized `source` + `wave` and returns default `review_priority=normal`, `manual_designation_required=false` when no row matches.

The accepted SWID integration branch and current Browser/control line diverge from merge base `25a63e08b0fcf7ef3dfc9de0c7b03325d26d918a`; the current line is not a descendant of the SWID repair integration line.

Therefore the defect is:

`EXISTING_ACCEPTED_AUTHORITY_NOT_INHERITED__CURRENT_CONTROL_EXECUTION_DIVERGENCE`

It is **not** `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`.

## Holding 7 — source dataset manifests corroborate current physical scope but are not semantic scope authority

The recovered source dataset manifests contain 44 rows/datasets, include EVS 1999 and omit Asian W6. They are useful source-inventory corroboration. They do not supersede the governed identity registry or itinerary manual semantics.

## Disposition

- `HARVEST-002`: `ADJUDICATED__EXISTING_AUTHORITY_NOT_INHERITED__FOLLOW_UP_REQUIRED`
- `EXP-002 CURRENT_35_SCOPE`: existing accepted identity/scope authority is mapped; current-control inheritance is not closed.
- `EXP-018 V550`: current-control itinerary lookup divergence is positively located.
- `EXP-026 EVS`: EVS1999 has substantial existing source/respondent/per-question authority; wave-level itinerary-gate supersession remains unproved.
- audit-publication binding remains intentionally blocked until hash-bound audit republication.
- no new semantic authority creation is authorized.
