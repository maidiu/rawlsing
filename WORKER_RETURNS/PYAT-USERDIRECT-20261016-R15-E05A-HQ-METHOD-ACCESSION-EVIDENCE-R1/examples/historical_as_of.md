# Sourcefree selected-world handoff

SOURCEFREE_OFF_NOT_INSTALLED · SELECTED_WORLD_VALUES_SERVED

Selection: AS_OF; valid 2026-06-01; known by 2026-03-01.

| Structural key | Actual value/state | Native unit |
|---|---|---|
| training_access | True | modeled policy eligibility boolean |
| training_fee | 2 | modeled resource tokens |
| exit_cost | 2 | modeled resource tokens |
| civil_open | True | modeled route eligibility boolean |
| civil_sanction | False | modeled sanction boolean |

| Empirical query | Native cells/support | State |
|---|---|---|
| Y given [['A', 1]] | 0: 14/32, 1: 18/32 | EXACT_SUPPORTED |
| Y given [['A', 1], ['B', 1]] | 0: 6/16, 1: 10/16 | EXACT_SUPPORTED |
| Y given [['A', 1], ['B', 1], ['C', 1]] | 0: 2/8, 1: 6/8 | EXACT_SUPPORTED |

| Native field | Actual values | Native unit / geography |
|---|---|---|
| GSS_RURAL_LIGHTING | {"denominator": 3288063, "electricity_subtypes": {"community_grid": 74490, "generator": 3640, "mains": 2288193, "solar_inverter": 21512, "wind": 357}, "numerator": 2388192, "published_percent": 72.6} | RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING / GHANA_RURAL |
| NCA_NATIONAL_MOBILE_DATA | {"active_subscriptions": 23414527, "postpaid": 177189, "prepaid": 23237338} | ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS / GHANA_NATIONAL |

NONPARENT_OPTIONS: OPTIONS_AND_SOURCE_SUPPORT_PRODUCED
{"civil": {"dependencies": ["civil_open", "civil_sanction"], "state": "ELIGIBLE", "value_refs": [{"content_hash": "704f450297cc2d79fdb4f4998bc5336c63524350a9983d378f5f500da920e27e", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:civil_open:1"}, {"content_hash": "fc9a722d4333076c338b0ad8993bac001e97de3d49ee816edebaacd85eb5154e", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:civil_sanction:1"}]}, "exit_constraint": {"dependencies": ["exit_cost"], "state": "WITHIN_MODELED_BUDGET", "value_refs": [{"content_hash": "5281accc231a8cbedce249f25863bffeca0c4cc2a6fdd755c085b2e19092fbfd", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:exit_cost:1"}]}, "training": {"dependencies": ["training_access", "training_fee"], "state": "ELIGIBLE", "value_refs": [{"content_hash": "3b4b4859dcbe858480d097147c719ce9458d4e1d88b4f47898a0416fe01e7174", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:training_access:1"}, {"content_hash": "7b81073f295d8eafe81abb7aaaac58251cd172d109325d87e2deb2f0b9b6f166", "kind": "E04_TEST_ONLY_FIELD", "object_id": "urn:test:e04:field:training_fee:1"}]}}

CONCEPTION_SCENARIO_PROPOSALS: FINITE_PROPOSALS_EVALUATED
[{"feasibility": "FEASIBLE_MODELED_PREMISE", "route": "institutional", "scenario_id": "HANDOFF_INSTITUTIONAL", "selection_weight": null}, {"feasibility": "FEASIBLE_MODELED_PREMISE", "route": "civil", "scenario_id": "HANDOFF_CIVIL", "selection_weight": null}]

Request hash: e335add7b07eff21541ef81875f768e983a0a9f20142d84e5c1c4dbabafbe344
Receipt hash: 62c98f42ef4a99830e64626d7069912d1d1800c88d9435979776aaaf277d9eaa

No HQ adoption, operative OC05/N9/N10W, real source issuance or person/V3 output.
