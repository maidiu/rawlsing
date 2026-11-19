#!/usr/bin/env python3
"""Actual saved-native I03 consumer guard witness.

Runs a sourcefree C11 candidate through write_direct_estate and the existing
CarrierNeutralResearchExecutor.execute_i03.  Set ANVIL_GUARD=1 to load the
isolated return-local guard modules; ANVIL_GUARD=0 uses the frozen evaluator.

No original source, no raw tokens, and no scientific rule are introduced.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

if os.environ.get("ANVIL_GUARD") == "1":
    import rawlsing_next  # noqa: F401
    for module_name, filename in (
        ("rawlsing_next._pre553_query_predicate", "pre553_query_predicate.worker.py"),
    ):
        spec = importlib.util.spec_from_file_location(module_name, HERE / filename)
        if spec is None or spec.loader is None:
            raise SystemExit("GUARD_MODULE_NOT_LOADABLE")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

from rawlsing_next.pre553_c11_ingest import (
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.tests.test_pre553_direct_estate_i03 import (
    _cold,
    _executor,
    _source_with_candidate,
)
import rawlsing_next.tests.test_pre553_empirical_query as native


class _MP:
    def __init__(self):
        self._saved = []

    def context(self):
        return self

    def setattr(self, obj, name, value):
        self._saved.append((obj, name, getattr(obj, name)))
        setattr(obj, name, value)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        for obj, name, value in reversed(self._saved):
            setattr(obj, name, value)


def _source(tag, rows=None):
    return _source_with_candidate(_MP(), tag, 1)


def _replace_event(source, candidate, state):
    respondent = source["respondents"]["R2"].ref
    events = []
    changed = 0
    for event in candidate.respondent_events:
        ref = event.scoped_respondent_ref
        same = (ref.get("object_id") == respondent.object_id
                and ref.get("content_hash") == respondent.content_hash)
        if same and changed == 0:
            from rawlsing_next.pre553_empirical_objects import RespondentEvent
            fields = dict(event.semantic_fields)
            fields.pop("typed_state", None)
            fields["response_state"] = state
            event = RespondentEvent(
                typed_state=state,
                authority_snapshot_refs=event.authority_snapshot_refs,
                dependency_refs=event.dependency_refs,
                producer_replay_locator_or_reference_root=event.producer_replay_locator_or_reference_root,
                **fields,
            )
            changed += 1
        events.append(event)
    if changed != 1:
        raise AssertionError("unresolved event replacement failed")
    replay = candidate.candidate_replay_manifest
    candidate = replace(candidate, respondent_events=tuple(events),
                        candidate_replay_manifest=None)
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
        replay_protocol_version=replay.replay_protocol_version,
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    repo = C11Repository()
    admitted = ingest_c11_source_release(candidate, repo)
    if not admitted.accepted:
        raise AssertionError("candidate with typed state refused")
    source = dict(source)
    source["repo"] = repo
    source["release_ref"] = admitted.release_ref
    return source, candidate


def _state_leaf(source, state):
    return {
        "op": "LEAF",
        "leaf_type": "TYPED_RESPONSE_STATE",
        "empirical_universe_ref": source["universe"].ref.as_dict(),
        "question_semantic_ref": source["qrefs"]["Y"].as_dict(),
        "typed_state_ref": source["qrefs"]["Y"].as_dict(),
        "state_semantic_authority_ref": source["source_auth"].authority_ref.as_dict(),
        "typed_state": state,
    }


def _execute(tag, root, *, state=None, condition="NOT", mapped=False):
    source, candidate = _source(tag, [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
    ])
    if state is not None:
        source, candidate = _replace_event(source, candidate, state)
    qa = native._query_authority(tag)
    diagnostic = _state_leaf(source, "INVALID_UNRESOLVED")
    value_leaf = _state_leaf(source, "SUBSTANTIVE_RESPONSE")
    if condition == "NOT":
        ast = {"op": "NOT", "children": [value_leaf]}
    elif condition == "POSITIVE":
        ast = value_leaf
    elif condition == "DIAGNOSTIC":
        ast = diagnostic
    elif condition == "MIXED":
        ast = {"op": "AND", "children": [
            diagnostic,
            {"op": "NOT", "children": [value_leaf]},
        ]}
    else:
        raise AssertionError("unknown condition")
    predicate = native._predicate(source, qa, ast, tag=f"{tag}-pred")
    query = native._query(source, qa, predicate, ("Y",), tag=f"{tag}-query")
    root = Path(root) / tag
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    estate_root, receipt = _cold(root, candidate, source["universe"].ref, "estate")
    executor = _executor(estate_root, receipt, source, qa, predicate, query)
    try:
        result = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        facts = tuple(result.facts)
        if not facts:
            return {"mode": condition, "fact_count": 0, "status": "NO_FACT"}
        fact = facts[0]
        fields = dict(fact.semantic_fields)
        return {
            "mode": condition,
            "fact_count": len(facts),
            "typed_state": fact.typed_state,
            "raw_denominator": fields.get("raw_denominator_support", 0),
            "raw_support": fields.get("raw_numerator_support", 0),
            "risk_count": len(fields.get("risk_set_member_refs", ())),
            "replay_ref": json.dumps(dict(fields.get("replay_ref", fact.replay_ref)), sort_keys=True),
            "detail": fields.get("execution_detail"),
        }
    except Exception as exc:
        return {"mode": condition, "status": "REFUSED", "code": type(exc).__name__,
                "detail": str(exc)[:240]}


def main():
    root = Path(os.environ.get(
        "ANVIL_GUARD_ROOT",
        "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/anvil-i03-guard",
    )).absolute()
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    out = {}
    for state, cond, label in (
        ("INVALID_UNRESOLVED", "NOT", "unresolved_not"),
        ("INVALID_UNRESOLVED", "POSITIVE", "unresolved_positive"),
        ("INVALID_UNRESOLVED", "MIXED", "unresolved_mixed"),
        ("INVALID_UNRESOLVED", "DIAGNOSTIC", "unresolved_diagnostic"),
        ("MISSING", "NOT", "known_missing_not"),
        (None, "NOT", "mapped_not"),
    ):
        out[label] = _execute(label, root, state=state, condition=cond)
    print(json.dumps({"guard": os.environ.get("ANVIL_GUARD") == "1", "results": out}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
