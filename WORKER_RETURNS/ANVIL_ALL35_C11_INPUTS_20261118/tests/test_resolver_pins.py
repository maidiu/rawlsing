from __future__ import annotations
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "resolve_config.py"
BUNDLE = ROOT / "bundles/SRC04.json"

def load_module():
    spec = importlib.util.spec_from_file_location("all35_resolver_under_test", RESOLVER)
    m = importlib.util.module_from_spec(spec); assert spec.loader is not None
    spec.loader.exec_module(m); return m

def run(tmp_path, *args):
    p = subprocess.run([sys.executable, "-B", str(RESOLVER), "--bundles", str(ROOT/"bundles"), *map(str,args)],
                       cwd=str(ROOT), text=True, capture_output=True,
                       env={**__import__("os").environ, "PYTHONPATH": str(ROOT.parents[1]), "PYTHONDONTWRITEBYTECODE": "1"})
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)

def test_both_exact_pins_resolve_and_materialize(tmp_path):
    m = load_module()
    assert m.SRC04_PINS["v2-historical"]["default_for_frozen_run"] is True
    assert m.SRC04_PINS["v3-accepted"]["default_for_frozen_run"] is False
    for pin_name, pin in (("v2-historical", m.SRC04_PINS["v2-historical"]), ("v3-accepted", m.SRC04_PINS["v3-accepted"])):
        out = tmp_path / pin_name; out.mkdir()
        row = run(out, "--source-id", "SRC04", "--src04-pin", pin_name, "--out-dir", out)
        assert row["selected_pin"] == pin_name
        assert row["file_sha256"] == pin["file_sha256"]
        assert row["canonical_sha256"] == pin["canonical_sha256"]
        raw = (out / "SRC04.config.json").read_bytes()
        assert __import__("hashlib").sha256(raw).hexdigest() == pin["file_sha256"]
    # Default remains historical v2.
    row = run(tmp_path, "--source-id", "SRC04")
    assert row["selected_pin"] == "v2-historical" and row["historical_default"] is True

def test_swapped_wave_and_arbitrary_revision_refuse(tmp_path):
    m = load_module()
    bundle = json.loads(BUNDLE.read_text()); bad = copy.deepcopy(bundle); bad["wave"] = "WRONG"
    bad_path = tmp_path / "bad.json"; bad_path.write_text(json.dumps(bad))
    try:
        m.resolve_one(bad_path, src04_pin="v3-accepted")
    except m.ResolveRefusal as exc:
        assert "CONFIG_BINDING_MISMATCH" in str(exc)
    else:
        raise AssertionError("swapped wave accepted")
    try:
        m.resolve_one(BUNDLE, src04_pin="v4-arbitrary")
    except m.ResolveRefusal as exc:
        assert "UNKNOWN_SRC04_PIN" in str(exc)
    else:
        raise AssertionError("arbitrary pin accepted")

def test_stale_historical_src04_refuses(tmp_path):
    m = load_module()
    bundle = json.loads(BUNDLE.read_text())
    bundle["source_config"].update({
        "revision_commit": "1924499ef52403a0f331b8aff9b7c7eff99bf1e2",
        "revision_path": "rawlsing_next/source_configuration/data/SRC04/source.config.json",
        "path": "rawlsing_next/source_configuration/data/SRC04/source.config.json",
        "file_sha256": "eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900",
    })
    p = tmp_path / "stale.json"; p.write_text(json.dumps(bundle))
    try:
        m.resolve_one(p, src04_pin="v2-historical")
    except m.ResolveRefusal as exc:
        assert "STALE_SRC04_CONFIG_REFUSED" in str(exc)
    else:
        raise AssertionError("stale SRC04 accepted")
