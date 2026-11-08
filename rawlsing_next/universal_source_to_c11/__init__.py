"""Universal source-to-C11 wiring for the declared R157 35-source estate.

This package is a thin, data-driven receive layer.  It imports the frozen R157
``rawlsing_next.source_configuration`` package at its exact cut and drives the
*current installed* C11 consumer owners:

* ``rawlsing_next.pre553_source_backed_c11_facade`` — governed projection and
  source-backed candidate construction;
* ``rawlsing_next.pre553_c11_ingest`` — the deciding C11 M01-M18 validator and
  atomic ingest;
* ``rawlsing_next.pre553_c11_repository`` — append-only exact-key repository.

It adds no empirical engine, no per-source branch and no replacement C11/I03/
Batch owner.  Original-source execution remains NOT_RUN and is not authorized
by this package.
"""
from __future__ import annotations

from .consumer import ConsumerReceipt, receive_fixture_release
from .ledger import build_ledger, ledger_row
from .provenance import current_owner_abi, imported_cut_manifest, verify_imported_cut
from .registry import UniversalSourceRegistry

__all__ = [
    "ConsumerReceipt",
    "receive_fixture_release",
    "build_ledger",
    "ledger_row",
    "UniversalSourceRegistry",
    "current_owner_abi",
    "imported_cut_manifest",
    "verify_imported_cut",
]
