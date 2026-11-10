"""Adversarial unit tests for copy-paste/agent type/intelligence preflight."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest
import json
import hashlib
import tempfile
import subprocess

SOURCE = Path(__file__).resolve().parents[1] / "CROSS_HQ_CONTROL_ROOM" / "verify_copy_paste_commission_r1.py"
spec = spec_from_file_location("commission_preflight", SOURCE)
gate = module_from_spec(spec)
spec.loader.exec_module(gate)

HEADER = {
 "REPOSITORY":"maidiu/rawlsing PRIVATE",
 "AGENT_TYPE":"Independent source-code forensic engineering investigator",
 "INTELLIGENCE_LEVEL":"I3",
 "SINGLE_AGENT_FULL_DELIVERABLE":"YES",
 "EXECUTION_SURFACE":"S2_LOCAL_GIT",
 "USER_SELECTED_EDITOR_MODEL_PAIR":"Proposed local OpenCode and DeepSeek Flash MAX user-selected",
 "MODEL":"DeepSeek V4.1-Flash",
 "REASONING":"MAX",
 "PROVIDER/EDITOR_HARNESS":"USER_SELECTED",
 "MODEL_MAX_AVAILABILITY":"UNKNOWN_UNTIL_VERIFIED",
 "HOST_ACCOUNT_QUOTA_COST":"UNKNOWN_UNTIL_VERIFIED",
 "BRANCH":"agent/example-historical-function-recovery-r1",
 "STARTUP_SHA":"a"*40,
 "ACTIVE_WORKER_NO_DISTURBANCE":"YES",
 "BROWSER?":"SCOPED_ONLY",
 "DEEPSEEK?":"MAX_PROPOSED",
 "CODEX_6_1_HIGH_NECESSARY?":"NO_PROOF",
 "OTHERWISE_MIDDLE?":"USER_DECISION",
 "WHY_NOT_BROWSER":"Needs local Git worktrees and runtime",
 "WHY_NOT_FLASH":"Not ruled out; verify MAX",
 "WHY_NOT_CODEX_HIGH":"No positive necessity",
 "WHY_NOT_MIDDLE":"Residual after evaluating MAX",
 "SCIENCE_SOURCE_ACTOR_AUTHORITY":"NO_SELF_ISSUANCE",
 "POST_RETURN_INDEPENDENT_REVIEW":"REQUIRED",
}

HEADER.update({
 "MCR":"REQUIRED",
 "COMMISSION_KIND":"BUILD",
 "CONTRACT_ID":"EXAMPLE-SOURCE-CONSUMER-COMMISSION",
 "CONTRACT_SOURCE_CUT":"CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py@"+"a"*40,
 "WORK_SCOPE_AND_FLIGHT":"PARENT=whole inherited source and consumer conservation; TRANCHE=all owned source-to-consumer claims; PILOT=NOT_APPLICABLE historical source check; PARALLEL=READY independent lanes",
 "TERMINAL_CONSUMER_AND_EFFECT":"CONSUMER=actual current selected-rule reader; EFFECT=authorized source rule affects downstream output",
 "FROZEN_ORACLE_AND_COUNTEREXAMPLE":"POS=expected selected source matches; NEG=unselected or absent source fails",
 "PREBUILD_CONTRACT_CHALLENGE":"CHALLENGE=short source pin silently accepted; DISPOSITION=reject incomplete Git commit identities",
 "EXECUTION_AND_AUTHOR_PREFLIGHT":"RUNNER=qualified Python Git checkout; PREFLIGHT=actual source and negative test at committed head",
 "CLOSURE_AND_OUT_OF_SCOPE":"ACCEPT_AT=source-graded complete owned obligation; EXCLUDE=unissued original source scientific rights",
})

EXAMPLE_SOURCE = {
 "path":"CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py",
 "commit":"a"*40, "blob":"b"*40,
}
EXAMPLE_SCOPE = {
 "parent":"Complete real source-to-consumer commissioned deliverable",
 "source":EXAMPLE_SOURCE,
 "expected_count":1,
 "enumerator":"RUN: python3 tools/frozen_source_id_enumerator.py",
 "no_drop_check":"RUN: python3 tools/exact_source_id_no_drop.py",
}
EXAMPLE_OBLIGATION = {
 "id":"EXACT-SOURCE-CONSUMER",
 "result":"Prove exact source identity and reader output within assigned scope",
 "output":"WORKER_RETURNS/commission/source-result.tsv",
 "check_kind":"SOURCE",
 "check":"SOURCE: compare exact Git source blob to frozen contract",
 "positive":"PASS=source tuple resolves exactly at required immutable version",
 "negative":"RED=truncated source hash fails the complete source identity test",
 "evidence":"WORKER_RETURNS/commission/demo-source-evidence.txt",
 "minimum_grade":"S1",
 "consumer":"actual current selected-rule consumer receiving boundary",
 "owner":"qualified independent source evidence reviewer",
 "failure":"INCOMPLETE",
 "source":EXAMPLE_SOURCE,
}
EXAMPLE_RECEIVING = {
 "gate":"python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --verify-return",
 "independent_owner":"distinct receiving reviewer of exact immutable candidate",
 "all_obligations":"PASS_REQUIRED",
 "author_ceiling":"DELIVERED_PENDING_RECEIVING",
 "on_any_failure":"INCOMPLETE",
}

def example_contract():
    return "\n".join([
        "MCR_COMPLETION_CONTRACT_BEGIN",
        "MCR_SCOPE: "+json.dumps(EXAMPLE_SCOPE, sort_keys=True),
        "MCR_OBLIGATION: "+json.dumps(EXAMPLE_OBLIGATION, sort_keys=True),
        "MCR_RECEIVING: "+json.dumps(EXAMPLE_RECEIVING, sort_keys=True),
        "MCR_COMPLETION_CONTRACT_END",
    ])

BODY = """
Perform exact historical source and review origin comparison with current receiving code.
Recover only sourcefully proven missing functions and name tests and first consumers.
ENGINEERING: compile/test on sourcefree qualified host; fault negatives.
SCIENTIFIC: distinguish tests from original measured meaning; unknown unless granted.
AUTHORITY: no source, model, N11/N12 or Sorok actor self-issuance.
Return function map and independent hostile review with precise source and current SHA.
"""


def prompt(overrides=None):
    hdr = {**HEADER, **(overrides or {})}
    inner = "LAUNCH - EXAMPLE COMMISSION\n" + "\n".join(f"{k}: {v}" for k,v in hdr.items())+"\n"+BODY+"\n"+example_contract()+"\n"
    fence = chr(96)*3
    return "**AGENT TYPE:** Independent Investigator **INTELLIGENCE LEVEL:** I3\n\n" + fence + "text\n"+inner+fence+"\n"


class CommissionProofTest(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(gate.validate(prompt())["status"].startswith("PASS"))
    def test_contract_source_sha_and_obligation_count(self):
        outcome = gate.validate(prompt())
        self.assertEqual(outcome["mcr_required_obligation_count"], 1)
        self.assertEqual(len(outcome["mcr_completion_contract_sha256"]), 64)

    def test_missing_authoring_contract_is_red(self):
        invalid = prompt().replace("MCR_COMPLETION_CONTRACT_BEGIN", "WRONG_BEGIN")
        self.assertEqual(gate.validate(invalid)["status"], "RED_INVALID_FOR_DISPATCH")

    def test_missing_obligation_is_red(self):
        invalid = "\n".join(line for line in prompt().splitlines()
                            if not line.startswith("MCR_OBLIGATION:"))
        self.assertIn("MCR_C_NO_OBLIGATIONS", gate.validate(invalid)["errors"])

    def test_duplicate_obligation_is_red(self):
        original = prompt()
        line = next(x for x in original.splitlines() if x.startswith("MCR_OBLIGATION:"))
        invalid = original.replace("MCR_RECEIVING:", line+"\nMCR_RECEIVING:")
        self.assertIn("MCR_C_DUPLICATE_ID_EXACT-SOURCE-CONSUMER",
                      gate.validate(invalid)["errors"])

    def test_truncated_material_source_sha_is_red(self):
        bad = prompt().replace('"commit": "'+"a"*40+'"', '"commit": "'+"a"*38+'"')
        self.assertEqual(gate.validate(bad)["status"], "RED_INVALID_FOR_DISPATCH")

    def test_hidden_filename_character_is_red(self):
        bad = prompt().replace("source-result.tsv", "sour\u00adce-result.tsv")
        self.assertIn("MCR_C_INVISIBLE_CHARACTER_IN_LAUNCH", gate.validate(bad)["errors"])

    def test_return_evidence_does_not_self_certify_completion(self):
        """Real Git checkout; exact committed source/output/coverage; never author adoption."""
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True,
                                      capture_output=True, text=True).stdout.strip()
            git("init")
            git("config", "user.name", "MCR Test")
            git("config", "user.email", "mcr-test@example.invalid")
            src_rel=EXAMPLE_SOURCE["path"]
            source_path=root/src_rel
            source_path.parent.mkdir(parents=True)
            source_path.write_text("frozen original source for MCR unit test\n")
            git("add", ".")
            git("commit", "-m", "freeze source")
            frozen=git("rev-parse", "HEAD")
            source_blob=git("rev-parse", frozen+":"+src_rel)
            commission=prompt().replace('"commit": "' + "a"*40 + '"',
                                        '"commit": "'+frozen+'"').replace(
                                        '"blob": "'+"b"*40+'"',
                                        '"blob": "'+source_blob+'"')
            source_cut="CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py@"
            commission=commission.replace(source_cut+"a"*40,source_cut+frozen)
            self.assertTrue(gate.validate(commission)["status"].startswith("PASS"))

            evidence_rel=Path(EXAMPLE_OBLIGATION["evidence"])
            output_rel=Path(EXAMPLE_OBLIGATION["output"])
            coverage_rel=Path("WORKER_RETURNS/commission/covered-ids.txt")
            for path, contents in (
                (evidence_rel,"actual source-to-consumer observation\n"),
                (output_rel,"id\tresult\nEXACT-SOURCE-CONSUMER\tPASS\n"),
                (coverage_rel,EXAMPLE_OBLIGATION["id"]+"\n"),
            ):
                dest=root/path
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_text(contents)
            git("add", ".")
            git("commit", "-m", "add exact delivered evidence")
            candidate=git("rev-parse","HEAD")
            contract_sha=gate.validate(commission)["mcr_completion_contract_sha256"]
            evidence={
                "id":EXAMPLE_OBLIGATION["id"], "candidate_sha":candidate,
                "contract_sha256":contract_sha,"status":"PASS","grade":"S1",
                "evidence_file":evidence_rel.as_posix(),
                "evidence_sha256":hashlib.sha256((root/evidence_rel).read_bytes()).hexdigest(),
                "output_file":output_rel.as_posix(),
                "output_sha256":hashlib.sha256((root/output_rel).read_bytes()).hexdigest(),
            }
            coverage={
                "candidate_sha":candidate, "contract_sha256":contract_sha,
                "delivered_ids_file":coverage_rel.as_posix(),
                "delivered_ids_sha256":hashlib.sha256((root/coverage_rel).read_bytes()).hexdigest(),
            }
            def make_return(proof=evidence,covered=coverage):
                data=["MCR_COMPLETION_EVIDENCE_BEGIN"]
                if covered is not None:
                    data.append("MCR_COVERAGE: "+json.dumps(covered,sort_keys=True))
                if proof is not None:
                    data.append("MCR_EVIDENCE: "+json.dumps(proof,sort_keys=True))
                return "\n".join([*data,"MCR_COMPLETION_EVIDENCE_END",""])
            ready=gate.verify_return(commission,make_return(),candidate,root)
            self.assertEqual(ready["status"],"READY_FOR_INDEPENDENT_RECEIVING",ready["errors"])
            self.assertNotIn("COMPLETE",ready["status"])
            mutations=[
                (dict(evidence,candidate_sha="e"*40),coverage,"MCR_C_PROOF_WRONG_CANDIDATE"),
                (dict(evidence,grade="S0"),coverage,"MCR_C_INSUFFICIENT_EVIDENCE_GRADE"),
                (dict(evidence,evidence_sha256="0"*64),coverage,"MCR_C_EVIDENCE_DIGEST_MISMATCH"),
                (dict(evidence,output_sha256="0"*64),coverage,"MCR_C_OUTPUT_DIGEST_MISMATCH"),
                (dict(evidence,status="NOT_RUN"),coverage,"MCR_C_PROOF_NOT_PASS"),
                (None,coverage,"MCR_C_MISSING_PROOF"),
                (evidence,None,"MCR_C_EXACT_ONE_SCOPE_COVERAGE_REQUIRED"),
                (evidence,dict(coverage,delivered_ids_sha256="0"*64),"MCR_C_COVERAGE_DIGEST_MISMATCH"),
                (evidence,dict(coverage,candidate_sha="e"*40),"MCR_C_COVERAGE_WRONG_CANDIDATE"),
            ]
            for proof,covered,marker in mutations:
                got=gate.verify_return(commission,make_return(proof,covered),candidate,root)
                self.assertEqual(got["status"],"RED_INCOMPLETE",marker)
                self.assertTrue(any(marker in err for err in got["errors"]),str(got))
            self.assertEqual(gate.verify_return(commission,make_return(),"f"*40,root)["status"],
                             "RED_INCOMPLETE")
            (root/evidence_rel).unlink()
            self.assertEqual(gate.verify_return(commission,make_return(),candidate,root)["status"],
                             "RED_INCOMPLETE")

    def test_no_agent_type(self):
        self.assertIn("MISSING_OR_EMPTY_AGENT_TYPE", gate.validate(prompt({"AGENT_TYPE":""}))["errors"])
    def test_bad_intelligence(self):
        self.assertIn("INVALID_INTELLIGENCE_CLASS", gate.validate(prompt({"INTELLIGENCE_LEVEL":"LOW"}))["errors"])
    def test_bad_sha(self):
        self.assertIn("EXACT_40_HEX_STARTUP_REQUIRED", gate.validate(prompt({"STARTUP_SHA":"main"}))["errors"])
    def test_invalid_branch(self):
        self.assertIn("EXACT_BRANCH_REQUIRED", gate.validate(prompt({"BRANCH":"maybe"}))["errors"])
    def test_no_visible_label(self):
        self.assertIn("NOT_VISIBLE_ABOVE_FENCE_AGENT_TYPE", gate.validate(prompt().replace("AGENT TYPE:", "ROLE:", 1))["errors"])
    def test_multiple_blocks(self):
        self.assertIn("REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK", gate.validate(prompt()+prompt())["errors"])
    def test_no_fence(self):
        self.assertIn("REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK", gate.validate(prompt().replace(chr(96)*3, ""))["errors"])


if __name__ == "__main__":
    unittest.main()
