"""Replace the S40 fresh-source shortcut for S42 speaking attempts only."""
from __future__ import annotations

from typing import Mapping

from .bootstrap import install

install()

from candidate import digest, seal  # noqa: E402
from language_mediation.artifacts import (  # noqa: E402
    build_native_artifact,
    build_translation_artifact,
)
from language_mediation.equivalence import evaluate_pair  # noqa: E402
from language_mediation.index import (  # noqa: E402
    LanguageRefusal,
    build_index,
    persist_index_cache,
)
import r31e.expression as expression  # noqa: E402
import s40.performer as s40_performer  # noqa: E402

from .errors import S43Refusal  # noqa: E402
from .planner import compile_historical_plan  # noqa: E402
from .registry import ATOMS, GRADE, PAIRS, REGISTRY_HASH  # noqa: E402

SPEAKING_OPTIONS = frozenset({"REQUEST_TOOL", "EXPLICIT_REFUSAL"})
BINDING_SCHEMA = "S40_GENERATED_LANGUAGE_BINDING@1"
S43_BINDING_SCHEMA = "S43_HISTORICAL_LANGUAGE_BINDING@1"
PROVENANCE = "TEST_ONLY_HISTORICAL_LANGUAGE_REPERTOIRE_NOT_EXTERNALLY_OBSERVED"


def _denied(session, attempt_request, generation_receipt, reason: str) -> dict:
    return s40_performer._result(
        actor_id=attempt_request["actor_id"],
        branch_id=session.branch_id,
        attempt_request=attempt_request,
        generation_receipt_hash=generation_receipt["hash"],
        status="DENIED",
        performed=False,
        reason=reason,
        clock=session.clock(),
    )


def perform_historical_attempt(
    session,
    attempt_request: Mapping[str, object],
    *,
    generation_receipt: Mapping[str, object],
    e1_identity: Mapping[str, object],
) -> dict:
    option = str(attempt_request["option_id"])
    if option not in SPEAKING_OPTIONS:
        return s40_performer.perform_generated_attempt(
            session,
            attempt_request,
            generation_receipt=generation_receipt,
            e1_identity=e1_identity,
        )

    context = session.s43_context()
    if not context:
        return _denied(session, attempt_request, generation_receipt,
                       "S43_EXPRESSION_CONTEXT_REQUIRED")
    try:
        index = build_index(session, actor_id="A")
        contract = expression.compile_contract(
            session,
            trigger_kind="GENERATED_ATTEMPT",
            trigger_text="",
            trigger_event_id=attempt_request["event_ref"],
        )
        plan, repertoire = compile_historical_plan(
            session,
            intent=option,
            context=context,
            contract=contract,
            index=index,
        )
        native = build_native_artifact(plan)
        translation = build_translation_artifact(plan, native)
        receipt = evaluate_pair(
            plan, native, translation, pairs=PAIRS, atom_universe=ATOMS
        )
        if receipt.get("status") != "ACCEPTED":
            return _denied(
                session, attempt_request, generation_receipt,
                "S43_EQUIVALENCE_REJECTED:"
                + ",".join(receipt.get("codes", [])),
            )

        selected = list(repertoire.get("selected_relations") or [])
        primary = selected[0]
        source = primary["source_event_ref"]
        access_id = primary["access_receipt"]["receipt_id"]
        world = session.world()
        candidate = session._candidate(plan, native)
        admission_id = digest({
            "candidate": candidate,
            "contract_hash": contract.get("contract_hash", ""),
            "plan_hash": plan.plan_hash,
            "native_artifact_hash": native["artifact_hash"],
            "translation_artifact_hash": translation["artifact_hash"],
            "clock": world.clock,
        })
        event = session._write_speech_event(
            plan, native, translation, receipt, contract, candidate,
            admission_id,
        )
        index_summary = {
            "index_hash": index["index_hash"],
            "readset_hash": index["readset_hash"],
            "cache_status": index["cache_status"],
        }
        admission = session._admission(
            plan, native, translation, receipt, contract, event,
            candidate, admission_id, index_summary,
        )
        s43_admission = {
            "schema": S43_BINDING_SCHEMA,
            "intent": repertoire["intent"],
            "unit_id": repertoire["unit_id"],
            "repertoire_id": repertoire["repertoire_id"],
            "repertoire_hash": repertoire["repertoire_hash"],
            "context": dict(repertoire["context"]),
            "selected_relation_ids": list(
                repertoire.get("selected_relation_ids") or []
            ),
            "selected_relations": list(
                repertoire.get("selected_relations") or []
            ),
            "contrary_relation_ids": list(
                repertoire.get("contrary_relation_ids") or []
            ),
            "contrary_relations": list(
                repertoire.get("contrary_relations") or []
            ),
            "invalidated_relation_ids": list(
                repertoire.get("invalidated_relation_ids") or []
            ),
            "invalidated_relations": list(
                repertoire.get("invalidated_relations") or []
            ),
            "contradictions": list(repertoire.get("contradictions") or []),
            "source_event_refs": list(repertoire.get("source_event_refs") or []),
            "access_receipt_ids": list(repertoire.get("access_receipt_ids") or []),
            "source_grades": dict(repertoire.get("source_grades") or {}),
            "registry_hash": REGISTRY_HASH,
            "private_generation_sources_in_plan": False,
        }
        admission["s43"] = s43_admission
        session.product._append_episode(
            session.branch_id, "A", "SAY", world.clock,
            {
                "event_id": event["event_id"],
                "text": native["text"],
                "language_tag": native["language_tag"],
                "gesture": candidate["gesture"],
                "tone": candidate["tone"],
                "strategy": candidate["strategy"],
                "contract_hash": contract.get("contract_hash", ""),
                "admission_id": admission_id,
                "plan_hash": plan.plan_hash,
                "spans": event["body"]["spans"],
            },
        )
        session.product._append_episode(
            session.branch_id, "A", "EXPRESSION_ADMISSION", world.clock,
            {
                "admission": admission,
                "candidate": candidate,
                "plan": plan.public(),
                "contract_hash": contract.get("contract_hash", ""),
                "multilingual_port": {
                    "schema": "S43_HISTORICAL_LANGUAGE_PORT@1",
                    "version": 1,
                },
            },
        )
        projection = session._write_translation_projection(
            event, plan, native, translation, receipt
        )
        session.product._checkpoint(session.branch_id, world.clock, world)
        persist_index_cache(session, index)
        binding = seal({
            "schema": BINDING_SCHEMA,
            "s43_schema": S43_BINDING_SCHEMA,
            "grade": GRADE,
            "provenance": PROVENANCE,
            "native": False,
            "intent": option,
            "language_tag": native["language_tag"],
            "target_language_tag": translation["target_language_tag"],
            "native_text": native["text"],
            "translation_text": translation["text"],
            "plan_hash": plan.plan_hash,
            "contract_hash": contract.get("contract_hash", ""),
            "native_artifact_hash": native["artifact_hash"],
            "translation_artifact_hash": translation["artifact_hash"],
            "equivalence_receipt_hash": receipt["receipt_hash"],
            "equivalence_status": receipt["status"],
            "equivalence_codes": list(receipt.get("codes", [])),
            "source_event_id": source["event_id"],
            "source_event_hash": source["event_hash"],
            "access_receipt_id": access_id,
            "source_event_refs": list(repertoire.get("source_event_refs") or []),
            "access_receipt_ids": list(repertoire.get("access_receipt_ids") or []),
            "speech_event_id": event["event_id"],
            "speech_event_hash": event["hash"],
            "admission_id": admission_id,
            "projection_episode_id": projection["episode_id"],
            "language_registry_hash": REGISTRY_HASH,
            "atom_universe_hash": digest(sorted(ATOMS)),
            "private_generation_sources_in_plan": False,
            "source_dependent": True,
            "source_dependent_refused": False,
            "fallback": False,
            "fallback_reason": "",
            "target_proposals": [],
            "e1_event_id": e1_identity["event_id"],
            "e1_event_hash": e1_identity["event_hash"],
            "s43_repertoire_id": repertoire["repertoire_id"],
            "s43_repertoire_hash": repertoire["repertoire_hash"],
            "s43_context": dict(repertoire["context"]),
            "s43_selected_relation_ids": list(
                repertoire.get("selected_relation_ids") or []
            ),
            "s43_contrary_relation_ids": list(
                repertoire.get("contrary_relation_ids") or []
            ),
            "s43_invalidated_relation_ids": list(
                repertoire.get("invalidated_relation_ids") or []
            ),
            "s43_source_event_refs": list(
                repertoire.get("source_event_refs") or []
            ),
            "s43_access_receipt_ids": list(
                repertoire.get("access_receipt_ids") or []
            ),
            "s43_source_grades": dict(repertoire.get("source_grades") or {}),
            "s43_contradictions": list(repertoire.get("contradictions") or []),
            "s43_index_hash": index["index_hash"],
            "s43_index_readset_hash": index["readset_hash"],
            "s43_index_cache_status": index["cache_status"],
        })
        return s40_performer._result(
            actor_id=attempt_request["actor_id"],
            branch_id=session.branch_id,
            attempt_request=attempt_request,
            generation_receipt_hash=generation_receipt["hash"],
            status="ADMITTED",
            performed=True,
            reason="OK",
            event=event,
            clock=session.clock(),
            language=binding,
        )
    except (S43Refusal, LanguageRefusal) as exc:
        return _denied(
            session, attempt_request, generation_receipt,
            "S43_SOURCE_BOUND_REFUSAL:" + getattr(exc, "code", type(exc).__name__),
        )


__all__ = [
    "BINDING_SCHEMA", "S43_BINDING_SCHEMA", "PROVENANCE", "SPEAKING_OPTIONS",
    "perform_historical_attempt",
]
