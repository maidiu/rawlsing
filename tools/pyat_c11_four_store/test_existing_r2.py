"""The original R2 custody file is bound to user-pinned host/purpose/root.

Sourcefree fake R2 decision: verifies guard rejects drift; it does NOT
constitute an actual recorded source authorization.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from .existing_r2 import R2Custody
from .stores import StoreFailure


class ExistingR2Tests(unittest.TestCase):
    def fixture(self, root):
        src="1"*64
        release=str(root/"custody"/"releases"/"exact-release")
        value={
            "host":"MainMac", "purpose":"P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2",
            "schema":"SOURCEFREE_TEST_ONLY", "waves":{
                "SRC04":{
                    "custody_estate_path":release,
                    "source_sha256":src, "manifest_sha256":"2"*64,
                    "decision_ref":"user-decided-sourcefree-fixture-not-real",
                    "saved_i02":{
                        "schema":"ANVIL_STREAM_C11_ESTATE@1",
                        "logical":"3"*64, "physical":"4"*64,
                        "source":"SOURCE_ARTIFACT|fake|"+src,
                        "release":"C11_STREAM_SOURCEFREE_RELEASE|fake|"+"5"*64,
                        "replay":"6"*64,
                        "universe":"EmpiricalUniverse@1.0.0|fake|"+"7"*64,
                    },
                },
            },
        }
        target=root/"r2_decision.json"
        target.write_text(json.dumps(value))
        return target,value

    def test_exact_user_scoped_r2_decision_and_revocation(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            path,value=self.fixture(root)
            custody=R2Custody(
                path,"SRC04",required_host="MainMac",
                required_purpose="P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2",
            )
            self.assertTrue(custody.check_current(custody.pins))
            value["waves"]["SRC04"]["decision_ref"]="changed"
            path.write_text(json.dumps(value))
            self.assertFalse(custody.check_current(custody.pins))

    def test_other_decision_field_edit_also_revokes_snapshot(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            path,value=self.fixture(root)
            custody=R2Custody(
                path,"SRC04",required_host="MainMac",
                required_purpose="P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2",
            )
            self.assertTrue(custody.check_current(custody.pins))
            # The old guard only compared a handful of identity fields,
            # incorrectly allowing an out-of-band permission-state change.
            value["waves"]["SRC04"]["status"]="REVOKED"
            path.write_text(json.dumps(value))
            self.assertFalse(custody.check_current(custody.pins))

    def test_cached_currentness_rechecks_same_size_rewrite_with_restored_mtime(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            path,value=self.fixture(root)
            custody=R2Custody(
                path,"SRC04",required_host="MainMac",
                required_purpose="P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2",
            )
            self.assertTrue(custody.check_current(custody.pins))
            before=path.stat()
            old=value["waves"]["SRC04"]["decision_ref"]
            value["waves"]["SRC04"]["decision_ref"]="x"*len(old)
            encoded=json.dumps(value)
            self.assertEqual(len(encoded),before.st_size)
            path.write_text(encoded)
            os.utime(path,ns=(before.st_atime_ns,before.st_mtime_ns))
            self.assertFalse(custody.check_current(custody.pins))

    def test_wrong_host_refused(self):
        with tempfile.TemporaryDirectory() as t:
            path,_=self.fixture(Path(t))
            with self.assertRaisesRegex(StoreFailure,"host/purpose"):
                R2Custody(path,"SRC04",required_host="NotMainMac",
                          required_purpose="P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2")

    def test_wrong_source_refused(self):
        with tempfile.TemporaryDirectory() as t:
            path,_=self.fixture(Path(t))
            with self.assertRaisesRegex(StoreFailure,"absent"):
                R2Custody(path,"SRC16",required_host="MainMac",
                          required_purpose="P0_TWO_SAVED_WAVES_ANALYTICAL_DOWNSTREAM_R2")


if __name__=="__main__":
    unittest.main()
