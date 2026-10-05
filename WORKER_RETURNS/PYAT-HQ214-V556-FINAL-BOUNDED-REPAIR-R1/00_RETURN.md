# 00 — HQ214 V556 final bounded repair — R1

Lane: `PYAT-HQ214-V556-FINAL-BOUNDED-REPAIR-R1`
Role: semantic-sensitive repair worker — Space Bunny Max
Commission tip: `0c75551ece03ec23b77043bf967fbd0112e9d1c2`
Repair base: `e4d7e6f7352e60da9de956c7875293fca141d371`
Hostile rereview: `agent/reviewer-pyat-hq213-v556-final-rereview-r1 @ 4bfbeb499883d52940131a087374b8087bf503ea`

**Disposition: `V556_FINAL_BOUNDED_REPAIR_COMPLETE__READY_FOR_HOSTILE_REREVIEW`**
**V556 remains unadopted.** Seam byte-identical. No architecture reopen. No self-adoption.

---

## D-1 — registry-level class/family coherence

**Reproduced first.** A probe read the registry build body and reported:

```
build_body_mentions_schema_class        : false
build_body_mentions_class_family_map    : false
author_body_mentions_class_family_map   : true
```

The ceiling existed at exactly **one of two** publication surfaces.

**Repair.** One named decision, `_refuse_if_class_family_mismatch`, now used by both.
At registry build the class is read from the **validated** contract *after*
`validate_result_contract_binding` has run, and the family from the **rule body** — not
from the caller-supplied dataclass attribute. Refuses both a mismatch and an unmapped class.
No class or family invented.

## The thing I'd want the rereview to check hardest

**In this tranche a mismatch with an *authorable* family is unconstructible.** All three
admitted classes are authorized by `V556_TOPOLOGY`, and `V556_TOPOLOGY` is the only
authorable family — so that pair-set is empty by construction of the authority-derived map.

Consequence: the family ceiling refuses every constructible mismatch **first**, shadowing the
new gate. I verified this rather than assuming it — deleting the registry coherence call left
the end-to-end test **still passing**.

So I proved the gate two other ways, each verified to fail when broken:

| Proof | Test | Result when target broken |
|---|---|---|
| Decision made never-raise | `test_d1_coherence_decision_refuses_genuine_mismatches` | **FAILED** ✓ |
| Decision made never-raise | `test_d1_unmapped_class_is_refused_by_the_coherence_decision` | **FAILED** ✓ |
| Registry call deleted | `test_d1_registry_build_is_wired_to_the_coherence_decision` | **FAILED** ✓ |
| Registry call deleted | `test_d1_registry_build_refuses_a_rehashed_hand_built_mismatched_rule` | still passed — **shadowing** |

I did **not** invent a second family to make the gate look exercised. That would be the
wrong trade, and the commission forbids it.

## D-2 — the vacuous court

The old test asserted `MAP["OBJECTIVE_WORLD_STATUS"] == "V556_TOPOLOGY"` — an entry
equalling itself. Removed. Replaced by six tests; four verified fail-capable. Both required
proofs are present: **authoring refuses** a genuine mismatch, and **direct registry build**
of a hand-built, consistently rehashed rule **refuses** (isolated from the stale-hash path).
Plus a positive control — the gate is not blanket refusal; all three admitted classes still
build a `GOVERNED_RULES_PRESENT` registry.

## D-3 — court theatre removed

`test_w10` built the banned names by concatenation and then scanned for literals that were
never in the file. It could not fail. **Removed, not decorated.**

Replaced with an AST test over substrate `ImportFrom` nodes. It never searches for a literal
name, so concatenation cannot defeat it. Verified: adding `BLOCKED_STRONG_NOUNS` to the
court's imports made it **FAIL**.

Honest residual: this is a **tripwire, not an invariant**. Self-reference protection stays a
review discipline — the commission's own permitted framing.

## D-4 — machine-readable classification

The old proof searched the helper's **docstring** for the word "court". Rewordable prose
cannot support a claim. Replaced with a **frozen** record
(`PAYLOAD_PARTICIPANT_HELPER_CLASSIFICATION`) with every field asserted directly, plus a
behavioural seam-absence proof against the real seam source. The docstring is now explicitly
demoted to explanation. No new seam added.

## Two of my own tests were wrong; both fixed

Worth recording, because a fail-capability audit exists precisely to catch this.

1. **My first neutering of the coherence decision was invalid.** I set `authorizing = semantic_class`, which *still raised* for the mismatch pairs — so it appeared to "pass". I discarded that attempt and used a genuine never-raise stub, which did fail the tests.
2. **My D-4 positive control proved the wrong thing.** It "demonstrated" refusal by swapping the two governed endpoints — but both *are* governed, so that must be accepted. Corrected to use a third, unbound route; the swap-accepted case is now asserted too.

## Qualification

Focused court **55 → 61**, M3 29, M2 28 → **118 passed**, deterministic across two runs.
Regression slice: **4 failing IDs → 0, zero new failures** (new court vs unrepaired module,
sorted ID sets compared with `comm`, module file-swapped and restoration sha256-verified).

HQ213's discriminating probes all still closed: P1/P2/P4/HAND1/HAND2/P7a/P7b refused, P5
**0 accepted / 10 refused**, both positive controls `SUPPORTED`. Semantic vs structural
`UNBOUNDED` separation holds — array `max_items="UNBOUNDED"` still authors, an `UNBOUNDED`
string item inside it is still refused.

Only **4 of the new tests are discriminating**; the rest are positive controls, structural or
preservation witnesses. Recorded so nobody over-counts them.

## Environment — still not governed

Unchanged and truthful: **no governed environment.** pytest 9.1.1 remains a throwaway venv
install. **Full-suite baseline not claimed** — only 4 of 157 test files are materialized under
the sparse scope.

## Six residuals, none blocking

D-1's observability shadowing · self-reference as review discipline · helper off the
production path · full-suite not reproduced · environment disclosure · non-discriminating
witness classification.

**This lane does not adopt V556, does not make a mismatch with an authorable family
constructible, and does not certify a full-suite baseline.**

`HQ214_V556_FINAL_BOUNDED_REPAIR_RETURNED__HOSTILE_REREVIEW_REQUIRED`