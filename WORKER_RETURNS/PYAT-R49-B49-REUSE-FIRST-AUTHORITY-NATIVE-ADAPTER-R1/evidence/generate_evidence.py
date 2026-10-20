#!/usr/bin/env python3
"""Generate the B49 source-rule, administered-U and manifest evidence artifacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
OUT = ROOT / "evidence"
OUT.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "WORKER_RETURNS" / "PYAT-R49-B49-REUSE-FIRST-AUTHORITY-NATIVE-ADAPTER-R1" / "corpus"))

import pandas as pd

from rawlsing_next.pre553_inherited_source_rules import (
    SourceAuthorityCorpus,
    all35_coverage_ledger,
    select_source_rules,
)
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture,
    build_projection_catalog,
    build_test_only_workload,
    execute_test_only_workload,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence, PhysicalVariable
from rawlsing_next.pre553_source_native_preimage_adapter import (
    InstrumentInventory,
    NativeInstrumentVariable,
    build_authority_set,
    materialize_native_preimages,
)

CORPUS = ROOT / "corpus" / "source_authority_corpus.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def main() -> int:
    corpus = SourceAuthorityCorpus.from_document(json.loads(CORPUS.read_text()))
    (OUT / "all35_coverage_ledger.json").write_text(
        json.dumps(all35_coverage_ledger(corpus), indent=2, sort_keys=True) + "\n"
    )
    package = select_source_rules(corpus, family="LiTS", wave="I", as_of="2026-10-20")
    (OUT / "selected_rule_package_lits_i.json").write_text(
        json.dumps(package.as_dict(), indent=2, sort_keys=True) + "\n"
    )

    columns = ("q301_2", "q301_7", "country", "w1", "id")
    rows = ((1, 2, "US", 1, "S1"), (3, 4, "US", 2, "S2"), (5, None, "US", 3, "S3"))
    variables = tuple(
        PhysicalVariable(i, name, None, f"label-{name}", {}, (), {}, {})
        for i, name in enumerate(columns, 1)
    )
    incidence = PhysicalSourceIncidence(
        source_sha256=package.source.declared_sha256,
        source_format="SYNTHETIC",
        row_count=3,
        variables=variables,
        reader_configuration={"fixture": "b49-synthetic"},
        file_metadata={"fixture": "b49-synthetic"},
        _frame=pd.DataFrame(rows, columns=columns),
    )
    inventory = InstrumentInventory(
        source_id="27",
        source_sha256=package.source.declared_sha256,
        variables=tuple(
            NativeInstrumentVariable(name, i, (), "TEST_ONLY_REPRESENTATION")
            for i, name in enumerate(columns, 1)
        ),
        respondent_count=3,
        id_variable="id",
        country_variable="country",
        weight_variable="w1",
        country_scope=("US",),
    )
    authorities = build_authority_set(source=package.source, as_of="2026-10-20")
    bundle = materialize_native_preimages(
        package=package,
        inventory=inventory,
        incidence=incidence,
        authorities=authorities,
        as_of="2026-10-20",
    )
    (OUT / "administered_u_ledger.json").write_text(json.dumps({
        "schema": bundle.schema,
        "source_sha256": bundle.source_sha256,
        "package_hash": bundle.package_hash,
        "inventory_hash": bundle.inventory_hash,
        "bundle_hash": bundle.bundle_hash,
        "administered": [x.as_dict() for x in bundle.administered],
        "held": [x.as_dict() for x in bundle.held],
        "excluded": [x.as_dict() for x in bundle.excluded],
        "unknown": [x.as_dict() for x in bundle.unknown],
    }, indent=2, sort_keys=True) + "\n")

    operation = OperationFixture(
        fixture_id="B49-EVIDENCE-1", target_variable_code="q301_2", response_value="1"
    )
    catalog, request = build_projection_catalog(
        bundle=bundle, operation=operation, as_of="2026-10-20"
    )
    issued = build_test_only_workload(
        bundle=bundle,
        projection=bundle.projection,
        catalog=catalog,
        request=request,
        operation=operation,
        as_of="2026-10-20",
        host="local-b49",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    result = execute_test_only_workload(
        issued=issued,
        source_factory=lambda ref: incidence,
        host="local-b49",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    fact = result.native_outputs[0].facts[0]
    fields = dict(fact.semantic_fields)
    (OUT / "native_execution_receipt.json").write_text(json.dumps({
        "schema": "B49_NATIVE_EXECUTION_RECEIPT@1.0.0",
        "scope": result.scope,
        "envelope_sha256": result.envelope_sha256,
        "manifest_units": len(result.manifest.units),
        "receipts": [getattr(r, "state", None) for r in result.receipts],
        "fact_ref": fact.ref.as_dict(),
        "fact_typed_state": fact.typed_state,
        "raw_numerator_support": fields.get("raw_numerator_support"),
        "raw_denominator_support": fields.get("raw_denominator_support"),
        "execution_detail": fields.get("execution_detail"),
        "prospective_original_e_pre": None,
        "original_35_scientific_product": None,
    }, indent=2, sort_keys=True) + "\n")

    modules = (
        "rawlsing_next/pre553_inherited_source_rules.py",
        "rawlsing_next/pre553_source_native_preimage_adapter.py",
        "rawlsing_next/pre553_native_workload_binding.py",
        "rawlsing_next/pre553_issued_workload.py",
    )
    manifest = []
    for rel in modules:
        path = REPO / rel
        manifest.append({
            "path": rel,
            "sha256": sha256(path),
            "git_blob_sha1": blob(path),
            "bytes": path.stat().st_size,
        })
    (OUT / "source_manifest.json").write_text(json.dumps({
        "schema": "B49_SOURCE_MANIFEST@1.0.0",
        "u43_staged_blob_expected": "31e84f49d624f5524906e9e7839d2873106f8249",
        "modules": manifest,
        "corpus_sha256": sha256(CORPUS),
        "h48_commit": "359ddabc89d78ceb4c8fa45561588ee4cad7dd11",
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "all35_rows": 35,
        "selected": len(package.selected),
        "administered": len(bundle.administered),
        "fact_state": fact.typed_state,
        "fact_numerator": fields.get("raw_numerator_support"),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
