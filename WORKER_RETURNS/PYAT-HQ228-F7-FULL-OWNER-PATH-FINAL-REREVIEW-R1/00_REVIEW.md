# PYAT HQ228 — F7 FULL OWNER-PATH FINAL HOSTILE REREVIEW — R1

**DISPOSITION:** `F7_FULL_OWNER_PATH_PARTIAL__NAMED_DEFECT`  
**BRANCH:** `agent/reviewer-pyat-hq228-f7-full-owner-path-final-rereview-r1`  
**COMMISSION TIP:** `b4698896ae345af2984164cef775bb2bb25e875c`  
**CANDIDATE RETURN:** `d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1`  
**CODE-BEARING HEAD:** `61acee605d618ed4a0db11d893f6139593ae5780`  
**PRIOR REVIEW:** `2b8946bfef1506bae34b46a55833bad83bfb9d16`

## Conclusion

HQ227 materially closes the HQ226 outer-dispatch and nested-registry defects, but full construction provenance is still forgeable after construction.

Blocking finding:

`F7-RR-04F__LIVE_AUTHENTICATED_OWNER_STATE_IS_EXPOSED_AND_POSTCONSTRUCTION_REPLACEABLE`

`pre553_source_relations.py` creates closure-owned custody, but then binds its loader to the module-level `_load_owner_state`. That loader returns the live `_AuthenticatedResolverState` object itself. The state is only `@dataclass(frozen=True)`; Python frozen dataclasses can still be changed with `object.__setattr__`. HQ227's own hostile court already treats `object.__setattr__` on private semantic state as an admissible attack.

A hostile caller can therefore construct a valid source resolver and an exact empty victim resolver, call `_load_owner_state` for both, and transplant the source state's `by_ref`, `by_key`, `authority_snapshots`, relation hashes, authority hashes and `custody_hash` onto the victim state with `object.__setattr__`. The captured authenticated entrypoint subsequently loads that already-mutated state and has no independent fact proving the relation was constructor-validated into the victim resolver.

This defeats mandatory attack 7 at the actual custody layer. HQ227's injection witness mutates only `victim._by_ref`, which the repair intentionally no longer consumes; it does not attack the live sealed state exposed by `_load_owner_state`.

## Repairs that are real and should be conserved

- F7 requires exact concrete `SourceRelationResolver`.
- construction requires exact concrete `AuthorityRegistry`;
- nested lookup uses captured base `AuthorityRegistry.resolve_exact`;
- relation semantic hash and replay identity are checked at construction and positive use;
- nested `AuthoritySnapshot` semantic identity is pinned and rehashed at use;
- returned `RelationDecision` replay binds request, relation ref, authority ref/operation, owner custody hash, and nested snapshot content hash;
- F7 cross-binds nested snapshot content hash to the separately resolved outer `SOURCE_EQUIVALENCE` snapshot;
- the repaired HQ226 targeted break patches the F7 alias actually consumed;
- the lawful cross-universe productive fixture remains present.

The defect is specifically that the provenance-bearing state behind those checks is itself obtainable and replaceable.

## Runtime truth

No lawful exact repository runtime was available. The auxiliary container had Python 3.13.5, pytest 9.0.2 and git 2.47.3, but no worktree. HTTPS clone failed because `github.com` could not be resolved. The exact code-bearing head has no GitHub Actions workflow runs or commit statuses. Existing workflows do not expose an exact F7 court at this head, and the commission forbids workflow/production mutation.

No pytest pass claim is made. Because the commission permits a non-adoption result without runtime when an independently decisive source defect exists, this return uses the named-defect disposition rather than the missing-evidence fallback.

## Required repair

Keep the semantic/replay hardening, but make authenticated owner custody unavailable for caller mutation/replacement. A repaired hostile witness must attack the actual state used by the authenticated entrypoint and prove that an exact empty resolver cannot acquire another resolver's custodied relation/authority state after construction.

`F7_FULL_OWNER_PATH_PARTIAL__NAMED_DEFECT`
