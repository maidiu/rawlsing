"""Self-tests of the mandatory shared proof gate; stdlib unittest only."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).with_name("proof_integrity_gate_r1.py")
spec = importlib.util.spec_from_file_location("proof_integrity_gate_r1", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ProofIntegrityGateTests(unittest.TestCase):
    def red(self, code):
        self.assertTrue(gate.lint_text(code, "test_example.py"), code)

    def test_reject_or_true(self):
        self.red("def test_x():\n    assert actual == expected or True\n")

    def test_reject_conditional_else_true(self):
        self.red("def test_x():\n    assert x == y if 'required' in obj else True\n")

    def test_reject_direct_true(self):
        self.red("def test_x():\n    assert True\n")

    def test_reject_noop_verification_loop(self):
        self.red("def test_x():\n    for step in steps:\n        pass\n")

    def test_reject_zero_length_hash_slice(self):
        self.red('def test_x():\n    assert blob == "abc"[:0] or len(blob) == 40\n')

    def test_reject_self_comparison(self):
        self.red("def test_x():\n    assert release == release\n")

    def test_allow_real_values_and_guarded_raises(self):
        code = (
            "import pytest\n"
            "def test_x():\n"
            "    assert released.ref == selected.ref\n"
            "    assert len(denominator_members) == 8\n"
            "    with pytest.raises(ValueError):\n"
            "        consume(None)\n"
        )
        self.assertEqual(gate.lint_text(code), [])

    def test_classifies_claim_word(self):
        code = "def test_release_to_consumer_join():\n    assert receipt == expected\n"
        self.assertTrue(gate.claimed_integration(code, "test_service.py"))
        self.assertFalse(gate.claimed_integration(
            "def test_hash_storage():\n    assert digest == expected\n", "test_hash_storage.py"))


    def test_executable_release_severance_witness(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory(prefix="proof-gate-selftest-") as d:
            root = Path(d)
            (root / "release.py").write_text("def get_release():\\n    return 3\\n".replace("\\n", "\n"), encoding="utf-8")
            (root / "test_link.py").write_text(
                "from release import get_release\\n"
                "def test_link_dependency():\\n"
                "    assert get_release() == 3\\n".replace("\\n", "\n"),
                encoding="utf-8",
            )
            manifest = root / "test_link.py.proof.json"
            manifest.write_text(json.dumps({
                "schema": gate.SCHEMA,
                "claims": [{
                    "claim_id": "SELFTEST_RELEASE_LINK",
                    "actual_consumer": "test_link_dependency",
                    "claimed_dependency": "release.get_release -> consumer",
                    "positive_node": "test_link.py::test_link_dependency",
                    "fault": {
                        "path": "release.py",
                        "old": "    return 3",
                        "new": "    return 4"
                    }
                }]
            }), encoding="utf-8")
            receipt = gate.witness(manifest, root)
            self.assertEqual(receipt["claims"][0]["fault_probe"], "TARGET_ASSERTION_FAILED")
            self.assertIn("return 3", (root / "release.py").read_text(encoding="utf-8"))



if __name__ == "__main__":
    unittest.main()
