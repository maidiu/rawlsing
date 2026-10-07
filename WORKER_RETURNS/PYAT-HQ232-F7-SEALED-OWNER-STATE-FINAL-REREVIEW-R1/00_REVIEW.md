# 00 — HQ232 F7 SEALED OWNER-STATE CUSTODY — FINAL HOSTILE REREVIEW — R1

**Role:** independent hostile reviewer. No production mutation. No repair. No self-adoption. No merge.
**Branch:** `agent/reviewer-pyat-hq232-f7-sealed-owner-state-final-rereview-r1`
**Review tip:** `b030d870abdacf20d689d17ef6828d4e26dfedd6` (verified equal to the pushed review branch before work)
**Candidate code-bearing head:** `62394d7ff817252d6d406c1e0ada96529697f5f2`
**Candidate return head:** `d6734e0150e91a60965e7db244ed2ef519ec831c`
**HQ234 supplemental hostile lead:** `282089225ebf1854736a16b4204599d26fc62528` — read in full as mandatory review terrain

## DISPOSITION

`F7_SEALED_CUSTODY_PARTIAL__NAMED_DEFECT`

**Blocker: `F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE` — REPRODUCED.**

I reproduce the HQ234 lead exactly, against the exact commissioned candidate, without monkeypatching production. The lexical custody ledger is held in a **closure cell**, and in CPython 3.11.3 `cell.cell_contents` is writable. A caller can therefore rebind the cell so that the victim resolver maps to a forged state that carries the **source resolver's** custody material bound to the victim's `owner_ref`. The victim then passes `_state_or_refuse` and reaches `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` on the **source's** relation.

The candidate's own court proves only that the retrieved **tuple** refuses item assignment. That proof is true and irrelevant: the defeat is not tuple mutability, it is **rebinding the cell that holds the tuple**. The candidate's fail-capability restores a *different* transplantable path and therefore cannot see this.

This is a **bounded provenance/custody implementation defect**, not a semantic or architectural conflict. I classify it as such deliberately: the relation semantics, registry provenance conservation and productive paths are all intact (section C–F below), all 155 F7 court tests and 24 source-relation court tests pass, and the attack requires in-process Python reflection. The defect is that the custody **owner-binding** is rebindable, while the custody **content** it hands over is genuinely valid.

## 1. The reproduction, exactly

Attack script committed verbatim at `artifacts/hq232_rr04g_attack.py`; controls at `artifacts/hq232_rr04g_controls.py`; custody proof at `artifacts/hq232_rr04g_custody_proof.py`.

### Step-by-step result

| Step | HQ234 lead instruction | Observed |
|---|---|---|
| 1 | source resolver A with genuine positive authorized relation | constructed via the court's own `_adjudicated_resolver`; `_registry` shared |
| 2 | victim resolver B without that relation, same registry | `SourceRelationResolver(relations=(), authority_registry=source._registry)`; `victim._registry is source._registry` → True |
| 3 | recover `_state_or_refuse` via `authenticated_source_relation_decision.__closure__` | recovered; `__name__ == "_state_or_refuse"` |
| 4 | recover the closure cell whose `cell_contents` is the lexical `entries` tuple | recovered; `ledger_len_before = 2`, `ledger_has_source = True`, `ledger_has_victim = True` |
| 5 | obtain `source_state` and `victim_state` | `source_state.owner_ref() is source` → True; `victim_state.owner_ref() is victim` → True; source `by_ref` has 1 entry, victim has 0 |
| 6 | forge a state carrying source custody bound to `victim_state.owner_ref` | constructed; `owner_ref() is victim` → True and `by_ref is source_state.by_ref` → True |
| 7 | rebind `entries_cell.cell_contents` so victim maps to the forged state | `cell_contents` assignment **succeeded**; `loader(victim) is forged_state` → True |
| 8 | invoke the normal authenticated F7 path for victim | **`TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`, reason `AUTHORIZED_ORDERED_PAIR_UNDER_BOUND_COMPARABILITY`, `comparability_status COMPARABLE`, `direction_claim INCREASE`** |

### Baseline (before the rebind) — the control that makes the result meaningful

```
source: TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / AUTHORIZED_ORDERED_PAIR_UNDER_BOUND_COMPARABILITY / COMPARABLE
victim: TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT / SOURCE_EQUIVALENCE_AUTHORITY_NOT_POSITIVE / NOT_COMPARABLE
```

The victim is correctly refused before the attack and becomes fully positive after it. The only change is the closure cell binding.

### The victim's own owner decision, before and after

This is the sharpest form of the finding — not merely an F7 receipt, but the P07 owner decision itself:

```
before:  source decision AUTHORIZED  (custody d31cd8dd…)
         victim decision REFUSED — "exact SourceUniverseRelation unavailable from authenticated owner custody"
after:   source decision AUTHORIZED  (custody d31cd8dd…)
         victim decision AUTHORIZED  (custody d31cd8dd…)
         victim_decision_carries_source_custody_hash = True
         victim_decision_binds_source_relation = True   (identical relation ref)
```

**The victim's positive decision carries the source's custody hash and the source's relation ref.** The victim resolver received source resolver custody while satisfying every owner-ref check.

## 2. Why it works — the three load-bearing weaknesses

### W1 — the custody ledger lives in a rebindable closure cell

```
entries: tuple[tuple[Any, _AuthenticatedResolverState], ...] = ()
```

`entries` is a `nonlocal` binding, so `_seal` mutates it. Python exposes that binding as a cell that any caller can reach through `loader.__closure__`, and CPython 3.11.3 permits `cell.cell_contents = ...`. The module's own comment says *"Construction is the only mutation point: _seal rebinds the tuple; no caller can mutate a retrieved ledger object in place"* — that is true of the **retrieved object** and false of the **cell**. The court's assertion `ledger[0] = ledger[-1]` → `TypeError` tests exactly the property that was never at risk.

### W2 — `_AuthenticatedResolverState` is caller-constructible and never re-bound to its owner

`_AuthenticatedResolverState` is a module-level `NamedTuple`, so any caller may construct one. This is not incidental: the candidate's own fail-capability test constructs one at `test_pre553_temporal_comparability.py:2362`, which concedes constructibility. The guard in `_state_or_refuse` is

```
if state.owner_ref() is not resolver: raise ...
```

and `owner_ref` is the *first field of the state itself*. It is therefore not evidence of custody — it is a self-declared field the forger sets. Both the ledger weakref and the state's own `owner_ref` point at the victim, so both checks pass.

### W3 — `custody_hash` is a transcription, not an owner-binding invariant

`custody_hash` is computed once in the constructor (`:966-985`) and thereafter only:

- copied into each `RelationDecision` (`:784`, `:800`)
- format-checked (`:694-697`) and folded into the replay identity (`:718`)

**No code path re-derives the custody hash from the resolver that actually owns the state**, and no path compares the state's hash against the owner or the owner's relations. So a forged state carrying the *source's* `custody_hash` while being bound to the *victim* is undetectable. The genuine custody content (relations, snapshots, semantic hashes) is self-consistent, so `_validate_positive_from_owner_state` runs clean.

### Why the sealer guard does not help

The lead's step 7 rebinds the cell directly and never calls `_seal`. The `"resolver owner custody already sealed"` single-assignment guard is not on the reachable path. Confirmed by control C5.

### Why this is not an impossible threat model

It uses only primitives the F7 hostile court already admitted and exercises: `function.__closure__`, callable recovery by `__name__`, and `_AuthenticatedResolverState` construction — the court's own file does all three at `:2265-2298` and `:2362`. The only extension is the one cell assignment, which is an ordinary Python data-model operation on CPython 3.11.3.

## 3. Section A — exact lineage and write terrain: PASS

| Requirement | Verdict |
|---|---|
| startup lineage exact and ancestry-preserving | **PASS** — `62394d7ff` is an ancestor of `d6734e015`; graph is linear (`d8caaec02 → 3a52d491c → 423bb27f8 → abfce9621 → d6734e015` plus the code commits) |
| production mutation limited to `rawlsing_next/pre553_source_relations.py` | **PASS** — three code commits touch that file only: `fbb735f69`, `52976c778`, `d5e6d6baa` |
| court mutation limited to `rawlsing_next/tests/test_pre553_temporal_comparability.py` | **PASS** — `62394d7ff` changes only that file (+5/−1) |
| `pre553_temporal_comparability.py` unchanged | **PASS** — blob `6f6b462b1cdef54d7989f15452473383c1661594` identical at repair base and candidate head |
| no unrelated accepted owner/authority material changed | **PASS** — full write terrain from startup `5d8794dff` is exactly the two files plus the HQ231 return directory |

## 4. Section B — live-state exposure attack: **FAIL (one live path found)**

I inspected every surface the commission named:

- **module globals and callable helpers** — `_make_sealed_source_relation_owner` is `del`-ed after use (`:1177`), so the factory is not reachable; the three exported names are the class plus two closures.
- **closures reachable from public entrypoints** — the live path. `authenticated_source_relation_decision.__closure__` yields `_state_or_refuse`; `loader.__closure__` yields the `entries` **cell** itself. This is the admitted reflection surface, and it is where the defect lives.
- **diagnostic/inspection surfaces** — `source_relation_owner_custody_diagnostic` returns `canonical_json` text only and never the state object; correct, and unchanged by the attack.
- **returned tuple/NamedTuple material** — the diagnostic returns `str`; verified `type(...) is str`.
- **weak-owner references and the lexical ledger** — the ledger is weakref-keyed and dies with the owner, which is fine; the problem is not the weakref, it is that the *cell holding the ledger* is writable.
- **constructor sealer and loader reachability through reflection** — sealer reachable via `SourceRelationResolver.__init__.__closure__` but not on the attack path; loader reachable and load-bearing.
- **ordinary resolver-visible fields and registry objects** — `_registry` is shared by design and is not the leak.

**Conclusion:** the claim that *no caller-visible path exposes the exact authenticated custody state* is **false**. The state is not returned directly, but it is obtainable (`loader(source)`, `loader(victim)`) and, decisively, the ledger that decides which state a resolver gets is caller-rebindable.

I explicitly did **not** accept underscore naming, frozen dataclasses, NamedTuple shape, or lexical closure as provenance guarantees — and the defect is precisely where those were treated as sufficient.

## 5. Section C — source→victim transplant hostile: **FAIL to refuse**

The HQ228 transplant shape was reconstructed from the court's own fixtures (`_adjudicated_resolver` → source A; `SourceRelationResolver(relations=(), authority_registry=source._registry)` → victim B). Every caller-reachable surface was obtained, then:

- `object.__setattr__(victim_state, ...)` → refused (`AttributeError`/`TypeError`), as the court shows. **Not sufficient**: the state is reconstructible, so in-place mutation is unnecessary.
- container mutation → the ledger **tuple** refuses item assignment, as the court shows. **Not sufficient**: the containing cell does not.
- closure-cell reachable objects → **this is the break.**
- resolver-visible field replacement → blocked by `MappingProxyType`, and irrelevant given W2.
- registry substitution → refused (section D).
- minimal local rebind (replace only the victim's own entry state, control C2) → **also succeeds**, so the attack does not depend on rebuilding the whole tuple.

Weakref/GC hazards: I found no aliasing or reuse hazard. The weakref correctly dies with the owner, and identity checks use `is`. The defect is independent of GC behaviour.

## 6. Section D — registry and snapshot provenance conservation: **PASS (and unaffected by the defect)**

Re-verified at the candidate head:

| Invariant | Status |
|---|---|
| exact concrete `AuthorityRegistry` pinned | PASS — `type(authority_registry) is not AuthorityRegistry` refuses |
| constructor-admitted snapshots | PASS |
| exact snapshot semantic/hash validation | PASS — `_semantic_hash_impl(snapshot.semantic_projection()) != snapshot.content_hash` refuses |
| registry replacement immunity | PASS (`test_hq227_exact_instance_registry_replacement_cannot_change_pinned_owner_snapshot`) |
| subclass/override redirection refusal | PASS (three `test_hq225_rr04c_*` and two `test_hq227_*` witnesses) |
| relation-decision replay identity | PASS — `validate_relation_decision_replay_identity` re-derives and refuses stale/corrupt |
| outer/nested authority cross-binding | PASS (`test_hq227_nested_registry_instance_dispatch_shadow_cannot_redirect_f7`) |

**Important classification point.** The attack does **not** corrupt custody *content*, forge snapshots, or substitute a registry. It reuses the source's genuinely valid, genuinely registry-pinned custody material and attacks only the **owner→custody binding**. That is why every invariant in this section still passes while the victim nevertheless opens. This is a custody-binding defect, not a provenance-conservation defect — and it is the reason the disposition is `PARTIAL` with a bounded defect rather than an architecture conflict.

## 7. Section E — semantic non-duplication: **PASS**

Compared the accepted P07/source-relation owner logic before and after the repair (`fbb735f69^` → candidate head), and confirmed at runtime:

```
RELATION_STATES : 12
AUTHORITY_KINDS : 19
ORDER_BASES     : 3
NEGATIVE_STATES : 9
```

- exact-zero / no tolerance, total precedence, 3+ anchor refusal, exact measure/use binding, `TEMPORAL_EVIDENCE` source-scope identity, explicit unrestricted-token law: all conserved (full F7 court 155 passed).
- no ranking / selection / interpolation / trajectory / causation / currentness / pooling / equivalence-creation / actor authority introduced.
- The repair is a custody-boundary change inside `pre553_source_relations.py`; it does **not** reimplement or fork relation semantics in F7. `pre553_temporal_comparability.py` is blob-identical to the repair base.

## 8. Section F — HQD-216 productive adequacy: **PASS**

A provenance fix that refuses everything would be unacceptable; this one does not. All five lawful productive paths remain available and are exercised green:

| Path | Witness | Result |
|---|---|---|
| same-universe | `test_witness_same_universe_needs_no_equivalence` | PASS |
| exact-zero | `test_witness_exact_zero_is_derived_not_asserted` | PASS |
| increase | `test_witness_decrease_direction_is_derived` / cross-universe increase | PASS |
| decrease | `test_witness_decrease_direction_is_derived` | PASS |
| lawful cross-universe relation | `test_hq227_full_owner_path_positive_cross_universe_service_remains_productive` + `_adjudicated_resolver` positive path | PASS |

Full court results at the candidate head: **`test_pre553_temporal_comparability.py` 155 passed**; **`test_pre553_source_relations.py` 24 passed**. No productive regression.

## 9. Section G — fail-capability: **INSUFFICIENT (stale/non-load-bearing for this defect)**

The candidate's fail-capability (`test_hq231_targeted_break_transplantable_loader_reopens_same_victim`, `:2343-2390`) constructs a transplanted state and **monkeypatches `tc._authenticated_source_relation_decide`** to a deliberately broken function that calls `sr._decide_from_owner_state(transplanted, ...)` directly.

That proves dependency on the authenticated entrypoint. It does **not** prove the actual lexical custody cell is protected, because:

1. it **replaces** the entrypoint rather than driving the real one;
2. it supplies its own transplanted state rather than reaching the live one through reflection;
3. it never touches the ledger cell.

My reproduction is strictly stronger: it drives the **real, unmodified** `authenticated_source_relation_decision` through the **real** `_state_or_refuse`, against the **real** live ledger, and defeats it by one cell assignment. The fail-capability is therefore neither stale in the sense of broken-file-drift nor load-bearing for `F7-RR-04G`; it is simply aimed at a different seam. Per the commission I reject it as non-load-bearing for this defect specifically.

## 10. What would actually defeat closure-cell rebinding

I do not repair, but I name the invariant, because the commission asks for it when the attack fails and it is equally useful here. Any one of these is sufficient:

1. **Non-forgeable custody binding.** Derive the owner binding from something the caller cannot set — e.g. hold custody in a per-instance slot written by the constructor and read via a guard that compares a *secret* per-instance token, not a self-declared `owner_ref` field. Rebindable-if-you-can-rebuild is the core failure.
2. **Re-derive `custody_hash` at decision time from the owning resolver** and compare against the state's recorded hash; a forged state carrying another owner's hash would then refuse.
3. **Remove `_AuthenticatedResolverState` from the caller-constructible surface** (the candidate's own fail-capability constructibility is the tell), so a forged state cannot be built even with a rebindable cell.
4. **Make the ledger content-addressed against the owner rather than a mutable cell binding** — e.g. a single immutable structure created at import that maps owners to states through a weak-keyed container whose *mapping* is not reachable as a rebindable cell.

Note that (2) alone is insufficient if the forger can also recompute the hash — which they can, since `semantic_hash` is public and the source's custody material is available. The durable fix is (1) or (3).

## 11. Runtime relationship

The parallel governed-runtime qualification lane (`agent/rabochii-pyat-hq232-f7-runtime-qualification-r1`) is not a dependency of this adjudication, and I did not read or mutate its branch history. Per the commission's own instruction, a green execution of the **existing** F7 court cannot dispose of this lead, because the existing court does not exercise `cell.cell_contents` rebinding — I confirmed that by reading the court: its only ledger assertion is `ledger[0] = ledger[-1]` → `TypeError`.

## 12. Answer to the commission, plainly

| Section | Verdict |
|---|---|
| A. exact lineage and write-terrain | **PASS** |
| B. live-state exposure attack | **FAIL — one live rebindable path found** |
| C. source→victim transplant hostile | **FAIL to refuse — victim becomes positive** |
| D. registry and snapshot provenance conservation | **PASS** |
| E. semantic non-duplication | **PASS** |
| F. HQD-216 productive adequacy | **PASS** |
| G. fail-capability | **INSUFFICIENT for this defect** |

`blocker = F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE`
`classification = bounded provenance/custody implementation defect` (not architectural; semantic and registry layers intact; requires in-process Python reflection)
`disposition = F7_SEALED_CUSTODY_PARTIAL__NAMED_DEFECT`
`full F7 adoption = FORBIDDEN` until this is repaired and re-reviewed.
`repair performed in this lane = NONE`

## 13. Bound on this review

No production mutation. No repair. No self-adoption. No merge. No other worker's worktree used. One isolated sparse worktree on the commissioned branch, backed by the canonical object store; no clone, no broad fetch, no sparse-scope widening, no rebase. The reproduction mutates only in-process closure state, which is the attack itself, and is therefore non-destructive to the repository. The only artifacts are this review plus the five required JSON files and the verbatim attack/control scripts.
