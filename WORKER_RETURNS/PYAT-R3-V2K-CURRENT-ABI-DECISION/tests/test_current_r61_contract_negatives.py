from types import SimpleNamespace
import pytest
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord, WorkloadAdmissionError, admit, execute_issued_workload,
)

DEC = ExactRef("DECISION", "urn:test:decision", "1"*64)
QREF = ExactRef("QUERY", "urn:test:query", "2"*64)
PREF = ExactRef("PREDICATE", "urn:test:pred", "3"*64)
SREF = ExactRef("SOURCE", "urn:test:source", "4"*64)
SCIP = ExactRef("SCIENCE", "urn:test:science", "5"*64)
UREF = ExactRef("UNIVERSE", "urn:test:universe", "6"*64)

class Catalog:
    def __init__(self, pred=PREF): self.pred=pred
    def resolve_query_exact(self, ref): return SimpleNamespace(condition_predicate_ref=self.pred)
    def resolve_predicate_exact(self, ref): return object()

def workload(env=None, pred=PREF):
    w=SimpleNamespace()
    w.decision_ref=DEC; w.source_factory_ref=ExactRef("FACTORY","urn:test:factory","7"*64)
    w.descriptor=b"{}"; w.projection=SimpleNamespace(expected_source_sha256="a"*64, universes=(SimpleNamespace(ref=UREF),))
    w.catalog=Catalog(pred); w.requests=(SimpleNamespace(query_ref=QREF,predicate_ref=PREF),); w.discoveries=()
    w.original_u_root="u"; w.expected_frontier_root="f"
    w.envelope=lambda: (env if env is not None else {"x":1})
    return w

def record(w, **kw):
    env_hash=semantic_hash(w.envelope())
    vals=dict(decision_ref=DEC, source_permission_ref=SREF, scientific_permission_refs=(SCIP,), host="h", purpose="p", source_sha256="a"*64, envelope_sha256=env_hash, original_u_root="u", expected_frontier_root="f", expected_jobs=(("QUERY",QREF.key,PREF.key),), currentness="CURRENT_GRANTED", scope="TEST_ONLY_SOURCEFREE")
    vals.update(kw); return IssuedWorkloadRecord(**vals)

class Resolver:
    def __init__(self, rec): self.rec=rec
    def resolve_current(self, ref): return self.rec

def test_baseline_admits():
    w=workload(); r=record(w); assert admit(w, Resolver(r), host="h", purpose="p", allow_test_only=True)==r

def test_foreign_issuer_refused():
    w=workload(); r=record(w, decision_ref=ExactRef("DECISION","urn:test:foreign","8"*64))
    with pytest.raises(WorkloadAdmissionError, match="CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED"):
        admit(w, Resolver(r), host="h", purpose="p", allow_test_only=True)

def test_removed_held_row_refused():
    w=workload(); r=record(w, expected_jobs=(("QUERY",QREF.key,PREF.key),("DISCOVERY","urn:test:missing","")))
    with pytest.raises(WorkloadAdmissionError, match="EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH"):
        admit(w, Resolver(r), host="h", purpose="p", allow_test_only=True)

def test_mutated_identity_refused():
    w=workload(); r=record(w, envelope_sha256="b"*64)
    with pytest.raises(WorkloadAdmissionError, match="ENTIRE_EXECUTION_DESCRIPTOR_NOT_THE_ISSUED_ENVELOPE"):
        admit(w, Resolver(r), host="h", purpose="p", allow_test_only=True)

def test_wrong_role_refused():
    w=workload(pred=ExactRef("PREDICATE","urn:test:other","9"*64)); r=record(w)  # record env hash made with wrong predicate, expected job uses PREF
    # expected_jobs uses PREF while request uses PREF but catalog returns other
    with pytest.raises(WorkloadAdmissionError, match="QUERY_TARGET_CONDITION_DIRECTION_MISMATCH"):
        admit(w, Resolver(r), host="h", purpose="p", allow_test_only=True)

def test_replay_prior_receipts_refused():
    w=workload(); r=record(w)
    with pytest.raises(WorkloadAdmissionError, match="RESTORE_THROUGH_EXISTING_ISSUED_FACT_RECEIPT_CUSTODY_REQUIRED"):
        execute_issued_workload(w, Resolver(r), source_factory=lambda ref: SimpleNamespace(source_sha256="a"*64), host="h", purpose="p", allow_test_only=True, prior_receipts=("old",))

def test_wrong_source_factory_refused():
    w=workload(); r=record(w)
    with pytest.raises(WorkloadAdmissionError, match="SOURCE_FACTORY_RETURNED_WRONG_EDITION"):
        execute_issued_workload(w, Resolver(r), source_factory=lambda ref: SimpleNamespace(source_sha256="b"*64), host="h", purpose="p", allow_test_only=True)


def test_severed_current_resolver_refused():
    w = workload()
    class MissingResolver:
        def resolve_current(self, ref):
            raise RuntimeError("CURRENT_DECISION_DEPENDENCY_SEVERED")
    with pytest.raises(RuntimeError, match="CURRENT_DECISION_DEPENDENCY_SEVERED"):
        admit(w, MissingResolver(), host="h", purpose="p", allow_test_only=True)
