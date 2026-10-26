"""Local YAML compatibility bridge for the recovered V3 source runtime.

The source runtime imports PyYAML, which is not installed in the qualified
Python runtime. The system Ruby Psych parser is read-only and converts YAML to
JSON; this bridge supplies only yaml.safe_load and does not install packages or
write outside the S50 return tree.
"""
from __future__ import annotations

import json
import subprocess
import sys
import types

_RUBY = (
    "require 'yaml'; require 'json'; "
    "print JSON.generate(YAML.safe_load(STDIN.read, [], [], true))"
)


def safe_load(value):
    if hasattr(value, "read"):
        value = value.read()
    if not isinstance(value, str):
        raise TypeError("yaml.safe_load expects text or a readable file")
    proc = subprocess.run(
        ["ruby", "-e", _RUBY], input=value, capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise ValueError("YAML_PARSE_FAILED: " + proc.stderr.strip()[:300])
    return json.loads(proc.stdout)


def install() -> None:
    module = sys.modules.get("yaml")
    if module is None:
        module = types.ModuleType("yaml")
        sys.modules["yaml"] = module
    if not hasattr(module, "safe_load"):
        module.safe_load = safe_load


__all__ = ["install", "safe_load"]
