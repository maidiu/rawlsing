"""Build the P3 keyed-fixture integration example from the frozen P0 example."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.source_configuration.schema import SourceConfig, canonical_config_hash

ROOT = Path(__file__).resolve().parents[3]
P0_CONFIG = ROOT / "source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json"
OUT = ROOT / "source_pre553_validation/integration/examples/SRC09_q101_keyed_fixture.config.json"


def main() -> int:
    p0 = SourceConfig(json.loads(P0_CONFIG.read_text(encoding="utf-8")))
    document = deepcopy(p0.document)
    document["config_id"] = "R157-P3-INTEGRATION-SRC09-Q101-KEYED-FIXTURE"
    document["config_revision"] = 1
    document["respondents"]["source_native_key_slot"] = {"ordinal": 1, "name": "country"}
    document["respondents"]["row_identity_grade"] = "NONRESPONDENT_FIXTURE_KEY_WITNESS"
    document["supported_scope"]["scope_id"] = "SRC09-Q101-P3-KEYED-EXAMPLE"
    document["supported_scope"]["notes"] = [
        *document["supported_scope"]["notes"],
        "P3 integration example configures the source-native key slot to prove exact row-key witness binding on the nonrespondent fixture.",
    ]
    material = json.dumps({
        "config_id": document["config_id"],
        "fixture_source_sha256": document["binding"]["source_sha256"],
        "key_slot": document["respondents"]["source_native_key_slot"],
    }, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    document["authority"]["projection_identity_ref"] = ExactRef(
        "C11_SEMANTIC_PROJECTION",
        "urn:rawlsing:r157:p3:integration:src09-q101-keyed-fixture",
        digest,
    ).as_dict()
    config = SourceConfig(document)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "config": str(OUT.relative_to(ROOT)),
        "config_sha256": canonical_config_hash(config),
        "key_slot": document["respondents"]["source_native_key_slot"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
