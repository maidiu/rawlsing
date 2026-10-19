"""Exact adopted successor contracts for PRE553 predicate/runtime execution.

This module is intentionally authority-data driven.  It contains no source,
question, selector, workload-lane, or frozen-hash special cases.  Source-specific
facts enter only through exact adopted authority records supplied by the caller.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence
import zlib

from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import (
    Pre553AuthorityError,
    validate_authority_snapshot,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

R4A_DIALECT_SCHEMA = "EE_P2R4A_F02_PREDICATE_DIALECT_SEMANTICS_MATRIX@1.0.0"
R4A_RESPONDENT_SCHEMA = "EE_P2R4A_RESPONDENT_BINDING_COMPATIBILITY_AUTHORITY@1.0.0"
R4A_MIXED_SCHEMA = "EE_P2R4A_PARENT_CHILD_GRAMMAR_COMPOSITION_AUTHORITY@1.0.0"
R4A_DERIVED_SCHEMA = "EE_P2R4A_DERIVED_PREDICATE_AUTHORITY_CONTRACT@1.0.0"
R4A_SUCCESSOR_SCHEMA = "EE_P2R4A_PUBLIC_PREDICATE_SUCCESSOR_AUTHORITY_CANDIDATE@1.0.0"
R5A_REALIZATION_SCHEMA = "EE_P2R5A_RELEASE_REALIZATION_RELATION_AUTHORITY_CANDIDATE@1.0.0"
R5A_BINDING_SCHEMA = "EE_P2R5A_CONCRETE_REALIZATION_BINDING_SCHEMA@1.0.0"
R5A_PRECONDITION_SCHEMA = "EE_P2R5A_R4A_RELEASE_PRECONDITION_SUCCESSOR_CLAUSE@1.0.0"
I03_OPERATION_SUCCESSOR_SCHEMA = "FIABC_LITS_I_I03_OPERATION_SUCCESSOR_AUTHORITY@1.0.0"
EXACT_RISK_SET_SUCCESSOR_SCHEMA = "FIABC_LITS_I_D03_RISK_SET_SUCCESSOR_AUTHORITY@1.0.0"
EVENT_REPRESENTATION_SUCCESSOR_SCHEMA = (
    "FIABC_LITS_I_F02_EVENT_REPRESENTATION_SUCCESSOR_AUTHORITY@1.0.0"
)
CONCRETE_BINDING_SCHEMA = "RELEASE_REALIZATION_BINDING@1.0.0"
ACTIVE_POSITIVE_BINDING = "ACTIVE_POSITIVE"


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise Pre553AuthorityError(f"{name} must be an exact mapping")
    return value


def _sequence(value: Any, name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise Pre553AuthorityError(f"{name} must be an exact sequence")
    if not allow_empty and not value:
        raise Pre553AuthorityError(f"{name} may not be empty")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Pre553AuthorityError(f"{name} must be exact non-empty text")
    return value.strip()


def _hash_identity(record: Mapping[str, Any], declared_hash: str, name: str) -> str:
    if len(declared_hash) != 64:
        raise Pre553AuthorityError(f"{name} must declare one sha256 content identity")
    material = _mapping(record.get("identity_material"), f"{name}.identity_material")
    if semantic_hash(material) != declared_hash:
        raise Pre553AuthorityError(f"{name} identity_material hash mismatch")
    return declared_hash


def _canonical_json_scalar_member_token(value: Any, name: str) -> str:
    """Validate a JSON object member name used as a typed scalar token.

    JSON object member names are necessarily strings.  The dialect authority
    uses each member name as the canonical JSON serialization of the source
    scalar (for example, the member name ``1`` denotes integer 1, while
    ``\"1\"`` would denote string "1").  Preserve that typed distinction rather
    than serializing the member-name text a second time.
    """
    if not isinstance(value, str) or not value:
        raise Pre553AuthorityError(f"{name} must be a canonical JSON scalar token")
    try:
        decoded = json.loads(value)
        canonical = canonical_json(canonicalize(decoded))
    except (TypeError, ValueError) as exc:
        raise Pre553AuthorityError(
            f"{name} must be a canonical JSON scalar token"
        ) from exc
    if isinstance(decoded, (Mapping, list)) or canonical != value:
        raise Pre553AuthorityError(f"{name} must be a canonical JSON scalar token")
    return value


def _authority_key(ref: AuthorityRef | Mapping[str, Any]) -> str:
    return authority_ref(ref).key


def _exact_key(ref: ExactRef | Mapping[str, Any]) -> str:
    return exact_ref(ref).key


def _walk_release_refs(node: Mapping[str, Any]) -> tuple[ExactRef, ...]:
    refs: list[ExactRef] = []
    raw = node.get("release_ref")
    if raw is not None:
        ref = exact_ref(raw, "predicate leaf release_ref")
        if ref.kind == "C11LogicalRelease":
            refs.append(ref)
    children = node.get("children")
    if isinstance(children, Sequence) and not isinstance(children, (str, bytes, bytearray)):
        for child in children:
            if isinstance(child, Mapping):
                refs.extend(_walk_release_refs(child))
    return tuple(sorted(set(refs), key=lambda x: x.key))


@dataclass(frozen=True)
class PredicateDialectContract:
    grammar_ref: AuthorityRef
    leaf_type: str
    operation: str
    frozen_scope_ref: ExactRef
    truth_semantics: str
    question_value_hashes: Mapping[tuple[str, str], str]
    missing_is_false: bool

    def validate_leaf(self, node: Mapping[str, Any]) -> tuple[ExactRef, ExactRef, Any, ExactRef]:
        if node.get("op") != "LEAF" or node.get("leaf_type") != self.leaf_type:
            raise Pre553AuthorityError("predicate dialect leaf family does not match exact interpreter contract")
        if node.get("operation") != self.operation:
            raise Pre553AuthorityError("predicate dialect operation does not match exact interpreter contract")
        question_ref = exact_ref(node.get("question_ref"), "dialect.question_ref")
        response_ref = exact_ref(node.get("response_value_ref"), "dialect.response_value_ref")
        release_ref = exact_ref(node.get("release_ref"), "dialect.release_ref")
        if release_ref != self.frozen_scope_ref:
            raise Pre553AuthorityError("predicate dialect release/scope ref mismatch")
        if "source_native_value" not in node:
            raise Pre553AuthorityError("predicate dialect requires exact source_native_value")
        native_value = canonicalize(node["source_native_value"])
        expected = self.question_value_hashes.get(
            (question_ref.content_hash, canonical_json(native_value))
        )
        if expected is None or expected != response_ref.content_hash:
            raise Pre553AuthorityError("predicate dialect exact question/value binding mismatch")
        return question_ref, response_ref, native_value, release_ref


@dataclass(frozen=True)
class MixedCompositionContract:
    composition_ref: AuthorityRef
    allowed_input_grammar_refs: tuple[AuthorityRef, ...]
    parent_binding: str
    child_binding: str
    respondent_compatibility_hash: str
    frozen_scope_ref: ExactRef
    accepted_base_release_ref: ExactRef | None
    operation: str
    maximum_arity: int
    derived_contract_hash: str
    derived_binding_semantics: str

    @property
    def allowed_grammar_keys(self) -> frozenset[str]:
        return frozenset(ref.key for ref in self.allowed_input_grammar_refs)


@dataclass(frozen=True)
class MixedCompositionResolution:
    grammar_authority_ref: AuthorityRef
    respondent_binding_semantics: str
    authority_snapshot_ref: AuthorityRef
    replay_material: Mapping[str, Any]


@dataclass(frozen=True)
class ReleaseRealizationContract:
    authority_ref: ExactRef
    aggregate_ref: ExactRef
    frozen_scope_ref: ExactRef
    source_sha256: str
    accepted_base_release_ref: ExactRef
    binding_schema_ref: ExactRef
    binding_schema: Mapping[str, Any]
    required_proof_families: tuple[str, ...]


@dataclass(frozen=True)
class I03OperationSuccessorContract:
    authority_content_hash: str
    runtime_catalog_identity: str
    runtime_snapshot_content_hash: str
    parent_authority_ref: AuthorityRef
    parent_operation: str
    successor_operation: str
    source_universe_refs: tuple[ExactRef, ...]
    query_refs: tuple[ExactRef, ...]
    governed_object_families: tuple[str, ...]


@dataclass(frozen=True)
class ExactRiskSetSuccessorContract:
    authority_content_hash: str
    source_sha256: str
    row_count: int
    release_refs: tuple[ExactRef, ...]
    source_universe_ref: ExactRef
    risk_set_ref: ExactRef
    query_refs: tuple[ExactRef, ...]
    target_role_map: Mapping[tuple[str, ...], str]
    respondent_key_prefix: str
    member_ordinals: Mapping[str, frozenset[int]]
    canonical_roots: Mapping[str, str]

    def respondent_row_ordinal(self, respondent_key: str) -> int:
        if not isinstance(respondent_key, str) or not respondent_key.startswith(
            self.respondent_key_prefix
        ):
            raise Pre553AuthorityError(
                "respondent key is outside exact adopted risk-set identity law"
            )
        suffix = respondent_key[len(self.respondent_key_prefix):]
        if len(suffix) != 12 or not suffix.isdigit():
            raise Pre553AuthorityError(
                "respondent key lacks exact twelve-digit source-row ordinal"
            )
        row = int(suffix)
        if row < 1 or row > self.row_count:
            raise Pre553AuthorityError("respondent source-row ordinal is out of scope")
        return row

    def is_member(self, *, respondent_key: str, target_refs: Sequence[ExactRef]) -> bool:
        target_key = tuple(ref.key for ref in target_refs)
        root_id = self.target_role_map.get(target_key)
        if root_id is None:
            raise Pre553AuthorityError(
                "target tuple is outside exact adopted risk-set role map"
            )
        return self.respondent_row_ordinal(respondent_key) in self.member_ordinals[root_id]


@dataclass(frozen=True)
class EventRepresentationSuccessorContract:
    authority_content_hash: str
    source_sha256: str
    frozen_scope_ref: ExactRef
    runtime_release_ref: ExactRef
    bindings: Mapping[tuple[str, str, str], Any]


class Pre553RuntimeAuthoritySet:
    """Immutable exact successor-authority registry.

    The registry activates only records whose immutable content identities are
    explicitly listed as adopted.  It never searches for adjacent versions.
    """

    def __init__(
        self,
        *,
        adopted_authority_hashes: Iterable[str] = (),
        predicate_dialect_matrices: Iterable[Mapping[str, Any]] = (),
        respondent_compatibility_authorities: Iterable[Mapping[str, Any]] = (),
        mixed_composition_authorities: Iterable[Mapping[str, Any]] = (),
        derived_predicate_contracts: Iterable[Mapping[str, Any]] = (),
        public_predicate_successor_authorities: Iterable[Mapping[str, Any]] = (),
        i03_operation_successor_authorities: Iterable[Mapping[str, Any]] = (),
        exact_risk_set_successor_authorities: Iterable[Mapping[str, Any]] = (),
        event_representation_successor_authorities: Iterable[Mapping[str, Any]] = (),
        historical_authority_snapshots: Iterable[AuthoritySnapshot] = (),
        release_realization_authorities: Iterable[Mapping[str, Any]] = (),
        realization_binding_schemas: Iterable[Mapping[str, Any]] = (),
        release_precondition_clauses: Iterable[Mapping[str, Any]] = (),
        realization_bindings: Iterable[Mapping[str, Any]] = (),
    ) -> None:
        adopted = frozenset(_text(x, "adopted authority hash") for x in adopted_authority_hashes)
        self._adopted = adopted
        self._bindings = tuple(canonicalize(x) for x in realization_bindings)

        historical: dict[str, AuthoritySnapshot] = {}
        for raw_snapshot in historical_authority_snapshots:
            snapshot = validate_authority_snapshot(raw_snapshot)
            if snapshot.authority_ref.authority_content_hash not in adopted:
                raise Pre553AuthorityError(
                    "historical runtime authority snapshot is not exactly adopted"
                )
            if snapshot.authority_ref.key in historical:
                raise Pre553AuthorityError(
                    "duplicate exact historical runtime authority snapshot"
                )
            historical[snapshot.authority_ref.key] = snapshot
        self._historical_authority_snapshots = MappingProxyType(historical)

        i03_successors: list[I03OperationSuccessorContract] = []
        for raw in i03_operation_successor_authorities:
            record = _mapping(raw, "I03 operation successor authority")
            if record.get("schema") != I03_OPERATION_SUCCESSOR_SCHEMA:
                raise Pre553AuthorityError("unrecognized I03 operation successor authority schema")
            digest = _text(
                record.get("authority_content_hash"),
                "I03 operation successor authority hash",
            )
            _hash_identity(record, digest, "I03 operation successor authority")
            if digest not in adopted:
                raise Pre553AuthorityError(
                    "I03 operation successor authority is not exactly adopted"
                )
            material = _mapping(
                record.get("identity_material"),
                "I03 operation successor identity",
            )
            catalog_identity = _text(
                material.get("runtime_catalog_identity"),
                "I03 operation successor runtime catalog identity",
            )
            if len(catalog_identity) != 64:
                raise Pre553AuthorityError(
                    "I03 operation successor runtime catalog identity must be sha256"
                )
            snapshot_hash = _text(
                material.get("runtime_snapshot_content_hash"),
                "I03 operation successor runtime snapshot content hash",
            )
            if len(snapshot_hash) != 64:
                raise Pre553AuthorityError(
                    "I03 operation successor runtime snapshot hash must be sha256"
                )
            queries = tuple(sorted(
                (
                    exact_ref(ref, "I03 operation successor query ref")
                    for ref in _sequence(material.get("query_refs"), "I03 query refs")
                ),
                key=lambda ref: ref.key,
            ))
            universes = tuple(sorted(
                (
                    exact_ref(ref, "I03 operation successor universe ref")
                    for ref in _sequence(
                        material.get("source_universe_refs"),
                        "I03 source universe refs",
                    )
                ),
                key=lambda ref: ref.key,
            ))
            families = tuple(sorted(
                _text(value, "I03 governed object family")
                for value in _sequence(
                    material.get("governed_object_families"),
                    "I03 governed object families",
                )
            ))
            negative_limits = _sequence(
                material.get("negative_limits"),
                "I03 operation successor negative limits",
            )
            if "NO_GENERIC_OPERATION_ALIAS" not in negative_limits:
                raise Pre553AuthorityError(
                    "I03 operation successor must prohibit generic operation aliasing"
                )
            i03_successors.append(I03OperationSuccessorContract(
                authority_content_hash=digest,
                runtime_catalog_identity=catalog_identity,
                runtime_snapshot_content_hash=snapshot_hash,
                parent_authority_ref=authority_ref(
                    material.get("parent_authority_ref"),
                    "I03 parent authority ref",
                ),
                parent_operation=_text(
                    material.get("parent_operation"), "I03 parent operation"
                ),
                successor_operation=_text(
                    material.get("successor_operation"), "I03 successor operation"
                ),
                source_universe_refs=universes,
                query_refs=queries,
                governed_object_families=families,
            ))
        self._i03_operation_successors = tuple(sorted(
            i03_successors, key=lambda contract: contract.authority_content_hash
        ))

        risk_set_successors: list[ExactRiskSetSuccessorContract] = []
        for raw in exact_risk_set_successor_authorities:
            record = _mapping(raw, "exact risk-set successor authority")
            if record.get("schema") != EXACT_RISK_SET_SUCCESSOR_SCHEMA:
                raise Pre553AuthorityError(
                    "unrecognized exact risk-set successor authority schema"
                )
            digest = _text(
                record.get("authority_content_hash"),
                "exact risk-set successor authority hash",
            )
            _hash_identity(record, digest, "exact risk-set successor authority")
            if digest not in adopted:
                raise Pre553AuthorityError(
                    "exact risk-set successor authority is not exactly adopted"
                )
            material = _mapping(
                record.get("identity_material"), "exact risk-set successor identity"
            )
            row_count = material.get("row_count")
            if (
                not isinstance(row_count, int)
                or isinstance(row_count, bool)
                or row_count < 1
            ):
                raise Pre553AuthorityError(
                    "exact risk-set successor row_count must be positive integer"
                )
            source_sha = _text(material.get("source_sha256"), "risk-set source sha256")
            if len(source_sha) != 64:
                raise Pre553AuthorityError("risk-set source identity must be sha256")
            queries = tuple(sorted(
                (
                    exact_ref(ref, "exact risk-set successor query ref")
                    for ref in _sequence(material.get("query_refs"), "risk-set query refs")
                ),
                key=lambda ref: ref.key,
            ))
            target_roles: dict[tuple[str, ...], str] = {}
            for role in _sequence(material.get("target_role_map"), "target role map"):
                role = _mapping(role, "target role")
                targets = tuple(
                    exact_ref(ref, "target role exact ref").key
                    for ref in _sequence(role.get("target_refs"), "target role refs")
                )
                root_id = _text(role.get("root_id"), "target role root id")
                if targets in target_roles:
                    raise Pre553AuthorityError("duplicate exact target role tuple")
                target_roles[targets] = root_id

            accepted = _mapping(material.get("accepted_d03"), "accepted D03 material")
            layout = _mapping(accepted.get("payload_layout"), "D03 payload layout")
            if layout.get("encoding") != "ZLIB9_BASE64" or layout.get("row_count") != row_count:
                raise Pre553AuthorityError("D03 payload encoding/layout drift")
            payload_text = _text(record.get("payload_base64"), "D03 payload base64")
            try:
                compressed = base64.b64decode(payload_text, validate=True)
            except Exception as exc:
                raise Pre553AuthorityError("D03 payload base64 is malformed") from exc
            if hashlib.sha256(compressed).hexdigest() != accepted.get("compressed_sha256"):
                raise Pre553AuthorityError("D03 compressed payload identity drift")
            try:
                payload = zlib.decompress(compressed)
            except zlib.error as exc:
                raise Pre553AuthorityError("D03 payload decompression failed") from exc
            if (
                len(payload) != accepted.get("raw_payload_length")
                or hashlib.sha256(payload).hexdigest() != accepted.get("raw_payload_sha256")
            ):
                raise Pre553AuthorityError("D03 raw payload identity drift")

            def segment(offset_name: str, length_name: str) -> bytes:
                offset, length = layout.get(offset_name), layout.get(length_name)
                if (
                    not isinstance(offset, int) or isinstance(offset, bool) or offset < 0
                    or not isinstance(length, int) or isinstance(length, bool) or length < 1
                    or offset + length > len(payload)
                ):
                    raise Pre553AuthorityError("D03 payload segment bounds drift")
                return payload[offset:offset + length]

            def two_bit_members(data: bytes) -> frozenset[int]:
                code = layout.get("two_bit_member_code")
                if code != 0 or len(data) * 4 < row_count:
                    raise Pre553AuthorityError("D03 two-bit member layout drift")
                return frozenset(
                    row for row in range(1, row_count + 1)
                    if ((data[(row - 1) // 4] >> (6 - 2 * ((row - 1) % 4))) & 3) == code
                )

            def bit_members(data: bytes) -> frozenset[int]:
                code = layout.get("bit_member_code")
                if code != 1 or len(data) * 8 < row_count:
                    raise Pre553AuthorityError("D03 one-bit member layout drift")
                return frozenset(
                    row for row in range(1, row_count + 1)
                    if ((data[(row - 1) // 8] >> (7 - ((row - 1) % 8))) & 1) == code
                )

            members = {
                "R2": two_bit_members(segment("r2_offset", "r2_length")),
                "R7": two_bit_members(segment("r7_offset", "r7_length")),
                "R27": bit_members(segment("r27_offset", "r27_length")),
            }
            roots_doc = _mapping(accepted.get("roots"), "accepted D03 roots")
            roots: dict[str, str] = {}
            header = b"source_sha256\tone_based_source_row_ordinal\n"
            for root_id, ordinals in members.items():
                root = _mapping(roots_doc.get(root_id), f"accepted D03 {root_id}")
                if len(ordinals) != root.get("member_count"):
                    raise Pre553AuthorityError(f"D03 {root_id} member count drift")
                expanded = bytearray(header)
                for row in sorted(ordinals):
                    expanded.extend(f"{source_sha}\t{row}\n".encode("ascii"))
                observed_root = hashlib.sha256(expanded).hexdigest()
                if observed_root != root.get("canonical_full_tsv_sha256"):
                    raise Pre553AuthorityError(f"D03 {root_id} canonical root drift")
                roots[root_id] = observed_root
            if members["R27"] != members["R2"] & members["R7"]:
                raise Pre553AuthorityError("D03 R27 is not exact R2/R7 intersection")
            if set(target_roles.values()) != set(members):
                raise Pre553AuthorityError("D03 target role map is not exact R2/R7/R27")
            negative_limits = set(
                _text(item, "risk-set negative limit")
                for item in _sequence(material.get("negative_limits"), "risk-set negative limits")
            )
            required_limits = {
                "NO_CURRENT_SOURCE_VALUE_DERIVATION",
                "NO_GENERIC_MISSINGNESS_OR_DENOMINATOR_RULE",
                "NO_CANDIDATE_OUTPUT_PARENTAGE",
                "NO_C11_RELEASE_MUTATION",
            }
            if not required_limits <= negative_limits:
                raise Pre553AuthorityError("exact risk-set negative limits are incomplete")
            release_refs = tuple(sorted(
                (
                    exact_ref(ref, "risk-set release ref")
                    for ref in _sequence(
                        material.get("release_refs"), "risk-set release refs"
                    )
                ),
                key=lambda ref: ref.key,
            ))
            if len(set(release_refs)) != len(release_refs):
                raise Pre553AuthorityError("duplicate exact risk-set release ref")
            risk_set_successors.append(ExactRiskSetSuccessorContract(
                authority_content_hash=digest,
                source_sha256=source_sha,
                row_count=row_count,
                release_refs=release_refs,
                source_universe_ref=exact_ref(
                    material.get("source_universe_ref"), "risk-set universe ref"
                ),
                risk_set_ref=exact_ref(material.get("risk_set_ref"), "risk-set ref"),
                query_refs=queries,
                target_role_map=MappingProxyType(target_roles),
                respondent_key_prefix=_text(
                    material.get("respondent_key_prefix"), "respondent key prefix"
                ),
                member_ordinals=MappingProxyType(members),
                canonical_roots=MappingProxyType(roots),
            ))
        self._exact_risk_set_successors = tuple(sorted(
            risk_set_successors, key=lambda contract: contract.authority_content_hash
        ))

        event_representation_successors: list[EventRepresentationSuccessorContract] = []
        for raw in event_representation_successor_authorities:
            record = _mapping(raw, "event representation successor authority")
            if record.get("schema") != EVENT_REPRESENTATION_SUCCESSOR_SCHEMA:
                raise Pre553AuthorityError(
                    "unrecognized event representation successor authority schema"
                )
            digest = _text(
                record.get("authority_content_hash"),
                "event representation successor authority hash",
            )
            _hash_identity(record, digest, "event representation successor authority")
            if digest not in adopted:
                raise Pre553AuthorityError(
                    "event representation successor authority is not exactly adopted"
                )
            material = _mapping(
                record.get("identity_material"),
                "event representation successor identity",
            )
            source_sha = _text(
                material.get("source_sha256"),
                "event representation source sha256",
            )
            if len(source_sha) != 64:
                raise Pre553AuthorityError(
                    "event representation source identity must be sha256"
                )
            bindings: dict[tuple[str, str, str], Any] = {}
            for item in _sequence(
                material.get("bindings"), "event representation bindings"
            ):
                item = _mapping(item, "event representation binding")
                if item.get("required_event_state") != "SUBSTANTIVE_RESPONSE":
                    raise Pre553AuthorityError(
                        "event representation binding state is not exact substantive response"
                    )
                question_ref = exact_ref(
                    item.get("question_ref"), "event representation question ref"
                )
                response_ref = exact_ref(
                    item.get("response_value_ref"),
                    "event representation response-value ref",
                )
                native_value = canonicalize(item.get("source_native_value"))
                key = (
                    question_ref.key,
                    response_ref.key,
                    canonical_json(native_value),
                )
                if key in bindings:
                    raise Pre553AuthorityError(
                        "duplicate exact event representation binding"
                    )
                bindings[key] = canonicalize(
                    item.get("exact_event_raw_response_value")
                )
            negative_limits = set(
                _text(item, "event representation negative limit")
                for item in _sequence(
                    material.get("negative_limits"),
                    "event representation negative limits",
                )
            )
            required_limits = {
                "NO_GENERIC_INT_FLOAT_DECIMAL_COERCION",
                "NO_STRING_NUMERIC_EQUIVALENCE",
                "NO_OTHER_SOURCE_RELEASE_SCOPE_QUESTION_VALUE_OR_STATE",
                "NO_C11_EVENT_OR_RELEASE_MUTATION",
                "NO_CANDIDATE_OUTPUT_PARENTAGE",
            }
            if not required_limits <= negative_limits:
                raise Pre553AuthorityError(
                    "event representation negative limits are incomplete"
                )
            event_representation_successors.append(
                EventRepresentationSuccessorContract(
                    authority_content_hash=digest,
                    source_sha256=source_sha,
                    frozen_scope_ref=exact_ref(
                        material.get("frozen_scope_ref"),
                        "event representation frozen scope ref",
                    ),
                    runtime_release_ref=exact_ref(
                        material.get("runtime_release_ref"),
                        "event representation runtime release ref",
                    ),
                    bindings=MappingProxyType(bindings),
                )
            )
        self._event_representation_successors = tuple(sorted(
            event_representation_successors,
            key=lambda contract: contract.authority_content_hash,
        ))

        compat: dict[str, Mapping[str, Any]] = {}
        for raw in respondent_compatibility_authorities:
            record = _mapping(raw, "respondent compatibility authority")
            if record.get("schema") != R4A_RESPONDENT_SCHEMA:
                raise Pre553AuthorityError("unrecognized respondent compatibility authority schema")
            digest = _text(record.get("authority_content_hash"), "respondent authority hash")
            _hash_identity(record, digest, "respondent compatibility authority")
            if digest not in adopted:
                raise Pre553AuthorityError("respondent compatibility authority is not exactly adopted")
            compat[digest] = record

        mixed: dict[str, Mapping[str, Any]] = {}
        for raw in mixed_composition_authorities:
            record = _mapping(raw, "mixed composition authority")
            if record.get("schema") != R4A_MIXED_SCHEMA:
                raise Pre553AuthorityError("unrecognized mixed composition authority schema")
            digest = _text(record.get("authority_content_hash"), "mixed composition authority hash")
            _hash_identity(record, digest, "mixed composition authority")
            if digest not in adopted:
                raise Pre553AuthorityError("mixed composition authority is not exactly adopted")
            mixed[digest] = record

        derived: dict[str, Mapping[str, Any]] = {}
        for raw in derived_predicate_contracts:
            record = _mapping(raw, "derived predicate authority")
            if record.get("schema") != R4A_DERIVED_SCHEMA:
                raise Pre553AuthorityError("unrecognized derived predicate authority schema")
            digest = _text(record.get("contract_content_hash"), "derived authority hash")
            _hash_identity(record, digest, "derived predicate authority")
            if digest not in adopted:
                raise Pre553AuthorityError("derived predicate authority is not exactly adopted")
            derived[digest] = record

        dialect_records = tuple(_mapping(x, "predicate dialect matrix") for x in predicate_dialect_matrices)
        for record in dialect_records:
            if record.get("schema") != R4A_DIALECT_SCHEMA:
                raise Pre553AuthorityError("unrecognized predicate dialect matrix schema")

        dialects: dict[tuple[str, str], PredicateDialectContract] = {}
        compositions: dict[str, MixedCompositionContract] = {}
        for raw in public_predicate_successor_authorities:
            successor = _mapping(raw, "public predicate successor authority")
            if successor.get("schema") != R4A_SUCCESSOR_SCHEMA:
                raise Pre553AuthorityError("unrecognized public predicate successor authority schema")
            successor_hash = _text(
                successor.get("authority_candidate_content_hash"), "public predicate successor hash"
            )
            _hash_identity(successor, successor_hash, "public predicate successor authority")
            if successor_hash not in adopted:
                raise Pre553AuthorityError("public predicate successor authority is not exactly adopted")
            material = _mapping(successor["identity_material"], "public predicate successor identity")

            compat_hash = exact_ref(
                material.get("respondent_binding_compatibility_ref"),
                "respondent compatibility ref",
            ).content_hash
            mixed_ref = authority_ref(material.get("mixed_grammar_authority_ref"), "mixed grammar authority ref")
            mixed_hash = mixed_ref.authority_content_hash
            derived_hash = exact_ref(
                material.get("derived_predicate_contract_ref"), "derived predicate contract ref"
            ).content_hash
            if compat_hash not in compat or mixed_hash not in mixed or derived_hash not in derived:
                raise Pre553AuthorityError("public predicate successor exact linked authority is unavailable")
            if not {compat_hash, mixed_hash, derived_hash} <= adopted:
                raise Pre553AuthorityError("public predicate successor linked authority is not adopted")

            mixed_material = _mapping(mixed[mixed_hash]["identity_material"], "mixed identity")
            compat_material = _mapping(compat[compat_hash]["identity_material"], "compatibility identity")
            derived_material = _mapping(derived[derived_hash]["identity_material"], "derived identity")
            if authority_ref(mixed[mixed_hash]["candidate_authority_ref"]) != mixed_ref:
                raise Pre553AuthorityError("mixed composition authority exact ref mismatch")
            if exact_ref(
                derived_material.get("respondent_binding_compatibility_ref")
            ).content_hash != compat_hash:
                raise Pre553AuthorityError("derived authority respondent compatibility link mismatch")
            if authority_ref(derived_material.get("composition_authority_ref")) != mixed_ref:
                raise Pre553AuthorityError("derived authority composition link mismatch")

            allowed = tuple(
                sorted(
                    (authority_ref(x, "allowed input grammar ref") for x in _sequence(
                        mixed_material.get("allowed_input_grammar_refs"),
                        "allowed_input_grammar_refs",
                    )),
                    key=lambda x: x.key,
                )
            )
            permitted = _mapping(
                mixed_material.get("permitted_mixed_composition"),
                "permitted_mixed_composition",
            )
            operation = _text(permitted.get("ast_operation"), "mixed ast operation")
            maximum_arity = permitted.get("maximum_arity")
            if not isinstance(maximum_arity, int) or isinstance(maximum_arity, bool) or maximum_arity < 2:
                raise Pre553AuthorityError("mixed composition maximum_arity must be exact integer >= 2")
            scope = _mapping(mixed_material.get("exact_workload_scope"), "mixed exact workload scope")
            frozen_scope = exact_ref(scope.get("release_ref"), "mixed frozen scope release")
            compat_scope = _mapping(compat_material.get("exact_scope"), "respondent compatibility scope")
            base_raw = compat_scope.get("base_release_ref")
            base_ref = exact_ref(base_raw, "accepted base release") if base_raw is not None else None
            if exact_ref(compat_scope.get("release_ref"), "compatibility release") != frozen_scope:
                raise Pre553AuthorityError("mixed and respondent compatibility scopes disagree")
            bindings = (compat_material.get("parent_binding"), compat_material.get("child_binding"))
            if not all(isinstance(x, str) and x for x in bindings):
                raise Pre553AuthorityError("respondent compatibility requires exact parent/child bindings")
            derived_binding = _text(
                _mapping(
                    derived_material.get("deterministic_construction"),
                    "derived deterministic construction",
                ).get("same_respondent_binding_semantics"),
                "derived respondent binding semantics",
            )
            compositions[mixed_ref.key] = MixedCompositionContract(
                composition_ref=mixed_ref,
                allowed_input_grammar_refs=allowed,
                parent_binding=bindings[0],
                child_binding=bindings[1],
                respondent_compatibility_hash=compat_hash,
                frozen_scope_ref=frozen_scope,
                accepted_base_release_ref=base_ref,
                operation=operation,
                maximum_arity=maximum_arity,
                derived_contract_hash=derived_hash,
                derived_binding_semantics=derived_binding,
            )

            evaluator = _mapping(material.get("evaluator_successor_contract"), "evaluator successor contract")
            child_operation = _text(evaluator.get("child_operation"), "child operation")
            leaf_families = _sequence(mixed_material.get("leaf_operation_families"), "leaf operation families")
            child_entries = [
                _mapping(x, "leaf operation family") for x in leaf_families
                if isinstance(x, Mapping) and x.get("exact_operation") == child_operation
            ]
            if len(child_entries) != 1:
                raise Pre553AuthorityError("exact child interpreter grammar cannot be resolved uniquely")
            child_grammar = authority_ref(child_entries[0].get("grammar_ref"), "child grammar ref")
            matrices = [
                m for m in dialect_records
                if m.get("operation") == child_operation
                and exact_ref(_mapping(m.get("exact_scope"), "dialect exact scope").get("release_ref")) == frozen_scope
            ]
            if len(matrices) != 1:
                raise Pre553AuthorityError("exact adopted predicate dialect matrix cannot be resolved uniquely")
            matrix = matrices[0]
            qv: dict[tuple[str, str], str] = {}
            for binding in _mapping(
                matrix.get("exact_question_value_bindings"), "exact question/value bindings"
            ).values():
                item = _mapping(binding, "question/value binding")
                qhash = _text(item.get("question_content_hash"), "question content hash")
                for native, response_hash in _mapping(item.get("values"), "response values").items():
                    key = (
                        qhash,
                        _canonical_json_scalar_member_token(
                            native, "response value native scalar token"
                        ),
                    )
                    response_hash = _text(response_hash, "response value content hash")
                    prior = qv.get(key)
                    if prior is not None and prior != response_hash:
                        raise Pre553AuthorityError("predicate dialect question/value authority conflicts")
                    qv[key] = response_hash
            law = _mapping(matrix.get("interpretation_law"), "dialect interpretation law")
            contract = PredicateDialectContract(
                grammar_ref=child_grammar,
                leaf_type=_text(matrix.get("leaf_family"), "dialect leaf family"),
                operation=child_operation,
                frozen_scope_ref=frozen_scope,
                truth_semantics=_text(law.get("operator_semantics"), "dialect truth semantics"),
                question_value_hashes=MappingProxyType(qv),
                missing_is_false=law.get("missing_is_false") is True,
            )
            dialects[(child_grammar.key, child_operation)] = contract

        schemas: dict[str, Mapping[str, Any]] = {}
        for raw in realization_binding_schemas:
            record = _mapping(raw, "realization binding schema")
            if record.get("schema") != R5A_BINDING_SCHEMA:
                raise Pre553AuthorityError("unrecognized realization binding schema")
            schema_ref = exact_ref(record.get("schema_ref"), "realization binding schema ref")
            _hash_identity(record, schema_ref.content_hash, "realization binding schema")
            if schema_ref.content_hash not in adopted:
                raise Pre553AuthorityError("realization binding schema is not exactly adopted")
            schemas[schema_ref.content_hash] = record

        clauses: dict[str, Mapping[str, Any]] = {}
        for raw in release_precondition_clauses:
            record = _mapping(raw, "release precondition clause")
            if record.get("schema") != R5A_PRECONDITION_SCHEMA:
                raise Pre553AuthorityError("unrecognized release precondition clause schema")
            clause_ref = exact_ref(record.get("clause_ref"), "release precondition clause ref")
            _hash_identity(record, clause_ref.content_hash, "release precondition clause")
            if clause_ref.content_hash not in adopted:
                raise Pre553AuthorityError("release precondition clause is not exactly adopted")
            clauses[clause_ref.content_hash] = record

        realizations: dict[str, ReleaseRealizationContract] = {}
        for raw in release_realization_authorities:
            record = _mapping(raw, "release realization authority")
            if record.get("schema") != R5A_REALIZATION_SCHEMA:
                raise Pre553AuthorityError("unrecognized release realization authority schema")
            rel_ref = exact_ref(record.get("authority_ref"), "release realization authority ref")
            _hash_identity(record, rel_ref.content_hash, "release realization authority")
            aggregate_ref = exact_ref(record.get("aggregate_candidate_ref"), "realization aggregate ref")
            if rel_ref.content_hash not in adopted or aggregate_ref.content_hash not in adopted:
                raise Pre553AuthorityError("release realization authority/aggregate is not exactly adopted")
            material = _mapping(record.get("identity_material"), "release realization identity")
            frozen_scope = exact_ref(material.get("frozen_scope_anchor"), "frozen scope anchor")
            base_ref = exact_ref(material.get("accepted_base_i02_release"), "accepted base release")
            source_sha = _text(material.get("source_sha256"), "source sha256")

            candidates = [
                s for s in schemas.values()
                if _mapping(s.get("identity_material"), "binding schema identity").get(
                    "relation_authority_candidate_hash"
                ) == rel_ref.content_hash
            ]
            if len(candidates) != 1:
                raise Pre553AuthorityError("exact realization binding schema cannot be resolved uniquely")
            schema = candidates[0]
            schema_ref = exact_ref(schema.get("schema_ref"), "binding schema ref")
            matching_clauses = []
            for clause in clauses.values():
                cm = _mapping(clause.get("identity_material"), "release precondition identity")
                if (
                    cm.get("relation_authority_candidate_hash") == rel_ref.content_hash
                    and cm.get("binding_schema_hash") == schema_ref.content_hash
                    and exact_ref(cm.get("frozen_scope_anchor"), "clause frozen scope") == frozen_scope
                ):
                    matching_clauses.append(clause)
            if len(matching_clauses) != 1:
                raise Pre553AuthorityError("exact adopted release precondition successor clause unavailable")
            clause_material = _mapping(matching_clauses[0]["identity_material"], "precondition clause identity")
            r4a_hash = _text(clause_material.get("adopted_r4a_aggregate_hash"), "linked R4A aggregate hash")
            if r4a_hash not in adopted:
                raise Pre553AuthorityError("release realization clause does not link an adopted R4A aggregate")

            required_families = tuple(
                _text(x, "required proof family")
                for x in _sequence(
                    _mapping(schema.get("identity_material"), "binding schema identity").get(
                        "required_proof_families"
                    ),
                    "required proof families",
                )
            )
            realizations[frozen_scope.key] = ReleaseRealizationContract(
                authority_ref=rel_ref,
                aggregate_ref=aggregate_ref,
                frozen_scope_ref=frozen_scope,
                source_sha256=source_sha,
                accepted_base_release_ref=base_ref,
                binding_schema_ref=schema_ref,
                binding_schema=MappingProxyType(dict(schema)),
                required_proof_families=required_families,
            )

        self._dialects = MappingProxyType(dialects)
        self._compositions = MappingProxyType(compositions)
        self._realizations = MappingProxyType(realizations)

    def is_positive_runtime_predicate_authority(self, ref: AuthorityRef | Mapping[str, Any]) -> bool:
        exact = authority_ref(ref)
        if exact.key in self._compositions:
            return True
        return any(grammar_key == exact.key for grammar_key, _ in self._dialects)

    def resolve_exact_runtime_authority(
        self, ref: AuthorityRef | Mapping[str, Any]
    ) -> AuthoritySnapshot | None:
        """Return only an explicitly adopted exact historical snapshot."""
        exact = authority_ref(ref, "historical runtime authority ref")
        return self._historical_authority_snapshots.get(exact.key)

    def authorize_i03_operation_successor(
        self,
        *,
        snapshot: AuthoritySnapshot,
        query: EmpiricalQuerySpec,
        requested_operation: str,
        universe_refs: Iterable[ExactRef],
        required_object_family: str,
        runtime_catalog_identity: str | None = None,
        historical_parent_snapshot: AuthoritySnapshot | None = None,
    ) -> I03OperationSuccessorContract:
        """Resolve one exact adopted operation-successor record or fail closed."""
        if not isinstance(snapshot, AuthoritySnapshot):
            raise Pre553AuthorityError("I03 operation successor requires AuthoritySnapshot")
        if not isinstance(query, EmpiricalQuerySpec):
            raise Pre553AuthorityError("I03 operation successor requires EmpiricalQuerySpec")
        catalog_identity = _text(
            runtime_catalog_identity,
            "I03 operation successor runtime catalog identity",
        )
        if (
            len(catalog_identity) != 64
            or any(ch not in "0123456789abcdef" for ch in catalog_identity)
        ):
            raise Pre553AuthorityError(
                "I03 operation successor runtime catalog identity must be exact sha256"
            )
        if historical_parent_snapshot is not None and not isinstance(
            historical_parent_snapshot, AuthoritySnapshot
        ):
            raise Pre553AuthorityError(
                "I03 operation successor historical parent must be AuthoritySnapshot"
            )
        operation = _text(requested_operation, "requested I03 successor operation")
        family = _text(required_object_family, "required I03 object family")
        universes = tuple(sorted(set(universe_refs), key=lambda ref: ref.key))
        matches = [
            contract
            for contract in self._i03_operation_successors
            if contract.runtime_catalog_identity == catalog_identity
            and contract.parent_authority_ref == snapshot.authority_ref
            and contract.runtime_snapshot_content_hash == snapshot.content_hash
            and contract.successor_operation == operation
            and query.ref in contract.query_refs
            and contract.source_universe_refs == universes
            and family in contract.governed_object_families
        ]
        if len(matches) != 1:
            raise Pre553AuthorityError(
                "no unique exact adopted I03 operation successor authority"
            )
        contract = matches[0]
        if snapshot.authority_kind != "PREDICATE_GRAMMAR" or snapshot.decision_state != "ALLOW":
            raise Pre553AuthorityError(
                "I03 operation successor runtime snapshot is not positive predicate authority"
            )
        if historical_parent_snapshot is None:
            raise Pre553AuthorityError(
                "I03 operation successor exact historical parent snapshot is required"
            )
        adopted_parent = self.resolve_exact_runtime_authority(
            contract.parent_authority_ref
        )
        if (
            adopted_parent is None
            or historical_parent_snapshot != adopted_parent
            or historical_parent_snapshot.authority_ref
            != contract.parent_authority_ref
        ):
            raise Pre553AuthorityError(
                "I03 operation successor historical parent snapshot is not exactly adopted"
            )
        if (
            historical_parent_snapshot.authority_kind != "PREDICATE_GRAMMAR"
            or historical_parent_snapshot.decision_state != "ALLOW"
        ):
            raise Pre553AuthorityError(
                "I03 operation successor historical parent is not positive predicate authority"
            )
        if contract.parent_operation not in historical_parent_snapshot.governed_operations:
            raise Pre553AuthorityError(
                "I03 operation successor parent operation is absent from exact historical authority"
            )
        query_authorities = {
            authority_ref(ref, "query authority ref") for ref in query.query_authority_refs
        }
        if contract.parent_authority_ref not in query_authorities:
            raise Pre553AuthorityError(
                "I03 operation successor parent authority is absent from exact query"
            )
        return contract

    def resolve_exact_risk_set_successor(
        self,
        *,
        query: EmpiricalQuerySpec,
        release_ref: ExactRef,
        source_universe_ref: ExactRef,
        risk_set_ref: ExactRef,
        target_refs: Sequence[ExactRef],
    ) -> ExactRiskSetSuccessorContract | None:
        """Resolve only one adopted exact risk-set extension for this query scope."""
        matches = [
            contract
            for contract in self._exact_risk_set_successors
            if query.ref in contract.query_refs
            and release_ref in contract.release_refs
            and source_universe_ref == contract.source_universe_ref
            and risk_set_ref == contract.risk_set_ref
            and tuple(ref.key for ref in target_refs) in contract.target_role_map
        ]
        if not matches:
            return None
        if len(matches) != 1:
            raise Pre553AuthorityError(
                "multiple adopted exact risk-set successor authorities match"
            )
        return matches[0]

    def resolve_predicate_dialect(
        self,
        grammar_ref: AuthorityRef | Mapping[str, Any],
        node: Mapping[str, Any],
    ) -> PredicateDialectContract:
        grammar = authority_ref(grammar_ref, "predicate grammar authority")
        operation = node.get("operation")
        if not isinstance(operation, str) or not operation:
            raise Pre553AuthorityError("governed predicate dialect requires exact operation")
        contract = self._dialects.get((grammar.key, operation))
        if contract is not None:
            return contract

        mixed = self._compositions.get(grammar.key)
        if mixed is not None:
            allowed = set(mixed.allowed_grammar_keys)
            matches = [
                dialect
                for (grammar_key, dialect_operation), dialect in self._dialects.items()
                if grammar_key in allowed and dialect_operation == operation
            ]
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                raise Pre553AuthorityError(
                    "mixed successor grammar resolves multiple child dialect interpreters")
        raise Pre553AuthorityError("no exact adopted predicate dialect interpreter authority")

    def match_exact_event_representation(
        self,
        *,
        frozen_scope_ref: ExactRef,
        runtime_release_ref: ExactRef,
        question_ref: ExactRef,
        response_value_ref: ExactRef,
        source_native_value: Any,
        event_raw_response_value: Any,
    ) -> bool:
        """Match one authority-declared successor event witness, if applicable."""
        native = canonicalize(source_native_value)
        observed = canonicalize(event_raw_response_value)
        if observed == native:
            return True
        key = (
            question_ref.key,
            response_value_ref.key,
            canonical_json(native),
        )
        scoped = [
            contract
            for contract in self._event_representation_successors
            if contract.frozen_scope_ref == frozen_scope_ref
            and contract.runtime_release_ref == runtime_release_ref
            and key in contract.bindings
        ]
        if not scoped:
            return False
        if len(scoped) != 1:
            raise Pre553AuthorityError(
                "multiple exact event representation successor authorities match"
            )
        contract = scoped[0]
        if contract.bindings[key] == observed:
            return True
        authorized_question_witnesses = {
            canonical_json(witness)
            for binding_key, witness in contract.bindings.items()
            if binding_key[0] == question_ref.key
        }
        if canonical_json(observed) in authorized_question_witnesses:
            return False
        raise Pre553AuthorityError(
            "runtime event witness differs from exact adopted representation"
        )

    def validate_predicate(self, predicate: EmpiricalPredicate) -> None:
        grammar = authority_ref(predicate.grammar_authority_ref, "predicate grammar authority")
        contract = self._compositions.get(grammar.key)
        if contract is not None:
            if predicate.predicate_ast.get("op") != contract.operation:
                raise Pre553AuthorityError(
                    "mixed predicate operation is not granted by exact composition authority")
            if predicate.same_respondent_binding_semantics != contract.derived_binding_semantics:
                raise Pre553AuthorityError(
                    "mixed derived predicate respondent binding does not match successor authority")
            release_refs = set(_walk_release_refs(predicate.predicate_ast))
            release_refs.update(
                exact_ref(x, "predicate scope ref")
                for x in predicate.scope_refs
                if isinstance(x, (ExactRef, Mapping))
                and exact_ref(x, "predicate scope ref").kind == "C11LogicalRelease"
            )
            if contract.frozen_scope_ref not in release_refs:
                raise Pre553AuthorityError(
                    "mixed derived predicate lacks exact frozen release scope")
            return

        dialects = {
            operation: dialect
            for (grammar_key, operation), dialect in self._dialects.items()
            if grammar_key == grammar.key
        }
        if not dialects:
            raise Pre553AuthorityError(
                "predicate grammar is not one exact adopted runtime grammar")

        def walk(node: Mapping[str, Any]) -> None:
            op = node.get("op")
            if op == "LEAF":
                operation = node.get("operation")
                if operation not in dialects:
                    raise Pre553AuthorityError(
                        "predicate leaf operation lacks exact adopted dialect authority")
                dialects[operation].validate_leaf(node)
                return
            children = node.get("children")
            if (
                op not in {"AND", "OR", "NOT"}
                or not isinstance(children, Sequence)
                or isinstance(children, (str, bytes, bytearray))
            ):
                raise Pre553AuthorityError("runtime predicate AST is not governed")
            for child in children:
                walk(_mapping(child, "runtime predicate child"))

        walk(_mapping(predicate.predicate_ast, "runtime predicate AST"))

    def authorize_mixed_predicate_composition(
        self,
        predicates: Sequence[EmpiricalPredicate],
        *,
        operation: str,
        tag_material: Any,
    ) -> MixedCompositionResolution:
        if len(predicates) < 2:
            raise Pre553AuthorityError("mixed composition requires at least two predicates")
        matches: list[MixedCompositionContract] = []
        grammar_refs = tuple(
            authority_ref(p.grammar_authority_ref, "input predicate grammar authority")
            for p in predicates
        )
        binding_set = {p.same_respondent_binding_semantics for p in predicates}
        for contract in self._compositions.values():
            if operation != contract.operation or len(predicates) > contract.maximum_arity:
                continue
            permitted_keys = set(contract.allowed_grammar_keys)
            permitted_keys.add(contract.composition_ref.key)
            if any(ref.key not in permitted_keys for ref in grammar_refs):
                continue
            if contract.composition_ref.key not in {r.key for r in grammar_refs}:
                if {r.key for r in grammar_refs} != set(contract.allowed_grammar_keys):
                    continue
                if binding_set != {contract.parent_binding, contract.child_binding}:
                    continue
            else:
                for p in predicates:
                    if authority_ref(p.grammar_authority_ref).key == contract.composition_ref.key:
                        self.validate_predicate(p)
                if not binding_set <= {
                    contract.parent_binding,
                    contract.child_binding,
                    contract.derived_binding_semantics,
                }:
                    continue

            release_refs: set[ExactRef] = set()
            for predicate in predicates:
                release_refs.update(_walk_release_refs(predicate.predicate_ast))
                for raw in predicate.scope_refs:
                    try:
                        ref = exact_ref(raw, "predicate scope ref")
                    except Exception:
                        continue
                    if ref.kind == "C11LogicalRelease":
                        release_refs.add(ref)
            allowed_releases = {contract.frozen_scope_ref}
            if contract.accepted_base_release_ref is not None:
                allowed_releases.add(contract.accepted_base_release_ref)
            if contract.frozen_scope_ref not in release_refs:
                continue
            if any(ref not in allowed_releases for ref in release_refs):
                continue
            matches.append(contract)

        if len(matches) != 1:
            raise Pre553AuthorityError(
                "mixed predicate composition lacks one exact positive adopted compatibility/composition authority"
            )
        contract = matches[0]
        ordered_refs = tuple(sorted((p.ref for p in predicates), key=lambda x: x.key))
        replay_material = canonicalize({
            "composition_authority_ref": contract.composition_ref.as_dict(),
            "operation": operation,
            "ordered_input_predicate_refs": [ref.as_dict() for ref in ordered_refs],
            "tag_material": tag_material,
            "derived_authority_contract_hash": contract.derived_contract_hash,
            "respondent_compatibility_hash": contract.respondent_compatibility_hash,
        })
        return MixedCompositionResolution(
            grammar_authority_ref=contract.composition_ref,
            respondent_binding_semantics=contract.derived_binding_semantics,
            authority_snapshot_ref=contract.composition_ref,
            replay_material=replay_material,
        )

    def frozen_selector_hashes(self) -> tuple[str, ...]:
        # Selector identities are authority-data observations only; runtime never mints them.
        hashes: set[str] = set()
        # The exact dialect matrices are deliberately not retained as semantic dispatch state.
        # No generated selector identity can therefore enter this set.
        return tuple(sorted(hashes))

    def require_realized_release(
        self,
        selector_scope_ref: ExactRef | Mapping[str, Any],
        *,
        repository: C11Repository,
        runtime_release_ref: ExactRef | Mapping[str, Any],
    ) -> C11LogicalRelease:
        if not isinstance(repository, C11Repository):
            raise Pre553AuthorityError("release realization requires accepted exact C11Repository")
        scope = exact_ref(selector_scope_ref, "selector release/scope ref")
        runtime_ref = exact_ref(runtime_release_ref, "runtime I02 release ref")
        contract = self._realizations.get(scope.key)
        if contract is None or scope != contract.frozen_scope_ref:
            raise Pre553AuthorityError("no exact adopted release realization authority for selector scope")

        active = []
        for raw in self._bindings:
            binding = _mapping(raw, "release realization binding")
            if binding.get("schema") != CONCRETE_BINDING_SCHEMA:
                continue
            if binding.get("typed_state") != ACTIVE_POSITIVE_BINDING:
                continue
            material = _mapping(binding.get("identity_material"), "binding identity material")
            try:
                relation_ref = exact_ref(material.get("relation_authority_ref"), "binding relation authority")
                bound_scope = exact_ref(material.get("frozen_scope_anchor_ref"), "binding frozen scope")
            except Exception:
                continue
            if relation_ref == contract.authority_ref and bound_scope == scope:
                active.append(binding)
        if len(active) == 0:
            raise Pre553AuthorityError("zero active positive concrete realization bindings; fail closed")
        if len(active) != 1:
            raise Pre553AuthorityError("multiple active positive concrete realization bindings; fail closed")
        return self._validate_binding(active[0], contract, repository, runtime_ref)

    def _validate_binding(
        self,
        binding: Mapping[str, Any],
        contract: ReleaseRealizationContract,
        repository: C11Repository,
        runtime_ref: ExactRef,
    ) -> C11LogicalRelease:
        material = _mapping(binding.get("identity_material"), "binding identity material")
        binding_ref = exact_ref(binding.get("binding_ref"), "binding ref")
        if binding_ref.content_hash != semantic_hash(material):
            raise Pre553AuthorityError("concrete realization binding identity hash mismatch")

        required = _mapping(
            contract.binding_schema.get("future_binding_required_fields"),
            "future binding required fields",
        )
        self._match_binding_template(required, material, path="binding")

        relation_ref = exact_ref(material.get("relation_authority_ref"), "binding relation authority")
        if relation_ref != contract.authority_ref:
            raise Pre553AuthorityError("concrete binding relation authority mismatch")
        scope_ref = exact_ref(material.get("frozen_scope_anchor_ref"), "binding frozen scope")
        if scope_ref != contract.frozen_scope_ref:
            raise Pre553AuthorityError("concrete binding frozen scope mismatch")
        source_sha = material.get("source_artifact_sha256")
        if source_sha != contract.source_sha256:
            raise Pre553AuthorityError("concrete binding source identity mismatch")
        base_ref = exact_ref(material.get("accepted_base_i02_release_ref"), "binding accepted base release")
        if base_ref != contract.accepted_base_release_ref:
            raise Pre553AuthorityError("concrete binding accepted base lineage mismatch")

        target_ref = exact_ref(material.get("runtime_i02_release_ref"), "binding runtime release")
        if target_ref == contract.frozen_scope_ref:
            raise Pre553AuthorityError("historical scope anchor may not be used as runtime repository key")
        if target_ref.kind != "C11LogicalRelease":
            raise Pre553AuthorityError("concrete binding target must be C11LogicalRelease")
        try:
            release = repository.resolve_release_exact(target_ref)
        except KeyError as exc:
            raise Pre553AuthorityError(
                "concrete binding runtime target is absent from exact C11Repository"
            ) from exc
        if release.release_ref != runtime_ref:
            raise Pre553AuthorityError("realization target does not equal current exact runtime release")
        if release.source_artifact_ref.content_hash != contract.source_sha256:
            raise Pre553AuthorityError("runtime release source artifact does not satisfy concrete binding contract")

        projection_hash = material.get("runtime_candidate_projection_hash")
        if projection_hash != release.replay_manifest.semantic_projection_hash:
            raise Pre553AuthorityError("runtime candidate projection evidence mismatch")
        replay_ref = exact_ref(material.get("runtime_replay_manifest_ref"), "runtime replay manifest ref")
        if replay_ref != release.replay_manifest.ref:
            raise Pre553AuthorityError("runtime replay manifest evidence mismatch")
        coverage = material.get("runtime_m01_m18_coverage")
        if canonical_json(coverage) != canonical_json(dict(release.m01_m18_coverage)):
            raise Pre553AuthorityError("runtime M01-M18 coverage evidence mismatch")
        expected_m = {f"M{i:02d}" for i in range(1, 19)}
        if set(release.m01_m18_coverage) != expected_m:
            raise Pre553AuthorityError("runtime release does not carry complete exact M01-M18 coverage")

        exact_ref(
            material.get("c11_repository_exact_resolution_receipt"),
            "C11Repository exact resolution receipt",
        )
        return release

    def _match_binding_template(self, expected: Any, actual: Any, *, path: str) -> None:
        if isinstance(expected, Mapping):
            if not isinstance(actual, Mapping):
                raise Pre553AuthorityError(f"{path} must be an exact mapping")
            for key, value in expected.items():
                if key not in actual:
                    raise Pre553AuthorityError(f"{path}.{key} is required")
                self._match_binding_template(value, actual[key], path=f"{path}.{key}")
            return
        if isinstance(expected, str) and (
            expected == "EXACT_ADOPTED_REF_REQUIRED"
            or expected.startswith("REQUIRED_AT_BINDING_TIME")
            or expected == "REQUIRED_COMPLETE"
            or expected == "REQUIRED"
        ):
            if actual is None:
                raise Pre553AuthorityError(f"{path} required value is absent")
            return
        if canonical_json(expected) != canonical_json(actual):
            raise Pre553AuthorityError(f"{path} does not match exact adopted binding schema")


__all__ = [
    "ACTIVE_POSITIVE_BINDING",
    "CONCRETE_BINDING_SCHEMA",
    "EXACT_RISK_SET_SUCCESSOR_SCHEMA",
    "ExactRiskSetSuccessorContract",
    "I03_OPERATION_SUCCESSOR_SCHEMA",
    "I03OperationSuccessorContract",
    "MixedCompositionResolution",
    "PredicateDialectContract",
    "Pre553RuntimeAuthoritySet",
    "ReleaseRealizationContract",
]
