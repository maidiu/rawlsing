# PYAT H02 — F1 owner / first-consumer crosswalk

Observed FINDING: two different F1 uses coexist. The analytical answer-distribution obligation is represented by the N10E/C1/I03 path and is executable on synthetic AT07 data, but no retained GT2 binding to its positioned-subject consumer was found. The retained GT2 empirical joint product is already consumed end-to-end by the Field Forge → PRE-V3 → V554/V557/V558 structural lane, which HQ222 independently accepted. Causal INTERPRETATION: the real retained first-consumer connection exists at the structural grain; the general analytical F1 retained-input connection is the remaining function-card item. Proposed HQ ACTION: accept the retained structural positive at its declared grain and decide whether the analytical lane is a separate required build. Accountable OWNER: Pyat HQ with the original C11/I03, Field Forge and V554/V557/V558 owners; no self-adoption here.

## 1. Analytical F1 obligation (HQD-125)

HQD-125 assigns exact answer distributions to EE01–EE04, selected Route B and I03. It grades them “represented and substantially implemented”, with “35-wave qualified occupancy at declared scope” still required. That is not `CURRENT_COMPOSED_REALIZATION`, `LIVE_35_WAVE_OCCUPANCY` or terminal PRE-V3 completion.

Current carrier code at base `299f41e`:

| Symbol / module | Git blob | Grade |
|---|---|---|
| `pre553_c11_repository.py` | `67c6eb6494522cd11aab1b93d0e73f9cef6036f3` | current receiving-control C11 repository |
| `pre553_empirical_query.py` | `03facecf70890bfd13b80418620d274cbcd69d02` | current I03 query execution |
| `pre553_discovery_exact.py` | `905f24d114419dbdd93879ad2bee5b59dd2f23af` | current bounded discovery |
| `pre553_source_backed_c11_facade.py` | `8a761119e4a8d68eb291fc4edfadb52e027f8284` | current source-backed release facade |
| `wave1_gt12_i03_positive_facts.py` / `execute_gt12b_i03_plan` | `067628dc6605f28be68bdcd86ef57b02a0db4348` | GT1/GT2 I03 producer; synthetic fixture tests |
| `wave1_gt12_a2_real_gt1.py` / `execute_and_replay_a2_gt1` | `595610fd3a0c453d8a4528f52fdd9be458db5e9c` | A2 GT1 composition; one pre-existing RED |
| `pre553_analytical_composition.py` / `compose_positioned_subject_possibility` | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` | accepted analytical composition seam |
| `pre553_empirical_possibility_provider.py` / `provide_empirical_possibility_slice` | `23167aa25291fb148b1e3cf210ac33fe7769b783` | accepted N10E provider seam |
| `source_backed_positioned_subject_possibility.py` / `evaluate_positioned_subject_possibility` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` | accepted positioned-subject consumer |

`provide_empirical_possibility_slice` accepts exact determinants, calls the analytical composition owner, generates `PossibilitySliceEvidence`, and runs `evaluate_positioned_subject_possibility`. Its public API forbids caller-supplied geometry. It is `REUSE_ALREADY_EXECUTABLE` at the synthetic AT07 grain.

Local execution: `test_pre553_empirical_possibility_provider.py` passed 43/43. The oracle is a 100-row synthetic law: forward 54 yes/60 → 9/10; reverse 54 P1/62 → 27/31; source, release, target-topology, denominator, zero/minority and replay negatives pass. This proves the general analytical machinery, not a retained GT2 first consumption.

The I03/A2 supporting subset passed 22/23. `test_wave1_gt12_a2_real_gt1.py::test_a2_claim_scoped_authorities_bind_actual_release_universe_and_replay` is a pre-existing RED at untouched `299f41e`: `GT12BI03BindingError: validated projection domain omits an observed exact source-native response state`. It is an analytical-fixture route, not the retained GT2 consumer; no repair was attempted because it is outside the reused positive and the one-repair budget was not needed.

## 2. V554 structural F1 (retained GT2 lane)

The separate structural `F1` is not the analytical answer-distribution owner. HQ222 accepted this bounded chain: retained Afrobarometer R5 GT2 Q86B→Q86A joint product (19,210 support, 36 cells) → Field Forge exact conditional-support profile → PRE-V3 relation admission for `STRUCTURAL_MEDIATION_INPUT` → SIG-004 V554 F1 → current V557/V558 `CONTEXT` publication. The independent review is `WORKER_RETURNS/PYAT-HQ222-C5-GT2-STRUCTURAL-POSITIVE-REALIZATION-REVIEW-R1/00_REVIEW.md`, blob `8b51f0c0ff21994a893744e8809744c7ca49d441`.

Current carriers:

| Symbol / module | Git blob | Role |
|---|---|---|
| `pre553_repo_native_current_payload.py` / `load_current_gt2_query_fact_from_committed_transport` | `b850e7794f387000afe4a6dfd49ca5092426f895` | real retained query/fact loader; no path argument |
| `field_forge_conditional_support.py` / `produce_exact_conditional_support_profile` | `a70decb20747d84cbcbe27d1280babc6de88ef33` | retained-fact consumer and distribution producer |
| `wave1_ff_prev3_relation_admission.py` | `c5fb675fd6f95cb7dc9e0ad505224803839cc645` | PRE-V3 admission owner |
| `gt12_c_to_d_relation_bridge.py` | `ea04ec079e8d60e6e5c7236ec5b54898876be4b3` | C→D bridge |
| `gt12_d_to_m4_typed_bridge.py` | `ca3d6b8d832d7ca8d959bd19e19a23b08cabde76` | D→M4 typed bridge |
| `m1_admitted_field_forge_relation_v554_ingress.py` | `0aeacd9e66c7e4340b36e1b622bb5c9bf2865fd5` | relation-specific M1/V554 ingress |
| `m4_v557_v558_publication_repository.py` | `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360` | V557/V558 current consumer repository |
| `v3_psepf_zero_positive_guard.py` | `e0528d65215cb431196570c38bac4eae94217a1b` | V3 zero-effect guard |
| `gt12_e2b_publication_governance_binding.py` | `5c0e730972ca7f31c3be92564c299822c431ccc5` | adopted current binding |
| `gt12_c_to_d_relation_bridge.admit_gt12_c_relation` | — | exact admission callable |
| `gt12_e2b_actual_object_consumer_harness.run_current_r1c_e2b_actual_objects` | — | downstream consumer callable |

Local execution: HQ222 court passed 40/40, including complete 36-cell geometry, 19,210 conservation, minority/zero preservation, wrong order, altered risk/source identity, incomplete joint domain, permission widening, actor injection and V555 refusal. The V554 F1 is `urn:rawlsing:v554:f1:sha256:3530f08f...`; B1 says V555 use allowed, but M2 refuses the relation basis because its contract is the empirical M1 contract and ADP-002 excludes SIG-004. That is an authority/contract gap, not a negative structural finding.

## 3. Historical candidate

`data/ddm_build_copy/ddm_v550_position_distribution.py`, blob `651329254244e9f42a8d88c2721ccae6bd768073`, computes historical respondent-position distributions. It is `HISTORICAL_CANDIDATE_ONLY`: no current semantic authority, functional equivalence or first consumer is established. It was not executed or adopted.

## 4. Exact missing connection

- Analytical lane: `RECOVER_AND_WIRE_EXISTING` is technically plausible, but no lawful retained GT2 query/model/witness binding to `provide_empirical_possibility_slice` exists. The N10E path is proved only on its synthetic AT07 fixture and its consumer is the synthetic positioned-subject query. The missing piece is an owner-qualified empirical-to-analytical consumer binding, not a new ontology.
- Structural lane: `REUSE_ALREADY_EXECUTABLE`; the retained GT2 product already reaches the current V554/V558 consumer. This is the real retained-object positive returned here.
- No claim is made that the V554 structural F1 is the general analytical F1 owner. The distinction is the central crosswalk result.

DONE: exact code/consumer mapping, retained positive, synthetic analytical proof, historical candidate boundary. REMAINING: HQ decision whether the analytical lane is required now and, if so, the exact model-rule/consumer-query authority. CRITICAL BLOCKERS: analytical retained binding and V555 relation authority. LARGEST PRODUCTIVE MOVE: owner supplies the GT2 analytical query/model binding or confirms the structural V554 lane is the intended first consumer. FLIGHT: local Git/Python only; no raw source or branch mutation outside this return branch. DELTA: the retained first-consumer positive is recovered and distinguished from the still-unwired analytical F1 lane.
