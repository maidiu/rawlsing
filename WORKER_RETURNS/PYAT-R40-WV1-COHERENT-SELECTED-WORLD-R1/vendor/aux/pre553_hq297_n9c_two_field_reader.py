"""HQ297 N9C isolated source-free candidate, NOT installed OC05 or issued N5/N6.

Tests real numeric value dereference from a defensive-copy fixture registry. Hashes
bind test fixture bytes only; they do not attest publisher custody or EE13 grants.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
from hashlib import sha256
import json
from typing import Any, Mapping

SCHEMA = "PRE553_HQ297_N9C_SOURCEFREE_VALUES_READER@1"
GSS = "GSS_RURAL_LIGHTING"
NCA = "NCA_NATIONAL_MOBILE_DATA"
ROLES = (GSS, NCA)
UNIT_GSS = "RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING"
UNIT_NCA = "ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS"


class TestOnlyReadError(ValueError):
    __test__ = False
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _hash(obj: Any) -> str:
    return sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value:
            raise ValueError("not an ISO date")
        return parsed
    except (ValueError, TypeError):
        raise TestOnlyReadError("INVALID_ASOF_OR_PUBLICATION_DATE") from None


def _integer(v: Any) -> bool:
    return type(v) is int and v >= 0


def _check_source(row: Mapping[str, Any]) -> None:
    if row.get("fixture_only") is not True or row.get("issued") is not False:
        raise TestOnlyReadError("FIELD_ISSUANCE_LAUNDERING")
    if row.get("source_pdf_sha256") is not None or row.get("issuer_ref") is not None:
        raise TestOnlyReadError("EXTERNAL_CUSTODY_OR_ISSUER_FORGERY")
    if row.get("permission") != "TEST_ONLY_NO_EXTERNAL_USE_GRANT":
        raise TestOnlyReadError("REAL_USE_PERMISSION_NOT_ISSUED")
    if row.get("status") not in ("AVAILABLE_TEST_ONLY", "REVOKED_TEST_ONLY"):
        raise TestOnlyReadError("UNKNOWN_SOURCE_STATE")
    if not isinstance(row.get("publication_date"), str):
        raise TestOnlyReadError("MISSING_PUBLICATION_CLOCK")
    _date(row["publication_date"])
    if not isinstance(row.get("observation_period"), str) or not row["observation_period"]:
        raise TestOnlyReadError("MISSING_OBSERVATION_CLOCK")
    # Bound documentary publication/observation clocks of this two-source fixture.
    # These anchors prove no source custody or archival release authenticity.
    expected_clocks = {
        GSS: ("2022-02-24", "2021 PHC"),
        NCA: ("2022-07-08", "2021-Q4 (90-day activity definition)"),
    }
    if (row.get("publication_date"), row.get("observation_period")) != expected_clocks.get(row.get("role")):
        raise TestOnlyReadError("PUBLICATION_OR_OBSERVATION_CLOCK_SUBSTITUTION")
    v = row.get("values")
    if not isinstance(v, dict):
        raise TestOnlyReadError("MISSING_NUMERIC_VALUES")
    if row.get("role") == GSS:
        if (row.get("family") != "GH_GSS_PHC_2021" or
            row.get("native_unit") != UNIT_GSS or
            row.get("native_geography") != "GHANA_RURAL" or
            row.get("native_measure") != "ELECTRICITY_MAIN_LIGHTING_ALL_SUBTYPES"):
            raise TestOnlyReadError("GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT")
        a, b, p = v.get("numerator"), v.get("denominator"), v.get("published_percent")
        parts = v.get("electricity_subtypes")
        if (not _integer(a) or not _integer(b) or b == 0 or a > b or
            type(p) not in (float, int) or
            round(100 * a / b, 1) != p or
            not isinstance(parts, dict) or len(parts) != 5 or
            any(not _integer(x) for x in parts.values()) or sum(parts.values()) != a):
            raise TestOnlyReadError("GSS_VALUE_DENOMINATOR_OR_SUBTYPE_INTEGRITY")
        if sorted(row.get("exclusions", [])) != ["SECONDARY_HOUSING", "VACANT_DWELLINGS"]:
            raise TestOnlyReadError("GSS_EXCLUSION_DROPPED")
    elif row.get("role") == NCA:
        if (row.get("family") != "GH_NCA_LICENSEE_REPORTS_2021Q4" or
            row.get("native_unit") != UNIT_NCA or
            row.get("native_geography") != "GHANA_NATIONAL" or
            row.get("native_measure") != "ACTIVE_MOBILE_DATA_90_DAY_TRAFFIC"):
            raise TestOnlyReadError("NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT")
        total,pre,post=v.get("active_subscriptions"),v.get("prepaid"),v.get("postpaid")
        if any(not _integer(x) for x in (total,pre,post)) or pre+post != total:
            raise TestOnlyReadError("NCA_VALUE_SPLIT_INTEGRITY")
        if row.get("unique_persons") is not False or row.get("rural_split") is not None:
            raise TestOnlyReadError("NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE")
    else:
        raise TestOnlyReadError("UNEXPECTED_FIELD_ROLE")


class TestOnlyRegistry:
    __test__ = False
    """Owns actual fixture numerics: requests carry refs, never the values."""
    def __init__(self, rows: list[dict[str, Any]]):
        self._records: dict[str, dict[str, Any]] = {}
        for source in rows:
            row = deepcopy(source)
            _check_source(row)
            ref = "TESTONLY_FIELD:" + _hash(row)
            if ref in self._records:
                raise TestOnlyReadError("DUPLICATE_SOURCE_FIELD")
            self._records[ref] = row

    def refs_by_role(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for ref, row in self._records.items():
            role = row["role"]
            if role in out:
                raise TestOnlyReadError("DUPLICATE_ROLE_IN_REGISTRY")
            out[role] = ref
        return out

    def dereference(self, ref: str) -> dict[str, Any]:
        if ref not in self._records:
            raise TestOnlyReadError("UNKNOWN_EXACT_FIELD_REF")
        row = deepcopy(self._records[ref])
        _check_source(row)
        if "TESTONLY_FIELD:"+_hash(row) != ref:
            raise TestOnlyReadError("FIELD_CONTENT_REF_MISMATCH")
        return row


def read_historical_test_only(
    registry: TestOnlyRegistry, *, selected_refs: Mapping[str, str],
    relation: Mapping[str, Any], as_of: str, clock_mode: str,
    partial_allowed: bool = False, requested_person_exposure: bool = False,
    requested_pooling: bool = False, requested_model_use: bool = False,
) -> dict[str, Any]:
    if not isinstance(registry, TestOnlyRegistry):
        raise TestOnlyReadError("INDEPENDENT_REGISTRY_REQUIRED")
    if clock_mode != "HISTORICAL_PUBLICATION_AWARE":
        raise TestOnlyReadError("CURRENT_OR_OTHER_CLOCK_NOT_AUTHORIZED")
    if requested_person_exposure or requested_pooling or requested_model_use:
        raise TestOnlyReadError("PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN")
    if set(selected_refs) != set(ROLES) or len(set(selected_refs.values())) != 2:
        raise TestOnlyReadError("TWO_DISTINCT_ROLE_REFS_REQUIRED")
    if (relation.get("kind") != "TEST_ONLY_NONPOOLED_COPRESENCE" or
        relation.get("fixture_only") is not True or
        relation.get("issued_EE13") is not False or
        relation.get("ordered_refs") != [selected_refs[GSS], selected_refs[NCA]] or
        relation.get("population_join") is not False):
        raise TestOnlyReadError("INDEPENDENT_EE13_NOT_ISSUED_OR_RELATION_CHANGED")
    asof = _date(as_of)
    records, denied = [], []
    for role in ROLES:
        ref = selected_refs[role]
        try:
            row = registry.dereference(ref)
            if row["role"] != role:
                raise TestOnlyReadError("ROLE_REF_SUBSTITUTION")
            if row["status"] != "AVAILABLE_TEST_ONLY":
                raise TestOnlyReadError("SOURCE_REVOKED")
            if asof < _date(row["publication_date"]):
                raise TestOnlyReadError("NOT_PUBLISHED_AT_SELECTED_ASOF")
            records.append({"role":role,"fixture_ref":ref,"source_family":row["family"],
                            "publisher":row["publisher"],"observation_period":row["observation_period"],
                            "publication_date":row["publication_date"],"native_unit":row["native_unit"],
                            "native_geography":row["native_geography"],"native_measure":row["native_measure"],
                            "uncertainty":row["uncertainty"],"values":deepcopy(row["values"])})
        except TestOnlyReadError as exc:
            denied.append({"role":role,"fixture_ref":ref,"reason":exc.code})
    if len({x["source_family"] for x in records}) != len(records):
        raise TestOnlyReadError("ORIGINAL_SOURCE_FAMILY_COLLISION")
    state = ("TWO_VALUES_READ_TEST_ONLY" if len(records)==2 else
             "PARTIAL_TEST_ONLY_NOT_POSITIVE" if partial_allowed and records else
             "REFUSED_REQUIRED_FIELD_TEST_ONLY")
    if state == "REFUSED_REQUIRED_FIELD_TEST_ONLY":
        records = []
    out={"schema":SCHEMA,"execution_grade":"ISOLATED_SOURCEFREE_TEST_ONLY",
         "operative_OC05":False,"real_N9_consumer":False,"issued_N5N6":False,
         "issued_EE13":False,"world_clock":"HISTORICAL_PUBLICATION_AWARE",
         "as_of":asof.isoformat(),"state":state,
         "values_read":records,"refusals":denied,
         "selected_fixture_refs":[selected_refs[x] for x in ROLES],
         "dependency_readset":[selected_refs[x] for x in ROLES],
         "successful_value_refset":[x["fixture_ref"] for x in records],"pooling":False,
         "person_exposure":False,"model_use":False}
    out["test_snapshot_ref"]="TESTONLY_SNAPSHOT:"+_hash(out)
    return out


def fixture_invalidation(previous: Mapping[str, Any], later: Mapping[str, Any]) -> dict[str, Any]:
    """Source-free provenance sensitivity, not actual B5 lifecycle invalidation."""
    if previous.get("schema")!=SCHEMA or later.get("schema")!=SCHEMA:
        raise TestOnlyReadError("INVALID_SNAPSHOT_PAIR")
    a={x["role"]:x for x in previous["values_read"]}
    b={x["role"]:x for x in later["values_read"]}
    changed=[role for role in ROLES if a.get(role)!=b.get(role)]
    unchanged=[role for role in ROLES if role not in changed]
    return {"kind":"TEST_ONLY_DEPENDENCY_DIFF_NOT_B5", "changed_roles":changed,
            "unaffected_roles":unchanged,"invalidate_previous_snapshot":bool(changed),
            "old_snapshot_ref":previous["test_snapshot_ref"],
            "new_snapshot_ref":later["test_snapshot_ref"]}
