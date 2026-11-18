"""Mechanical timer/partial-receipt smoke; no native writer/build execution."""
from __future__ import annotations
import json, tempfile
from pathlib import Path
from timed_writer import Recorder, _span
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "progress.json"
    r = Recorder(p)
    with _span(r, "build_sourcefree_direct_i02"):
        for family in ("RespondentEvent", "RoutingEligibilityFact"):
            for _ in range(4):
                r.add_family(family, "_Sink.add", 0.000001, 1)
                r.tick(1)
    with _span(r, "_verify_emitted_physical_payloads"):
        pass
    with _span(r, "write_direct_estate_total"):
        pass
    r.mark("smoke_done")
    r.write()
    d = json.loads(p.read_text())
    assert d["events"] == 8
    assert "derived" in d
    assert d["derived"]["sink_add_inclusive"] >= 0
    assert d["derived"]["proof_residual_not_pure_sql"] >= 0
    print(json.dumps({"smoke": "PASS", "events": d["events"], "derived": d["derived"]}, sort_keys=True))
