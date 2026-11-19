#!/usr/bin/env python3
"""Sourcefree RED/GREEN probe for the isolated I05 unresolved repair.

Run with ANVIL_IMPLEMENTER pointing at a tree containing rawlsing_next.  The
probe uses the existing prepared-saved fixture and the actual native I05
`execute_exact_bounded_discovery` path.  No Batch owner is invoked or edited.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

IMPLEMENTER = Path(os.environ["ANVIL_IMPLEMENTER"]).resolve()
sys.path.insert(0, str(IMPLEMENTER))

import pytest  # noqa: E402
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog  # noqa: E402
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission  # noqa: E402
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError  # noqa: E402
from rawlsing_next.tests.test_pre553_discovery_exact import (  # noqa: E402
    _atom,
    _d_auth,
    _discovery_authority,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (  # noqa: E402
    _branch_predicate,
    _query,
)
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture  # noqa: E402
from rawlsing_next.tests.test_pyat940_s2f_b_negative_and_multisource import (  # noqa: E402
    _unsupported_topology_query,
)


def main() -> int:
    scratch = Path(tempfile.mkdtemp(
        prefix="src16-i05-repair-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode",
    ))
    monkeypatch = pytest.MonkeyPatch()
    out = {
        "schema": "ANVIL_SRC16_I05_UNRESOLVED_VERIFY@1",
        "tree": str(IMPLEMENTER),
        "sourcefree": True,
        "batch_invoked": False,
    }
    try:
        source, qa, all_p, _other, queries, base = _fixture(
            monkeypatch, scratch / "fixture", "I05-REPAIR",
        )
        negative_query = _unsupported_topology_query(
            source, qa, all_p, tag="i05-repair-negative",
        )
        dn = _d_auth("i05-repair-negative")
        negative_grammar = _grammar(
            operation="I03-OP-i05-repair-negative",
            atoms=[_atom("ALL", all_p, "BRANCH")],
            templates=[_qt("NEG", negative_query)],
            rules=[_rule(
                "negative",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("ALL",),
                baseline_atom_id="ALL",
                query_template_id="NEG",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )],
        )
        negative_authority = _discovery_authority(
            source, negative_grammar, dn, tag="i05-repair-negative",
        )

        empty_predicate = _branch_predicate(source, qa, members=(), tag="i05-repair-empty")
        empty_query = _query(source, qa, empty_predicate, ("Y",), tag="i05-repair-empty")
        de = _d_auth("i05-repair-empty")
        empty_grammar = _grammar(
            operation="I03-OP-i05-repair-empty",
            atoms=[
                _atom("ALL", all_p, "BRANCH"),
                _atom("EMPTY", empty_predicate, "BRANCH"),
            ],
            templates=[_qt("EMPTY", empty_query)],
            rules=[_rule(
                "empty",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("EMPTY",),
                baseline_atom_id="ALL",
                query_template_id="EMPTY",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )],
        )
        empty_authority = _discovery_authority(
            source, empty_grammar, de, tag="i05-repair-empty",
        )

        catalog = RuntimeObjectCatalog(
            authorities=tuple((*source["authorities"], qa, dn, de)),
            predicates=(all_p, empty_predicate),
            queries=(queries["selected"], negative_query, empty_query),
            discovery_authorities=(negative_authority, empty_authority),
        )
        admission = PreparedSavedC11Admission.open(
            root=Path(base.estate_path).parents[1],
            exact_path=base.estate_path,
            independently_held_manifest_sha256=base.manifest_sha256,
            independently_held_i02=base.i02,
            release_ref=base.release_ref,
            runtime_catalog=catalog,
            current_authorizer=lambda _roots: True,
        )
        positive = admission.execute_i03(
            query_ref=queries["selected"].ref, predicate_ref=all_p.ref,
        )
        unresolved = admission.execute_i05(
            discovery_authority_ref=negative_authority.ref,
        )
        empty = admission.execute_i05(
            discovery_authority_ref=empty_authority.ref,
        )
        out["positive"] = {
            "typed_state": positive.facts[0].typed_state,
            "raw_denominator_support": positive.facts[0].raw_denominator_support,
        }
        out["unresolved"] = {
            "fact_states": [f.typed_state for f in unresolved.empirical_facts],
            "coverage_state": unresolved.receipts[0].coverage_state,
            "typed_state": unresolved.receipts[0].typed_state,
            "valid_empty": unresolved.valid_empty,
        }
        out["valid_empty"] = {
            "fact_states": [f.typed_state for f in empty.empirical_facts],
            "coverage_state": empty.receipts[0].coverage_state,
            "typed_state": empty.receipts[0].typed_state,
            "valid_empty": empty.valid_empty,
        }

        state = {"now": True}
        denied = PreparedSavedC11Admission.open(
            root=Path(base.estate_path).parents[1],
            exact_path=base.estate_path,
            independently_held_manifest_sha256=base.manifest_sha256,
            independently_held_i02=base.i02,
            release_ref=base.release_ref,
            runtime_catalog=catalog,
            current_authorizer=lambda _roots: state["now"],
        )
        state["now"] = False
        try:
            denied.execute_i05(discovery_authority_ref=negative_authority.ref)
            out["authority_denial"] = "NOT_REFUSED"
        except DirectEstateError as exc:
            out["authority_denial"] = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
        out["status"] = "GREEN" if out["unresolved"]["coverage_state"] == "EVALUATED_UNRESOLVED" else "RED"
    except Exception as exc:
        out["status"] = "ERROR"
        out["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        monkeypatch.undo()
    print(json.dumps(out, sort_keys=True))
    return 0 if out["status"] == "GREEN" and out["authority_denial"] != "NOT_REFUSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
