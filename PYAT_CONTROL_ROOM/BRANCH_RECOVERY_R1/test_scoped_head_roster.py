#!/usr/bin/env python3
"""Exact post-integration head roster invariants. HEAD-ONLY, no science or code admission."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
CUT=ROOT/"SCOPED_ROSTER"
NAMES=("S1","S2","S3","S4","S5")
N=(175,175,174,161,160)
STRICT="2026-10-09T22:31:19Z"


def blob_sha(contents):
    return hashlib.sha1(b"blob "+str(len(contents)).encode()+b"\0"+contents).hexdigest()


class ScopedHeadRosterTests(unittest.TestCase):
    def test_roster_has_exact_scope_not_historic_2831(self):
        manifest=json.loads((CUT/"11_00_SCOPED_HEAD_ROSTER_MANIFEST.json").read_text())
        self.assertEqual(manifest["snapshot"]["post_dense_relevant"],845)
        self.assertEqual(manifest["scope_proof"]["distinct_tip_sha"],838)
        self.assertEqual(manifest["scope_proof"]["unknown_tip_name_count"],30)
        self.assertEqual(manifest["snapshot"]["strict_core_relevant"],524)
        self.assertEqual(manifest["snapshot"]["transitional_relevant"],321)
        self.assertEqual(len(manifest["rosters"]),5)

    def test_every_named_head_appears_once_and_globally_deduplicates(self):
        manifest=json.loads((CUT/"11_00_SCOPED_HEAD_ROSTER_MANIFEST.json").read_text())
        names,heads,rows=set(),set(),[]
        for i,shard in enumerate(manifest["rosters"]):
            path=ROOT.parents[1]/shard["path"]
            self.assertTrue(path.is_file(),shard["path"])
            contents=path.read_bytes()
            self.assertEqual(blob_sha(contents),shard["git_blob_sha"])
            data=json.loads(contents)
            self.assertEqual(data["worker"],NAMES[i])
            self.assertEqual(data["name_count"],N[i])
            self.assertEqual(data["status"],"HEAD_ONLY_NOT_CONTENT_INDEXED")
            for row in data["branch_heads"]:
                self.assertNotIn(row["branch"],names)
                names.add(row["branch"])
                heads.add(row["tip_sha"])
                rows.append(row)
                self.assertEqual(row["index_state"],"NEEDS_CONTENT_AND_RETURN_PROOF_INDEX")
        self.assertEqual(len(names),845)
        self.assertEqual(len(heads),838)
        self.assertEqual(sum(row["kind"]=="UNKNOWN_REQUIRES_CONTENT_TRIAGE" for row in rows),30)
        def strict(row): return row["committer_time_utc"]>=STRICT.replace("Z","+00:00")
        self.assertEqual(sum(strict(x) for x in rows),524)
        self.assertEqual(sum(not strict(x) for x in rows),321)
        self.assertTrue(all((i<3)==(shard["tier"]=="STRICT_CORE_OCT09_PLUS") for i,shard in enumerate(manifest["rosters"])))

    def test_no_scoped_content_claim_is_falsely_accepted(self):
        manifest=json.loads((CUT/"11_00_SCOPED_HEAD_ROSTER_MANIFEST.json").read_text())
        self.assertEqual(manifest["status"],"COMPLETE_TEMPORAL_HEAD_ROSTER__CONTENT_INDEX_NOT_YET_EXECUTED")
        self.assertEqual(manifest["index_gate"],"HOLD_RECOVERY_UNTIL_CONTENT_INDEX_AND_INDEPENDENT_ACCEPTANCE")


if __name__=="__main__":
    unittest.main()
