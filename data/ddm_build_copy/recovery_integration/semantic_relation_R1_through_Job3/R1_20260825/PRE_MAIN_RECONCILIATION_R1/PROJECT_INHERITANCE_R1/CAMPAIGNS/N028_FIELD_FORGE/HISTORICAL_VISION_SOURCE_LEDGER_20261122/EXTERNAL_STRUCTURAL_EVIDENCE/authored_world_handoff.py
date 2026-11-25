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


def _prepare(evidence, *, scenario_id, rationale, positions, rules):
    """Translate explicit fictional premises to R36's exact four-key contract.

    Caller supplies complete authored positions/rules except source_ref. The
    incumbent owns admission (actors, sites, operations, intervals, clauses).
    Evidence is never translated automatically into a rule or personal fact.
    The returned sidecar must be retained with the exact authored spec.
    """
    if not all(type(x) is str and x.strip() for x in (scenario_id, rationale)):
        raise ValueError("explicit fictional scenario and rationale required")
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


def prepare_authored_history(evidence, *, scenario_id, rationale, positions, rules):
    """Preserve R9 native retrospective evidence contract without widening it."""
    if evidence.get("grade") != "NATIVE_RETROSPECTIVE_CONTEXT_NOT_WORLD_AUTHORITY":
        raise ValueError("unexpected evidence grade")
    return _prepare(evidence, scenario_id=scenario_id, rationale=rationale,
                    positions=positions, rules=rules)


def prepare_repertoire_authored_history(inquiry, *, scenario_id, rationale, positions,
                                        rules, public_notices):
    """R12: retain an R11 sourcefree inquiry beside independent fictional premises.

    A public institutional account is not its objective rule. The caller
    proposes both separately and the world owner admits/executes them. No
    automatic norm-to-rule, actor inference, or source authorization.
    Only the sourcefree experimental lane is eligible; native context stays
    internal and cannot be forwarded through this seam.
    """
    from rawlsing_next.pre553_s04_general_joint_algebra import S04ProjectionAnswer
    from rawlsing_next.pre553_empirical_objects import canonical_json
    if (type(inquiry) is not dict
            or inquiry.get("grade") != "INTERNAL_SOURCEFREE_FF_INQUIRY_NOT_SOURCE_OR_WORLD_ISSUANCE"
            or inquiry.get("state") != "PROVISIONAL_CONCEPT_REVISED_NOT_CERTIFIED"
            or inquiry.get("context_alignment") != "NO_SURVEY_TO_MATERIAL_CROSSWALK"
            or inquiry.get("independent_native_context") != {
                "grade": "HELD_NO_SELECTED_NATIVE_CONTEXT", "observations": []}):
        raise ValueError("only completed sourcefree inquiry without native context can enter this experiment")
    for export in (inquiry["baseline"], inquiry["contrast"]["left"],
                   inquiry["contrast"]["right"], inquiry["reverse"]):
        m = export["material"]
        a = S04ProjectionAnswer(canonical_json(m), export["ref"]["content_hash"])
        if (a.ref.as_dict() != export["ref"]
                or m["knowledge_ref"] != inquiry["knowledge_ref"]
                or m["source_fact_ref"] != inquiry["observation"]["fact_ref"]
                or m["independent_original_source_issuer"] is not None):
            raise ValueError("inconsistent sourcefree projection receipt")
    if inquiry["reverse"]["material"]["state"] != "OBSERVED_FULL_CASE_SUPPORT":
        raise ValueError("no positive observed motif to motivate a modeled alternative")
    if type(public_notices) is not list or not public_notices:
        raise ValueError("explicit fictional public account required")
    # Exactly the incumbent R48 authored world notice input, not a new
    # publication API. Keep separate from the structural-history spec.
    for n in public_notices:
        if (type(n) is not dict or set(n) != {
                "id", "public", "location", "public_terms", "public_text",
                "effective_from", "effective_until"} or n["public"] is not True
                or not all(type(n[k]) is str and n[k].strip()
                           for k in ("id", "location", "public_text"))
                or type(n["public_terms"]) is not list
                or not all(type(t) is str and t.strip() for t in n["public_terms"])
                or type(n["effective_from"]) is not int or type(n["effective_until"]) is not int
                or not 0 <= n["effective_from"] <= n["effective_until"]):
            raise ValueError("invalid explicit public account")
    if len({n["id"] for n in public_notices}) != len(public_notices):
        raise ValueError("duplicate public account")
    evidence = {"grade": "SOURCEFREE_REPERTOIRE_AND_FICTIONAL_ACCOUNT_NOT_WORLD_AUTHORITY",
                "inquiry": deepcopy(inquiry), "public_notices": deepcopy(public_notices)}
    return _prepare(evidence, scenario_id=scenario_id, rationale=rationale,
                    positions=positions, rules=rules)


def verify_handoff(packet):
    """Verify exact replay; not an authorization or incumbent admission check."""
    evidence = packet["evidence"]
    if evidence.get("grade") == "SOURCEFREE_REPERTOIRE_AND_FICTIONAL_ACCOUNT_NOT_WORLD_AUTHORITY":
        return prepare_repertoire_authored_history(
            evidence["inquiry"], public_notices=evidence["public_notices"],
            **packet["fictional_choice"]) == packet
    return prepare_authored_history(evidence, **packet["fictional_choice"]) == packet
