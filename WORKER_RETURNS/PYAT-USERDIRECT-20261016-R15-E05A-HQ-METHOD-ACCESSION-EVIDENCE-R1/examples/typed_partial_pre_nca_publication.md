# Sourcefree selected-world handoff

SOURCEFREE_OFF_NOT_INSTALLED · TYPED_PARTIAL_SELECTED_WORLD

Selection: AS_OF; valid 2022-06-01; known by 2022-06-01.

| Structural key | Actual value/state | Native unit |
|---|---|---|
| training_access | UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK | typed unavailable |
| training_fee | UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK | typed unavailable |
| exit_cost | UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK | typed unavailable |
| civil_open | UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK | typed unavailable |
| civil_sanction | UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK | typed unavailable |

| Empirical query | Native cells/support | State |
|---|---|---|

| Native field | Actual values | Native unit / geography |
|---|---|---|
| GSS_RURAL_LIGHTING | {"denominator": 3288063, "electricity_subtypes": {"community_grid": 74490, "generator": 3640, "mains": 2288193, "solar_inverter": 21512, "wind": 357}, "numerator": 2388192, "published_percent": 72.6} | RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING / GHANA_RURAL |
| NCA_NATIONAL_MOBILE_DATA | NOT_PUBLISHED_AT_SELECTED_ASOF | Typed missing arm |

NONPARENT_OPTIONS: PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT
{"civil": {"dependencies": ["civil_open", "civil_sanction"], "state": "UNAVAILABLE_AUTHORITY_OR_CLOCK", "value_refs": [null, null]}, "exit_constraint": {"dependencies": ["exit_cost"], "state": "UNAVAILABLE_AUTHORITY_OR_CLOCK", "value_refs": [null]}, "training": {"dependencies": ["training_access", "training_fee"], "state": "UNAVAILABLE_AUTHORITY_OR_CLOCK", "value_refs": [null, null]}}

CONCEPTION_SCENARIO_PROPOSALS: PARTIAL_PROPOSALS_EVALUATED
[{"feasibility": "UNKNOWN_PREMISE", "route": "institutional", "scenario_id": "HANDOFF_INSTITUTIONAL", "selection_weight": null}, {"feasibility": "UNKNOWN_PREMISE", "route": "civil", "scenario_id": "HANDOFF_CIVIL", "selection_weight": null}]

Request hash: c800fd715f4c35ad4a0962d50dab236c6ddfb9f7ab412640ab8b90f47423c56a
Receipt hash: b53ba096872d81347d9b3e3187436dc5523d86184e9b332cf18ea6640d6b2d8c

No HQ adoption, operative OC05/N9/N10W, real source issuance or person/V3 output.
