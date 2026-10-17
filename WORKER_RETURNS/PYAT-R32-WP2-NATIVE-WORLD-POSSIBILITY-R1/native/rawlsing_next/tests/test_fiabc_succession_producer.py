from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping

import pytest

from rawlsing_next import fiabc_succession_producer as p
from rawlsing_next.fiabc_succession_preflight import (
    EvidenceResolver,
    ResolvedEvidence,
    evaluate_manifest,
)


ROOT = Path(__file__).resolve().parents[2]
HEAD = "a" * 40


class FakeResolver(EvidenceResolver):
    def resolve(self, evidence_ref: Mapping[str, Any]) -> ResolvedEvidence:
        return ResolvedEvidence(
            commit_sha=str(evidence_ref["resolved_commit_sha"]),
            blob_sha=str(evidence_ref.get("git_blob_sha", "b" * 40)),
            content_sha256=str(evidence_ref.get("content_sha256", "c" * 64)),
        )


def _t2() -> dict[str, Any]:
    return json.loads((ROOT / p.T2_PATH).read_text(encoding="utf-8"))


def _t5() -> dict[str, Any]:
    return json.loads((ROOT / p.T5_PATH).read_text(encoding="utf-8"))


def _fake_ref(
    repo_root: Path,
    *,
    commit: str,
    path: str,
    evidence_class: str,
    claim: str | None = None,
) -> dict[str, Any]:
    del repo_root
    value: dict[str, Any] = {
        "repo": "maidiu/rawlsing",
        "path": path,
        "ref": commit,
        "resolved_commit_sha": commit,
        "evidence_class": evidence_class,
    }
    if claim:
        value["claim"] = claim
    return value


def _fake_current_ref(
    repo_root: Path,
    head: str,
    path: str,
    evidence_class: str,
    claim: str | None = None,
) -> dict[str, Any]:
    return _fake_ref(
        repo_root,
        commit=head,
        path=path,
        evidence_class=evidence_class,
        claim=claim,
    )


@pytest.fixture
def synthetic_refs(monkeypatch):
    monkeypatch.setattr(p, "evidence_ref", _fake_ref)
    monkeypatch.setattr(p, "current_ref", _fake_current_ref)


def _built(synthetic_refs):
    del synthetic_refs
    t2, t5 = _t2(), _t5()
    manifest = p.build_manifest(
        repo_root=ROOT,
        head=HEAD,
        t2=t2,
        t5=t5,
    )
    lifecycle = p.build_lifecycle_context(
        repo_root=ROOT,
        head=HEAD,
        t2=t2,
        t5=t5,
    )
    return manifest, lifecycle


def test_generated_commit_sha_tracks_supplied_exact_head(synthetic_refs):
    manifest, lifecycle = _built(synthetic_refs)
    identity = manifest["manifest_identity"]
    assert identity["generated_from_commit_sha"] == HEAD
    assert identity["generated_from_ref"] == HEAD
    assert identity["frozen_before_candidate_execution"] is True
    assert lifecycle["generated_from_commit_sha"] == HEAD
    assert lifecycle["frozen_before_candidate_execution"] is True


def test_stale_or_wrong_head_is_rejected(synthetic_refs):
    manifest, lifecycle = _built(synthetic_refs)
    stale = copy.deepcopy(manifest)
    stale["manifest_identity"]["generated_from_commit_sha"] = "d" * 40
    with pytest.raises(p.SuccessionProducerError, match="stale"):
        p.assert_exact_head_binding(stale, lifecycle, actual_head=HEAD)

    with pytest.raises(p.SuccessionProducerError, match="does not equal expected head"):
        p.assert_exact_head_binding(
            manifest,
            lifecycle,
            actual_head=HEAD,
            expected_head="e" * 40,
        )


def test_wvs7_c_is_sixth_cell_and_order_matches_current_t2(synthetic_refs):
    _manifest, lifecycle = _built(synthetic_refs)
    assert lifecycle["cell_order"] == [
        {"source": "LITS_I", "candidate": "A"},
        {"source": "LITS_I", "candidate": "B"},
        {"source": "LITS_I", "candidate": "C"},
        {"source": "WVS7", "candidate": "A"},
        {"source": "WVS7", "candidate": "B"},
        {"source": "WVS7", "candidate": "C"},
    ]
    assert lifecycle["cell_order"][5] == {"source": "WVS7", "candidate": "C"}


def test_lits_a_s01_remains_measured_current_work(synthetic_refs):
    _manifest, lifecycle = _built(synthetic_refs)
    s01 = lifecycle["lits_a_s01"]
    assert s01["classification"] == "MEASURED_CURRENT_WORK__NOT_HISTORICAL_PRESERVATION"
    assert s01["manifest_tuple"][0] == "READY__RUN_LOCALLY"
    assert s01["manifest_tuple"][2] is True
    assert s01["manifest_tuple"][3] is True


def test_candidate_local_and_common_source_failure_scopes_are_exact(synthetic_refs):
    _manifest, lifecycle = _built(synthetic_refs)
    next_by_cell = lifecycle["candidate_local_failure_scope"]["next_by_cell"]
    assert next_by_cell == {
        "LITS_I/A": "LITS_I/B/S00_SOURCE_PREFLIGHT_IDENTITY",
        "LITS_I/B": "LITS_I/C/S00_SOURCE_PREFLIGHT_IDENTITY",
        "LITS_I/C": "WVS7/A/S00_SOURCE_PREFLIGHT_IDENTITY",
        "WVS7/A": "WVS7/B/S00_SOURCE_PREFLIGHT_IDENTITY",
        "WVS7/B": "WVS7/C/S01_CANDIDATE_PREPARATION_BUILD",
        "WVS7/C": "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION",
    }
    assert lifecycle["candidate_local_failure_scope"]["law"] == (
        "ONLY_CURRENT_CELL_IS_FAILED__LATER_LAWFUL_CELLS_REMAIN_REACHABLE"
    )
    assert lifecycle["common_source_failure_scope"] == {
        "law": "BLOCK_REMAINING_GOVERNED_STAGES_OF_CURRENT_SOURCE__THEN_ADVANCE_TO_NEXT_SOURCE_OR_FINAL_COURT_GATE",
        "terminal_disposition": "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
    }
    assert lifecycle["common_court_failure_scope"]["terminal_disposition"] == (
        "BLOCKED_BY_COMMON_COURT_AUTHORITY"
    )


def test_candidate_b_and_wvs7_c_no_cache_laws_are_preserved(synthetic_refs):
    _manifest, lifecycle = _built(synthetic_refs)
    assert lifecycle["candidate_b_no_cache"]["stop_law_ref"] == "PURE_B_NO_CACHE"
    assert lifecycle["wvs7_c_zero_accelerator_no_cache"]["stop_law_ref"] == (
        "C_ZERO_ACCELERATOR_NO_CACHE"
    )
    assert lifecycle["candidate_b_no_cache"]["stages"] == [
        "S12_STALE_CACHE_OR_PERSISTENT_STATE",
        "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE",
    ]


def test_generated_manifest_and_context_pass_existing_evaluator_on_synthetic_exact_refs(
    synthetic_refs,
):
    manifest, lifecycle = _built(synthetic_refs)
    result = evaluate_manifest(
        manifest,
        resolver=FakeResolver(),
        lifecycle_context=lifecycle,
    )
    assert result.status == "PASS", result.failure_codes
    assert len(result.checks) == 11
    assert all(check["status"] == "PASS" for check in result.checks)


def test_candidate_outputs_or_processes_cannot_be_nonzero(synthetic_refs):
    _manifest, lifecycle = _built(synthetic_refs)
    p.assert_zero_candidate_state(lifecycle)

    for key, value in (
        ("candidate_processes_started", 1),
        ("candidate_outputs_seen", 1),
        ("candidate_owned_roots_consulted", ["cells/LITS_I/A"]),
        ("ranking_or_selection", True),
    ):
        hostile = copy.deepcopy(lifecycle)
        hostile[key] = value
        with pytest.raises(p.SuccessionProducerError):
            p.assert_zero_candidate_state(hostile)


def test_current_owner_mapping_covers_exact_profile_required_function_set():
    profile = p.load_governing_profile()
    required = set(profile["function_boundary"]["required_before_terminal"])
    assert set(p.CURRENT_OWNER_PATHS) == required
    assert set(profile["function_boundary"]["all_functions"]) == (
        required | set(profile["function_boundary"]["deferred_beyond_terminal"])
    )


def test_repaired_execution_dependencies_are_provenance_not_semantic_owners():
    required = {
        "rawlsing_next/ee_p2x_darwin_stage_backend.py",
        "rawlsing_next/fiabc_lits_common_representation.py",
        "rawlsing_next/fiabc_lits_i_representation_authority.py",
        "rawlsing_next/fiabc_final_oracle_freeze_producers.py",
    }
    assert required <= set(p.CURRENT_EXECUTION_PROVENANCE_PATHS)
    assert required <= set(p.CURRENT_REQUIRED_PATHS)
    assert not required.intersection(p.CURRENT_OWNER_PATHS.values())


def test_real_current_head_producer_binds_repaired_dependencies_exactly(tmp_path: Path):
    head = p.checked_out_head(ROOT)
    manifest_path = tmp_path / "succession_manifest.json"
    lifecycle_path = tmp_path / "lifecycle_context.json"
    receipt_path = tmp_path / "producer_receipt.json"
    receipt = p.produce(
        repo_root=ROOT,
        manifest_output=manifest_path,
        lifecycle_output=lifecycle_path,
        receipt_output=receipt_path,
        expected_head=head,
        require_clean=True,
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lifecycle = json.loads(lifecycle_path.read_text(encoding="utf-8"))
    written_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    assert manifest["manifest_identity"]["generated_from_commit_sha"] == head
    assert lifecycle["generated_from_commit_sha"] == head
    assert receipt["generated_from_commit_sha"] == head
    assert receipt["expected_head"] == head
    assert receipt["clean_worktree_required"] is True
    manifest_bindings = manifest["current_head_bindings"]
    assert manifest_bindings["generated_from_commit_sha"] == head
    manifest_files = manifest_bindings["required_files"]
    receipt_files = receipt["current_head_bindings"]["required_files"]
    required = set(p.CURRENT_EXECUTION_PROVENANCE_PATHS)
    assert required == set(manifest_files)
    assert required <= set(receipt_files)
    assert written_receipt == receipt

    for path in sorted(required):
        manifest_ref = manifest_files[path]
        ref = receipt_files[path]
        blob = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "--verify", f"{head}:{path}"],
            text=True,
        ).strip()
        content = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{head}:{path}"]
        )
        assert ref["resolved_commit_sha"] == head
        assert ref["git_blob_sha"] == blob
        assert ref["content_sha256"] == hashlib.sha256(content).hexdigest()
        assert manifest_ref["path"] == path
        assert manifest_ref["ref"] == head
        assert manifest_ref["resolved_commit_sha"] == head
        assert manifest_ref["evidence_class"] == "CURRENT_IMPLEMENTATION"
        assert manifest_ref["git_blob_sha"] == blob
        assert manifest_ref["content_sha256"] == hashlib.sha256(content).hexdigest()

    assert receipt["evaluator_status"] == "PASS"
    assert receipt["evaluator_failure_codes"] == []
    assert receipt["candidate_processes_started"] == 0
    assert receipt["candidate_outputs_seen"] == 0
    assert receipt["candidate_owned_roots_consulted"] == []
    assert lifecycle["candidate_processes_started"] == 0
    assert lifecycle["candidate_outputs_seen"] == 0
    assert lifecycle["candidate_owned_roots_consulted"] == []
    assert lifecycle["cell_order"] == [
        {"source": "LITS_I", "candidate": "A"},
        {"source": "LITS_I", "candidate": "B"},
        {"source": "LITS_I", "candidate": "C"},
        {"source": "WVS7", "candidate": "A"},
        {"source": "WVS7", "candidate": "B"},
        {"source": "WVS7", "candidate": "C"},
    ]
    capability_realizations = {
        (item["source_id"], item["candidate_id"]): item["production_realization_ref"]
        for item in manifest["source_candidate_capabilities"]
    }
    assert p.CANDIDATE_REALIZATIONS == {
        "A": (p.OWNER_COMMIT, "rawlsing_next/pre553_r5_source_backed_adapter.py"),
        "B": (p.OWNER_COMMIT, "rawlsing_next/pre553_source_backed_c11_facade.py"),
        "C": ("CURRENT_HEAD", "rawlsing_next/pre553_candidate_c_production_binding.py"),
    }
    for source in ("LITS_I", "WVS7"):
        assert capability_realizations[(source, "A")]["resolved_commit_sha"] == p.OWNER_COMMIT
        assert capability_realizations[(source, "B")]["resolved_commit_sha"] == p.OWNER_COMMIT
        assert capability_realizations[(source, "C")]["resolved_commit_sha"] == head


def test_current_manifest_law_rejects_preserved_lits_a_s01():
    t2, t5 = _t2(), _t5()
    hostile = copy.deepcopy(t2)
    cell = next(
        cell for cell in hostile["cells"]
        if cell["source"] == "LITS_I" and cell["candidate"] == "A"
    )
    cell["stages"]["S01_CANDIDATE_PREPARATION_BUILD"][0] = "DONE__PRESERVE"
    with pytest.raises(p.SuccessionProducerError, match="LiTS/A current S01"):
        p._assert_current_manifest_law(hostile, t5)


def test_current_manifest_law_rejects_nonzero_accelerator_cache_escape():
    t2, t5 = _t2(), _t5()
    hostile = copy.deepcopy(t2)
    cell = next(
        cell for cell in hostile["cells"]
        if cell["source"] == "WVS7" and cell["candidate"] == "C"
    )
    cell["stages"]["S12_STALE_CACHE_OR_PERSISTENT_STATE"][0] = "READY__RUN_LOCALLY"
    with pytest.raises(p.SuccessionProducerError, match="zero-accelerator"):
        p._assert_current_manifest_law(hostile, t5)


def test_checked_out_head_is_derived_from_git_not_a_baked_commit(monkeypatch, tmp_path: Path):
    seen = []

    def fake_git(repo_root: Path, *args: str, binary: bool = False):
        del repo_root, binary
        seen.append(args)
        assert args == ("rev-parse", "--verify", "HEAD^{commit}")
        return HEAD

    monkeypatch.setattr(p, "_git", fake_git)
    assert p.checked_out_head(tmp_path) == HEAD
    assert seen == [("rev-parse", "--verify", "HEAD^{commit}")]


def test_dirty_worktree_blocks_before_production(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        p,
        "_git",
        lambda repo_root, *args, binary=False: " M rawlsing_next/file.py"
        if args == ("status", "--porcelain")
        else HEAD,
    )
    with pytest.raises(p.SuccessionProducerError, match="clean working tree"):
        p.require_clean_worktree(tmp_path)
