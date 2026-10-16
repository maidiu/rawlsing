#!/usr/bin/env python3
"""Precommit the independently authored original-scope register.

Writes `freezes/01_PRECOMMITTED_ORIGINAL_EXPECTED_SET_AND_SOURCE_IDENTITY.json`
BEFORE any accepted-owner execution, so a candidate caller cannot relabel,
rekey, suppress or cherry-pick by supplying its own E.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RETURN / 'repro'))

import pv2_original_scope_register as PV2  # noqa: E402


def main() -> int:
    register = PV2.author_sourcefree_original_scope_register()
    binding = register.binding()
    payload = dict(
        schema=PV2.SCHEMA, origin=PV2.ORIGIN,
        source_kind=register.source_kind,
        source_artifact_identity=register.source_artifact_identity,
        expected_consumer=register.expected_consumer,
        fixture_use_grant=register.fixture_use_grant.binding(),
        obligation_multiset=sorted(
            [list(k), n] for k, n in register.obligation_multiset.items()),
        runnable_multiset=sorted(
            [list(k), n] for k, n in register.runnable_multiset.items()),
        held_multiset=sorted([list(k), n] for k, n in register.held_multiset.items()),
        register_binding=binding,
        committed_root=register.committed_root,
        source_inventory_root=register.source_inventory_root,
        obligations=[o.binding() for o in sorted(
            register.obligations, key=lambda o: o.obligation_key)],
    )
    # Self-consistency before writing the freeze: the committed root must
    # reproduce exactly from the independently authored binding.
    if PV2.frozen_root_from_payload(binding) != register.committed_root:
        raise SystemExit('PRECOMMIT_ROOT_UNSTABLE')
    if payload['committed_root'] != PV2.frozen_root_from_payload(binding):
        raise SystemExit('PRECOMMIT_PAYLOAD_ROOT_UNSTABLE')
    target = RETURN / 'freezes' / '01_PRECOMMITTED_ORIGINAL_EXPECTED_SET_AND_SOURCE_IDENTITY.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
    obligations = payload['obligations']
    print(json.dumps(dict(
        frozen=str(target), committed_root=register.committed_root,
        source_inventory_root=register.source_inventory_root,
        obligations=len(obligations),
        runnable=sum(1 for o in obligations if o['state'] == 'RUNNABLE'),
        held=sum(1 for o in obligations if o['state'] != 'RUNNABLE'),
        held_scopes=[o['slot'] for o in obligations if o['state'] != 'RUNNABLE'],
    ), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
