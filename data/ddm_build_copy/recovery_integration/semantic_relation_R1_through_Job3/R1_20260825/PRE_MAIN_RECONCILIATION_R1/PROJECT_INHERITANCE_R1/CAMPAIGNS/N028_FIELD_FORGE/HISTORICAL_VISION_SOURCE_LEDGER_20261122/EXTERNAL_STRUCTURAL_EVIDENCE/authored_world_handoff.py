"""R9: prepare the existing R36 authored structural-history input.

The evidence body is retained separately. Explicit fictional choices, not
native observations or survey answers, constitute the R36 rules/positions.
No world mutation, rule evaluation, source issuance, or psychological model.
"""
from copy import deepcopy
import hashlib
import json

from native_priority_readers import FINDEX_MARGINS, JOIN_STATUS, WBL_QUESTIONS


FIELDS = {
    "EPR": ("gwid", "gwgroupid", "from", "to", "status", "size", "reg_aut"),
    "WBL": ("economycode", "year", "reportyr", *WBL_QUESTIONS),
    "JOIN": ("Country Code", "Year of survey", "Survey Data Source", "Survey Type",
             "Subsample", *JOIN_STATUS, "Share of work contract", "Share of social security"),
    "FINDEX": ("codewb", "year", "group", "group2", *FINDEX_MARGINS),
}


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def select_world_evidence(pack, requests):
    """Read only demanded sources; keep separate keys, dates and unmatched rows.

    No implicit economy/polity mapping. Explicit requests are caller-selected,
    not source-qualified crosswalks or actual actor memberships.
    """
    results = []
    for request in requests:
        if set(request) != {"source", "keys", "reference_year"}:
            raise ValueError("explicit source, keys and reference_year required")
        source, keys, year = request["source"], request["keys"], request["reference_year"]
        if source not in FIELDS or not isinstance(keys, dict) or not keys:
            raise ValueError("unsupported source or empty native selection")
        required = {"EPR": {"gwid"}, "WBL": {"economycode", "year"},
                    "JOIN": {"Country Code", "Year of survey", "Subsample"},
                    "FINDEX": {"codewb", "year", "group", "group2"}}[source]
        if not required <= keys.keys() or (source == "EPR") != (year is not None):
            raise ValueError("missing native scope")
        results.append(pack.select(source, keys, FIELDS[source], year=year))
    return {"grade": "NATIVE_RETROSPECTIVE_CONTEXT_NOT_WORLD_AUTHORITY",
            "alignment": "INDEPENDENT_CALLER_SELECTED_NATIVE_SCOPES", "observations": results}


def prepare_authored_history(evidence, *, scenario_id, rationale, positions, rules):
    """Translate explicit fictional premises to R36's exact four-key contract.

    Caller supplies complete authored positions/rules except source_ref. The
    incumbent owns admission (actors, sites, operations, intervals, clauses).
    Evidence is never translated automatically into a rule or personal fact.
    The returned sidecar must be retained with the exact authored spec.
    """
    if not all(type(x) is str and x.strip() for x in (scenario_id, rationale)):
        raise ValueError("explicit fictional scenario and rationale required")
    if evidence.get("grade") != "NATIVE_RETROSPECTIVE_CONTEXT_NOT_WORLD_AUTHORITY":
        raise ValueError("unexpected evidence grade")
    if type(positions) is not list or type(rules) is not list:
        raise ValueError("explicit authored premises required")
    choice = {"scenario_id": scenario_id, "rationale": rationale,
              "positions": deepcopy(positions), "rules": deepcopy(rules)}
    for row in choice["positions"] + choice["rules"]:
        if type(row) is not dict or "source_ref" in row:
            raise ValueError("do not present a native source as rule authority")
    evidence = deepcopy(evidence)
    identity = _digest({"evidence": evidence, "fictional_choice": choice})
    ref = "fictional:ff:authored-history:sha256:" + identity
    spec = {"grade": "EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY", "source_ref": ref,
            "positions": [dict(row, source_ref=ref) for row in choice["positions"]],
            "rules": [dict(row, source_ref=ref) for row in choice["rules"]]}
    return {"grade": "PROVISIONAL_FICTIONAL_HANDOFF_NOT_NATIVE_ADMISSION",
            "evidence": evidence, "fictional_choice": choice,
            "authored_structural_history": spec, "content_hash": identity}


def verify_handoff(packet):
    """Verify exact replay; not an authorization or incumbent admission check."""
    return prepare_authored_history(packet["evidence"], **packet["fictional_choice"]) == packet
