"""Actual source-free call path into the pinned PE / C1 / N10E producers.

The empirical lane of the SC0 port is **producer-derived**:
  1. the pinned N10E provider (``pre553_empirical_possibility_provider.
     provide_empirical_possibility_slice``) over the pinned AT07 fixture rows
     executes the accepted C1 composition (``pre553_analytical_composition.
     compose_positioned_subject_possibility``) and the public N10E consumer,
     computing the exact support fractions the possibility receipt reports;
  2. the pinned PE candidate (``pre553_postastra_pe_generic_world_possibility.
     serve_generic_world_situated_possibility``) is executed as the PE seam
     witness on its own real fixture case.

Static TEST_ONLY hints are NOT accepted as the connection oracle: the call
counter records real calls into the pinned modules and the receipt's support is
the computed geometry, never caller-written.

Pinned blobs (staging/staging_manifest.json):
  PE   58484f4c3d9aae148d4116dcf00420c432aefcbd
  C1   604c8d591d4cc2b646e9b149cdb233fc9d69cf6b
  N10E 23167aa25291fb148b1e3cf210ac33fe7769b783
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Dict

RET = Path(__file__).resolve().parents[1]
_NS = RET / "staging" / "ns"
_REPO = RET.parents[1]
for _p in (str(_REPO), str(_NS), str(_NS / "rawlsing_next" / "tests"),
           str(_REPO / "rawlsing_next" / "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import rawlsing_next.pre553_analytical_composition as _C1  # noqa: E402
import rawlsing_next.pre553_empirical_possibility_provider as _N10E  # noqa: E402
import rawlsing_next.pre553_postastra_pe_generic_world_possibility as _PE  # noqa: E402

PINNED_MODULES = {"PE": _PE, "C1": _C1, "N10E": _N10E}
_FILE_KEYS = {str(Path(m.__file__).resolve()): n for n, m in PINNED_MODULES.items()}


def _blob(p: Path) -> str:
    b = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def pinned_provenance() -> Dict[str, Any]:
    return {
        name: {
            "file": str(Path(mod.__file__).resolve().relative_to(_REPO)),
            "git_blob_sha1": _blob(Path(mod.__file__).resolve()),
        }
        for name, mod in PINNED_MODULES.items()
    }


_ACTIVE: list = []


def _dispatch(frame, event, arg):
    if event == "call" and _ACTIVE:
        name = _FILE_KEYS.get(frame.f_code.co_filename)
        if name is not None:
            key = (name, frame.f_code.co_name)
            for counter in _ACTIVE:
                counter.calls[key] = counter.calls.get(key, 0) + 1
    return _dispatch


class ProducerCallCounter:
    """Real call counter into the pinned modules (no monkeypatch, no fake estimator).

    Nest-safe: an outer probe counter and the adapter's internal counter both
    observe the same real call events (single dispatcher, active stack).
    """

    def __init__(self) -> None:
        self.calls: Dict[tuple, int] = {}

    def reset(self) -> None:
        self.calls = {}

    def __enter__(self) -> "ProducerCallCounter":
        _ACTIVE.append(self)
        sys.setprofile(_dispatch)
        return self

    def __exit__(self, *exc) -> None:
        if self in _ACTIVE:
            _ACTIVE.remove(self)
        if not _ACTIVE:
            sys.setprofile(None)

    def summary(self) -> list:
        return sorted(
            ({"module": k[0], "function": k[1], "calls": v} for k, v in self.calls.items()),
            key=lambda d: (d["module"], d["function"]),
        )

    def total(self) -> int:
        return sum(self.calls.values())

    def modules_touched(self) -> list:
        return sorted({k[0] for k in self.calls})


def compute_pinned_empirical_lane(
    *, counter: "ProducerCallCounter | None" = None
) -> Dict[str, Any]:
    """Execute pinned N10E->C1->consumer (production lane) and the PE seam.

    Returns producer-derived support and cell geometry.  Nothing in the result
    is caller-written: the fractions come from the accepted composition path.
    """
    from rawlsing_next.tests import n10e_empirical_slice_fixture as fx

    case = fx.build_provider_case("forward")
    own = counter if counter is not None else ProducerCallCounter()
    started_profile = counter is None
    if started_profile:
        own.__enter__()
    try:
        n10e_result = _N10E.provide_empirical_possibility_slice(
            repository=case["source"]["repo"],
            empirical_query=case["empirical_query"],
            predicate=case["predicate"],
            authority_registry=case["registry"],
            release_refs=case["release_refs"],
            consumer_query=case["consumer_query"],
            model_rule=case["model_rule"],
            condition_binding_witness=case["condition_binding_witness"],
        )
    finally:
        if started_profile:
            own.__exit__(None, None, None)

    evidence = n10e_result.generated_evidence_or_null
    geometry = (evidence.geometry or {}) if evidence is not None else {}
    denom = (geometry.get("denominator") or {}).get("raw_denominator_support")
    cells = []
    yes = no = None
    for cell in geometry.get("cells", []):
        frac = (cell.get("raw_probability_exact_fraction") or {}).get("$exact_fraction")
        n = cell.get("raw_numerator_support")
        cells.append({"value": cell.get("cell"), "n": n, "fraction": frac,
                      "cell_state": cell.get("cell_state")})
        if cell.get("cell") == "yes":
            yes = n
        elif cell.get("cell") == "no":
            no = n

    # PE seam witness (own real fixture case; also executes C1 underneath)
    from rawlsing_next.tests.test_postastra_pe_fixture import law_a_cases

    pe_case = law_a_cases()["multi_binding_parent_context"]
    if started_profile:
        own.__enter__()
    try:
        pe_result = _PE.serve_generic_world_situated_possibility(
            repository=pe_case["repository"],
            empirical_query=pe_case["empirical_query"],
            predicate=pe_case["predicate"],
            authority_registry=pe_case["registry"],
            release_refs=pe_case["release_refs"],
            request=pe_case["request"],
            model_rule=pe_case["model_rule"],
            condition_binding_witness=pe_case["witness"],
        )
    finally:
        if started_profile:
            own.__exit__(None, None, None)

    support = {
        "target_yes": yes,
        "target_no": no,
        "denominator": denom,
        "base_ratio": f"{yes}/{denom}" if yes is not None and denom else None,
        "minority_ratio": f"{no}/{denom}" if no is not None and denom else None,
        "risk_set": "fx:risk:asked_eligible",
        "routing": "fx:routing:asked",
        "weight": "fx:design_weight:unit",
        "uncertainty": "fx:u:fixture_no_real_inference",
    }
    return {
        "connected": True,
        "producer": "PINNED_N10E_C1_CONSUMER_PLUS_PE_SEAM",
        "n10e_result_state": getattr(n10e_result, "provider_state", None),
        "pe_result_state": getattr(pe_result, "result_state", None),
        "cells": cells,
        "support": support,
        "denominator": denom,
        "evidence_digest": getattr(getattr(evidence, "evidence_ref", None), "content_hash", None),
        "lane_digest": hashlib.sha256(
            (str(sorted((k, v) for k, v in own.calls.items())) + str(cells) + str(support)).encode()
        ).hexdigest(),
        "calls": own.summary(),
        "call_total": own.total(),
        "modules_touched": own.modules_touched(),
    }
