"""Targetless same-root C12 for B share that A did not receive."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPS = ROOT / "deps"
os.environ.setdefault("M35_JOIN_E_RETURN", str(DEPS / "join_e"))
if str(DEPS / "m35") not in sys.path:
    sys.path.insert(0, str(DEPS / "m35"))
import install  # noqa: E402
install.install()

from bp2_joined.producer import _c9_summary  # noqa: E402
from historical_actor_producer import build_life  # noqa: E402
from joined.refusal import RefusalProduct  # noqa: E402
from r31j.scenarios import evaluated  # noqa: E402
import firstclass  # noqa: E402


class NoAccessProduct(RefusalProduct):
    """A targetless C12 root carrying B's share but no A admission/response."""

    def __init__(self, root, *, life, source, c8_binding, variant,
                 write_sidecar=False, branch_id="root", sidecar_document=None):
        self.no_access_path = Path(root) / "no_access.json"
        super().__init__(root, life=life, source=source, c8_binding=c8_binding,
                         variant=variant, write_sidecar=False,
                         branch_id=branch_id, sidecar_document=sidecar_document)

    def append_no_access(self, c9: dict) -> dict:
        body = {
            "gm01_source": self.source,
            "c8_state_digest": self.c8_binding["c8_state_digest"],
            "e1_event_hash": self.c8_binding["e1_event_hash"],
            "c9": c9,
            "target_id": "",
            "a_access_admitted": False,
            "a_response": None,
            "s35_status": "UNKNOWN_RECEIVABILITY",
            "s35_t": "NO_CHANGE",
            "native": False,
        }
        self._append_episode("root", "A", "GM01_NO_ACCESS",
                             self._world("root").clock, body)
        self._checkpoint("root", self._world("root").clock, self._world("root"))
        self.no_access_path.write_text(json.dumps({
            "schema": "SOROK_P1_NO_ACCESS@1",
            "source": self.source,
            "c8": self.c8_binding,
            "c9": c9,
            "variant": self.variant,
            "target_id": "",
            "a_access_admitted": False,
            "a_response": None,
            "native": False,
        }, indent=2, sort_keys=True) + "\n", encoding="utf8")
        return body

    def no_access_view(self) -> dict:
        return {
            "schema": "SOROK_P1_NO_ACCESS_VIEW@1",
            "source": self.source,
            "target_id": "",
            "a_access_admitted": False,
            "a_response": None,
            "a_tools": self._world("root").actor_state["A"]["tools_remaining"],
            "s35_status": "UNKNOWN_RECEIVABILITY",
            "s35_t": "NO_CHANGE",
            "c12": self.c12_verify("root"),
            "episodes": [row for row in self.store.episodes("root")
                          if row.get("kind") == "GM01_NO_ACCESS"],
            "native": False,
        }


def build_no_access(state_root) -> tuple[NoAccessProduct, dict]:
    """Create B SHARE -> C8 -> C9 denied, with a no-A-access C12 record."""
    state_root = Path(state_root).resolve()
    state_root.mkdir(parents=True, exist_ok=True)
    if (state_root / "product").exists() or (state_root / "bp2").exists():
        raise ValueError("ORPHAN_PRODUCT_ROOT")
    case = evaluated(share=True, e2=False)["case"]
    source = firstclass.validate_source(firstclass.source_from_case(case), case)
    producer = firstclass._producer(state_root / "bp2", source, "A_REPAIR_LONG")
    try:
        producer.stage_world()
        producer.stage_c8()
        producer.stage_out9()
        producer.stage_c9(material_access="denied")
        c9 = _c9_summary(producer, producer.pipeline)
        c8_binding = {
            "occurrence_id": producer.out9.occurrence_id,
            "journal_path": str(producer.env.journal_path),
            "key_path": str(producer.env.key_path),
            "key_id": producer.env.key_store.key_id,
            "anchor_log": str(producer.env.anchor.log_path),
            "anchor_watermark": str(producer.env.anchor.watermark_path),
            "c8_state_digest": producer.out9.readset["state_digest"],
            "e1_event_hash": producer.e1_event["hash"],
        }
        life = producer.historical_life
    finally:
        producer.close()
    product = NoAccessProduct(state_root / "product", life=life, source=source,
                              c8_binding=c8_binding, variant="A_REPAIR_LONG",
                              write_sidecar=True)
    body = product.append_no_access(c9)
    product.write_no_access_sidecar = True
    return product, {"source": source, "c8": c8_binding, "c9": c9, "body": body}


def open_no_access(state_root) -> tuple[NoAccessProduct, dict]:
    state_root = Path(state_root).resolve()
    sidecar = json.loads((state_root / "product" / "no_access.json").read_text())
    life = build_life(sidecar.get("variant", "A_REPAIR_LONG"))
    product = NoAccessProduct(state_root / "product", life=life,
                              source=sidecar["source"], c8_binding=sidecar["c8"],
                              variant=sidecar.get("variant", "A_REPAIR_LONG"),
                              write_sidecar=False, sidecar_document=None)
    return product, sidecar
