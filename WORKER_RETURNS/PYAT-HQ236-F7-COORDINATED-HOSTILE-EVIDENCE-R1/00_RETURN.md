# PYAT HQ236 — F7 COORDINATED SUBSTITUTION INDEPENDENT HOSTILE EVIDENCE — R1

**DISPOSITION:** `F7_COORDINATED_CUSTODY_SUBSTITUTION_INDEPENDENTLY_REPRODUCED__ARCHITECTURE_DECISION_REQUIRED`
**LANE:** `agent/reviewer-pyat-hq236-f7-coordinated-hostile-evidence-r1`
**CANDIDATE BASE:** `c86ae335eaf70e82b5764c46754b16ca7e1587ce`
**WORKTREE:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq236-f7-coordinated-hostile`
**INTERPRETER:** governed CPython 3.11.3, sha256 `11d6f541…`, pytest 9.1.1 — no substitution
**MODE:** READ-ONLY / NO REPAIR / NO PRODUCTION OR COURT MUTATION / NO SELF-ADOPTION

---

## 1. Bottom line

HQ235 was **honest and correct in substance and understated in its own favour's disfavour**:
the coordinated substitution reproduces, and a **narrower** attack than HQ235 reported also
reproduces. HQ235 stated that "every single admitted reflection primitive is closed" and
that only a *coordinated replacement of all live anchors plus ledger rebind* still forges.
That is **falsified**: the exact lexical ledger-cell rebind — the named blocker
`F7-RR-04G` — still forges custody with **no live-container replacement at all**.

| # | Probe | Result |
|---|---|---|
| A | source resolver (own relation) | **POSITIVE** (AUTHORIZED / `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`) |
| B | empty victim resolver | **NEGATIVE** (`TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT`) |
| 1 | exact HQ234 single-cell rebind (source anchor fields copied) | **REFUSED** — confirms HQ235 |
| 2 | HQ235 "coordinated" replacement of `_by_ref` + `_by_key` + ledger rebind | **FORGED POSITIVE** |
| 3 | **narrower**: ledger rebind only, anchor fields = victim's own untouched live containers | **FORGED POSITIVE** |
| 4 | **narrowest**: same, payload `by_ref` only | **FORGED POSITIVE** |
| R | ledger restored | source POSITIVE again, victim NEGATIVE again |

A green test that asserts forgery is **evidence of an open defect, not an acceptance PASS**.

## 2. Exact receipt (attack 3 — the decisive one)

No live container was replaced (`id(victim._by_ref)` and `id(victim._by_key)` unchanged, both
still empty). The attacker constructed a state carrying the **source** payload
(`by_ref`, `authority_snapshots`, hashes, `custody_hash`) while setting
`sealed_by_ref_owner = victim._by_ref`, `sealed_by_key_owner = victim._by_key` and
`sealed_relations_fingerprint = _custody_relations_fingerprint(live_by_ref=victim._by_ref)`
(the public, trivially derivable fingerprint of the victim's own empty container), then
rebound the ledger cell. Observed victim decision:

- P07: `AUTHORIZED`, custody `d31cd8dd…c72bc8`, relation `…SourceUniverseRelation:sha256:33e5a745…`
- F7: `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`, reason `AUTHORIZED_ORDERED_PAIR_UNDER_BOUND_COMPARABILITY`, direction `INCREASE`

**Root cause.** The HQ235 gate authenticates the state's *anchor fields* against the live
containers, but the decision consumes `state.by_ref` / `state.by_key` /
`state.authority_snapshots` / `state.custody_hash` and **never binds that payload to the live
containers**. The anchor fields are attacker-supplied, so they are self-referential. The
docstring claim that `custody_hash` is "re-derived … at every decision" is not implemented.
The relation fingerprint is likewise non-load-bearing — the attacker computes the same public
function over the same untouched container.

## 3. Attack mechanics — what privilege is required

No production callable, module, class or method was monkeypatched; no accepted code was
rewritten; no positive authority was smuggled to the victim (control B stays negative). The
attacker needs only ordinary in-process reflection: walk
`authenticated_source_relation_decision.__closure__` to `_state_or_refuse`, walk its
`__closure__` to the `(weakref, state)` ledger tuple cell, assign `cell.cell_contents`, and
construct the public NamedTuple. Per the commission this was executed from an independent
script that does **not** reuse HQ235's witness helpers (`_hq235_victim_pair`,
`_hq235_reflection_seam`, or any `test_hq235_*` body); it reuses only the pre-existing lawful
fixtures `_adjudicated_resolver` / `_cross_universe_request` / `_run`, which the
309-added / 0-removed test diff proves unchanged.

## 4. Anchor implementation audit

- **Changes**: three new `_AuthenticatedResolverState` fields; `_custody_relations_fingerprint`;
  `_authenticate_owner_custody_anchor`, called from `_state_or_refuse` on every lookup.
- **Conserves**: P07 relation states/precedence, semantic content hashes and replay identity,
  authority kinds and snapshot pinning, source-composition law, temporal-comparability
  semantics, V554/V557/V558 semantics, and the accepted court bodies.
- **Registry**: correctly **not** anchored. Anchoring `_registry` by identity would fail after
  a lawful `resolver._registry = AuthorityRegistry((shadow,))` and convert an authorized
  decision into a refusal, breaking the accepted
  `test_hq227_exact_instance_registry_replacement_cannot_change_pinned_owner_snapshot`
  (verified passing at this tip). HQ235's choice here is independently endorsed.
- **Gap**: a narrower unaudited path still yields a false positive (attack 3/4 above).

## 5. Regression

Targeted courts under the governed interpreter: **228 passed / 0 failed / 0 errors**
(F7 163 + source-relations 24 + M1 ingress 14 + M1 dedup 27). All five lawful positive paths
pass, and the HQ227 registry-immunity test passes. HQ235's witness subset is 8/8 green,
including the forgery witness asserted `True`.

Broad regression (`rawlsing_next/tests/`, same 9 environmental exclusions) was rerun
independently; see `03_ANCHOR_IMPLEMENTATION_AND_REGRESSION_AUDIT.json` for the final numbers.

## 6. Proof limits — the narrowest justified statement

The demonstrated exploit is of **one specific implementation**. It is **not** a proof that
no pure-Python owner scheme could satisfy the invariant; that remains a reasoned reachability
argument (every Python-level container the owner can reach appears caller-reachable and
re-assignable; any value the owner re-derives the caller can recompute). No native extension,
IPC boundary, or OS handle was built, imported, or executed, so those designs are returned as
**design-level uncertainty**, not evaluated.

**Narrowest justified statement:** against candidate `c86ae335e`, the required non-forgeability
invariant is **not established**; the lexical ledger-cell rebind alone (specifically the
blocker `F7-RR-04G`) still mints custody for an empty resolver, without coordinated
live-anchor replacement; HQ235's "all single primitives closed" sub-claim is falsified; and
the universal impossibility claim remains unproven either way.

## 7. Disposition

`F7_COORDINATED_CUSTODY_SUBSTITUTION_INDEPENDENTLY_REPRODUCED__ARCHITECTURE_DECISION_REQUIRED`

No production, court, semantic or owner-authority change; no self-adoption; no repair.
