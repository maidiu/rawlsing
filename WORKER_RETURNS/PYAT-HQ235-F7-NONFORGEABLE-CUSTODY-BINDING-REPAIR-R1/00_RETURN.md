# PYAT HQ235 — F7 NON-FORGEABLE CUSTODY-BINDING REPAIR — R1 RETURN

**DISPOSITION:** `F7_NONFORGEABLE_CUSTODY_REPAIR_BLOCKED__OWNER_BOUNDARY_ARCHITECTURE_DECISION_REQUIRED`
**BRANCH:** `agent/rabochii-pyat-hq235-f7-nonforgeable-custody-binding-repair-r1`
**EXACT STARTUP TIP:** `326262ee45d0cef440eb60b2c1639e63c068061c`
**BLOCKER:** `F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE`
**SEMANTIC MUTATION:** NONE · **SELF-ADOPTION:** NONE · **MERGED INTO CONTROL:** NONE

---

## 1. Bottom line

I did not fake closure. Two things are true and they must be reported together:

1. **The exact HQ234 04G attack is now refused**, and custody is genuinely anchored to the
   resolver's live containers with decision-time re-derivation. Every *single* admitted
   reflection primitive is closed.
2. **A caller who substitutes all live anchors and rebinds the ledger in one coordinated
   step still mints custody.** The commission's required invariant is therefore **not
   establishable inside the current pure-Python owner boundary**, so I am returning the
   architecture-boundary disposition rather than a closure claim.

I could have shipped a fully green court by simply omitting the coordinated witness. It
is in the suite instead, asserted `True`, as the evidentiary basis for this disposition.

---

## 2. Reproduction, then repair

I independently reproduced the blocker at the startup tip — victim
`TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT` → `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`
via ledger-cell rebind, no production monkeypatching.

**The repair is pattern-level, not a rename.** A self-declared `owner_ref` is no longer
treated as proof of custody. Each sealed state now also carries:

| Anchor | Rule | Defeats |
|---|---|---|
| `sealed_by_ref_owner` | must be *identically* the live `_by_ref` | transplanted `by_ref` material |
| `sealed_by_key_owner` | must be *identically* the live `_by_key` | `by_key` substitution |
| `sealed_relations_fingerprint` | re-derived from live `_by_ref` at decision time | in-place relation mutation (HQ232 W3) |

`_state_or_refuse` gates every lookup on `_authenticate_owner_custody_anchor`.

### One design constraint I discovered by exact proof, not assumption
My first iteration also anchored `_registry`. That **broke an accepted test** —
`test_hq227_exact_instance_registry_replacement_cannot_change_pinned_owner_snapshot` —
because HQ227's accepted law requires that replacing the caller-visible registry leaves
adjudication *unchanged* (snapshots are pinned). Making registry identity load-bearing
would have converted that accepted immunity into a hard refusal — a **semantic mutation**,
which is forbidden. So I removed it and narrowed re-derivation to relation semantic
content only. Recorded rather than quietly reverted.

---

## 3. Witness results

| # | Attack | Result |
|---|---|---|
| 1 | exact HQ234 `cell.cell_contents` 04G rebind | **refused** |
| 2 | caller-constructed state with victim `owner_ref` | **refused** |
| 3 | source remains productive after attack | **positive** |
| 4 | victim refused before *and* after every mutation | **refused** |
| 5 | visible `_by_ref` / `_by_key` replacement | **refused** |
| 6 | recovered sealer cannot transplant custody | **refused** |
| 7 | replacement binding primitive attacked | **FORGES — asserted `True`** |
| 8 | fail-capability on the new invariant | recorded with honest outcome |

On witness 8 I want to be precise rather than flattering: breaking the container-identity
anchor alone cannot reopen the victim, because an attacker with no source relation has
nothing to authenticate. The anchor's load-bearing status is established by witnesses
1/3/5 refusing — not by that test.

---

## 4. Why the invariant is not establishable in pure Python

Probed empirically on the governed CPython 3.11.3:

| Resists | Forged by the admitted caller |
|---|---|
| tuple item assignment | `cell.cell_contents` assignment |
| `int` attribute mutation | `object.__setattr__` on frozen dataclasses **and** `__slots__` |
| | module/class/instance attribute rebinding |
| | `__defaults__`, `__code__`, property, method replacement |
| | `WeakKeyDictionary` (attacker controls `__eq__`/`__hash__`) |

Only C-level **values** resist. But custody is an owner→material **mapping**, so it must
live in a container — and every Python-level container the owner can reach is also
caller-reachable and re-assignable. Therefore any secret the owner holds is **readable**,
and anything derived from it (`semantic_hash` is public) is **recomputable**.

Anchoring N containers only raises the attack from *one* primitive to *N coordinated*
primitives. It does not establish non-forgeability. That is the honest limit.

**Smallest architecture change required:** move the P07 custody ledger behind a small
native (C-extension) boundary — an opaque per-resolver capability handle holding custody
in C memory with no Python-visible accessor, exposing only "is this the handle sealed for
resolver X" plus a resolve. Then every Python object can be rebound and custody is still
unforgeable. Alternatives: process isolation with a narrow IPC surface; an OS-backed
opaque handle; or — cheapest if a native boundary is deferred — **explicitly accept the
residual coordinated-substitution risk and downgrade the F7 claim** from
"non-forgeable" to "adversarial-single-primitive".

---

## 5. Productive adequacy and semantics

All five lawful positive paths preserved — same-universe, exact-zero, increase, decrease,
lawful positive cross-universe (`10 passed, 153 deselected`). Fail-closed correctness was
**not** treated as sufficiency.

No accepted P07 semantics, relation states/precedence, authority kinds, source-composition
law, temporal-comparability semantics, or V554/V557/V558 semantics changed. **No accepted
test was edited to make results pass.** Production change is confined to
`pre553_source_relations.py` custody anchoring; the other change is the F7 court.

---

## 6. Runtime and regression

Governed interpreter, **no substitution** (sha256 `11d6f541…`).
Targeted courts **228 passed** (F7 + source-relations + M1).

Broad regression at this tip, with the same 9 environmental exclusions as HQ230:

| | baseline | repaired |
|---|---|---|
| normalized FAILED/ERROR | **54** | **54** |
| SHA-256 | `278854ee…` | `278854ee…` |
| passed | 2683 | 2691 (+8 = new witnesses) |

**Zero regression.** This is worker-local development evidence, **not** final independent
acceptance — a separate hostile rereview and runtime qualification still required.

---

## 7. What HQ must decide

The choice is not "is the repair good enough" — it is **which of these three is accepted**:

1. authorize a native boundary for P07 custody (true non-forgeability), or
2. isolate the owner behind IPC, or
3. formally accept the residual coordinated-substitution risk and restate the F7 custody
   claim at its true strength.

Adopting F7 without choosing would record a non-forgeability claim the code does not
support. I recommend option 1, with option 3 as the honest interim if a native boundary is
not immediately available.

`HQ235_F7_NONFORGEABLE_CUSTODY_REPAIR_BLOCKED__OWNER_BOUNDARY_ARCHITECTURE_DECISION_REQUIRED`