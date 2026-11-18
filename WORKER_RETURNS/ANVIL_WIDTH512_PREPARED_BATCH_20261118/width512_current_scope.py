"""Exact test-only current callback bound to the retained WIDTH128 scope."""
from __future__ import annotations

import json
import os
from pathlib import Path

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots

_CONTRACT_PATH = Path(os.environ["ANVIL_WIDTH512_CONTRACT"])
_CONTRACT = json.loads(_CONTRACT_PATH.read_text())
_EXPECTED = ExternalI02Roots(**_CONTRACT["i02"])


def authorize(roots):
    """Allow only the independently held WIDTH128 I02 roots; no fallback."""
    return roots == _EXPECTED
