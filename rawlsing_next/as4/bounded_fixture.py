"""B21/HB04 bounded governed fixture adapter.

This module is an implementation/qualification vehicle only.  It deliberately
reuses already-governed B20 Route-C and Route-A test material.  It never opens
LiTS-I/WVS7 and cannot be selected as a production source provider.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from rawlsing_next.as4.loader import HB04FreezeError, repository_root
from rawlsing_next.as4.protocol import HB04PreparedSource, HB04Workload
from rawlsing_next.pre553_source_backed_c11_facade import build_validated_source_backed_c11_release


_B20_DRIVER = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/"
    "WORKERS/B20_AS4I_ROUTE_C_CACC1_CACC2_PARITY_ADAPTER_R1/"
    "01_ROUTE_C_IMPLEMENTATION_QUALIFICATION.py"
)


def _load_b20():
    path = repository_root() / _B20_DRIVER
    spec = importlib.util.spec_from_file_location("_hb04_bounded_b20", path)
    if spec is None or spec.loader is None:
        raise HB04FreezeError("cannot load frozen B20 bounded qualification fixture")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_bounded_source(candidate: str, workdir: Path) -> HB04PreparedSource:
    if candidate not in {"A", "B", "C"}:
        raise HB04FreezeError("bounded HB04 candidate must be A/B/C")
    m = _load_b20()
    tag = "hb04-common-bounded"
    fx, incidence, stream, projection, determinants = m._route_c_fixture(tag)

    release = build_validated_source_backed_c11_release(incidence, projection)
    source = m._runtime_source(fx, release)
    qauth = m._query_authority("hb04-common-bounded-query")
    all_p = m._branch_predicate(source, qauth, tag="hb04-all")
    x1 = m._predicate(
        source,
        qauth,
        m._route_c_response_leaf(source, qauth, "X", 1),
        tag="hb04-x1",
    )
    query = m._route_c_query(source, qauth, all_p, ("M",), tag="hb04-query")

    dauth = m._d_auth("hb04-common-bounded-discovery")
    operation = "I03-OP-hb04-common-bounded-discovery"
    dquery = m._route_c_query(
        source, qauth, all_p, ("M",), tag="hb04-discovery-template"
    )
    grammar = m._grammar(
        operation=operation,
        atoms=[m._atom("ALL", all_p, "BRANCH"), m._atom("X1", x1, "RESPONSE")],
        templates=[m._qt("M", dquery)],
        rules=[
            m._rule(
                "minority",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("X1",),
                baseline_atom_id="ALL",
                query_template_id="M",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
        ],
    )
    da = m._discovery_authority(source, grammar, dauth, tag="hb04-da")
    registry = m._registry(source, qauth, dauth)
    workload = HB04Workload(
        authority_registry=registry,
        i03_query=query,
        i03_predicate=all_p,
        discovery_authority=da,
        predicate_catalog=(all_p, x1),
        query_template_catalog=(dquery,),
        required_cacc2_roles_for_i03=("A000",),
    )

    c2det = m.Cacc2Determinants(
        cacc1_determinant_hash=determinants.content_hash,
        discovery_authority_ref=m.ExactRef(
            "DiscoveryAuthority@1.0.0",
            f"urn:test:hb04:da:{m._h('hb04-da')}",
            m._h("hb04-da"),
        ),
        predicate_catalog_hash=m._h("hb04-predicate-catalog"),
        risk_partition_hash=m._h("hb04-risk-partition"),
        production_operation_identity="HB04_BOUNDED_GOVERNED_FIXTURE_OPERATION",
        candidate_frontier_ref=m.ExactRef(
            "PRE553_I05_EVALUATED_FRONTIER",
            f"urn:test:hb04:frontier:{m._h('hb04-frontier')}",
            m._h("hb04-frontier"),
        ),
    )

    cleanup_root = Path(workdir) / "bounded_source"
    cleanup_root.mkdir(parents=True, exist_ok=True)
    r5_reader = None
    transport: Any = incidence
    if candidate == "A":
        from rawlsing_next.tests.test_pre553_r5_source_backed_adapter import _reader

        fx_for_a = dict(fx)
        fx_for_a.update(
            {
                "incidence": incidence,
                "projection": projection,
                "source_sha": incidence.source_sha256,
                "cells": tuple(incidence.iter_cells()),
            }
        )
        r5_reader = _reader(cleanup_root, fx_for_a, name="route_a")
    elif candidate == "C":
        transport = stream

    return HB04PreparedSource(
        source_sha256=incidence.source_sha256,
        projection=projection,
        transport=transport,
        workload=workload,
        mode="BOUNDED_GOVERNED_FIXTURE",
        r5_reader=r5_reader,
        route_c_determinants=determinants if candidate == "C" else None,
        route_c_cacc2_determinants=c2det if candidate == "C" else None,
        route_c_atom_bindings=m._atom_bindings(all_p, x1) if candidate == "C" else (),
        cleanup_paths=(cleanup_root,),
        source_identity_receipt={
            "schema": "HB04_BOUNDED_GOVERNED_SOURCE_IDENTITY@1.0.0",
            "source_sha256": incidence.source_sha256,
            "row_count": incidence.row_count,
            "transport": "R5_FROZEN_REOPEN" if candidate == "A" else (
                "SOURCE_BACKED_VIRTUAL_C11" if candidate == "B" else "ROUTE_C_EXACT_STREAM"
            ),
            "real_lits1_opened": False,
            "real_wvs7_opened": False,
            "c09_executed": False,
        },
    )


__all__ = ["build_bounded_source"]
