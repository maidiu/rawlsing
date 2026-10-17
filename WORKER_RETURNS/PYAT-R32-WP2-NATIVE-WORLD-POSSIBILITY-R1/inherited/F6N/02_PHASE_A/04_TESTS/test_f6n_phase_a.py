"""F6N Phase-A independent consumer/authority falsifiers.

Frozen before F6M content is read.  These tests are additive to the inherited
F6L 26-test safe-behaviour court and the F6J/F6C/35-native courts.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[2]
F6L = RET / "01_INHERITED_F6L"
sys.dont_write_bytecode = True
sys.path.insert(0, str(F6L / "01_STAGED_NATIVE"))
sys.path.insert(0, str(F6L / "02_PHASE_A/03_SCRIPTS"))
sys.path.insert(0, str(RET / "02_PHASE_A/03_SCRIPTS"))

from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, SynthesisError, METHOD)
import rawlsing_next.pre553_heterogeneous_synthesis as PRODUCER  # noqa: E402
import f6l_worlds as W  # noqa: E402
import f6n_worlds as N  # noqa: E402

CASES = json.loads((RET / "02_PHASE_A/01_FROZEN_CONSUMER_CASES.json").read_text())
CASE = {c["id"]: c for c in CASES["cases"]}
COMPLETE_ALLOWED = {"SYNTHETIC_CANDIDATE", "COMPLETE_TARGET_JOINT",
                    "SYNTHETIC_COMPLETE_CANDIDATE"}
PARTIAL_MARKERS = ("PARTIAL", "NO_COMPLETE", "INCOMPLETE", "BACKOFF", "UNIDENTIFIED")


def cells(cell_list):
    return {tuple(c["categories"]): F(c["probability"]) for c in cell_list}


def run(world):
    return synthesize(world["target"], world["sources"], world["policy"],
                      admit=lambda *_: True)


def is_partial(decision):
    return decision not in COMPLETE_ALLOWED and any(m in decision for m in PARTIAL_MARKERS)


def test_n1_rare_category_not_silently_renormalized_into_false_complete():
    world = N.rare_renormalization(150)
    out = run(world)
    cand = out["candidate"]
    assert cand is not None
    support = cand["support"]["Z1"]
    assert support["excluded_sources"] == ["R1"]
    full_complete = (cand["distribution"] is not None
                     and F(cand["uncovered_target_mass"]) == 0
                     and out["decision"] in COMPLETE_ALLOWED)
    assert not full_complete, (
        "rare-category source excluded but a complete S2-only population point "
        "was still issued")


def test_n2_source_scope_risk_substitution_is_refused():
    world = N.scope_mismatch()
    out = synthesize(world["target"], world["sources"], world["policy"],
                     admit=lambda *_: True)
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"
    assert out["candidate"] is None
    assert "TARGET_SCOPE_MISMATCH" in out["refusals"]["S1"]


def test_n3_mapping_hash_substitution_is_refused():
    world = N.mapping_hash_substitution()
    out = synthesize(world["target"], world["sources"], world["policy"],
                     admit=lambda *_: True)
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"
    assert out["candidate"] is None
    assert "MAPPING_REVIEW_PREIMAGE_MISMATCH" in out["refusals"]["S1"]


def test_n4_product_ref_substitution_binds_current_source_identity():
    pristine = run(N.positive_world())
    swapped_world = N.product_ref_substitution()
    swapped = synthesize(swapped_world["target"], swapped_world["sources"],
                         swapped_world["policy"], admit=lambda *_: True)
    assert swapped["decision"] == "SYNTHETIC_CANDIDATE"
    assert [b["measured_parent_ref"] for b in swapped["baseline"]] == [
        "F6L_PRODUCT_S2", "F6L_PRODUCT_S1"]
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    assert [b["input_hash"] for b in swapped["baseline"]] == [
        semantic_hash(s) for s in swapped_world["sources"]]
    assert swapped["content_hash"] != pristine["content_hash"]


def test_n5_duplicate_source_identity_is_refused():
    world = N.duplicate_source_identity()
    out = synthesize(world["target"], world["sources"], world["policy"],
                     admit=lambda *_: True)
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"
    assert out["candidate"] is None
    assert out["overlap_diagnostics"][0]["reason"] == "DUPLICATE_SAMPLE"


def test_n6_producer_hash_substitution_is_detectable():
    src = F6L / "01_STAGED_NATIVE/rawlsing_next/pre553_heterogeneous_synthesis.py"
    raw = src.read_bytes()
    good_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert good_blob == CASES["native_under_test"]["producer_blob"]

    def guard(path, expected):
        data = Path(path).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if blob != expected:
            raise RuntimeError("PRODUCER_IDENTITY_MISMATCH")
        return blob

    assert guard(src, good_blob) == good_blob
    with tempfile.TemporaryDirectory() as td:
        mutated = Path(td) / "producer.py"
        data = bytearray(raw)
        data[-1] ^= 1
        mutated.write_bytes(bytes(data))
        with pytest.raises(RuntimeError, match="PRODUCER_IDENTITY_MISMATCH"):
            guard(mutated, good_blob)


def test_n7_machine_independent_relative_staging_is_reproducible():
    stage = F6L / "01_STAGED_NATIVE"
    assert not any(p.is_symlink() for p in stage.rglob("*")), "stage must not use symlinks"
    world = N.positive_world()
    script = """
import json,sys
from rawlsing_next.pre553_heterogeneous_synthesis import synthesize
w=json.load(open(sys.argv[1]))
out=synthesize(w['target'],w['sources'],w['policy'],admit=lambda *_: True)
print(out['content_hash'])
"""
    hashes = []
    with tempfile.TemporaryDirectory() as parent:
        for root in ("root-a", "root-b"):
            stage_copy = Path(parent) / root / "stage"
            shutil.copytree(stage, stage_copy)
            inp = Path(parent) / root / "world.json"
            inp.write_text(json.dumps(world))
            env = dict(__import__("os").environ)
            env["PYTHONPATH"] = str(stage_copy)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            proc = subprocess.run([sys.executable, "-B", "-c", script, str(inp)],
                                  capture_output=True, text=True, env=env, check=True)
            hashes.append(proc.stdout.strip())
    assert hashes[0] == hashes[1]
    assert len(hashes[0]) == 64


def test_n8_positive_complete_sourcefree_world_is_preserved():
    out = run(N.positive_world())
    cand = out["candidate"]
    assert cand is not None
    assert cand["distribution"] is not None
    assert F(cand["uncovered_target_mass"]) == 0
    assert cells(cand["distribution"]) == {
        ("LOW", "NO"): F(1, 3), ("LOW", "YES"): F(1, 6),
        ("HIGH", "NO"): F(1, 6), ("HIGH", "YES"): F(1, 3),
    }
    cond = conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION")
    assert cond["state"] == "SUPPORTED_MODEL"
    assert F(cond["probabilities"]["YES"]) == F(1, 3)
    assert cond["uncertainty"] == "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED"
    assert out["decision"] in COMPLETE_ALLOWED
