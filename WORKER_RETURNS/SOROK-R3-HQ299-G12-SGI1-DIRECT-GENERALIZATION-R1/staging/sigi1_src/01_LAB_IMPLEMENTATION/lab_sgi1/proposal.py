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
import ssl
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .core import canon, h_obj, h_concat, typed, S, Ledger
from . import LAB_RULE_STATUS

PROPOSAL_GRAMMAR_VERSION = "SCENARIO_CANDIDATE_GRAMMAR@1.0-LAB"

PROPOSAL_SYSTEM_PROMPT = (
    "You are a scenario proposal component inside a SOURCE-FREE SYNTHETIC GENEALOGY LAB. "
    "You may propose FINITE encounter/scenario candidates ONLY. "
    "You may NOT set empirical probabilities, may NOT write causal actor state, "
    "may NOT mint an admitted father, may NOT write memories as fact, "
    "may NOT use or reference any future-child outcome. "
    "Proposals must be machine-readable JSON only."
)


def build_proposal_prompt(anchor_dict: Dict[str, Any], target: Dict[str, Any],
                          world_summary: Dict[str, Any], route_filter: Optional[str],
                          max_proposals: int) -> str:
    """Visible input model: mother anchor (allowed fields), target, world summary.

    Deliberately excludes the entire prohibited_future_input partition.
    """
    allowed_anchor = {
        "actor_id": anchor_dict["actor_id"],
        "variant": anchor_dict["variant"],
        "t_preconception": anchor_dict["t_preconception"],
        "psyche": anchor_dict["psyche"],
        "route_availability": anchor_dict["route_availability"],
        "mobility_history_present": anchor_dict["mobility_history_present"],
        "known_counterpart_identity_ref_or_null": anchor_dict["known_counterpart_identity_ref_or_null"],
        "already_generated_child_refs": anchor_dict["already_generated_child_refs"],
    }
    return json.dumps(
        {
            "instruction": "Propose finite conception-scenario encounter candidates for the pending target.",
            "scenario_grammar_version": PROPOSAL_GRAMMAR_VERSION,
            "mother_anchor_visible_fields": allowed_anchor,
            "pending_target": target,
            "world_summary": world_summary,
            "route_filter": route_filter,
            "max_proposals": max_proposals,
            "required_candidate_fields": [
                "candidate_local_id",
                "candidate_kind",
                "route_kind_id",
                "endpoint_constraints",
                "assumptions",
                "falsifiers",
                "plausibility_rank_ordinal",
            ],
            "hard_rules": [
                "candidate_kind in {KNOWN_COUNTERPART, PROVISIONAL_COUNTERPART, NONOCCURRENCE}",
                "plausibility_rank_ordinal is an ordinal rank only, never a frequency",
                "no future-child outcome may be referenced anywhere",
            ],
        },
        sort_keys=True,
        indent=None,
    )


# ---------------------------------------------------------------------------
# Model transport (real call, full capture). Fallback marks NOT_TESTED.
# ---------------------------------------------------------------------------

def _load_env(path: str = "/Users/matthewsmith/Desktop/Rawlsing/.env") -> Dict[str, str]:
    env: Dict[str, str] = {}
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#) ") and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def call_model(prompt: str, system: str, model: str, provider: str,
               max_tokens: int = 1600) -> Dict[str, Any]:
    """Single real model call. Returns raw capture; raises on transport failure."""
    import certifi

    env = _load_env()
    ctx = ssl.create_default_context(cafile=certifi.where())
    t0 = time.perf_counter()
    if provider == "openai":
        key = env.get("OPENAI_API_KEY", "")
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
            data = json.loads(r.read())
        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return {
            "ok": True,
            "provider": "openai",
            "model_requested": model,
            "model_returned": data.get("model"),
            "prompt": prompt,
            "system": system,
            "raw_output": text,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "wall_seconds": round(time.perf_counter() - t0, 4),
            "request_body": body,
        }
    if provider == "anthropic":
        key = env.get("ANTHROPIC_API_KEY", "")
        body = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(body).encode(),
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
            data = json.loads(r.read())
        text = "".join(b.get("text", "") for b in data.get("content", []))
        usage = data.get("usage", {})
        return {
            "ok": True,
            "provider": "anthropic",
            "model_requested": model,
            "model_returned": data.get("model"),
            "prompt": prompt,
            "system": system,
            "raw_output": text,
            "prompt_tokens": usage.get("input_tokens", 0),
            "completion_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
            "wall_seconds": round(time.perf_counter() - t0, 4),
            "request_body": body,
        }
    raise ValueError("unsupported provider: " + provider)


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
    ec = c.get("endpoint_constraints") or {}
    if not isinstance(ec, dict):
        ec = {"_raw_endpoint_constraints": ec}
    key_obj = {
        "route_kind_id": c.get("route_kind_id"),
        "candidate_kind": c.get("candidate_kind"),
        "endpoint_time": ec.get("time_or_interval"),
        "required_relation_objective_refs": sorted(
            str(x) for x in ec.get("required_relation_objective_refs", []) or []
        ),
        "second_parent_structure_constraints": sorted(
            str(x) for x in ec.get("second_parent_structure_and_position_constraints", []) or []
        ),
        "conception_witness_requirements": sorted(
            str(x) for x in ec.get("conception_witness_requirements", []) or []
        ),
    }
    return h_obj(key_obj)


def dedup_candidates(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Collapse semantic paraphrases into equivalence classes; preserve every proposal.

    Canonical ordering by class key (NFC/UTF-8 via canon()), never input index.
    Representative IDs are derived from the class key itself (semantic content),
    so neither phrasing multiplicity nor input order can alter the class set.
    """
    classes: Dict[str, Dict[str, Any]] = {}
    merge_receipts: List[Dict[str, Any]] = []
    for c in candidates:
        ck = semantic_class_key(c)
        rep_id = "CLS_" + ck.split(":")[-1][:24]
        if ck in classes:
            classes[ck]["member_ids"].append(c["candidate_local_id"])
            classes[ck]["member_count"] += 1
            merge_receipts.append({
                "action": "MERGE_INTO_CLASS",
                "class_key": ck,
                "member": c["candidate_local_id"],
                "representative": rep_id,
            })
        else:
            classes[ck] = {
                "class_key": ck,
                "representative_id": rep_id,
                "member_ids": [c["candidate_local_id"]],
                "member_count": 1,
                "candidate": c,
            }
    ordered = sorted(classes.values(), key=lambda x: x["class_key"])
    # Canonical representative payload: the member with the lexicographically
    # smallest candidate id — independent of input order and phrasing count.
    for x in ordered:
        members = [c for c in candidates
                   if c["candidate_local_id"] in x["member_ids"]]
        members.sort(key=lambda c: c["candidate_local_id"])
        x["candidate"] = members[0]
    # class-set hash binds SEMANTIC CLASSES ONLY: phrasings cannot multiply mass
    class_set_hash = h_obj(sorted(x["class_key"] for x in ordered))
    return {
        "classes": ordered,
        "class_set_hash": class_set_hash,
        "n_input_candidates": len(candidates),
        "n_classes": len(ordered),
        "merge_receipts": merge_receipts,
        "canonical_order": [x["class_key"] for x in ordered],
        "class_member_index": {
            x["class_key"]: sorted(x["member_ids"]) for x in ordered
        },
        "coverage_receipt": {
            "OTHER_UNRESOLVED": True,
            "note": "unenumerated scenarios may exist; completeness NOT claimed",
        },
    }


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
