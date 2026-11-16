from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.fiabc_succession_preflight import (
    PREFLIGHT_CONTRACT_ID,
    EvidenceResolver,
    PreflightResult,
    ResolvedEvidence,
    SuccessionPreflightBlocked,
    evaluate_manifest,
    load_governing_profile,
    run_only_after_preflight_pass,
    seal_manifest,
)


BASE = "56697a27e94eb9603dfa412a15ab8f1feb819b0c"
WORKLOAD = "617c9c9426db12a3c0f7fea6b68a582c10759553"
DEAD = "f" * 40
FIXTURES = Path(__file__).with_name("fixtures") / "fiabc_succession_preflight_hostile_cases.json"
CURRENT_EXECUTION_PROVENANCE_PATHS = (
    "rawlsing_next/ee_p2x_darwin_stage_backend.py",
    "rawlsing_next/fiabc_lits_common_representation.py",
    "rawlsing_next/fiabc_lits_i_representation_authority.py",
    "rawlsing_next/fiabc_final_oracle_freeze_producers.py",
)


class FakeResolver(EvidenceResolver):
    def __init__(self, fail_commits: set[str] | None = None) -> None:
        self.fail_commits = set(fail_commits or set())

    def resolve(self, evidence_ref: Mapping[str, Any]) -> ResolvedEvidence:
        commit = str(evidence_ref["resolved_commit_sha"])
        if commit in self.fail_commits:
            raise ValueError("fixture marks ref unresolved")
        return ResolvedEvidence(
            commit_sha=commit,
            blob_sha=str(evidence_ref.get("git_blob_sha", "a" * 40)),
            content_sha256=str(evidence_ref.get("content_sha256", "b" * 64)),
        )


def ev(
    path: str,
    evidence_class: str,
    commit: str = BASE,
    *,
    blob: str | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "repo": "maidiu/rawlsing",
        "path": path,
        "ref": commit,
        "resolved_commit_sha": commit,
        "evidence_class": evidence_class,
    }
    if blob is not None:
        value["git_blob_sha"] = blob
    return value


def _court_ref(name: str) -> dict[str, Any]:
    return ev(f"WORKER_RETURNS/FIABC-HQ-WAVE2-FANIN/{name}", "COURT_ADJUDICATION")


def _required_chain(function_id: str) -> dict[str, Any]:
    authority_id = f"AUTH_{function_id}"
    owner_id = f"OWNER_{function_id}"
    consumer_id = f"CONSUMER_{function_id}"
    historical = ev(f"historical/{function_id}.md", "HISTORICAL_EVIDENCE")
    authority = ev(f"authority/{function_id}.json", "ACCEPTED_AUTHORITY")
    current = ev(f"rawlsing_next/{function_id.lower()}_owner.py", "CURRENT_IMPLEMENTATION")
    receipt = ev(f"receipts/{function_id}.json", "GOVERNED_EXECUTION_RECEIPT")
    law = ev(f"authority/{function_id}_negative_state.json", "ACCEPTED_AUTHORITY")
    return {
        "function_id": function_id,
        "comparison_requirement": "REQUIRED_BEFORE_TERMINAL",
        "disposition": "PRESERVED_AND_CONSUMED",
        "obligation": {
            "function_id": function_id,
            "description": f"fixture obligation {function_id}",
            "historical_evidence_ref": historical,
        },
        "accepted_authority": [
            {
                "state": "PROVED",
                "authority_id": authority_id,
                "semantic_jurisdiction": f"JURISDICTION_{function_id}",
                "scope_exact": True,
                "resolution_evidence_ref": _court_ref("00_RETURN.md"),
                "authority_ref": authority,
            }
        ],
        "current_owner": {
            "state": "PROVED",
            "owner_id": owner_id,
            "owner_status": "CURRENT",
            "semantic_owner_id": authority_id,
            "resolution_evidence_ref": _court_ref("00_RETURN.md"),
            "implementation_ref": current,
            "currentness_ref": _court_ref("02_IMPLEMENTATION_OBLIGATION_LEDGER.csv"),
        },
        "executable_binding": {
            "state": "PROVED",
            "producer_owner_id": owner_id,
            "consumer_id": consumer_id,
            "entrypoint": f"rawlsing_next.{function_id.lower()}_owner:consume",
            "binding_identity_matches_owner": True,
            "resolution_evidence_ref": _court_ref("00_RETURN.md"),
            "binding_ref": current,
            "contract_receipt_ref": receipt,
        },
        "live_consumer": {
            "state": "LIVE",
            "consumer_id": consumer_id,
            "receipt_code_commit_matches": True,
            "receipt_after_required_repairs": True,
            "resolution_evidence_ref": receipt,
            "execution_code_ref": current,
            "receipt_ref": receipt,
        },
        "negative_state_law": {
            "state": "PROVED",
            "required_distinctions": ["UNKNOWN", "BLOCKED", "VALID_EMPTY"],
            "collapse_forbidden": True,
            "resolution_evidence_ref": _court_ref("00_RETURN.md"),
            "law_ref": law,
            "consumer_preservation_proof_ref": receipt,
        },
        "provenance_refs": [authority, current, receipt],
        "abc_class": {
            "invariant_ids": ["INV001"],
            "semantic_owner_id": authority_id,
            "cost_owner_id": f"COST_{function_id}",
            "cost_class": "CANDIDATE_OWNED_EXECUTION",
            "must_match_semantically": True,
        },
    }


def _deferred_chain(function_id: str, boundary_ref: Mapping[str, Any]) -> dict[str, Any]:
    authority_id = f"DEFERRED_AUTH_{function_id}"
    owner_id = f"DEFERRED_OWNER_{function_id}"
    consumer_id = f"DEFERRED_CONSUMER_{function_id}"
    historical = ev(f"historical/{function_id}.md", "HISTORICAL_EVIDENCE")
    return {
        "function_id": function_id,
        "comparison_requirement": "INTENTIONALLY_DEFERRED_BEYOND_TERMINAL",
        "deferment_authority_ref": copy.deepcopy(dict(boundary_ref)),
        "disposition": "INTENTIONALLY_DEFERRED_BEYOND_COMPARISON_BOUNDARY",
        "obligation": {
            "function_id": function_id,
            "description": f"fixture deferred obligation {function_id}",
            "historical_evidence_ref": historical,
        },
        "accepted_authority": [
            {
                "state": "DEFERRED_BY_AUTHORITY",
                "authority_id": authority_id,
                "semantic_jurisdiction": f"DEFERRED_{function_id}",
                "scope_exact": True,
                "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
            }
        ],
        "current_owner": {
            "state": "DEFERRED_BY_AUTHORITY",
            "owner_id": owner_id,
            "owner_status": "UNRESOLVED",
            "semantic_owner_id": authority_id,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "executable_binding": {
            "state": "DEFERRED_BY_AUTHORITY",
            "producer_owner_id": owner_id,
            "consumer_id": consumer_id,
            "entrypoint": "DEFERRED_BY_BOUNDARY",
            "binding_identity_matches_owner": True,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "live_consumer": {
            "state": "DEFERRED_BY_AUTHORITY",
            "consumer_id": consumer_id,
            "receipt_code_commit_matches": False,
            "receipt_after_required_repairs": False,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "negative_state_law": {
            "state": "DEFERRED_BY_AUTHORITY",
            "required_distinctions": ["DEFERRED_BY_AUTHORITY"],
            "collapse_forbidden": True,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "provenance_refs": [copy.deepcopy(dict(boundary_ref))],
        "abc_class": {
            "invariant_ids": [],
            "semantic_owner_id": authority_id,
            "cost_owner_id": "EXCLUDED_DOWNSTREAM",
            "cost_class": "EXCLUDED_DOWNSTREAM",
            "must_match_semantically": False,
        },
    }


def passing_manifest() -> dict[str, Any]:
    profile = load_governing_profile()
    scope = profile["court_scope"]
    boundary_ref = profile["comparison_terminal"]["boundary_adjudication_ref"]
    closure_ref = profile["semantic_authority_closure"]["closure_ref"]
    required = set(profile["function_boundary"]["required_before_terminal"])
    deferred = set(profile["function_boundary"]["deferred_beyond_terminal"])

    chains: list[dict[str, Any]] = []
    for number in range(1, 37):
        function_id = f"F{number:03d}"
        if function_id in required:
            chains.append(_required_chain(function_id))
        elif function_id in deferred:
            chains.append(_deferred_chain(function_id, boundary_ref))
        else:
            raise AssertionError(f"profile leaves {function_id} unclassified")

    capabilities = []
    for source in scope["sources"]:
        for candidate in scope["candidates"]:
            capabilities.append(
                {
                    "source_id": source,
                    "candidate_id": candidate,
                    "state": "PROVED",
                    "capability_contract_ref": ev(
                        f"authority/capability_{source}_{candidate}.json", "ACCEPTED_AUTHORITY"
                    ),
                    "resolution_evidence_ref": _court_ref("00_RETURN.md"),
                    "production_realization_ref": ev(
                        f"rawlsing_next/candidate_{candidate.lower()}_{source.lower()}.py",
                        "CURRENT_IMPLEMENTATION",
                    ),
                    "synthetic_fixture_substitution_forbidden": True,
                    "disposition": "PRESERVED_AND_CONSUMED",
                }
            )

    manifest = {
        "manifest_schema": "RAWLSING_FIABC_SUCCESSION_MANIFEST@1.0.0",
        "manifest_identity": {
            "generated_from_ref": BASE,
            "generated_from_commit_sha": BASE,
            "manifest_content_sha256": "0" * 64,
            "frozen_before_candidate_execution": True,
        },
        "current_head_bindings": {
            "generated_from_commit_sha": BASE,
            "required_files": {
                path: ev(path, "CURRENT_IMPLEMENTATION")
                for path in CURRENT_EXECUTION_PROVENANCE_PATHS
            },
        },
        "court_scope": {
            "sources": list(scope["sources"]),
            "candidates": list(scope["candidates"]),
            "claim_scope_id": scope["claim_scope_id"],
            "workload_ref": copy.deepcopy(scope["workload_ref"]),
        },
        "comparison_terminal": {
            "state": "PROVED",
            "terminal_id": profile["comparison_terminal"]["terminal_id"],
            "resolution_evidence_ref": copy.deepcopy(boundary_ref),
            "output_contract_ref": _court_ref("00_RETURN.md"),
            "boundary_adjudication_ref": copy.deepcopy(boundary_ref),
        },
        "upstream_freeze": {
            "state": "PROVED",
            "resolution_evidence_ref": _court_ref("00_RETURN.md"),
            "candidate_neutral_work_frozen": True,
            "semantic_authority_closure_ref": copy.deepcopy(closure_ref),
            "producer_outputs": [copy.deepcopy(scope["workload_ref"])],
        },
        "function_chains": chains,
        "abc_invariants": [
            {
                "invariant_id": "INV001",
                "state": "PROVED",
                "logical_property": "Exact governed terminal semantics/replay/output remain candidate-neutral.",
                "must_match_across_abc": True,
                "physical_difference_allowed": True,
                "resolution_evidence_ref": _court_ref("00_RETURN.md"),
                "authority_ref": ev("authority/inv001.json", "ACCEPTED_AUTHORITY"),
                "proof_ref": ev("receipts/inv001.json", "GOVERNED_EXECUTION_RECEIPT"),
            }
        ],
        "source_candidate_capabilities": capabilities,
        "parity_oracle": {
            "state": "PROVED",
            "resolution_evidence_ref": _court_ref("00_RETURN.md"),
            "frozen_before_candidate_output": True,
            "candidate_output_used_to_construct_expected_truth": False,
            "oracle_contract_ref": ev("authority/parity_contract.json", "COURT_ADJUDICATION"),
            "oracle_material_ref": ev("authority/parity_expected_truth.json", "ACCEPTED_AUTHORITY"),
            "fixed_frontier_ref": ev("authority/fixed_frontier.json", "ACCEPTED_AUTHORITY"),
            "negative_state_expectation_ref": ev("authority/negative_states.json", "ACCEPTED_AUTHORITY"),
        },
        "accounting_contract": {
            "state": "PROVED",
            "resolution_evidence_ref": _court_ref("00_RETURN.md"),
            "semantic_owner_cost_owner_separated": True,
            "constitution_ref": ev("authority/equal_work.json", "MEASUREMENT_CONSTITUTION"),
            "candidate_start_stop_ref": ev("authority/candidate_boundaries.json", "MEASUREMENT_CONSTITUTION"),
            "preserved_work_treatment_ref": ev("authority/preserved_work.json", "MEASUREMENT_CONSTITUTION"),
            "candidate_process_isolation_ref": ev("authority/process_isolation.json", "MEASUREMENT_CONSTITUTION"),
            "metrics": [
                {
                    "metric_id": "cpu_candidate_total_ns",
                    "definition_ref": ev("authority/metric_cpu.json", "MEASUREMENT_CONSTITUTION"),
                    "candidate_local": True,
                    "accumulation_semantics": "TOTAL_OVER_CANDIDATE_BOUNDARY",
                    "measurement_kind": "OBSERVED",
                    "overwritten_before_terminal": False,
                    "method_identity_across_candidates": "CPU_PROCESS_TIME_CANDIDATE_TOTAL@1",
                }
            ],
        },
        "preflight_evaluation": {
            "contract_id": PREFLIGHT_CONTRACT_ID,
            "status": "BLOCK",
            "checks": [
                {
                    "check_id": "UNEVALUATED",
                    "status": "BLOCK",
                    "failure_code": "PF_UNEVALUATED",
                    "evidence_refs": [],
                }
            ],
            "evaluated_manifest_sha256": "0" * 64,
        },
    }
    return seal_manifest(manifest)


def passing_lifecycle() -> dict[str, Any]:
    return {
        "state": "PROVED",
        "failure_scope_ambiguous": False,
        "failure_scope_misclassified": False,
        "lifecycle_order_matches": True,
        "terminal_history_fresh_for_retry": True,
        "evidence_refs": [ev("receipts/lifecycle.json", "GOVERNED_EXECUTION_RECEIPT")],
    }


def _chain(manifest: dict[str, Any], function_id: str) -> dict[str, Any]:
    return next(item for item in manifest["function_chains"] if item["function_id"] == function_id)


def _cell(manifest: dict[str, Any], source: str, candidate: str) -> dict[str, Any]:
    return next(
        item
        for item in manifest["source_candidate_capabilities"]
        if item["source_id"] == source and item["candidate_id"] == candidate
    )


def _complete_missingness() -> dict[str, Any]:
    return {
        "historical_authority_checked": True,
        "alternate_current_owner_checked": True,
        "disconnected_binding_checked": True,
        "superseded_implementation_checked": True,
        "intentional_deferral_checked": True,
        "search_evidence_refs": [_court_ref("00_RETURN.md")],
    }


def apply_mutation(
    mutation: str,
    manifest: dict[str, Any],
    lifecycle: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], FakeResolver]:
    resolver = FakeResolver()

    if mutation == "missing_binding_and_receipt":
        chain = _chain(manifest, "F032")
        chain["executable_binding"]["state"] = "MISSING"
        chain["live_consumer"]["state"] = "PRESENT_NOT_LIVE_PROVED"
    elif mutation == "stale_binding_ref":
        ref = _chain(manifest, "F004")["executable_binding"]["binding_ref"]
        ref["ref"] = DEAD
        ref["resolved_commit_sha"] = DEAD
        resolver = FakeResolver({DEAD})
    elif mutation == "wrong_owner_wrapper":
        binding = _chain(manifest, "F004")["executable_binding"]
        binding["producer_owner_id"] = "WRONG_OWNER"
        binding["binding_identity_matches_owner"] = False
        binding["entrypoint"] = "wrapper:self"
    elif mutation == "stale_live_receipt":
        consumer = _chain(manifest, "F032")["live_consumer"]
        consumer["state"] = "PRESENT_NOT_LIVE_PROVED"
        consumer["receipt_code_commit_matches"] = False
        consumer["receipt_after_required_repairs"] = False
    elif mutation == "candidate_self_replay_oracle":
        oracle = manifest["parity_oracle"]
        oracle["frozen_before_candidate_output"] = False
        oracle["candidate_output_used_to_construct_expected_truth"] = True
        oracle["oracle_material_ref"] = copy.deepcopy(_cell(manifest, "LITS_I", "A")["production_realization_ref"])
    elif mutation == "unequal_work_accounting":
        accounting = manifest["accounting_contract"]
        accounting["state"] = "UNRESOLVED"
        metric = accounting["metrics"][0]
        metric["candidate_local"] = False
        metric["overwritten_before_terminal"] = True
        metric["accumulation_semantics"] = "DOCUMENTARY_ONLY"
        metric["measurement_kind"] = "OBSERVED"
    elif mutation == "lits_c_partial_capability":
        cell = _cell(manifest, "LITS_I", "C")
        cell["state"] = "MISSING"
        cell["disposition"] = "PARTIAL_SUCCESSION"
        cell.pop("production_realization_ref", None)
        cell["synthetic_fixture_substitution_forbidden"] = False
    elif mutation == "wvs_c_not_applicable_portability":
        cell = _cell(manifest, "WVS7", "C")
        cell["state"] = "NOT_APPLICABLE"
        cell["disposition"] = "GENUINELY_MISSING"
        cell.pop("production_realization_ref", None)
        cell["missingness_search"] = _complete_missingness()
    elif mutation == "missing_semantic_authority":
        authority = _chain(manifest, "F005")["accepted_authority"][0]
        authority["state"] = "MISSING"
        authority["authority_ref"]["evidence_class"] = "CURRENT_IMPLEMENTATION"
    elif mutation == "lifecycle_scope_and_order":
        lifecycle["failure_scope_misclassified"] = True
        lifecycle["lifecycle_order_matches"] = False
        lifecycle["terminal_history_fresh_for_retry"] = False
    elif mutation == "producer_consumer_contract_mismatch":
        _chain(manifest, "F023")["executable_binding"]["consumer_id"] = "WRONG_CONSUMER"
    elif mutation == "stale_verifier_and_unclosed_provenance":
        chain = _chain(manifest, "F023")
        chain["executable_binding"]["consumer_id"] = "WRONG_CONSUMER"
        chain["provenance_refs"] = []
    elif mutation == "floating_evidence_ref":
        manifest["court_scope"]["workload_ref"]["ref"] = "HEAD"
    elif mutation == "historical_owner":
        _chain(manifest, "F010")["current_owner"]["owner_status"] = "HISTORICAL_ONLY"
    elif mutation == "negative_state_collapse":
        _chain(manifest, "F010")["negative_state_law"]["collapse_forbidden"] = False
    elif mutation == "semantic_inference_substitution":
        _chain(manifest, "F005")["accepted_authority"][0]["authority_ref"]["evidence_class"] = "CURRENT_IMPLEMENTATION"
    elif mutation == "metric_method_mismatch":
        other = copy.deepcopy(manifest["accounting_contract"]["metrics"][0])
        other["method_identity_across_candidates"] = "INCOMPATIBLE_CPU_METHOD@1"
        manifest["accounting_contract"]["metrics"].append(other)
    elif mutation == "illegal_deferment":
        chain = _chain(manifest, "F010")
        chain["comparison_requirement"] = "INTENTIONALLY_DEFERRED_BEYOND_TERMINAL"
        chain["deferment_authority_ref"] = copy.deepcopy(
            load_governing_profile()["comparison_terminal"]["boundary_adjudication_ref"]
        )
        chain["disposition"] = "INTENTIONALLY_DEFERRED_BEYOND_COMPARISON_BOUNDARY"
    elif mutation == "genuine_missing_without_search":
        chain = _chain(manifest, "F010")
        chain["disposition"] = "GENUINELY_MISSING"
        chain.pop("missingness_search", None)
    elif mutation == "semantic_cost_owner_conflated":
        abc = _chain(manifest, "F010")["abc_class"]
        abc["cost_owner_id"] = abc["semantic_owner_id"]
    else:
        raise AssertionError(f"unknown hostile mutation: {mutation}")

    return seal_manifest(manifest), lifecycle, resolver


class SuccessionPreflightTests(unittest.TestCase):
    def test_complete_manifest_passes_all_eleven_phases(self) -> None:
        result = evaluate_manifest(
            passing_manifest(),
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertEqual(result.status, "PASS", result.failure_codes)
        self.assertEqual(len(result.checks), 11)
        self.assertTrue(all(item["status"] == "PASS" for item in result.checks))

    def test_current_execution_provenance_requires_all_four_exact_head_bindings(self) -> None:
        manifest = passing_manifest()
        result = evaluate_manifest(
            manifest,
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertEqual(result.status, "PASS", result.failure_codes)
        bindings = manifest["current_head_bindings"]
        self.assertEqual(bindings["generated_from_commit_sha"], BASE)
        self.assertEqual(set(bindings["required_files"]), set(CURRENT_EXECUTION_PROVENANCE_PATHS))
        p00 = next(check for check in result.checks if check["check_id"] == "P00")
        p00_paths = {ref["path"] for ref in p00["evidence_refs"]}
        self.assertTrue(set(CURRENT_EXECUTION_PROVENANCE_PATHS) <= p00_paths)
        self.assertTrue(
            all(
                ref["path"] == path
                and ref["ref"] == BASE
                and ref["resolved_commit_sha"] == BASE
                for path, ref in bindings["required_files"].items()
            )
        )

        missing = copy.deepcopy(manifest)
        del missing["current_head_bindings"]["required_files"][CURRENT_EXECUTION_PROVENANCE_PATHS[0]]
        missing = seal_manifest(missing)
        missing_result = evaluate_manifest(
            missing,
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertEqual(missing_result.status, "BLOCK")
        self.assertIn("PF_CURRENT_HEAD_BINDING_MISSING", missing_result.failure_codes)

        mismatched = copy.deepcopy(manifest)
        mismatched["current_head_bindings"]["required_files"][CURRENT_EXECUTION_PROVENANCE_PATHS[0]]["ref"] = DEAD
        mismatched["current_head_bindings"]["required_files"][CURRENT_EXECUTION_PROVENANCE_PATHS[0]]["resolved_commit_sha"] = DEAD
        mismatched = seal_manifest(mismatched)
        mismatch_result = evaluate_manifest(
            mismatched,
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertEqual(mismatch_result.status, "BLOCK")
        self.assertIn("PF_CURRENT_HEAD_BINDING_MISMATCH", mismatch_result.failure_codes)

    def test_missing_lifecycle_context_fails_closed(self) -> None:
        result = evaluate_manifest(
            passing_manifest(),
            resolver=FakeResolver(),
            lifecycle_context=None,
        )
        self.assertEqual(result.status, "BLOCK")
        self.assertIn("PF_FAILURE_SCOPE_AMBIGUOUS", result.failure_codes)
        self.assertIn("PF_LIFECYCLE_ORDER_MISMATCH", result.failure_codes)

    def test_mutation_after_freeze_breaks_manifest_identity(self) -> None:
        manifest = passing_manifest()
        manifest["court_scope"]["claim_scope_id"] = "MUTATED_AFTER_FREEZE"
        result = evaluate_manifest(
            manifest,
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertEqual(result.status, "BLOCK")
        self.assertIn("PF_REF_CONTENT_MISMATCH", result.failure_codes)

    def test_all_known_blockers_and_false_pass_cases_block(self) -> None:
        fixture = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cases = fixture["known_blocker_replays"] + fixture["false_pass_challenges"]
        for case in cases:
            with self.subTest(case_id=case["case_id"], mutation=case["mutation"]):
                manifest = copy.deepcopy(passing_manifest())
                lifecycle = copy.deepcopy(passing_lifecycle())
                manifest, lifecycle, resolver = apply_mutation(case["mutation"], manifest, lifecycle)
                result = evaluate_manifest(
                    manifest,
                    resolver=resolver,
                    lifecycle_context=lifecycle,
                )
                self.assertEqual(result.status, "BLOCK")
                for expected in case["expected_failure_codes"]:
                    self.assertIn(expected, result.failure_codes)

    def test_repository_presence_without_live_consumption_cannot_pass(self) -> None:
        manifest = passing_manifest()
        chain = _chain(manifest, "F033")
        self.assertEqual(chain["current_owner"]["state"], "PROVED")
        chain["live_consumer"]["state"] = "PRESENT_NOT_LIVE_PROVED"
        result = evaluate_manifest(
            seal_manifest(manifest),
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertIn("PF_LIVE_CONSUMER_DISCONNECTED", result.failure_codes)
        self.assertIn("PF_LIVE_RECEIPT_MISSING", result.failure_codes)

    def test_historical_immutable_evidence_is_not_rejected_unless_used_as_current_owner(self) -> None:
        manifest = passing_manifest()
        # Historical evidence is lawful in the obligation/provenance estate.
        self.assertEqual(_chain(manifest, "F010")["obligation"]["historical_evidence_ref"]["evidence_class"], "HISTORICAL_EVIDENCE")
        pass_result = evaluate_manifest(
            manifest,
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertEqual(pass_result.status, "PASS")

        _chain(manifest, "F010")["current_owner"]["owner_status"] = "HISTORICAL_ONLY"
        block_result = evaluate_manifest(
            seal_manifest(manifest),
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        self.assertIn("PF_OWNER_SUPERSEDED_OR_HISTORICAL", block_result.failure_codes)

    def test_guard_never_invokes_execution_action_on_block(self) -> None:
        manifest = passing_manifest()
        _chain(manifest, "F032")["live_consumer"]["state"] = "PRESENT_NOT_LIVE_PROVED"
        result = evaluate_manifest(
            seal_manifest(manifest),
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        called: list[str] = []

        def measured_action() -> str:
            called.append("called")
            return "should-not-run"

        with self.assertRaises(SuccessionPreflightBlocked):
            run_only_after_preflight_pass(result, measured_action)
        self.assertEqual(called, [])

    def test_guard_invokes_action_only_after_pass(self) -> None:
        result: PreflightResult = evaluate_manifest(
            passing_manifest(),
            resolver=FakeResolver(),
            lifecycle_context=passing_lifecycle(),
        )
        called: list[str] = []

        def action() -> str:
            called.append("called")
            return "ok"

        self.assertEqual(run_only_after_preflight_pass(result, action), "ok")
        self.assertEqual(called, ["called"])


if __name__ == "__main__":
    unittest.main()
