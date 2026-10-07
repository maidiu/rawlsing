# PYAT HQ231 — F7 SEALED OWNER-STATE CUSTODY REPAIR — R1 RETURN

**DISPOSITION:** `F7_SEALED_OWNER_STATE_CUSTODY_COMPLETE__READY_FOR_FINAL_REREVIEW`  
**BRANCH:** `agent/rabochii-pyat-hq231-f7-sealed-owner-state-custody-r1`  
**COMMISSION TIP:** `5d8794dff64e69d44e0605294a2672459ac8c70a`  
**EXACT STARTUP TIP:** `d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1`  
**BLOCKING REVIEW:** `agent/reviewer-pyat-hq228-f7-full-owner-path-final-rereview-r1 @ 11eb7488895665a15b4f820c57f41909e0201fef`  
**CODE-BEARING HEAD:** `62394d7ff817252d6d406c1e0ada96529697f5f2`

## Blocker closed

`F7-RR-04F__LIVE_AUTHENTICATED_OWNER_STATE_IS_EXPOSED_AND_POSTCONSTRUCTION_REPLACEABLE`

HQ227 kept trusted state in a closure-owned store but exported `_load_owner_state`, which returned the exact live frozen-dataclass state. HQ228 correctly showed that `object.__setattr__` could transplant valid source custody into an already-constructed victim.

HQ231 removes that live-state boundary rather than adding another outer type check.

## Sealed custody design

- `_load_owner_state`, `_seal_owner_state`, and `_make_owner_state_store` no longer exist as module-visible callables.
- `_AuthenticatedResolverState` is now a tuple-backed `NamedTuple`; its fields cannot be rewritten through HQ228's `object.__setattr__` primitive.
- every custody capsule carries a weak identity binding to the exact resolver that constructed it;
- the lexical owner ledger is a persistent immutable tuple of weak-owner/capsule pairs, not a mutable dictionary;
- construction is single-assignment: the lexical sealer rejects both a source capsule presented for a victim and any attempt to reseal an already-constructed victim;
- authenticated loading verifies that the ledger owner and capsule owner are the exact resolver before returning the capsule internally;
- the only supported custody inspection surface returns canonical detached JSON text, never the trusted capsule.

The hostile court goes beyond the original HQ228 surface: it reflects into the authenticated function, recovers the lexical loader, recovers the immutable ledger snapshot, and recovers the constructor sealer. `object.__setattr__` cannot mutate the capsule, the ledger cannot be item-assigned, source→victim reseal is refused by owner identity, and victim reseal is refused by single-assignment.

## P07/F7 semantic conservation

No P07 relation semantics were rewritten. Static comparison against the startup tip confirms byte-identical bodies for:

- `_owner_state_resolve_exact`;
- `_validate_positive_from_owner_state`;
- `_relation_decision_replay_identity`;
- `validate_relation_decision_replay_identity`;
- `_decide_from_owner_state`.

`rawlsing_next/pre553_temporal_comparability.py` is byte-identical to startup. F7 therefore continues to consume the adopted owner's `authenticated_source_relation_decision`; no relation semantics were duplicated into F7.

HQ227 registry/snapshot hardening remains intact: exact concrete `AuthorityRegistry`, captured base `resolve_exact`, constructor-pinned snapshots, semantic rehash/replay validation, decision replay binding, and F7 outer/nested snapshot cross-binding.

## Hostile court

Five HQ231 witnesses were added to the existing F7 court:

1. exact source→empty-victim attack through legacy visible fields plus proof that the old live accessor/sealer/store names are absent;
2. diagnostic inspection returns detached text; `object.__setattr__` cannot affect custody;
3. reflection-level recovery of loader, capsule, immutable ledger, and sealer cannot transplant source custody into an already-constructed victim;
4. inherited nested owner-method / registry-instance monkeypatch hardening remains load-bearing and positive;
5. same-fixture fail-capability: repaired victim is negative; replacing F7's actual authenticated seam with a deliberately transplantable pre-repair-style state path makes that same victim positive; undoing the break restores refusal.

Inherited HQ227 witnesses continue to cover registry subclass override, corrupt relation replay, wrong snapshot body under the same outer `AuthorityRef`, visible-map/registry replacement, nested helper monkeypatching, and lawful positive cross-universe service.

## HQD-216 productive adequacy

The repair does not solve authenticity by refusing production. The existing genuine constructor-admitted cross-universe positive witness remains in the court and the semantic decision machinery is unchanged. Same-universe, exact-zero, increase, decrease and lawful cross-universe positive paths remain source-visible.

## Runtime truth

No lawful repository execution surface was available in this session.

- machine/worktree: not established;
- auxiliary container execution attempts failed at the tool boundary before a repository runtime could be established;
- GitHub Actions runs for code head `62394d7ff817252d6d406c1e0ada96529697f5f2`: none;
- commit statuses for code head: none;
- workflow dispatch is not available on the connected GitHub tool surface.

Therefore **no pytest pass/fail claim is made**.

Exact rereview command surface, when available:

`PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=. python -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_pre553_temporal_comparability.py rawlsing_next/tests/test_pre553_source_relations.py rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`

Static accounting only:
- HQ227 expected F7 collection: 150;
- HQ231 adds 5 scalar witnesses, so expected F7 collection is 155 if prior parametrized collection is otherwise unchanged;
- source-relation court blob is unchanged;
- historical F7 qualification M1 court blob is unchanged (HQ219/HQ222 recorded 27 collected/passed there);
- no runtime aggregate is asserted.

## Write terrain

Production:
- `rawlsing_next/pre553_source_relations.py` only.

Court:
- `rawlsing_next/tests/test_pre553_temporal_comparability.py` only.

No `pre553_temporal_comparability.py` mutation. No other production/court mutation. No self-adoption.

`F7_SEALED_OWNER_STATE_CUSTODY_COMPLETE__READY_FOR_FINAL_REREVIEW`
