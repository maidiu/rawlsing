# v3/io/field_injection.py
# Wave 5: build state.field.raw from world_slice, driver_vec, civic_soul, imperial_block (harmonization layer).
# field_update merges config["field_injection"] in systems/field.py.

from __future__ import annotations

from typing import Any

from v3.io.v5_field_bridge import build_v5_field_bridge_injection


def _provenance_entry(
    source: str,
    value: float,
    *,
    confidence: float,
    overwritten_by: str | None = None,
    conflict: bool = False,
    note: str | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "source": source,
        "value": value,
        "confidence": confidence,
        "conflict": conflict,
    }
    if overwritten_by:
        entry["overwritten_by"] = overwritten_by
    if note:
        entry["note"] = note
    return entry


def _integrity_payload(
    status: str,
    *,
    reasons: list[str] | None = None,
    conflicts: list[dict[str, Any]] | None = None,
    confidence: float | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": status,
        "reasons": reasons or [],
        "conflicts": conflicts or [],
        "conflict_count": len(conflicts or []),
    }
    if confidence is not None:
        payload["confidence"] = confidence
    if error:
        payload["error"] = error
    return payload


def build_field_raw_from_civic_soul(civic_soul: dict[str, Any]) -> dict[str, float]:
    """
    Map civic_soul (v2/harmonization) to field.raw. Keys: e.g. solidarity, legitimacy, participation → morale, legitimacy.
    """
    out: dict[str, float] = {}
    for key in ("legitimacy", "morale", "repression_baseline", "economy"):
        v = civic_soul.get(key)
        if v is not None and isinstance(v, (int, float)):
            out[key] = max(0.0, min(100.0, float(v)))
    return out


def build_field_raw_from_imperial_block(imperial_block: dict[str, Any]) -> dict[str, float]:
    """
    Map imperial_block (country → block label or pressure dict) to field.raw. E.g. repression_justification, fear.
    """
    out: dict[str, float] = {}
    for key in ("repression_justification", "fear", "repression_baseline", "legitimacy"):
        v = imperial_block.get(key)
        if v is not None and isinstance(v, (int, float)):
            out[key] = max(0.0, min(100.0, float(v)))
    return out


def build_field_raw_from_world_slice(world_slice: dict[str, Any]) -> dict[str, float]:
    """
    Map v2 WorldSlice (or dict with same keys) to state.field.raw entries.
    v3 field.raw keys used: economy, repression_baseline, morale, recruitment, legitimacy,
    fear, defections, repression_justification. WorldSlice has gdp_per_capita (0-100),
    state_repression, inequality_index, etc.
    """
    out: dict[str, float] = {}
    gdp = world_slice.get("gdp_per_capita")
    if gdp is not None:
        out["economy"] = max(0, min(100, float(gdp)))
    rep = world_slice.get("state_repression")
    if rep is not None:
        out["repression_baseline"] = max(0, min(100, float(rep)))
    # Optional: inequality, unemployment, conflict → proxy for morale/legitimacy
    ineq = world_slice.get("inequality_index")
    if ineq is not None:
        # High inequality → lower baseline morale
        out["morale"] = max(0, min(100, 60.0 - (float(ineq) - 50) * 0.3))
    return out


def build_field_raw_from_driver_vec(driver_vec: dict[str, Any]) -> dict[str, float]:
    """
    Map v2 DriverVector (or dict) to field.raw where relevant.
    trust_vs_distrust → legitimacy; fatalism_vs_agency → morale proxy.
    """
    out: dict[str, float] = {}
    trust = driver_vec.get("trust_vs_distrust")
    if trust is not None:
        out["legitimacy"] = max(0, min(100, float(trust)))
    fatalism = driver_vec.get("fatalism_vs_agency")
    if fatalism is not None:
        out["morale"] = max(0, min(100, float(fatalism)))
    return out


def merge_field_injection(
    from_world_slice: dict[str, float],
    from_driver_vec: dict[str, float],
) -> dict[str, Any]:
    """Merge world_slice and driver_vec field dicts; driver_vec overrides where both set."""
    merged = dict(from_world_slice)
    provenance: dict[str, Any] = {}
    conflicts: list[dict[str, Any]] = []
    for k, v in from_driver_vec.items():
        if k in merged and merged[k] != v:
            conflicts.append(
                {
                    "key": k,
                    "world_slice_value": merged[k],
                    "driver_vec_value": v,
                    "override_source": "driver_vec",
                }
            )
            provenance[k] = _provenance_entry(
                "driver_vec",
                float(v),
                confidence=85.0,
                overwritten_by="driver_vec",
                conflict=True,
                note="driver_vec_overrode_world_slice",
            )
        else:
            provenance[k] = _provenance_entry("driver_vec", float(v), confidence=95.0)
        merged[k] = v
    for k, v in from_world_slice.items():
        provenance.setdefault(k, _provenance_entry("world_slice", float(v), confidence=95.0))
    reasons = []
    if not from_world_slice:
        reasons.append("missing_world_slice")
    if not from_driver_vec:
        reasons.append("missing_driver_vec")
    status = "ok"
    if not from_world_slice and not from_driver_vec:
        status = "failed"
        reasons.append("no_field_sources")
    elif not from_world_slice or not from_driver_vec:
        status = "degraded"
        reasons.append("no_field_sources")
    merged["_integrity"] = _integrity_payload(
        status,
        reasons=reasons,
        conflicts=conflicts,
        confidence=100.0 if status == "ok" else 60.0 if status == "degraded" else 0.0,
    )
    merged["_provenance"] = {
        "sources": {
            "world_slice": {
                "present": bool(from_world_slice),
                "keys": sorted(from_world_slice.keys()),
            },
            "driver_vec": {
                "present": bool(from_driver_vec),
                "keys": sorted(from_driver_vec.keys()),
            },
        },
        "fields": provenance,
        "conflicts": conflicts,
    }
    return merged


def build_field_injection_from_harmonization(
    driver_model_output: dict[str, Any] | None = None,
    civic_soul: dict[str, Any] | None = None,
    imperial_block: dict[str, Any] | None = None,
    world_slice: dict[str, Any] | None = None,
    driver_vec: dict[str, Any] | None = None,
    v5_field_bridge: dict[str, Any] | None = None,
) -> dict[str, float]:
    """
    Build field_injection dict from harmonization inputs. Later sources override earlier.
    field_update uses this when config["field_injection"] is set (e.g. by run script from v2/harmonization).
    """
    out: dict[str, float] = {}
    if world_slice:
        for k, v in build_field_raw_from_world_slice(world_slice).items():
            out[k] = v
    if driver_vec:
        for k, v in build_field_raw_from_driver_vec(driver_vec).items():
            out[k] = v
    if driver_model_output and isinstance(driver_model_output, dict):
        for key in ("economy", "morale", "legitimacy", "repression_baseline", "repression_justification", "fear"):
            v = driver_model_output.get(key)
            if v is not None and isinstance(v, (int, float)):
                out[key] = max(0.0, min(100.0, float(v)))
    if civic_soul:
        for k, v in build_field_raw_from_civic_soul(civic_soul).items():
            out[k] = v
    if imperial_block:
        for k, v in build_field_raw_from_imperial_block(imperial_block).items():
            out[k] = v
    if v5_field_bridge:
        for k, v in build_v5_field_bridge_injection(v5_field_bridge).items():
            out[k] = v
    return out


def get_field_injection(
    country_code: str,
    year: int,
    age: int,
    gender: str | None = None,
) -> dict[str, Any]:
    """
    Optional: fetch world_slice and driver_vec from v2 data_access and return field_injection dict.
    On lookup failure or v2 import failure, returns a dict with an `_integrity` payload describing
    the failure instead of silently returning an empty mapping.
    """
    try:
        from v2.data_access import get_world_slice, get_driver_vec
    except ImportError:
        return {
            "_integrity": _integrity_payload(
                "failed",
                reasons=["v2_data_access_unavailable"],
                confidence=0.0,
            ),
            "_provenance": {
                "sources": {"world_slice": {"present": False, "keys": []}, "driver_vec": {"present": False, "keys": []}},
                "fields": {},
                "conflicts": [],
            },
        }

    try:
        ws = get_world_slice(country_code, year)
        dv = get_driver_vec(country_code, year, age, gender=gender)
        ws_dict = ws.__dict__ if hasattr(ws, "__dict__") else (ws if isinstance(ws, dict) else {})
        dv_dict = dv.__dict__ if hasattr(dv, "__dict__") else (dv if isinstance(dv, dict) else {})
        a = build_field_raw_from_world_slice(ws_dict)
        b = build_field_raw_from_driver_vec(dv_dict)
        return merge_field_injection(a, b)
    except Exception as exc:
        return {
            "_integrity": _integrity_payload(
                "failed",
                reasons=["field_injection_lookup_failed"],
                confidence=0.0,
                error=exc.__class__.__name__,
            ),
            "_provenance": {
                "sources": {
                    "world_slice": {"present": False, "keys": []},
                    "driver_vec": {"present": False, "keys": []},
                },
                "fields": {},
                "conflicts": [],
                "error": exc.__class__.__name__,
            },
        }


def get_field_injection_for_year(
    country_code: str,
    year: int,
    age: int,
    gender: str | None = None,
) -> dict[str, Any]:
    """Alias for get_field_injection for use in run_and_print (per-year injection)."""
    return get_field_injection(country_code, year, age, gender=gender)
