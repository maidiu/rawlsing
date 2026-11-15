# G3 — Concrete bounded-nine respondent-joint family: JCFG-GSS-ABORTION-CONDITIONS

## 1. Concrete family identity (not a generic field tuple)

**Family:** `gss_abortion_condition_family`
**Bounded joint configuration:** `JCFG-GSS-ABORTION-CONDITIONS`
**Source / wave / country:** `GSS` / `2010` / `US`
**Adjudication:** `V550JADJ-0005`
**Decision:** `ACCEPTED_EXISTING_GSS_EXECUTABLE_CONTROL`
**Authority release:** `V550J-BOUNDED-AUTHORITY-2026-08-02-R1`
**Item count / minimum answered:** 6 / 3
**Signed boundary authority:** true
**P3 bound item count / source-local-only item count:** 0 / 6
**Authority ceiling:** `GOVERNED_BOUNDED_CANARY_ONLY`; `NO_PRODUCTION_COMPLETENESS_CLAIM`

**Ordered items (from `bounded_joint_configuration_item_crosswalk.csv` rows 12-17):**

| order | var_code | question_implementation_id | p2_lineage_id | condition_label |
|---:|---|---|---|---|
| 1 | `abdefect` | `question_impl.phase0.8da159b3ddb964ba6920` | `p2lineage_639a0997464b39d19a7eb44f` | fetal_defect |
| 2 | `abhlth` | `question_impl.phase0.dc8a1f84391d374d3994` | `p2lineage_6eb15213aa7dc0324c5767d8` | woman_health |
| 3 | `abrape` | `question_impl.phase0.6bd976214617dc817176` | `p2lineage_7327e9857bf33d69a3737e87` | rape |
| 4 | `abany` | `question_impl.phase0.1569f26ce284ee346a1c` | `p2lineage_ad9d097fefd6086c987c98fa` | any_reason |
| 5 | `absingle` | `question_impl.phase0.bbbde435f9f054f959b6` | `p2lineage_88c9ec1cabb9e2b4cf482110` | unmarried |
| 6 | `abnomore` | `question_impl.phase0.7555028a2eafddb1c875` | `p2lineage_5664ff0044b0691645d96b3b` | no_more_children |

All six share `response_families=["binary_contrast"]`, `response_values=["", "1", "2"]`, labeled `yes=1`/`no=2`, `directional_certification_statuses=["CERTIFIED"]`, `response_semantics_statuses=["manual_authority_all_eight"]`, and response-semantics contract hash `9573e1f8fb4e0b7126fa44c74892a2acb70db046e5d2e110079a30fe15730821`.

The registry's `item_role_groups` also lists `abpoor`; the bounded authority row explicitly narrows to the six exact variables present in the 2010 fixture, so `abpoor` is outside this selected bounded configuration.

**Metadata evidence**

- `data/ddm_build_copy/manifests/question_family_registry.yaml:7-85`, blob `54eb6dd138b5e30305b0308fcdb8f078994b1c40` (family id, eligible waves, item roles, response-role rules).
- `section85/authority/bounded_joint_configuration_authority.csv:6`, blob `92d5f21a8f3d11314b665449ebb84a48fc7eb718` (JCFG row, GSS/2010/US, six items, authority ceiling).
- `section85/authority/bounded_joint_configuration_item_crosswalk.csv:12-17`, blob `ab7fc8f8b01b4f41bffd4d30df4990d923f8df61` (ordered item identities and response semantics).
- `section85/CURRENT_STATE.json:2,27`, blob `4439d305667a19917ad0ff2b79cf0dd5035fe610` (`archive_contains_respondent_level_substrate=false`; `real_empirical_j_chain_status=NOT_RUN_REQUIRES_LIVE_RESPONDENT_DATABASE_AND_PYARROW`).

## 2. Historical execution status — HELD

`HISTORICAL_EXECUTED = NO`.

Prior C4R1 records `POSITIVE_LOAD_PROVED=NO`, `0/9` bounded source-family/wave scopes, and no respondent-level substrate (`.../G1A_C4R1_V550J_V551J_V552J_INFORMATION_CONSERVATION_RETURN.md`, blob `efe49ce5b9b93d19a49e321a44e8148987fad67b`, §5). `section85/CURRENT_STATE.json` independently records the real J chain as `NOT_RUN_REQUIRES_LIVE_RESPONDENT_DATABASE_AND_PYARROW` and the archive as lacking respondent-level substrate.

No raw SAV/respondent read, synthetic execution, invented pattern id, or fake output row was used. The family trace below is therefore a **source-executable expected path with exact missing artifacts**, not a historical execution claim.

## 3. Actual input graph — diamond, not a serial chain

```
(V550 ordinary distributions: answer_distribution / country_answer_distribution)
        |
        v
  V551 direct atoms (signed direction/intensity, counts)
        |                                   \
        |                                    v
        |                             V552 structural pressure facts
        |                                    |
(V550J prepared same-person patterns)       |
        |                                   |
        +---------> V551J component match <--+
                         |
                         v
                 V551J certified/review packets
                         |
                         +---------> V552J exact-scope join <---- V552 facts/keys
                                                |
                                                v
                                      V553 canonical/probe consumer
```

There is **no V550J → V551 atom edge** and **no V551J → V552 fact edge**. V551 atoms come from ordinary V550 direct distributions; V550J patterns and V551 atoms converge at V551J; V551 atoms also feed V552 facts; V551J packets and V552 facts converge at V552J.

## 4. Concrete family trace through all stages

Expected paths below substitute the selected scope `GSS` / `2010` / `US`; `<run_id>` and `<shard_id>` are exact producer run identities that do not exist in the inspected repository.

| Stage | Expected producer/path or authority | Exact status for this family | Missing link / observed evidence |
|---|---|---|---|
| 0. Registry/crosswalk | `question_family_registry.yaml`; `bounded_joint_configuration_authority.csv`; `bounded_joint_configuration_item_crosswalk.csv` | PRESENT | Family/authority metadata present; no run row. |
| 1. V550J prepared substrate | `data/ddm_repository_copy/v550j/cache/prepared_response_substrate/source=GSS/wave=2010/country_code=US/v550j_prepared_response_substrate.parquet` + `..._manifest.json` | MISSING | No prepared parquet/manifest for GSS/2010/US in inspected tree; `prepared_required` would fail closed (`build_v550j_prepared_substrate.py:373-374`). |
| 2. V550J run: pattern, item, relation, membership | `data/ddm_repository_copy/v550j/runs/<run_id>/<shard_id>/joint_patterns/v550j_manifest.json`, `joint_response_pattern_index.parquet`, `joint_response_pattern_item_index.parquet`, `joint_pattern_relation_signature.parquet`, `joint_pattern_respondent_membership.parquet`; expected shard id `GSS__2010` | MISSING | No V550J run/manifest or pattern_id/row for this family. Writer paths: `compile_v550j_joint_response_patterns.py:2051,2218`; membership build/emit: `ddm_v550j_joint_patterns.py:3514-3550,5280`; shard id construction from source__wave. |
| 3. V551 direct atoms | `data/ddm_repository_copy/v551/runs/<run_id>/relation_evidence_atoms.parquet` + `manifest.json` | MISSING | No V551 run/manifest or atom rows. V551 atoms derive from ordinary V550 direct distributions, not from V550J (`ddm_v551_atoms.py:21,123,141-158`). |
| 4. V551J candidate/certified/review packets | `data/ddm_repository_copy/v551j/runs/<run_id>/packets/v551j_joint_packet_candidate_index.parquet`, `v551j_certified_joint_packet_index.parquet`, `v551j_review_surface.parquet`; `manifest/manifest.json` | MISSING | No V551J run/packet. Exact match requires source_family=`GSS`, canonical_wave=`2010`, country_code=`US`, then item question_id/var_code/response; no rows exist (`ddm_v551j_packets.py:1114-1160`; writer `compile_v551j_joint_evidence_packets.py:1591-1597`). |
| 5. V552 structural facts | `data/ddm_repository_copy/v552/runs/<run_id>/structural/v552_structural_fact_index.parquet`, `structural/v552_temporal_key_source_index.parquet` + `manifest.json` | MISSING | No V552 run/manifest or fact/row. Facts derive from V551 atoms, not from V551J (`ddm_v552_structural.py:100-199`; writer subdir `compile_v552_structural_ddm.py:241-246,340-350`). |
| 6. V552J join | `data/ddm_repository_copy/v552j/runs/<run_id>/manifest.json`, `packets/v552j_structural_join_index.parquet`, `audits/v552j_join_audit.parquet`, `packets/v552j_v553_input_index.parquet`, `packets/v552j_to_v553_handoff_index.parquet` | MISSING | No V552J run/manifest/join. Exact scope and semantic match cannot be evaluated without the V551J packet and V552 fact rows (`ddm_v552j_handoff.py:79-142`). |
| 7. V553 canonical/probe output | Caller-supplied `--output-root`; no repository default V553 run root | MISSING | No V553 run/manifest/output or probe row. Canonical adapter requires the V552J manifest/join/audit/input/handoff (`ddm_v553_canonical_harmonization.py:47-51,86-88,414-545`). |

## 5. Exact-respondent membership loss (distinct from aggregate pattern/item membership)

V550J persists `joint_pattern_respondent_membership` with `respondent_id`, `respondent_id_norm`, `pattern_weight_value`, `answered_item_count`, `pattern_id`, `family_id`, source/wave/country and related pattern metadata (`ddm_v550j_joint_patterns.py:3514-3550`; emitted at `:5280`). The V551J compiler has no membership path in its required inputs (`compile_v551j_joint_evidence_packets.py:1140-1210`). D11 records the exact-respondent grain as `STRANDED` after V550J: aggregate joint-pattern semantics survive; exact respondent identity does not (`.../06a46105705d__RESULT.md:153-172`, blob `06a46105705d8beb159b16336eb671ee0381e726`).

Therefore this path's V551J/V552J/V553 rows can preserve pattern/item/component membership but **cannot** be used to re-identify the same respondents or reconstruct respondent-level joints from the downstream carrier.

## 6. Numerical semantics and qualifications (source-executable)

- **V550J pattern:** same-person pattern counts (`pattern_count_unweighted`, `pattern_count_weighted`), probabilities, support status/gate/score, and multiple denominators. The association field named `mutual_information` is a scaled pointwise log-ratio (`log2(p_pattern/p_baseline) * pattern_count_unweighted/family_count`), not joint MI. Denominators are non-collapsible.
- **V551 atom:** direct-lane promotion only for `answer_distribution`/`country_answer_distribution`; signed direction/intensity plus `n_unweighted`, `n_weighted`, `pct_*`, semantics/authority hashes. Derived determinicity is excluded from atoms.
- **V551J packet:** exact scope + question/var + response matching; at least two matched relation components; all authority/direction/target/structural gates; packet measurements from V550J pattern, not from V551 atom counts. It does not reconstruct `P(response | A AND B)`.
- **V552 fact:** requires one unique positive `n_respondents`; `pressure_score = Σ(normalized_weight × canonical_signed_component)` in [-1,1]; `OBSERVED_ZERO`/`OBSERVED_NONZERO`; heterogeneous/absent denominator is `APPLICABLE_BUT_UNRESOLVED`, not renormalized.
- **V552J:** exact scope + semantic score (relation 4, target 3, driver facet 3, question 2); `ALLOW` only for certified + both producer permissions ALLOW + fact permission ALLOW + observed pressure; temporal field always false.
- **V553:** canonical manifest/join/audit/input/handoff checks; probe-only key when `temporal_field_allowed=False`; single-wave `ready_for_v553_probe` is not temporal-field authority.

## 7. Source-executable vs historical-executed

`SOURCE_EXECUTABLE = YES` for the expected family path and code-level producers/consumers above.
`HISTORICAL_EXECUTED = NO`; exact output rows, pattern ids, packet ids, join ids and V553 ids remain `HELD_EXACT_EVIDENCE`.

No claim of historical numerical transformation, positive load, or functional conservation is made.
