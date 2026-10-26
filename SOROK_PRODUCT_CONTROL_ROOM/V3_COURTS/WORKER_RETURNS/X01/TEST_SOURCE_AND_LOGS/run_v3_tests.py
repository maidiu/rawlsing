"""Run original v3 tests sourcefree with a read-only YAML bridge.

PyYAML is absent in the qualified Python. The system Ruby Psych parser is used
only to supply yaml.safe_load; numeric YAML keys are converted back to ints so
the original age-bracket tests are not changed by JSON stringification.
Set RAWLSING_STAGING_ROOT to the extracted Rawlsing_code_bundle_staging root.
"""
from __future__ import annotations
import json, os, subprocess, sys, types
from pathlib import Path

SOURCE = Path(os.environ["RAWLSING_STAGING_ROOT"])
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))
_RUBY = "require 'yaml'; require 'json'; print JSON.generate(YAML.safe_load(STDIN.read, [], [], true))"
def _conv(obj):
    if isinstance(obj, dict):
        return {(int(k) if isinstance(k, str) and k.isdigit() else k): _conv(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_conv(v) for v in obj]
    return obj
def safe_load(value):
    if hasattr(value, "read"):
        value = value.read()
    p = subprocess.run(["ruby", "-e", _RUBY], input=value, capture_output=True, text=True)
    if p.returncode != 0:
        raise ValueError("YAML_PARSE_FAILED: " + p.stderr.strip()[:300])
    return _conv(json.loads(p.stdout))
_m = sys.modules.get("yaml") or types.ModuleType("yaml")
_m.safe_load = safe_load
sys.modules["yaml"] = _m
import pytest
raise SystemExit(pytest.main(["-q", "-p", "no:cacheprovider", *sys.argv[1:]]))
