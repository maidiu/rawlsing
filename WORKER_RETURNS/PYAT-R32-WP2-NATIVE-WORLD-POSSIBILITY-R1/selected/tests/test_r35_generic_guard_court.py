"""FIABC-R35-Q01 generic physical-guard hostile court.

This is a qualification/specification court, not a PRE553 semantic owner and
not sibling production code.  Sibling implementations may choose internal
names freely; fan-in must project their real receipts into this frozen
observation contract without weakening these validators.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest
from typing import Any, Mapping


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "WORKER_RETURNS"
    / "FIABC-R35-Q01"
    / "01_HOSTILE_FIXTURES.json"
)
COMPATIBILITY_ONLY = "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY"


class QualificationFailure(AssertionError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise QualificationFailure(code, message)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _path_get(value: Mapping[str, Any], path: str) -> Any:
    current: Any = value
    for token in path.split("."):
        if not isinstance(current, Mapping) or token not in current:
            raise KeyError(path)
        current = current[token]
    return current


def _selected(material: Mapping[str, Any], paths: list[str]) -> dict[str, Any]:
    selected: dict[str, Any] = {}
    for path in paths:
        try:
            selected[path] = _path_get(material, path)
        except KeyError as exc:
            raise QualificationFailure(
                "Q01_PHYSICAL_WITNESS_DROPPED",
                f"required physical witness missing: {path}",
            ) from exc
    return selected


def validate_raw_source(payload: Mapping[str, Any]) -> None:
    _require(
        payload.get("opened_sha256") == payload.get("canonical_source_sha256"),
        "Q01_RAW_SOURCE_SHA_MISMATCH",
        "same filename/shape cannot substitute for exact opened-byte SHA",
    )


def validate_parentage(payload: Mapping[str, Any]) -> None:
    receipt = payload.get("external_parent_receipt")
    _require(
        isinstance(receipt, Mapping),
        "Q01_DERIVATIVE_PARENT_RECEIPT_REQUIRED",
        "asserted source_sha256 inside a derivative is not parentage",
    )
    required = (
        "external_to_derivative_payload",
        "canonical_source_sha256",
        "derivative_hash",
        "producer_identity",
        "producer_code_identity",
        "producer_version",
        "derivation_operation",
        "scope_identity",
        "currentness_identity",
        "parent_receipt_identity",
        "replay_identity",
    )
    _require(
        all(key in receipt and receipt.get(key) not in (None, "") for key in required),
        "Q01_DERIVATIVE_PARENT_RECEIPT_MISMATCH",
        "parent receipt is incomplete",
    )
    _require(
        receipt.get("external_to_derivative_payload") is True,
        "Q01_DERIVATIVE_PARENT_RECEIPT_MISMATCH",
        "parentage must be external to the derivative payload",
    )
    _require(
        receipt.get("canonical_source_sha256") == payload.get("canonical_source_sha256")
        and receipt.get("derivative_hash") == payload.get("derivative_hash"),
        "Q01_DERIVATIVE_PARENT_RECEIPT_MISMATCH",
        "receipt does not bind this derivative to this canonical source",
    )
    if payload.get("decode_participates"):
        _require(
            bool(receipt.get("reader_config_identity")),
            "Q01_DERIVATIVE_PARENT_RECEIPT_MISMATCH",
            "source-decoding derivative receipt must bind exact reader/config",
        )
    expected_binding = payload.get("expected_binding")
    if expected_binding is not None:
        _require(
            receipt.get("binding") == expected_binding,
            "Q01_DERIVATIVE_CURRENTNESS_MISMATCH",
            "ancestry alone cannot qualify an old/wrong workload/runtime/root carrier",
        )


def validate_reader_config(payload: Mapping[str, Any]) -> None:
    candidate = payload.get("candidate_reader_config")
    expected = payload.get("expected_reader_config")
    _require(
        isinstance(candidate, Mapping) and isinstance(expected, Mapping)
        and dict(candidate) == dict(expected),
        "Q01_READER_CONFIG_MISMATCH",
        "canonical SHA does not authorize a different decoder/version/config/compatibility mode",
    )
    _require(
        candidate.get("encoding") not in {"auto", "guess", "fallback"},
        "Q01_READER_CONFIG_MISMATCH",
        "automatic reader guessing/fallback is forbidden",
    )


def validate_compatibility_boundary(payload: Mapping[str, Any]) -> None:
    _require(
        payload.get("compatibility_mode") == COMPATIBILITY_ONLY,
        "Q01_COMPATIBILITY_CANNOT_BECOME_SEMANTIC_AUTHORITY",
        "compatibility execution must retain its physical-only authority tag",
    )
    _require(
        payload.get("semantic_text_authority_claimed") is False
        and payload.get("repaired_text_promoted") is False,
        "Q01_COMPATIBILITY_CANNOT_BECOME_SEMANTIC_AUTHORITY",
        "successful compatibility decoding cannot manufacture intended-text semantics",
    )
    _require(
        payload.get("canonical_raw_retained") is True,
        "Q01_COMPATIBILITY_CANNOT_BECOME_SEMANTIC_AUTHORITY",
        "compatibility decoding cannot retire the canonical raw source",
    )


def validate_physical_metadata(payload: Mapping[str, Any]) -> None:
    paths = payload.get("required_paths")
    _require(
        isinstance(paths, list) and paths and all(isinstance(x, str) and x for x in paths),
        "Q01_PHYSICAL_WITNESS_DROPPED",
        "physical metadata court requires explicit applicable witness paths",
    )
    canonical = payload.get("canonical_physical")
    candidate = payload.get("candidate_physical")
    _require(
        isinstance(canonical, Mapping) and isinstance(candidate, Mapping),
        "Q01_PHYSICAL_WITNESS_DROPPED",
        "both canonical and candidate physical observations are required",
    )
    expected_selected = _selected(canonical, paths)
    candidate_selected = _selected(candidate, paths)
    _require(
        _digest(candidate_selected) == _digest(expected_selected),
        "Q01_PHYSICAL_METADATA_DIGEST_MISMATCH",
        "candidate dropped/rewrote/normalized a required physical witness",
    )


def validate_whole_source(payload: Mapping[str, Any]) -> None:
    claims_whole = payload.get("claims_whole_source") is True
    scope = payload.get("transport_scope")
    if not claims_whole:
        _require(
            scope == "WORKLOAD_EQUIVALENT",
            "Q01_WORKLOAD_STREAM_NOT_WHOLE_SOURCE",
            "non-whole-source transport must be explicitly workload-scoped",
        )
        return
    _require(
        scope == "WHOLE_SOURCE",
        "Q01_WORKLOAD_STREAM_NOT_WHOLE_SOURCE",
        "a queried-row/slot subset cannot be promoted to whole-source equivalence",
    )
    _require(
        payload.get("candidate_edge_classes") == payload.get("expected_edge_classes"),
        "Q01_WHOLE_SOURCE_EDGE_CLASS_CLOSURE_MISMATCH",
        "whole-source receipt must close every applicable S35 edge class",
    )
    _require(
        payload.get("candidate_physical_digest") == payload.get("canonical_physical_digest"),
        "Q01_WHOLE_SOURCE_PHYSICAL_DIGEST_MISMATCH",
        "I05 semantic parity cannot substitute for candidate-neutral whole-source physical digest equality",
    )


def validate_verdict_boundary(payload: Mapping[str, Any]) -> None:
    if payload.get("physical_equivalence") != "PASS":
        return
    implied = {"PASS_BY_IMPLICATION", "PASS_INFERRED_FROM_PHYSICAL"}
    _require(
        payload.get("semantic_parity") not in implied
        and payload.get("source_certification") not in implied,
        "Q01_PHYSICAL_PASS_CANNOT_IMPLY_SEMANTIC_CERTIFICATION",
        "physical equivalence is not semantic parity, source certification, weighting authority, or documentary authority",
    )
    if payload.get("semantic_parity") == "PASS":
        _require(
            payload.get("independent_semantic_receipt") is True,
            "Q01_PHYSICAL_PASS_CANNOT_IMPLY_SEMANTIC_CERTIFICATION",
            "semantic PASS requires its own independent receipt",
        )
    if payload.get("source_certification") == "PASS":
        _require(
            payload.get("independent_certification_receipt") is True,
            "Q01_PHYSICAL_PASS_CANNOT_IMPLY_SEMANTIC_CERTIFICATION",
            "source-certification PASS requires its own independent receipt",
        )


VALIDATORS = {
    "raw_source": validate_raw_source,
    "parentage": validate_parentage,
    "reader_config": validate_reader_config,
    "compatibility_boundary": validate_compatibility_boundary,
    "physical_metadata": validate_physical_metadata,
    "whole_source": validate_whole_source,
    "verdict_boundary": validate_verdict_boundary,
}


class R35GenericPhysicalGuardCourtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = cls.document["fixtures"]

    def test_fixture_schema_base_and_unique_ids(self):
        self.assertEqual(self.document["schema"], "FIABC_R35_Q01_HOSTILE_FIXTURES@1.0.0")
        self.assertEqual(self.document["base_sha"], "770d95c1a604ea1f47ac2971b923673c14c42984")
        self.assertTrue(self.document["no_raw_source_carriers_opened"])
        self.assertFalse(self.document["measured_p2x_run"])
        ids = [fixture["id"] for fixture in self.fixtures]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 20)

    def test_all_required_validator_families_present(self):
        present = {fixture["validator"] for fixture in self.fixtures}
        self.assertEqual(present, set(VALIDATORS))

    def test_positive_controls_pass(self):
        positives = [x for x in self.fixtures if x["expected_result"] == "PASS"]
        self.assertGreaterEqual(len(positives), 8)
        for fixture in positives:
            with self.subTest(fixture=fixture["id"]):
                VALIDATORS[fixture["validator"]](fixture["payload"])

    def test_hostile_fixtures_reject_with_exact_code(self):
        negatives = [x for x in self.fixtures if x["expected_result"] == "REJECT"]
        self.assertGreaterEqual(len(negatives), 16)
        for fixture in negatives:
            with self.subTest(fixture=fixture["id"]):
                with self.assertRaises(QualificationFailure) as caught:
                    VALIDATORS[fixture["validator"]](fixture["payload"])
                self.assertEqual(caught.exception.code, fixture["expected_code"])

    def test_commission_minimum_hostiles_are_explicit(self):
        required = {
            "R35Q-H01","R35Q-H02","R35Q-H03","R35Q-H04","R35Q-H05","R35Q-H06",
            "R35Q-H07","R35Q-H08","R35Q-H09","R35Q-H10","R35Q-H11","R35Q-H12",
            "R35Q-H13","R35Q-H14","R35Q-H15","R35Q-H16","R35Q-H17","R35Q-H18",
        }
        present = {fixture["id"] for fixture in self.fixtures}
        self.assertTrue(required.issubset(present), sorted(required - present))

    def test_latin2024_positive_control_preserves_both_conflicting_physical_witnesses(self):
        fixture = next(x for x in self.fixtures if x["id"] == "R35Q-P05")
        physical = fixture["payload"]["candidate_physical"]["layout"]
        self.assertEqual(physical["raw_header"]["nominal_case_size"], 174)
        self.assertEqual(physical["traversed"]["variable_count"], 332)
        self.assertNotEqual(
            physical["raw_header"]["nominal_case_size"],
            physical["traversed"]["variable_count"],
        )

    def test_equal_semantic_projection_can_still_fail_physical_metadata(self):
        fixture = next(x for x in self.fixtures if x["id"] == "R35Q-H17")
        self.assertEqual(fixture["payload"]["semantic_projection_digest"], "IDENTICAL-I05-PROJECTION")
        with self.assertRaises(QualificationFailure) as caught:
            validate_physical_metadata(fixture["payload"])
        self.assertEqual(caught.exception.code, "Q01_PHYSICAL_METADATA_DIGEST_MISMATCH")

    def test_i05_semantic_parity_does_not_override_whole_source_physical_failure(self):
        fixture = next(x for x in self.fixtures if x["id"] == "R35Q-H16")
        self.assertTrue(fixture["payload"]["i05_semantic_parity"])
        with self.assertRaises(QualificationFailure) as caught:
            validate_whole_source(fixture["payload"])
        self.assertEqual(caught.exception.code, "Q01_WHOLE_SOURCE_PHYSICAL_DIGEST_MISMATCH")

    def test_workload_equivalent_stream_can_be_lawful_without_claiming_whole_source(self):
        fixture = next(x for x in self.fixtures if x["id"] == "R35Q-P09")
        self.assertFalse(fixture["payload"]["claims_whole_source"])
        validate_whole_source(fixture["payload"])

    def test_physical_pass_never_implies_semantic_or_certification_pass(self):
        fixture = next(x for x in self.fixtures if x["id"] == "R35Q-P11")
        validate_verdict_boundary(fixture["payload"])
        self.assertEqual(fixture["payload"]["semantic_parity"], "NOT_ADJUDICATED_BY_R35_Q01")
        self.assertEqual(fixture["payload"]["source_certification"], "NOT_ADJUDICATED_BY_R35_Q01")


if __name__ == "__main__":
    unittest.main()
