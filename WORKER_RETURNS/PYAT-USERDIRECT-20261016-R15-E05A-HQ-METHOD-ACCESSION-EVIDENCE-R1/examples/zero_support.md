# Sourcefree selected-world handoff

SOURCEFREE_OFF_NOT_INSTALLED · TYPED_PARTIAL_SELECTED_WORLD

Selection: TEST_CURRENT; valid 2027-09-01; known by 2027-09-01.

| Structural key | Actual value/state | Native unit |
|---|---|---|
| training_access | False | modeled policy eligibility boolean |
| training_fee | 2 | modeled resource tokens |
| exit_cost | 8 | modeled resource tokens |
| civil_open | True | modeled route eligibility boolean |
| civil_sanction | False | modeled sanction boolean |

| Empirical query | Native cells/support | State |
|---|---|---|
| Y given [['A', 1]] | 0: 12/24, 1: 12/24 | EXACT_SUPPORTED |
| Y given [['A', 1], ['B', 1]] | 0: 4/8, 1: 4/8 | EXACT_SUPPORTED |
| Y given [['A', 1], ['B', 1], ['C', 1]] | No numeric cells | ZERO_SUPPORT |

| Native field | Actual values | Native unit / geography |
|---|---|---|
| GSS_RURAL_LIGHTING | {"denominator": 3288063, "electricity_subtypes": {"community_grid": 74490, "generator": 3640, "mains": 2288193, "solar_inverter": 21512, "wind": 357}, "numerator": 2388192, "published_percent": 72.6} | RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING / GHANA_RURAL |
| NCA_NATIONAL_MOBILE_DATA | {"active_subscriptions": 23414527, "postpaid": 177189, "prepaid": 23237338} | ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS / GHANA_NATIONAL |

NONPARENT_OPTIONS: PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT
{"civil": {"dependencies": ["civil_open", "civil_sanction"], "state": "ELIGIBLE", "value_refs": [{"content_hash": "704f450297cc2d79fdb4f4998bc5336c63524350a9983d378f5f500da920e27e", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:civil_open:1"}, {"content_hash": "fc9a722d4333076c338b0ad8993bac001e97de3d49ee816edebaacd85eb5154e", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:civil_sanction:1"}]}, "exit_constraint": {"dependencies": ["exit_cost"], "state": "RESOURCE_CONSTRAINED", "value_refs": [{"content_hash": "4e69e0588de3faefae9511aa75c59f342a08694f42f67d4457063d99d1470b69", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:exit_cost:2"}]}, "training": {"dependencies": ["training_access", "training_fee"], "state": "BLOCKED_BY_MODELED_RULE", "value_refs": [{"content_hash": "cd91e67dda69e7d93128ba9e41306f3a0321290b849aa8628db0dc02daf246bb", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:training_access:2"}, {"content_hash": "7b81073f295d8eafe81abb7aaaac58251cd172d109325d87e2deb2f0b9b6f166", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:training_fee:1"}]}}

CONCEPTION_SCENARIO_PROPOSALS: PARTIAL_PROPOSALS_EVALUATED
[{"feasibility": "INFEASIBLE_MODELED_PREMISE", "route": "institutional", "scenario_id": "HANDOFF_INSTITUTIONAL", "selection_weight": null}, {"feasibility": "FEASIBLE_MODELED_PREMISE", "route": "civil", "scenario_id": "HANDOFF_CIVIL", "selection_weight": null}]

Request hash: 313225ea83f1f77f78f35f6f1934d337fadafd3b9cb272fcc64542efe1bbc220
Receipt hash: ea09380936f7331b185841f1c3932d9e985e875351514255cb25e2ba2515159c

No HQ adoption, operative OC05/N9/N10W, real source issuance or person/V3 output.
