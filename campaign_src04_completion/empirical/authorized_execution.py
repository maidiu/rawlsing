"""Authenticated native SRC04 observed-response issuance and execution.

This module consumes the human-issued ``USER_EMPIRICAL_GRANT.json`` and an
exact, already-validated native C11 release.  It constructs positive operation,
source-literal, topology and target-use authority snapshots through the existing
``AuthoritySnapshot``/``AuthorityRegistry`` mechanisms, derives an authorized
``ObservedResponseContract`` and executes the existing native workload builder.

It never opens, stats, hashes or decodes the original SAV.  If the full native
release is absent, it returns a precise pending-input record rather than a
permission refusal or fictional completion.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from campaign_src04_completion.empirical.native_workload import (
    NativeWorkload,
    NativeWorkloadRefusal,
    WorkloadPolicy,
    execute_native_workload,
)
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_observed_response import (
    ObservedResponseContract,
    ObservedResponseTopologyBinding,
    validate_contract_authority,
)
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier, ParquetCarrierError

GRANT_SCHEMA = "PYAT_SRC04_NATIVE_EMPIRICAL_USER_GRANT@1.0.0"
GRANT_SHA256 = "757ee9e0eddd933b9d23d9cb84450e0dafabd8b1b6a1ad7e737d433b32c0130f"
GRANT_OPERATION = "PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0"
SOURCE_LITERAL_OPERATION = "OBSERVED_RESPONSE_SOURCE_LITERAL_BINDING@1.0.0"
TOPOLOGY_OPERATION = "R157_PREPARE_SOURCE_TOPOLOGY"
TARGET_USE_OPERATION = "SOURCE_LOCAL_OBSERVED_RESPONSE_PUBLICATION@1.0.0"
TARGET_USE_REF = ExactRef(
    "TARGET_USE",
    "urn:rawlsing:pre553:target-use:SRC04:source-local-observed-response",
    "d5e81ebfc35b86a3488f9c7a4cef69b173a1a585d4e35fc26307f7bf8e019f36",
)
ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "SRC04"
SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
EXPECTED_ROWS = 7337
ALLOWED_ONE_EVENT_KINDS = frozenset({
    "SCALAR", "ORDINAL_CONTEXT", "NOMINAL_CHOICE", "BINARY_FACTUAL",
    "BINARY_CONTRAST", "RANKED_CHOICE",
})
REQUIRED_METHODS = frozenset({
    "UNARY_OBSERVED_DISTRIBUTION",
    "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
    "SAME_RESPONDENT_JOINT_DISTRIBUTION",
})


class AuthorizedExecutionRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


@dataclass(frozen=True)
class HumanGrant:
    path: Path
    sha256: str
    document: Mapping[str, Any]

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            "USER_EMPIRICAL_GRANT",
            f"urn:rawlsing:user-empirical-grant:SRC04:{self.sha256}",
            self.sha256,
        )


@dataclass(frozen=True)
class IssuedExecution:
    grant: HumanGrant
    release: C11LogicalRelease
    repository: C11Repository
    registry: AuthorityRegistry
    contract: ObservedResponseContract
    policy: WorkloadPolicy
    source_literal_authority_ref: AuthorityRef
    topology_authority_refs: Mapping[str, AuthorityRef]
    target_use_authority_ref: AuthorityRef
    held_targets: tuple[Mapping[str, Any], ...]
    authorities: tuple[AuthoritySnapshot, ...] = ()


def _sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def authenticate_grant(path: str | Path, expected_sha256: str = GRANT_SHA256) -> HumanGrant:
    path = Path(path)
    if not path.is_file():
        raise AuthorizedExecutionRefusal("GRANT_FILE_ABSENT", str(path))
    actual = _sha_file(path)
    if actual != expected_sha256:
        raise AuthorizedExecutionRefusal("GRANT_SHA256_MISMATCH", actual)
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != GRANT_SCHEMA:
        raise AuthorizedExecutionRefusal("GRANT_SCHEMA_MISMATCH")
    if document.get("source_id") != SOURCE_ID or document.get("source_sha256") != SOURCE_SHA256:
        raise AuthorizedExecutionRefusal("GRANT_SOURCE_MISMATCH")
    if document.get("operation") != GRANT_OPERATION:
        raise AuthorizedExecutionRefusal("GRANT_OPERATION_MISMATCH")
    if document.get("decision") != "ALLOW_WITHIN_EXACT_SCOPE":
        raise AuthorizedExecutionRefusal("GRANT_DECISION_NOT_ALLOW")
    if document.get("currentness") != "CURRENT_GRANTED":
        raise AuthorizedExecutionRefusal("GRANT_NOT_CURRENT")
    scope = document.get("scope")
    if not isinstance(scope, Mapping):
        raise AuthorizedExecutionRefusal("GRANT_SCOPE_MISSING")
    methods = set(scope.get("methods", ()))
    if not REQUIRED_METHODS.issubset(methods):
        raise AuthorizedExecutionRefusal("GRANT_METHOD_SCOPE_INCOMPLETE", repr(sorted(methods)))
    if set(scope.get("denominators", ())) != {"PER_TARGET_OBSERVED", "CO_OBSERVED_TARGETS"}:
        raise AuthorizedExecutionRefusal("GRANT_DENOMINATOR_SCOPE_MISMATCH")
    if scope.get("condition_observation") != "ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED":
        raise AuthorizedExecutionRefusal("GRANT_CONDITION_POLICY_MISMATCH")
    use = " ".join(str(x) for x in scope.get("source_local_use", ())).lower()
    if "existingnativei03" not in use.replace(" ", "") and "i03empiricalfact" not in use.replace(" ", ""):
        raise AuthorizedExecutionRefusal("GRANT_SOURCE_LOCAL_USE_MISSING")
    return HumanGrant(path=path, sha256=actual, document=document)


def load_parquet_release(
    *,
    root: str | Path,
    source_sha256: str,
    release_id: str,
    semantic_hash_value: str,
) -> C11LogicalRelease:
    try:
        release = ParquetC11Carrier(Path(root)).reopen(
            source_sha256, release_id, semantic_hash_value)
    except ParquetCarrierError as exc:
        raise AuthorizedExecutionRefusal("NATIVE_RELEASE_INPUT_INVALID", str(exc)) from exc
    if release.source_artifact_ref.content_hash != SOURCE_SHA256:
        raise AuthorizedExecutionRefusal("RELEASE_SOURCE_IDENTITY_MISMATCH")
    if release.release_id.startswith("R157_FIXTURE") or "FIXTURE" in release.release_id.upper():
        raise AuthorizedExecutionRefusal("FIXTURE_RELEASE_CANNOT_BE_ORIGINAL")
    return release


def _target_events(release: C11LogicalRelease, target_ref: ExactRef) -> list[Any]:
    matches = []
    for obj in release.public_objects:
        if obj.schema_id != "RespondentEvent":
            continue
        native = exact_ref(obj.native_question_ref, "native_question_ref")
        canonical = obj.canonical_question_ref_if_authorized
        component = obj.component_or_subitem_ref
        if target_ref == native:
            matches.append(obj)
        elif canonical is not None and target_ref == exact_ref(canonical, "canonical_question_ref"):
            matches.append(obj)
        elif component is not None and target_ref == exact_ref(component, "component_or_subitem_ref"):
            matches.append(obj)
    return matches


def _topology_valid_targets(
    release: C11LogicalRelease,
    contract: ObservedResponseContract,
) -> tuple[tuple[ObservedResponseTopologyBinding, ...], tuple[Mapping[str, Any], ...], tuple[AuthorityRef, ...]]:
    respondents = tuple(
        record for record in release.internal_records if isinstance(record, RespondentIdentity))
    respondent_keys = {record.ref.key for record in respondents}
    valid: list[ObservedResponseTopologyBinding] = []
    held: list[Mapping[str, Any]] = []
    event_authorities: set[AuthorityRef] = set()
    contract_bindings = {binding.target_ref.key: binding for binding in contract.topology_bindings}
    release_targets = sorted(
        {
            exact_ref(obj.native_question_ref, "native_question_ref")
            for obj in release.public_objects if obj.schema_id == "RespondentEvent"
        },
        key=lambda ref: ref.key,
    )
    all_bindings = list(contract.topology_bindings)
    for target_ref in release_targets:
        if target_ref.key in contract_bindings:
            continue
        events = [e for e in _target_events(release, target_ref) if e.typed_state in contract.observed_states]
        if not events:
            held.append({"target_ref": target_ref.as_dict(), "code": "NO_OBSERVED_EVENTS"})
            continue
        first = events[0]
        fields = first.multiplicity_order_rank_fields
        kind = str(fields.get("kind") or "") if isinstance(fields, Mapping) else ""
        all_bindings.append(ObservedResponseTopologyBinding(
            target_ref=target_ref,
            source_native_topology_ref=exact_ref(first.response_topology_ref, "response_topology_ref"),
            source_native_kind=kind,
            i03_topology="SCALAR_SINGULAR",
            topology_operation=TOPOLOGY_OPERATION,
            topology_authority_ref=None,
            response_semantic_authority_refs=(),
        ))
    for binding in all_bindings:
        events = _target_events(release, binding.target_ref)
        observed = [event for event in events if event.typed_state in contract.observed_states]
        if not observed:
            held.append({"target_ref": binding.target_ref.as_dict(), "code": "NO_OBSERVED_EVENTS"})
            continue
        per_respondent: dict[str, int] = {}
        kinds: set[str] = set()
        topology_refs: set[ExactRef] = set()
        bad_canonical = False
        for event in observed:
            respondent = exact_ref(event.scoped_respondent_ref, "scoped_respondent_ref")
            if respondent.key not in respondent_keys:
                held.append({"target_ref": binding.target_ref.as_dict(), "code": "UNKNOWN_RESPONDENT"})
                break
            per_respondent[respondent.key] = per_respondent.get(respondent.key, 0) + 1
            fields = event.multiplicity_order_rank_fields
            if not isinstance(fields, Mapping):
                kinds.add("MISSING_TOPOLOGY_FIELDS")
            else:
                kinds.add(str(fields.get("kind") or ""))
            topology_refs.add(exact_ref(event.response_topology_ref, "response_topology_ref"))
            if event.canonical_response_value_if_authorized is not None:
                bad_canonical = True
        else:
            if any(count > 1 for count in per_respondent.values()):
                held.append({"target_ref": binding.target_ref.as_dict(),
                             "code": "MULTIPLE_EVENTS_PER_RESPONDENT_FOR_SCALAR_PROJECTION"})
                continue
            if len(kinds) != 1:
                held.append({"target_ref": binding.target_ref.as_dict(),
                             "code": "AMBIGUOUS_SOURCE_NATIVE_TOPOLOGY", "kinds": sorted(kinds)})
                continue
            kind = next(iter(kinds))
            if kind not in ALLOWED_ONE_EVENT_KINDS:
                held.append({"target_ref": binding.target_ref.as_dict(),
                             "code": "UNSUPPORTED_SOURCE_NATIVE_TOPOLOGY", "kind": kind})
                continue
            if topology_refs != {binding.source_native_topology_ref}:
                held.append({"target_ref": binding.target_ref.as_dict(),
                             "code": "TOPOLOGY_REF_MISMATCH"})
                continue
            if kind != binding.source_native_kind:
                held.append({"target_ref": binding.target_ref.as_dict(),
                             "code": "TOPOLOGY_KIND_MISMATCH",
                             "contract_kind": binding.source_native_kind, "release_kind": kind})
                continue
            if binding.i03_topology != "SCALAR_SINGULAR":
                held.append({"target_ref": binding.target_ref.as_dict(),
                             "code": "NON_SCALAR_CONTRACT_TOPOLOGY"})
                continue
            if bad_canonical:
                held.append({"target_ref": binding.target_ref.as_dict(),
                             "code": "CANONICAL_VALUE_PRESENT_FOR_SOURCE_LITERAL"})
                continue
            for event in observed:
                for ref in event.authority_snapshot_refs:
                    event_authorities.add(authority_ref(ref, "event authority"))
            valid.append(ObservedResponseTopologyBinding(
                target_ref=binding.target_ref,
                source_native_topology_ref=binding.source_native_topology_ref,
                source_native_kind=binding.source_native_kind,
                i03_topology=binding.i03_topology,
                topology_operation=TOPOLOGY_OPERATION,
                topology_authority_ref=None,
                response_semantic_authority_refs=binding.response_semantic_authority_refs,
            ))
    if not valid:
        raise AuthorizedExecutionRefusal("NO_SOURCE_QUALIFIED_TARGETS")
    return (
        tuple(sorted(valid, key=lambda item: item.target_ref.key)),
        tuple(held),
        tuple(sorted(event_authorities, key=lambda ref: ref.key)),
    )


def _snapshot(
    *,
    authority_id: str,
    kind: str,
    operations: tuple[str, ...],
    families: tuple[str, ...],
    scope: Mapping[str, Any],
    material: Mapping[str, Any],
    dependencies: Iterable[ExactRef],
    tag: str,
) -> AuthoritySnapshot:
    digest = semantic_hash(material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=tuple(sorted(set(dependencies), key=lambda ref: ref.key)),
        producer_replay_locator_or_reference_root=ExactRef(
            "REPLAY_ROOT", f"urn:rawlsing:user-grant-replay:{tag}:{digest}", digest),
        authority_id=authority_id,
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=operations,
        governed_object_families=families,
        scope_envelope=scope,
        effective_time_or_interval="2026-10-28/USER_EMPIRICAL_GRANT",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=digest,
        replay_protocol_ref=ExactRef(
            "REPLAY_PROTOCOL", f"urn:rawlsing:user-grant-replay-protocol:{tag}", digest),
    )


def _base_scope(grant: HumanGrant, release: C11LogicalRelease, universe_ref: ExactRef, risk_set_ref: ExactRef) -> dict[str, Any]:
    return {
        "source_universe_refs": [universe_ref.as_dict()],
        "predicate_or_risk_set_refs": [risk_set_ref.as_dict()],
        "release_ref": release.release_ref.as_dict(),
        "source_artifact_ref": release.source_artifact_ref.as_dict(),
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA256,
        "grant_sha256": grant.sha256,
        "grant_ref": grant.ref.as_dict(),
        "fixture_only": False,
        "grade": "USER_EMPIRICAL_GRANT",
        "canonical_adoption": "DENY",
    }


def issue_authorized_execution(
    *,
    grant: HumanGrant,
    release: C11LogicalRelease,
    pending_contract: ObservedResponseContract,
    policy: WorkloadPolicy,
) -> IssuedExecution:
    if release.source_artifact_ref.content_hash != SOURCE_SHA256:
        raise AuthorizedExecutionRefusal("RELEASE_SOURCE_IDENTITY_MISMATCH")
    if release.source_release_manifest_hash in (None, ""):
        raise AuthorizedExecutionRefusal("RELEASE_MANIFEST_HASH_MISSING")
    if pending_contract.universe_ref is None:
        raise AuthorizedExecutionRefusal("CONTRACT_UNIVERSE_REQUIRED")
    respondents = tuple(
        record for record in release.internal_records if isinstance(record, RespondentIdentity))
    if len(respondents) != EXPECTED_ROWS:
        raise AuthorizedExecutionRefusal("RELEASE_RESPONDENT_COUNT_MISMATCH", str(len(respondents)))
    valid_bindings, held, event_authorities = _topology_valid_targets(release, pending_contract)
    universe_obj = next(
        (obj for obj in release.public_objects if obj.ref == pending_contract.universe_ref), None)
    if universe_obj is None:
        raise AuthorizedExecutionRefusal("RELEASE_UNIVERSE_NOT_FOUND")
    event_authorities = tuple(sorted(
        set(event_authorities)
        | {authority_ref(ref, "universe authority") for ref in universe_obj.authority_snapshot_refs},
        key=lambda ref: ref.key,
    ))
    target_refs = tuple(binding.target_ref for binding in valid_bindings)
    if not target_refs:
        raise AuthorizedExecutionRefusal("NO_SOURCE_QUALIFIED_TARGETS")
    release_event_targets = {
        exact_ref(obj.native_question_ref, "native_question_ref")
        for obj in release.public_objects if obj.schema_id == "RespondentEvent"
    }
    base_scope = _base_scope(grant, release, pending_contract.universe_ref, pending_contract.risk_set_ref)
    grammar_material = {
        "authority_id": "SRC04-USER-EMPIRICAL-PREDICATE-GRAMMAR",
        "kind": "PREDICATE_GRAMMAR",
        "operation": grant.document["operation"],
        "scope": base_scope,
        "grant_sha256": grant.sha256,
    }
    grammar = _snapshot(
        authority_id="SRC04-USER-EMPIRICAL-PREDICATE-GRAMMAR",
        kind="PREDICATE_GRAMMAR",
        operations=(grant.document["operation"],),
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        scope=base_scope,
        material=grammar_material,
        dependencies=(grant.ref, pending_contract.ref),
        tag="predicate-grammar",
    )
    literal_scope = {
        **base_scope,
        "historical_event_authority_refs": [ref.as_dict() for ref in event_authorities],
        "source_literal_only": True,
        "canonical_adoption": "DENY",
    }
    literal_material = {
        "authority_id": "SRC04-USER-EMPIRICAL-SOURCE-LITERAL",
        "kind": "PHYSICAL_NATIVE_REPRESENTATION_BINDING",
        "operation": SOURCE_LITERAL_OPERATION,
        "scope": literal_scope,
        "grant_sha256": grant.sha256,
    }
    literal = _snapshot(
        authority_id="SRC04-USER-EMPIRICAL-SOURCE-LITERAL",
        kind="PHYSICAL_NATIVE_REPRESENTATION_BINDING",
        operations=(SOURCE_LITERAL_OPERATION,),
        families=("RespondentEvent@1.0.0", "EmpiricalUniverse@1.0.0"),
        scope=literal_scope,
        material=literal_material,
        dependencies=(grant.ref,),
        tag="source-literal",
    )
    topology_by_key: dict[str, AuthoritySnapshot] = {}
    authorized_bindings: list[ObservedResponseTopologyBinding] = []
    for binding in valid_bindings:
        topology_scope = {
            **base_scope,
            "target_ref": binding.target_ref.as_dict(),
            "source_native_topology_ref": binding.source_native_topology_ref.as_dict(),
            "source_native_kind": binding.source_native_kind,
            "i03_topology": binding.i03_topology,
            "one_event_per_respondent": True,
            "topology_operation": TOPOLOGY_OPERATION,
        }
        topology_authority_id = (
            "SRC04-USER-EMPIRICAL-TOPOLOGY-" + binding.target_ref.content_hash[:16]
        )
        topology_material = {
            "authority_id": topology_authority_id,
            "kind": "SOURCE_SEMANTICS_TOPOLOGY",
            "target_ref": binding.target_ref.as_dict(),
            "source_native_topology_ref": binding.source_native_topology_ref.as_dict(),
            "source_native_kind": binding.source_native_kind,
            "i03_topology": binding.i03_topology,
            "scope": topology_scope,
            "grant_sha256": grant.sha256,
        }
        topology = _snapshot(
            authority_id=topology_authority_id,
            kind="SOURCE_SEMANTICS_TOPOLOGY",
            operations=(TOPOLOGY_OPERATION,),
            families=("RespondentEvent@1.0.0",),
            scope=topology_scope,
            material=topology_material,
            dependencies=(grant.ref,),
            tag=f"topology-{binding.target_ref.content_hash[:12]}",
        )
        topology_by_key[binding.target_ref.key] = topology
        authorized_bindings.append(replace(
            binding,
            topology_authority_ref=topology.authority_ref,
            response_semantic_authority_refs=(literal.authority_ref,),
        ))
    use_scope = {
        **base_scope,
        "target_use_refs": [TARGET_USE_REF.as_dict()],
        "source_local_use": "EXISTING_NATIVE_I03_EMPIRICALFACT",
    }
    use_material = {
        "authority_id": "SRC04-USER-EMPIRICAL-TARGET-USE",
        "kind": "TARGET_USE_PERMISSION",
        "operation": TARGET_USE_OPERATION,
        "scope": use_scope,
        "target_use_ref": TARGET_USE_REF.as_dict(),
        "grant_sha256": grant.sha256,
    }
    target_use = _snapshot(
        authority_id="SRC04-USER-EMPIRICAL-TARGET-USE",
        kind="TARGET_USE_PERMISSION",
        operations=(TARGET_USE_OPERATION,),
        families=("EmpiricalFact@1.0.0",),
        scope=use_scope,
        material=use_material,
        dependencies=(grant.ref,),
        tag="target-use",
    )
    authorized_contract = replace(
        pending_contract,
        contract_state="AUTHORIZED",
        authority_grade="ORIGINAL_SCIENTIFIC",
        release_ref=release.release_ref,
        source_release_manifest_hash=release.source_release_manifest_hash,
        universe_ref=pending_contract.universe_ref,
        operation_authority_ref=grammar.authority_ref,
        target_refs=target_refs,
        topology_bindings=tuple(sorted(authorized_bindings, key=lambda item: item.target_ref.key)),
        source_literal_authority_ref=literal.authority_ref,
        source_literal_operation=SOURCE_LITERAL_OPERATION,
        source_event_authority_refs=event_authorities,
        target_use_ref=TARGET_USE_REF,
        target_use_authority_ref=target_use.authority_ref,
        target_use_operation=TARGET_USE_OPERATION,
    )
    release_authorities = tuple(
        obj for obj in release.public_objects if obj.schema_id == "AuthoritySnapshot")
    issued_authorities = (grammar, literal, target_use, *topology_by_key.values())
    registry = AuthorityRegistry((*release_authorities, *issued_authorities))
    validate_contract_authority(authorized_contract, registry)
    return IssuedExecution(
        grant=grant,
        release=release,
        repository=C11Repository((release,)),
        registry=registry,
        contract=authorized_contract,
        policy=policy,
        source_literal_authority_ref=literal.authority_ref,
        topology_authority_refs={key: snap.authority_ref for key, snap in topology_by_key.items()},
        target_use_authority_ref=target_use.authority_ref,
        held_targets=held,
        authorities=tuple(release_authorities) + tuple(issued_authorities),
    )


def execute_issued(
    issued: IssuedExecution,
    *,
    start_after_operation_id: str | None = None,
) -> NativeWorkload:
    return execute_native_workload(
        repository=issued.repository,
        release_ref=issued.release.release_ref,
        contract=issued.contract,
        authority_registry=issued.registry,
        policy=issued.policy,
        start_after_operation_id=start_after_operation_id,
    )


def preflight(
    *,
    grant: HumanGrant,
    pending_contract: ObservedResponseContract,
    scope: Mapping[str, Any],
) -> dict[str, Any]:
    """Authenticated issuer preflight with no release input."""
    return {
        "schema": "PYAT_SRC04_AUTHORIZED_EXECUTION_PREFLIGHT@1.0.0",
        "status": "AUTHENTICATED_GRANT_ISSUER_READY__RELEASE_INPUT_PENDING",
        "grant": {
            "path": (str(grant.path.relative_to(ROOT)) if grant.path.is_relative_to(ROOT) else str(grant.path)),
            "sha256": grant.sha256,
            "ref": grant.ref.as_dict(),
            "operation": grant.document["operation"],
            "issuer": grant.document.get("issuer"),
        },
        "pending_contract_ref": pending_contract.ref.as_dict(),
        "scope": {
            "available_response_fields": scope.get("physical_accounting", {}).get("available_response_fields"),
            "held_response_fields": scope.get("physical_accounting", {}).get("held_response_fields"),
            "available_analytical_coordinates": scope.get("physical_accounting", {}).get("available_analytical_coordinates"),
        },
        "issuer_outputs_ready": [
            "positive PREDICATE_GRAMMAR",
            "positive PHYSICAL_NATIVE_REPRESENTATION_BINDING source-literal",
            "positive SOURCE_SEMANTICS_TOPOLOGY per validated one-event target",
            "positive TARGET_USE_PERMISSION for SOURCE_LOCAL_STATISTIC",
            "authorized contract + AuthorityRegistry",
        ],
        "release_input_required": {
            "backend": "PRE553_PARQUET_C11_CARRIER",
            "required_fields": ["parquet_root", "source_sha256", "release_id", "semantic_hash"],
            "source_sha256": SOURCE_SHA256,
            "accepted_42_field_release_is_not_sufficient": True,
            "note": "A full-source construction candidate/replay format is not final; no polling or duplicate read is performed by Lane C.",
        },
        "original_workload_issued": False,
        "source_read_performed": False,
    }


__all__ = [
    "GRANT_SCHEMA", "GRANT_SHA256", "GRANT_OPERATION", "SOURCE_LITERAL_OPERATION",
    "TOPOLOGY_OPERATION", "TARGET_USE_OPERATION", "TARGET_USE_REF",
    "AuthorizedExecutionRefusal", "HumanGrant", "IssuedExecution",
    "authenticate_grant", "load_parquet_release", "issue_authorized_execution",
    "execute_issued", "preflight",
]
