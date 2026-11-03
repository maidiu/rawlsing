"""One M35 C8/E1 world, one C12 root/branch, and targetless S35 C9 evaluations."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from install import install

install()

import firstclass
from bp2_joined import JoinedProducer
from bp2_joined import ports
from bp2_joined.producer import (
    make_actor_record,
    make_conditioning_source,
    make_e1_event,
)
from bp4.store import C12Store
from candidate import (
    CandidateStore,
    LaterActionConsumer,
    ResponseRule,
    ResponseRuleRegistry,
    ResponseStatus,
    TargetBranch,
    TargetReason,
    TargetRuleRegistry,
    bind_conditioning,
    digest,
    eligible_material,
    lookup_rule,
)
from candidate.pipeline import run_candidate_path

from . import access
from .access import S35ActorAccessRequest, S35Context, S35Evaluation

WORLD_SCHEMA = "SOROK_S35_ACCESS_WORLD@2"
RUN_SCHEMA = "SOROK_S35_ACCESS_RUN@2"
GRADE = "TEST_ONLY_SOURCEFREE_NOT_NATIVE"
RULE_ID = "TEST_ONLY_S35_CAN008_A"
RULE_AUTHORITY = "TEST_ONLY_S35_CAN008_A_AUTHORITY"
RULE_VERSION = "1"
RULE_CONTENT_HASH = digest(
    {"schema": "S35_ACTOR_ACCESS_RESPONSE_RULE@2", "test_only": True}
)
RULE_ISSUER = "TEST_ONLY_S35_RESPONSE_OWNER"
READER_ID = "TEST_ONLY_S35_TARGETLESS_READER"


class S35Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


@dataclass(frozen=True)
class S35Run:
    label: str
    run_dir: Path
    committed: bool
    refused: bool
    refusal_reason: str
    store_path: Path | None
    response: Any
    decision: Any
    pipeline: Any
    receipt: Mapping[str, Any]
    response_row_hash: str
    c9_receipt_hash: str
    target_state_rows: int
    target_ids: tuple[str, ...]
    context: S35Context

    @property
    def outcome(self) -> str:
        return str(self.response.reason) if self.response is not None else ""


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf8",
    )


def _response_rule(actor_id: str) -> ResponseRule:
    return ResponseRule(
        RULE_ID,
        RULE_VERSION,
        RULE_CONTENT_HASH,
        RULE_AUTHORITY,
        "1",
        RULE_ISSUER,
        True,
        (actor_id,),
        (access.S35_ACCESS_SOURCE_CLASS, access.S35_ACTION_SOURCE_CLASS),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
        (
            "a_local_perception_receipt",
            "a_owned_action_occurrence_receipt",
            "root_branch_clock_binding",
            "zero_target_proposals",
        ),
    )


class S35World:
    def __init__(
        self,
        root: Path,
        *,
        case: Mapping[str, Any],
        source: Mapping[str, Any],
        variant: str,
        producer: JoinedProducer,
        c12: C12Store,
        context: S35Context,
        c8_binding: Mapping[str, Any],
        root_branch: Mapping[str, Any],
        branch: Mapping[str, Any],
        root_state: Mapping[str, Any],
        rule: ResponseRule,
        conditioning_source: Mapping[str, Any],
        actor_record: Mapping[str, Any],
        e1_event: Mapping[str, Any],
        material_access: str,
    ) -> None:
        self.root = Path(root)
        self.case = dict(case)
        self.source = dict(source)
        self.variant = variant
        self.producer = producer
        self.c12 = c12
        self.context = context
        self.c8_binding = dict(c8_binding)
        self.root_branch = dict(root_branch)
        self.branch = dict(branch)
        self.root_state = dict(root_state)
        self.rule = rule
        self.conditioning_source = dict(conditioning_source)
        self.actor_record = dict(actor_record)
        self.e1_event = dict(e1_event)
        self.material_access = material_access
        self.response_registry = ResponseRuleRegistry.test_only((rule,))
        self._closed = False
        self.conditioning = bind_conditioning(
            subject=context.actor_id,
            sources=[self.conditioning_source],
            as_of=context.as_of,
        )
        self.material_eligible, self.eligible_material_refs, self.material_reason = (
            eligible_material(
                self.conditioning,
                event_scene=context.scene,
                event_time=context.event_time,
                as_of=context.as_of,
            )
        )
        self.source_actor_map = {
            "TEST_ONLY_R31J_A": producer.occurrence.actor_id,
            "TEST_ONLY_R31J_B": producer.occurrence.other_id,
        }

    @classmethod
    def build(
        cls,
        root,
        *,
        case: Mapping[str, Any],
        source: Mapping[str, Any] | None = None,
        variant: str = "A_REPAIR_LONG",
    ) -> "S35World":
        root = Path(root)
        if (root / "world.json").exists():
            raise S35Refusal("S35_WORLD_EXISTS", str(root))
        root.mkdir(parents=True, exist_ok=True)
        typed = firstclass.validate_source(
            source or firstclass.source_from_case(dict(case)), case
        )
        producer = JoinedProducer(
            root / "m35",
            material_source=typed,
            life=firstclass.prepare_life(typed, variant),
        )
        try:
            producer.stage_world()
            producer.stage_c8()
            producer.stage_out9()
            occurrence = producer.occurrence
            out9 = producer.out9
            e1 = ports.ADP019EventPort().bind_test_only_e1(
                occurrence={
                    "occurrence_id": out9.occurrence_id,
                    "identity_digest": out9.event.get("identity_digest"),
                    "_state_digest": out9.readset["state_digest"],
                    "_commit_receipt_id": out9.readset["commit_receipt_id"],
                    "_writer_version": out9.readset["writer_version"],
                },
                event_time=producer.event_time,
                verified_proof=out9.verified_proof,
            )
            actor_record = make_actor_record(occurrence, occurrence.actor_snapshot)
            e1_event = make_e1_event(
                occurrence, out9, e1, time=producer.event_time
            )
            material_access = (
                "granted" if typed["b_operation"] == "SHARE_TOOL" else "denied"
            )
            conditioning_source = make_conditioning_source(
                occurrence, as_of=producer.as_of, access=material_access
            )
            life = producer.historical_life
            state = {
                "A": dict(life.a_snapshot["state"]),
                "B": dict(life.b_snapshot["state"]),
            }
            c12 = C12Store(root / "c12.sqlite")
            c12.create_root(
                "root",
                clock=producer.event_time,
                actor_ids=["A", "B", "U"],
                state=state,
            )
            c12.fork("root", "s35")
            c12.checkpoint("s35", producer.event_time + 2, state)
            root_branch = c12.branch("root")
            branch = c12.branch("s35")
            root_state = c12.checkpoints("root")[-1]
            context = S35Context(
                actor_id=occurrence.actor_id,
                event_ref=e1_event["hash"],
                event_id=e1_event["event_id"],
                event_time=producer.event_time,
                as_of=producer.as_of,
                scene=str(e1_event["content"].get("scene", "")),
                root_id=str(root_branch["branch_id"]),
                root_branch_hash=digest(root_branch),
                root_state_hash=str(root_state["hash"]),
                branch_id=str(branch["branch_id"]),
                branch_hash=digest(branch),
                branch_parent_id=str(branch["parent_branch_id"]),
                branch_fork_clock=int(branch["fork_clock"]),
                clock=int(c12.last_clock("s35")),
                material_eligible=False,
                eligible_material_refs=(),
            )
            conditioning = bind_conditioning(
                subject=context.actor_id,
                sources=[conditioning_source],
                as_of=context.as_of,
            )
            material_ok, material_refs, _ = eligible_material(
                conditioning,
                event_scene=context.scene,
                event_time=context.event_time,
                as_of=context.as_of,
            )
            context = S35Context(
                **{
                    **context.as_dict(),
                    "eligible_material_refs": tuple(material_refs),
                    "material_eligible": material_ok,
                }
            )
            c8_binding = {
                "occurrence_id": out9.occurrence_id,
                "c8_state_digest": out9.readset["state_digest"],
                "c8_content_hash": out9.event.get("content_hash"),
                "c8_commit_receipt_id": out9.readset["commit_receipt_id"],
                "c8_writer_version": out9.readset["writer_version"],
                "e1_event_hash": e1_event["hash"],
                "e1_event_id": e1_event["event_id"],
                "journal_path": str(producer.env.journal_path),
                "key_path": str(producer.env.key_path),
                "key_id": producer.env.key_store.key_id,
                "anchor_log": str(producer.env.anchor.log_path),
                "anchor_watermark": str(producer.env.anchor.watermark_path),
            }
            rule = _response_rule(occurrence.actor_id)
            world = cls(
                root,
                case=case,
                source=typed,
                variant=variant,
                producer=producer,
                c12=c12,
                context=context,
                c8_binding=c8_binding,
                root_branch=root_branch,
                branch=branch,
                root_state=root_state,
                rule=rule,
                conditioning_source=conditioning_source,
                actor_record=actor_record,
                e1_event=e1_event,
                material_access=material_access,
            )
            manifest = {
                "schema": WORLD_SCHEMA,
                "grade": GRADE,
                "native": False,
                "variant": variant,
                "custody": {
                    "grade": "PRIVATE_TEST_ONLY_WORLD_INPUT",
                    "native": False,
                    "source": typed,
                    "case_preimage": firstclass.case_preimage(dict(case)),
                },
                "public_projection": access.public_source_projection(typed),
                "source_actor_map": world.source_actor_map,
                "material_access": material_access,
                "material_eligible": material_ok,
                "material_refs": list(material_refs),
                "c8": c8_binding,
                "context": context.as_dict(),
                "root_branch": root_branch,
                "branch": branch,
                "root_state": root_state,
                "rule": rule.as_dict(),
            }
            _write_json(root / "world.json", manifest)
            return world
        except Exception:
            producer.close()
            raise

    def perception_receipt(
        self,
        *,
        source_ref: str = "TEST_ONLY_ADP017_ACCESS_S35_A_LOCAL_PERCEPTION",
        perception_ref: str | None = None,
        access_status: str,
        perceived_at: int | None = None,
        scene: str | None = None,
        content: Mapping[str, Any] | None = None,
        revoked: bool = False,
        evidence_grade: str = access.S35_GRADE_CONTROLLED,
        actual_actor_input: bool = False,
        native: bool = False,
        qualification: str = access.S35_QUALIFICATION_CONTROLLED,
    ) -> dict:
        if perception_ref is None:
            perception_ref = "TEST_ONLY_A_PERCEPTION_" + str(access_status)
        return access.make_a_local_perception_receipt(
            context=self.context,
            source_ref=source_ref,
            perception_ref=perception_ref,
            access_status=access_status,
            perceived_at=(
                self.context.event_time if perceived_at is None else perceived_at
            ),
            scene=scene,
            content=content,
            revoked=revoked,
            evidence_grade=evidence_grade,
            actual_actor_input=actual_actor_input,
            native=native,
            qualification=qualification,
        )

    def action_receipt(
        self,
        *,
        source_ref: str = "TEST_ONLY_A_ACTION_S35_A_OWNED",
        action_ref: str | None = None,
        action_kind: str,
        performed: bool,
        action_time: int | None = None,
        content: Mapping[str, Any] | None = None,
        revoked: bool = False,
        evidence_grade: str = access.S35_GRADE_CONTROLLED,
        actual_actor_input: bool = False,
        native: bool = False,
        qualification: str = access.S35_QUALIFICATION_CONTROLLED,
    ) -> dict:
        if action_ref is None:
            action_ref = "TEST_ONLY_A_ACTION_" + str(action_kind)
        return access.make_a_owned_action_receipt(
            context=self.context,
            source_ref=source_ref,
            action_ref=action_ref,
            action_kind=action_kind,
            performed=performed,
            action_time=(
                self.context.event_time + 1 if action_time is None else action_time
            ),
            content=content,
            revoked=revoked,
            evidence_grade=evidence_grade,
            actual_actor_input=actual_actor_input,
            native=native,
            qualification=qualification,
        )

    def _public_source_binding(self) -> dict:
        return access.public_source_projection(self.source)

    def evaluate(
        self,
        label: str,
        *,
        perception_receipt: Mapping[str, Any] | None = None,
        action_receipt: Mapping[str, Any] | None = None,
        contradictory_context: bool = False,
        contradictory_refs: tuple[str, ...] = (),
        revoked_source_refs: frozenset[str] = frozenset(),
        qualified_owner_resolver: Any = None,
        enacted_history_refs: tuple[str, ...] = (),
        other_person_offer_ref: str = "",
        material_opportunity_ref: str = "",
        as_of: int | None = None,
    ) -> S35Run:
        label = str(label)
        if not label or "/" in label:
            raise S35Refusal("S35_RUN_LABEL_INVALID", label)
        run_dir = self.root / "runs" / label
        if run_dir.exists():
            raise S35Refusal("S35_RUN_EXISTS", str(run_dir))
        run_dir.mkdir(parents=True)
        request = S35ActorAccessRequest(
            perception_receipt=perception_receipt,
            action_receipt=action_receipt,
            contradictory_context=bool(contradictory_context),
            contradictory_refs=tuple(contradictory_refs),
            revoked_source_refs=frozenset(revoked_source_refs),
            qualified_owner_resolver=qualified_owner_resolver,
        )
        evaluated_as_of = self.context.as_of if as_of is None else int(as_of)
        lookup = lookup_rule(
            self.response_registry,
            authority_id=self.rule.authority_id,
            rule_version=self.rule.rule_version,
            rule_content_hash=self.rule.rule_content_hash,
            subject=self.context.actor_id,
        )
        evaluation = access.evaluate_actor_access_response(
            rule_lookup=lookup,
            event_ref=self.context.event_ref,
            event_time=self.context.event_time,
            subject=self.context.actor_id,
            request=request,
            conditioning_readset=self.conditioning.readset_refs,
            context=self.context,
            as_of=evaluated_as_of,
            material_eligible=self.material_eligible,
            eligible_material_refs=self.eligible_material_refs,
        )
        if evaluation.response.status in (
            ResponseStatus.REFUSED,
            ResponseStatus.HELD,
        ):
            refusal = {
                "schema": RUN_SCHEMA,
                "grade": GRADE,
                "native": False,
                "label": label,
                "refused": True,
                "committed": False,
                "reason": evaluation.response.reason,
                "response_status": evaluation.response.status.value,
                "target_proposals": 0,
                "target_state_rows": 0,
                "context": self.context.as_dict(),
                "source_binding": self._public_source_binding(),
                "private_custody_ref": "world.json",
                "c8": self.c8_binding,
                "request": {
                    "perception_receipt": dict(perception_receipt)
                    if isinstance(perception_receipt, Mapping)
                    else None,
                    "action_receipt": dict(action_receipt)
                    if isinstance(action_receipt, Mapping)
                    else None,
                    "contradictory_context": bool(contradictory_context),
                    "contradictory_refs": list(contradictory_refs),
                    "revoked_source_refs": sorted(revoked_source_refs),
                },
            }
            _write_json(run_dir / "run.json", refusal)
            return S35Run(
                label=label,
                run_dir=run_dir,
                committed=False,
                refused=True,
                refusal_reason=evaluation.response.reason,
                store_path=None,
                response=evaluation.response,
                decision=None,
                pipeline=None,
                receipt={},
                response_row_hash="",
                c9_receipt_hash="",
                target_state_rows=0,
                target_ids=(),
                context=self.context,
            )

        store_path = run_dir / "c9.sqlite"
        store = CandidateStore(store_path)
        expected = {
            "event_time": self.context.event_time,
            "conditioning_readset": self.conditioning.readset_refs,
            "material_eligible": self.material_eligible,
            "eligible_material_refs": self.eligible_material_refs,
            "actor_history_refs": tuple(enacted_history_refs),
            "other_person_offer_ref": other_person_offer_ref,
            "material_opportunity_ref": material_opportunity_ref,
            "prior_response_count": 0,
            "rule_lookup": lookup,
        }
        current = {
            "context": self.context,
            "request": request,
            "evaluation": evaluation,
            "expected": expected,
        }
        token = access.set_current_context(current)
        try:
            pipeline = run_candidate_path(
                store=store,
                actor_raw=self.actor_record,
                event_raw=self.e1_event,
                conditioning_sources=[self.conditioning_source],
                response_registry=self.response_registry,
                target_registry=TargetRuleRegistry.production(),
                authority_id=self.rule.authority_id,
                rule_version=self.rule.rule_version,
                rule_content_hash=self.rule.rule_content_hash,
                as_of=evaluated_as_of,
                permitted_issuer_refs=frozenset(),
                other_person_offer_ref=other_person_offer_ref,
                material_opportunity_ref=material_opportunity_ref,
                enacted_history_refs=tuple(enacted_history_refs),
                later_consumer=LaterActionConsumer(
                    READER_ID, "committed_target_state"
                ),
                later_as_of=self.producer.later_as_of,
                target_permission=None,
                action_owner_receipt=None,
                expected_act="",
            )
        finally:
            access.reset_current_context(token)

        if pipeline.response is not evaluation.response:
            raise S35Refusal("S35_PIPELINE_RESPONSE_REPLACED")
        if (
            pipeline.decision is None
            or pipeline.decision.branch is not TargetBranch.NO_CHANGE
            or pipeline.decision.reason is not TargetReason.NO_PROPOSAL
            or pipeline.decision.target_id
        ):
            raise S35Refusal(
                "S35_TARGETLESS_DECISION_EXPECTED",
                str(getattr(pipeline.decision, "branch", "")),
            )
        target_ids = tuple(sorted(store.committed_target_ids()))
        if target_ids:
            raise S35Refusal("S35_TARGET_ROWS_PRESENT", ",".join(target_ids))
        if pipeline.response.target_proposals:
            raise S35Refusal("S35_TARGET_PROPOSALS_PRESENT")
        if pipeline.receipt is None or not pipeline.receipt.committed:
            raise S35Refusal("S35_C9_NOT_COMMITTED")
        receipt = evaluation.receipt
        if not receipt or not access.valid(dict(receipt)):
            raise S35Refusal("S35_RECEIPT_INTEGRITY_FAILURE")
        if receipt["hash"] != pipeline.response.receipt_hash:
            raise S35Refusal("S35_RECEIPT_BINDING_MISMATCH")
        _write_json(run_dir / "s35_receipt.json", dict(receipt))
        run = S35Run(
            label=label,
            run_dir=run_dir,
            committed=True,
            refused=False,
            refusal_reason="",
            store_path=store_path,
            response=pipeline.response,
            decision=pipeline.decision,
            pipeline=pipeline,
            receipt=receipt,
            response_row_hash=pipeline.receipt.response_ref,
            c9_receipt_hash=pipeline.receipt.receipt_hash,
            target_state_rows=len(target_ids),
            target_ids=target_ids,
            context=self.context,
        )
        episode_body = {
            "schema": "SOROK_S35_C12_ACCESS_BINDING@2",
            "grade": GRADE,
            "native": False,
            "label": label,
            "source_binding": self._public_source_binding(),
            "private_custody_ref": "world.json",
            "c8": self.c8_binding,
            "context": self.context.as_dict(),
            "s35_receipt": dict(receipt),
            "s35_receipt_hash": receipt["hash"],
            "response_ref": pipeline.receipt.response_ref,
            "c9_receipt_hash": pipeline.receipt.receipt_hash,
            "outcome": pipeline.response.reason,
            "target_branch": pipeline.decision.branch.value,
            "target_reason": pipeline.decision.reason.value,
            "target_id": "",
            "target_proposals": 0,
        }
        episode = self.c12.append_episode(
            self.context.branch_id,
            actor_id="A",
            kind="S35_ACCESS_RESPONSE",
            clock=self.context.clock,
            body=episode_body,
        )
        summary = {
            "schema": RUN_SCHEMA,
            "grade": GRADE,
            "native": False,
            "label": label,
            "refused": False,
            "committed": True,
            "outcome": pipeline.response.reason,
            "response_status": pipeline.response.status.value,
            "response_receipt_hash": pipeline.response.receipt_hash,
            "response_row_hash": pipeline.receipt.response_ref,
            "c9_receipt_hash": pipeline.receipt.receipt_hash,
            "target_branch": pipeline.decision.branch.value,
            "target_reason": pipeline.decision.reason.value,
            "target_id": pipeline.decision.target_id,
            "target_proposals": 0,
            "target_state_rows": len(target_ids),
            "context": self.context.as_dict(),
            "source_binding": self._public_source_binding(),
            "private_custody_ref": "world.json",
            "c8": self.c8_binding,
            "s35_receipt": dict(receipt),
            "s35_receipt_hash": receipt["hash"],
            "evidence_grade": receipt.get("evidence_grade"),
            "actual_actor_input": receipt.get("actual_actor_input"),
            "qualification": receipt.get("qualification"),
            "hold_reason": receipt.get("hold_reason"),
            "c12_episode": episode,
            "c12_episode_hash": episode["hash"],
            "request": {
                "perception_receipt": dict(perception_receipt)
                if isinstance(perception_receipt, Mapping)
                else None,
                "action_receipt": dict(action_receipt)
                if isinstance(action_receipt, Mapping)
                else None,
                "contradictory_context": bool(contradictory_context),
                "contradictory_refs": list(contradictory_refs),
                "revoked_source_refs": sorted(revoked_source_refs),
            },
        }
        _write_json(run_dir / "run.json", summary)
        store.close()
        return run

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self.producer.close()
        finally:
            self.c12.close()


__all__ = [
    "GRADE",
    "RULE_AUTHORITY",
    "RULE_CONTENT_HASH",
    "RULE_ID",
    "RULE_ISSUER",
    "RULE_VERSION",
    "RUN_SCHEMA",
    "S35Refusal",
    "S35Run",
    "S35World",
    "WORLD_SCHEMA",
]
