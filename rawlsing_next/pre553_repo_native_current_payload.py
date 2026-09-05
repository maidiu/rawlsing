"""Fixed repo-native rehydration of the exact current GT2 PRE553 query/fact.

This module is the current-only A -> B bridge.  It reads only the four immutable
Worker-A transport resources already committed in this repository, verifies their
frozen identities/counts, reconstructs the exact-ref closures, and invokes the
ordinary existing EmpiricalQuerySpec and EmpiricalFact constructors.

No Library, source data, empirical carrier, authority override, identity override,
or caller-selected filesystem path is accepted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Final, Mapping

from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    exact_ref,
)


class CurrentGT2RehydrationError(Pre553IntegrityError):
    """The fixed committed current transport failed closed."""


_TRANSPORT_ROOT: Final[Path] = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/"
    "R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/"
    "R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/"
    "R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2"
)
_MANIFEST_PATH: Final[Path] = Path("02_CONSTRUCTOR_COMPLETE_MANIFEST.json")
_MANIFEST_SHA256: Final[str] = (
    "c2d008a96ce1cf9156cd9e10ebaf513f300139853a60db5856569f1375233c89"
)
_EXECUTION_CHECKPOINT: Final[str] = "43cf3df0fc9002a38d72ad57f1fe4dfe1f3736fb"
_WORKER_A_TERMINAL: Final[str] = (
    "PASS__GT12_R4A_CURRENT_GT2_EXECUTED__ACTUAL_QUERY_FACT_OBTAINED__"
    "CONSTRUCTOR_COMPLETE_PAYLOAD_EXTRACTED"
)

CURRENT_PREDICATE_HASH: Final[str] = (
    "bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3"
)
CURRENT_QUERY_HASH: Final[str] = (
    "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0"
)
CURRENT_FACT_HASH: Final[str] = (
    "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46"
)
CURRENT_REPLAY_HASH: Final[str] = (
    "c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f"
)
_HISTORICAL_A3_QUERY_HASH: Final[str] = (
    "e91970c161736113201a3e9880034f8d088099aad67300a5aa689b7a08200670"
)
_HISTORICAL_A3_FACT_HASH: Final[str] = (
    "7bdb8752df31905a737d1a21c2ada61fe0c64d9cb4db17ea9bb748a1cf25b27f"
)
_HISTORICAL_A3_REPLAY_HASH: Final[str] = (
    "10c4c50af557fe92866c6033a424ba2ab56847400bf9f970e6666612f435cae0"
)

_BINARY_SPECS: Final[dict[str, dict[str, Any]]] = {
    "respondent_refs": {
        "path": "payload/respondent_ref_hashes.bin",
        "count": 19_210,
        "bytes": 614_720,
        "sha256": "9c34860a8a2a474e667e72ec5141e199b853672efb851bddebbd2dcde0d7a80b",
        "kind": "C11Internal:RespondentIdentity",
        "object_id_template": "urn:rawlsing:pre553:c11:RespondentIdentity:sha256:{hash}",
    },
    "routing_refs": {
        "path": "payload/routing_ref_hashes.bin",
        "count": 38_420,
        "bytes": 1_229_440,
        "sha256": "9ab1b53264a159d9446c8cfaef4c63c7c9786cd12e6e96d143ee57e6ad894825",
        "kind": "RoutingEligibilityFact@1.0.0",
        "object_id_template": "urn:rawlsing:pre553:RoutingEligibilityFact:sha256:{hash}",
    },
    "event_refs": {
        "path": "payload/event_ref_hashes.bin",
        "count": 38_420,
        "bytes": 1_229_440,
        "sha256": "2fa09161ad457750dc3c80865811731908bdeb1c82dfdd36e958f178ede041b1",
        "kind": "RespondentEvent@1.0.0",
        "object_id_template": "urn:rawlsing:pre553:RespondentEvent:sha256:{hash}",
    },
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _fixed_resource(relative: Path | str) -> Path:
    return _repo_root() / _TRANSPORT_ROOT / Path(relative)


def _read_committed_transport() -> tuple[bytes, dict[str, bytes]]:
    manifest = _fixed_resource(_MANIFEST_PATH).read_bytes()
    payloads = {
        name: _fixed_resource(spec["path"]).read_bytes()
        for name, spec in _BINARY_SPECS.items()
    }
    return manifest, payloads


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CurrentGT2RehydrationError(f"{name} must be a mapping")
    return value


def _require_manifest_identity(manifest: Mapping[str, Any]) -> None:
    if manifest.get("schema") != "GT12_R4A_CURRENT_GT2_CONSTRUCTOR_COMPLETE_TRANSPORT@3":
        raise CurrentGT2RehydrationError("current constructor manifest schema drift")
    if manifest.get("execution_checkpoint_commit") != _EXECUTION_CHECKPOINT:
        raise CurrentGT2RehydrationError("current execution checkpoint identity drift")
    if manifest.get("worker_terminal") != _WORKER_A_TERMINAL:
        raise CurrentGT2RehydrationError("current Worker A terminal identity drift")

    identity = _mapping(manifest.get("identity"), "manifest.identity")
    triple = (identity.get("query"), identity.get("fact"), identity.get("replay"))
    if triple == (
        _HISTORICAL_A3_QUERY_HASH,
        _HISTORICAL_A3_FACT_HASH,
        _HISTORICAL_A3_REPLAY_HASH,
    ):
        raise CurrentGT2RehydrationError(
            "historical A3 query/fact/replay identities cannot impersonate current"
        )
    expected = {
        "predicate": CURRENT_PREDICATE_HASH,
        "query": CURRENT_QUERY_HASH,
        "fact": CURRENT_FACT_HASH,
        "replay": CURRENT_REPLAY_HASH,
    }
    if dict(identity) != expected:
        raise CurrentGT2RehydrationError("fixed current query/fact/replay/predicate identity drift")

    forbidden = _mapping(manifest.get("forbidden_material"), "manifest.forbidden_material")
    if dict(forbidden) != {
        "e2b_execution": False,
        "raw_respondent_response_values": False,
        "sav": False,
        "source_rows": False,
    }:
        raise CurrentGT2RehydrationError("forbidden empirical material entered current transport")


def _verify_binary_manifest(manifest: Mapping[str, Any]) -> None:
    closure = _mapping(manifest.get("closure_rehydration"), "manifest.closure_rehydration")
    for name, spec in _BINARY_SPECS.items():
        meta = _mapping(closure.get(name), f"closure_rehydration.{name}")
        if (
            meta.get("count") != spec["count"]
            or meta.get("kind") != spec["kind"]
            or meta.get("object_id_template") != spec["object_id_template"]
            or meta.get("canonical_order") != "ExactRef.key ascending"
        ):
            raise CurrentGT2RehydrationError(f"{name} fixed reconstruction metadata drift")
        shards = meta.get("shards")
        expected_shard = {
            "bytes": spec["bytes"],
            "count": spec["count"],
            "path": spec["path"],
            "sha256": spec["sha256"],
            "start_index": 0,
        }
        if shards != [expected_shard]:
            raise CurrentGT2RehydrationError(f"{name} fixed shard descriptor drift")

    if closure.get("risk_set_member_refs") != {
        "count": 19_210,
        "source": "respondent_refs",
    }:
        raise CurrentGT2RehydrationError("risk-set member reconstruction law drift")
    if closure.get("denominator_member_refs") != {
        "count": 19_210,
        "exact_sequence_equal_to_risk_set_members": True,
        "source": "respondent_refs",
    }:
        raise CurrentGT2RehydrationError("denominator member reconstruction law drift")

    provenance = _mapping(
        closure.get("source_empirical_provenance_refs"),
        "closure_rehydration.source_empirical_provenance_refs",
    )
    if provenance.get("count") != 76_843 or provenance.get("law") != (
        "canonical ExactRef set(release_ref,replay_manifest_ref,"
        "empirical_universe_ref,routing_refs,event_refs)"
    ):
        raise CurrentGT2RehydrationError("source provenance closure law drift")
    dependencies = _mapping(
        closure.get("dependency_refs"), "closure_rehydration.dependency_refs"
    )
    if dependencies.get("count") != 76_846 or dependencies.get("law") != (
        "canonical ExactRef set(query_ref,predicate_ref,replay_ref,"
        "source_empirical_provenance_refs)"
    ):
        raise CurrentGT2RehydrationError("dependency closure law drift")


def _decode_exact_ref_hashes(name: str, raw: bytes) -> tuple[ExactRef, ...]:
    spec = _BINARY_SPECS[name]
    if len(raw) != spec["bytes"]:
        raise CurrentGT2RehydrationError(f"{name} exact byte count mismatch")
    if _sha256(raw) != spec["sha256"]:
        raise CurrentGT2RehydrationError(f"{name} payload sha256 mismatch")
    if len(raw) % 32:
        raise CurrentGT2RehydrationError(f"{name} payload is not exact 32-byte hashes")
    if len(raw) // 32 != spec["count"]:
        raise CurrentGT2RehydrationError(f"{name} exact ref count mismatch")

    refs = tuple(
        ExactRef(
            spec["kind"],
            spec["object_id_template"].format(hash=(digest := raw[i : i + 32].hex())),
            digest,
        )
        for i in range(0, len(raw), 32)
    )
    if len(refs) != len(set(refs)):
        raise CurrentGT2RehydrationError(f"{name} contains duplicate exact refs")
    if refs != tuple(sorted(refs, key=lambda ref: ref.key)):
        raise CurrentGT2RehydrationError(f"{name} canonical ExactRef order drift")
    return refs


def _canonical_ref_set(*groups: Any) -> tuple[ExactRef, ...]:
    refs: set[ExactRef] = set()
    for group in groups:
        if isinstance(group, ExactRef):
            refs.add(group)
        else:
            refs.update(group)
    return tuple(sorted(refs, key=lambda ref: ref.key))


def _rehydrate_verified_transport(
    manifest_bytes: bytes,
    payloads: Mapping[str, bytes],
) -> tuple[EmpiricalQuerySpec, EmpiricalFact]:
    if _sha256(manifest_bytes) != _MANIFEST_SHA256:
        raise CurrentGT2RehydrationError("constructor manifest sha256 mismatch")
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CurrentGT2RehydrationError("constructor manifest is not valid UTF-8 JSON") from exc

    _require_manifest_identity(manifest)
    _verify_binary_manifest(manifest)

    if set(payloads) != set(_BINARY_SPECS):
        raise CurrentGT2RehydrationError("fixed binary payload set drift")
    respondent_refs = _decode_exact_ref_hashes("respondent_refs", payloads["respondent_refs"])
    routing_refs = _decode_exact_ref_hashes("routing_refs", payloads["routing_refs"])
    event_refs = _decode_exact_ref_hashes("event_refs", payloads["event_refs"])

    actual_query = _mapping(manifest.get("actual_query"), "manifest.actual_query")
    query_projection = _mapping(
        actual_query.get("constructor_semantic_projection"),
        "manifest.actual_query.constructor_semantic_projection",
    )
    query_ref = exact_ref(actual_query.get("ref"), "manifest.actual_query.ref")
    if query_ref.content_hash != CURRENT_QUERY_HASH:
        raise CurrentGT2RehydrationError("actual query ref is not exact current query")

    qfields = dict(_mapping(query_projection.get("semantic_fields"), "query.semantic_fields"))
    query = EmpiricalQuerySpec(
        typed_state=query_projection["typed_state"],
        authority_snapshot_refs=query_projection["authority_snapshot_refs"],
        dependency_refs=query_projection["dependency_refs"],
        producer_replay_locator_or_reference_root=query_projection[
            "producer_replay_locator_or_reference_root"
        ],
        object_id=query_ref.object_id,
        content_hash=query_ref.content_hash,
        schema_id=query_projection["schema_id"],
        schema_version=query_projection["schema_version"],
        **qfields,
    )
    if query.ref != query_ref or query.content_hash != CURRENT_QUERY_HASH:
        raise CurrentGT2RehydrationError("existing query constructor did not reproduce current identity")
    predicate_ref = exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref")
    if predicate_ref.content_hash != CURRENT_PREDICATE_HASH:
        raise CurrentGT2RehydrationError("existing query constructor predicate identity drift")

    actual_fact = _mapping(manifest.get("actual_fact"), "manifest.actual_fact")
    fact_input = _mapping(actual_fact.get("constructor_input"), "manifest.actual_fact.constructor_input")
    fact_ref = exact_ref(actual_fact.get("ref"), "manifest.actual_fact.ref")
    if fact_ref.content_hash != CURRENT_FACT_HASH:
        raise CurrentGT2RehydrationError("actual fact ref is not exact current fact")

    if fact_input.get("dependency_refs") != "EXTERNAL_CLOSURE__dependency_refs":
        raise CurrentGT2RehydrationError("fact dependency closure placeholder drift")
    ffields = dict(_mapping(fact_input.get("semantic_fields"), "fact.semantic_fields"))
    expected_placeholders = {
        "risk_set_member_refs": "EXTERNAL_CLOSURE__respondent_refs",
        "denominator_member_refs": "EXTERNAL_CLOSURE__respondent_refs",
        "source_empirical_provenance_refs": "EXTERNAL_CLOSURE__source_empirical_provenance_refs",
    }
    for key, marker in expected_placeholders.items():
        if ffields.get(key) != marker:
            raise CurrentGT2RehydrationError(f"fact {key} closure placeholder drift")

    replay_ref = exact_ref(ffields["replay_ref"], "fact.replay_ref")
    if replay_ref.content_hash != CURRENT_REPLAY_HASH:
        raise CurrentGT2RehydrationError("fact replay is not exact current replay")
    fact_query_ref = exact_ref(ffields["empirical_query_spec_ref"], "fact.empirical_query_spec_ref")
    if fact_query_ref != query.ref:
        raise CurrentGT2RehydrationError("fact does not bind exact reconstructed current query")
    fact_predicate_ref = exact_ref(ffields["condition_predicate_ref"], "fact.condition_predicate_ref")
    if fact_predicate_ref != predicate_ref:
        raise CurrentGT2RehydrationError("fact/query predicate binding drift")

    empirical_universes = tuple(
        exact_ref(x, "query.empirical_universe_refs") for x in query.empirical_universe_refs
    )
    if len(empirical_universes) != 1:
        raise CurrentGT2RehydrationError("current query must bind exact single empirical universe")
    release_ref = exact_ref(_mapping(manifest.get("release"), "manifest.release")["ref"], "release.ref")
    replay_manifest_ref = exact_ref(
        _mapping(manifest.get("release"), "manifest.release")["replay_manifest_ref"],
        "release.replay_manifest_ref",
    )
    provenance_refs = _canonical_ref_set(
        release_ref,
        replay_manifest_ref,
        empirical_universes,
        routing_refs,
        event_refs,
    )
    if len(provenance_refs) != 76_843:
        raise CurrentGT2RehydrationError("exact source provenance ref count mismatch")

    dependency_refs = _canonical_ref_set(
        query.ref,
        predicate_ref,
        replay_ref,
        provenance_refs,
    )
    if len(dependency_refs) != 76_846:
        raise CurrentGT2RehydrationError("exact dependency ref count mismatch")

    ffields["risk_set_member_refs"] = respondent_refs
    ffields["denominator_member_refs"] = respondent_refs
    ffields["source_empirical_provenance_refs"] = provenance_refs

    fact = EmpiricalFact(
        typed_state=fact_input["typed_state"],
        authority_snapshot_refs=fact_input["authority_snapshot_refs"],
        dependency_refs=dependency_refs,
        producer_replay_locator_or_reference_root=fact_input[
            "producer_replay_locator_or_reference_root"
        ],
        object_id=fact_ref.object_id,
        content_hash=fact_ref.content_hash,
        **ffields,
    )
    if fact.ref != fact_ref or fact.content_hash != CURRENT_FACT_HASH:
        raise CurrentGT2RehydrationError("existing fact constructor did not reproduce current identity")
    if fact.raw_denominator_support != 19_210:
        raise CurrentGT2RehydrationError("current fact denominator is not exact 19,210")
    if tuple(exact_ref(x, "fact.risk_set_member_refs") for x in fact.risk_set_member_refs) != respondent_refs:
        raise CurrentGT2RehydrationError("fact risk-set member exact reconstruction drift")
    if tuple(exact_ref(x, "fact.denominator_member_refs") for x in fact.denominator_member_refs) != respondent_refs:
        raise CurrentGT2RehydrationError("fact denominator member exact reconstruction drift")
    constructed_provenance = tuple(
        exact_ref(x, "fact.source_empirical_provenance_refs")
        for x in fact.source_empirical_provenance_refs
    )
    if (
        len(constructed_provenance) != len(provenance_refs)
        or set(constructed_provenance) != set(provenance_refs)
    ):
        raise CurrentGT2RehydrationError("fact exact provenance closure drift")
    if fact.dependency_refs != dependency_refs:
        raise CurrentGT2RehydrationError("fact exact dependency closure drift")

    return query, fact


def load_current_gt2_query_fact_from_committed_transport() -> tuple[EmpiricalQuerySpec, EmpiricalFact]:
    """No-argument current loader over the fixed committed Worker-A repo transport."""
    manifest_bytes, payloads = _read_committed_transport()
    return _rehydrate_verified_transport(manifest_bytes, payloads)


__all__ = [
    "CURRENT_PREDICATE_HASH",
    "CURRENT_QUERY_HASH",
    "CURRENT_FACT_HASH",
    "CURRENT_REPLAY_HASH",
    "CurrentGT2RehydrationError",
    "load_current_gt2_query_fact_from_committed_transport",
]
