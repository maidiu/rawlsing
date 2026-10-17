#!/usr/bin/env python3
"""Bounded D1' hosting, reverse-dependency, invalidation, and replay adapter.

This module does not define mechanism rules, decide rule authority, or write a
world. It hosts exact references supplied by upstream owners and orchestrates
only direct derivation lineage plus determinant-scoped redrive. Any current
rule consequence is admitted only through the frozen R1 rule-authority binding
contract; R2 never infers, selects, or mints rule authority.
"""
from __future__ import annotations

from dataclasses import dataclass
import heapq
import re
from typing import Callable, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.sdtf_r4_mechanism_rule_authority_binding import (
    MechanismRuleAuthorityBinding,
    MechanismRuleIdentity,
    R4MechanismRuleAuthorityBindingError,
    require_current_rule_admission,
)

CONTRACT_ID = "SDTF_R4_D1_HOSTING_REPLAY_R1@2.0.0"
CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID = (
    "SDTF_R4_R2_CURRENT_RULE_ADMISSION_CONSERVATION_R1@1.0.0"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class D1HostingIntegrityError(ValueError):
    """Exact D1 hosting identity, lineage, or dependency closure is invalid."""


class D1ReplayParityError(AssertionError):
    """A deterministic replay receipt cannot be verified exactly."""


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise D1HostingIntegrityError(f"{name} must be a non-empty string")
    return value.strip()


def _hash(value: object, name: str) -> str:
    value = _text(value, name)
    if not SHA256_RE.fullmatch(value):
        raise D1HostingIntegrityError(f"{name} must be a lowercase sha256")
    return value


def _unique_refs(values: Iterable[ExactRef], name: str) -> tuple[ExactRef, ...]:
    refs = tuple(values)
    if any(not isinstance(ref, ExactRef) for ref in refs):
        raise D1HostingIntegrityError(f"{name} must contain ExactRef values")
    keys = [ref.key for ref in refs]
    if len(keys) != len(set(keys)):
        raise D1HostingIntegrityError(f"{name} must be exact and duplicate-free")
    return tuple(sorted(refs, key=lambda ref: ref.key))


@dataclass(frozen=True, order=True)
class D1Context:
    """Exact world/state/version/valid-time coordinates owned upstream."""

    world_id: str
    state_id: str
    state_version: str
    valid_time_id: str

    def __post_init__(self) -> None:
        for field in ("world_id", "state_id", "state_version", "valid_time_id"):
            object.__setattr__(self, field, _text(getattr(self, field), field))

    @property
    def key(self) -> tuple[str, str, str, str]:
        return (self.world_id, self.state_id, self.state_version, self.valid_time_id)

    def as_dict(self) -> dict[str, str]:
        return {
            "world_id": self.world_id,
            "state_id": self.state_id,
            "state_version": self.state_version,
            "valid_time_id": self.valid_time_id,
        }


@dataclass(frozen=True, order=True)
class D1FactPointer:
    """An exact existing fact reference plus the coordinates where it obtains."""

    fact_ref: ExactRef
    context: D1Context

    def __post_init__(self) -> None:
        if not isinstance(self.fact_ref, ExactRef):
            raise D1HostingIntegrityError("fact_ref must be ExactRef")
        if not isinstance(self.context, D1Context):
            raise D1HostingIntegrityError("context must be D1Context")

    def as_dict(self) -> dict[str, object]:
        return {"fact_ref": self.fact_ref.as_dict(), "context": self.context.as_dict()}


@dataclass(frozen=True, order=True)
class D1RuleApplicationRef:
    """Exact rule-application descriptor; R1 alone proves rule currentness."""

    rule_application_id: str
    rule_id: str
    rule_version: str
    rule_hash: str

    def __post_init__(self) -> None:
        for field in ("rule_application_id", "rule_id", "rule_version"):
            object.__setattr__(self, field, _text(getattr(self, field), field))
        object.__setattr__(self, "rule_hash", _hash(self.rule_hash, "rule_hash"))
        try:
            MechanismRuleIdentity(self.rule_id, self.rule_version, self.rule_hash)
        except R4MechanismRuleAuthorityBindingError as exc:
            raise D1HostingIntegrityError("rule application must carry an exact lawful R1 rule identity") from exc

    def semantic_projection(self) -> dict[str, object]:
        return {
            "contract_id": CONTRACT_ID,
            "admission_conservation_contract_id": CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID,
            "rule_application_id": self.rule_application_id,
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "rule_hash": self.rule_hash,
            "mechanism_rule_ref": self.mechanism_rule_ref.as_dict(),
        }

    @property
    def mechanism_rule_ref(self) -> ExactRef:
        """The exact canonical R1 mechanism-rule identity; no R2 re-kind is permitted."""
        return MechanismRuleIdentity(
            self.rule_id,
            self.rule_version,
            self.rule_hash,
        ).ref

    @property
    def exact_ref(self) -> ExactRef:
        content_hash = semantic_hash(self.semantic_projection())
        return ExactRef(
            kind="RULE_APPLICATION_RECORD",
            object_id=self.rule_application_id,
            content_hash=content_hash,
        )

    @property
    def key(self) -> str:
        return self.exact_ref.key


@dataclass(frozen=True)
class D1Evaluation:
    """Rule-engine result consumed by this adapter; no rule semantics are embedded."""

    supported: bool
    determinant_facts: tuple[D1FactPointer, ...]
    output_fact: D1FactPointer | None = None
    evidence_witness_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        facts = tuple(self.determinant_facts)
        if any(not isinstance(fact, D1FactPointer) for fact in facts):
            raise D1HostingIntegrityError("determinant_facts must contain D1FactPointer values")
        fact_keys = [fact.fact_ref.key for fact in facts]
        if len(fact_keys) != len(set(fact_keys)):
            raise D1HostingIntegrityError("determinant_facts must be exact and duplicate-free")
        if not facts:
            raise D1HostingIntegrityError("determinant_facts must remain non-empty for reverse dependency lineage")
        object.__setattr__(self, "determinant_facts", tuple(sorted(facts, key=lambda x: x.fact_ref.key)))
        object.__setattr__(
            self,
            "evidence_witness_refs",
            _unique_refs(self.evidence_witness_refs, "evidence_witness_refs"),
        )
        if self.supported and not isinstance(self.output_fact, D1FactPointer):
            raise D1HostingIntegrityError("supported evaluation requires exact output_fact")
        if not self.supported and self.output_fact is not None:
            raise D1HostingIntegrityError(
                "unsupported evaluation must close output, not synthesize an opposite fact"
            )


@dataclass(frozen=True)
class D1ApplicationRevision:
    application: D1RuleApplicationRef
    determinant_facts: tuple[D1FactPointer, ...]
    output_fact: D1FactPointer | None
    evidence_witness_refs: tuple[ExactRef, ...]
    status: str
    prior_revision_ref: ExactRef | None
    trigger_refs: tuple[ExactRef, ...]
    rule_authority_binding_ref: ExactRef | None
    current_rule_admission_ref: ExactRef | None

    def __post_init__(self) -> None:
        if self.status not in {"SUPPORTED_CURRENT", "CLOSED_UNSUPPORTED"}:
            raise D1HostingIntegrityError("application revision status invalid")
        for name in ("rule_authority_binding_ref", "current_rule_admission_ref"):
            value = getattr(self, name)
            if value is not None and not isinstance(value, ExactRef):
                raise D1HostingIntegrityError(f"{name} must be ExactRef or None")
        if self.status == "SUPPORTED_CURRENT":
            if self.output_fact is None:
                raise D1HostingIntegrityError("supported revision requires output_fact")
            if self.current_rule_admission_ref is None:
                raise D1HostingIntegrityError(
                    "SUPPORTED_CURRENT revision requires exact R1 current-rule admission proof"
                )
            if self.rule_authority_binding_ref != self.current_rule_admission_ref:
                raise D1HostingIntegrityError(
                    "current rule admission must conserve the exact R1 authority-binding identity"
                )
        if self.status == "CLOSED_UNSUPPORTED" and self.output_fact is not None:
            raise D1HostingIntegrityError("closed revision may not carry an opposite output")
        if (
            self.current_rule_admission_ref is not None
            and self.rule_authority_binding_ref != self.current_rule_admission_ref
        ):
            raise D1HostingIntegrityError(
                "current rule admission ref cannot diverge from consumed R1 authority binding"
            )

    def semantic_projection(self) -> dict[str, object]:
        return {
            "contract_id": CONTRACT_ID,
            "admission_conservation_contract_id": CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID,
            "application_ref": self.application.exact_ref.as_dict(),
            "mechanism_rule_ref": self.application.mechanism_rule_ref.as_dict(),
            "rule_application_id": self.application.rule_application_id,
            "rule_version": self.application.rule_version,
            "determinant_facts": [fact.as_dict() for fact in self.determinant_facts],
            "output_fact": None if self.output_fact is None else self.output_fact.as_dict(),
            "evidence_witness_refs": [ref.as_dict() for ref in self.evidence_witness_refs],
            "status": self.status,
            "prior_revision_ref": (
                None if self.prior_revision_ref is None else self.prior_revision_ref.as_dict()
            ),
            "trigger_refs": [ref.as_dict() for ref in self.trigger_refs],
            "rule_authority_binding_ref": (
                None
                if self.rule_authority_binding_ref is None
                else self.rule_authority_binding_ref.as_dict()
            ),
            "current_rule_admission_ref": (
                None
                if self.current_rule_admission_ref is None
                else self.current_rule_admission_ref.as_dict()
            ),
        }

    @property
    def exact_ref(self) -> ExactRef:
        content_hash = semantic_hash(self.semantic_projection())
        return ExactRef(
            kind="SDTF_R4_D1_RULE_APPLICATION_REVISION",
            object_id=f"{self.application.rule_application_id}:{content_hash[:24]}",
            content_hash=content_hash,
        )


@dataclass(frozen=True)
class D1ReplayStep:
    application_ref: ExactRef
    before_revision_ref: ExactRef
    after_revision_ref: ExactRef
    disposition: str
    changed_output_refs: tuple[ExactRef, ...]
    rule_authority_binding_ref: ExactRef | None
    current_rule_admission_ref: ExactRef | None

    def as_dict(self) -> dict[str, object]:
        return {
            "application_ref": self.application_ref.as_dict(),
            "before_revision_ref": self.before_revision_ref.as_dict(),
            "after_revision_ref": self.after_revision_ref.as_dict(),
            "disposition": self.disposition,
            "changed_output_refs": [ref.as_dict() for ref in self.changed_output_refs],
            "rule_authority_binding_ref": (
                None
                if self.rule_authority_binding_ref is None
                else self.rule_authority_binding_ref.as_dict()
            ),
            "current_rule_admission_ref": (
                None
                if self.current_rule_admission_ref is None
                else self.current_rule_admission_ref.as_dict()
            ),
        }


@dataclass(frozen=True)
class D1ReplayReceipt:
    trigger_refs: tuple[ExactRef, ...]
    before_current_output_refs: tuple[ExactRef, ...]
    after_current_output_refs: tuple[ExactRef, ...]
    steps: tuple[D1ReplayStep, ...]
    exact_affected_edges: tuple[tuple[str, str, str | None], ...]
    content_hash: str

    def semantic_projection(self) -> dict[str, object]:
        return {
            "contract_id": CONTRACT_ID,
            "admission_conservation_contract_id": CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID,
            "trigger_refs": [ref.as_dict() for ref in self.trigger_refs],
            "before_current_output_refs": [ref.as_dict() for ref in self.before_current_output_refs],
            "after_current_output_refs": [ref.as_dict() for ref in self.after_current_output_refs],
            "steps": [step.as_dict() for step in self.steps],
            "exact_affected_edges": [list(edge) for edge in self.exact_affected_edges],
        }

    @property
    def exact_ref(self) -> ExactRef:
        return ExactRef(
            kind="SDTF_R4_D1_REPLAY_RECEIPT",
            object_id=f"d1-redrive:{self.content_hash[:24]}",
            content_hash=self.content_hash,
        )

    def verify(self) -> None:
        if semantic_hash(self.semantic_projection()) != self.content_hash:
            raise D1ReplayParityError("D1 replay receipt semantic projection/hash mismatch")


Evaluator = Callable[[D1RuleApplicationRef, D1ApplicationRevision], D1Evaluation]
RuleAdmissionResolver = Callable[
    [D1RuleApplicationRef, D1ApplicationRevision],
    MechanismRuleAuthorityBinding | None,
]


def _require_exact_current_rule_admission(
    application: D1RuleApplicationRef,
    binding: MechanismRuleAuthorityBinding | None,
) -> MechanismRuleAuthorityBinding:
    if not isinstance(binding, MechanismRuleAuthorityBinding):
        raise D1HostingIntegrityError(
            "exact R1 MechanismRuleAuthorityBinding current-rule admission is required"
        )
    try:
        admitted = require_current_rule_admission(binding)
    except R4MechanismRuleAuthorityBindingError as exc:
        raise D1HostingIntegrityError(
            "exact R1 current-rule admission failed closed"
        ) from exc
    if admitted.rule_identity.ref != application.mechanism_rule_ref:
        raise D1HostingIntegrityError(
            "R1 admitted rule identity does not exactly match R2 rule application identity"
        )
    return admitted


class D1HostingAdapter:
    """Append-only exact-ref adapter with logical-current indexes and reverse edges.

    This is deliberately not a database or a V558 replacement: semantic bodies stay
    with their competent existing owners/CAS. The adapter keeps only exact refs,
    immutable derivation revisions, logical-current pointers, reverse indexes, and
    the exact R1 rule-authority binding identities consumed at the admission seam.
    """

    def __init__(self) -> None:
        self._fact_context: dict[str, D1Context] = {}
        self._mechanism_rule_refs: dict[str, ExactRef] = {}
        self._rule_authority_binding_refs: dict[str, ExactRef] = {}
        self._evidence_witness_refs: dict[str, ExactRef] = {}
        self._fact_pointer: dict[str, D1FactPointer] = {}
        self._application_by_key: dict[str, D1RuleApplicationRef] = {}
        self._current_revision: dict[str, D1ApplicationRevision] = {}
        self._history: dict[str, list[D1ApplicationRevision]] = {}
        self._revision_by_ref: dict[str, D1ApplicationRevision] = {}
        self._producer_revision_by_fact: dict[str, D1ApplicationRevision] = {}
        self._reverse_current: dict[str, set[str]] = {}
        self._reverse_history: dict[str, set[str]] = {}
        self._current_derived_outputs: set[str] = set()

    def host_fact(self, fact: D1FactPointer) -> ExactRef:
        if not isinstance(fact, D1FactPointer):
            raise D1HostingIntegrityError("host_fact requires D1FactPointer")
        existing = self._fact_context.get(fact.fact_ref.key)
        if existing is not None and existing != fact.context:
            raise D1HostingIntegrityError("exact fact ref cannot change world/state/version/valid-time")
        self._fact_context[fact.fact_ref.key] = fact.context
        self._fact_pointer[fact.fact_ref.key] = fact
        return fact.fact_ref

    def _host_many(self, facts: Sequence[D1FactPointer]) -> None:
        for fact in facts:
            self.host_fact(fact)

    def hosted_mechanism_rule_refs(self) -> tuple[ExactRef, ...]:
        return tuple(self._mechanism_rule_refs[key] for key in sorted(self._mechanism_rule_refs))

    def hosted_rule_authority_binding_refs(self) -> tuple[ExactRef, ...]:
        return tuple(
            self._rule_authority_binding_refs[key]
            for key in sorted(self._rule_authority_binding_refs)
        )

    def hosted_evidence_witness_refs(self) -> tuple[ExactRef, ...]:
        return tuple(self._evidence_witness_refs[key] for key in sorted(self._evidence_witness_refs))

    def current_output_refs(self) -> tuple[ExactRef, ...]:
        return tuple(
            self._fact_pointer[key].fact_ref for key in sorted(self._current_derived_outputs)
        )

    def current_revision(self, application: D1RuleApplicationRef) -> D1ApplicationRevision:
        if not isinstance(application, D1RuleApplicationRef):
            raise D1HostingIntegrityError("current_revision requires D1RuleApplicationRef")
        try:
            return self._current_revision[application.key]
        except KeyError as exc:
            raise D1HostingIntegrityError("exact rule application is not hosted") from exc

    def history(self, application: D1RuleApplicationRef) -> tuple[D1ApplicationRevision, ...]:
        if not isinstance(application, D1RuleApplicationRef):
            raise D1HostingIntegrityError("history requires D1RuleApplicationRef")
        return tuple(self._history.get(application.key, ()))

    def reverse_dependents(
        self, fact_ref: ExactRef, *, historical: bool = False
    ) -> tuple[D1RuleApplicationRef, ...]:
        if not isinstance(fact_ref, ExactRef):
            raise D1HostingIntegrityError("reverse dependency lookup requires ExactRef")
        index = self._reverse_history if historical else self._reverse_current
        return tuple(
            self._application_by_key[key] for key in sorted(index.get(fact_ref.key, ()))
        )

    def _ancestor_producer_revisions(self, fact_ref: ExactRef) -> tuple[D1ApplicationRevision, ...]:
        seen_facts: set[str] = set()
        seen_revisions: dict[str, D1ApplicationRevision] = {}
        stack = [fact_ref.key]
        while stack:
            fact_key = stack.pop()
            if fact_key in seen_facts:
                continue
            seen_facts.add(fact_key)
            producer = self._producer_revision_by_fact.get(fact_key)
            if producer is None:
                continue
            seen_revisions[producer.exact_ref.key] = producer
            stack.extend(pointer.fact_ref.key for pointer in producer.determinant_facts)
        return tuple(seen_revisions[key] for key in sorted(seen_revisions))

    def _assert_no_same_context_self_ancestry(
        self,
        application: D1RuleApplicationRef,
        determinant_facts: Sequence[D1FactPointer],
        output_fact: D1FactPointer,
    ) -> None:
        target_fact_key = output_fact.fact_ref.key
        target_context = output_fact.context
        for determinant in determinant_facts:
            if determinant.fact_ref.key == target_fact_key and determinant.context == target_context:
                raise D1HostingIntegrityError(
                    "same world/state/version/valid-time direct self-ancestry forbidden"
                )
            for producer in self._ancestor_producer_revisions(determinant.fact_ref):
                if producer.output_fact is None:
                    continue
                if (
                    producer.output_fact.fact_ref.key == target_fact_key
                    and producer.output_fact.context == target_context
                ):
                    raise D1HostingIntegrityError(
                        "same world/state/version/valid-time transitive fact self-ancestry forbidden"
                    )
                if (
                    producer.application.key == application.key
                    and producer.output_fact.context == target_context
                ):
                    raise D1HostingIntegrityError(
                        "same world/state/version/valid-time rule-application self-ancestry forbidden"
                    )

    def _replace_current_reverse_edges(
        self,
        application_key: str,
        old_facts: Sequence[D1FactPointer],
        new_facts: Sequence[D1FactPointer],
    ) -> None:
        for fact in old_facts:
            users = self._reverse_current.get(fact.fact_ref.key)
            if users is not None:
                users.discard(application_key)
                if not users:
                    self._reverse_current.pop(fact.fact_ref.key, None)
        for fact in new_facts:
            self._reverse_current.setdefault(fact.fact_ref.key, set()).add(application_key)
            self._reverse_history.setdefault(fact.fact_ref.key, set()).add(application_key)

    def _append_revision(self, revision: D1ApplicationRevision) -> None:
        ref = revision.exact_ref
        existing = self._revision_by_ref.get(ref.key)
        if existing is not None and existing != revision:
            raise D1HostingIntegrityError("revision content-address collision")
        app_key = revision.application.key
        self._revision_by_ref[ref.key] = revision
        self._history.setdefault(app_key, []).append(revision)
        self._current_revision[app_key] = revision
        if revision.output_fact is not None:
            old_producer = self._producer_revision_by_fact.get(revision.output_fact.fact_ref.key)
            if old_producer is not None and old_producer.application.key != app_key:
                raise D1HostingIntegrityError("exact consequence fact cannot have two producer applications")
            self._producer_revision_by_fact[revision.output_fact.fact_ref.key] = revision

    def _record_admission(self, binding: MechanismRuleAuthorityBinding) -> None:
        rule_ref = binding.rule_identity.ref
        self._mechanism_rule_refs[rule_ref.key] = rule_ref
        self._rule_authority_binding_refs[binding.ref.key] = binding.ref

    def host_direct_derivation(
        self,
        application: D1RuleApplicationRef,
        *,
        determinant_facts: Sequence[D1FactPointer],
        output_fact: D1FactPointer,
        evidence_witness_refs: Sequence[ExactRef] = (),
        rule_admission: MechanismRuleAuthorityBinding | None = None,
    ) -> D1ApplicationRevision:
        if not isinstance(application, D1RuleApplicationRef):
            raise D1HostingIntegrityError("host_direct_derivation requires exact application")
        admitted = _require_exact_current_rule_admission(application, rule_admission)
        if application.key in self._current_revision:
            raise D1HostingIntegrityError("rule application already hosted; use determinant-scoped redrive")
        determinants = tuple(determinant_facts)
        if not determinants:
            raise D1HostingIntegrityError("direct derivation requires at least one determinant")
        evaluation = D1Evaluation(
            supported=True,
            determinant_facts=determinants,
            output_fact=output_fact,
            evidence_witness_refs=tuple(evidence_witness_refs),
        )
        self._host_many(evaluation.determinant_facts)
        self.host_fact(output_fact)
        self._assert_no_same_context_self_ancestry(
            application, evaluation.determinant_facts, output_fact
        )
        self._application_by_key[application.key] = application
        self._record_admission(admitted)
        for witness_ref in evaluation.evidence_witness_refs:
            self._evidence_witness_refs[witness_ref.key] = witness_ref
        revision = D1ApplicationRevision(
            application=application,
            determinant_facts=evaluation.determinant_facts,
            output_fact=output_fact,
            evidence_witness_refs=evaluation.evidence_witness_refs,
            status="SUPPORTED_CURRENT",
            prior_revision_ref=None,
            trigger_refs=(),
            rule_authority_binding_ref=admitted.ref,
            current_rule_admission_ref=admitted.ref,
        )
        self._replace_current_reverse_edges(application.key, (), revision.determinant_facts)
        self._append_revision(revision)
        self._current_derived_outputs.add(output_fact.fact_ref.key)
        return revision

    def _application_depth(self, application_key: str) -> int:
        memo: dict[str, int] = {}
        active: set[str] = set()

        def depth(key: str) -> int:
            if key in memo:
                return memo[key]
            if key in active:
                raise D1HostingIntegrityError("current D1 dependency graph contains a cycle")
            active.add(key)
            revision = self._current_revision[key]
            parent_depths: list[int] = []
            for determinant in revision.determinant_facts:
                producer = self._producer_revision_by_fact.get(determinant.fact_ref.key)
                if (
                    producer is not None
                    and producer.application.key != key
                    and producer.application.key in self._current_revision
                ):
                    parent_depths.append(depth(producer.application.key))
            active.remove(key)
            memo[key] = (max(parent_depths) + 1) if parent_depths else 0
            return memo[key]

        return depth(application_key)

    @staticmethod
    def _changed_output_refs(
        before: D1ApplicationRevision, after: D1ApplicationRevision
    ) -> tuple[ExactRef, ...]:
        before_ref = None if before.output_fact is None else before.output_fact.fact_ref
        after_ref = None if after.output_fact is None else after.output_fact.fact_ref
        if before_ref == after_ref and before.status == after.status:
            return ()
        refs = [ref for ref in (before_ref, after_ref) if ref is not None]
        return _unique_refs(refs, "changed_output_refs")

    def _apply_evaluation(
        self,
        application: D1RuleApplicationRef,
        before: D1ApplicationRevision,
        evaluation: D1Evaluation,
        trigger_refs: tuple[ExactRef, ...],
        admitted: MechanismRuleAuthorityBinding,
    ) -> tuple[D1ApplicationRevision, str, tuple[ExactRef, ...]]:
        admitted = _require_exact_current_rule_admission(application, admitted)
        self._host_many(evaluation.determinant_facts)
        if evaluation.output_fact is not None:
            self.host_fact(evaluation.output_fact)
            self._assert_no_same_context_self_ancestry(
                application, evaluation.determinant_facts, evaluation.output_fact
            )
        self._record_admission(admitted)
        for witness_ref in evaluation.evidence_witness_refs:
            self._evidence_witness_refs[witness_ref.key] = witness_ref
        after = D1ApplicationRevision(
            application=application,
            determinant_facts=evaluation.determinant_facts,
            output_fact=evaluation.output_fact,
            evidence_witness_refs=evaluation.evidence_witness_refs,
            status="SUPPORTED_CURRENT" if evaluation.supported else "CLOSED_UNSUPPORTED",
            prior_revision_ref=before.exact_ref,
            trigger_refs=trigger_refs,
            rule_authority_binding_ref=admitted.ref,
            current_rule_admission_ref=admitted.ref,
        )
        same_semantics = (
            before.status == after.status
            and before.determinant_facts == after.determinant_facts
            and before.output_fact == after.output_fact
            and before.evidence_witness_refs == after.evidence_witness_refs
            and before.rule_authority_binding_ref == after.rule_authority_binding_ref
            and before.current_rule_admission_ref == after.current_rule_admission_ref
        )
        if same_semantics:
            return before, "UNCHANGED", ()

        changed = self._changed_output_refs(before, after)
        self._replace_current_reverse_edges(
            application.key, before.determinant_facts, after.determinant_facts
        )
        if before.output_fact is not None:
            self._current_derived_outputs.discard(before.output_fact.fact_ref.key)
        if after.output_fact is not None:
            self._current_derived_outputs.add(after.output_fact.fact_ref.key)
        self._append_revision(after)
        disposition = (
            "CLOSED_UNSUPPORTED"
            if not evaluation.supported
            else "REPLACED_OUTPUT" if changed else "SUPPORTED_DEPENDENCY_REFRESH"
        )
        return after, disposition, changed

    def _close_for_rule_admission_failure(
        self,
        application: D1RuleApplicationRef,
        before: D1ApplicationRevision,
        trigger_refs: tuple[ExactRef, ...],
        supplied_binding: MechanismRuleAuthorityBinding | None,
        disposition: str,
    ) -> tuple[D1ApplicationRevision, str, tuple[ExactRef, ...]]:
        binding_ref = (
            supplied_binding.ref
            if isinstance(supplied_binding, MechanismRuleAuthorityBinding)
            else None
        )
        if isinstance(supplied_binding, MechanismRuleAuthorityBinding):
            self._rule_authority_binding_refs[binding_ref.key] = binding_ref
        after = D1ApplicationRevision(
            application=application,
            determinant_facts=before.determinant_facts,
            output_fact=None,
            evidence_witness_refs=before.evidence_witness_refs,
            status="CLOSED_UNSUPPORTED",
            prior_revision_ref=before.exact_ref,
            trigger_refs=trigger_refs,
            rule_authority_binding_ref=binding_ref,
            current_rule_admission_ref=None,
        )
        same_semantics = (
            before.status == after.status
            and before.determinant_facts == after.determinant_facts
            and before.output_fact == after.output_fact
            and before.evidence_witness_refs == after.evidence_witness_refs
            and before.rule_authority_binding_ref == after.rule_authority_binding_ref
            and before.current_rule_admission_ref is None
        )
        if same_semantics:
            return before, "UNCHANGED", ()
        changed = self._changed_output_refs(before, after)
        self._replace_current_reverse_edges(
            application.key, before.determinant_facts, after.determinant_facts
        )
        if before.output_fact is not None:
            self._current_derived_outputs.discard(before.output_fact.fact_ref.key)
        self._append_revision(after)
        return after, disposition, changed

    def redrive(
        self,
        changed_determinant_refs: Sequence[ExactRef],
        evaluator: Evaluator,
        rule_admission_resolver: RuleAdmissionResolver | None = None,
    ) -> D1ReplayReceipt:
        triggers = _unique_refs(changed_determinant_refs, "changed_determinant_refs")
        if not triggers:
            raise D1HostingIntegrityError("redrive requires at least one changed determinant ref")
        if not callable(evaluator):
            raise D1HostingIntegrityError("redrive evaluator must be callable")
        if rule_admission_resolver is not None and not callable(rule_admission_resolver):
            raise D1HostingIntegrityError("rule_admission_resolver must be callable or None")

        before_outputs = self.current_output_refs()
        pending: list[tuple[int, str, str]] = []
        pending_keys: set[str] = set()
        trigger_by_application: dict[str, set[str]] = {}
        exact_affected_edges: set[tuple[str, str, str | None]] = set()

        def schedule_for_fact(ref: ExactRef) -> None:
            for app_key in sorted(self._reverse_current.get(ref.key, ())):
                trigger_by_application.setdefault(app_key, set()).add(ref.key)
                if app_key not in pending_keys:
                    depth = self._application_depth(app_key)
                    heapq.heappush(pending, (depth, app_key, app_key))
                    pending_keys.add(app_key)

        for ref in triggers:
            schedule_for_fact(ref)

        steps: list[D1ReplayStep] = []
        evaluated_at_revision: set[tuple[str, str]] = set()
        while pending:
            _, app_key, _ = heapq.heappop(pending)
            pending_keys.discard(app_key)
            before = self._current_revision[app_key]
            eval_key = (app_key, before.exact_ref.key)
            if eval_key in evaluated_at_revision:
                continue
            evaluated_at_revision.add(eval_key)
            application = self._application_by_key[app_key]
            step_trigger_keys = sorted(trigger_by_application.pop(app_key, ()))
            step_triggers = tuple(
                self._fact_pointer[key].fact_ref
                if key in self._fact_pointer
                else next(ref for ref in triggers if ref.key == key)
                for key in step_trigger_keys
            )
            before_output_key = None if before.output_fact is None else before.output_fact.fact_ref.key
            for determinant in before.determinant_facts:
                exact_affected_edges.add(
                    (determinant.fact_ref.key, application.exact_ref.key, before_output_key)
                )

            supplied_binding = (
                None
                if rule_admission_resolver is None
                else rule_admission_resolver(application, before)
            )
            try:
                admitted = _require_exact_current_rule_admission(application, supplied_binding)
            except D1HostingIntegrityError as exc:
                mismatch = (
                    isinstance(supplied_binding, MechanismRuleAuthorityBinding)
                    and supplied_binding.rule_identity.ref != application.mechanism_rule_ref
                )
                disposition = (
                    "CLOSED_RULE_ADMISSION_IDENTITY_MISMATCH"
                    if mismatch
                    else "CLOSED_RULE_NOT_CURRENT_OR_UNADMITTED"
                )
                after, disposition, changed_outputs = self._close_for_rule_admission_failure(
                    application,
                    before,
                    step_triggers,
                    supplied_binding,
                    disposition,
                )
            else:
                evaluation = evaluator(application, before)
                if not isinstance(evaluation, D1Evaluation):
                    raise D1HostingIntegrityError("evaluator must return D1Evaluation")
                after, disposition, changed_outputs = self._apply_evaluation(
                    application, before, evaluation, step_triggers, admitted
                )
            steps.append(
                D1ReplayStep(
                    application_ref=application.exact_ref,
                    before_revision_ref=before.exact_ref,
                    after_revision_ref=after.exact_ref,
                    disposition=disposition,
                    changed_output_refs=changed_outputs,
                    rule_authority_binding_ref=after.rule_authority_binding_ref,
                    current_rule_admission_ref=after.current_rule_admission_ref,
                )
            )
            for changed_ref in changed_outputs:
                schedule_for_fact(changed_ref)

        after_outputs = self.current_output_refs()
        receipt_material = {
            "contract_id": CONTRACT_ID,
            "admission_conservation_contract_id": CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID,
            "trigger_refs": [ref.as_dict() for ref in triggers],
            "before_current_output_refs": [ref.as_dict() for ref in before_outputs],
            "after_current_output_refs": [ref.as_dict() for ref in after_outputs],
            "steps": [step.as_dict() for step in steps],
            "exact_affected_edges": [list(edge) for edge in sorted(exact_affected_edges)],
        }
        receipt = D1ReplayReceipt(
            trigger_refs=triggers,
            before_current_output_refs=before_outputs,
            after_current_output_refs=after_outputs,
            steps=tuple(steps),
            exact_affected_edges=tuple(sorted(exact_affected_edges)),
            content_hash=semantic_hash(receipt_material),
        )
        receipt.verify()
        return receipt


__all__ = [
    "CONTRACT_ID",
    "CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID",
    "D1HostingIntegrityError",
    "D1ReplayParityError",
    "D1Context",
    "D1FactPointer",
    "D1RuleApplicationRef",
    "D1Evaluation",
    "D1ApplicationRevision",
    "D1ReplayStep",
    "D1ReplayReceipt",
    "Evaluator",
    "RuleAdmissionResolver",
    "D1HostingAdapter",
]
