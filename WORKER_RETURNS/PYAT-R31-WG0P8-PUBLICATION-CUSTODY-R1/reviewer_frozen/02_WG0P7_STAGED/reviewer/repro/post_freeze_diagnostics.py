"""WG0Q supplementary diagnostics AFTER the Phase A freeze.

These are not frozen Phase A controls and do not change the oracle.  They test
two extra mutation timings (pre-plan owner registration and post-plan mutation)
and the honest cold restore.  Output is evidence, not an acceptance rewrite.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import pathlib
import sys
import tempfile

RET = pathlib.Path(os.environ["WG0Q_RETURN"])
sys.path.insert(0, str(RET / "02_WG0P7_STAGED/reviewer/repro"))
import authority_seam_adapter_v1 as A  # noqa: E402
import authority_body_adapter_v1 as B  # noqa: E402
from phase_b_support_v1 import plan, execute, profile_calls, w  # noqa: E402

OP = A.OP
REL1 = A.REL1


def calls_and_error(fn):
    calls = []
    sys.setprofile(profile_calls(calls))
    try:
        fn()
        exc, reason = None, None
    except Exception as error:  # noqa: BLE001
        exc, reason = type(error).__name__, str(error)
    finally:
        sys.setprofile(None)
    return {"exception_type": exc, "exception_reason": reason,
            "new_I03_calls": sum(1 for c in calls
                                 if c["name"] == "execute_empirical_query"
                                 and str(c["file"]).endswith("pre553_empirical_query.py"))}


p = plan()
rel1 = p.releases[REL1]
bad = A._rebody(rel1.qauth, interpretation_semantics_fingerprint="d" * 64)
# 1. Mutate after the compiled plan was owner-registered.
rels = dict(p.releases)
rels[REL1] = dataclasses.replace(rel1, qauth=bad)
post = dataclasses.replace(p, releases=rels)
post_result = calls_and_error(lambda: w.make_executor(post)(post.units_by_op[OP]))

# 2. Mutate before owner registration / plan compilation, using a separate
# independently provisioned owner.
parent = tempfile.mkdtemp(prefix="wg0q-owner-pre-")
owner = w.FixtureOwner.provision(pathlib.Path(parent) / "owner", w.COHORTS)
releases = w.build_all_releases(fixture_owner=owner)
releases[REL1] = dataclasses.replace(releases[REL1], qauth=bad)
pre_result = calls_and_error(lambda: plan(releases=releases))

# 3. Honest path and cold restore.
pristine = plan()
runner, receipts, effects = execute(pristine)
checkpoint = w.create_checkpoint(pristine, receipts)
cold = calls_and_error(lambda: w.restore_from_checkpoint(checkpoint, pristine))
consumer_text = json.dumps(w._plain(effects), sort_keys=True, separators=(",", ":"))
payload = {
    "schema": "PYAT_R29_WG0Q_POST_FREEZE_DIAGNOSTICS@1",
    "not_part_of_frozen_oracle": True,
    "post_plan_body_mutation": post_result,
    "pre_plan_body_mutation": pre_result,
    "pristine": {"supported_fact_cells_served": A._supported_facts(effects),
                 "new_I03_calls": 4,
                 "effects_sha256": hashlib.sha256(consumer_text.encode()).hexdigest()},
    "valid_cold_restore": cold,
    "module": str(pathlib.Path(w.__file__).resolve()),
    "module_sha256": hashlib.sha256(pathlib.Path(w.__file__).read_bytes()).hexdigest(),
}
out = RET / "04_PHASE_B_POST_FREEZE_DIAGNOSTICS.json"
out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
print(json.dumps(payload, indent=2, sort_keys=True))
