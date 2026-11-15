# D11 RESULT — Current V551/V551J/V552/V552J Downstream Consumption

**Court:** VOZHD TRII D11  
**Base SHA:** `92df14a7f3a9c2077b3e1a426ce3f4fa549e90eb`  
**Branch:** `agent/vozhd-trii-d11-current-downstream-consumption`  
**Disposition:** `PASS_WITH_MATERIAL_STRANDED_MEANING_AND_PROVENANCE_NARROWING`

## 1. Jurisdiction and proof boundary

This is a fresh current-main executable dependency/dataflow audit after Final R1 migration. It does not import frozen VT3 dependency conclusions as proof. Each ruling is based on a live current reader/call path, a current explicit exclusion/gate, or an absence at the current producer boundary proven by the reader schema/arguments.

D05 remains binding: no populated database was available to this court, so D11 makes **no claims about actual populated coverage, prevalence, support distribution, or empirical completeness**. Static executable/dataflow rulings are not blocked by that limitation.

No architecture recommendation is made. D11 does not adjudicate D09 meaning-field normativity, D10 empirical→structural ontology legitimacy, D12 terminal-human necessity, or later storage architecture.

## 2. Finite current-main verdict

The current downstream empirical spine is materially narrower than the V550/V550J output surface.

The **active non-joint spine** is:

`V550 answer_distribution / country_answer_distribution`
→ `ddm_v550_bridge.py`
→ current Final R1 relation-authority re-resolution
→ V551 v3 directional adjudication / relation-evidence atoms / coverage
→ V552 pressure components / pressure observations / structural facts
→ V552J structural matching where joined
→ V553 canonical V552J input/handoff consumer.

The **active joint spine** is:

V550J governed `joint_response_pattern_index`
+ `joint_response_pattern_item_index`
+ `joint_pattern_relation_signature`
→ V551J component matching and packet certification
→ V552J producer-bound join with V552 structural facts
→ V553 canonical V552J input/handoff consumer.

A large part of the remaining V550/V550J analytical surface is not on either spine.

## 3. V550 → V551: the bridge is broad, canonical V551 v3 is narrow

`ddm_v550_bridge.py` knows about all of the following V550 families:

- `answer_distribution`
- `country_answer_distribution`
- `position_distribution`
- `position_indicator_summary`
- `indicator_answer_matrix`
- `outlier_cohort_summary`
- `secondary_indicator_summary`
- `recursive_branch_nodes`
- `branch_position_signature`
- `branch_relation_co_signature`
- `branch_co_signature`
- `question_response_attitude_cloud`
- quarantine/audit families.

But bridge presence is not canonical V551 consumption. `BRIDGE_EVIDENCE_LANE_MAP` assigns:

- answer/country-answer distributions → `direct_relation_response`;
- indicator matrix, outlier, secondary, recursive branch → `derived_determinicity`;
- position distribution, position indicator, branch position signature → `position_context`;
- attitude cloud and branch relation/co-signatures → `disabled_artifact`.

The decisive current gate is in `ddm_v551_atoms.py`:

`APPROVED_DIRECT_TABLES = {"answer_distribution", "country_answer_distribution"}`.

`build_v551_certification_candidate_bridge` requires all of:

1. `directional_applicability_status == APPLICABLE_BY_AUTHORITY`;
2. `bridge_evidence_lane == direct_relation_response`;
3. `source_table` is exactly `answer_distribution` or `country_answer_distribution`;
4. substantive;
5. not missing;
6. not special.

Therefore bridge admission or a familiar field name does **not** prove canonical V551 v3 consumption. Canonical V551 v3 atom production excludes the position, recursive, indicator, cohort, co-signature and cloud families listed above.

## 4. Final R1 authority is re-resolved before use

The bridge does not trust stale upstream relation semantics.

`_base_bridge_row` calls `apply_question_relation_authority`. `_bridge_additional_fields` treats QUC-owned authority fields specially and records stale disagreement as:

`STALE_CANDIDATE_AUTHORITY_OVERRIDDEN_BY_CURRENT_QUC`.

`apply_question_relation_authority` then applies the installed Final R1 question-relation authority. Resolved directional rows receive current structural coordinates and current eligibility. Non-directional, administrative, blocked, unresolved or nonmatching rows fail closed and cannot retain stale relation coordinates.

There is one narrow no-match preservation rule: when the active registry has no row, an already-certified QUC relation row may survive only if its semantic role is `RELATION_EVIDENCE`, both directional eligibility flags are true, and structural mapping is `COMPLETE`. That path is stamped:

`QUC_AUTHORITY_PRESERVED_ACTIVE_REGISTRY_NO_MATCH`.

Otherwise coordinates and relation eligibility are cleared.

**Ruling:** empirical row content can survive while old relation-authority semantics are `SUPERSEDED_BY_CURRENT_AUTHORITY` / `RE_RESOLVED_BEFORE_USE`.

## 5. Unary position-conditioned meaning and conditional determinicity

### 5.1 `position_distribution`

`position_distribution` enters the bridge as `position_context`, not as a direct relation response. It therefore fails the canonical V551 v3 source-table gate.

V552 later has a `position_conditioning_profile`, but that profile is built from **observed V552 pressure observations whose direct V551 atoms carry nonblank `subject_position_signature` or `position_conditioning` metadata**. `_roll` groups those pressure observations and uses:

`basis = equal_weight_mean_of_v552_primary_pressure_observations`.

That is not proof of equivalence to the upstream unary empirical object `P(response | position_field = position_value)`. The original position predicate, denominator, response surface and row identity are not demonstrated to survive.

**Ruling:** exact unary `position_distribution` meaning is `STRANDED`. The V552 profile is a later, non-equivalent recomputation/rollup.

### 5.2 Auxiliary conditional path

`ddm_v551_conditional.py` can build a `conditional_determinicity_index` from eligible `derived_determinicity` bridge rows. This proves an auxiliary compatibility capability exists.

It is not the canonical V551 v3 producer path: `compile_v551_relation_evidence_atoms.py` emits only directional adjudication, atoms and coverage.

`compile_v552_structural_ddm.py` optionally loads a conditional-determinicity parquet and passes it to `build_v552_structural_outputs`, but `build_v552_structural_outputs` does not use the argument in any build step and creates an empty `conditional_determinicity_status_audit`.

**Ruling:** the current V552 conditional-determinicity socket is `DEAD_SOCKET`. Arbitrary conjunction conditional distributions are not demonstrated to be reconstructed by `strata_path`, `position_modifiers`, or `conditional_strata_weights`; those metadata fields do not prove predicate/denominator equivalence.

## 6. Explicit stranded-meaning adjudications

| Meaning | D11 ruling | Current-main reason |
|---|---|---|
| Unary position-conditioned empirical distributions | `STRANDED` | `position_distribution` is `position_context`; canonical V551 v3 excludes it; V552 profile is non-equivalent rollup. |
| Arbitrary conjunction conditionals | `STRANDED` | No canonical reconstruction; auxiliary conditional socket is unused by V552. |
| Historical V548 branch-cohort meaning | `STRANDED` | `recursive_branch_nodes` is `derived_determinicity` and excluded from canonical V551 v3. |
| Historical V549 branch-conditioned cotravel | `STRANDED` | branch relation/co-signature families are `disabled_artifact`; current generic cloud is not equivalent. |
| Current V550 attitude cloud | `STRANDED` | `question_response_attitude_cloud` is explicitly `disabled_artifact`. |
| Current V550J joint response patterns | `CONSUMED_AFTER_TRANSFORMATION` | Three governed V550J tables are mandatory V551J inputs and become component/packet contracts. |
| V550J association summaries | `COMPATIBILITY_ONLY` | Association presence is audited, but core packet semantics explicitly do not consume association measurements. |

These are implementation/dataflow rulings only; D11 does not decide which stranded meanings are terminally required.

## 7. V550J direct prepared path versus alternate modes

`compile_v550j_joint_response_patterns.py` preserves distinct execution modes.

In `prepared_required` + `--forbid-database-access` mode:

- database URL use is rejected;
- an explicit prepared substrate and manifest are required;
- the parquet is validated against the shared-substrate contract and logical hash;
- family selection runs directly over the prepared rows;
- the explicit prepared branch does not call live question re-harmonization.

Other modes (`prepared_or_build`, `prepared_or_forensic_fallback`, `forensic_reharmonize`) may independently prefetch/query and call harmonization. D11 does not collapse those paths into the no-database prepared ruling.

The shared prepared substrate can carry respondent identity, weights, base/joint membership and overlap roles, and association-eligibility metadata. Those fields can affect V550J computation.

## 8. Exact respondent grain stops at V550J

V550J itself can persist `joint_pattern_respondent_membership` with:

- `respondent_id`;
- `respondent_id_norm`;
- pattern ID/signature;
- weight;
- answered-item count;
- aggregate pattern support/probability.

But `compile_v551j_joint_evidence_packets.py` has no membership-path argument, and the governed V550J→V551J producer boundary is exactly:

1. `joint_response_pattern_index`;
2. `joint_response_pattern_item_index`;
3. `joint_pattern_relation_signature`.

Therefore exact respondent membership is not carried through the canonical V550J→V551J boundary.

**Ruling:** respondent-grain joint membership is `STRANDED` after V550J. Aggregate joint-pattern semantics survive; exact respondent identity does not.

## 9. V551J consumption and optional sockets

V551J verifies the governed V550J producer bundle and the V551 v3 producer bundle, including scope, typed state, canonical parquet declaration, hashes, row counts and contract versions.

It then matches V550J pattern items to V551 atoms. Component rows carry both sides of the match: V550J item response identity and V551 `atom_id`, atom-contract hash, empirical distribution ID, measurement-contract hash, counts/percentages and structural identity.

Packet rows carry pattern/packet identity, component hashes, matched atom IDs/hashes, joint measurement and semantic/structural signatures, component denominator vectors, certification state and explicit downstream permissions.

### Association index

The current v2.2.3 builder records whether association measurements are present, but explicitly sets:

`association_measurements_used_in_core_packet = False`.

Its association sidecar is initialized empty. Therefore association row semantics do not enter the core packet.

### Position signature and meaning summary

The optional `position_signature` and `meaning_summary` arguments exist, but the current v2.2.3 builder initializes the corresponding sidecars empty.

**Rulings:**

- association rows: `COMPATIBILITY_ONLY` (presence metadata, not core semantics);
- V550J position signature: `DEAD_SOCKET`;
- V550J meaning summary: `DEAD_SOCKET`.

## 10. V551 → V552 evidence identity

Canonical V552 requires exactly the V551 v3 producer bundle:

- `relation_evidence_atoms`;
- `directional_distribution_coverage`;
- `directional_candidate_adjudication`.

It verifies manifest identity, schema/compiler version, canonical artifact hashes, row counts, run/scope identity, atom uniqueness, distribution uniqueness and conservation.

For each V551 atom, `build_v552_pressure_component_index` creates a V552 pressure component and explicitly preserves:

- `source_atom_id`;
- source atom-contract hash;
- source measurement-contract hash;
- `empirical_distribution_id`;
- response identity;
- V551 signed side/intensity and projection-authority hash;
- counts/percentages/weight status;
- evidence/provenance basis.

V552 does not reinterpret V551 sign/magnitude.

Pressure observations group components by `empirical_distribution_id`, preserve source atom IDs/hashes, preserve unresolved mass from coverage, and mint a new pressure-measurement hash.

Then `_facts` mints a new `v552_structural_fact_id` whose source is the pressure observation and whose source row hash is the pressure-measurement hash.

**Identity ruling:** V552 has strong exact provenance to V551 atom/distribution identities, but the V552 structural fact is a **new derived structural statement**, not the same semantic object as the empirical distribution.

## 11. Current V552J producer-bound join

The Final R1 current producer-bound compiler is `compile_v552j_structural_handoff.py`; `test_w06_v552j_join.py` tests that compiler and the `ddm_v552j_handoff.py` join semantics.

It consumes:

- V551J certified packets;
- V551J review rows enriched from candidate packet identity;
- V552 structural facts;
- V552 temporal-key source rows.

It enforces exact run/source/wave/country-or-shard scope before semantic matching. Semantic match score is built from relation axis, target entity, driver facet and question identity. A selected fact must meet the structural-match threshold.

A joined row mints `v552j_join_id` and carries:

- V551J `packet_id`;
- selected `v552_structural_fact_id`;
- selected V552 temporal-key source ID;
- structural dimensions;
- pressure score/status;
- measurement evidence state;
- join permission and repair debt;
- producer manifest SHA256s.

Only certified, producer-authorized, observed structural measurements can receive `ALLOW`; review rows remain review-only and unresolved/denied rows do not become observed zero.

The join schema does **not** carry V551 atom IDs or respondent IDs.

## 12. V552J → V553 current Final R1 seam

`compile_v552j_structural_handoff.py` writes:

- canonical `v552j_structural_join_index`;
- canonical `v552j_join_audit`;
- compatibility-kind `v552j_v553_input_index`;
- compatibility-kind `v552j_to_v553_handoff_index`.

The compatibility projection aliases:

- `packet_id` → `v552j_packet_id`;
- `v552j_join_id` → `v553_input_id`;
- selected V552 fact/key identities into V553 source fields.

Although those two artifacts are marked `artifact_kind=compatibility`, they are **active current V553 consumer surfaces**.

`ddm_v553_canonical_harmonization.py` explicitly states that the old `v552j_structural_handoff_packet.json` is obsolete. It fail-closed verifies the full V552J publication: producer manifest, join/audit, V553 input/handoff indexes, readiness and handoff manifest. It rejects missing, corrupt, schema-invalid or integrity-invalid surfaces.

`ddm_v553_temporal_pressure.py` then reads the V553 input/handoff rows, forms structural/temporal profiles and carries:

- `source_v552j_packet_ids_json`;
- `source_v552j_input_ids_json`;
- selected V552 structural-fact IDs;
- selected V552 temporal-key source IDs;
- structural pressure looked up from the selected V552 fact.

This is the last demonstrated current path on which packet/join/V552 fact row identities remain explicit semantic provenance.

## 13. Evidence identity toward V554–V558

The identity chain narrows after V553.

V554 turns V553 country/year pressure into bounded seed affordances. Its row-level `source_pressure_ids_json` uses synthesized `country:year` identifiers and it mints `seed_affordance_id`. It does not expose V551 atom IDs or V550J respondent IDs as direct seed keys.

V555 carries V554 seed-affordance IDs into mediation-slot/register objects. V556 consumes V555 mediation contract status into pressureflow slots and V557 consumes V556 into renderer-boundary objects. V556 and V557 also retain V553 harmonization evidence as artifact-level authority context, but that is not the same thing as preserving the original empirical row identity.

V558 then reads the V557 renderer contract, readiness report, prompt-shape audit and forbidden-inference audit, revalidates runtime admissibility, and constructs a normalized runtime-input governance object. That object carries V557 run/artifact paths and renderer/governance fields; it does not restore or directly key on V551 atom IDs, V550J respondent IDs, V552 structural-fact IDs, or V552J packet/join IDs.

Thus the demonstrated identity ladder is:

`V550 source_row_hash`
→ `V551 atom_id / empirical_distribution_id`
→ `V552 source_atom IDs/hashes + v552_structural_fact_id`
→ `V552J packet_id + v552j_join_id + selected V552 fact/key IDs`
→ `V553 source_v552j_packet/input IDs + selected V552 fact/key IDs + new temporal key`
→ `V554 country:year pressure IDs + seed_affordance_id`
→ later mediation/pressureflow/renderer contract IDs
→ `V558 normalized runtime-input governance fields + V557 run/artifact references`.

An artifact pointer, a derived structural statement ID, and semantic preservation are not treated as interchangeable.

## 14. Classification summary

### Actively consumed / consumed after transformation

- V550 `answer_distribution`;
- V550 `country_answer_distribution`;
- current question-use/current relation authority metadata after re-resolution;
- V551 atoms/adjudication/coverage;
- V550J governed joint pattern index/item/relation-signature tables;
- V552 structural facts/temporal-key source rows;
- V551J certified/review packet identities at V552J;
- V552J V553 input/handoff compatibility surfaces at V553.

### Re-resolved / superseded

- stale upstream question-relation structural authority.

### Compatibility only

- auxiliary derived-determinicity/conditional helper path;
- V550J association index row semantics (presence audit only);
- V552J V553 projection is named compatibility but is an active V553 reader surface.

### Dead sockets

- V552 `conditional_determinicity` semantic input;
- V551J optional position-signature sidecar;
- V551J optional meaning-summary sidecar.

### Stranded / no demonstrated canonical consumer

- exact V550 `position_distribution`;
- position indicator summary;
- outlier/secondary determinicity summaries;
- recursive branch nodes;
- branch position signature;
- branch relation/co-signatures;
- current attitude cloud;
- V550J exact respondent membership.

## 15. No-DB and nonclaims

D11 does not claim:

- that any of these artifacts are populated in production;
- how many rows/waves/countries actually satisfy the gates;
- actual support/prevalence/completeness;
- that stranded meaning is terminally required;
- that current empirical→structural interpretation is normatively correct;
- an architecture/storage prescription.

Those questions remain outside D11 jurisdiction.

## 16. Machine-readable companions

- `CURRENT_DOWNSTREAM_DATAFLOW.csv` gives exact edge-level readers, transforms, gates, outputs and identity rulings.
- `UPSTREAM_FACT_CONSUMER_MATRIX.csv` gives one-family-at-a-time consumption/equivalence/provenance rulings.
- `RESULT.json` contains the finite verdict and explicit stranded-meaning adjudications.
