# HARVEST-004 Adjudication — D62 Producer and Duplicate-Shadowing Provenance

Status: `ADJUDICATED__GSS_LITS_IDENTITY_MISMATCH_APPEND_PRODUCER_PROVED__LAST_ROW_SEMANTIC_PRECEDENCE_UNAUTHORIZED__PRE_A_TRANSIENT_MASTER_UNRECOVERED`

Packet SHA-256: `b7ce4c0de1aea7db1e08d4c4faf3447f22809b62b95800502f0f3ee52c0c7abd`
Packet size: `14,235,501` bytes

## Packet integrity

Browser independently inspected the uploaded ZIP and verified:

- exact outer SHA-256 and byte size;
- ZIP integrity;
- all `111/111` internal `SHA256SUMS.txt` entries;
- required receipts and payload present;
- no updater was executed by the local worker.

## Holding 1 — the GSS/LiTS duplicate layer has an exact recovered producer

Recovered producer:

- `apply_gss_lits_p0_structural_mappings.py`
- SHA-256 `6ddb066f76001488debcb822352aa39b5eabe3fd544d832eed783080e41ea6b9`

The producer explicitly describes itself as a pattern-based first-pass scaffold, requires review files, and says it must not pretend ambiguous rows are final.

Its append logic reads `questions_master_drivers.csv` and `questions_master.csv`, then states that if GSS/LiTS rows exist in `questions_master` but not drivers it will append pending rows. Crucially, existence is tested only through `item_id`:

`existing_ids = set(drivers["item_id"].astype(str))`

and GSS/LiTS rows whose `questions_master.item_id` is absent from that set are appended. New rows begin as blank shells in the driver-master schema with copied identity/source text columns and `mapping_status = pending_structural_facet_mapping`.

The same producer then pattern-maps GSS/LiTS rows and may assign `accepted_block_child`, driver/facet/domain/axis/target fields and review notes that still say target/relation may need refinement.

This proves an intentional row-append mechanism. It does **not** prove intentional semantic replacement of an earlier row sharing the same `(source,wave,var_name)`.

## Holding 2 — the append condition misidentified already-present questions as missing

Browser mechanically inspected the exact `d62accad...` bytes from the packet.

`d62accad...` has:

- 28,983 rows;
- 18,519 distinct `(source,wave,var_name)` keys;
- 10,462 duplicated natural keys;
- 10,464 duplicate-excess rows.

The first 18,528 rows have 18,519 distinct natural keys. The final 10,455 rows are all GSS/LiTS:

- GSS: 6,021;
- LiTS: 4,434.

Every one of those 10,455 tail natural keys already exists in the first 18,528 rows: `10,455 / 10,455` exact `(source,wave,var_name)` overlap.

But among the corresponding 10,455 first-segment GSS/LiTS rows, 10,454 have blank `item_id`. The appended tail has 10,455 distinct nonblank `item_id` values.

Therefore the producer's `item_id`-only absence test treated an already-present question occurrence as absent because the earlier semantic representation lacked the newer identity field. It then appended a second physical representation of the same source/wave/variable question.

Classification:

`IDENTITY_MIGRATION_MISMATCH__DUPLICATE_QUESTION_REPRESENTATION_APPENDED`

## Holding 3 — downstream last-row-wins converted that carrier defect into effective semantic precedence

HARVEST-003 already proved that the historical question-structure builder consumes `questions_master_drivers.csv` through a dict keyed by `(source,wave,var_name)` and therefore keeps the last duplicate row.

H004 now proves why the later duplicate row exists.

The two stages use incompatible identity assumptions:

1. GSS/LiTS structural onboarding decides whether a question already exists by `item_id`;
2. the structure-register consumer identifies that same question by `(source,wave,var_name)`;
3. when old rows lack `item_id`, onboarding appends a second row;
4. the consumer collapses both rows and silently chooses the later one by row order.

No recovered producer, migration specification, review artifact or acceptance receipt defines last-row-wins as semantic supersession law.

The migration specification instead requires preservation of existing columns (`do_not_delete_existing_columns: true`) and backups before writing. The GSS/LiTS producer calls itself a first-pass scaffold and requires review. These are incompatible with treating incidental row order as authorization to erase earlier semantic authority.

Disposition:

`DUPLICATE_SHADOWING_PRODUCER_PROVED__INCIDENTAL_CARRIER_KEY_COLLISION__NO_SEMANTIC_SUPERSESSION_AUTHORITY`

In plain terms: the system did not consciously re-adjudicate 2,056 GSS/LiTS semantic judgments. It failed to recognize old semantic rows and new structural rows as the same questions because one side lacked `item_id`, appended second rows, and a separate downstream dict accidentally made the second rows win.

## Holding 4 — later structural enrichment is real authority material, but it must be separated from semantic retirement

Recovered migration law adds structural fields such as:

- `question_block_id`
- `structural_domain_id`
- `driver_facet_id`
- `relation_axis_id`
- `target_entity_id`
- `mapping_status`
- `evidence_kind`
- review/missingness/strata/channel/forbidden-inference fields.

The recovered mapping-status vocabulary includes `accepted_exact`, `accepted_block_child`, `accepted_strata_only`, `accepted_context_only`, review/defer/reject and pending states.

Recovered later GSS/LiTS deepening code (`deepen_gss_lits_semantic_rows.py`, SHA `a0c164aed477041a6717054a17eea9faa822595ccd44cdb24817373bb03454e7`) performs an in-place rule-based pass only over pending GSS/LiTS rows and assigns structural/semantic fields plus `semantic_deepening_pass` provenance. It is useful later structural capital, but its own rule-based mechanism is not a global owner adjudication and does not authorize retirement of a prior semantic row merely because both representations occupy one CSV.

The lawful preservation posture is therefore **noncollapse**:

- preserve positively accepted prior semantic judgments;
- preserve later structural mappings/review states as their own authority assertions where their provenance and scope are valid;
- do not use row order to make one class destroy the other.

This directly supports the planned normalized unified-authority substrate: semantic assertions and structural mappings need distinct relation identities/cardinalities around a common question identity.

## Holding 5 — the remaining 92 Register-A → d62 differences are not duplicate shadowing

Of the 2,148 Register-A keys whose nine semantic/driver fields differ from the final effective d62 lookup:

- 2,056 have duplicate d62 natural keys and belong to the proved duplicate-shadow mechanism;
- 92 have exactly one d62 natural-key row.

For those 92:

- 81 change only `final_driver_label`;
- 11 change only `semantic_secondary_driver`;
- source distribution is Afrobarometer 67, Arab Barometer 11, WVS 5, EVS 4, Asian Barometer 3, Latinobarómetro 2.

The 11 secondary-driver changes are Arab Barometer W8. Recovered `apply_arab_barometer_w8_p0_structural_mappings.py` explicitly assigns blank `semantic_secondary_driver` inside direct P0 promotion specifications while setting structural/semantic fields and `accepted_context_only`/`accepted_block_child` statuses.

These 92 are therefore a different lineage: later in-place structural normalization/remapping rather than the GSS/LiTS duplicate append defect. H004 does not establish that every changed prior semantic value was losslessly superseded. Preserve prior and later assertions until the full-universe quality/authority court adjudicates the relevant scopes.

## Holding 6 — the exact transient pre-d62 master that generated Register A was not recovered

H004 found only two distinct physical driver-master identities in the searched corpus:

- V525b `53feb282...` — 6,211 rows;
- later `d62accad...` — 28,983 rows.

V525b does not mechanically reproduce Register A: only 5,128 Register-A keys match it and 1,963 matched keys differ across the nine-field projection.

Therefore V525b is not the immediate master that generated Register A. The exact transient intermediate master is not physically recovered by H004.

Register A remains a positive downstream witness of the effective pre-shadow semantic/driver projection for its covered keys. The missing transient full master is a bounded provenance gap, not permission to regenerate or guess it.

Disposition:

`TRANSIENT_PRE_D62_MASTER_NOT_RECOVERED__REGISTER_A_EFFECTIVE_PROJECTION_WITNESS_PRESERVED`

The historical tree identifies `build_questions_master_drivers.py` SHA `e056bd2b8b388a8ad133b8a98682e68fb1612aedf6e6689122054d8c26925b6b` / 6,445 bytes / 2026-05-10 13:23 EDT, but H004 did not package that script's bytes. Its absence does not block the duplicate-producer ruling above.

## Holding 7 — V525b contains a small pre-existing natural-key imperfection that must not be conflated with H004

The 6,211-row V525b driver master has:

- 6,202 distinct `(source,wave,var_name)` keys;
- 7 duplicate natural keys;
- 9 duplicate-excess rows;
- 4 blank-key rows.

This is a small historical cardinality imperfection and should be checked during future canonical question-identity work. It is not the cause of the later 10,455-row GSS/LiTS duplicate layer.

## Adjudication

- `HARVEST-004`: `ADJUDICATED__GSS_LITS_IDENTITY_MISMATCH_APPEND_PRODUCER_PROVED__LAST_ROW_SEMANTIC_PRECEDENCE_UNAUTHORIZED__PRE_A_TRANSIENT_MASTER_UNRECOVERED`
- `EXP-007 DRIVER_FACET`: later structural capital exists, but d62 is not a lawful flat semantic successor; duplicate-shadowing mechanism is positively explained as identity/cardinality collision.
- `EXP-006 EARLY_SEMANTIC_MASTER`: V525b accepted authority remains protected; H004 strengthens the reason not to infer retirement from d62 packaging.
- `EXP-030 SUPERSESSION_REGISTRY`: no global supersession law recovered; last-row-wins specifically rejected as authority law for this lineage.
- no substantive semantic authority creation is authorized by H004.

## Next dependency

D62 archaeology no longer needs to be the active frontier. The next useful evidence step is to establish the governed current-35 question-occurrence universe and mechanically map which existing semantic/driver/structure authority surfaces cover each identity, without creating or adjudicating new semantics.

This will provide the identity spine and coverage baseline needed for the future unified empirical-authority substrate and for the subsequent full-universe quality court.
