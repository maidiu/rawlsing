"""Cheap sourcefree guards for option parsing and repeat-result enforcement.

Actual original-source S3 performance must be executed by its authorized user
on the real host. Do not replace it with these mocks or call mocks native evidence.
"""
from __future__ import annotations

import argparse
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from . import prepared_s3_runner as prep
from . import sourcefree_s3_scale as sf
from .stores import StoreFailure, canonical, digest

class S3RunnerSourcefreeTests(unittest.TestCase):
    def test_counts_reject_duplicate_zero_negative_over_cap(self):
        self.assertEqual(prep.parse_counts("1,10,100"),(1,10,100))
        for raw in ("", "0", "-1", "101", "1,1", "10,foo"):
            with self.subTest(raw=raw), self.assertRaises(argparse.ArgumentTypeError):
                prep.parse_counts(raw)

    def test_scale_cases_bounded_and_no_fake_scientific_claim(self):
        self.assertEqual(sf.parse_cases("8:1,8:2"),((8,1),(8,2)))
        self.assertIn("NOT_NATIVE_I03",sf.GRADE)
        for raw in ("0:1", "8:0", "8:101", "8:2,8:2", "8foo"):
            with self.subTest(raw=raw),self.assertRaises(argparse.ArgumentTypeError):
                sf.parse_cases(raw)
        self.assertEqual(sf.make_row("RespondentEvent",sf.ref("RespondentEvent",2),
            respondent=sf.ref("RespondentIdentity",1))["typed_state"],"SOURCEFREE_SCALED_STATE")

    def test_native_repeats_use_one_prepared_session_and_compare_exact_output(self):
        op={"query":SimpleNamespace(ref=SimpleNamespace(key="ISSUED_Q103")),
            "name":"ISSUED_Q103","recorded_plan":object()}
        original={"facts":[{"state":"SUPPORTED"}],"s04":{"status":"PRODUCED_TESTONLY_S04"}}
        prior={"query_report":{"native":[{"output":original}]}}
        verified=SimpleNamespace(_live=lambda: True)
        src=SimpleNamespace(verified=verified)
        fresh=object(); prepared=object()
        store=object(); emits=[]; calls=[]
        def execute(*args,prepared_session=None):
            calls.append(prepared_session)
            return original
        with patch.object(prep.runner,"_native_operations",return_value=([op],
                   "ORIGINAL_ISSUED_OPERATION_OBJECTS_PROVIDED_BY_EXTERNAL_OWNER")),\
             patch.object(prep,"open_native_session",return_value=prepared),\
             patch.object(prep,"execute_issued",side_effect=execute):
            outcome=prep._native_repeat(store,src,{},__import__("pathlib").Path("/tmp/bundle.json"),
                      prior,(1,3),2,lambda **kw:emits.append(kw),
                      SimpleNamespace(check=lambda:None))
        self.assertEqual(len(calls),6)
        self.assertEqual(calls[:2],[None,None])
        self.assertEqual(calls[2:],[prepared]*4)
        self.assertTrue(outcome["same_original_operation_repeated"])
        self.assertEqual(outcome["distinct_issued_operations"],1)
        self.assertEqual(outcome["exact_original_output_sha256"],digest(canonical(original).encode()))

    def test_prepared_hook_rejects_foreign_session(self):
        # Exercise the opt-in refusal branch in the real native module after
        # installation. This cannot authorize an original-science operation.
        from .native import execute_issued
        op={"query":SimpleNamespace(ref=SimpleNamespace(key="SOURCEFREE_ONLY")),
            "predicate":object(),"authority_registry":object()}
        with self.assertRaisesRegex(StoreFailure,"prepared native session"):
            execute_issued(SimpleNamespace(name="S3",db=object()),object(),op,
                           prepared_session=object())

    def test_native_repeat_detects_changed_answer(self):
        op={"query":SimpleNamespace(ref=SimpleNamespace(key="ISSUED_Q103")),
            "name":"ISSUED_Q103"}
        prior={"query_report":{"native":[{"output":{"facts":[{"state":"SUPPORTED"}]}}]}}
        with patch.object(prep.runner,"_native_operations",return_value=([op],
                   "ORIGINAL_ISSUED_OPERATION_OBJECTS_PROVIDED_BY_EXTERNAL_OWNER")),\
             patch.object(prep,"execute_issued",return_value={"facts":[{"state":"REFUSED"}]}):
            with self.assertRaisesRegex(StoreFailure,"differs from original"):
                prep._native_repeat(object(),SimpleNamespace(verified=SimpleNamespace(_live=lambda:None)),
                     {},__import__("pathlib").Path("/tmp/fixture"),prior,(1,),1,
                     lambda **kw:None,SimpleNamespace(check=lambda:None))

if __name__=="__main__":unittest.main()
