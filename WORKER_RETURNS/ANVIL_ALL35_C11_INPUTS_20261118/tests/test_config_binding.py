from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "producer.py"
RESOLVER = ROOT / "resolve_config.py"
MATRIX = ROOT / "evidence" / "35_row_source_rights_matrix.json"


def load_producer():
    spec = importlib.util.spec_from_file_location("all35_producer_under_test", PRODUCER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_producer(tmp_path):
    out = tmp_path / "result.json"
    bundles = tmp_path / "bundles"
    p = subprocess.run(
        [sys.executable, "-B", str(PRODUCER), "--matrix", str(MATRIX),
         "--out", str(out), "--bundles", str(bundles)],
        cwd=str(ROOT), text=True, capture_output=True,
        env={**__import__("os").environ, "PYTHONPATH": str(ROOT.parents[1]),
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert p.returncode == 0, p.stderr
    return json.loads(out.read_text()), bundles


def test_all35_exact_config_revisions_are_bound_to_wave_source_sha_and_shape(tmp_path):
    producer = load_producer()
    matrix = producer.load_matrix(MATRIX)
    index = producer.load_config_index(matrix)
    result, bundles = run_producer(tmp_path)
    assert result["config_binding_count"] == 35
    assert result["config_binding_failures"] == 0
    assert result["q2_executable_bundles"] == 0
    assert result["q2_held_bundles"] == 35
    refs = set()
    with tempfile.TemporaryDirectory(prefix="anvil-all35-bind-test-") as tmp:
        for source, index_row in zip(matrix["sources"], index["rows"]):
            sid = source["source_id"]
            bundle = json.loads((bundles / f"{sid}.json").read_text())
            binding = producer.bind_one_config(index_row, bundle, source, tmp)
            assert all(binding["checks"].values()), (sid, binding["checks"])
            assert binding["wave"] == bundle["wave"] == source["wave"]
            assert binding["file_sha256"] == bundle["source_config"]["file_sha256"]
            assert binding["canonical_sha256"] == bundle["source_config"]["canonical_sha256"]
            assert "current materialized SourceConfig" not in bundle["missing_q2_inputs"]
            refs.add(binding["revision_ref"])
        assert len(refs) == 35


def test_resolver_reopens_all_35_exact_configs(tmp_path):
    _, bundles = run_producer(tmp_path)
    p = subprocess.run(
        [sys.executable, "-B", str(RESOLVER), "--bundles", str(bundles), "--all"],
        cwd=str(ROOT), text=True, capture_output=True,
        env={**__import__("os").environ, "PYTHONPATH": str(ROOT.parents[1]),
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert p.returncode == 0, p.stderr
    data = json.loads(p.stdout)
    assert data["status"] == "PASS"
    assert data["resolved"] == 35
    assert data["distinct_revisions"] == 35
    assert all(all(r["checks"].values()) for r in data["rows"])


def test_swapped_config_is_refused(tmp_path):
    producer = load_producer()
    matrix = producer.load_matrix(MATRIX)
    index = producer.load_config_index(matrix)
    _, bundles = run_producer(tmp_path)
    row = copy.deepcopy(index["rows"][0])
    row["source_config"] = copy.deepcopy(index["rows"][1]["source_config"])
    bundle = json.loads((bundles / "SRC01.json").read_text())
    with tempfile.TemporaryDirectory(prefix="anvil-all35-bind-swap-") as tmp:
        with pytest.raises(producer.ProducerRefusal, match="CONFIG_BINDING_MISMATCH|CONFIG_SOURCE"):
            producer.bind_one_config(row, bundle, matrix["sources"][0], tmp)


def test_swapped_wave_and_source_sha_are_refused(tmp_path):
    producer = load_producer()
    matrix = producer.load_matrix(MATRIX)
    index = producer.load_config_index(matrix)
    _, bundles = run_producer(tmp_path)
    bundle = json.loads((bundles / "SRC01.json").read_text())
    wrong_wave = copy.deepcopy(bundle)
    wrong_wave["wave"] = "WRONG_WAVE"
    wrong_sha = copy.deepcopy(bundle)
    wrong_sha["source_sha256"] = "0" * 64
    with tempfile.TemporaryDirectory(prefix="anvil-all35-bind-wave-") as tmp:
        with pytest.raises(producer.ProducerRefusal, match="CONFIG_BINDING_MISMATCH"):
            producer.bind_one_config(index["rows"][0], wrong_wave, matrix["sources"][0], tmp)
        with pytest.raises(producer.ProducerRefusal, match="CONFIG_BINDING_MISMATCH"):
            producer.bind_one_config(index["rows"][0], wrong_sha, matrix["sources"][0], tmp)


def test_stale_src04_row_is_refused(tmp_path):
    producer = load_producer()
    matrix = producer.load_matrix(MATRIX)
    index = producer.load_config_index(matrix)
    _, bundles = run_producer(tmp_path)
    row = copy.deepcopy(next(r for r in index["rows"] if r["source_id"] == "SRC04"))
    row["source_config"].update({
        "revision_commit": "1924499ef52403a0f331b8aff9b7c7eff99bf1e2",
        "revision_path": "rawlsing_next/source_configuration/data/SRC04/source.config.json",
        "file_sha256": "eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900",
    })
    bundle = json.loads((bundles / "SRC04.json").read_text())
    with tempfile.TemporaryDirectory(prefix="anvil-all35-bind-stale-") as tmp:
        with pytest.raises(producer.ProducerRefusal, match="STALE_SRC04_CONFIG_REFUSED"):
            producer.bind_one_config(row, bundle, matrix["sources"][3], tmp)
