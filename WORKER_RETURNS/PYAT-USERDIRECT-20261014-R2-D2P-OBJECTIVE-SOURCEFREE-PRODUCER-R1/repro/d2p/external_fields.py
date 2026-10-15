"""D2P sourcefree candidate producer: ExternalPublishedAggregateField.

Minimal test-only candidate that binds versioned GSS vs NCA native units,
numeric values, denominator/source-observation and publication clocks, and
typed source authority requirements. No false legitimate issuance: every
record carries issued=False, TEST_ONLY permission, NULL binary custody, NULL
issuer signature. Reuses N9C row material as the underlying numeric rows
(read-only); adds the producer-contract header plus an explicit authority
requirements check.

Nothing here is an N5/N6 field, a source issuer, EE13, N7, N9 or OC05.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
from hashlib import sha256
import json
from typing import Any, Mapping

SCHEMA = "D2P_EXTERNAL_PUBLISHED_AGGREGATE_FIELD@1"
PRODUCER_ID = "D2P_SOURCEFREE_TEST_ONLY_FIELD_PRODUCER@1"
FIELD_VERSION_GSS = "GH_GSS_PHC_2021_V3K_TABLE5P10@TESTONLY1"
FIELD_VERSION_NCA = "GH_NCA_Q4_2021_BULLETIN_TABLE10@TESTONLY1"

GSS = "GSS_RURAL_LIGHTING"
NCA = "NCA_NATIONAL_MOBILE_DATA"
ROLES = (GSS, NCA)

REQUIRED_TEST_AUTHORITY = {
    "fixture_only": True,
    "issued": False,
    "issuer_signature": None,
    "source_pdf_sha256": None,
    "issuer_ref": None,
    "permission": "TEST_ONLY_NO_EXTERNAL_USE_GRANT",
}


class FieldProducerError(ValueError):
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
        raise FieldProducerError("INVALID_FIELD_CLOCK") from None


def check_field_authority(row: Mapping[str, Any]) -> None:
    """Typed source authority requirements: must hold for every produced field.

    No issuance is manufactured: a field that claims issued=True, a real
    permission, a non-NULL binary SHA or an issuer signature/ref is rejected
    as ISSUER_FORGERY / REAL_USE_PERMISSION_NOT_ISSUED.
    """
    if row.get("fixture_only") is not True:
        raise FieldProducerError("FIELD_ISSUANCE_LAUNDERING")
    if row.get("issued") is not False:
        raise FieldProducerError("ISSUER_FORGERY")
    if row.get("issuer_signature") is not None:
        raise FieldProducerError("ISSUER_FORGERY")
    if row.get("source_pdf_sha256") is not None:
        raise FieldProducerError("UNVERIFIED_BINARY_CUSTODY")
    if row.get("issuer_ref") is not None:
        raise FieldProducerError("EXTERNAL_CUSTODY_OR_ISSUER_FORGERY")
    if row.get("permission") != REQUIRED_TEST_AUTHORITY["permission"]:
        raise FieldProducerError("REAL_USE_PERMISSION_NOT_ISSUED")


def check_field_clocks(row: Mapping[str, Any]) -> None:
    if not isinstance(row.get("publication_date"), str):
        raise FieldProducerError("MISSING_PUBLICATION_CLOCK")
    _date(row["publication_date"])
    if not isinstance(row.get("observation_period"), str) or not row["observation_period"]:
        raise FieldProducerError("MISSING_OBSERVATION_CLOCK")


EXPECTED_FIELD_VERSION = {
    GSS: FIELD_VERSION_GSS,
    NCA: FIELD_VERSION_NCA,
}


def produce_field(row: Mapping[str, Any]) -> dict[str, Any]:
    """Bind one row into a versioned ExternalPublishedAggregateField candidate."""
    material = deepcopy(dict(row))
    check_field_authority(material)
    check_field_clocks(material)
    role = material.get("role")
    if role not in ROLES:
        raise FieldProducerError("UNEXPECTED_FIELD_ROLE")
    field = {
        "schema": SCHEMA,
        "producer_id": PRODUCER_ID,
        "producer_grade": "SOURCEFREE_TEST_ONLY_NO_ISSUANCE",
        "field_version": EXPECTED_FIELD_VERSION[role],
        "role": role,
        "native_unit": material.get("native_unit"),
        "native_geography": material.get("native_geography"),
        "native_measure": material.get("native_measure"),
        "values": deepcopy(material.get("values")),
        "observation_clock": material.get("observation_period"),
        "publication_clock": material.get("publication_date"),
        "typed_authority_requirements": deepcopy(REQUIRED_TEST_AUTHORITY),
        "underlying_row": material,
    }
    field["field_ref"] = "D2P_TESTONLY_FIELD:" + _hash(field)
    return field


def produce_two_fields(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Bind GSS and NCA rows into two independently content-addressed fields."""
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        field = produce_field(row)
        if field["role"] in out:
            raise FieldProducerError("DUPLICATE_FIELD_ROLE")
        out[field["role"]] = field
    if set(out) != set(ROLES):
        raise FieldProducerError("TWO_INDEPENDENT_FIELDS_REQUIRED")
    if out[GSS]["field_ref"] == out[NCA]["field_ref"]:
        raise FieldProducerError("FIELD_REF_COLLISION")
    return out


def field_content_ref(field: Mapping[str, Any]) -> str:
    return field["field_ref"]
