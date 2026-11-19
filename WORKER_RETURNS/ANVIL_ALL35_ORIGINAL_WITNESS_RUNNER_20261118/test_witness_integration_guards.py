#!/usr/bin/env python3
"""Offline fail-closed guards: no original data, no source path opened."""
import sys, tempfile, types, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import witness_caller as w

class Resolver:
    def __init__(self,req,state="CURRENT_GRANTED",revoked=False,locator=None):
        fields=("source_id","source_sha256","source_format","custody_locator_binding",
                "host","purpose","consumer_use","read_operation",
                "physical_read_extent","metadata_freeze_refs","semantic_use_scope")
        data={field:getattr(req,field) for field in fields}
        if locator is not None: data["custody_locator_binding"]=locator
        self.decision=types.SimpleNamespace(**data,currentness=state,
                      revocation_ref="rev" if revoked else None,decision_ref=req.decision_ref)
    def resolve_current(self,request): return self.decision

class GuardTests(unittest.TestCase):
    def test_direct_producer_requires_launch_flag(self):
        with self.assertRaises(w.CallerRefusal) as ctx:
            w.producer(types.SimpleNamespace(authorized_source_launch=False))
        self.assertEqual(ctx.exception.code,"EXPLICIT_SOURCE_LAUNCH_AUTHORIZATION_REQUIRED")

    def test_resume_root_reused_and_not_swapped(self):
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp)/"runs"
            root=work/"SRC04_WITNESS_test"
            private=root/"private"
            private.mkdir(parents=True,mode=0o700)
            private.chmod(0o700)
            cp=private/"prepared-sections.checkpoint.json"
            cp.write_text("{}")
            self.assertEqual(w._resume_existing_root(cp,work),root)
            with self.assertRaises(w.CallerRefusal):
                w._resume_existing_root(cp,Path(tmp)/"other")
            other=private/"alien.json"
            cp.rename(other)
            with self.assertRaises(w.CallerRefusal):
                w._resume_existing_root(other,work)

    def test_reader_reference_cannot_be_false_positive(self):
        ok={"RespondentEvent":w.ACCEPTED["RespondentEvent"],
            "EmpiricalCoordinateFact":w.ACCEPTED["EmpiricalCoordinateFact"]}
        w._enforce_src04_reference(ok,w.ACCEPTED["release_hash"])
        with self.assertRaises(w.CallerRefusal):
            w._enforce_src04_reference({**ok,"RespondentEvent":0},w.ACCEPTED["release_hash"])
        with self.assertRaises(w.CallerRefusal):
            w._enforce_src04_reference(ok,"0"*64)

    def test_current_revocation_and_locator_scope(self):
        req=types.SimpleNamespace(decision_ref="decision",source_id="SRC04",
          source_sha256="a"*64,source_format="SAV",custody_locator_binding="EXACT",
          host="USER_LOCAL_MAC",purpose="FULL_SRC04_ORIGINAL_C11_CONSTRUCTION",
          consumer_use="EXISTING_PRE553_SOURCE_BACKED_C11",
          read_operation="SOURCE_RESPONSE_DECODE",physical_read_extent="EXACT_FILE",
          metadata_freeze_refs=(),semantic_use_scope=("SRC04",))
        held=object()
        self.assertTrue(w._reader_current(Resolver(req),req,req.decision_ref,held,held))
        self.assertFalse(w._reader_current(Resolver(req,revoked=True),req,req.decision_ref,held,held))
        self.assertFalse(w._reader_current(Resolver(req,locator="OTHER"),req,req.decision_ref,held,held))
        self.assertFalse(w._reader_current(Resolver(req),req,req.decision_ref,object(),held))

if __name__=="__main__":
    unittest.main()
