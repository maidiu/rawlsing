# FIABC-A03 — Eliminated Stage Assumptions

This file records **redesign doctrine**, not an assertion that every current runtime path already obeys it.

## 1. Immediate predecessor is not the only lawful upstream

Dva's `ARCHITECTURE_PASS_LAW.md` requires workers to reason over **cumulative lawful upstream reality**, not merely the immediate predecessor, and provides `DIRECT_UPSTREAM_REUSE_SUFFICIENT` as an explicit disposition. It then states that direct DAG reuse is first-class and that stages must not force all earlier material through the current stage.

Evidence: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/ARCHITECTURE_PASS_LAW.md`.

**Eliminated assumption:** every piece of information must be copied through every numbered stage between producer and consumer.

## 2. Logical jurisdiction does not require physical stage isolation

The accepted HQ genealogy freezes:

`SEMANTIC_STAGE_IDENTITY != SEPARATE_PHYSICAL_STAGE`

and allows stage rename, physical co-packaging, derivation on demand and caches provided exact authority/replay survives.

Evidence: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/31_PREV3_ARCHITECTURE_GENEALOGY_R1_HQ_JOIN_AND_DISCRIMINATOR_AUTHORITY.md`, `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PREV3_ARCHITECTURE_GENEALOGY_R1/HQ_JOIN/FUNCTIONAL_ACCEPTANCE_CONSTITUTION.md`.

**Eliminated assumption:** one logical semantic distinction requires one standalone file/table/program boundary.

## 3. A later object is not owner of all earlier truth

Dva's accepted direct-DAG law assigns each transformation only its unique new meaning. Publication and repository stages are explicitly non-reowning; exact producer refs survive.

Evidence: `b06184f6535dff856914790e8f88855421708677:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PREV3_ARCHITECTURE_GENEALOGY_R1/DVA_INHERITANCE/RESULT.md`, `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`.

**Eliminated assumption:** if V555/V557/V558 carries an upstream value, that carrier becomes authoritative owner of the value.

## 4. Canonical semantic product is not mandatory permanent payload

Trii's genealogy distinguishes D12/D13 information-theoretic obligations from D15's selected append-only persistent C11 strategy. The accepted HQ join makes this explicit:

`CANONICAL_SEMANTIC_OBJECT != MANDATORY_PERMANENT_PAYLOAD_TABLE`.

Evidence: `183a2c33639c1da8be38999dce832782258c56b4:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PREV3_ARCHITECTURE_GENEALOGY_R1/TRII_D00_D15/RESULT.md`, `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/31_PREV3_ARCHITECTURE_GENEALOGY_R1_HQ_JOIN_AND_DISCRIMINATOR_AUTHORITY.md`.

**Eliminated assumption:** correctness requires every canonical semantic object to have a permanently stored transformed row representation.

## 5. Rebuildable is not disposable

Chetiri C07 makes semantic-product requirement, physical persistence, warm retention and primary epistemic authority independent questions. A learned release can be rebuildable yet still need durable identity because downstream products cite that release.

Evidence: `35042be0a7b289c33335ddafbe7705ee1c4f0dbc:data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C07/LEARNED_WORLD_PRODUCT_AND_SERVICE_CONSTITUTION.md`.

**Eliminated assumption:** if bytes can be regenerated, historical semantic/release identity may be erased.

## 6. Persistent cache/index is not epistemic authority

C07/C08 allow optional warm indexes/caches and determinant-scoped rebuilds. Cache deletion may change latency; it must not change meaning.

Evidence: `35042be0a7b289c33335ddafbe7705ee1c4f0dbc:data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C07/LEARNED_WORLD_PRODUCT_AND_SERVICE_CONSTITUTION.md`, `b433435bfc9ca0c7a7ba9ec349faec069479656c:data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C08/C08_RESULT.json`.

**Eliminated assumption:** operational persistence automatically becomes semantic authority.

## 7. Source bytes are necessary but not semantically sufficient

Chetiri source-backed law preserves manually/governedly established semantic/topology/routing/design bindings separately from reconstructible raw payload.

Evidence: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/31_PREV3_ARCHITECTURE_GENEALOGY_R1_HQ_JOIN_AND_DISCRIMINATOR_AUTHORITY.md`, `bcb12368e3b7f443bc4bea9402ba4f89f74104c0:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PREV3_ARCHITECTURE_GENEALOGY_R1/CHETIRI_D15_CHALLENGE/PERSISTENCE_NECESSITY_EVIDENCE_LEDGER.csv`, `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/authority/semantic_relation_dag_recovery/R1_20260825/03_DVA_TRII_CHETIRI_CONSUMER_GUIDE.md`.

**Eliminated assumption:** a virtual/source-backed route may infer all required meaning again from source labels/layout/frequencies.

## 8. Mixed-producer publication does not require filler transformations

The accepted Dva/HQ law permits publication of V553–V556 objects directly under exact identity and permission. No V556 filler object is required merely to preserve serial adjacency.

Evidence: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/31_PREV3_ARCHITECTURE_GENEALOGY_R1_HQ_JOIN_AND_DISCRIMINATOR_AUTHORITY.md`, `b06184f6535dff856914790e8f88855421708677:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PREV3_ARCHITECTURE_GENEALOGY_R1/DVA_INHERITANCE/RESULT.md`.

**Eliminated assumption:** every path must instantiate every stage before terminal publication.

## 9. Runtime consumers are stage-blind

The runtime-prior design requires V3 to consume a stable `StructuralPriorRepository` / `ResolvedStructuralContext`, not private `load_v552/load_v553/... ` calls. Denormalization may exist for efficiency but must retain exact producer refs.

Evidence: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/synthesis/RUNTIME_PRIOR_RESOLUTION_EXPLORATION.md`.

**Eliminated assumption:** downstream consumers should know historical compiler stage topology.

## 10. PRE-V3 is not a person generator

D15 and Dva closure preserve:

`POPULATION FACT != POSITIONED-SUBJECT POSSIBILITY != V3 REALIZED LIFE`.

Evidence: `4450c54930533527b7bbb7ceb73a6a46b6ac9eba:data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D15/RESULT.md`, `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`.

**Eliminated assumption:** because evidence is useful to eventual person generation, PRE-V3 may precompute actor belief/disposition/history.

## 11. Carrier choice does not authorize source retirement

D15 and the HQ genealogy keep source retirement behind a separate equivalence/replay governance gate.

Evidence: `4450c54930533527b7bbb7ceb73a6a46b6ac9eba:data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D15/RESULT.md`, `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/31_PREV3_ARCHITECTURE_GENEALOGY_R1_HQ_JOIN_AND_DISCRIMINATOR_AUTHORITY.md`.

**Eliminated assumption:** a successful transformed carrier, virtual route or benchmark automatically earns source-deletion/storage-retirement credit.
