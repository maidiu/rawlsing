# HQ217 — H-D/F8 BINDING AUTHENTICATION REPAIR — RETURN

**LANE:** `PYAT-HQ217-HD-F8-BINDING-AUTHENTICATION-REPAIR-R1`
**BRANCH:** `agent/rabochii-pyat-hq217-hd-f8-binding-authentication-repair-r1`
**COMMISSION TIP:** `29f8583ff24e372e5fe7948b6dc400e05ee69851`
**EXACT STARTUP TIP:** `09e4dc0d9e8dba21eadab0b5dd55821af7f4811c`
**HOSTILE REREVIEW:** `6df6c86816a949d02bd91d33b6686ba0de728050`
**INHERITED DISPOSITION:** `HD_F8_REPAIR_AUTHORITY_OVERREACH`
**PUSHED SHA:** `d588f709a8b923082d5d458ed6a671e2ae57fb76`
**REMOTE VERIFIED EQUALS LOCAL:** yes
**DISPOSITION:** `HD_F8_AUTHENTICATION_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`

---

## 1. Plain answer

The authority bypass is closed. A caller can no longer manufacture source eligibility
by directly constructing or `dataclasses.replace`-ing the binding, and handing the
evaluator a **genuine** authoritative receipt alongside a forged binding no longer
helps — because the admitted set and provenance are now **re-derived from the receipt**
and never read from the presented binding.

I reproduced the bypass before changing anything. All four attacks reached F8 with
`state=EXACT_SUPPORTED` for a source the receipt had refused. All four now refuse.

This is COMPLETE / READY FOR REREVIEW, which is **not acceptance**.

## 2. Reproduced first

Fixture: a real adopted receipt where **only A is admitted** and B is refused.

| Attack | Before the repair |
|---|---|
| 1. direct constructor forgery + genuine receipt | **ALLOWED** `EXACT_SUPPORTED` source=B |
| 2. direct constructor forgery + genuine receipt + a request | **ALLOWED** `EXACT_SUPPORTED` source=B |
| 3. `dataclasses.replace` of a lawful binding + genuine receipt | **ALLOWED** `EXACT_SUPPORTED` source=B |
| 4. copied receipt id and replay identity | **ALLOWED** `EXACT_SUPPORTED` source=B |

**One thing worth flagging.** Attack 3 *first* refused, with
`ADMISSION_PROVENANCE_MISSING`. That was an accident of my incomplete forgery — the
replaced binding still carried A's provenance rows while claiming B. A court written
against that would have been a **false negative**: green, and testing nothing. Once I
forged a provenance row for B as well, it bypassed too. The forgery was made complete
before it was recorded as a failing attack.

## 3. The fix — one enforcement point

New module-private `_authenticate_binding_against_authority(binding, *, request, receipt, rule)`:

1. requires the exact request, the authoritative receipt, and the bound rule;
2. recovers `currentness_result` from the binding so re-derivation is exact;
3. calls the **existing** `verify_service_f8_scope_binding_replay` (commission req. 3);
4. adds a second explicit material gate so a future weakening of the verifier cannot
   silently reopen the hole;
5. **returns the re-derived binding.**

`binding_ref` is a deterministic `semantic_hash` over a seed containing
`request.material()`, `receipt.replay_identity()`, `receipt.receipt_id`,
`rule.rule_hash` and the admitted set. A caller cannot produce the lawful `binding_ref`
without the authoritative receipt's own replay identity — which is exactly why
re-derivation is the sound defence.

| Path | Before | After |
|---|---|---|
| `evaluate_bound_positioned_subject_possibility` | trusted binding fields; `receipt` **optional** | `request` and `receipt` **required**; authenticates first, then uses the re-derived binding |
| `assert_query_source_admitted` (power 1) | asserted from the binding's own admitted tuple | requires `request`/`receipt`/`rule`; decides against the re-derived set |
| `expose_unranked_admitted_source_set` (power 2) | returned the binding's own tuple | requires `request`/`receipt`/`rule`; returns the re-derived tuple |

**Why I closed the two powers too.** The commission's fifth requirement is that
construction and `replace` must not *manufacture source eligibility* — broader than
reaching F8. Power 1 returns `admitted: true`; power 2 returns the admitted set. Leaving
either unauthenticated would have left the same overreach through a different door.

**No `__post_init__`, no self-hash.** A caller can fabricate a self-consistent binding.
The court proves it by rehashing a forgery with the module's own `semantic_hash`,
carrying the genuine receipt id and replay identity — and it still refuses.

## 4. Dead code removed — deliberately

The evaluator's explicit `rule_hash` comparison became **unreachable** once
authentication was added: the authenticated binding derives its `f8_rule_hash` from the
very rule object presented, so the comparison could never be false.

I removed it, along with the then-unreachable `BINDING_RULE_REPLAY_MISMATCH`. Leaving
unreachable code with a comment overstating its role is precisely the dead-branch defect
class HQ211 raised as F3 — in the very module my parent lane had just repaired. It is
replaced by an assertion documenting that authentication must derive the binding from
the presented rule, so a broken authentication path fails loudly.

**Consequence, disclosed:** a tampered rule now refuses with `BINDING_REPLAY_MISMATCH`.
Two pre-existing assertions were retargeted at that code — one was also *tightened* to
mutate only a non-admitted row, so it isolates receipt-mismatch detection instead of
passing via an incidental coverage refusal. Neither was loosened to accept anything.

## 5. Public-surface accounting repaired

The HQ213 census excluded the two exported dataclasses **by name** and enumerated only
the two pinned powers, hiding twelve other public methods. The dataclass constructors
are exactly the forgery surface this lane exists to close.

| Count | Value |
|---|---|
| names in `__all__` | 28 |
| exported **classes** | 3 (incl. both forgery-surface dataclasses) |
| exported functions | 4 |
| public methods on the binding | 14 |
| eligibility-revealing powers | 2 |
| loud refusals | 8 |

Nothing is excluded by name, and every name is pinned as a literal so an *added* public
method fails the census rather than silently reducing the count.

## 6. HQD-216 — the repair is not refuse-everything

Four court tests **require** positive lawful behaviour and would fail if I had
over-refused. A competent receipt plus a bound rule still reaches `EXACT_SUPPORTED`
with the correct source, geometry, `model_rule_hash`, model/walkback authority refs and
replay determinants all unchanged.

**Disclosure:** the commission directs reading
`PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`.
**That file does not exist at the commission tip** — the highest HQD law present is
`24_HQD125`. I applied HQD-216 as the commission states it inline (local grain; prove
competent applicability carries into F8; don't inherit unrelated upstream occupancy
blockers) and disclosed the absence rather than inventing its contents.

## 7. Courts and regression

**215 collected, 215 passed, 0 failed, 0 skipped**, deterministic across seeds 0 / 0 /
12345.

New hostile court: **25 tests** — all eight commissioned witnesses plus eleven more,
including seven single-field mutations that must each refuse alone, and signature
introspection proving `request`/`receipt` are *required*, not optional.

**Negative control.** The pre-authentication binder was extracted from the commission
tip and swapped into a shadow tree outside the repository:

| Code under test | Result |
|---|---|
| pre-authentication binder | **18 failed**, 7 passed |
| repaired binder | **25 passed** |

All four forgery attacks fail on the vulnerable code and pass on the repair.

**Regression: 74 pre-existing slice files, compared as sorted failure-identity sets.**

| | baseline | repaired |
|---|---|---|
| failed / errors / skipped | 91 / 48 / 1 | 91 / 48 / 1 |
| passed | 1448 | 1448 |
| **distinct failing/error IDs** | **139** | **139** |

**New failures: 0. Changed: 0. Delta empty both ways.** None of the 139 touch the
binder or its owners.

## 8. Write terrain

Exactly four files. All three adopted owners byte-identical, verified in the shell *and*
inside all three courts:

```
3e40caca29e8c96ee1f412f919cfc7dba63f96c4  pre553_service_source_applicability.py
62e5eced47b64512f47b004e3e13a6ef3fe21de7  source_backed_positioned_subject_possibility.py
f30fca20e7b56e00348e82765d95f974b4b6a195  objective_consumer_bounded_evidence.py
```

No raw source, no live C4, no C7, no locator, no warrant, no actor/person work, no
architecture reopen, no new authority, no merge, no self-adoption.

## 9. The caveat that matters most

**This is a breaking API change, not only a bug fix.** All three authority-consuming
entry points now *require* the authoritative request, receipt and rule. Any caller
outside this repository's courts must be updated; downstream consumers matching on
`BINDING_RULE_REPLAY_MISMATCH` will see different codes. That is the repair working as
commissioned, but it should be reviewed as a contract change.

## 10. What the rerereviewer should attack first

1. Whether **any** remaining public path reports eligibility or reaches F8 without
   passing through `_authenticate_binding_against_authority` — enumerate the surface
   independently of my census.
2. Whether closing power 1 and power 2 was correct scope, or over-reach beyond the
   commissioned evaluation path.
3. Whether recovering `currentness_result` from the binding can diverge from what was
   actually bound.
4. Whether the 20 hoisted request variables weakened any existing assertion.
5. Whether removing the dead rule-hash check was right, or defence-in-depth was better.

Full caveats in `04_FINAL_DISPOSITION.json`.

## 11. Terminal

`HQ217_HD_F8_BINDING_AUTHENTICATION_REPAIR_RETURNED__FINAL_REREVIEW_REQUIRED`