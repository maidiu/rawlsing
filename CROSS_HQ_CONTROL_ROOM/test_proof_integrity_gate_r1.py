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

    def test_requires_witness_for_claiming_join(self):
        code = "def test_release_to_consumer_join():\n    assert receipt == expected\n"
        self.assertTrue(gate.claimed_integration(code, "test_service.py"))
        self.assertFalse(gate.claimed_integration(
            "def test_hash_storage():\n    assert digest == expected\n", "test_hash_storage.py"))


if __name__ == "__main__":
    unittest.main()
