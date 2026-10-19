"""Shared F6P test fixtures: actual F6M/A/A0 products from the pinned sources."""
from __future__ import annotations

import copy
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "native", ROOT / "oracle"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import f6c_oracle_worlds as OW  # noqa: E402
from rawlsing_next import pre553_heterogeneous_synthesis as F6M  # noqa: E402
from rawlsing_next import pre553_heterogeneous_synthesis_A as A  # noqa: E402
from rawlsing_next import pre553_heterogeneous_synthesis_A0 as A0  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

MODULES = {"A": A, "A0": A0, "B": F6M}


def build(kind, world):
    target, sources, policy = OW.WORLD_BUILDERS[world]()
    return MODULES[kind].synthesize(target, sources, policy)


def request(world):
    conditions, outcome = OW.CONSUMER_REQUEST[world]
    return {"conditions": dict(conditions), "outcome": outcome}


def rehash(bundle):
    out = copy.deepcopy(bundle)
    out.pop("content_hash", None)
    out["content_hash"] = semantic_hash(out)
    return out


def git_blob(path):
    raw = Path(path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def f6m_blob():
    return git_blob(F6M.__file__)
