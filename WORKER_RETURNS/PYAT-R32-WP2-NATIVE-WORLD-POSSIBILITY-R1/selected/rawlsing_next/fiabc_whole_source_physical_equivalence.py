"""Candidate-neutral whole-source physical-equivalence receipts for CLOSED_35.

This module is deliberately physical-only.  It proves that a candidate
realization preserves the source-native information required by a declared
physical scope.  It does not certify survey semantics, replace I05, or mint
weight/population authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash


SOURCE_SCOPE_SCHEMA = "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0"
EXPECTATION_SCHEMA = "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0"
REALIZATION_SCHEMA = "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0"
RECEIPT_SCHEMA = "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0"

PASS_STATUS = "PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS"
COMPATIBILITY_PHYSICAL_ONLY = "PHYSICAL_EXTRACTION_ONLY__NO_SOURCE_TEXT_OR_SEMANTIC_AUTHORITY"
NO_COMPATIBILITY_SEMANTIC_CLAIM = "NO_COMPATIBILITY_OVERRIDE__NO_SEMANTIC_CLAIM"

REQUIRED_CANDIDATES = ("A", "B", "C")
EDGE_CLASSES = tuple(f"EC{i:02d}" for i in range(1, 15))
ATOMIC_EDGE_CLASSES = tuple(f"EC{i:02d}" for i in range(1, 14))

BASE_REQUIRED_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "row_replay_identity",
)

EDGE_REQUIRED_DIMENSIONS: Mapping[str, tuple[str, ...]] = {
    "EC01": (),
    "EC02": (),
    "EC03": ("compatibility_decode_evidence",),
    "EC04": ("raw_display_separation",),
    "EC05": ("typed_missingness",),
    "EC06": ("all_missing_column_retention",),
    "EC07": ("native_id_replay_evidence",),
    "EC08": ("native_mr_sets",),
    "EC09": ("occurrence_rank_topology",),
    "EC10": ("form_module_skip_routing_carriers",),
    "EC11": ("variable_dictionaries",),
    "EC12": ("weight_design_variables",),
    "EC13": ("source_local_coordinate_carriers",),
    "EC14": (),
}


class PhysicalEquivalenceError(ValueError):
    """Fail-closed whole-source physical-equivalence violation."""


def _sha(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value.lower() != value
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise PhysicalEquivalenceError(f"{name} must be lowercase sha256")
    return value


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PhysicalEquivalenceError(f"{name} must be a mapping")
    return value


def _nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PhysicalEquivalenceError(f"{name} must be a non-empty string")
    return value


def canonical_digest(material: Any) -> str:
    """Return the repository-standard canonical semantic digest."""
    return semantic_hash(canonicalize(material))


def _source_identity(value: Mapping[str, Any]) -> dict[str, Any]:
    source = dict(_mapping(value, "source_identity"))
    required = ("family", "wave_or_release", "canonical_filename", "sha256", "format")
    missing = [key for key in required if key not in source]
    if missing:
        raise PhysicalEquivalenceError(f"source identity missing fields: {missing}")
    for key in ("family", "wave_or_release", "canonical_filename", "format"):
        _nonempty(source[key], f"source_identity.{key}")
    _sha(source["sha256"], "source_identity.sha256")
    return canonicalize(source)


def _reader_binding(source_sha256: str, value: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    reader = dict(_mapping(value, "reader_configuration"))
    required = (
        "decoder_implementation",
        "decoder_version",
        "decoder_mode",
        "config",
        "compatibility_mode",
        "compatibility_semantic_scope",
    )
    missing = [key for key in required if key not in reader]
    if missing:
        raise PhysicalEquivalenceError(f"reader configuration missing fields: {missing}")
    for key in ("decoder_implementation", "decoder_version", "decoder_mode", "compatibility_mode",
                "compatibility_semantic_scope"):
        _nonempty(reader[key], f"reader_configuration.{key}")
    _mapping(reader["config"], "reader_configuration.config")

    if reader.get("semantic_authority") is True:
        raise PhysicalEquivalenceError("reader/compatibility configuration may not claim semantic authority")

    compatibility_mode = reader["compatibility_mode"]
    semantic_scope = reader["compatibility_semantic_scope"]
    if "COMPATIBILITY_EXECUTION_ONLY" in compatibility_mode and semantic_scope != COMPATIBILITY_PHYSICAL_ONLY:
        raise PhysicalEquivalenceError(
            "compatibility execution must remain physical-only and nonsemantic"
        )
    if compatibility_mode == "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE" and semantic_scope not in (
        NO_COMPATIBILITY_SEMANTIC_CLAIM,
        COMPATIBILITY_PHYSICAL_ONLY,
    ):
        raise PhysicalEquivalenceError("native/no-override reader mode may not mint semantic authority")

    normalized = canonicalize(reader)
    identity = canonical_digest({
        "source_sha256": source_sha256,
        "reader_configuration": normalized,
    })
    return normalized, identity


def _physical_metadata_binding(source_sha256: str, value: Mapping[str, Any]) -> dict[str, Any]:
    binding = dict(_mapping(value, "physical_metadata_binding"))
    required = (
        "contract",
        "receipt_identity",
        "source_sha256",
        "physical_metadata_digest",
        "verification_state",
    )
    missing = [key for key in required if key not in binding]
    if missing:
        raise PhysicalEquivalenceError(f"physical metadata binding missing fields: {missing}")
    _nonempty(binding["contract"], "physical_metadata_binding.contract")
    _sha(binding["receipt_identity"], "physical_metadata_binding.receipt_identity")
    _sha(binding["source_sha256"], "physical_metadata_binding.source_sha256")
    _sha(binding["physical_metadata_digest"], "physical_metadata_binding.physical_metadata_digest")
    if binding["source_sha256"] != source_sha256:
        raise PhysicalEquivalenceError("physical metadata binding source SHA drift")
    if binding["verification_state"] != "VERIFIED":
        raise PhysicalEquivalenceError("physical metadata binding must be externally VERIFIED")
    if binding.get("semantic_authority") is True:
        raise PhysicalEquivalenceError("physical metadata receipt may not claim semantic authority")
    return canonicalize(binding)


def _parentage_binding(
    source_sha256: str,
    reader_configuration_digest: str,
    value: Mapping[str, Any],
) -> dict[str, Any]:
    binding = dict(_mapping(value, "derivative_parentage_binding"))
    required = (
        "contract",
        "receipt_identity",
        "parent_receipt_identity",
        "canonical_source_sha256",
        "derivative_identity",
        "producer_identity",
        "operation",
        "reader_configuration_digest",
        "scope_state",
        "verification_state",
    )
    missing = [key for key in required if key not in binding]
    if missing:
        raise PhysicalEquivalenceError(f"derivative parentage binding missing fields: {missing}")
    for key in ("contract", "producer_identity", "operation", "scope_state", "verification_state"):
        _nonempty(binding[key], f"derivative_parentage_binding.{key}")
    for key in (
        "receipt_identity",
        "parent_receipt_identity",
        "canonical_source_sha256",
        "derivative_identity",
        "reader_configuration_digest",
    ):
        _sha(binding[key], f"derivative_parentage_binding.{key}")
    if binding["canonical_source_sha256"] != source_sha256:
        raise PhysicalEquivalenceError("derivative parentage terminates at the wrong canonical source")
    if binding["reader_configuration_digest"] != reader_configuration_digest:
        raise PhysicalEquivalenceError("derivative parentage reader/config binding drift")
    if binding["scope_state"] != "CURRENT_AND_SCOPE_COMPLETE":
        raise PhysicalEquivalenceError("derivative parentage does not cover the declared physical scope")
    if binding["verification_state"] != "VERIFIED":
        raise PhysicalEquivalenceError("derivative parentage must be externally VERIFIED")
    if binding.get("semantic_authority") is True:
        raise PhysicalEquivalenceError("derivative parentage receipt may not claim semantic authority")
    return canonicalize(binding)


def _edge_classes(values: Sequence[str]) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise PhysicalEquivalenceError("applicable_edge_classes must be a sequence")
    edges = tuple(sorted(set(values)))
    if not edges or any(edge not in EDGE_CLASSES for edge in edges):
        raise PhysicalEquivalenceError("unknown or empty S35 edge-class declaration")
    if "EC01" not in edges:
        raise PhysicalEquivalenceError("whole-source CLOSED_35 scope must include EC01 format-family law")
    if "EC14" in edges and len([edge for edge in edges if edge in ATOMIC_EDGE_CLASSES]) < 2:
        raise PhysicalEquivalenceError("EC14 requires a compound declaration of atomic edge classes")
    return edges


def required_dimensions(applicable_edge_classes: Sequence[str]) -> tuple[str, ...]:
    edges = _edge_classes(applicable_edge_classes)
    required = set(BASE_REQUIRED_DIMENSIONS)
    for edge in edges:
        required.update(EDGE_REQUIRED_DIMENSIONS[edge])
    return tuple(sorted(required))


def _evidence_digests(
    evidence_material: Mapping[str, Any],
    physical_metadata_digest: str,
) -> dict[str, str]:
    evidence = dict(_mapping(evidence_material, "evidence_material"))
    if "physical_metadata" in evidence:
        raise PhysicalEquivalenceError(
            "physical_metadata is supplied only by the external metadata receipt"
        )
    digests = {str(key): canonical_digest(value) for key, value in evidence.items()}
    digests["physical_metadata"] = _sha(physical_metadata_digest, "physical_metadata_digest")
    return dict(sorted(digests.items()))


def _validate_dimension_coverage(edges: Sequence[str], evidence_digests: Mapping[str, str]) -> None:
    missing = [name for name in required_dimensions(edges) if name not in evidence_digests]
    if missing:
        raise PhysicalEquivalenceError(
            f"declared physical scope lacks required evidence dimensions: {missing}"
        )
    for name, digest in evidence_digests.items():
        _nonempty(name, "evidence dimension")
        _sha(digest, f"evidence digest {name}")


def build_canonical_expectation(
    *,
    scope_id: str,
    source_identity: Mapping[str, Any],
    reader_configuration: Mapping[str, Any],
    applicable_edge_classes: Sequence[str],
    evidence_material: Mapping[str, Any],
    physical_metadata_binding: Mapping[str, Any],
) -> dict[str, Any]:
    """Freeze the candidate-neutral expected physical state for one source scope."""
    scope_id = _nonempty(scope_id, "scope_id")
    source = _source_identity(source_identity)
    source_sha = source["sha256"]
    reader, reader_digest = _reader_binding(source_sha, reader_configuration)
    metadata = _physical_metadata_binding(source_sha, physical_metadata_binding)
    edges = _edge_classes(applicable_edge_classes)
    evidence = _evidence_digests(evidence_material, metadata["physical_metadata_digest"])
    _validate_dimension_coverage(edges, evidence)

    body = canonicalize({
        "schema": EXPECTATION_SCHEMA,
        "scope": {
            "schema": SOURCE_SCOPE_SCHEMA,
            "scope_id": scope_id,
            "claim_kind": "WHOLE_SOURCE_PHYSICAL_EQUIVALENCE",
            "applicable_edge_classes": edges,
            "required_dimensions": required_dimensions(edges),
        },
        "source_identity": source,
        "reader_configuration": reader,
        "reader_configuration_digest": reader_digest,
        "physical_metadata_binding": metadata,
        "evidence_digests": evidence,
        "semantic_or_certification_authority": False,
    })
    body = dict(body)
    body["expectation_identity"] = canonical_digest(body)
    return canonicalize(body)


def verify_canonical_expectation(expectation: Mapping[str, Any]) -> str:
    frozen = dict(_mapping(expectation, "expectation"))
    identity = _sha(frozen.pop("expectation_identity", None), "expectation_identity")
    if frozen.get("schema") != EXPECTATION_SCHEMA:
        raise PhysicalEquivalenceError("unexpected physical expectation schema")
    if canonical_digest(frozen) != identity:
        raise PhysicalEquivalenceError("canonical physical expectation mutated after freeze")
    scope = _mapping(frozen.get("scope"), "expectation.scope")
    if scope.get("schema") != SOURCE_SCOPE_SCHEMA:
        raise PhysicalEquivalenceError("unexpected source physical scope schema")
    edges = _edge_classes(scope.get("applicable_edge_classes"))
    evidence = _mapping(frozen.get("evidence_digests"), "expectation.evidence_digests")
    _validate_dimension_coverage(edges, evidence)
    source = _source_identity(_mapping(frozen.get("source_identity"), "expectation.source_identity"))
    _, reader_digest = _reader_binding(
        source["sha256"],
        _mapping(frozen.get("reader_configuration"), "expectation.reader_configuration"),
    )
    if frozen.get("reader_configuration_digest") != reader_digest:
        raise PhysicalEquivalenceError("expectation reader/config identity drift")
    _physical_metadata_binding(
        source["sha256"],
        _mapping(frozen.get("physical_metadata_binding"), "expectation.physical_metadata_binding"),
    )
    if frozen.get("semantic_or_certification_authority") is not False:
        raise PhysicalEquivalenceError("physical expectation may not claim semantic/certification authority")
    return identity


def build_candidate_realization(
    *,
    candidate: str,
    expectation: Mapping[str, Any],
    source_identity: Mapping[str, Any],
    reader_configuration: Mapping[str, Any],
    applicable_edge_classes: Sequence[str],
    evidence_material: Mapping[str, Any],
    physical_metadata_binding: Mapping[str, Any],
    realization_kind: str = "DIRECT_RAW",
    derivative_parentage_binding: Mapping[str, Any] | None = None,
    semantic_observation_digest: str | None = None,
) -> dict[str, Any]:
    """Build one candidate's governed physical realization descriptor."""
    if candidate not in REQUIRED_CANDIDATES:
        raise PhysicalEquivalenceError("candidate must be one of A/B/C")
    expectation_identity = verify_canonical_expectation(expectation)
    source = _source_identity(source_identity)
    reader, reader_digest = _reader_binding(source["sha256"], reader_configuration)
    metadata = _physical_metadata_binding(source["sha256"], physical_metadata_binding)
    edges = _edge_classes(applicable_edge_classes)
    evidence = _evidence_digests(evidence_material, metadata["physical_metadata_digest"])
    _validate_dimension_coverage(edges, evidence)
    realization_kind = _nonempty(realization_kind, "realization_kind")

    parentage = None
    if realization_kind == "DIRECT_RAW":
        if derivative_parentage_binding is not None:
            raise PhysicalEquivalenceError("DIRECT_RAW realization may not smuggle derivative parentage")
    else:
        if derivative_parentage_binding is None:
            raise PhysicalEquivalenceError(
                "non-raw realization requires an externally verified derivative parentage receipt"
            )
        parentage = _parentage_binding(
            source["sha256"],
            reader_digest,
            derivative_parentage_binding,
        )

    if semantic_observation_digest is not None:
        _sha(semantic_observation_digest, "semantic_observation_digest")

    body = canonicalize({
        "schema": REALIZATION_SCHEMA,
        "candidate": candidate,
        "expectation_identity": expectation_identity,
        "source_identity": source,
        "reader_configuration": reader,
        "reader_configuration_digest": reader_digest,
        "applicable_edge_classes": edges,
        "physical_metadata_binding": metadata,
        "evidence_digests": evidence,
        "realization_kind": realization_kind,
        "derivative_parentage_binding": parentage,
        "semantic_observation_digest": semantic_observation_digest,
        "semantic_observation_used_as_physical_truth": False,
    })
    body = dict(body)
    body["realization_identity"] = canonical_digest(body)
    return canonicalize(body)


def verify_candidate_physical_equivalence(
    expectation: Mapping[str, Any],
    realization: Mapping[str, Any],
) -> dict[str, Any]:
    """Fail closed unless the candidate closes every declared physical dimension."""
    expectation_identity = verify_canonical_expectation(expectation)
    expected = _mapping(expectation, "expectation")
    observed = dict(_mapping(realization, "realization"))

    realization_identity = _sha(
        observed.pop("realization_identity", None),
        "realization_identity",
    )
    if observed.get("schema") != REALIZATION_SCHEMA:
        raise PhysicalEquivalenceError("unexpected candidate physical realization schema")
    if canonical_digest(observed) != realization_identity:
        raise PhysicalEquivalenceError("candidate physical realization mutated after freeze")
    candidate = observed.get("candidate")
    if candidate not in REQUIRED_CANDIDATES:
        raise PhysicalEquivalenceError("candidate identity drift")
    if observed.get("expectation_identity") != expectation_identity:
        raise PhysicalEquivalenceError("candidate realization targets the wrong physical expectation")
    if canonicalize(observed.get("source_identity")) != canonicalize(expected.get("source_identity")):
        raise PhysicalEquivalenceError("canonical source identity/SHA mismatch")
    if observed.get("reader_configuration_digest") != expected.get("reader_configuration_digest"):
        raise PhysicalEquivalenceError("exact reader/decoder/version/config mismatch")
    if canonicalize(observed.get("reader_configuration")) != canonicalize(expected.get("reader_configuration")):
        raise PhysicalEquivalenceError("reader configuration payload mismatch")
    if tuple(observed.get("applicable_edge_classes") or ()) != tuple(
        _mapping(expected.get("scope"), "expectation.scope").get("applicable_edge_classes") or ()
    ):
        raise PhysicalEquivalenceError("declared S35 edge-class scope mismatch")

    observed_metadata = _physical_metadata_binding(
        _mapping(observed.get("source_identity"), "realization.source_identity")["sha256"],
        _mapping(observed.get("physical_metadata_binding"), "realization.physical_metadata_binding"),
    )
    expected_metadata = _mapping(expected.get("physical_metadata_binding"), "expectation.physical_metadata_binding")
    if observed_metadata["physical_metadata_digest"] != expected_metadata["physical_metadata_digest"]:
        raise PhysicalEquivalenceError("raw-layout/display/file physical metadata digest mismatch")

    expected_evidence = _mapping(expected.get("evidence_digests"), "expectation.evidence_digests")
    observed_evidence = _mapping(observed.get("evidence_digests"), "realization.evidence_digests")
    missing = [name for name in expected_evidence if name not in observed_evidence]
    if missing:
        raise PhysicalEquivalenceError(f"candidate realization dropped required physical evidence: {missing}")
    mismatched = [
        name for name, digest in expected_evidence.items()
        if observed_evidence.get(name) != digest
    ]
    if mismatched:
        raise PhysicalEquivalenceError(
            f"candidate realization is physically nonequivalent on: {mismatched}"
        )

    kind = observed.get("realization_kind")
    if kind != "DIRECT_RAW":
        _parentage_binding(
            _mapping(observed.get("source_identity"), "realization.source_identity")["sha256"],
            observed["reader_configuration_digest"],
            _mapping(observed.get("derivative_parentage_binding"), "derivative_parentage_binding"),
        )
    elif observed.get("derivative_parentage_binding") is not None:
        raise PhysicalEquivalenceError("DIRECT_RAW realization contains derivative parentage")

    extra_dimensions = tuple(sorted(set(observed_evidence) - set(expected_evidence)))
    receipt = canonicalize({
        "schema": RECEIPT_SCHEMA,
        "status": PASS_STATUS,
        "candidate": candidate,
        "scope_id": _mapping(expected.get("scope"), "expectation.scope")["scope_id"],
        "expectation_identity": expectation_identity,
        "realization_identity": realization_identity,
        "canonical_source_sha256": _mapping(expected.get("source_identity"), "expectation.source_identity")["sha256"],
        "reader_configuration_digest": expected["reader_configuration_digest"],
        "physical_metadata_digest": expected_metadata["physical_metadata_digest"],
        "applicable_edge_classes": _mapping(expected.get("scope"), "expectation.scope")["applicable_edge_classes"],
        "matched_required_dimensions": tuple(sorted(expected_evidence)),
        "candidate_extra_dimensions_not_used_as_truth": extra_dimensions,
        "realization_kind": kind,
        "derivative_parentage_receipt_identity": (
            None if kind == "DIRECT_RAW"
            else _mapping(observed.get("derivative_parentage_binding"), "derivative_parentage_binding")["receipt_identity"]
        ),
        "semantic_observation_digest": observed.get("semantic_observation_digest"),
        "semantic_observation_used_as_physical_truth": False,
        "semantic_parity_claimed": False,
        "source_certification_claimed": False,
        "documentary_semantic_authority_claimed": False,
        "weight_population_authority_claimed": False,
    })
    receipt = dict(receipt)
    receipt["receipt_identity"] = canonical_digest(receipt)
    return canonicalize(receipt)


__all__ = [
    "ATOMIC_EDGE_CLASSES",
    "BASE_REQUIRED_DIMENSIONS",
    "COMPATIBILITY_PHYSICAL_ONLY",
    "EDGE_CLASSES",
    "EDGE_REQUIRED_DIMENSIONS",
    "EXPECTATION_SCHEMA",
    "NO_COMPATIBILITY_SEMANTIC_CLAIM",
    "PASS_STATUS",
    "PhysicalEquivalenceError",
    "RECEIPT_SCHEMA",
    "REALIZATION_SCHEMA",
    "REQUIRED_CANDIDATES",
    "SOURCE_SCOPE_SCHEMA",
    "build_candidate_realization",
    "build_canonical_expectation",
    "canonical_digest",
    "required_dimensions",
    "verify_candidate_physical_equivalence",
    "verify_canonical_expectation",
]
