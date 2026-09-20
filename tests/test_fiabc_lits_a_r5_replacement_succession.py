from __future__ import annotations

import json
import subprocess
import unittest
from copy import deepcopy
from pathlib import Path

from rawlsing_next.fiabc_derivative_parentage import (
    mint_derivative_parentage_receipt,
    mint_parentage_bundle,
    mint_source_verification_receipt,
)
from rawlsing_next.fiabc_lits_a_r5_replacement_succession import (
    ReplacementSuccessionError,
    evaluate_replacement_attempt,
    verify_successor_authority,
)

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = ROOT / "WORKER_RETURNS" / "FIABC-LM1-R1B" / "02_R5_REPLACEMENT_SUCCESSION.json"
BACKEND_PATH = ROOT / "rawlsing_next" / "ee_p2x_darwin_stage_backend.py"
T2_PATH = ROOT / "WORKER_RETURNS" / "FIABC-T2" / "01_SIX_CELL_EXECUTION_MANIFEST.json"
EXPECTED_T2_GIT_BLOB = "0864534765a34eded37137c545d750f741e31d7a"
EXPECTED_T2_SHA256 = "035a20dfaa9e1009fd845d653ca089ca77517e446cd47106ecdb1e1eda252bf6"
MALFORMED = {
    "72f8e8a2b6b2330332030e3978077c11e38ec8db",
    "92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55",
    "62cea85788eb160796642ba09d9f0d41f987a3d43",
    "cef346fca029fa920db16e83db908d466018f39e",
    "ffb07a9d0bafbf685d27aa1161ce830bcfc810fc",
}
OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
CORRECT_BY_PATH = {
    "rawlsing_next/pre553_r5_codec.py": "72f8f3c03ed065e86fea4e76bb17f8e06c2bf540",
    "rawlsing_next/pre553_r5_compact_carrier.py": "92e364b31eaf27be1bca2081eff65f6ffb779c3d",
    "rawlsing_next/pre553_r5_model.py": "62ce608829c3d9c2fb7c999aefe40188637edf80",
    "rawlsing_next/pre553_r5_seam.py": "cef326ebbc40468428378f7fdbe76e4756179f39",
    "rawlsing_next/pre553_r5_single_pass_audit69.py": "ffb063b93c86e215604eecb29a9545c7efdff399",
}
CORRECT = {
    "72f8f3c03ed065e86fea4e76bb17f8e06c2bf540",
    "92e364b31eaf27be1bca2081eff65f6ffb779c3d",
    "62ce608829c3d9c2fb7c999aefe40188637edf80",
    "cef326ebbc40468428378f7fdbe76e4756179f39",
    "ffb063b93c86e215604eecb29a9545c7efdff399",
}


class ReplacementSuccessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.authority = json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))

    def request(self, **overrides):
        values = dict(
            source_id="LITS_I",
            candidate="A",
            derivative_family="R5",
            attempt_state="INTERRUPTED_INCOMPLETE",
        )
        values.update(overrides)
        return evaluate_replacement_attempt(self.authority, **values)

    def test_01_malformed_five_object_pointer_set_rejected(self):
        text = BACKEND_PATH.read_text(encoding="utf-8")
        self.assertTrue(all(pointer not in text for pointer in MALFORMED))

    def test_02_corrected_pointers_are_accepted_owner_objects(self):
        text = BACKEND_PATH.read_text(encoding="utf-8")
        self.assertTrue(all(pointer in text for pointer in CORRECT))
        for path, expected_blob in CORRECT_BY_PATH.items():
            actual = subprocess.check_output(
                ["git", "rev-parse", f"{OWNER_COMMIT}:{path}"],
                cwd=ROOT,
                text=True,
            ).strip()
            self.assertEqual(actual, expected_blob)

    def test_03_nonexistent_builder_blob_cannot_be_admitted(self):
        broken = deepcopy(self.authority)
        broken["replacement_contract"]["builder"]["code_blob"] = "92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55"
        with self.assertRaises(ReplacementSuccessionError):
            verify_successor_authority(broken)

    def test_04_old_unparented_r5_stays_invalid(self):
        with self.assertRaises(ReplacementSuccessionError):
            self.request(
                attempt_state="SUCCESSFULLY_SEALED",
                admitted_derivative_identity="a" * 64,
            )

    def test_05_scope_is_only_lits_a_r5(self):
        self.assertEqual(self.request()["status"], "RETRY_ALLOWED_UNDER_EXISTING_RECOVERY_LAW")
        with self.assertRaises(ReplacementSuccessionError):
            self.request(derivative_family="CACHE")

    def test_06_candidate_b_cannot_consume(self):
        with self.assertRaises(ReplacementSuccessionError):
            self.request(candidate="B")

    def test_07_wvs_cannot_consume(self):
        with self.assertRaises(ReplacementSuccessionError):
            self.request(source_id="WVS7")

    def test_08_second_successful_replacement_forbidden(self):
        with self.assertRaises(ReplacementSuccessionError):
            self.request(successful_replacement_receipt_identities=("b" * 64,))

    def test_09_interrupted_attempt_is_retryable(self):
        result = self.request(attempt_state="INTERRUPTED_INCOMPLETE")
        self.assertFalse(result["success_consumed"])

    def test_10_new_replacement_requires_generic_parentage(self):
        derivative_identity = "c" * 64
        with self.assertRaises(ReplacementSuccessionError):
            self.request(
                attempt_state="SUCCESSFULLY_SEALED",
                admitted_derivative_identity=derivative_identity,
            )

        contract = self.authority["replacement_contract"]
        source_producer = {"identity": "LITS_SOURCE_VERIFIER", "code_blob": "d" * 40, "version": "1"}
        source_scope = {"source": "LITS_I"}
        source_currentness = {"authority": self.authority["authority_identity"]}
        source_ownership = {"source": "LITS_I", "candidate": "A"}
        source = mint_source_verification_receipt(
            source_id="LITS_I",
            canonical_source_sha256=contract["canonical_source_sha256"],
            observed_source_sha256=contract["canonical_source_sha256"],
            producer=source_producer,
            operation="VERIFY_CANONICAL_LITS_I_BYTES",
            reader_config=contract["reader_config"],
            scope_determinants=source_scope,
            currentness_determinants=source_currentness,
            ownership=source_ownership,
        )
        metadata = {"physical_root_id": derivative_identity, "build_config": contract["build_config"]}
        scope = {
            "source": "LITS_I",
            "derivative_scope": "PRESERVED_R5_PHYSICAL_SOURCE_CARRIER",
            "projection_identity": contract["fixed_identities"]["lits_projection_identity"],
            "runtime_catalog": contract["fixed_identities"]["runtime_catalog"],
        }
        currentness = {
            "owner_commit": contract["builder"]["owner_commit"],
            "candidate_owner_blob": contract["builder"]["consumer_adapter_blob"],
            "runtime_catalog": contract["fixed_identities"]["runtime_catalog"],
            "active_binding": contract["fixed_identities"]["active_binding"],
            "runtime_release": contract["fixed_identities"]["runtime_release"],
        }
        ownership = {"source": "LITS_I", "candidate": "A", "physical_root_id": derivative_identity}
        derivative = mint_derivative_parentage_receipt(
            source_receipt=source,
            derivative_class="LITS_A_PRESERVED_R5_CARRIER",
            derivative_identity=derivative_identity,
            derivative_hash=derivative_identity,
            derivative_metadata=metadata,
            producer=contract["builder"],
            derivation_operation=contract["derivation_operation"],
            reader_config=contract["reader_config"],
            scope_determinants=scope,
            currentness_determinants=currentness,
            ownership=ownership,
        )
        bundle = mint_parentage_bundle(source_receipt=source, derivative_receipt=derivative)
        expectations = {
            "expected_source_id": "LITS_I",
            "expected_source_sha256": contract["canonical_source_sha256"],
            "expected_derivative_class": "LITS_A_PRESERVED_R5_CARRIER",
            "expected_derivative_identity": derivative_identity,
            "expected_derivative_receipt_identity": derivative["receipt_identity"],
            "expected_derivative_hash": derivative_identity,
            "expected_derivative_metadata": metadata,
            "expected_producer": contract["builder"],
            "expected_derivation_operation": contract["derivation_operation"],
            "expected_reader_config": contract["reader_config"],
            "expected_scope_determinants": scope,
            "expected_currentness_determinants": currentness,
            "expected_ownership": ownership,
            "expected_source_receipt_identity": source["receipt_identity"],
            "expected_source_operation": "VERIFY_CANONICAL_LITS_I_BYTES",
            "expected_source_producer": source_producer,
            "expected_source_reader_config": contract["reader_config"],
            "expected_source_scope_determinants": source_scope,
            "expected_source_currentness_determinants": source_currentness,
            "expected_source_ownership": source_ownership,
        }
        result = self.request(
            attempt_state="SUCCESSFULLY_SEALED",
            admitted_derivative_identity=derivative_identity,
            parentage_bundle=bundle,
            parentage_expectations=expectations,
        )
        self.assertEqual(result["accounting"], "EXECUTED_NOW")

    def test_11_old_r5_numeric_credit_remains_zero(self):
        self.assertEqual(self.authority["accounting_treatment"]["old_r5_numeric_preserved_work_credit"], 0)

    def test_12_new_build_accounting_is_executed_now(self):
        self.assertEqual(self.authority["accounting_treatment"]["replacement_build"], "EXECUTED_NOW")

    def test_13_historical_t2_manifest_is_byte_identical(self):
        import hashlib
        self.assertEqual(hashlib.sha256(T2_PATH.read_bytes()).hexdigest(), EXPECTED_T2_SHA256)
        self.assertEqual(self.authority["predecessor_authority"]["git_blob"], EXPECTED_T2_GIT_BLOB)

    def test_14_candidate_a_semantics_runtime_workload_unchanged(self):
        fixed = self.authority["replacement_contract"]["fixed_identities"]
        self.assertEqual(fixed["lits_projection_identity"], "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872")
        self.assertEqual(fixed["expected_learned_product"], "47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d")
        self.assertEqual(fixed["semantic_replay_identity"], "301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5")
        self.assertEqual(fixed["runtime_catalog"], "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02")
        self.assertEqual((fixed["learned_candidates"], fixed["query_role_executions"]), (50, 77))


if __name__ == "__main__":
    unittest.main()
