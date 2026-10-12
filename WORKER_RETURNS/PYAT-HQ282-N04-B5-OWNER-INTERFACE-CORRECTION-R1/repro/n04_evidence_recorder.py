"""PYAT HQ282 N04 — evidence recorder for the B5 checkpoint correction.

Executes the checkpoint defect demonstration and method inventory,
and records the evidence as JSON.
Source-free: no raw data, no real subjects, no G0b/B5/Field-Forge.
"""

from __future__ import annotations

import json
import pathlib
import time

import rawlsing_next.pre553_n04_b5_checkpoint_interface_correction as n04


def main() -> dict:
    started = time.time()
    defect = n04.demonstrate_checkpoint_defect()
    inventory = n04.inventory_b5_state_changing_methods()
    elapsed = time.time() - started

    return {
        "contract_id": n04.N04_CONTRACT_ID,
        "defect_demonstration": defect,
        "method_inventory": {
            "b5_wrapped": list(inventory["b5_methods"]["WRAPPED"]),
            "b5_unwrapped": list(inventory["b5_methods"]["UNWRAPPED"]),
            "b5_partial": list(inventory["b5_methods"]["PARTIAL"]),
            "m2_wrapped": list(inventory["m2_methods"]["WRAPPED"]),
            "m2_unwrapped": list(inventory["m2_methods"]["UNWRAPPED"]),
            "checkpoint_defect": inventory["checkpoint_defect"],
            "identity_mismatch": inventory["identity_mismatch"],
        },
        "effects": dict(n04.effects()),
        "elapsed_seconds": round(elapsed, 3),
    }


if __name__ == "__main__":
    result = main()
    out = pathlib.Path(__file__).parent / "n04_evidence.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"evidence written to {out}")
    print(f"defect_reproduced: {result['defect_demonstration']['defect_reproduced']}")
    print(f"correction_works: {result['defect_demonstration']['correction_works']}")
    print(f"elapsed: {result['elapsed_seconds']}s")
