"""Trusted fixture installation command, run before exposing RequestAPI.
Never called by request handlers or a replay. Existing withdrawals are retained.
"""

from pathlib import Path
import json, os
from fixture_owner import FixtureOwnerControl

R = Path(__file__).resolve().parents[1]
o = FixtureOwnerControl(
    policy_path=R / "runtime_root/fixture_owner/current.json", provision=True
)
(R / "observations/fixture_owner_installation.json").write_text(
    json.dumps(
        {
            "pid": os.getpid(),
            "expected_root": o.installation.expected_root,
            "register_root": o.installation.register_root,
            "profile": o.installation.profile,
            "before_request_and_source_execution": True,
            "expected": json.loads(o.installation.expected_json),
        },
        indent=2,
    )
    + "\n"
)
print("SEPARATELY_PROVISIONED_TEST_ONLY_OWNER", o.installation.expected_root)
