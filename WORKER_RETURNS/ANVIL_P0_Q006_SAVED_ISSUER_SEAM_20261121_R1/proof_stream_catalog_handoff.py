#!/usr/bin/env python3
"""Sourcefree proof of the missing saved-stream catalog/query/predicate handoff.

This is a disposable evidence probe, not an issuer.  It reuses the existing
sourcefree VerifiedAnvilStreamEstate fixture and the existing native I03 owner
to show the exact seam: the verified estate can consume an *externally supplied*
RuntimeObjectCatalog, but nothing produces that catalog from the saved stream.
"""
from __future__ import annotations

import dataclasses
import json
import os
import sys
import tempfile
from pathlib import Path

IMPLEMENTER = Path(os.environ.get(
    "ANVIL_IMPLEMENTER",
    "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/REMONT_Q006_ISSUER",
)).resolve()
sys.path.insert(0, str(IMPLEMENTER))

import pytest  # noqa: E402
from rawlsing_next.pre553_anvil_stream_native_i03 import (  # noqa: E402
    VerifiedAnvilStreamEstate,
    execute_anvil_stream_i03,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog  # noqa: E402
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError  # noqa: E402
from rawlsing_next.tests.test_pre553_anvil_stream_native_i03 import _stream  # noqa: E402


def _roots(estate):
    return dataclasses.asdict(estate.i02)


def main() -> int:
    scratch = Path(tempfile.mkdtemp(
        prefix="q006-saved-issuer-proof-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode",
    ))
    mp = pytest.MonkeyPatch()
    out = {
        "schema": "ANVIL_Q006_SAVED_ISSUER_SEAM_PROOF@1",
        "sourcefree": True,
        "original_source_accessed": False,
        "estate_writes": False,
        "status": "UNKNOWN",
    }
    try:
        (source, auth, predicate, query, catalog, root, release, manifest,
         held, grant) = _stream(scratch, mp, "HANDOFF", source_id="SRC04")
        estate = VerifiedAnvilStreamEstate(
            root, exact_path=release, independently_held=held,
            current_authorizer=grant,
        )
        roots_before = _roots(estate)
        out["verified_estate"] = {
            "stream_roots": roots_before,
            "has_runtime_catalog_attribute": hasattr(estate, "runtime_catalog"),
            "has_query_attribute": hasattr(estate, "query"),
            "has_predicate_attribute": hasattr(estate, "predicate"),
            "native_catalog_constructor_from_estate": None,
            "catalog_needed_by": "execute_anvil_stream_i03(estate, runtime_catalog, query_ref, predicate_ref)",
        }
        out["supplied_catalog"] = {
            "authority_count": len(catalog.authorities),
            "predicate_count": len(catalog.predicates),
            "query_count": len(catalog.queries),
            "origin": "test helper / sourcefree C11 candidate; not produced from VerifiedAnvilStreamEstate",
            "query_ref": query.ref.as_dict(),
            "predicate_ref": predicate.ref.as_dict(),
        }
        positive = execute_anvil_stream_i03(
            estate=estate, runtime_catalog=catalog,
            query_ref=query.ref, predicate_ref=predicate.ref,
        )
        fact = positive.facts[0]
        out["positive"] = {
            "typed_state": fact.typed_state,
            "raw_denominator_support": fact.raw_denominator_support,
            "release_ref": [ref.as_dict() for ref in positive.release_refs],
            "fact_replay_ref": fact.semantic_fields.get("replay_ref"),
            "roots_unchanged": _roots(estate) == roots_before,
            "stream_release_matches_estate": (
                positive.release_refs == (estate.native_release_ref,)
            ),
        }

        # The missing handoff: an empty catalog is not inferred from the estate.
        empty = RuntimeObjectCatalog(
            authorities=tuple(catalog.authorities),
            predicates=(), queries=(), discovery_authorities=(),
        )
        try:
            execute_anvil_stream_i03(
                estate=estate, runtime_catalog=empty,
                query_ref=query.ref, predicate_ref=predicate.ref,
            )
            empty_result = "NOT_REFUSED"
        except Exception as exc:
            empty_result = {"type": type(exc).__name__, "message": str(exc)}
        out["missing_catalog_negative"] = {
            "catalog_constructed_from_estate": False,
            "empty_catalog_result": empty_result,
        }

        # A foreign catalog is not accepted even when structurally valid.
        (source2, auth2, predicate2, query2, catalog2, root2, release2,
         manifest2, held2, grant2) = _stream(
            scratch, mp, "FOREIGN", source_id="SRC16",
        )
        estate2 = VerifiedAnvilStreamEstate(
            root2, exact_path=release2, independently_held=held2,
            current_authorizer=grant2,
        )
        try:
            execute_anvil_stream_i03(
                estate=estate, runtime_catalog=catalog2,
                query_ref=query2.ref, predicate_ref=predicate2.ref,
            )
            foreign_result = "NOT_REFUSED"
        except Exception as exc:
            foreign_result = {"type": type(exc).__name__, "message": str(exc)}
        out["foreign_catalog_negative"] = {
            "result": foreign_result,
            "estate_universe": estate.i02.universe,
            "foreign_universe": estate2.i02.universe,
        }

        # Current authority is checked before and after native execution.
        allowed = {"yes": True}
        (source3, auth3, predicate3, query3, catalog3, root3, release3,
         manifest3, held3, grant3) = _stream(
            scratch, mp, "REVOKE", source_id="SRC04",
            grant=lambda _: allowed["yes"],
        )
        estate3 = VerifiedAnvilStreamEstate(
            root3, exact_path=release3, independently_held=held3,
            current_authorizer=grant3,
        )
        allowed["yes"] = False
        try:
            execute_anvil_stream_i03(
                estate=estate3, runtime_catalog=catalog3,
                query_ref=query3.ref, predicate_ref=predicate3.ref,
            )
            authority_result = "NOT_REFUSED"
        except Exception as exc:
            authority_result = {"type": type(exc).__name__, "message": str(exc)}
        out["authority_negative"] = authority_result

        # A post-admission member mutation remains fail-closed.
        altered = Path(release) / "RespondentEvent.parquet"
        with altered.open("ab") as handle:
            handle.write(b"ALTERED_AFTER_PROOF")
        try:
            estate._recheck_unchanged_members()
            altered_result = "NOT_REFUSED"
        except Exception as exc:
            altered_result = {"type": type(exc).__name__, "message": str(exc)}
        out["member_mutation_negative"] = altered_result

        out["nonanswer_state"] = {
            "proven_by_sourcefree_fixture": False,
            "reason": "the reusable fixture proves the stream/catalog seam only; q103 97/98/99 and asked routing remain outside this sourcefree fixture",
            "q103_nonanswer_cells": "NOT_PROVEN__SOURCE_AUTHORITY_MISSING",
        }
        out["status"] = "NO_SAVED_STREAM_CATALOG_PRODUCER__SEAM_AND_NEGATIVES_EXECUTED"
    except Exception as exc:
        out["status"] = "ERROR"
        out["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        mp.undo()
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
