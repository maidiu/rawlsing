"""Trusted composition root. Import this before receiving any request."""

from fixture_owner import FixtureOwnerControl
from pv3_candidate import RequestAPI

from pathlib import Path
POLICY=Path(__file__).resolve().parents[1]/"runtime_root/fixture_owner/current.json"
owner = FixtureOwnerControl(policy_path=POLICY)
api = RequestAPI(owner.client(), owner._attest)


def install_test_profile(profile="BASELINE"):
    # Test/deployment control only. Deliberately absent from RequestAPI.
    global owner, api
    owner = FixtureOwnerControl(profile)
    api = RequestAPI(owner.client(), owner._attest)
    return api
