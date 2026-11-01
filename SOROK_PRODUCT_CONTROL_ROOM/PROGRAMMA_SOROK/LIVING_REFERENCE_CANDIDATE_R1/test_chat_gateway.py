"""Tests for the read-only ChatGPT query adapter; no native actor or external data."""
import json
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import Mock

import chat_gateway


class ReadOnlyChatGatewayTests(unittest.TestCase):
    def test_allowed_programme_queries(self):
        self.assertEqual(chat_gateway.validate({"verb": "home"}), ["home"])
        self.assertEqual(chat_gateway.validate({"verb": "focus", "id": "Q_HEALTH_001", "depth": 2}), ["focus", "Q_HEALTH_001", "--depth", "2"])
        self.assertEqual(chat_gateway.validate({"verb": "whole-gaps", "stage": "T"}), ["whole-gaps", "--stage", "T"])

    def test_rejects_mutations_unsafe_args_and_invented_commands(self):
        for req in (
            {"verb": "intake-return", "file": "whatever"},
            {"verb": "apply-authorized-transition"},
            {"verb": "refresh"},
            {"verb": "home", "id": "CAN011"},
            {"verb": "focus", "id": "../bad"},
            {"verb": "focus", "id": "Q_HEALTH_001", "depth": 100},
            {"verb": "whole-gaps", "stage": "T;rm -rf x"},
            {"verb": "home", "not_a_real_filter": "a"},
        ):
            with self.subTest(req=req), self.assertRaises(chat_gateway.ChatQueryError):
                chat_gateway.validate(req)

    def test_wrapper_returns_read_only_evidence_status_without_promotion(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "living_reference.py").write_text("pass\n")
            (root / "state.json").write_text("{}\n")
            runner = Mock(return_value=CompletedProcess(["python"], 0, json.dumps({"kernel": "KERNEL_UNRESOLVED"}), ""))
            output = chat_gateway.query({"verb": "home"}, root=root, runner=runner)
            self.assertEqual(output["result"]["kernel"], "KERNEL_UNRESOLVED")
            self.assertEqual(output["authority"]["native_science"], "HELD")
            argv = runner.call_args.args[0]
            self.assertNotIn("intake-return", argv)
            self.assertTrue(argv[-1] == "home")
            self.assertFalse(runner.call_args.kwargs["check"])

    def test_non_json_or_failure_cannot_promote(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "living_reference.py").write_text("pass\n")
            (root / "state.json").write_text("{}\n")
            for status, payload in ((0, "not JSON"), (2, "")):
                runner = Mock(return_value=CompletedProcess(["python"], status, payload, "bad"))
                with self.assertRaises(chat_gateway.ChatQueryError):
                    chat_gateway.query({"verb": "home"}, root=root, runner=runner)


if __name__ == "__main__":
    unittest.main()
