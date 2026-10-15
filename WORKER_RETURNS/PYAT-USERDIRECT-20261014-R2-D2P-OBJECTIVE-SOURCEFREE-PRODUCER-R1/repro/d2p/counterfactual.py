"""D2P no-actor 2021 Ghana person-context counterfactual (executable, sourcefree).

Shows, with executable checks on the fixture aggregates, why two published
aggregate fields cannot determine any particular person's electricity/internet
exposure or psyche:

1. The GSS value is a rural dwelling-unit main-lighting share (72.6% of
   3,288,063 occupied rural dwelling units), not a person attribute. A person
   in a lit rural household may be absent, and a person in an unlit household
   may spend days in lit places. The aggregate carries no person-level joint.
2. The NCA value is national active mobile-data SUBSCRIPTIONS (23,414,527 =
   prepaid + postpaid), explicitly not unique persons, households, rural use,
   or ownership. One person may hold many subscriptions; many persons hold none.
3. The two fields have different statistical units, geographies, observation
   windows and denominators (rural dwelling units vs national subscriptions).
   No same-population joint exists, so no pooled individual inference is
   licensed. The reader's NONPOOLED_CONTEXTUAL_CO_PRESENCE_ONLY relation is the
   only lawful coexistence, and it is test-only/unissued.
4. Publication timing: a 2021 person cannot know 2022-02-24 (GSS) or
   2022-07-08 (NCA) publications. A historical counterfactual conditioning a
   2021 life on these fields as known-in-2021 is refused by the reader.

Executable form: each numbered claim is a check against the two field records;
a `counterfactual_request(person_exposure=True)` or `pooling=True` through the
reader must be refused.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


def counterfactual_holds(fields: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Verify the four structural facts that block person-level inference."""
    gss = fields["GSS_RURAL_LIGHTING"]["underlying_row"]
    nca = fields["NCA_NATIONAL_MOBILE_DATA"]["underlying_row"]
    checks: dict[str, Any] = {}

    checks["gss_unit_is_dwelling_not_person"] = (
        gss["native_unit"] == "RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING"
        and "PERSON" not in gss["native_unit"]
    )
    checks["gss_excludes_vacant_and_secondary"] = (
        sorted(gss["exclusions"]) == ["SECONDARY_HOUSING", "VACANT_DWELLINGS"]
    )
    checks["gss_subtypes_are_dwelling_lighting"] = (
        set(gss["values"]["electricity_subtypes"])
        == {"mains", "community_grid", "generator", "solar_inverter", "wind"}
    )

    checks["nca_unit_is_subscriptions_not_persons"] = (
        nca["native_unit"] == "ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS"
    )
    checks["nca_no_unique_persons"] = nca.get("unique_persons") is False
    checks["nca_no_rural_split"] = nca.get("rural_split") is None
    checks["nca_prepaid_postpaid_sum"] = (
        nca["values"]["prepaid"] + nca["values"]["postpaid"]
        == nca["values"]["active_subscriptions"]
    )

    checks["units_geographies_denominators_distinct"] = (
        gss["native_unit"] != nca["native_unit"]
        and gss["native_geography"] != nca["native_geography"]
        and gss["values"]["denominator"] != nca["values"]["active_subscriptions"]
    )
    checks["publications_postdate_2021"] = (
        gss["publication_date"] > "2021-12-31"
        and nca["publication_date"] > "2021-12-31"
    )
    checks["all_hold"] = all(checks.values())
    checks["conclusion"] = (
        "Two aggregates do not determine any 2021 person's electricity/internet "
        "exposure or psyche. A world-conditioned context may reference them; "
        "no person attribute is licensed."
        if checks["all_hold"]
        else "COUNTERFACTUAL_STRUCTURE_BROKEN"
    )
    return checks


def mutation_values(field_row: Mapping[str, Any], role: str) -> dict[str, Any]:
    """Return the numeric values a person-level reading would need but cannot get."""
    return {
        "role": role,
        "has_person_joint": False,
        "has_person_exposure": False,
        "person_level_values_available": [],
        "aggregate_values": deepcopy(field_row["values"]),
    }
