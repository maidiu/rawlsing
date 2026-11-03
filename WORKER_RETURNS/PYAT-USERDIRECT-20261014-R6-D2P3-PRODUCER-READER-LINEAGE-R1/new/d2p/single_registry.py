"""D2P3 one owner-produced sourcefree field registry and exact-ref reader.

The producer builds immutable ExternalPublishedAggregateField records once and
registers them in one ProducerRegistry. The reader accepts only those exact
D2P_TESTONLY_FIELD refs; it does not reconstruct a parallel row registry.
Everything remains TEST_ONLY: no original PDF bytes/rights, no N5/N6/EE13,
no N9/OC05, no person-level or pooled/causal inference.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

SCHEMA = "D2P3_EXTERNAL_PUBLISHED_AGGREGATE_FIELD@1"
REGISTRY_SCHEMA = "D2P3_ONE_PRODUCER_REGISTRY@1"
GSS = "GSS_RURAL_LIGHTING"
NCA = "NCA_NATIONAL_MOBILE_DATA"
ROLES = (GSS, NCA)
FIELD_VERSION = {
    GSS: "GH_GSS_PHC_2021_V3K_TABLE5P10@TESTONLY1",
    NCA: "GH_NCA_Q4_2021_BULLETIN_TABLE10@TESTONLY1",
}
PUBLISHER = {
    GSS: "Ghana Statistical Service",
    NCA: "National Communications Authority",
}
FAMILY = {
    GSS: "GH_GSS_PHC_2021",
    NCA: "GH_NCA_LICENSEE_REPORTS_2021Q4",
}
NATIVE_UNIT = {
    GSS: "RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING",
    NCA: "ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS",
}
NATIVE_GEOGRAPHY = {GSS: "GHANA_RURAL", NCA: "GHANA_NATIONAL"}
NATIVE_MEASURE = {
    GSS: "ELECTRICITY_MAIN_LIGHTING_ALL_SUBTYPES",
    NCA: "ACTIVE_MOBILE_DATA_90_DAY_TRAFFIC",
}
PUBLICATION_DATE = {GSS: "2022-02-24", NCA: "2022-07-08"}
OBSERVATION_PERIOD = {
    GSS: "2021 PHC", NCA: "2021-Q4 (90-day activity definition)",
}
EXPECTED_SUBTYPES = {
    "mains": 2288193,
    "community_grid": 74490,
    "generator": 3640,
    "solar_inverter": 21512,
    "wind": 357,
}
PERMISSION = "TEST_ONLY_NO_EXTERNAL_USE_GRANT"


class D2P3Error(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _hash(obj: Any) -> str:
    return sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _date(value: Any) -> date:
    if not isinstance(value, str):
        raise D2P3Error("MISSING_OR_INVALID_CLOCK")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise D2P3Error("MISSING_OR_INVALID_CLOCK") from None
    if parsed.isoformat() != value:
        raise D2P3Error("MISSING_OR_INVALID_CLOCK")
    return parsed


def _int(value: Any) -> bool:
    return type(value) is int and value >= 0


def _check_row(row: Mapping[str, Any]) -> None:
    role = row.get("role")
    if role not in ROLES:
        raise D2P3Error("UNEXPECTED_FIELD_ROLE")
    if row.get("fixture_only") is not True:
        raise D2P3Error("FIELD_ISSUANCE_LAUNDERING")
    if row.get("issued") is not False:
        raise D2P3Error("ISSUER_FORGERY")
    if row.get("issuer_signature") is not None:
        raise D2P3Error("ISSUER_FORGERY")
    if row.get("source_pdf_sha256") is not None:
        raise D2P3Error("UNVERIFIED_BINARY_CUSTODY")
    if row.get("issuer_ref") is not None:
        raise D2P3Error("EXTERNAL_CUSTODY_OR_ISSUER_FORGERY")
    if row.get("permission") != PERMISSION:
        raise D2P3Error("REAL_USE_PERMISSION_NOT_ISSUED")
    if row.get("publisher") != PUBLISHER[role]:
        raise D2P3Error("OFFICIAL_PUBLISHER_IDENTITY_MISMATCH")
    if row.get("family") != FAMILY[role]:
        raise D2P3Error("SOURCE_FAMILY_IDENTITY_MISMATCH")
    if row.get("native_unit") != NATIVE_UNIT[role]:
        raise D2P3Error("NATIVE_UNIT_OR_MEASURE_MISMATCH")
    if row.get("native_geography") != NATIVE_GEOGRAPHY[role]:
        raise D2P3Error("NATIVE_GEOGRAPHY_MISMATCH")
    if row.get("native_measure") != NATIVE_MEASURE[role]:
        raise D2P3Error("NATIVE_UNIT_OR_MEASURE_MISMATCH")
    if row.get("status") not in {"AVAILABLE_TEST_ONLY", "REVOKED_TEST_ONLY"}:
        raise D2P3Error("UNKNOWN_SOURCE_STATE")
    if row.get("publication_date") != PUBLICATION_DATE[role]:
        raise D2P3Error("PUBLICATION_CLOCK_MISMATCH")
    if row.get("observation_period") != OBSERVATION_PERIOD[role]:
        raise D2P3Error("OBSERVATION_CLOCK_MISMATCH")
    values = row.get("values")
    if not isinstance(values, dict):
        raise D2P3Error("MISSING_NUMERIC_VALUES")
    if role == GSS:
        if row.get("exclusions") != ["SECONDARY_HOUSING", "VACANT_DWELLINGS"]:
            raise D2P3Error("GSS_EXCLUSION_DROPPED")
        a, b, pct = values.get("numerator"), values.get("denominator"), values.get("published_percent")
        parts = values.get("electricity_subtypes")
        if (not _int(a) or not _int(b) or b == 0 or a > b or
                type(pct) not in (int, float) or round(100 * a / b, 1) != pct):
            raise D2P3Error("GSS_VALUE_DENOMINATOR_OR_SUBTYPE_INTEGRITY")
        if (not isinstance(parts, dict) or set(parts) != set(EXPECTED_SUBTYPES)
                or sum(parts.values()) != a):
            raise D2P3Error("GSS_ELECTRICITY_SUBTYPE_IDENTITY_MISMATCH")
    else:
        total, pre, post = (
            values.get("active_subscriptions"), values.get("prepaid"), values.get("postpaid")
        )
        if (not all(_int(x) for x in (total, pre, post)) or pre + post != total):
            raise D2P3Error("NCA_VALUE_SPLIT_INTEGRITY")
        if row.get("unique_persons") is not False or row.get("rural_split") is not None:
            raise D2P3Error("NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE")


def _field_payload(row: Mapping[str, Any]) -> dict[str, Any]:
    """All scientific identity fields, deliberately excluding the emitted ref."""
    role = row["role"]
    return {
        "schema": SCHEMA,
        "producer_id": "D2P3_SOURCEFREE_TEST_ONLY_FIELD_PRODUCER@1",
        "producer_grade": "SOURCEFREE_TEST_ONLY_NO_ISSUANCE",
        "source_family": FAMILY[role],
        "publisher": PUBLISHER[role],
        "field_version": FIELD_VERSION[role],
        "edition_or_revision": "UNKNOWN_TYPED",
        "role": role,
        "native_unit": NATIVE_UNIT[role],
        "native_geography": NATIVE_GEOGRAPHY[role],
        "native_measure": NATIVE_MEASURE[role],
        "observation_clock": OBSERVATION_PERIOD[role],
        "publication_clock": PUBLICATION_DATE[role],
        "typed_authority_requirements": {
            "fixture_only": True,
            "issued": False,
            "issuer_signature": None,
            "source_pdf_sha256": None,
            "issuer_ref": None,
            "permission": PERMISSION,
        },
        "values": deepcopy(row["values"]),
        # Keep the source row for the no-person-unit counterfactual, but never
        # expose it as a second independent registry identity.
        "source_row": deepcopy(dict(row)),
    }


def field_content_ref(field: Mapping[str, Any]) -> str:
    """Recompute and verify the complete scientific-field content ref."""
    material = dict(field)
    claimed = material.pop("field_ref", None)
    if not isinstance(claimed, str) or not claimed.startswith("D2P_TESTONLY_FIELD:"):
        raise D2P3Error("MISSING_OR_FOREIGN_FIELD_REF")
    digest = _hash(material)
    if claimed != "D2P_TESTONLY_FIELD:" + digest:
        raise D2P3Error("FIELD_CONTENT_REF_MISMATCH")
    return claimed


def produce_field(row: Mapping[str, Any]) -> dict[str, Any]:
    _check_row(row)
    field = _field_payload(row)
    field["field_ref"] = "D2P_TESTONLY_FIELD:" + _hash(field)
    return field


def produce_registry(rows: Iterable[Mapping[str, Any]]) -> "ProducerRegistry":
    fields = []
    for row in rows:
        fields.append(produce_field(row))
    return ProducerRegistry(fields)


@dataclass(frozen=True)
class ProducerField:
    field_ref: str
    payload: Mapping[str, Any]


class ProducerRegistry:
    """The only field store; producer emits, reader dereferences exact refs."""
    schema = REGISTRY_SCHEMA

    def __init__(self, fields: Iterable[Mapping[str, Any]]):
        self._records: dict[str, dict[str, Any]] = {}
        self._revoked: set[str] = set()
        self._by_role: dict[str, str] = {}
        for raw in fields:
            field = deepcopy(dict(raw))
            _check_row(field["source_row"])
            ref = field_content_ref(field)
            if ref in self._records:
                raise D2P3Error("DUPLICATE_FIELD_REF")
            role = field["role"]
            if role in self._by_role:
                raise D2P3Error("DUPLICATE_FIELD_ROLE")
            self._records[ref] = field
            self._by_role[role] = ref
        if set(self._by_role) != set(ROLES):
            raise D2P3Error("TWO_INDEPENDENT_FIELDS_REQUIRED")

    def refs_by_role(self) -> dict[str, str]:
        return dict(self._by_role)

    def dependency_refset(self) -> tuple[str, ...]:
        return tuple(self._by_role[role] for role in ROLES)

    def dereference(self, ref: str) -> Mapping[str, Any]:
        field = self._records.get(ref)
        if field is None:
            raise D2P3Error("UNKNOWN_EXACT_FIELD_REF")
        if ref in self._revoked:
            raise D2P3Error("FIELD_REGISTRY_REVOKED")
        field_content_ref(field)
        _check_row(field["source_row"])
        if field["source_row"].get("status") != "AVAILABLE_TEST_ONLY":
            raise D2P3Error("SOURCE_REVOKED")
        return deepcopy(field)

    def revoke(self, ref: str) -> None:
        if ref not in self._records:
            raise D2P3Error("UNKNOWN_EXACT_FIELD_REF")
        self._revoked.add(ref)

    def snapshot_ref(self) -> str:
        return "D2P3_REGISTRY_SNAPSHOT:" + _hash({
            "schema": self.schema,
            "records": [
                {"field_ref": ref, "content_hash": field["field_ref"].split(":", 1)[1]}
                for ref, field in sorted(self._records.items())
            ],
            "revoked": sorted(self._revoked),
        })


def _field_row(field: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(field["source_row"]))


def read_exact(
    registry: ProducerRegistry,
    *,
    selected_refs: Mapping[str, str],
    relation: Mapping[str, Any],
    as_of: str,
    clock_mode: str,
    partial_allowed: bool = False,
    requested_person_exposure: bool = False,
    requested_pooling: bool = False,
    requested_model_use: bool = False,
) -> dict[str, Any]:
    """Read only the exact producer refs; no parallel row registry exists."""
    if not isinstance(registry, ProducerRegistry):
        raise D2P3Error("PRODUCER_OWNED_REGISTRY_REQUIRED")
    if clock_mode != "HISTORICAL_PUBLICATION_AWARE":
        raise D2P3Error("CURRENT_OR_OTHER_CLOCK_NOT_AUTHORIZED")
    if requested_person_exposure or requested_pooling or requested_model_use:
        raise D2P3Error("PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN")
    if set(selected_refs) != set(ROLES) or len(set(selected_refs.values())) != 2:
        raise D2P3Error("TWO_DISTINCT_ROLE_REFS_REQUIRED")
    if (relation.get("kind") != "TEST_ONLY_NONPOOLED_COPRESENCE" or
            relation.get("fixture_only") is not True or
            relation.get("issued_EE13") is not False or
            relation.get("ordered_refs") != [selected_refs[GSS], selected_refs[NCA]] or
            relation.get("population_join") is not False):
        raise D2P3Error("INDEPENDENT_EE13_NOT_ISSUED_OR_RELATION_CHANGED")
    asof = _date(as_of)
    values_read = []
    refusals = []
    for role in ROLES:
        ref = selected_refs[role]
        try:
            field = registry.dereference(ref)
            if field["role"] != role:
                raise D2P3Error("ROLE_REF_SUBSTITUTION")
            if asof < _date(field["publication_clock"]):
                raise D2P3Error("NOT_PUBLISHED_AT_SELECTED_ASOF")
            values_read.append({
                "role": role,
                "field_ref": ref,
                "source_family": field["source_family"],
                "publisher": field["publisher"],
                "native_unit": field["native_unit"],
                "native_geography": field["native_geography"],
                "native_measure": field["native_measure"],
                "observation_clock": field["observation_clock"],
                "publication_clock": field["publication_clock"],
                "values": deepcopy(field["values"]),
            })
        except D2P3Error as exc:
            refusals.append({"role": role, "field_ref": ref, "reason": exc.code})
    state = (
        "TWO_VALUES_READ_TEST_ONLY" if len(values_read) == 2
        else "PARTIAL_TEST_ONLY_NOT_POSITIVE" if partial_allowed and values_read
        else "REFUSED_REQUIRED_FIELD_TEST_ONLY"
    )
    if state == "REFUSED_REQUIRED_FIELD_TEST_ONLY":
        values_read = []
    out = {
        "schema": "D2P3_EXACT_PRODUCER_REF_READER@1",
        "execution_grade": "ISOLATED_SOURCEFREE_TEST_ONLY",
        "state": state,
        "as_of": asof.isoformat(),
        "world_clock": "HISTORICAL_PUBLICATION_AWARE",
        "selected_refs": [selected_refs[role] for role in ROLES],
        "dependency_readset": [selected_refs[role] for role in ROLES],
        "values_read": values_read,
        "refusals": refusals,
        "registry_snapshot_ref": registry.snapshot_ref(),
        "operative_OC05": False,
        "real_N9_consumer": False,
        "issued_N5N6": False,
        "issued_EE13": False,
        "pooling": False,
        "person_exposure": False,
        "model_use": False,
    }
    out["test_snapshot_ref"] = "D2P3_SNAPSHOT:" + _hash(out)
    return out


def read_produced_registry(registry: ProducerRegistry, *, as_of: str, partial_allowed: bool = False, **flags) -> dict[str, Any]:
    refs = registry.refs_by_role()
    relation = {
        "kind": "TEST_ONLY_NONPOOLED_COPRESENCE",
        "fixture_only": True,
        "issued_EE13": False,
        "ordered_refs": [refs[GSS], refs[NCA]],
        "population_join": False,
    }
    return read_exact(registry, selected_refs=refs, relation=relation, as_of=as_of,
                      clock_mode="HISTORICAL_PUBLICATION_AWARE",
                      partial_allowed=partial_allowed, **flags)
