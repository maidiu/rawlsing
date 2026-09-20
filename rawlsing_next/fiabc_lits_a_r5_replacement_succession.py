"""Narrow current authority for one LiTS-I Candidate-A R5 replacement.

This module does not build R5.  It validates the successor document and gates a
later local attempt without changing the historical T2 manifest.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from rawlsing_next.fiabc_derivative_parentage import (
    ParentageError,
    canonical_digest,
    verify_parentage_bundle,
)

AUTHORITY_SCHEMA = "FIABC_LITS_A_R5_REPLACEMENT_SUCCESSION@1.0.0"
AUTHORITY_IDENTITY = "1be0cccc9938a8ad5594faa58d516ef6574b2daf3182d2ef9cb04a2435bfea88"
SOURCE_ID = "LITS_I"
CANDIDATE = "A"
DERIVATIVE_FAMILY = "R5"
DERIVATIVE_CLASS = "LITS_A_PRESERVED_R5_CARRIER"
CANONICAL_SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
BUILDER_BLOB = "92e364b31eaf27be1bca2081eff65f6ffb779c3d"
OLD_R5_CLASSIFICATION = "PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY"
EXECUTION_ACCOUNTING = "EXECUTED_NOW"


class ReplacementSuccessionError(ValueError):
    """The narrow replacement succession cannot admit the requested action."""


def _exact(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise ReplacementSuccessionError(f"{label} mismatch")


def verify_successor_authority(
    authority: Mapping[str, Any],
    *,
    expected_authority_identity: str | None = None,
) -> Mapping[str, Any]:
    if not isinstance(authority, Mapping):
        raise ReplacementSuccessionError("successor authority must be a mapping")
    _exact(authority.get("schema"), AUTHORITY_SCHEMA, "authority schema")
    identity = authority.get("authority_identity")
    if not isinstance(identity, str) or len(identity) != 64:
        raise ReplacementSuccessionError("authority identity absent or malformed")
    unsigned = {k: v for k, v in authority.items() if k != "authority_identity"}
    _exact(canonical_digest(unsigned), identity, "authority identity")
    _exact(identity, AUTHORITY_IDENTITY, "adopted authority identity")
    if expected_authority_identity is not None:
        _exact(identity, expected_authority_identity, "expected authority identity")

    predecessor = authority.get("predecessor_authority", {})
    _exact(predecessor.get("prohibition"), "NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD", "predecessor prohibition")
    _exact(predecessor.get("historical_manifest_mutable"), False, "historical manifest immutability")

    scope = authority.get("supersession_scope", {})
    _exact(scope.get("source_id"), SOURCE_ID, "source scope")
    _exact(scope.get("candidate"), CANDIDATE, "candidate scope")
    _exact(scope.get("derivative_family"), DERIVATIVE_FAMILY, "derivative family")
    _exact(scope.get("derivative_class"), DERIVATIVE_CLASS, "derivative class")
    _exact(scope.get("successful_replacement_limit"), 1, "successful replacement limit")
    _exact(scope.get("general_no_repeat_law_remains"), True, "general no-repeat law")

    contract = authority.get("replacement_contract", {})
    _exact(contract.get("canonical_source_sha256"), CANONICAL_SOURCE_SHA256, "canonical source")
    _exact(
        contract.get("builder"),
        {
            "identity": "R5CompactLongShardedBuilder",
            "code_blob": BUILDER_BLOB,
            "version": "R5_LONG_SHARDED_TYPED_INCIDENCE_V1",
            "owner_commit": "0b96b8de9aac774566f872cf0630ebd4ddeb70e6",
            "consumer_adapter_blob": "d4915e7e6755ba1850756aebff72f982f73a332b",
        },
        "builder contract",
    )
    _exact(contract.get("derivation_operation"), "BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE", "operation")
    reader = contract.get("reader_config", {})
    _exact(reader.get("reader_version"), "1.3.6", "reader version")
    _exact(reader.get("user_missing"), True, "user_missing")
    _exact(reader.get("apply_value_formats"), False, "apply_value_formats")
    _exact(reader.get("encoding"), "latin1", "encoding")
    _exact(reader.get("authority_status"), "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY", "reader authority")
    _exact(
        contract.get("build_config"),
        {
            "run_max_rows": 4096,
            "run_max_bytes": 4194304,
            "shard_max_rows": 16384,
            "shard_max_bytes": 16777216,
            "merge_fan_in": 8,
            "verified_spool_memory_bytes": 1048576,
        },
        "build config",
    )
    _exact(
        contract.get("fixed_identities"),
        {
            "lits_projection_identity": "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872",
            "expected_learned_product": "47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d",
            "semantic_replay_identity": "301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5",
            "runtime_catalog": "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02",
            "active_binding": "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308",
            "runtime_release": "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
            "candidate_a_owner_adapter": "d4915e7e6755ba1850756aebff72f982f73a332b",
            "learned_candidates": 50,
            "query_role_executions": 77,
        },
        "fixed semantics/runtime/workload identities",
    )

    parentage = authority.get("generic_parentage_requirement", {})
    _exact(parentage.get("required"), True, "generic parentage requirement")
    _exact(parentage.get("self_asserted_source_sha_sufficient"), False, "self-asserted source rule")
    _exact(parentage.get("bundle_schema"), "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0", "bundle schema")
    _exact(parentage.get("source_receipt_schema"), "FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0", "source receipt schema")
    _exact(parentage.get("derivative_receipt_schema"), "FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0", "derivative receipt schema")
    accounting = authority.get("accounting_treatment", {})
    _exact(accounting.get("replacement_build"), EXECUTION_ACCOUNTING, "new-build accounting")
    _exact(accounting.get("old_r5_numeric_preserved_work_credit"), 0, "old R5 numeric credit")
    old = authority.get("old_r5_disposition", {})
    _exact(old.get("classification"), OLD_R5_CLASSIFICATION, "old R5 classification")
    _exact(old.get("current_source_free_parentage_admissible"), False, "old R5 admission")
    _exact(authority.get("prohibition_on_second_successful_replacement"), True, "second-success prohibition")
    return authority


def evaluate_replacement_attempt(
    authority: Mapping[str, Any],
    *,
    source_id: str,
    candidate: str,
    derivative_family: str,
    attempt_state: str,
    successful_replacement_receipt_identities: Sequence[str] = (),
    admitted_derivative_identity: str | None = None,
    parentage_bundle: Mapping[str, Any] | None = None,
    parentage_expectations: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    verified = verify_successor_authority(authority)
    _exact(source_id, SOURCE_ID, "requested source")
    _exact(candidate, CANDIDATE, "requested candidate")
    _exact(derivative_family, DERIVATIVE_FAMILY, "requested derivative family")
    if successful_replacement_receipt_identities:
        raise ReplacementSuccessionError("one successful replacement already sealed")

    if attempt_state in {"INTERRUPTED_INCOMPLETE", "FAILED_INCOMPLETE"}:
        if admitted_derivative_identity is not None:
            raise ReplacementSuccessionError("incomplete attempt may not admit a derivative")
        return {
            "status": "RETRY_ALLOWED_UNDER_EXISTING_RECOVERY_LAW",
            "success_consumed": False,
            "accounting": None,
        }
    if attempt_state != "SUCCESSFULLY_SEALED":
        raise ReplacementSuccessionError("unknown replacement attempt state")
    if admitted_derivative_identity is None:
        raise ReplacementSuccessionError("sealed replacement lacks admitted derivative identity")
    if parentage_bundle is None or parentage_expectations is None:
        raise ReplacementSuccessionError("sealed replacement requires generic R35 parentage")

    expectations = dict(parentage_expectations)
    _exact(expectations.get("expected_source_id"), SOURCE_ID, "parentage source")
    _exact(expectations.get("expected_source_sha256"), CANONICAL_SOURCE_SHA256, "parentage source SHA")
    _exact(expectations.get("expected_derivative_class"), DERIVATIVE_CLASS, "parentage derivative class")
    _exact(expectations.get("expected_derivative_identity"), admitted_derivative_identity, "parentage derivative identity")
    contract = verified["replacement_contract"]
    _exact(expectations.get("expected_producer"), contract["builder"], "parentage producer")
    _exact(expectations.get("expected_derivation_operation"), contract["derivation_operation"], "parentage operation")
    _exact(expectations.get("expected_reader_config"), contract["reader_config"], "parentage reader config")
    verify_parentage_bundle(parentage_bundle, **expectations)
    return {
        "status": "SUCCESSFULLY_SEALED_REPLACEMENT_ADMITTED",
        "success_consumed": True,
        "accounting": EXECUTION_ACCOUNTING,
        "old_r5_numeric_credit": 0,
        "derivative_identity": admitted_derivative_identity,
    }


__all__ = [
    "AUTHORITY_SCHEMA",
    "AUTHORITY_IDENTITY",
    "ReplacementSuccessionError",
    "evaluate_replacement_attempt",
    "verify_successor_authority",
]
