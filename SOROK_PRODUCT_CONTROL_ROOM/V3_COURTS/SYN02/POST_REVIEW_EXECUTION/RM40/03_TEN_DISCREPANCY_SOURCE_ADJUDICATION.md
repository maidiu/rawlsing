# SYN02-RM40 — ten S04/S05 mismatch adjudications

**Status:** `SOURCE_LEVEL_ADJUDICATION__TEN_OF_TEN_RECONCILED__NO_NATIVE_GRANT`.
**Input matrix:** S05 at architecture target `321fa29bb3e51849a43cb7caf1600625bf215539`; S04 at the same target; independent S-R `ac55c36e42ded82957176896cbc5953db62f7209`; source hashes in `02_VERIFIED_480_CELL_M_TO_N_CROSSWALK.json`.
**Baseline:** 40 M rows × 12 N columns = 480 cells; **126 X / 354 dash**. The ten mismatches are exactly the cells where S05 has X but S04's last-column N list does not. **Adjudicated:** 124 X / 356 dash; ten cells changed; eight remain indirect source-only, two are unsupported and removed.

The distinction used here is strict:

- **DIRECT** — an old function reads or writes an N-specific object/input and a plausible first consumer can use it without adding a new semantic operation.
- **INDIRECT** — an old carrier can condition a later N response, but it does not itself form the N relation; the link survives only as a conditional carrier.
- **UNSUPPORTED** — no old function/field names the N relation and no plausible first consumer reads it without inventing a new operation.
- **HELD** — source exists but a required owner/rule/source/permission is missing.

No adjudication is a scientific issuance. A name in `NEED_AXES` or a capacity scalar is not a formed motive.

## 1. Discrepancy table

| M/N | Old source function(s) | N requirement | Adjudication | Potential first E2 reader | Falsifier |
|---|---|---|---|---|---|
| **M09/N01** | `Crack`, `update_cracks`, `ensure_min_cracks` | N01 need/object/motive formed through activity | **INDIRECT** — tension/contradiction carrier; no need axis, object or activity field | CAN008/C9 later appraisal; no current production Rule A | Remove/toggle crack state with world/activity fixed; N01 object/motive formation must not change. If N01 changes, there is a hidden direct path. |
| **M10/N01** | `Buffer`, `BufferCostProfile`, `update_buffers` | N01 need/object/motive | **INDIRECT** — external support/cost carrier; no need axis or motive target | C9/world interval → later CAN008 | Remove support buffer while holding actual world resource history; N01 object formation must stay independent. |
| **M11/N01** | `Framework`, `update_framework_weights`, `enforce_framework_caps` | N01 need/object/motive | **INDIRECT** — interpretive mediator/capacity operator; no need/object | CAN011 mediator → C9 later read | Remove framework weight/operator and hold event/activity fixed; N01 motive/object formation must not depend on it. |
| **M13/N01** | `PracticeStack`, `update_practice_stack` | N01 need/object/motive formed by activity | **INDIRECT** — practice category scalar; no need axis or actual activity episode | CAN011 PRACTICE → C9 E2 | Remove seeded/event practice scalar; no N01 object/motive formation should change absent actual activity. |
| **M14/N02** | `PeakRouting`, `update_loop_topology`, `update_solidarity_boundary`, `update_coherence` | N02 scoped care expectation / availability | **UNSUPPORTED** — loop/boundary/coherence has no caregiver, care, expectation or scope operation | None for N02; C9 only if a new expectation operation is added | Remove/change topology/boundary; N02 expectation with actual care history must remain unchanged. No X retained. |
| **M18/N01** | `RuptureShard`, `create_rupture_shard_from_event`, `update_wound_vector_from_rupture` | N01 need/object/motive | **INDIRECT** — rupture of an assumption/domain can disturb need response; no need axis/object | CAN012 rupture → later C9 | Remove rupture/wound update with world/event fixed; N01 need/object formation must not be inferred from it. |
| **M19/N01** | `MetabolizationProcess`, `compute_metabolization_delta`, `update_metabolization_and_plasticity_step` | N01 need/object/motive | **INDIRECT** — process changes capacity/biases; no need/object/activity formation | CAN012 process → later C9 | Sever process/prose effect; N01 object/motive formation must not change; if it does, the old path is doing illicit formation. |
| **M24/N01** | `stability_threshold_inertia`, `stability_inertia_dissipation` | N01 need/object/motive | **INDIRECT** — residue/inertia can condition persistence; no need object | CAN011 residue → later C9 | Remove inertia with event/activity fixed; N01 formation must be unchanged. |
| **M36/N01** | `infer_parent_baseline_and_regime`, `derive_child_expectation_baseline` | N01 need/object/motive | **INDIRECT** — `NEED_AXES` labels are expectation vocabulary, not a formed motive/object; source is primarily N02 | C9/CAN010 expectation read; no N01 motive | Remove default/expectation labels; no N01 object/motive is created; if a consumer claims one, the link is misclassified. |
| **M39/N01** | `maybe_inject_rupture_at_band_age` | N01 need/object/motive | **UNSUPPORTED** — age/RNG rupture has no need/object/activity link; the old N01 crosswalk warning is stale | None; CAN012 only if a real admitted event is supplied | Remove age injection; N01 formation remains unchanged. No X retained. |

## 2. Why eight are indirect rather than direct

The eight retained X cells are not evidence that these mechanisms construct needs or motives. They are historical carriers that can condition a later response if an owner-issued N01 operation exists:

- **M09/M18/M19/M24:** tension, rupture, metabolization and residue can alter how an already formed need/object is handled; they do not create one. N01 requires actual activity/object formation; a crack/rupture/process is a later condition, not the missing operation.
- **M10:** support/buffer resources can enable or constrain activity; the buffer record does not name a need or object.
- **M11:** a framework/mediator can interpret an object; it is not an object or motive.
- **M13:** practice categories can describe an activity history; the scalar does not establish that the activity occurred or that a motive formed.
- **M36:** the only N01-adjacent content is the finite `NEED_AXES` vocabulary; the function derives expectations and parent defaults, not motives or objects. It is primarily N02 and must not be promoted to N01 coverage.

Retaining X as `INDIRECT` preserves the S05 conditional historical-relevance claim while preventing the false inference that the old source already covers N01. The patch matrix marks these as `ADAPT` (or `REMOVE` for M36) and requires a new owner rule.

## 3. Why two are unsupported

**M14/N02.** `PeakRouting` and its topology/boundary/coherence functions operate on global loop labels, solidarity boundary movement and coherence. There is no caregiver, care act, availability, expectation, scope or reception. The event boundary target is a label, not care. The closest expectation source is M15/M36, not M14. The S05 X was an over-broad orientation claim; it is removed.

**M39/N01.** `maybe_inject_rupture_at_band_age` is an age-band random injection that creates a `RuptureShard`/`MetabolizationProcess` and wound bump. It has no need axis, object, activity or motive. Its old N01 warning is stale and should not be preserved as source coverage. It is replaced by admitted `RuptureRecord`/CAN012; N01 remains a separate need/object operation.

## 4. The other 470 cells

The remaining 470 cells are not adjudicated as new coverage:

- **116 unchanged X cells?** The final matrix retains 124 X: 116 untouched X + 8 indirect mismatch X. The exact count is in `02`. The 116 are conditional selected-source links where S04/S05 agree; none is a current import.
- **354 baseline dashes + 2 newly unsupported dashes = 356 final dashes.** No unsupported original link is silently promoted to X.
- A **dash** is not a negative scientific finding. It means S04 and S05 do not assert a direct selected-source link at this court. The original source/review may still be relevant through a new operation, but that requires an owner and a new function, not a matrix edit.

## 5. E2 reader and authority status

The potential E2 reader is the same class across the ten: a later C9/CAN008 semantic read, or a CAN011/CAN012 target read, not the old LLM summary or a V2 prose line. Current exact status remains:

- S36 `run_candidate_path` exists as a sourcefree C9 transaction, but production CAN008/CAN011 rule registries are empty at the reviewed cut.
- S37 is targetless/test-only; S48 is one-call transport; S49 natural B is empty; S52 is withheld.
- Therefore all ten adjudications are **source/design only**; none produces a native C9/C12 positive.

The original science owners remain: CAN010/CAN011 for need/motive/expectation/middle-state; CAN008 for immediate Rule A recruitment; CAN012 for rupture/metabolization; ADP016/017/SCI05 for memory/access/reflection; C0/C8/ADP019/SDTF for world/B/activity. The RM40 author does not issue any of these.

## 6. Changed-cell receipt

Exactly ten cells changed from the S05 baseline:

| Changed cell | Baseline | Final | Change |
|---|---|---|---|
| M09/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M10/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M11/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M13/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M14/N02 | X | — (UNSUPPORTED) | X removed |
| M18/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M19/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M24/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M36/N01 | X | X (INDIRECT) | relation downgraded; X retained |
| M39/N01 | X | — (UNSUPPORTED) | X removed |

All 40 M rows and 480 cells remain present in `02_VERIFIED_480_CELL_M_TO_N_CROSSWALK.json`; the matrix is versioned and does not rewrite S04/S05.

**No new psychological coefficient, no native rule, no current consumer, no production edit.**
