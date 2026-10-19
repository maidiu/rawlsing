#!/usr/bin/env python3
"""Exact NO_CHANGE receipt: disqualify the history witness, then take NO_CHANGE."""
from __future__ import annotations

import json
import sys
from pathlib import Path

run_dir = Path(sys.argv[1]).resolve()
return_root = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(run_dir))
import kernel  # noqa: E402
from test_heldout_actor_independence import seeded_past  # noqa: E402
from test_r4_i2_new_hostiles import observe  # noqa: E402

scene, state = seeded_past()
scene = observe(scene, history_observer="other_P")
modes = sorted({c.mode for c in kernel.eligible(scene, state, "later")})
candidate = kernel.eligible(scene, state, "later")[0]
proposal = kernel.propose(scene, state, "later", candidate.id)
grant = kernel.fixture_grant(proposal, "child")
before = state.hash()
returned = kernel.append_test_only(scene, state, proposal, grant)
audit = kernel.audit_no_change(scene, state, proposal, grant)
after = state.hash()
payload = dict(
    schema="SOROK_M2R4E_NO_CHANGE_RECEIPT@1",
    rule=kernel.RULE,
    rule_hash=kernel.RULE_HASH,
    modes=modes,
    selected_mode=candidate.mode,
    state_hash_before=before,
    state_hash_after=after,
    returned_state_is_same_object=returned is state,
    no_mutation=before == after,
    audit_hash=audit.hash,
    audit_state_before_hash=audit.state_before_hash,
    audit_matches_before=audit.state_before_hash == before,
    candidate_hash=proposal["candidate_hash"],
    source_preimage_count=len(proposal["source_preimages"]),
    relation_preimages_empty=not any(
        row[0].startswith("RELATION_") for row in proposal["source_preimages"]),
)
print(json.dumps(payload, sort_keys=True, indent=2))
