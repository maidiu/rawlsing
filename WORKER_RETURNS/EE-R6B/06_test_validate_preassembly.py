from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ee_r6b_validator", HERE / "05_validate_preassembly.py")
v = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(v)

FILES = [
    "01_FINAL_PREASSEMBLY_MANIFEST.json",
    "02_READY_14_EXECUTION_ORACLE_PROFILES.json",
    "03_EE_R6A_FOUR_CELL_SPLICE_CONTRACT.json",
    "04_EXECUTION_MEASUREMENT_ORDER_RESET_LAW.json",
]

def read_json(name):
    return json.loads((HERE/name).read_text())

def write_fixture(root: Path, docs):
    for name, doc in docs.items():
        (root/name).write_text(json.dumps(doc, sort_keys=True))

class TestEER6BPreassembly(unittest.TestCase):
    def setUp(self):
        self.docs = {name:read_json(name) for name in FILES}

    def mutate_and_fail(self, fn):
        docs = copy.deepcopy(self.docs)
        fn(docs)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_fixture(root, docs)
            with self.assertRaises(v.ValidationError):
                v.validate_preassembly(root)

    def test_valid_preassembly(self):
        got = v.validate_preassembly(HERE)
        self.assertEqual(got["ready_cells"],14)
        self.assertEqual(got["pending_splice_slots"],4)
        self.assertFalse(got["abc_run"])
        self.assertFalse(got["ranking"])

    def test_owner_substitution_rejected(self):
        self.mutate_and_fail(lambda d: d[FILES[0]]["candidates"]["A"].__setitem__("blob","0"*40))

    def test_candidate_c_extra_accelerator_rejected(self):
        self.mutate_and_fail(lambda d: d[FILES[0]]["candidates"]["C"]["accelerators"].append("CACC3_UNAUTHORIZED"))

    def test_missing_ready_cell_rejected(self):
        self.mutate_and_fail(lambda d: d[FILES[1]]["profiles"].pop())

    def test_source_substitution_rejected(self):
        self.mutate_and_fail(lambda d: d[FILES[0]]["universes"]["WVS7"].__setitem__("sha256","0"*64))

    def test_splice_qid_substitution_rejected(self):
        self.mutate_and_fail(lambda d: d[FILES[2]]["slots"][0]["frozen_qids"].__setitem__(0,"replacement.qid"))

    def test_metric_law_mutation_rejected(self):
        self.mutate_and_fail(lambda d: d[FILES[3]]["measurement"]["telemetry_fields"].pop())

    def test_candidate_order_mutation_rejected(self):
        self.mutate_and_fail(lambda d: d[FILES[3]].__setitem__("candidate_execution_order",["C","B","A"]))

    def test_candidate_specific_omission_surface_rejected(self):
        def mutate(d):
            d[FILES[1]]["profiles"][0]["candidate_exclusions"]=["C"]
        self.mutate_and_fail(mutate)

    def test_test_only_structurally_complete_r6a_splice_shape(self):
        # This fixture exercises only the deterministic splice checker. It does not
        # assert survey authority and is not a substitute for an HQ-accepted EE-R6A return.
        contract = self.docs[FILES[2]]
        slots=[]
        for c in contract["slots"]:
            slot = {
                "slot_id":c["slot_id"],
                "universe_id":c["universe_id"],
                "operation_id":c["operation_id"],
                "source_sha256":c["source_sha256"],
                "frozen_qids":c["frozen_qids"],
                "frozen_pair_newline_stream_sha256":c["frozen_pair_newline_stream_sha256"],
                "source_coordinate_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "routing_applicability_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "risk_set_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "denominator_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "response_semantic_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "reference_oracle":{"kind":"TEST_ONLY_STRUCTURAL_FIXTURE","laws":c["required_oracle_laws"]},
                "oracle_authority_refs":["TEST_ONLY_DOES_NOT_MINT_AUTHORITY"],
                "oracle_materialization":{
                    "law":v.MAT,
                    "candidate_outputs_may_not_define_or_modify_oracle":True,
                },
            }
            slot["profile_content_sha256"]=hashlib.sha256(
                json.dumps(slot,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
            ).hexdigest()
            slots.append(slot)
        payload={"schema":contract["r6a_payload_schema"],"slots":slots}
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"splice.json"
            p.write_text(json.dumps(payload))
            got=v.validate_r6a_splice_payload(p,HERE)
            self.assertEqual(got["spliced_ready_cells"],18)
            self.assertEqual(got["pending_splice_slots"],0)

    def test_splice_content_hash_mutation_rejected(self):
        contract = self.docs[FILES[2]]
        slots=[]
        for c in contract["slots"]:
            slot = {
                "slot_id":c["slot_id"],
                "universe_id":c["universe_id"],
                "operation_id":c["operation_id"],
                "source_sha256":c["source_sha256"],
                "frozen_qids":c["frozen_qids"],
                "frozen_pair_newline_stream_sha256":c["frozen_pair_newline_stream_sha256"],
                "source_coordinate_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "routing_applicability_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "risk_set_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "denominator_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "response_semantic_binding":{"test_only":"STRUCTURAL_FIXTURE"},
                "reference_oracle":{"kind":"TEST_ONLY_STRUCTURAL_FIXTURE","laws":c["required_oracle_laws"]},
                "oracle_authority_refs":["TEST_ONLY_DOES_NOT_MINT_AUTHORITY"],
                "oracle_materialization":{
                    "law":v.MAT,
                    "candidate_outputs_may_not_define_or_modify_oracle":True,
                },
                "profile_content_sha256":"0"*64,
            }
            slots.append(slot)
        payload={"schema":contract["r6a_payload_schema"],"slots":slots}
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"splice.json"
            p.write_text(json.dumps(payload))
            with self.assertRaises(v.ValidationError):
                v.validate_r6a_splice_payload(p,HERE)

if __name__=="__main__":
    unittest.main()
