"""Run original cold executable with declared PV3 request adapter in a fresh PID."""

from pathlib import Path
import os, sys, types

R = Path(__file__).resolve().parents[1]
if os.environ.get("PV3_COLD_MODE", "REPAIRED") == "REPAIRED":
    import deployment as D
    import pv2_original_scope_register as OLD
    import json

    (R / "observations" / (sys.argv[3] + ".installation.json")).write_text(
        json.dumps(
            {
                "pid": os.getpid(),
                "installed_before_caller_fixture": True,
                "expected_root": D.owner.installation.expected_root,
                "register_root": D.owner.installation.register_root,
                "full_expected_preimage": json.loads(
                    D.owner.installation.expected_json
                ),
                "profile": D.owner.installation.profile,
            },
            indent=2,
        )
        + "\n"
    )
    proxy = types.ModuleType("pv2_original_scope_register")
    proxy.__dict__.update(OLD.__dict__)
    proxy.run_sourcefree_with_register = D.api.run_sourcefree_with_register

    def read(reg, report):
        try:
            return D.api.read_current_consumer_material(reg, report)
        except ValueError as e:
            return {"servable": False, "claim": str(e)}

    proxy.read_current_consumer_material = read
    sys.modules["pv2_original_scope_register"] = proxy
exec(
    compile((R / "frozen_pv2i/repro/cold_child.py").read_text(), str(__file__), "exec")
)
