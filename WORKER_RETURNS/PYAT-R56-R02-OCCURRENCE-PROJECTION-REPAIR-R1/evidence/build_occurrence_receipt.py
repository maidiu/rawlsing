from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEST = ROOT / "rawlsing_next/tests/test_universal_source_projection.py"
spec = importlib.util.spec_from_file_location("r56_r02_witness", TEST)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory(prefix="r56-r02-evidence-") as directory:
    path = Path(directory) / "s3_12x2.sav"
    rows = module.s3_rows(respondents=12, occasions=2)
    bundle = module.build_s3(path, rows)
    fact = module.run_repeated(bundle, module.domain_from_bundle(bundle))
    tuples = module.event_tuples(bundle)
    payload = {
        "schema": "R56_R02_OCCURRENCE_PROJECTION_RECEIPT@1",
        "source_sha256": bundle.source_sha256,
        "package_hash": bundle.package_hash,
        "projection_ref": bundle.projection.projection_identity_ref.as_dict(),
        "release_ref": bundle.release.release_ref.as_dict(),
        "event_count": len(tuples),
        "event_tuples": [list(row) for row in tuples],
        "i03_fact_ref": fact.ref.as_dict(),
        "i03_state": fact.typed_state,
        "i03_raw_denominator": fact.raw_denominator_support,
        "i03_raw_numerator": fact.raw_numerator_support,
        "i03_cell_count": len(fact.target_topology.get(
            "complete_cell_semantic_projection", [])),
        "administered_ids": list(bundle.administered_ids),
        "respondent_rows": [dict(row) for row in bundle.respondent_rows],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, default=dict))
