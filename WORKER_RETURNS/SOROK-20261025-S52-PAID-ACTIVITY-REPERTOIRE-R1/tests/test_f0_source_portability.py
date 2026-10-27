"""F0 adversarial checks for portable S52 source binding and cold open."""
from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

import pytest

from s52.bootstrap import REPO, install, roots

install()

from s51.source_binding import SourceBindingError, verify_expected  # noqa: E402
from s52.session import CANDIDATE_KIND, S52ColdOpenRefusal, S52Session, candidate_digest  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(state):
 c=case_for(True)
 return S52Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),
  language_context={"milieu_id":"workshop"})


def test_source_roots_are_resolved_without_embedded_user_paths():
 r=roots()
 assert Path(r["g18_source"]).is_dir()
 assert r["g18_source_verified"] is True
 assert r["dependency_verified"] is True
 assert r["source_verified"] is True
 assert r["source_count"] == 31
 for rel in (
  "WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py",
  "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/bootstrap.py",
  "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py",
 ):
  assert "/Users/" not in Path(REPO, rel).read_text()


def test_tampered_dependency_is_rejected_by_hash():
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp); (root/"lab_sgi1").mkdir(); (root/"lab_sgi1"/"joint.py").write_text("tampered")
  with pytest.raises(SourceBindingError) as exc:
   verify_expected(root, {"lab_sgi1/joint.py": "0"*64})
  assert exc.value.code=="SOURCE_HASH_MISMATCH"


def test_substituted_dependency_root_is_rejected():
 from s52.source_registry import verify_dependencies
 r=dict(roots()); r["g18_source"]=str(Path(tempfile.mkdtemp()))
 with pytest.raises(SourceBindingError):
  verify_dependencies(r)


def test_clean_cold_open_still_verifies():
 root=Path(tempfile.mkdtemp()); s=_start(root)
 try:
  s.run_experiment()
 finally:s.close()
 c=S52Session.open(root)
 try:
  assert c.verify()["ok"] is True
 finally:c.close()


def test_cold_open_rejects_rehashed_candidate_instead_of_returning_false_session():
 root=Path(tempfile.mkdtemp()); s=_start(root)
 try:
  actual=s.run_experiment()
  forged=deepcopy(actual["candidate"]); forged.pop("episode_id",None)
  forged["task_parameters"]["payment_per_actor"]=999
  forged["candidate_hash"]=candidate_digest(forged)
  forged["repertoire"]["candidate_hash"]=forged["candidate_hash"]
  s._append(CANDIDATE_KIND,forged)
 finally:s.close()
 with pytest.raises(S52ColdOpenRefusal) as exc:
  S52Session.open(root)
 assert exc.value.code=="S52_COLD_OPEN_INVALID"
 assert "S52_CANDIDATE_SEMANTIC_INVALID" in str(exc.value)
