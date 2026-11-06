"""The joined BP3 -> BP1 -> C9R source-free producer.

One whole causal chain, executed as separable stages so every source edge can be
cut and restored:

    BP1 actor/world occurrence
      -> BP3 keyed exclusive append (C8 occurrence + proof + external anchor)
      -> accepted OUT9 read-only consumer read (actual committed readset)
      -> C9R actor ingress + E1 event witness (same occurrence id, actor id,
         source owner, clock and BP1 causal parents)
      -> TEST_ONLY CAN008 RULE_A response
      -> separately owned TEST_ONLY CAN011 RULE_T + grant
      -> durable SQLite full-record commit
      -> cold later read by a named consumer
      -> independently performed TEST_ONLY E2 admission

No upstream engine is re-implemented. The only new code is the adapter that
binds the three exact sources together and the native-ready ports it receives
them through.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp1.composer import build_two_actor_life  # noqa: E402
from bp1.ledger import verify_snapshot  # noqa: E402
TEST_ONLY_NS = "TEST_ONLY_"

from . import binding, ports  # noqa: E402
from .binding import (  # noqa: E402
    Out9Binding,
    WorldOccurrence,
    build_world_occurrence,
    commit_world_occurrence,
    e1_content,
    read_out9,
    verify_out9_against_source,
)

RULE_A_ISSUER = "TEST_ONLY_BP2_CAN008_RULE_A_ISSUER"
TARGET_OWNER = "TEST_ONLY_BP2_CAN011_TARGET_OWNER"
GRANT_ISSUER = "TEST_ONLY_BP2_CAN011_GRANT_ISSUER"
E2_OWNER = "TEST_ONLY_BP2_E2_OWNER"
ACTUATOR = "TEST_ONLY_ACTUATOR_BP2_INDEPENDENT"
OCCURRENCE_E2 = "TEST_ONLY_OCCURRENCE_BP2_E2"
READER_ID = "TEST_ONLY_BP2_LATER_E2_READER"
EVENT_OWNER = "TEST_ONLY_BP2_E1_EVENT_OWNER"
SCENE = binding.SCENE
EXPECTED_ACT = "inspect_with_tool"

STAGES = (
    "world_occurrence",
    "c8_exclusive_append",
    "out9_read",
    "e1_binding",
    "c9_commit",
    "later_e2",
)

SEVER_CODES = {
    "C8_PROOF_WITHHELD": "PROOF_VERIFIER_REQUIRED",
    "BP1_ACTOR_SWAPPED": "ACTOR_ROLE_NOT_FOCAL",
    "BP1_OTHER_SELF_OFFER": "OTHER_OFFER_NOT_DISTINCT",
    "RULE_A_WITHHELD": "CAN008_RULE_A_UNISSUED",
    "RULE_A_REGISTRY_EMPTY": "NO_PROPOSAL",
    "RULE_T_GRANT_WITHHELD": "CAN011_TARGET_GRANT_UNISSUED",
    "RULE_T_SELF_ISSUED": "PERMISSION_SELF_ISSUED",
    "TARGET_RECORD_MUTATED": "CONSUMER_READSET_MISMATCH",
    "E2_SELF_ACTUATOR": "E2_ACTUATOR_SELF_BOUND",
    "E2_ACTION_BEFORE_COMMIT": "RESOURCE_NOT_YET_EFFECTIVE",
}


class JoinedRefusal(ValueError):
    """A joined stage refused. Carries the exact stage and code."""

    def __init__(self, stage: str, code: str, detail: str = "") -> None:
        super().__init__(f"{stage}:{code}" if not detail else f"{stage}:{code}: {detail}")
        self.stage = stage
        self.code = code
        self.detail = detail


# ---------------------------------------------------------------------------
# root / keystore / journal plumbing
# ---------------------------------------------------------------------------
@dataclass
class JournalEnv:
    root: Path
    journal: Any
    anchor: Any
    key_store: Any
    capability: Any
    key_path: Path
    journal_path: Path

    def summary(self) -> dict:
        return {
            "journal_path": str(self.journal_path),
            "journal_id": self.journal.journal_id,
            "effective_clock_source": "BP2_TEST_ONLY_LOGICAL_CLOCK",
            "key_path": str(self.key_path),
            "key_id": self.key_store.key_id,
            "anchor_log": str(self.anchor.log_path),
            "anchor_watermark": str(self.anchor.watermark_path),
            "key_custody": "TEST_ONLY_EXTERNAL_KEY_FILE_NOT_PRODUCTION_KMS",
            "anchor_grade": self.anchor.grade,
        }


def prepare_journal_env(root: Path, *, writer_id: str = "bp2-writer",
                        clock=None) -> JournalEnv:
    """Create the TEST_ONLY external key store, anchor and keyed journal.

    ``clock`` defaults to the BP3 test-only OS clock. The joined producer passes
    an explicit source-free logical clock so the committed envelope identity is
    reproducible; this is a declared fixture clock, NOT a trusted time source.
    """
    import base64

    import c8_exclusive_writer as writer

    root = Path(root)
    journal_dir = root / "journal"
    journal_dir.mkdir(parents=True, exist_ok=True)
    key_dir = root / "keys"
    key_dir.mkdir(parents=True, exist_ok=True)
    key_path = key_dir / "writer_keys.json"
    if not key_path.exists():
        key = os.urandom(32)
        key_path.write_text(
            json.dumps({"key_id": "BP2-TEST-KEY",
                        "key_b64": base64.b64encode(key).decode("utf8")}),
            encoding="utf8",
        )
    key_store = writer.WriterKeyStore.load(key_path, "BP2-TEST-KEY")
    anchor = writer.KeyedMonotonicAnchor(
        root / "anchor" / "rows.json",
        root / "anchor" / "watermark.json",
        key_store,
    )
    journal_path = journal_dir / "journal.json"
    journal = writer.ExclusiveJournal(
        journal_path, store=key_store, anchor=anchor)
    if clock is not None:
        # The accepted C8O base class exposes ``clock`` as an injectable
        # constructor hook; BP3's subclass does not forward it, so the same
        # attribute the base class already uses is set on the instance. The
        # upstream bytes are untouched.
        journal.clock = clock
    capability = writer.KeyedCapability.issue(
        key_store, journal.journal_id, writer_id, ttl_seconds=3600)
    # Deterministic TEST_ONLY capability nonce so the committed envelope identity
    # is reproducible across processes. Re-signed with BP3's own HMAC domain;
    # this is a fixture nonce, not a production credential.
    import hashlib
    from dataclasses import replace

    nonce = hashlib.sha256(
        f"{journal.journal_id}:{writer_id}".encode("utf8")).hexdigest()[:32]
    capability = replace(capability, nonce=nonce)
    capability = replace(
        capability,
        signature=writer._mac(key_store.key, capability._body()),
    )
    return JournalEnv(
        root=root, journal=journal, anchor=anchor,
        key_store=key_store, capability=capability, key_path=key_path,
        journal_path=journal_path,
    )


# ---------------------------------------------------------------------------
# TEST_ONLY resources presented through the native-ready ports
# ---------------------------------------------------------------------------
def rule_a_semantics(actor_id: str) -> dict:
    return {
        "rule_id": "TEST_ONLY_BP2_CAN008_RULE_A",
        "rule_version": "1",
        "authority_id": "TEST_ONLY_CAN008",
        "authority_version": "1",
        "allowed_subjects": [actor_id],
        "permitted_readset_classes": ["ResolvedStructuralContext"],
        "predicates": [
            "two distinct declared enacted acts",
            "independent other offer",
            "material access",
        ],
        "native": False,
    }


def target_semantics(rule_a_hash: str) -> dict:
    return {
        "rule_id": "TEST_ONLY_BP2_CAN011_RULE_T",
        "rule_version": "1",
        "authority_id": "TEST_ONLY_CAN011",
        "authority_version": "1",
        "response_rule_content_hash": rule_a_hash,
        "state_kind_id": "V3MS_PRACTICE",
        "allowed_operations": ["CREATE"],
        "accepted_semantic_objects": ["c9p:coordinated_material_inspection"],
        "native": False,
    }


def make_rule_a(occurrence: WorldOccurrence, *, as_of: int,
                effective_from: int | None = None):
    semantics = rule_a_semantics(occurrence.actor_id)
    content_hash = digest(semantics)
    body = {
        "schema": "BP2_CAN008_RULE_A@1",
        "issuer_ref": RULE_A_ISSUER,
        "issuer_verified": True,
        "grade": ports.TEST_ONLY_GRADE,
        "rule_content_hash": content_hash,
        "rule_semantics": semantics,
        "native_claim": False,
    }
    return ports.test_only_rule_resource(
        resource_id="TEST_ONLY_BP2_CAN008_RULE_A_RESOURCE",
        version="1",
        body=body,
        issuer_ref=RULE_A_ISSUER,
        source_owner="TEST_ONLY_CAN008_ISSUING_OFFICE",
        permission_ref="TEST_ONLY_BP2_RULE_A_SCOPE",
        effective_from=as_of if effective_from is None else effective_from,
        readset_refs=("ResolvedStructuralContext",),
        currentness_as_of=as_of,
    )


def make_target_rule(occurrence: WorldOccurrence, rule_a_content_hash: str, *,
                     as_of: int):
    """Build the separate CAN011 RULE_T resource.

    C9R's accepted contract links a target update to the CAN008 response-rule
    content hash (``TargetRule.rule_content_hash`` and the proposal's
    ``source_update_rule_ref``). The RULE_T's own identity is therefore carried
    as its own ``rule_t_content_hash`` and as its exact ``rule_id`` inside the
    sealed authorization preimage, not by overwriting C9R's dependency field.
    """
    semantics = target_semantics(rule_a_content_hash)
    content_hash = digest(semantics)
    body = {
        "schema": "BP2_CAN011_RULE_T@1",
        "issuer_ref": TARGET_OWNER,
        "issuer_verified": True,
        "grade": ports.TEST_ONLY_GRADE,
        "rule_content_hash": rule_a_content_hash,
        "rule_t_content_hash": content_hash,
        "rule_semantics": semantics,
        "native_claim": False,
    }
    return ports.test_only_rule_resource(
        resource_id="TEST_ONLY_BP2_CAN011_RULE_T_RESOURCE",
        version="1",
        body=body,
        issuer_ref=TARGET_OWNER,
        source_owner="TEST_ONLY_CAN011_TARGET_OFFICE",
        permission_ref="TEST_ONLY_BP2_RULE_T_SCOPE",
        effective_from=as_of,
        readset_refs=("V3MS_PRACTICE",),
        currentness_as_of=as_of,
    )


def make_target_grant(*, occurrence: WorldOccurrence, rule_t, response_hash: str,
                      before_target_hash: str, as_of: int, revoked: bool = False):
    body = {
        "schema": "BP2_CAN011_TARGET_GRANT@1",
        "grant_id": "TEST_ONLY_BP2_TARGET_GRANT",
        "actor_id": occurrence.actor_id,
        "rule_content_hash": dict(rule_t.body)["rule_content_hash"],
        "rule_t_content_hash": dict(rule_t.body)["rule_t_content_hash"],
        "response_hash": response_hash,
        "before_target_hash": before_target_hash,
        "issued_at": as_of - 1,
        "expires_at": None,
        "revoked": revoked,
        "grade": ports.TEST_ONLY_GRADE,
        "native_claim": False,
    }
    return ports.test_only_rule_resource(
        resource_id="TEST_ONLY_BP2_CAN011_TARGET_GRANT_RESOURCE",
        version="1",
        body=body,
        issuer_ref=GRANT_ISSUER,
        source_owner="TEST_ONLY_CAN011_GRANT_OFFICE",
        permission_ref="TEST_ONLY_BP2_GRANT_SCOPE",
        effective_from=as_of - 1,
        readset_refs=(response_hash, before_target_hash),
        currentness_as_of=as_of,
        revoked=revoked,
    )


def make_conditioning_source(occurrence: WorldOccurrence, *, as_of: int,
                             access: str = "granted"):
    from candidate import make_conditioning_source as c9_make_source

    snapshot = occurrence.actor_snapshot
    return c9_make_source(
        source_ref=TEST_ONLY_NS + "BP2_MATERIAL_" + occurrence.actor_key,
        source_class="ResolvedStructuralContext",
        subject=occurrence.actor_id,
        body={
            "access": access,
            "as_of": occurrence.event_time,
            "scene": SCENE,
            "material_remaining": snapshot["state"].get("material_remaining"),
            "cash": snapshot["state"].get("cash"),
            "completed_units": snapshot["state"].get("completed_units"),
            "material_ref": occurrence.material_ref,
            "source_grade": ports.TEST_ONLY_GRADE,
            "native_grant": ports.NATIVE_GRANT_NOT_GRANTED,
            "as_of_frame": as_of,
        },
    )


def make_actor_record(occurrence: WorldOccurrence, snapshot: Mapping[str, Any],
                      *, actor_id: str | None = None,
                      source_ref: str | None = None):
    from candidate import ActorIdentityRecord

    accepted, reason = verify_snapshot(snapshot, expected_hash=snapshot["hash"])
    if not accepted:
        raise JoinedRefusal("e1_binding", "BP1_ACTOR_SNAPSHOT_NOT_AUTHENTICATED",
                            str(reason))
    return ActorIdentityRecord(
        actor_id=occurrence.actor_id if actor_id is None else actor_id,
        activation_status="ACTIVE",
        standing_state=snapshot["state_hash"],
        currentness_as_of=int(snapshot["last_clock"]),
        source_ref=occurrence.actor_source_ref if source_ref is None else source_ref,
        source_hash=snapshot["hash"],
    ).sealed()


def make_e1_event(occurrence: WorldOccurrence, out9: Out9Binding, e1,
                  *, time: int):
    from candidate import make_event_witness

    content = e1_content(occurrence, out9, e1)
    return make_event_witness(
        event_id=TEST_ONLY_NS + "BP2_E1_" + out9.occurrence_id,
        owner_ref=EVENT_OWNER,
        time=time,
        content=content,
        actor_role=occurrence.actor_id,
        causal_parent_refs=(),
    )


def make_e2_resource(*, occurrence: WorldOccurrence, consumed_state_hash: str,
                     action_time: int, target_commit_time: int,
                     actuator_ref: str = ACTUATOR,
                     occurrence_ref: str = OCCURRENCE_E2):
    from candidate import make_performed_action_receipt

    sealed = make_performed_action_receipt(
        actor_id=occurrence.actor_id,
        act=EXPECTED_ACT,
        actuator_ref=actuator_ref,
        occurrence_ref=occurrence_ref,
        action_time=action_time,
        consumed_state_hash=consumed_state_hash,
        target_commit_time=target_commit_time,
    )
    return ports.test_only_rule_resource(
        resource_id="TEST_ONLY_BP2_E2_OWNER_RECEIPT",
        version="1",
        body=sealed,
        issuer_ref=E2_OWNER,
        source_owner="TEST_ONLY_BP2_E2_OWNER_OFFICE",
        permission_ref="TEST_ONLY_BP2_E2_SCOPE",
        effective_from=target_commit_time,
        readset_refs=(consumed_state_hash,),
        currentness_as_of=action_time,
    )


# ---------------------------------------------------------------------------
# outcome
# ---------------------------------------------------------------------------
@dataclass
class JoinedOutcome:
    """Everything the joined chain actually produced, with typed failure."""

    ok: bool
    stage_reached: str
    failure_code: str = ""
    failure_detail: str = ""
    receipts: dict = field(default_factory=dict)

    def receipt(self) -> dict:
        return {
            "schema": "BP2_JOINED_CHAIN_RECEIPT@1",
            "ok": self.ok,
            "stage_reached": self.stage_reached,
            "failure_code": self.failure_code,
            "failure_detail": self.failure_detail,
            **self.receipts,
        }


def joined_consumer_assertion(outcome: JoinedOutcome) -> None:
    """THE named downstream joined-consumer assertion.

    Every severance trial in this return must redden this exact function and
    return to passing when the cut edge is restored. It asserts the whole causal
    identity, not a local stage success.
    """
    if not outcome.ok:
        raise AssertionError(
            "JOINED_CONSUMER_POSITIVE: chain refused at stage "
            f"{outcome.stage_reached} with {outcome.failure_code}"
        )
    r = outcome.receipts
    string_fields = (
        "c8_occurrence_id", "out9_occurrence_id", "c8_state_digest",
        "out9_state_digest", "actor_source_hash", "actor_standing_state",
        "actor_id", "other_actor_id", "other_source_hash", "performed_act_ref",
        "other_act_ref", "declared_offer_ref", "rule_a_content_hash",
        "rule_t_content_hash", "grant_hash", "response_hash",
        "target_record_hash", "consumed_state_hash", "computed_state_digest",
        "target_branch", "adp019_admission_receipt", "e2_actuator_ref",
        "e2_occurrence_ref", "e2_consumed_state_hash",
    )
    for name in string_fields:
        value = r.get(name)
        if not isinstance(value, str) or not value:
            raise AssertionError(f"JOINED_CONSUMER_POSITIVE: missing {name}")
    if r["c8_occurrence_id"] != r["out9_occurrence_id"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: OUT9 read a different occurrence")
    if r["c8_state_digest"] != r["out9_state_digest"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: OUT9 readset diverges from commit")
    if r["computed_state_digest"] != r["consumed_state_hash"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: E2 consumed a different target")
    if r["e2_consumed_state_hash"] != r["consumed_state_hash"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: E2 receipt consumed different state")
    if r["target_record_hash"] != r.get("linearized_record_hash"):
        raise AssertionError("JOINED_CONSUMER_POSITIVE: later read saw a different record")
    if r["creation_rule_ref"] != r["rule_t_dependency_hash"]:
        raise AssertionError(
            "JOINED_CONSUMER_POSITIVE: durable record lost the RULE_A/RULE_T link")
    if r["target_branch"] != "CREATE":
        raise AssertionError("JOINED_CONSUMER_POSITIVE: no durable CREATE target")
    if r.get("e2_admitted") is not True:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: later E2 not independently admitted")
    if r.get("e2_self_performed") is not False:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: E2 was not independently performed")
    if r["e2_actuator_ref"] == r["actor_id"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: actor performed its own E2")
    if r["other_act_ref"] == r["performed_act_ref"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: no genuinely other performed act")
    if r["declared_offer_ref"] != r["other_act_ref"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: response used a non-other offer")
    if r["actor_source_hash"] == r["other_source_hash"]:
        raise AssertionError("JOINED_CONSUMER_POSITIVE: the two actor histories collapsed")
    if r["adp019_admission_receipt"] != "ADP019_ADMISSION_RECEIPT_ABSENT":
        raise AssertionError("JOINED_CONSUMER_POSITIVE: ADP019 was self-issued")
    if r.get("native_claims"):
        raise AssertionError("JOINED_CONSUMER_POSITIVE: unauthorized native claim")
    if r.get("psychology_claims"):
        raise AssertionError("JOINED_CONSUMER_POSITIVE: fabricated psychology")


# ---------------------------------------------------------------------------
# the producer
# ---------------------------------------------------------------------------
class JoinedProducer:
    """Staged joined producer over one root directory."""

    def __init__(self, root, *, actor: str = "A", as_of_offset: int = 5,
                 later_offset: int = 10) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.actor_key = actor
        self.as_of_offset = as_of_offset
        self.later_offset = later_offset
        self.clock = {"value": 0}
        self.env = prepare_journal_env(
            self.root,
            clock=lambda: {
                "source": "BP2_TEST_ONLY_LOGICAL_CLOCK",
                "value": str(self.clock["value"]),
            },
        )
        from candidate import CandidateStore

        self.c9 = CandidateStore(self.root / "c9.sqlite")
        self.life = None
        self.occurrence = None
        self.commit = None
        self.out9 = None
        self.e1 = None
        self.pipeline = None
        self.actor_record = None
        self.e1_event = None
        self.conditioning = None
        self.response_rule = None
        self.rule_a = None
        self.rule_t = None
        self.target_rule_obj = None
        self.grant = None
        self.response_hash = ""
        self.reader = None
        self.later_read = None
        self.e2 = None
        self.e2_resource = None
        self.stage = "world_occurrence"

    # -- lifecycle -------------------------------------------------------
    def close(self) -> None:
        try:
            self.c9.close()
        except Exception:  # noqa: BLE001 - closing must not mask a refusal
            pass

    def __enter__(self) -> "JoinedProducer":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    @property
    def event_time(self) -> int:
        return self.occurrence.event_time

    @property
    def as_of(self) -> int:
        return self.occurrence.event_time + self.as_of_offset

    @property
    def later_as_of(self) -> int:
        return self.as_of + self.later_offset

    # -- stage 1: BP1 world occurrence -----------------------------------
    def stage_world(self) -> WorldOccurrence:
        self.stage = "world_occurrence"
        self.life = build_two_actor_life()
        self.occurrence = build_world_occurrence(self.life, actor=self.actor_key)
        self.clock["value"] = self.occurrence.event_time
        return self.occurrence

    # -- stage 2: BP3 keyed exclusive append -----------------------------
    def stage_c8(self):
        self.stage = "c8_exclusive_append"
        if self.occurrence is None:
            self.stage_world()
        self.commit = commit_world_occurrence(
            self.env.journal, self.env.capability, self.occurrence)
        return self.commit

    # -- stage 3: OUT9 read ----------------------------------------------
    def stage_out9(self, *, proof_verifier="default") -> Out9Binding:
        self.stage = "out9_read"
        if self.commit is None:
            raise JoinedRefusal("out9_read", "C8_NOT_COMMITTED")
        if proof_verifier == "default":
            proof_verifier = self.env.journal.verify_journal
        try:
            self.out9 = read_out9(
                journal_path=self.env.journal_path,
                expected_state_digest=self.commit.state_digest,
                expected_occurrence_id=self.commit.occurrence_id,
                proof_verifier=proof_verifier,
            )
        except Exception as error:  # typed upstream refusal
            raise JoinedRefusal("out9_read", _upstream_code(error), str(error)) from error
        verify_out9_against_source(self.out9, self.commit, self.occurrence)
        return self.out9

    # -- stage 4/5: C9R E1 -> RULE_A -> RULE_T -> commit -------------------
    def stage_c9(self, *, actor_snapshot=None, actor_identity=None,
                 rule_a="default", rule_a_registry="default",
                 target_rule="default", grant="default",
                 other_offer_ref=None, material_access="granted",
                 self_issued: bool = False, enacted_override=None) -> Any:
        from candidate import (
            LaterActionConsumer,
            ResponseRule,
            ResponseRuleRegistry,
            TargetRule,
            TargetRuleRegistry,
            bind_conditioning,
            evaluate_response,
            lookup_rule,
            make_target_permission,
        )
        from candidate.pipeline import run_candidate_path

        self.stage = "e1_binding"
        if self.out9 is None:
            raise JoinedRefusal("e1_binding", "OUT9_NOT_READ")
        occurrence = self.occurrence
        snapshot = occurrence.actor_snapshot if actor_snapshot is None else actor_snapshot
        if actor_identity is None:
            actor_id, source_ref = occurrence.actor_id, occurrence.actor_source_ref
        elif actor_identity == "B":
            actor_id, source_ref = occurrence.other_id, occurrence.other_source_ref
        else:
            raise JoinedRefusal("e1_binding", "ACTOR_IDENTITY_UNKNOWN")
        self.actor_record = make_actor_record(
            occurrence, snapshot, actor_id=actor_id, source_ref=source_ref)
        self.e1 = ports.ADP019EventPort().bind_test_only_e1(
            occurrence={"occurrence_id": self.out9.occurrence_id,
                        "identity_digest": self.out9.event.get("identity_digest"),
                        "_state_digest": self.out9.readset["state_digest"],
                        "_commit_receipt_id": self.out9.readset["commit_receipt_id"],
                        "_writer_version": self.out9.readset["writer_version"]},
            event_time=self.event_time,
            verified_proof=self.out9.verified_proof,
        )
        self.e1_event = make_e1_event(occurrence, self.out9, self.e1,
                                      time=self.event_time)

        # ---- RULE_A resource through the CAN008 port ----
        if rule_a == "withheld":
            rule_a = None
        elif rule_a == "default":
            rule_a = make_rule_a(occurrence, as_of=self.event_time)
        can008 = ports.CAN008RulePort()
        rule_a = can008.bind(
            rule=rule_a,
            subject=occurrence.actor_id,
            conditioning_class="ResolvedStructuralContext",
            now=self.as_of,
        )
        self.rule_a = rule_a
        semantics = dict(rule_a.body)["rule_semantics"]
        rule_content_hash = dict(rule_a.body)["rule_content_hash"]
        self.response_rule = ResponseRule(
            str(semantics["rule_id"]),
            str(semantics["rule_version"]),
            rule_content_hash,
            str(semantics["authority_id"]),
            str(semantics["authority_version"]),
            RULE_A_ISSUER,
            True,
            tuple(semantics["allowed_subjects"]),
            tuple(semantics["permitted_readset_classes"]),
            ports.TEST_ONLY_GRADE,
            tuple(semantics["predicates"]),
        )
        if rule_a_registry == "empty":
            response_registry = ResponseRuleRegistry.production()
        elif rule_a_registry == "default":
            response_registry = ResponseRuleRegistry.test_only((self.response_rule,))
        else:
            response_registry = rule_a_registry

        # ---- conditioning / history / offer refs ----
        if material_access not in {"granted", "denied"}:
            raise JoinedRefusal("e1_binding", "MATERIAL_ACCESS_INVALID")
        source = make_conditioning_source(occurrence, as_of=self.as_of,
                                          access=material_access)
        sources = [dict(source)]
        offer = occurrence.other_act_ref if other_offer_ref is None else other_offer_ref
        enacted = (self._history_refs(occurrence) if enacted_override is None
                   else tuple(enacted_override))
        before_target_hash = self.c9.target_state_hash()

        # ---- the response receipt hash that the grant must bind ----
        lookup = lookup_rule(
            response_registry,
            authority_id=self.response_rule.authority_id,
            rule_version=self.response_rule.rule_version,
            rule_content_hash=rule_content_hash,
            subject=occurrence.actor_id,
        )
        conditioning = bind_conditioning(
            subject=occurrence.actor_id, sources=sources, as_of=self.as_of)
        response = evaluate_response(
            rule_lookup=lookup,
            event_ref=self.e1_event["hash"],
            event_time=self.event_time,
            subject=occurrence.actor_id,
            conditioning_readset=conditioning.readset_refs,
            actor_history_refs=enacted,
            other_person_offer_ref=offer,
            material_opportunity_ref=source["source_ref"],
            prior_response_count=0,
            material_eligible=material_access == "granted",
            eligible_material_refs=(source["source_ref"],),
        )
        self.conditioning = conditioning
        self.response_hash = response.receipt_hash

        # ---- RULE_T + grant through the CAN011 port ----
        if target_rule == "withheld":
            target_rule = None
        elif target_rule == "default":
            target_rule = make_target_rule(
                occurrence, rule_content_hash, as_of=self.event_time)
        can011 = ports.CAN011TargetPort(response_owner=RULE_A_ISSUER)
        target_rule = can011.bind_rule(rule=target_rule, now=self.as_of)
        self.rule_t = target_rule
        t_semantics = dict(target_rule.body)["rule_semantics"]
        t_hash = dict(target_rule.body)["rule_t_content_hash"]
        t_dependency = dict(target_rule.body)["rule_content_hash"]
        self.target_rule_obj = TargetRule(
            str(t_semantics["rule_id"]) + "@" + t_hash,
            str(t_semantics["rule_version"]),
            t_dependency,
            str(t_semantics["authority_id"]),
            str(t_semantics["authority_version"]),
            TARGET_OWNER,
            True,
            str(t_semantics["state_kind_id"]),
            tuple(t_semantics["allowed_operations"]),
            tuple(t_semantics["accepted_semantic_objects"]),
            ports.TEST_ONLY_GRADE,
        )
        if grant == "withheld":
            grant = None
        elif grant == "revoked":
            grant = make_target_grant(
                occurrence=occurrence, rule_t=target_rule,
                response_hash=self.response_hash,
                before_target_hash=before_target_hash,
                as_of=self.event_time, revoked=True)
        elif grant == "default":
            grant = make_target_grant(
                occurrence=occurrence, rule_t=target_rule,
                response_hash=self.response_hash,
                before_target_hash=before_target_hash,
                as_of=self.event_time)
        self.grant = can011.bind_grant(
            grant=grant,
            rule=target_rule,
            actor_id=occurrence.actor_id,
            response_hash=self.response_hash,
            before_target_hash=before_target_hash,
            now=self.as_of,
        )
        target_permission = make_target_permission(
            grant_id="TEST_ONLY_BP2_TARGET_GRANT",
            issuer_ref=GRANT_ISSUER,
            actor_id=occurrence.actor_id,
            rule_content_hash=t_dependency,
            before_target_hash=before_target_hash,
            response_hash=self.response_hash,
            issued_at=self.event_time - 1,
        )

        # ---- the actual C9R candidate path ----
        self.stage = "c9_commit"
        self.reader = LaterActionConsumer(READER_ID, "committed_target_state")
        target_registry = TargetRuleRegistry.test_only((self.target_rule_obj,))
        try:
            self.pipeline = run_candidate_path(
                store=self.c9,
                actor_raw=self.actor_record,
                event_raw=self.e1_event,
                conditioning_sources=sources,
                response_registry=response_registry,
                target_registry=target_registry,
                authority_id=self.response_rule.authority_id,
                rule_version=self.response_rule.rule_version,
                rule_content_hash=rule_content_hash,
                as_of=self.as_of,
                permitted_issuer_refs=frozenset({GRANT_ISSUER}),
                other_person_offer_ref=offer,
                material_opportunity_ref=source["source_ref"],
                enacted_history_refs=enacted,
                later_consumer=self.reader,
                later_as_of=self.later_as_of,
                target_permission=target_permission,
                action_owner_receipt=None,
                expected_act=EXPECTED_ACT,
                request_is_self_issued=self_issued,
            )
        except Exception as error:  # typed upstream refusal
            raise JoinedRefusal("c9_commit", _upstream_code(error), str(error)) from error
        if not self.pipeline.committed:
            failed = next((stage for stage in self.pipeline.stages if not stage.ok), None)
            raise JoinedRefusal(
                "c9_commit",
                failed.reason if failed is not None else "C9_NOT_COMMITTED",
                failed.stage if failed is not None else "",
            )
        return self.pipeline

    # -- stage 6: independently performed later E2 ------------------------
    def stage_e2(self, *, actuator_ref: str = ACTUATOR,
                 occurrence_ref: str = OCCURRENCE_E2,
                 action_time: int | None = None,
                 consumed_state_hash: str | None = None,
                 target_commit_time: int | None = None) -> Any:
        from candidate import admit_performed_action, read_target_for_later_action

        self.stage = "later_e2"
        if self.pipeline is None or not getattr(self.pipeline, "committed", False):
            raise JoinedRefusal("later_e2", "TARGET_NOT_COMMITTED")
        decision = self.pipeline.decision
        if decision is None or decision.branch.value != "CREATE":
            raise JoinedRefusal(
                "later_e2",
                decision.reason.value if decision is not None else "NO_DECISION",
                "branch=" + (decision.branch.value if decision is not None else ""),
            )
        target_id = decision.target_id
        read = read_target_for_later_action(
            self.c9,
            consumer=self.reader,
            middle_state_id=target_id,
            as_of=self.later_as_of,
            commit_time=self.event_time,
            expected_actor_id=self.occurrence.actor_id,
            expected_act=EXPECTED_ACT,
        )
        self.later_read = read
        if read.status.value not in {"READ_OK", "ACTION_ADMISSION_HELD"}:
            raise JoinedRefusal("later_e2", read.status.value, read.reason)
        state_hash = read.state_hash if consumed_state_hash is None else consumed_state_hash
        time = self.later_as_of if action_time is None else action_time
        commit_time = self.event_time if target_commit_time is None else target_commit_time
        resource = make_e2_resource(
            occurrence=self.occurrence,
            consumed_state_hash=state_hash,
            action_time=time,
            target_commit_time=commit_time,
            actuator_ref=actuator_ref,
            occurrence_ref=occurrence_ref,
        )
        ports.E2OwnerPort().bind(
            receipt=resource,
            actor_id=self.occurrence.actor_id,
            act=EXPECTED_ACT,
            consumed_state_hash=state_hash,
            target_commit_time=commit_time,
            now=time,
        )
        admission = admit_performed_action(
            owner_receipt=dict(resource.body),
            expected_actor_id=self.occurrence.actor_id,
            expected_act=EXPECTED_ACT,
            consumed_state_hash=state_hash,
            as_of=time,
            target_commit_time=commit_time,
        )
        self.e2 = admission
        self.e2_resource = resource
        return admission

    # -- helpers ---------------------------------------------------------
    @staticmethod
    def _history_refs(occurrence: WorldOccurrence) -> tuple[str, ...]:
        life = occurrence.life
        ledger = life.a_ledger if occurrence.actor_key == "A" else life.b_ledger
        return tuple(
            event.event_id for event in ledger.events
            if event.kind in {"PRIOR_HISTORY", "PERFORMED_ACTION"}
        )

    def mutate_target_row(self) -> dict:
        """Deliberate physical mutation of the committed target row."""
        decision = self.pipeline.decision
        row = self.c9.db.execute(
            "SELECT body FROM target_state WHERE id=?", (decision.target_id,)
        ).fetchone()
        if row is None:
            raise JoinedRefusal("later_e2", "TARGET_ROW_ABSENT")
        self._target_row_backup = (decision.target_id, row[0])
        body = json.loads(row[0])
        # Cut the committed record's own sealed preimage: the outer row still
        # parses but no longer matches its record_hash.
        body["record_preimage"]["governed_payload"] = {
            "practice_label": "MUTATED_TARGET_ROW"}
        self.c9.db.execute(
            "UPDATE target_state SET body=? WHERE id=?",
            (json.dumps(body, sort_keys=True, separators=(",", ":")),
             decision.target_id),
        )
        self.c9.db.commit()
        return {"mutated_target_id": decision.target_id,
                "original_state_hash": digest(json.loads(self._target_row_backup[1]))}

    def restore_target_row(self) -> None:
        """Restore the exact committed bytes mutated by ``mutate_target_row``."""
        target_id, body = self._target_row_backup
        self.c9.db.execute(
            "UPDATE target_state SET body=? WHERE id=?", (body, target_id))
        self.c9.db.commit()

    # -- resume / restore ------------------------------------------------
    def resume(self) -> JoinedOutcome:
        """Continue from the committed C8 occurrence with the edge restored."""
        receipts: dict = {"native_claims": [], "psychology_claims": []}
        try:
            self.stage_out9()
            receipts["out9"] = self.out9.summary()
            pipeline = self.stage_c9()
            receipts["c9"] = _c9_summary(self, pipeline)
            e2 = self.stage_e2()
            receipts["e2"] = _e2_summary(self, e2)
            receipts.update(self._flat_receipts(pipeline, e2))
            return JoinedOutcome(ok=True, stage_reached="later_e2", receipts=receipts)
        except Exception as error:  # noqa: BLE001 - typed refusal surfaced
            code = getattr(error, "code", None) or _upstream_code(error)
            receipts.update(self._partial_receipts())
            return JoinedOutcome(
                ok=False,
                stage_reached=self.stage,
                failure_code=str(code),
                failure_detail=str(error),
                receipts=receipts,
            )

    def outcome_after_e2(self, e2=None) -> JoinedOutcome:
        """Build a positive outcome from the current committed state + E2."""
        admission = self.e2 if e2 is None else e2
        receipts: dict = {"native_claims": [], "psychology_claims": []}
        if self.pipeline is None or admission is None:
            receipts.update(self._partial_receipts())
            return JoinedOutcome(
                ok=False, stage_reached=self.stage,
                failure_code="NOT_COMMITTED", receipts=receipts,
            )
        receipts["c9"] = _c9_summary(self, self.pipeline)
        receipts["e2"] = _e2_summary(self, admission)
        receipts.update(self._flat_receipts(self.pipeline, admission))
        return JoinedOutcome(ok=True, stage_reached="later_e2", receipts=receipts)

    # -- whole chain ------------------------------------------------------
    def run(self, *, sever: str | None = None) -> JoinedOutcome:
        receipts: dict = {
            "native_claims": [],
            "psychology_claims": [],
        }
        try:
            occurrence = self.stage_world()
            receipts["world"] = occurrence.summary()
            receipts["bp1_ledger"] = {
                "actor_events": [e.kind for e in occurrence.life.a_ledger.events],
                "other_events": [e.kind for e in occurrence.life.b_ledger.events],
                "actor_state_hash": occurrence.actor_snapshot["state_hash"],
                "other_state_hash": occurrence.other_snapshot["state_hash"],
            }
            commit = self.stage_c8()
            receipts["c8"] = commit.summary()
            proof_verifier = (
                None if sever == "C8_PROOF_WITHHELD" else self.env.journal.verify_journal
            )
            self.stage_out9(proof_verifier=proof_verifier)
            receipts["out9"] = self.out9.summary()

            c9_kwargs: dict = {}
            if sever == "BP1_ACTOR_SWAPPED":
                c9_kwargs["actor_snapshot"] = occurrence.other_snapshot
                c9_kwargs["actor_identity"] = "B"
            elif sever == "BP1_OTHER_SELF_OFFER":
                c9_kwargs["other_offer_ref"] = occurrence.performed_act_ref
            elif sever == "RULE_A_WITHHELD":
                c9_kwargs["rule_a"] = "withheld"
            elif sever == "RULE_A_REGISTRY_EMPTY":
                c9_kwargs["rule_a_registry"] = "empty"
            elif sever == "RULE_T_GRANT_WITHHELD":
                c9_kwargs["grant"] = "withheld"
            elif sever == "RULE_T_SELF_ISSUED":
                c9_kwargs["self_issued"] = True
            pipeline = self.stage_c9(**c9_kwargs)
            receipts["c9"] = _c9_summary(self, pipeline)
            if sever == "TARGET_RECORD_MUTATED":
                receipts["target_mutation"] = self.mutate_target_row()
            e2_kwargs: dict = {}
            if sever == "E2_SELF_ACTUATOR":
                e2_kwargs["actuator_ref"] = occurrence.actor_id
            elif sever == "E2_ACTION_BEFORE_COMMIT":
                e2_kwargs["action_time"] = self.event_time - 1
            e2 = self.stage_e2(**e2_kwargs)
            receipts["e2"] = _e2_summary(self, e2)
            receipts.update(self._flat_receipts(pipeline, e2))
            return JoinedOutcome(ok=True, stage_reached="later_e2", receipts=receipts)
        except Exception as error:  # typed refusal -> RED outcome, never a claim
            code = getattr(error, "code", None) or _upstream_code(error)
            receipts.update(self._partial_receipts())
            return JoinedOutcome(
                ok=False,
                stage_reached=self.stage,
                failure_code=str(code),
                failure_detail=str(error),
                receipts=receipts,
            )

    def _partial_receipts(self) -> dict:
        """Best-effort identity fields even when the chain refused mid-way."""
        values: dict = {
            "c8_occurrence_id": self.commit.occurrence_id if self.commit else "",
            "c8_state_digest": self.commit.state_digest if self.commit else "",
            "out9_occurrence_id": self.out9.occurrence_id if self.out9 else "",
            "out9_state_digest": self.out9.readset["state_digest"] if self.out9 else "",
            "actor_id": self.occurrence.actor_id if self.occurrence else "",
            "other_actor_id": self.occurrence.other_id if self.occurrence else "",
            "actor_source_hash": self.occurrence.actor_source_hash
            if self.occurrence else "",
            "other_source_hash": self.occurrence.other_source_hash
            if self.occurrence else "",
            "actor_standing_state": self.occurrence.actor_snapshot["state_hash"]
            if self.occurrence else "",
            "performed_act_ref": self.occurrence.performed_act_ref
            if self.occurrence else "",
            "other_act_ref": self.occurrence.other_act_ref if self.occurrence else "",
            "declared_offer_ref": "",
            "rule_a_content_hash": "",
            "rule_t_content_hash": "",
            "grant_hash": "",
            "response_hash": self.response_hash,
            "target_branch": (self.pipeline.decision.branch.value
                              if self.pipeline and self.pipeline.decision else ""),
            "target_record_hash": (self.pipeline.decision.record_hash
                                   if self.pipeline and self.pipeline.decision else ""),
            "linearized_record_hash": "",
            "consumed_state_hash": (self.later_read.state_hash
                                    if self.later_read else ""),
            "computed_state_digest": "",
            "e2_admitted": False,
            "e2_self_performed": None,
            "e2_actuator_ref": "",
            "e2_occurrence_ref": "",
            "e2_consumed_state_hash": "",
            "adp019_admission_receipt": (self.e1.adp019_admission_receipt
                                         if self.e1 else ""),
        }
        if self.rule_a is not None:
            values["rule_a_content_hash"] = dict(self.rule_a.body)["rule_content_hash"]
        if self.rule_t is not None:
            values["rule_t_content_hash"] = dict(self.rule_t.body)["rule_t_content_hash"]
            values["rule_t_dependency_hash"] = dict(self.rule_t.body)["rule_content_hash"]
        if self.grant is not None:
            values["grant_hash"] = self.grant.content_hash
        if self.pipeline is not None and self.pipeline.response is not None:
            values["declared_offer_ref"] = self.pipeline.response.declared_offer_ref
        return values

    def _flat_receipts(self, pipeline, e2) -> dict:
        decision = pipeline.decision
        values = {
            "c8_occurrence_id": self.out9.occurrence_id,
            "c8_state_digest": self.out9.readset["state_digest"],
            "c8_commit_receipt_id": self.out9.readset["commit_receipt_id"],
            "c8_writer_version": self.out9.readset["writer_version"],
            "out9_occurrence_id": self.out9.occurrence_id,
            "out9_state_digest": self.out9.readset["state_digest"],
            "actor_id": self.occurrence.actor_id,
            "other_actor_id": self.occurrence.other_id,
            "actor_source_hash": self.occurrence.actor_source_hash,
            "other_source_hash": self.occurrence.other_source_hash,
            "actor_standing_state": self.occurrence.actor_snapshot["state_hash"],
            "performed_act_ref": self.occurrence.performed_act_ref,
            "other_act_ref": self.occurrence.other_act_ref,
            "declared_offer_ref": pipeline.response.declared_offer_ref
            if pipeline.response else "",
            "rule_a_content_hash": dict(self.rule_a.body)["rule_content_hash"],
            "rule_t_content_hash": dict(self.rule_t.body)["rule_t_content_hash"],
            "rule_t_dependency_hash": dict(self.rule_t.body)["rule_content_hash"],
            "grant_hash": self.grant.content_hash,
            "grant_id": self.grant.body.get("grant_id"),
            "response_hash": self.response_hash,
            "target_branch": decision.branch.value if decision else "",
            "target_reason": decision.reason.value if decision else "",
            "target_id": decision.target_id if decision else "",
            "target_record_hash": decision.record_hash if decision else "",
            "creation_rule_ref": (decision.record_body or {}).get("creation_rule_ref", "")
            if decision else "",
            "linearized_record_hash": (self.later_read.committed_record or {}).get(
                "record_hash", "") if self.later_read else "",
            "consumed_state_hash": self.later_read.state_hash if self.later_read else "",
            "computed_state_digest": _recompute_state_hash(self),
            "e2_admitted": bool(getattr(e2, "admitted", False)),
            "e2_self_performed": getattr(e2, "actuator_ref", "")
            == self.occurrence.actor_id,
            "e2_actuator_ref": getattr(e2, "actuator_ref", ""),
            "e2_occurrence_ref": getattr(e2, "occurrence_ref", ""),
            "e2_consumed_state_hash": getattr(e2, "consumed_state_hash", ""),
            "e2_receipt_hash": getattr(e2, "receipt_hash", ""),
            "adp019_admission_receipt": self.e1.adp019_admission_receipt,
            "persisted": {
                "root": str(self.root),
                "journal_path": str(self.env.journal_path),
                "journal_id": self.env.journal.journal_id,
                "c9_db_path": str(self.root / "c9.sqlite"),
                "c8_occurrence_id": self.out9.occurrence_id,
                "c8_state_digest": self.out9.readset["state_digest"],
                "c8_content_hash": self.out9.event.get("content_hash"),
                "c8_identity_digest": self.out9.event.get("identity_digest"),
                "c8_commit_receipt_id": self.out9.readset["commit_receipt_id"],
                "c8_writer_version": self.out9.readset["writer_version"],
                "c8_canonical_bytes_sha256": self.out9.canonical_bytes_sha256,
                "target_id": decision.target_id if decision else "",
                "target_record_hash": decision.record_hash if decision else "",
                "consumed_state_hash": self.later_read.state_hash
                if self.later_read else "",
                "event_time": self.event_time,
                "as_of": self.as_of,
                "later_as_of": self.later_as_of,
                "actor_id": self.occurrence.actor_id,
                "other_actor_id": self.occurrence.other_id,
                "actor_source_hash": self.occurrence.actor_source_hash,
                "other_source_hash": self.occurrence.other_source_hash,
                "actor_snapshot_hash": self.occurrence.actor_snapshot["hash"],
                "rule_a_content_hash": dict(self.rule_a.body)["rule_content_hash"],
                "rule_t_content_hash": dict(self.rule_t.body)["rule_t_content_hash"],
                "rule_t_dependency_hash": dict(self.rule_t.body)["rule_content_hash"],
                "grant_hash": self.grant.content_hash,
                "grant_id": self.grant.body.get("grant_id"),
                "response_hash": self.response_hash,
                "e1_event_id": self.e1_event["event_id"] if self.e1_event else "",
                "e1_event_hash": self.e1_event["hash"] if self.e1_event else "",
                "c9_commit_receipt_hash": pipeline.receipt.receipt_hash
                if pipeline.receipt else "",
                "c9_authorization_hash": decision.authorization_hash
                if decision else "",
                "e2_owner_receipt": dict(self.e2_resource.body)
                if self.e2_resource else {},
                "e2_owner_receipt_resource_hash": self.e2_resource.content_hash
                if self.e2_resource else "",
                "e2_receipt_hash": getattr(e2, "receipt_hash", ""),
                "expected_act": EXPECTED_ACT,
            },
            "c9_pipeline_stages": [
                {"stage": s.stage, "ok": s.ok, "reason": s.reason}
                for s in pipeline.stages
            ],
        }
        return values


def _recompute_state_hash(producer: JoinedProducer) -> str:
    if producer.pipeline is None or producer.pipeline.decision is None:
        return ""
    target_id = producer.pipeline.decision.target_id
    if not target_id:
        return ""
    record = producer.c9.read_target_state(target_id)
    if record is None:
        return ""
    return digest(dict(record))


def _c9_summary(producer: JoinedProducer, pipeline) -> dict:
    decision = pipeline.decision
    response = pipeline.response
    return {
        "committed": bool(pipeline.committed),
        "no_ghost": bool(pipeline.no_ghost),
        "target_branch": decision.branch.value if decision else "",
        "target_reason": decision.reason.value if decision else "",
        "target_id": decision.target_id if decision else "",
        "record_hash": decision.record_hash if decision else "",
        "proposal_hash": decision.proposal_hash if decision else "",
        "response_status": response.status.value if response else "",
        "response_reason": response.reason if response else "",
        "response_receipt_hash": response.receipt_hash if response else "",
        "declared_offer_ref": response.declared_offer_ref if response else "",
        "rule_lookup": response.rule_lookup.status.value if response else "",
        "material_eligible": pipeline.material_eligible,
        "material_reason": pipeline.material_reason,
        "actor_id": pipeline.actor.actor_id if pipeline.actor else "",
        "actor_source_grade": getattr(pipeline.actor, "source_grade", "")
        if pipeline.actor else "",
        "actor_readset": list(pipeline.actor.readset_refs) if pipeline.actor else [],
        "event_id": pipeline.event.event_id if pipeline.event else "",
        "event_hash": pipeline.event.event_hash if pipeline.event else "",
        "event_reason": pipeline.event.reason.value if pipeline.event else "",
        "conditioning_readset": list(pipeline.conditioning.readset_refs)
        if pipeline.conditioning else [],
        "stages": [
            {"stage": s.stage, "ok": s.ok, "reason": s.reason} for s in pipeline.stages
        ],
        "rule_a_content_hash": dict(producer.rule_a.body)["rule_content_hash"],
        "rule_t_content_hash": dict(producer.rule_t.body)["rule_t_content_hash"],
        "rule_t_dependency_hash": dict(producer.rule_t.body)["rule_content_hash"],
        "grant_hash": producer.grant.content_hash,
        "grant_id": producer.grant.body.get("grant_id"),
        "response_hash": producer.response_hash,
        "c8_occurrence_id": producer.out9.occurrence_id,
        "c8_state_digest": producer.out9.readset["state_digest"],
        "c8_commit_receipt_id": producer.out9.readset["commit_receipt_id"],
        "e1_adp019": producer.e1.as_dict(),
        "adp019_admission_receipt": producer.e1.adp019_admission_receipt,
        "later_read_status": pipeline.later_read.status.value
        if pipeline.later_read else "",
        "later_read_state_hash": pipeline.later_read.state_hash
        if pipeline.later_read else "",
    }


def _e2_summary(producer: JoinedProducer, e2) -> dict:
    return {
        "admitted": bool(getattr(e2, "admitted", False)),
        "status": getattr(getattr(e2, "status", None), "value", ""),
        "reason": getattr(getattr(e2, "reason", None), "value", str(e2)),
        "actuator_ref": getattr(e2, "actuator_ref", ""),
        "occurrence_ref": getattr(e2, "occurrence_ref", ""),
        "consumed_state_hash": getattr(e2, "consumed_state_hash", ""),
        "action_time": getattr(e2, "action_time", 0),
        "target_commit_time": getattr(e2, "target_commit_time", 0),
        "receipt_hash": getattr(e2, "receipt_hash", ""),
        "actor_id": getattr(e2, "actor_id", ""),
        "self_performed": getattr(e2, "actuator_ref", "") == producer.occurrence.actor_id,
        "later_read_status": producer.later_read.status.value
        if producer.later_read else "",
        "later_read_state_hash": producer.later_read.state_hash
        if producer.later_read else "",
        "later_read_receipt": producer.later_read.read_receipt_hash
        if producer.later_read else "",
        "later_read_record_hash": (producer.later_read.committed_record or {}).get(
            "record_hash", "") if producer.later_read else "",
    }


def _upstream_code(error: Exception) -> str:
    code = getattr(error, "code", None)
    if isinstance(code, str) and code:
        return code
    return type(error).__name__.upper()


__all__ = [
    "ACTUATOR",
    "E2_OWNER",
    "EVENT_OWNER",
    "EXPECTED_ACT",
    "GRANT_ISSUER",
    "JoinedOutcome",
    "JoinedProducer",
    "JoinedRefusal",
    "JournalEnv",
    "OCCURRENCE_E2",
    "READER_ID",
    "RULE_A_ISSUER",
    "SEVER_CODES",
    "STAGES",
    "TARGET_OWNER",
    "joined_consumer_assertion",
    "make_conditioning_source",
    "make_rule_a",
    "make_target_grant",
    "make_target_rule",
    "prepare_journal_env",
    "rule_a_semantics",
    "target_semantics",
]
