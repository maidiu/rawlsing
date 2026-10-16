"""M03 finite selector custody and read-time validation; no response selection.

This validates the existing TEST_ONLY M01 first-event/claim contract. It neither
issues an owner grant nor implements a new memory-to-belief mechanism.
"""

import json
from dataclasses import asdict
from candidate import can008_candidate_rule as rule, owner_transitions as owner
from candidate.candidate_registry_fixture import canon, digest, parse_time

SCHEMA = "M03_CANONICAL_CLAIM_SELECTION@1"


def require(ok, code):
    from cell import Refusal

    if not ok:
        raise Refusal(code)


def source_basis(c):
    from cell import events, RULE_ID, VERSION

    first, _ = events()
    c.verify_grant()
    require(c.e1 == first and c.reg.verify_event(first), "CLAIM_SOURCE_EVENT_BINDING")
    require(
        c.ctx.verify() and c.ctx.actor_id == first.actor_scope,
        "CLAIM_CONTEXT_INTEGRITY",
    )
    expected_rule = rule.build_default_binding()
    require(c.binding == expected_rule, "CLAIM_RULE_BINDING")
    claim = owner.canonical_claim(
        first.actor_scope,
        "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL",
        "RESPECTED",
        first.effective_causal_time,
        first.actor_scope,
        [first.event_id],
    )
    require(
        c.ctx.claims.get(claim["claim_id"]) == claim, "CLAIM_CANONICAL_SOURCE_BINDING"
    )
    receipt = c.first_receipt
    require(isinstance(receipt, dict), "CLAIM_FIRST_RESPONSE_MISSING")
    require(
        receipt.get("receipt_hash")
        == rule._sha(
            rule._canon({k: v for k, v in receipt.items() if k != "receipt_hash"})
        ),
        "CLAIM_FIRST_RESPONSE_INTEGRITY",
    )
    expected_event = {
        k: getattr(first, k)
        for k in (
            "event_id",
            "event_hash",
            "issuer_authority_id",
            "issuer_authority_version",
            "actor_scope",
            "world_ref",
            "world_as_of",
            "effective_causal_time",
        )
    }
    expected_event["role"] = "PRECIPITATING_EVENT_STREAM"
    require(
        receipt.get("precipitating_event") == expected_event,
        "CLAIM_FIRST_RESPONSE_SOURCE",
    )
    require(
        (
            receipt.get("rule_id"),
            receipt.get("rule_version"),
            receipt.get("rule_content_hash"),
        )
        == (
            expected_rule.rule_id,
            expected_rule.rule_version,
            expected_rule.rule_content_hash,
        ),
        "CLAIM_FIRST_RESPONSE_RULE",
    )
    return dict(
        schema=SCHEMA,
        canonical_claim_ref=claim["claim_id"],
        canonical_claim_hash=claim["canonical_content_hash"],
        actor=first.actor_scope,
        world_ref=first.world_ref,
        world_as_of=first.world_as_of,
        source_event=asdict(first),
        owning_rule_id=expected_rule.rule_id,
        owning_rule_version=expected_rule.rule_version,
        owning_rule_hash=expected_rule.rule_content_hash,
        response_rule_id=RULE_ID,
        response_rule_version=VERSION,
        response_source_hash=c.grant,
        first_response_receipt_hash=receipt["receipt_hash"],
    )


def committed_binding(c):
    basis = source_basis(c)
    entries = c.journal.read_effects("FIRST_EVENT_COMPLETE")
    require(len(entries) == 1, "CLAIM_FIRST_COMMIT_REQUIRED")
    entry = entries[0]
    payload = entry["payload"]
    require(
        canon(payload.get("claim_selection_basis")) == canon(basis),
        "CLAIM_FIRST_COMMIT_SELECTION_BINDING",
    )
    require(
        payload["source_rule"] == c.grant
        and payload["state_hash"] == digest(payload["state"]),
        "CLAIM_FIRST_COMMIT_INTEGRITY",
    )
    require(
        entry["effective_causal_time"] == c.e1.effective_causal_time
        and entry["causal_parent_refs"] == [c.e1.event_id],
        "CLAIM_FIRST_COMMIT_TIME_SOURCE",
    )
    require(
        payload["state"]["claims"].get(basis["canonical_claim_ref"])
        == c.ctx.claims[basis["canonical_claim_ref"]],
        "CLAIM_FIRST_COMMIT_CANONICAL_STATE",
    )
    return dict(
        schema=SCHEMA,
        basis=basis,
        first_event_entry_hash=entry["entry_hash"],
        first_owner_state_hash=payload["state_hash"],
    )


def validate_binding(c):
    """Validate preserved commitment, not the untrusted outer selector hint."""
    from cell import Refusal

    try:
        if c._claim_selection_binding_json is None:
            require(
                c.claim_id is None
                and c.first_receipt is None
                and c.ctx.verify()
                and not c.ctx.claims
                and not c.ctx.memories
                and not c.reg._events
                and not c.journal.entries
                and not c.history.entries,
                "CLAIM_SELECTION_BINDING_MISSING",
            )
            return None
        require(
            isinstance(c._claim_selection_binding_json, str),
            "CLAIM_SELECTION_BINDING_TYPE",
        )
        binding = json.loads(c._claim_selection_binding_json)
        expected = committed_binding(c)
        require(canon(binding) == canon(expected), "CLAIM_SELECTION_CHECKPOINT_BINDING")
        return expected
    except Refusal:
        raise
    except (ValueError, TypeError, KeyError, AttributeError):
        raise Refusal("CLAIM_SELECTION_BINDING_MALFORMED") from None


def bind_committed(c):
    c._claim_selection_binding_json = canon(committed_binding(c))


def effect_provenance(c, effect, transition, cut, selected):
    require(
        parse_time(effect["effective_causal_time"]) <= cut,
        "CLAIM_EFFECT_AFTER_RESPONSE",
    )
    require(
        effect["effective_causal_time"] == c.e1.effective_causal_time,
        "CLAIM_EFFECT_SOURCE_TIME",
    )
    require(
        effect["actor_id"] == c.ctx.actor_id and effect["claim_ref"] == selected,
        "CLAIM_EFFECT_ACTOR_SCOPE",
    )
    require(
        (
            effect["owning_rule_id"],
            effect["owning_rule_version"],
            effect["owning_rule_hash"],
        )
        == (c.binding.rule_id, c.binding.rule_version, c.binding.rule_content_hash),
        "CLAIM_EFFECT_RULE",
    )
    require(
        tuple(effect["causal_parent_refs"]) == (c.e1.event_id,)
        and tuple(effect["actor_facing_basis_refs"])
        == (c.e1.event_id + ":" + c.e1.event_hash,),
        "CLAIM_EFFECT_SOURCE_BASIS",
    )
    require(
        transition["effect"] == effect
        and transition["actor_id"] == c.ctx.actor_id
        and transition["authority_hash"] == owner.PINS["ADP017_JSON"],
        "CLAIM_EFFECT_TRANSITION_BINDING",
    )
    fields = {k: v for k, v in effect.items() if k != "effect_id"}
    require(
        effect["effect_id"]
        == digest(
            [
                "EPISTEMIC_EFFECT",
                fields,
                transition["pre_state_hash"],
                transition["target_record_ref"],
            ]
        ),
        "CLAIM_EFFECT_IDENTITY",
    )
    original_record = {
        k: v
        for k, v in transition.items()
        if k not in ("transition_id", "post_state_set_hash")
    }
    require(
        transition["transition_id"] == digest(original_record),
        "CLAIM_TRANSITION_IDENTITY",
    )
    for parent in effect["causal_parent_refs"]:
        event = c.reg.event(parent)
        require(
            event is not None and parse_time(event["effective_causal_time"]) <= cut,
            "CLAIM_PARENT_AFTER_RESPONSE_OR_MISSING",
        )
    return dict(
        effect_id=effect["effect_id"],
        transition_id=transition["transition_id"],
        effective_causal_time=effect["effective_causal_time"],
    )


def validate_consumption(c, at):
    """Read actual selected claim/effects/permission at the response cut."""
    from cell import Refusal

    try:
        binding = validate_binding(c)
        require(binding is not None, "CLAIM_SELECTION_NOT_COMMITTED")
        native_ancestry = validate_native_ancestry(c)
        cut = parse_time(at)
        require(
            parse_time("1998-01-01T00:00:00Z")
            <= cut
            < parse_time("2001-01-01T00:00:00Z"),
            "CLAIM_RESPONSE_OUTSIDE_RULE_SCOPE",
        )
        selected = c.claim_id
        claim = c.ctx.claims.get(selected)
        require(claim is not None, "CLAIM_SELECTION_UNKNOWN")
        require(owner.verify_claim(claim), "CLAIM_SELECTION_CANONICAL_INTEGRITY")
        require(
            parse_time(claim["temporal_scope"]) <= cut, "CLAIM_SELECTION_AFTER_RESPONSE"
        )
        require(
            selected == binding["basis"]["canonical_claim_ref"],
            "CLAIM_SELECTION_SOURCE_SCOPE",
        )
        grant = c.ctx.emissions.get(selected)
        require(
            grant is not None
            and grant["event_id"] == c.e1.event_id
            and grant["event_hash"] == c.e1.event_hash
            and grant["rule_hash"] == c.binding.rule_content_hash
            and grant["stance_kind"] == "BELIEF",
            "CLAIM_EMISSION_SOURCE_BINDING",
        )
        active = [
            (k, v) for k, v in c.ctx.stances.items() if v["claim_ref"] == selected
        ]
        snapshot = c.ctx.state_sets.get(selected)
        permission = c.ctx.permissions.get(selected)
        transitions = [
            t
            for t in c.ctx.epistemic_transitions
            if t["effect"]["claim_ref"] == selected
        ]
        proofs = []
        if snapshot is None:
            require(
                not active and not transitions and permission is None,
                "CLAIM_STATE_MATERIAL_MISSING",
            )
            disposition = "BOUND_CANONICAL_CLAIM_NO_APPLIED_STANCE"
        else:
            require(
                snapshot["actor_id"] == c.ctx.actor_id
                and snapshot["claim_id"] == selected,
                "CLAIM_SNAPSHOT_ACTOR_SCOPE",
            )
            require(
                snapshot["current_state_hash"]
                == digest(
                    {k: v for k, v in snapshot.items() if k != "current_state_hash"}
                ),
                "CLAIM_SNAPSHOT_INTEGRITY",
            )
            require(
                tuple(snapshot["accessibility_basis_refs"])
                == (c.e1.event_id + ":" + c.e1.event_hash,),
                "CLAIM_ACCESS_SOURCE_BINDING",
            )
            require(
                permission is not None
                and permission["actor_id"] == c.ctx.actor_id
                and permission["claim_id"] == selected
                and permission["epistemic_state_hash"] == snapshot["current_state_hash"]
                and tuple(permission["basis_refs"])
                == (c.e1.event_id + ":" + c.e1.event_hash,),
                "CLAIM_CURRENT_PERMISSION_BINDING",
            )
            expected_permission = owner.first_person_permission(
                "BELIEF" if active else None, snapshot["current_claim_accessibility"]
            )
            require(
                permission["permission"] == expected_permission,
                "CLAIM_CURRENT_PERMISSION_VALUE",
            )
            require(
                len({v["effect_id"] for k, v in active}) == len(active)
                and all(k == v["effect_id"] for k, v in active),
                "CLAIM_DUPLICATE_EFFECT",
            )
            for key, effect in active:
                matches = [
                    t
                    for t in transitions
                    if t["effect"]["effect_id"] == effect["effect_id"]
                ]
                require(len(matches) == 1, "CLAIM_EFFECT_TRANSITION_REQUIRED")
                proofs.append(effect_provenance(c, effect, matches[0], cut, selected))
            last = [
                t
                for t in transitions
                if t["transition_id"] == snapshot["last_transition_ref"]
            ]
            require(
                len(last) == 1
                and last[0]["post_state_set_hash"] == snapshot["current_state_hash"],
                "CLAIM_LAST_TRANSITION_BINDING",
            )
            last_proof = effect_provenance(c, last[0]["effect"], last[0], cut, selected)
            if last_proof not in proofs:
                proofs.append(last_proof)
            disposition = "BOUND_CANONICAL_CLAIM_WITH_NATIVE_STATE"
        return dict(
            schema=SCHEMA,
            verified_binding=binding,
            selected_claim_ref=selected,
            response_as_of=at,
            canonical_claim_time=claim["temporal_scope"],
            actual_effect_provenance=proofs,
            native_owner_ancestry=native_ancestry,
            disposition=disposition,
            production_authority="NOT_ISSUED_TEST_ONLY",
        )
    except Refusal:
        raise
    except (ValueError, TypeError, KeyError, AttributeError):
        raise Refusal("CLAIM_CONSUMPTION_PROVENANCE_MALFORMED") from None


# M05: reconstruction through original native owners, not digest self-attestation.
def _native_event(c, event_id):
    raw = c.reg.event(event_id)
    require(raw is not None, 'CLAIM_ANCESTRY_EVENT_MISSING')
    event = type(c.e1)(**raw)
    require(c.reg.verify_event(event), 'CLAIM_ANCESTRY_EVENT_INTEGRITY')
    return event


def _copy_native(c, state):
    ctx = owner.FixtureOwnerState(c.reg)
    ctx.restore(dict(state=state, pending={}))
    return ctx


def _replay_owner(c, start, target):
    """Reproduce an exact native store from a proven predecessor.

    The original ADP017 receipt omits the accessibility argument but commits its
    resulting snapshot hash. Enumerate only the three original API categories
    and require byte-equivalent native receipts; never derive new semantics.
    ADP016's noninvertible formation inputs are separately retained and replayed.
    Neither witness is sufficient without original native validation/results.
    """
    import json
    from copy import deepcopy
    require(set(start) == set(target), 'CLAIM_ANCESTRY_STATE_SCHEMA')
    for family in ('memories', 'memory_transitions', 'claims', 'emissions'):
        require(all(k in target[family] and canon(v) == canon(target[family][k])
                    for k, v in start[family].items()), 'CLAIM_ANCESTRY_PREFIX_' + family.upper())
    n = len(start['epistemic_transitions'])
    require(canon(target['epistemic_transitions'][:n]) == canon(start['epistemic_transitions']),
            'CLAIM_ANCESTRY_TRANSITION_PREFIX')
    require(len(target['epistemic_transitions']) >= n, 'CLAIM_ANCESTRY_TRUNCATED')
    claims = tuple(sorted(set(target['claims']) - set(start['claims'])))
    memories = tuple(sorted(set(target['memories']) - set(start['memories'])))
    require(set(target['emissions']) == set(target['claims']), 'CLAIM_ANCESTRY_EMISSION_SET')
    visited = set()

    def walk(ctx, pending_claims, pending_memories):
        key = ctx.state_hash
        if key in visited:
            return None
        visited.add(key)
        index = len(ctx.epistemic_transitions)
        if not pending_claims and not pending_memories and index == len(target['epistemic_transitions']):
            return [] if canon(ctx.data()) == canon(target) else None
        candidates = []
        if index < len(target['epistemic_transitions']):
            transition = target['epistemic_transitions'][index]
            if transition['pre_state_hash'] == ctx.state_hash:
                effect = transition['effect']
                for access in ('CLAIM_ACCESSIBLE', 'CLAIM_INACCESSIBLE', 'CLAIM_ACCESS_UNKNOWN'):
                    nxt = _copy_native(c, ctx.data())
                    args = {k: deepcopy(v) for k, v in effect.items() if k != 'effect_id'}
                    args.update(context=nxt, pre_state_hash=ctx.state_hash,
                                target_record_ref=transition['target_record_ref'], claim_accessibility=access)
                    result = owner.adp017_apply_epistemic_effect(**args)
                    if (result['decision_state'] == 'APPLIED_EPISTEMIC_TRANSITION'
                            and canon(result['transition']) == canon(transition)):
                        candidates.append((nxt, pending_claims, pending_memories,
                            dict(kind='ADP017', pre_state_hash=ctx.state_hash, post_state_hash=nxt.state_hash,
                                 transition_id=transition['transition_id'], native_result=result)))
        for mid in pending_memories:
            memory = target['memories'][mid]
            transition = target['memory_transitions'].get(memory['last_transition_id'])
            if transition is None or transition['pre_state_hash'] != ctx.state_hash:
                continue
            witness = c._native_formation_inputs.get(transition['memory_transition_id'])
            if not isinstance(witness, dict):
                continue
            args = deepcopy(witness)
            event = _native_event(c, args['basis_event']['event_id'])
            if canon(args['basis_event']) != canon(asdict(event)):
                continue
            args['basis_event'] = event
            nxt = _copy_native(c, ctx.data()); args['context'] = nxt
            try:
                proposal = owner.adp016_form_causal_trace(**args)
                if (canon(proposal['memory']) != canon(memory)
                        or canon(proposal['transition']) != canon(transition)):
                    continue
                result = nxt.commit_memory(proposal)
            except owner.OwnerTransitionError:
                continue
            candidates.append((nxt, pending_claims, tuple(k for k in pending_memories if k != mid),
                dict(kind='ADP016', pre_state_hash=ctx.state_hash, post_state_hash=nxt.state_hash,
                     transition_id=transition['memory_transition_id'], native_proposal=proposal, native_result=result)))
        for ref in pending_claims:
            claim = target['claims'][ref]
            emission = target['emissions'].get(ref)
            if not isinstance(emission, dict):
                continue
            nxt = _copy_native(c, ctx.data())
            try:
                event = _native_event(c, emission['event_id'])
                actual_ref = nxt.bind_claim(claim, event, stance_kind=emission['stance_kind'])
                if actual_ref != ref or canon(nxt.emissions[ref]) != canon(emission):
                    continue
            except owner.OwnerTransitionError:
                continue
            candidates.append((nxt, tuple(k for k in pending_claims if k != ref), pending_memories,
                dict(kind='CANONICAL_CLAIM_BIND', pre_state_hash=ctx.state_hash,
                     post_state_hash=nxt.state_hash, claim_ref=ref, event_id=event.event_id, event_hash=event.event_hash)))
        for nxt, pc, pm, proof in candidates:
            suffix = walk(nxt, pc, pm)
            if suffix is not None:
                return [proof] + suffix
        return None

    result = walk(_copy_native(c, start), claims, memories)
    require(result is not None, 'CLAIM_NATIVE_OWNER_TRAJECTORY_INVALID')
    return result


def validate_native_ancestry(c):
    """Anchor in the actual first journal, then prove terminal complete state.

    Replaying uses isolated original owner instances. Actual source owner,
    registry, journals, permission records and read log are never mutated.
    A valid complete checkpoint may replay; hybrid snapshots may not.
    """
    from cell import Refusal
    try:
        entries = c.journal.read_effects()
        first = [e for e in entries if e['kind'] == 'FIRST_EVENT_COMPLETE']
        require(len(first) == 1, 'CLAIM_ANCESTRY_FIRST_COMMIT_REQUIRED')
        entry = first[0]; state = entry['payload']['state']
        empty = owner.FixtureOwnerState(c.reg).data()
        require(digest(empty) == c.initial, 'CLAIM_ANCESTRY_NATIVE_ROOT')
        require(state['actor_id'] == c.ctx.actor_id, 'CLAIM_ANCESTRY_ACTOR')
        basis = source_basis(c)
        require(set(state['claims']) == {basis['canonical_claim_ref']}, 'CLAIM_ANCESTRY_FIRST_CLAIM_SET')
        first_steps = _replay_owner(c, empty, state)
        initial_rows = [e for e in entries[:entry['seq']] if e['kind'] in ('ADP016_COMMIT', 'ADP017_COMMIT')]
        native_steps = [s for s in first_steps if s['kind'] in ('ADP016', 'ADP017')]
        require(len(initial_rows) == len(native_steps), 'CLAIM_ANCESTRY_FIRST_JOURNAL_COVERAGE')
        for row, step in zip(initial_rows, native_steps):
            p = row['payload']
            require(row['kind'] == step['kind'] + '_COMMIT'
                    and row['effective_causal_time'] == c.e1.effective_causal_time
                    and row['causal_parent_refs'] == [c.e1.event_id]
                    and p['before'] == step['pre_state_hash'] and p['after'] == step['post_state_hash'],
                    'CLAIM_ANCESTRY_FIRST_NATIVE_PRESTATE')
            if step['kind'] == 'ADP016':
                require(canon(p['proposal']) == canon(step['native_proposal'])
                        and canon(p['commit']) == canon(step['native_result']), 'CLAIM_ANCESTRY_FIRST_MEMORY_RECEIPT')
            else:
                require(canon(p['result']) == canon(step['native_result']), 'CLAIM_ANCESTRY_FIRST_EPISTEMIC_RECEIPT')
        current = c.ctx.data()
        later_steps = _replay_owner(c, state, current)
        terminal = {}
        for t in current['epistemic_transitions']:
            terminal[t['effect']['claim_ref']] = t['transition_id']
        for ref, tid in terminal.items():
            require(current['state_sets'][ref]['last_transition_ref'] == tid,
                    'CLAIM_ANCESTRY_TERMINAL_TRANSITION')
        def portable(steps):
            return [{k: v for k, v in s.items() if k not in ('native_result', 'native_proposal')} for s in steps]
        return dict(schema='M05_NATIVE_OWNER_ANCESTRY@1', rooted_in_first_journal=True,
                    root_state_hash=digest(empty), first_event_entry_hash=entry['entry_hash'],
                    first_owner_state_hash=digest(state), current_owner_state_hash=digest(current),
                    first_steps=portable(first_steps), later_steps=portable(later_steps),
                    terminal_transition_refs=terminal,
                    authority='ORIGINAL_SOURCEFREE_NATIVE_REPLAY; NOT_A_PRODUCTION_SIGNER')
    except Refusal:
        raise
    except (ValueError, TypeError, KeyError, AttributeError, IndexError, owner.OwnerTransitionError):
        raise Refusal('CLAIM_NATIVE_OWNER_ANCESTRY_MALFORMED') from None
