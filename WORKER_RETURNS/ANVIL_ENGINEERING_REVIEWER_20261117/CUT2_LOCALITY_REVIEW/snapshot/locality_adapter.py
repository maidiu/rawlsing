"""Test-only physical-order adapter for DirectEstateI03Session._respondent_family.

Reads one respondent/family in physical gid/off order, then restores the
externally observable canonical ref-key order before yielding.  This is not a
product edit; it is installed only in the profiling process and restored.
"""
from __future__ import annotations

import json
from typing import Any, Iterator

from rawlsing_next.pre553_direct_estate_i03 import (
    DirectEstateError, DirectEstateI03Session,
    EmpiricalCoordinateFact, RoutingEligibilityFact, WeightMeasureFact,
)
from rawlsing_next.pre553_parquet_carrier import _object_from_row
from rawlsing_next.pre553_source_direct_parquet_estate import _key


def physical_order_respondent_family(
    self: DirectEstateI03Session, family: str, respondent_key: str,
) -> Iterator[Any]:
    db = self._require_live()
    expected_type = {
        "EmpiricalCoordinateFact": EmpiricalCoordinateFact,
        "RoutingEligibilityFact": RoutingEligibilityFact,
        "WeightMeasureFact": WeightMeasureFact,
    }[family]
    physical = self._files[family]
    cache = self._row_group_cache.setdefault(family, {})
    group = None
    rows = None
    # The ONLY locality change: physical gid/off order, not ref order.
    cursor = db.execute(
        "SELECT ref,gid,off FROM members WHERE family=? AND respondent=? "
        "ORDER BY gid,off", (family, respondent_key),
    )
    materialized: list[Any] = []
    for ref, gid, offset in cursor:
        self._require_live()
        if gid != group:
            if cache.get("gid") == gid:
                rows = cache["rows"]
            else:
                rows = physical.read_row_group(
                    gid, columns=["body_json", "ref"],
                ).to_pylist()
                cache.clear()
                cache.update({"gid": gid, "rows": rows})
            group = gid
        if rows is None or not 0 <= offset < len(rows):
            raise DirectEstateError("native I03 cold family locator out of bounds")
        row = rows[offset]
        obj = _object_from_row(json.loads(row["body_json"]))
        if (type(obj) is not expected_type or obj.ref.key != ref
                or row["ref"] != ref
                or _key(obj.scoped_respondent_ref) != respondent_key
                or _key(obj.empirical_universe_ref) != self.estate.i02.universe):
            raise DirectEstateError("native I03 cold family body/index identity mismatch")
        materialized.append(obj)
    # Restore the externally observable ORDER BY ref contract before yield.
    for obj in sorted(materialized, key=lambda item: item.ref.key):
        yield obj


def install() -> Any:
    original = DirectEstateI03Session._respondent_family
    DirectEstateI03Session._respondent_family = physical_order_respondent_family
    return original


def restore(original: Any) -> None:
    DirectEstateI03Session._respondent_family = original
