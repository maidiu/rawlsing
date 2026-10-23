import json
from pathlib import Path


def pytest_sessionfinish(session, exitstatus):
    for item in session.items:
        module = getattr(item, "module", None)
        observations = getattr(module, "OBSERVATIONS", None)
        if observations is not None:
            target = (
                Path(__file__).resolve().parents[1]
                / "outcomes"
                / "hostile_observations.json"
            )
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(observations, indent=2, sort_keys=True, default=str) + "\n",
                encoding="utf-8",
            )
            return
