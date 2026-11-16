# Astra PRE-V3 First-Wave Branch Registry R1

Status: `C01_C08_COMMISSION_BRANCHES_MINTED`

Audit packet banked by PR #357 merge: `ba8fe3b05489c951994024a502b5c3280627acbb`

HQ audit-evidence acceptance and release commit: `2a88795031d80cb5bc49979c34ace0dd2427ca6e`

All worker branches descend from the HQ release commit and contain the banked audit packet plus one committed bounded HQ commission. C01 is not a global predecessor barrier for C02–C08.

| ID | Lane | Branch | Commission tip | Exact grain |
|---|---|---|---|---|
| C01 | HQ direct | `agent/rabochii-astra-c01-prev3-completion-r1` | `0b8739527f35b2d23a0c45d4895a90e25ac50632` | `PREV3_COMPLETION_SCOPE_AND_OBLIGATION_RECONCILIATION_R1_ONLY` |
| C02 | Sub-Vozhd II | `agent/rabochii-astra-c02-world-release-valid-time-r1` | `7689d794ad09975a0313fa95c74ff82d85e63dc2` | `PREV3_OBJECTIVE_WORLD_RELEASE_AND_VALID_TIME_BOOTSTRAP_R1_ONLY` |
| C03 | Sub-Vozhd I | `agent/rabochii-astra-c03-learned-world-positive-workload-r1` | `153cb7efb3397327f746d29bf8617dc4481f8e4c` | `PREV3_SOURCE_AND_LEARNED_WORLD_POSITIVE_WORKLOAD_R1_ONLY` |
| C04 | Sub-Vozhd I | `agent/rabochii-astra-c04-field-forge-structural-coverage-r1` | `34ac12b7800a013eab7956fcf186e68d9449cd54` | `PREV3_FIELD_FORGE_STRUCTURAL_PRODUCTION_COVERAGE_R1_ONLY` |
| C05 | Sub-Vozhd II | `agent/rabochii-astra-c05-sdtf-objective-r1` | `8688f8886601cb18ca34cc0150d055f036ed4836` | `SDTF_OBJECTIVE_RULE_BODY_AND_WORLD_POPULATION_R1_ONLY` |
| C06 | Sub-Vozhd III | `agent/rabochii-astra-c06-non-event-serving-v3-ingress-r1` | `f167a696984647979e5438083a3d09cf871c00be` | `PREV3_OBJECTIVE_NON_EVENT_SERVING_AND_V3_INGRESS_R1_ONLY` |
| C07 | Sub-Vozhd III | `agent/rabochii-astra-c07-producer-firewall-contract-drift-r1` | `eafced006fbad2ddb92c83e27bd7713f9fbac028` | `PREV3_PRODUCER_RESULT_FIREWALL_AND_CONTRACT_DRIFT_REPAIR_COURT_R1_ONLY` |
| C08 | Sub-Vozhd III | `agent/rabochii-astra-c08-objective-consumer-bounded-policy-r1` | `61c891a088759e859f04699aa467487440fd6808` | `PREV3_OBJECTIVE_CONSUMER_BOUNDED_EVIDENCE_POLICY_R1_ONLY` |

Each worker must execute the committed `00_COMMISSION.md` under its `WORKER_COMMISSIONS/ASTRA-C0X/` directory and the bound detailed packet card. Do not replace or rebase the branch.

All sibling returns remain candidate evidence until frozen by the competent lane integrator or HQ for a named successor. Waiting implementation successors remain uncommissioned.

Terminal: `ASTRA_PREV3_FIRST_WAVE_C01_C08__BRANCHES_MINTED__PARALLEL_RELEASE_ACTIVE`
