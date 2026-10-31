"""Adversarial unit tests for copy-paste/agent type/intelligence preflight."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

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
    inner = "LAUNCH - EXAMPLE COMMISSION\n" + "\n".join(f"{k}: {v}" for k,v in hdr.items())+"\n"+BODY
    fence = chr(96)*3
    return "**AGENT TYPE:** Independent Investigator **INTELLIGENCE LEVEL:** I3\n\n" + fence + "text\n"+inner+fence+"\n"


class CommissionProofTest(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(gate.validate(prompt())["status"].startswith("PASS"))
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
