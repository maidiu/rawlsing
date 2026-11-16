from __future__ import annotations

import copy
import unittest

from rawlsing_next.fiabc_derivative_parentage import (
    ParentageError,
    canonical_digest,
    mint_derivative_parentage_receipt,
    mint_parentage_bundle,
    mint_source_verification_receipt,
    r5_root_metadata,
    verify_parentage_bundle,
    wvs_structural_metadata,
)


LITS_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
WVS_SHA = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
WRONG_SHA = "1" * 64

WVS_PRODUCER = {
    "identity": "WVS7_PROJECTION_STRUCTURAL_MATERIALIZER",
    "code_blob": "11b28416aac5a4899706150721f2f8ac8bb6ee43",
    "version": "EE_P2R6S_WVS7_PROJECTION_STRUCTURAL_INPUT@1.0.0",
}
WVS_READER = {
    "reader": "pyreadstat",
    "reader_version": "1.3.6",
    "apply_value_formats": False,
    "user_missing": True,
    "metadata_read": {"metadataonly": True},
    "country_read": {"usecols": ["B_COUNTRY"]},
    "compatibility_mode": None,
}
WVS_SCOPE = {
    "source": "WVS7",
    "derivative_scope": "PROJECTION_STRUCTURAL_PREIMAGE",
    "projection_identity": "838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d",
}
WVS_CURRENT = {
    "owner_commit": "0b96b8de9aac774566f872cf0630ebd4ddeb70e6",
    "materializer_blob": WVS_PRODUCER["code_blob"],
    "projection_identity": WVS_SCOPE["projection_identity"],
    "lock2": "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188",
}
WVS_OWNERSHIP = {
    "source": "WVS7",
    "candidate": "A",
    "root_lineage_identity": "2" * 64,
    "process_lineage": "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0",
}

LITS_PRODUCER = {
    "identity": "R5CompactLongShardedBuilder",
    "code_blob": "92e364b31eaf27be1bca2081eff65f6ffb779c3d",
    "version": "R5_LONG_SHARDED_TYPED_INCIDENCE_V1",
    "owner_commit": "0b96b8de9aac774566f872cf0630ebd4ddeb70e6",
    "consumer_adapter_blob": "d4915e7e6755ba1850756aebff72f982f73a332b",
}
LITS_READER = {
    "reader": "pyreadstat",
    "reader_version": "1.3.6",
    "user_missing": True,
    "apply_value_formats": False,
    "encoding": "latin1",
    "authority_status": "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY",
}
LITS_SCOPE = {
    "source": "LITS_I",
    "derivative_scope": "PRESERVED_R5_PHYSICAL_SOURCE_CARRIER",
    "projection_identity": "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872",
    "runtime_catalog": "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02",
}
LITS_CURRENT = {
    "owner_commit": "0b96b8de9aac774566f872cf0630ebd4ddeb70e6",
    "candidate_owner_blob": "d4915e7e6755ba1850756aebff72f982f73a332b",
    "runtime_catalog": LITS_SCOPE["runtime_catalog"],
    "active_binding": "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308",
    "runtime_release": "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
}


def wvs_doc(country_token: int = 840):
    unsigned = {
        "schema": "EE_P2R6S_WVS7_PROJECTION_STRUCTURAL_INPUT@1.0.0",
        "source_sha256": WVS_SHA,
        "rows": 97220,
        "variables": 613,
        "physical_variables": [
            {"ordinal": 1, "name": "B_COUNTRY", "missing_declarations": []}
        ],
        "b_country_values": [{"t": "int", "v": country_token}],
    }
    return {**unsigned, "structural_input_identity": canonical_digest(unsigned)}


def r5_root(root_id: str):
    return {
        "root_schema_version": "PRE553_R5_ROOT@1.0.0",
        "carrier_schema_version": "PRE553_R5_CANONICAL_CARRIER@1.0.0",
        "carrier_id": "R5_LONG_SHARDED_TYPED_INCIDENCE_V1",
        "typed_codec_version": "PRE553_R5_TYPED_VALUE_CODEC@1.0.0",
        "logical_stream_digest": "3" * 64,
        "canonical_row_count": 100,
        "member_inventory": {
            "path": "member_inventory.jsonl",
            "sha256": "4" * 64,
            "byte_length": 1234,
            "member_count": 2,
        },
        "build_config": {"shard_max_rows": 16384},
        "release_identity": {
            "release_id": "LITS-A-PRESERVED",
            "semantic_release_hash": "5" * 64,
            "source_artifact_ref": {
                "kind": "SOURCE_SHA256",
                "content_hash": LITS_SHA,
            },
            "source_release_manifest_hash": "6" * 64,
            "decoder_receipt": {"contract": "PRE553_FROZEN_PHYSICAL_DECODER"},
            "compiler_contract_digest": "7" * 64,
            "c11_authority_digest": "8" * 64,
        },
        "physical_root_id": root_id,
    }


class DerivativeParentageContractTests(unittest.TestCase):
    def _source(
        self,
        *,
        source_id,
        source_sha,
        producer,
        reader,
        scope,
        current,
        ownership,
        operation,
    ):
        return mint_source_verification_receipt(
            source_id=source_id,
            canonical_source_sha256=source_sha,
            observed_source_sha256=source_sha,
            producer=producer,
            operation=operation,
            reader_config=reader,
            scope_determinants=scope,
            currentness_determinants=current,
            ownership=ownership,
        )

    def _wvs_bundle(self, doc=None):
        doc = doc or wvs_doc()
        source = self._source(
            source_id="WVS7",
            source_sha=WVS_SHA,
            producer=WVS_PRODUCER,
            reader=WVS_READER,
            scope=WVS_SCOPE,
            current=WVS_CURRENT,
            ownership=WVS_OWNERSHIP,
            operation="VERIFY_CANONICAL_WVS7_RAW_SHA_AND_EXTRACT_STRUCTURAL_INPUT",
        )
        derivative = mint_derivative_parentage_receipt(
            source_receipt=source,
            derivative_class="WVS7_STRUCTURAL_PREIMAGE",
            derivative_identity=doc["structural_input_identity"],
            derivative_hash=doc["structural_input_identity"],
            derivative_metadata=wvs_structural_metadata(doc),
            producer=WVS_PRODUCER,
            derivation_operation="MATERIALIZE_WVS7_STRUCTURAL_PREIMAGE_FROM_CANONICAL_SAV",
            reader_config=WVS_READER,
            scope_determinants=WVS_SCOPE,
            currentness_determinants=WVS_CURRENT,
            ownership=WVS_OWNERSHIP,
        )
        return mint_parentage_bundle(source_receipt=source, derivative_receipt=derivative)

    def _verify_wvs(self, bundle, doc):
        return verify_parentage_bundle(
            bundle,
            expected_source_id="WVS7",
            expected_source_sha256=WVS_SHA,
            expected_source_receipt_identity=(
                bundle.get("source_receipt", {}).get("receipt_identity")
                if isinstance(bundle, dict)
                else None
            ),
            expected_source_operation="VERIFY_CANONICAL_WVS7_RAW_SHA_AND_EXTRACT_STRUCTURAL_INPUT",
            expected_derivative_class="WVS7_STRUCTURAL_PREIMAGE",
            expected_derivative_identity=doc["structural_input_identity"],
            expected_derivative_receipt_identity=(
                bundle.get("derivative_receipt", {}).get("receipt_identity")
                if isinstance(bundle, dict)
                else None
            ),
            expected_derivative_hash=doc["structural_input_identity"],
            expected_derivative_metadata=wvs_structural_metadata(doc),
            expected_producer=WVS_PRODUCER,
            expected_derivation_operation="MATERIALIZE_WVS7_STRUCTURAL_PREIMAGE_FROM_CANONICAL_SAV",
            expected_reader_config=WVS_READER,
            expected_scope_determinants=WVS_SCOPE,
            expected_currentness_determinants=WVS_CURRENT,
            expected_ownership=WVS_OWNERSHIP,
            expected_source_producer=WVS_PRODUCER,
            expected_source_reader_config=WVS_READER,
            expected_source_scope_determinants=WVS_SCOPE,
            expected_source_currentness_determinants=WVS_CURRENT,
            expected_source_ownership=WVS_OWNERSHIP,
        )

    def test_positive_wvs_parentage_closes(self):
        doc = wvs_doc()
        bundle = self._wvs_bundle(doc)
        self.assertIs(self._verify_wvs(bundle, doc), bundle)

    def test_forged_derivative_with_correct_asserted_source_sha_is_rejected(self):
        forged = {
            "source_sha256": WVS_SHA,
            "rows": 97220,
            "variables": 613,
            "structural_input_identity": "9" * 64,
        }
        with self.assertRaises(ParentageError):
            self._verify_wvs(forged, wvs_doc())

    def test_recomputed_structural_preimage_self_hash_does_not_prove_ancestry(self):
        original = wvs_doc(840)
        bundle = self._wvs_bundle(original)
        altered = wvs_doc(124)
        self.assertNotEqual(
            original["structural_input_identity"],
            altered["structural_input_identity"],
        )
        with self.assertRaises(ParentageError):
            self._verify_wvs(bundle, altered)

    def test_wrong_reader_config_is_rejected(self):
        doc = wvs_doc()
        bundle = self._wvs_bundle(doc)
        bad_reader = dict(WVS_READER)
        bad_reader["reader_version"] = "9.9.9"
        with self.assertRaises(ParentageError):
            verify_parentage_bundle(
                bundle,
                expected_source_id="WVS7",
                expected_source_sha256=WVS_SHA,
                expected_derivative_class="WVS7_STRUCTURAL_PREIMAGE",
                expected_derivative_identity=doc["structural_input_identity"],
                expected_derivative_hash=doc["structural_input_identity"],
                expected_derivative_metadata=wvs_structural_metadata(doc),
                expected_producer=WVS_PRODUCER,
                expected_derivation_operation="MATERIALIZE_WVS7_STRUCTURAL_PREIMAGE_FROM_CANONICAL_SAV",
                expected_reader_config=bad_reader,
                expected_scope_determinants=WVS_SCOPE,
                expected_currentness_determinants=WVS_CURRENT,
                expected_ownership=WVS_OWNERSHIP,
            )

    def test_correct_row_count_but_wrong_ancestor_is_rejected(self):
        doc = wvs_doc()
        wrong_source = self._source(
            source_id="WVS7",
            source_sha=WRONG_SHA,
            producer=WVS_PRODUCER,
            reader=WVS_READER,
            scope=WVS_SCOPE,
            current=WVS_CURRENT,
            ownership=WVS_OWNERSHIP,
            operation="VERIFY_CANONICAL_WVS7_RAW_SHA_AND_EXTRACT_STRUCTURAL_INPUT",
        )
        derivative = mint_derivative_parentage_receipt(
            source_receipt=wrong_source,
            derivative_class="WVS7_STRUCTURAL_PREIMAGE",
            derivative_identity=doc["structural_input_identity"],
            derivative_hash=doc["structural_input_identity"],
            derivative_metadata=wvs_structural_metadata(doc),
            producer=WVS_PRODUCER,
            derivation_operation="MATERIALIZE_WVS7_STRUCTURAL_PREIMAGE_FROM_CANONICAL_SAV",
            reader_config=WVS_READER,
            scope_determinants=WVS_SCOPE,
            currentness_determinants=WVS_CURRENT,
            ownership=WVS_OWNERSHIP,
        )
        bundle = mint_parentage_bundle(
            source_receipt=wrong_source,
            derivative_receipt=derivative,
        )
        with self.assertRaises(ParentageError):
            self._verify_wvs(bundle, doc)

    def test_compatibility_decoded_persisted_copy_without_receipt_is_rejected(self):
        with self.assertRaises(ParentageError):
            verify_parentage_bundle(
                None,
                expected_source_id="LITS_I",
                expected_source_sha256=LITS_SHA,
                expected_derivative_class="COMPATIBILITY_DECODED_COPY",
                expected_derivative_identity="a" * 64,
                expected_derivative_hash="a" * 64,
                expected_derivative_metadata={"rows": 100},
                expected_producer=LITS_PRODUCER,
                expected_derivation_operation="PERSIST_COMPATIBILITY_DECODED_COPY",
                expected_reader_config=LITS_READER,
                expected_scope_determinants=LITS_SCOPE,
                expected_currentness_determinants=LITS_CURRENT,
                expected_ownership={"source": "LITS_I", "candidate": "A"},
            )

    def test_positive_lits_r5_parentage_binds_root_manifest_and_currentness(self):
        root = r5_root("a" * 64)
        ownership = {
            "source": "LITS_I",
            "candidate": "A",
            "physical_root_id": root["physical_root_id"],
        }
        source = self._source(
            source_id="LITS_I",
            source_sha=LITS_SHA,
            producer={
                "identity": "PRE553_FROZEN_PHYSICAL_DECODER",
                "code_blob": "decoder-blob",
                "version": "1.0.0",
            },
            reader=LITS_READER,
            scope=LITS_SCOPE,
            current=LITS_CURRENT,
            ownership={"source": "LITS_I", "candidate": "A"},
            operation="VERIFY_CANONICAL_LITS_RAW_SHA_AND_DECODE",
        )
        derivative = mint_derivative_parentage_receipt(
            source_receipt=source,
            derivative_class="LITS_A_PRESERVED_R5_CARRIER",
            derivative_identity=root["physical_root_id"],
            derivative_hash=root["physical_root_id"],
            derivative_metadata=r5_root_metadata(root),
            producer=LITS_PRODUCER,
            derivation_operation="BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE",
            reader_config=LITS_READER,
            scope_determinants=LITS_SCOPE,
            currentness_determinants=LITS_CURRENT,
            ownership=ownership,
        )
        bundle = mint_parentage_bundle(source_receipt=source, derivative_receipt=derivative)
        verified = verify_parentage_bundle(
            bundle,
            expected_source_id="LITS_I",
            expected_source_sha256=LITS_SHA,
            expected_derivative_class="LITS_A_PRESERVED_R5_CARRIER",
            expected_derivative_identity=root["physical_root_id"],
            expected_derivative_receipt_identity=derivative["receipt_identity"],
            expected_derivative_hash=root["physical_root_id"],
            expected_derivative_metadata=r5_root_metadata(root),
            expected_producer=LITS_PRODUCER,
            expected_derivation_operation="BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE",
            expected_reader_config=LITS_READER,
            expected_scope_determinants=LITS_SCOPE,
            expected_currentness_determinants=LITS_CURRENT,
            expected_ownership=ownership,
            expected_source_reader_config=LITS_READER,
        )
        self.assertIs(verified, bundle)

    def test_copied_old_r5_root_is_rejected_even_with_same_source_sha(self):
        old_root = r5_root("b" * 64)
        current_root = r5_root("c" * 64)
        old_ownership = {
            "source": "LITS_I",
            "candidate": "A",
            "physical_root_id": old_root["physical_root_id"],
        }
        source = self._source(
            source_id="LITS_I",
            source_sha=LITS_SHA,
            producer={
                "identity": "PRE553_FROZEN_PHYSICAL_DECODER",
                "code_blob": "decoder-blob",
                "version": "1.0.0",
            },
            reader=LITS_READER,
            scope=LITS_SCOPE,
            current=LITS_CURRENT,
            ownership={"source": "LITS_I", "candidate": "A"},
            operation="VERIFY_CANONICAL_LITS_RAW_SHA_AND_DECODE",
        )
        derivative = mint_derivative_parentage_receipt(
            source_receipt=source,
            derivative_class="LITS_A_PRESERVED_R5_CARRIER",
            derivative_identity=old_root["physical_root_id"],
            derivative_hash=old_root["physical_root_id"],
            derivative_metadata=r5_root_metadata(old_root),
            producer=LITS_PRODUCER,
            derivation_operation="BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE",
            reader_config=LITS_READER,
            scope_determinants=LITS_SCOPE,
            currentness_determinants=LITS_CURRENT,
            ownership=old_ownership,
        )
        bundle = mint_parentage_bundle(source_receipt=source, derivative_receipt=derivative)
        with self.assertRaises(ParentageError):
            verify_parentage_bundle(
                bundle,
                expected_source_id="LITS_I",
                expected_source_sha256=LITS_SHA,
                expected_derivative_class="LITS_A_PRESERVED_R5_CARRIER",
                expected_derivative_identity=current_root["physical_root_id"],
                expected_derivative_receipt_identity=derivative["receipt_identity"],
                expected_derivative_hash=current_root["physical_root_id"],
                expected_derivative_metadata=r5_root_metadata(current_root),
                expected_producer=LITS_PRODUCER,
                expected_derivation_operation="BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE",
                expected_reader_config=LITS_READER,
                expected_scope_determinants=LITS_SCOPE,
                expected_currentness_determinants=LITS_CURRENT,
                expected_ownership={
                    "source": "LITS_I",
                    "candidate": "A",
                    "physical_root_id": current_root["physical_root_id"],
                },
            )

    def test_receipt_currentness_drift_is_rejected(self):
        doc = wvs_doc()
        bundle = self._wvs_bundle(doc)
        stale = copy.deepcopy(WVS_CURRENT)
        stale["owner_commit"] = "f" * 40
        with self.assertRaises(ParentageError):
            verify_parentage_bundle(
                bundle,
                expected_source_id="WVS7",
                expected_source_sha256=WVS_SHA,
                expected_derivative_class="WVS7_STRUCTURAL_PREIMAGE",
                expected_derivative_identity=doc["structural_input_identity"],
                expected_derivative_hash=doc["structural_input_identity"],
                expected_derivative_metadata=wvs_structural_metadata(doc),
                expected_producer=WVS_PRODUCER,
                expected_derivation_operation="MATERIALIZE_WVS7_STRUCTURAL_PREIMAGE_FROM_CANONICAL_SAV",
                expected_reader_config=WVS_READER,
                expected_scope_determinants=WVS_SCOPE,
                expected_currentness_determinants=stale,
                expected_ownership=WVS_OWNERSHIP,
            )


if __name__ == "__main__":
    unittest.main()
