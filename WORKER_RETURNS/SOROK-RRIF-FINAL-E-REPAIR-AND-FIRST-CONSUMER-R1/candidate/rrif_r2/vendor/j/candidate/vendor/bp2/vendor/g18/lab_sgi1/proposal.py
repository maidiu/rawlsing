"""Scenario candidate proposal: real LLM capture, frozen records, semantic dedup.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
LLM output may propose scenarios ONLY. It may not set empirical probabilities, write
causal actor state, mint an admitted father, or write memories as fact.
Replay resolves the frozen exact proposal record; it never resamples the model.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import ssl
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .core import canon, h_obj, h_concat, typed, S, Ledger
from . import LAB_RULE_STATUS

PROPOSAL_GRAMMAR_VERSION = "SCENARIO_CANDIDATE_GRAMMAR@2.0-G15-CLOSED"

PROPOSAL_SYSTEM_PROMPT = (
    "You are a scenario proposal component inside a SOURCE-FREE SYNTHETIC GENEALOGY LAB. "
    "You may propose FINITE encounter/scenario candidates ONLY. "
    "You may NOT set empirical probabilities, may NOT write causal actor state, "
    "you may NOT mint an admitted father, may NOT write memories as fact, "
    "may NOT use or reference any future-child outcome. "
    "Proposals must be machine-readable JSON only."
)


# ---------------------------------------------------------------------------
# G13 REPAIR (defect family 4 -- future-child embargo membrane)
#
# The pre-repair prompt constructor selected a fixed allow-list of mother-anchor
# keys but passed `target`, `world_summary` and the nested `psyche` object
# through verbatim. A future-child field planted in ANY of those paths reached the
# model-visible prompt.
#
# The embargo is now enforced by recursive structural scrubbing of EVERY
# model-visible input path, not by key selection at one level. Scrubbing (rather
# than raising) preserves the historical clean prompts byte-for-byte, because
# absent prohibited material is never modified.
# ---------------------------------------------------------------------------

FUTURE_CHILD_REDACTION = "__FUTURE_CHILD_MATERIAL_REDACTED_EMBARGO__"

# The declared prohibited_future_input partition (SGI1 fixture manifest) plus
# generic future-child markers. Matching is case-insensitive substring on keys.
PROHIBITED_FUTURE_INPUT_MARKERS = (
    "future_child_outcome_label",
    "future_child_personality",
    "future_child_desired_adversity_tag",
    "future_child_health_outcome",
    "future_child_education_outcome",
    "any_field_derived_from_future_child",
)

_FUTURE_CHILD_KEY_RE = re.compile(
    r"future[_-]?child|child[_-]?(outcome|personality|adversity|wound|health|education)"
    r"|desired[_-]?(adversity|wound)|post[_-]?conception[_-]?outcome",
    re.IGNORECASE,
)


def _key_is_prohibited(key: str) -> bool:
    if not isinstance(key, str):
        return False
    k = key.lower()
    if k in {m.lower() for m in PROHIBITED_FUTURE_INPUT_MARKERS}:
        return True
    return bool(_FUTURE_CHILD_KEY_RE.search(k))


def scrub_future_child_material(value: Any, path: str = "$",
                                findings: Optional[List[Dict[str, Any]]] = None
                                ) -> Any:
    """Recursively redact future-child material from a model-visible structure.

    Redacts by KEY anywhere in the tree and by VALUE when a string literal
    carries a future-child marker. Returns the scrubbed structure and records
    every redaction so the caller can receipt it.
    """
    if findings is None:
        findings = []
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            child_path = f"{path}.{k}"
            if _key_is_prohibited(k):
                findings.append({"path": child_path, "reason": "PROHIBITED_KEY",
                                 "key": k})
                out[k] = FUTURE_CHILD_REDACTION
            else:
                out[k] = scrub_future_child_material(v, child_path, findings)
        return out
    if isinstance(value, list):
        return [scrub_future_child_material(v, f"{path}[{i}]", findings)
                for i, v in enumerate(value)]
    if isinstance(value, str) and _FUTURE_CHILD_KEY_RE.search(value):
        findings.append({"path": path, "reason": "PROHIBITED_VALUE_LITERAL"})
        return FUTURE_CHILD_REDACTION
    return value



def find_future_child_material(value: Any, path: str = "$",
                               findings: Optional[List[Dict[str, Any]]] = None
                               ) -> List[Dict[str, Any]]:
    """Recursively find future-child partition material in any visible structure.

    G18 repair: the old joint-material guard inspected only top-level keys. This
    scan covers every nested dict/list, every key (including aliases matched by
    the declared marker grammar), every string value, and opaque serialized JSON
    carried inside a string. It records the exact path; it never silently drops
    or redacts a live input packet.
    """
    if findings is None:
        findings = []
    if isinstance(value, dict):
        for k, v in value.items():
            child_path = f"{path}.{k}"
            if _key_is_prohibited(k):
                findings.append({"path": child_path, "reason": "PROHIBITED_KEY",
                                 "key": k})
            findings = find_future_child_material(v, child_path, findings)
        return findings
    if isinstance(value, (list, tuple)):
        for i, v in enumerate(value):
            findings = find_future_child_material(v, f"{path}[{i}]", findings)
        return findings
    if isinstance(value, str):
        if _FUTURE_CHILD_KEY_RE.search(value):
            findings.append({"path": path, "reason": "PROHIBITED_VALUE_LITERAL"})
        stripped = value.strip()
        if stripped[:1] in ("{", "["):
            try:
                parsed = json.loads(stripped)
            except (TypeError, ValueError):
                parsed = None
            if parsed is not None:
                findings = find_future_child_material(
                    parsed, f"{path}<serialized-json>", findings)
    return findings


def build_proposal_prompt(anchor_dict: Dict[str, Any], target: Dict[str, Any],
                          world_summary: Dict[str, Any], route_filter: Optional[str],
                          max_proposals: int) -> str:
    """Visible input model: mother anchor (allowed fields), target, world summary.

    G13 repair: every model-visible path (pending target, world summary and the
    nested psyche object) is recursively scrubbed of the prohibited future-child
    partition before serialisation. Clean inputs are unchanged byte-for-byte.
    """
    from .membrane import visible_prompt_parts
    a,t,w,route,findings=visible_prompt_parts(anchor_dict,target,world_summary,route_filter)
    return json.dumps(dict(instruction="Propose finite research encounter candidates under closed grammar",
        scenario_grammar_version=PROPOSAL_GRAMMAR_VERSION,mother_anchor_visible_fields=a,
        pending_target=t,world_summary=w,route_filter=route,max_proposals=max_proposals,
        boundary_status="HOLD_UNCLASSIFIED_INPUT" if findings else "SCREENED_CLOSED_SCHEMA",
        boundary_findings=findings),sort_keys=True)


# ---------------------------------------------------------------------------
# Model transport (real call, full capture). Fallback marks NOT_TESTED.
# ---------------------------------------------------------------------------

def call_model(*args,**kwargs):
    raise RuntimeError("G15_LIVE_PROVIDER_NOT_GRANTED")


def parse_candidate_json(raw: str) -> List[Dict[str, Any]]:
    """Extract the JSON candidate list from model output defensively."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
    start = raw.find("[")
    end = raw.rfind("]")
    obj: Any = None
    if start != -1 and end != -1:
        try:
            obj = json.loads(raw[start:end + 1])
        except json.JSONDecodeError:
            obj = None
    if obj is None:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            try:
                obj = json.loads(raw[start:end + 1])
            except json.JSONDecodeError:
                return []
    if obj is None:
        return []
    if isinstance(obj, dict):
        for k in ("candidates", "scenario_candidates", "proposals", "items", "data"):
            if isinstance(obj.get(k), list):
                obj = obj[k]
                break
        else:
            obj = [obj]
    out: List[Dict[str, Any]] = []
    for c in obj:
        if isinstance(c, dict):
            # normalize endpoint_constraints shape
            ec = c.get("endpoint_constraints")
            if isinstance(ec, list):
                c["endpoint_constraints"] = {
                    "second_parent_structure_and_position_constraints": ec
                }
            elif ec is None:
                c["endpoint_constraints"] = {}
            out.append(c)
    return out


# ---------------------------------------------------------------------------
# Dedup / canonicalization over semantic equivalence classes
# ---------------------------------------------------------------------------

def semantic_class_key(c: Dict[str, Any]) -> str:
    """Equivalence over route, endpoint causal requirements, counterpart constraints,
    witness obligations — NOT linguistic phrasing."""
    from .membrane import semantic_candidate
    return h_obj(semantic_candidate(c))


def dedup_candidates(candidates):
    from .membrane import semantic_candidate
    import unicodedata
    ids=[unicodedata.normalize('NFC',str(c.get('candidate_local_id',''))) for c in candidates]
    bad=not all(ids) or len(ids)!=len(set(ids))
    classes={};merges=[]
    if not bad:
        for c in candidates:
            ck=semantic_class_key(c)
            if ck not in classes:
                # A semantic representative never depends on wording or local ID.
                operative=semantic_candidate(c)
                operative['candidate_local_id']='SEM_'+ck.split(':')[-1]
                classes[ck]=dict(class_key=ck,representative_id='CLS_'+ck.split(':')[-1],member_ids=[],member_count=0,candidate=operative,raw_proposals=[])
            classes[ck]['member_ids'].append(c['candidate_local_id'])
            classes[ck]['member_count']+=1
            classes[ck]['raw_proposals'].append(dict(c))
    ordered=sorted(classes.values(),key=lambda x:x['class_key'])
    for x in ordered:
        x['member_ids'].sort();x['raw_proposals'].sort(key=lambda c:canon(c))
    return dict(classes=ordered,class_set_hash=h_obj([x['class_key'] for x in ordered]),n_input_candidates=len(candidates),n_classes=len(ordered),merge_receipts=merges,canonical_order=[x['class_key'] for x in ordered],class_member_index={x['class_key']:x['member_ids'] for x in ordered},coverage_receipt=dict(OTHER_UNRESOLVED=True,note='finite research grammar; not exhaustive'),status='DEDUP_UNDERDETERMINED' if bad else 'COMMITTED',hold_reasons=['DUPLICATE_OR_MISSING_CANDIDATE_ID'] if bad else [])


# ---------------------------------------------------------------------------
# Frozen proposal records
# ---------------------------------------------------------------------------

@dataclass
class ProposalRecord:
    record_id: str
    fixture_id: str
    route_filter: Optional[str]
    provider: str
    model_requested: str
    model_returned: Optional[str]
    prompt_text: str
    prompt_hash: str
    system_text: str
    system_hash: str
    raw_output: str
    raw_output_hash: str
    parsed_candidates: List[Dict[str, Any]]
    candidate_ids: List[str]
    dedup: Dict[str, Any]
    proposal_hash: str
    usage: Dict[str, int]
    wall_seconds: float
    lmm_automated_status: str  # AUTOMATED_LLM_PROPOSAL_EXECUTED | NOT_TESTED

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


def freeze_proposal_record(fixture_id: str, route_filter: Optional[str],
                           prompt: str, system: str, call: Dict[str, Any],
                           max_proposals: int) -> ProposalRecord:
    raw = call.get("raw_output", "")
    parsed = parse_candidate_json(raw)[:max_proposals] if raw else []
    for i, c in enumerate(parsed):
        c.setdefault("candidate_local_id", f"C_LLM_{fixture_id}_{i}")
        c.setdefault("candidate_kind", "PROVISIONAL_COUNTERPART")
        c.setdefault("candidate_origin", "LLM_PROPOSAL")
        c["plausibility_rank_ordinal"] = c.get("plausibility_rank_ordinal", i + 1)
        c["model_relative_plausibility_NOT_frequency"] = True
    ded = dedup_candidates(parsed)
    prompt_hash = h_obj({"prompt": prompt, "system": system})
    proposal_hash = h_obj({
        "prompt_hash": prompt_hash,
        "raw_output_hash": h_obj(raw),
        "parsed": parsed,
        "dedup_class_set_hash": ded["class_set_hash"],
    })
    return ProposalRecord(
        record_id=h_concat("PROPOSAL", fixture_id, str(route_filter), proposal_hash),
        fixture_id=fixture_id,
        route_filter=route_filter,
        provider=call.get("provider", "none"),
        model_requested=call.get("model_requested", ""),
        model_returned=call.get("model_returned"),
        prompt_text=prompt,
        prompt_hash=prompt_hash,
        system_text=system,
        system_hash=h_obj(system),
        raw_output=raw,
        raw_output_hash=h_obj(raw),
        parsed_candidates=parsed,
        candidate_ids=[c["candidate_local_id"] for c in parsed],
        dedup=ded,
        proposal_hash=proposal_hash,
        usage={
            "prompt_tokens": call.get("prompt_tokens", 0),
            "completion_tokens": call.get("completion_tokens", 0),
            "total_tokens": call.get("total_tokens", 0),
        },
        wall_seconds=call.get("wall_seconds", 0.0),
        lmm_automated_status=(
            "AUTOMATED_LLM_PROPOSAL_EXECUTED" if call.get("ok") else
            "AUTOMATED_LLM_PROPOSAL_NOT_TESTED"
        ),
    )


def frozen_fallback_record(fixture_id: str, route_filter: Optional[str]) -> ProposalRecord:
    """Independently authored frozen candidate set used ONLY if no model is callable.

    Marked AUTOMATED_LLM_PROPOSAL_NOT_TESTED. Never presented as model output.
    """
    base = [
        {
            "candidate_local_id": "C_FROZEN_0",
            "candidate_kind": "PROVISIONAL_COUNTERPART",
            "route_kind_id": "ROUTE_LOCAL_CLOSED",
            "endpoint_constraints": {
                "time_or_interval": "T_ENCOUNTER_LAB_WINDOW",
                "required_relation_objective_refs": ["REL_ENCOUNTER_WITNESSED"],
                "second_parent_structure_and_position_constraints": ["waged_artisan_local"],
                "conception_witness_requirements": ["ENCOUNTER_WITNESS_MIN_1"],
            },
            "assumptions": ["workplace adjacency contact"],
            "falsifiers": ["no shared shift overlap"],
            "plausibility_rank_ordinal": 1,
        },
        {
            "candidate_local_id": "C_FROZEN_1",
            "candidate_kind": "PROVISIONAL_COUNTERPART",
            "route_kind_id": "ROUTE_INSTITUTIONAL",
            "endpoint_constraints": {
                "time_or_interval": "T_ENCOUNTER_LAB_WINDOW",
                "required_relation_objective_refs": ["REL_ENCOUNTER_WITNESSED"],
                "second_parent_structure_and_position_constraints": ["evening_class_attendee"],
                "conception_witness_requirements": ["ENCOUNTER_WITNESS_MIN_1"],
            },
            "assumptions": ["evening class enrollment"],
            "falsifiers": ["class not attended"],
            "plausibility_rank_ordinal": 2,
        },
    ]
    if route_filter:
        base = [c for c in base if c["route_kind_id"] == route_filter] or base
    ded = dedup_candidates(base)
    ph = h_obj({"frozen": base, "fixture": fixture_id, "route": route_filter})
    return ProposalRecord(
        record_id=h_concat("FROZEN_PROPOSAL", fixture_id, str(route_filter)),
        fixture_id=fixture_id,
        route_filter=route_filter,
        provider="frozen_author",
        model_requested="NONE",
        model_returned=None,
        prompt_text="",
        prompt_hash=ph,
        system_text="",
        system_hash=h_obj(""),
        raw_output=json.dumps(base),
        raw_output_hash=h_obj(base),
        parsed_candidates=base,
        candidate_ids=[c["candidate_local_id"] for c in base],
        dedup=ded,
        proposal_hash=ph,
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        wall_seconds=0.0,
        lmm_automated_status="AUTOMATED_LLM_PROPOSAL_NOT_TESTED",
    )
