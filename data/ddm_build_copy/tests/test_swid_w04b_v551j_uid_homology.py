import unittest
import unicodedata

import pandas as pd

from data.ddm_build_copy.ddm_source_wave_identity import ProductionMembershipError
from data.ddm_build_copy.ddm_v551j_contract import (
    recompute_v551j_component_id,
    recompute_v551j_homology_key,
    recompute_v551j_packet_id,
    recompute_v551j_uid_native_packet_id,
    resolve_v551j_scope_identity,
)
from data.ddm_build_copy.ddm_v551j_packets import _uid_audit_fields, _uid_payload
from data.ddm_build_copy.ddm_v551j_semantic_diff import _diff_fields, _frame_to_rows


class W04BUidAndHomologyTests(unittest.TestCase):
    def test_alias_invariance(self):
        cases = [
            ("Arab Barometer", ["I", "W1", "Wave 1", "1"]),
            ("EVS", ["1981", "W1"]),
            ("EVS", ["1999", "W3"]),
            ("Afrobarometer", ["R1", "ROUND1", "Round 1"]),
            ("Latinobarómetro", ["1995", "1995"]),
        ]
        for source, waves in cases:
            identities = [resolve_v551j_scope_identity({"source": source, "wave": wave}) for wave in waves]
            self.assertEqual({(item["source_family_uid"], item["wave_uid"]) for item in identities}, {(identities[0]["source_family_uid"], identities[0]["wave_uid"])})
            ids = [recompute_v551j_uid_native_packet_id({"source": source, "wave": wave, "country_code": "US", "family_id": "f", "pattern_id": "p"}, identity=item) for wave, item in zip(waves, identities)]
            self.assertEqual(len(set(ids)), 1)

    def test_latinobarometro_nfc_nfd_and_unaccented_aliases(self):
        aliases = ["Latinobarómetro", unicodedata.normalize("NFD", "Latinobarómetro"), "Latinobarometro"]
        identities = [resolve_v551j_scope_identity({"source": alias, "wave": "1995"}) for alias in aliases]
        self.assertEqual({item["source_family_uid"] for item in identities}, {identities[0]["source_family_uid"]})
        self.assertEqual({item["wave_uid"] for item in identities}, {identities[0]["wave_uid"]})

    def test_asian_w6_is_recognized_but_excluded(self):
        with self.assertRaises(ProductionMembershipError):
            resolve_v551j_scope_identity({"source": "Asian Barometer", "wave": "W6"}, require_closed_35=True)

    def test_contradictory_redundancy_fails_closed(self):
        with self.assertRaises(ValueError):
            resolve_v551j_scope_identity({"source": "Afrobarometer", "source_family": "EVS", "wave": "R1"})
        with self.assertRaises(ValueError):
            resolve_v551j_scope_identity({"source": "Afrobarometer", "wave": "R1", "canonical_wave": "R5"})

    def test_legacy_ids_are_unchanged_and_uid_ids_are_additive(self):
        row = {"source": "Afrobarometer", "wave": "R1", "country_code": "LS", "family_id": "f", "pattern_id": "p", "item_order": 1, "question_id": "q", "var_code": "v", "response_value_normalized": "1"}
        identity = resolve_v551j_scope_identity(row)
        self.assertEqual(recompute_v551j_packet_id(row), recompute_v551j_packet_id({**row, "source_family_uid": identity["source_family_uid"], "wave_uid": identity["wave_uid"]}))
        self.assertTrue(recompute_v551j_uid_native_packet_id(row, identity=identity).startswith("v551j_uid_v1__packet__"))
        self.assertEqual(
            recompute_v551j_component_id(row),
            recompute_v551j_component_id({**row, "source_family_uid": identity["source_family_uid"], "wave_uid": identity["wave_uid"]}),
        )

    def test_production_packet_path_rejects_excluded_wave(self):
        with self.assertRaises(ProductionMembershipError):
            _uid_payload({"source": "Asian Barometer", "wave": "W6", "family_id": "f", "pattern_id": "p"})

    def test_active_audit_surfaces_copy_candidate_uid_identity(self):
        candidate = {"source_family_uid": "sf_ev", "wave_uid": "wave_ev_1981", "uid_key": "sf_ev|wave_ev_1981"}
        audit_identity = _uid_audit_fields(candidate)
        self.assertEqual(audit_identity, {
            "source_family_uid": "sf_ev",
            "wave_uid": "wave_ev_1981",
            "uid_key": "sf_ev|wave_ev_1981",
        })
        self.assertTrue(all(audit_identity.values()))

    def test_homology_is_wave_independent_but_family_specific(self):
        left = {"source": "EVS", "wave": "1981", "family_id": "f", "pattern_id": "p"}
        right = {"source": "EVS", "wave": "1999", "family_id": "f", "pattern_id": "p"}
        components = [{"item_order": 1, "v550j_item_question_id": "q-left", "v550j_item_var_code": "v-left", "v550j_item_response_value_normalized": "1", "v550j_item_role": "pressure", "v550j_item_semantic_response_role": "support", "v550j_relation_axis_id": "axis", "v550j_family_target_entity_id": "target"}]
        self.assertEqual(recompute_v551j_homology_key(left, components), recompute_v551j_homology_key(right, components))
        other = {"source": "WVS", "wave": "W1", "family_id": "f", "pattern_id": "p"}
        self.assertNotEqual(recompute_v551j_homology_key(left, components), recompute_v551j_homology_key(other, components))

    def test_homology_ignores_all_raw_wave_local_ids_but_distinguishes_semantics(self):
        left = {"source": "EVS", "wave": "1981", "family_id": "f", "pattern_id": "p1"}
        right = {"source": "EVS", "wave": "1999", "family_id": "f", "pattern_id": "p2"}
        left_components = [{"item_order": 1, "v550j_item_question_id": "q1", "v550j_item_var_code": "v1", "v550j_item_role": "pressure", "v550j_item_semantic_response_role": "support", "v550j_item_response_value_normalized": "1"}]
        right_components = [{"item_order": 1, "v550j_item_question_id": "q2", "v550j_item_var_code": "v2", "v550j_item_role": "pressure", "v550j_item_semantic_response_role": "support", "v550j_item_response_value_normalized": "1"}]
        self.assertEqual(recompute_v551j_homology_key(left, left_components), recompute_v551j_homology_key(right, right_components))
        changed = [{**right_components[0], "v550j_item_semantic_response_role": "oppose"}]
        self.assertNotEqual(recompute_v551j_homology_key(right, right_components), recompute_v551j_homology_key(right, changed))

    def test_missing_and_duplicate_homology_keys_fail_closed(self):
        with self.assertRaises(ValueError):
            _frame_to_rows(pd.DataFrame([{"packet_id": "p"}]))
        frame = pd.DataFrame([
            {"packet_id": "p1", "cross_wave_homology_key_v1": "h"},
            {"packet_id": "p2", "cross_wave_homology_key_v1": "h"},
        ])
        with self.assertRaises(ValueError):
            _frame_to_rows(frame)

    def test_wave_local_identity_does_not_create_semantic_diff(self):
        left = {"packet_id": "p1", "wave_uid": "w1", "wave": "1981", "canonical_wave": "1981", "packet_status": "CERTIFIED"}
        right = {"packet_id": "p2", "wave_uid": "w2", "wave": "1999", "canonical_wave": "1999", "packet_status": "CERTIFIED"}
        self.assertEqual(_diff_fields(left, right, ["packet_status"]), [])


if __name__ == "__main__":
    unittest.main()
