import json

from rawlsing_next import rabochii_return_beacon as rb

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40
BLOB_A = "d" * 40
BLOB_B = "e" * 40
BRANCH = "agent/rabochii-example-r1"
RETURN_PATH = "data/returns/RETURN.md"


def valid_manifest():
    return {
        "schema_id": rb.MANIFEST_SCHEMA,
        "task_id": "EXAMPLE_R1",
        "branch": BRANCH,
        "commission": {
            "authority_ref": SHA_A,
            "exact_start_sha": SHA_B,
        },
        "return": {
            "result": "PASS",
            "terminal": "RABOCHII_EXAMPLE_R1__RETURN_TO_SUB_VOZHD",
            "phase": "CLOSURE_ONLY",
            "completion": {
                "commission_consumed": True,
                "all_required_outputs_durable": True,
                "no_required_work_remaining": True,
                "no_background_work_remaining": True,
                "return_packet_durable": True,
                "terminal_state_entered": True,
            },
        },
        "separation": {
            "performed_only_commissioned_role": True,
            "no_uncommissioned_repair": True,
            "no_uncommissioned_review": True,
        },
        "return_packet": {
            "path": RETURN_PATH,
            "blob_sha": BLOB_A,
        },
        "required_outputs": [
            {
                "name": "return_packet",
                "kind": "path",
                "path": RETURN_PATH,
                "blob_sha": BLOB_A,
                "status": "DURABLE",
            },
            {
                "name": "candidate",
                "kind": "commit",
                "sha": SHA_C,
                "status": "DURABLE",
            },
        ],
        "evidence": {
            "required": True,
            "workflow_name": "Rabochii Governed Bounded Court",
            "workflow_run_id": 123456789,
            "conclusion": "success",
            "evidence_execution_sha": SHA_C,
            "artifact_id": 456789,
        },
    }


def test_valid_manifest_shape_passes():
    assert rb.validate_manifest_shape(valid_manifest(), branch=BRANCH) == ()


def test_incomplete_manifest_never_certifies_shape():
    manifest = valid_manifest()
    manifest["return"]["completion"]["no_required_work_remaining"] = False
    errors = rb.validate_manifest_shape(manifest, branch=BRANCH)
    assert "return.completion.no_required_work_remaining must be true" in errors


def test_wrong_branch_and_nonclosure_rejected():
    manifest = valid_manifest()
    manifest["return"]["phase"] = "TERMINAL"
    errors = rb.validate_manifest_shape(manifest, branch="agent/other")
    assert "branch must exactly match the branch being certified" in errors
    assert "return.phase must be CLOSURE_ONLY" in errors


def test_invalid_terminal_rejected():
    manifest = valid_manifest()
    manifest["return"]["terminal"] = "looks done"
    assert any("return.terminal" in e for e in rb.validate_manifest_shape(manifest, branch=BRANCH))


def test_fail_is_valid_completed_outcome():
    manifest = valid_manifest()
    manifest["return"]["result"] = "FAIL"
    assert rb.validate_manifest_shape(manifest, branch=BRANCH) == ()


def test_blocked_is_valid_completed_outcome():
    manifest = valid_manifest()
    manifest["return"]["result"] = "BLOCKED"
    assert rb.validate_manifest_shape(manifest, branch=BRANCH) == ()


def test_incomplete_result_is_rejected():
    manifest = valid_manifest()
    manifest["return"]["result"] = "INCOMPLETE"
    assert "return.result must be PASS, FAIL, or BLOCKED" in rb.validate_manifest_shape(manifest, branch=BRANCH)


def test_required_output_must_be_durable():
    manifest = valid_manifest()
    manifest["required_outputs"][0]["status"] = "PENDING"
    assert any("status must be DURABLE" in e for e in rb.validate_manifest_shape(manifest, branch=BRANCH))


def test_evidence_required_needs_run_and_sha():
    manifest = valid_manifest()
    manifest["evidence"]["workflow_run_id"] = None
    manifest["evidence"]["evidence_execution_sha"] = None
    errors = rb.validate_manifest_shape(manifest, branch=BRANCH)
    assert any("workflow_run_id" in e for e in errors)
    assert any("evidence_execution_sha" in e for e in errors)


def test_evidence_can_be_explicitly_not_required():
    manifest = valid_manifest()
    manifest["evidence"] = {"required": False}
    assert rb.validate_manifest_shape(manifest, branch=BRANCH) == ()


def test_legacy_complete_pass_is_recognized():
    text = f"""
    State after terminal: `CLOSURE_ONLY`.
    Recommendation: `PASS__READY_FOR_REVIEW`
    `SELF_REVIEW_PERFORMED = NO`
    Run: `34253660939`
    Terminal: `RABOCHII_EXAMPLE_R6__RETURN_TO_SUB_VOZHD_E`
    """
    cert = rb.certify_legacy_return_text(text, branch=BRANCH, tip_sha=SHA_A)
    assert cert is not None
    assert cert.result == "PASS"
    assert cert.evidence_run_id == 34253660939
    assert cert.mode == "LEGACY_STRICT"


def test_legacy_incomplete_never_recognized():
    text = """
    Work is INCOMPLETE.
    CLOSURE_ONLY
    PASS__MAYBE
    SELF_REVIEW_PERFORMED = NO
    RABOCHII_EXAMPLE__RETURN_TO_SUB_VOZHD
    """
    assert rb.certify_legacy_return_text(text, branch=BRANCH, tip_sha=SHA_A) is None


def test_legacy_without_separation_marker_never_recognized():
    text = """
    CLOSURE_ONLY
    PASS__READY
    RABOCHII_EXAMPLE__RETURN_TO_SUB_VOZHD
    """
    assert rb.certify_legacy_return_text(text, branch=BRANCH, tip_sha=SHA_A) is None


class FakeClient:
    def __init__(self, manifest, *, evidence_conclusion="success", manifest_changed=True, packet_changed=True):
        self.manifest = manifest
        self.evidence_conclusion = evidence_conclusion
        self.manifest_changed = manifest_changed
        self.packet_changed = packet_changed

    def get_branch_tip(self, branch):
        assert branch == BRANCH
        return SHA_A

    def get_commit(self, sha):
        assert sha in {SHA_A, SHA_C}
        if sha == SHA_C:
            return {"sha": SHA_C}
        files = []
        if self.manifest_changed:
            files.append({"filename": rb.MANIFEST_PATH})
        if self.packet_changed:
            files.append({"filename": RETURN_PATH})
        return {"sha": SHA_A, "files": files, "commit": {"message": "Return EXAMPLE"}}

    def get_content(self, path, ref):
        assert ref == BRANCH
        if path == rb.MANIFEST_PATH:
            return json.dumps(self.manifest), BLOB_B
        if path == RETURN_PATH:
            return "return", BLOB_A
        raise FileNotFoundError(path)

    def resolve_commit(self, sha):
        assert sha == SHA_C

    def get_workflow_run(self, run_id):
        assert run_id == 123456789
        return {
            "status": "completed",
            "conclusion": self.evidence_conclusion,
            "name": "Rabochii Governed Bounded Court",
            "head_sha": SHA_C,
        }

    def get_artifact(self, artifact_id):
        assert artifact_id == 456789
        return {"id": artifact_id, "expired": False}


def test_repository_crosscheck_certifies_valid_manifest():
    manifest = valid_manifest()
    cert, errors = rb.certify_manifest_at_tip(FakeClient(manifest), branch=BRANCH)
    assert errors == ()
    assert cert is not None
    assert cert.tip_sha == SHA_A
    assert cert.result == "PASS"


def test_manifest_must_be_written_in_tip_commit():
    manifest = valid_manifest()
    cert, errors = rb.certify_manifest_at_tip(
        FakeClient(manifest, manifest_changed=False), branch=BRANCH
    )
    assert cert is None
    assert any("manifest must be written/updated" in e for e in errors)


def test_return_packet_must_be_written_in_same_tip():
    manifest = valid_manifest()
    cert, errors = rb.certify_manifest_at_tip(
        FakeClient(manifest, packet_changed=False), branch=BRANCH
    )
    assert cert is None
    assert any("return packet must be written/updated" in e for e in errors)


def test_evidence_conclusion_is_independently_crosschecked():
    manifest = valid_manifest()
    cert, errors = rb.certify_manifest_at_tip(
        FakeClient(manifest, evidence_conclusion="failure"), branch=BRANCH
    )
    assert cert is None
    assert "evidence workflow conclusion does not match manifest" in errors
