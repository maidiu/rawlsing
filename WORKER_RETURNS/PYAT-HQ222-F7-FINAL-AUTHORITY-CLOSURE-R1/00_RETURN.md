# PYAT HQ222 — F7 FINAL AUTHORITY CLOSURE — R1 RETURN

**DISPOSITION:** `F7_FINAL_AUTHORITY_CLOSURE_COMPLETE__READY_FOR_FINAL_REREVIEW`

**BRANCH:** `agent/rabochii-pyat-hq222-f7-final-authority-closure-r1`
**FILES CHANGED:** 2 (both inside commissioned write terrain)
**F7 COURT:** 114 → **135 passed, 0 failed**
**M1 COURT:** 27 passed
**NEW TESTS FAILING AGAINST PRE-REPAIR PRODUCTION:** **20 of 21**
**REGRESSIONS INTRODUCED:** **0** (62-entry failure set byte-identical before and after)

---

## 1. All four findings closed

No architecture reopen. No new authority kind, relation state, reason family, source
ontology, or actor capability.

### A. F7-RR-04B — the owner's returned proof is now conserved

**The defect.** F7 called the adopted `SourceRelationResolver.require(...)` and assigned
the returned `RelationDecision` to nothing, then fabricated a local POSITIVE record from
the *caller's* `equivalence_ref`. The owner returns the exact authorized `relation_ref`
**and** the exact relation-authorizing `authority_ref` — both discarded. F7 separately
resolved a caller-supplied SOURCE_EQUIVALENCE snapshot B. So it proved *some* owner
decision was positive and *some* supplied snapshot was positive, but never that B
authorized the relation. **Positive plus positive is not identity.**

**The repair.**
1. The returned decision is captured and validated against the exact request by a new
   helper `_relation_decision_defect`: authorized state, relation kind, relation-ref
   identity, non-null authority ref, the exact source universe **pair**, target use, and
   operation scope. Any mismatch refuses.
2. The resolution record now carries **the owner's own** `decision.authority_ref` and
   `authority_operation`. This also fixes a latent type violation — `equivalence_ref` is
   an `ExactRef` of the relation and was being recorded into an `AuthorityRef` field.
3. **No A/B split:** the supplied SOURCE_EQUIVALENCE snapshot's `authority_ref` must
   equal the returned decision's `authority_ref`.

I **retained** the duplicate authority input rather than removing it. Removing it would
change the accepted request contract; cross-binding it removes the split-brain while
preserving the contract, which is what the commission's "no A/B split" demands.

**Discriminating witnesses.** With the production file reverted:
- `test_hq222_rr04b_a_forged_owner_proof_is_refused` → **FAILS pre-repair** (a stand-in
  object merely claiming `authorized=True` bought a positive relation)
- `test_hq222_rr04b_unrelated_positive_equivalence_snapshot_cannot_ride_the_relation`
  → **FAILS pre-repair** (the A/B split itself was accepted). Control on the same
  registry with the authorizing ref stays positive.

### B. F7-RR-03B — the identity owner is now bound to the compared source scope

**The defect.** The identity-owning TEMPORAL_EVIDENCE authority was resolved with **no**
`required_universe_refs`. Once positive by kind/state, the custom keys
`temporal_identity_contract_refs` and `identity_surface_jointly_satisfied` alone decided
the identity gate — so an out-of-scope snapshot could own identity merely by carrying
those keys.

**The repair.** The `temporal_evidence` slot now resolves with
`required_universe_refs=(universes[0], universes[1])`, reusing the existing
`resolve_required_authority` machinery. No new authority kind or identity registry.

**All three commissioned attacks fail closed — and all three FAIL pre-repair:**
unrelated source universe; only one of two compared universes; stale/wrong universe ref.

For the "one of two" attack the cross-universe path is given a **genuine** positive owner
decision so nothing higher-precedence can mask the identity defect, with a both-universes
control that stays positive.

**Precedence note.** An out-of-scope owner surfaces in the higher-precedence
`TEMPORAL_INSUFFICIENT_AUTHORITY` state, not `TEMPORAL_IDENTITY_UNRESOLVED`. Both are
lawful refusals and total precedence is unchanged. The witnesses discriminate the intended
mechanism by asserting on the `temporal_evidence` **resolution record**
(`AUTHORITY_SCOPE_MISMATCH`) and `comparability_status`, not on one arbitrary label.

### C. F7-RR-02C — both adopted unrestricted representations honored

Inspection confirmed both tokens **are** valid in the adopted law
(`pre553_empirical_authority._scope_contains`). New constant
`ADOPTED_UNRESTRICTED_SCOPE_REPRESENTATIONS = {EXPLICIT_UNRESTRICTED,
UNRESTRICTED_BY_THIS_AUTHORITY}` applied to all three scope helpers.

**No third token invented; omission is still not unrestricted** — the helpers return
False for `None`, empty collections, empty string, and every other literal. A witness
pins the constant to exactly the two adopted literals and cross-checks F7 against the
general law so the sets cannot drift again.

### D. COURT-HQ220-01 — a genuine same-fixture fail-capability witness

**The defect.** HQ219's RR-03 break observed an unsatisfied-owner refusal, monkeypatched
one exact-ref helper, then built a **separate satisfied registry**. It never disabled
owner-satisfaction consultation on the same fixture, so it could not demonstrate fail
capability.

**The repair.** A single production seam,
`_temporal_evidence_identity_scope(snapshot)`, is the only point through which F7 reads
the owner's identity verdict. It adds no adjudication. The new witness uses **one**
fixture — the unsatisfied-owner registry — and falsifies only the owner's satisfaction
verdict on it. The outcome flips to authorized; restoring the real consultation restores
`IDENTITY_SURFACE_NOT_JOINTLY_SATISFIED`. That is exactly the self-authorization path,
opened on the same fixture.

**The RR-04 break was also rewritten, and this deserves HQ's attention:** its old
assertion was *"the break must reopen the gap"* — i.e. it **demanded the vulnerability**.
Once F7 validates the returned proof, a non-returning fake is refused, so that assertion
had come to assert the very defect the repair closes. The replacement falsifies the real
`RelationDecision` on the same DENIED fixture; the forged-impostor case is split into its
own hardening witness.

---

## 2. Productive adequacy — no refuse-everything repair

All five commissioned productive paths remain positive:

| path | state | direction |
|---|---|---|
| same-universe comparable | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` | — |
| exact zero | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` | `NO_AUTHORIZED_CHANGE` |
| increase | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` | `INCREASE` |
| decrease | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` | `DECREASE` |
| genuine positive cross-universe relation | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` | `INCREASE` |

Sustained ceilings verified intact: **12** relation states, **19** authority kinds,
exact-zero with no deadband/rounding/tolerance, 3+ anchor refusal, total precedence,
exact measure binding, complete ExactRef use scope, and no F8 / ranking / selection /
interpolation / trajectory / causation / currentness / pooling / equivalence-creation /
actor power.

## 3. Regression evidence

Method: full `rawlsing_next/tests/` sweep post-repair (2663 passed), then the identical
sweep over the 26 implicated files with production reverted to `e88cfeb10`, then diff.

**62-entry failure set: IDENTICAL, byte-for-byte. Zero introduced.** No failure touches
F7 or `temporal_comparability`. The pre-existing set is dependency-driven (`pyarrow` and
`pyreadstat` absent) and unrelated-lane; HQ219 reported the same class and HQ220 declined
to charge it to F7.

## 4. Residual risks flagged, not silently widened

1. **`isinstance(resolver, SourceRelationResolver)` still accepts subclasses.** F7 now
   trusts the returned decision's content, so a hostile *subclass* of the real resolver
   could still return a fabricated AUTHORIZED decision. HQ220 raised this as a related
   boundary weakness; it was **not** one of the four commissioned findings and was not
   repaired. Flagged rather than silently widened.
2. **Governed-use contract mismatch unchanged.** F7's governed use is an ExactRef while
   the source-relation owner keys `target_use` as a string, so F7 projects
   `governed_use_id.object_id`. Still an integration/producer **occupancy** gap, not an
   F7 defect.
3. **`IDENTITY_CONTRACT_INSTANCE_MISSING`** remains an upstream estate-occupancy gap. This
   lane consumes competent owner-backed fixtures; it creates no production identity
   instance.
4. **RR-03 witness needs the new seam**, so it cannot execute against pre-repair
   production. Its pre-repair discriminating power is carried by the three RR-03B scope
   witnesses, which do fail pre-repair. Disclosed rather than hidden.

## 5. Truthful discrepancy

The commission names startup tip `9adc8cc9b…`, which is the **parent** of launch tip
`e88cfeb10…` (the commit that adds `00_COMMISSION.md`). The launch tip was used so the
commission document is present — the same pattern seen in HQ221. No governed environment
was named; a pre-existing stdlib-only pytest venv was used, so this is reproduced-execution
evidence, not governed certification.

## 6. Artifacts

```
WORKER_RETURNS/PYAT-HQ222-F7-FINAL-AUTHORITY-CLOSURE-R1/
  00_RETURN.md
  01_RELATION_DECISION_AUTHORITY_CROSSBIND.json
  02_TEMPORAL_EVIDENCE_SOURCE_SCOPE_BINDING.json
  03_UNRESTRICTED_REPRESENTATION_AND_FAIL_CAPABILITY.json
  04_PRODUCTIVE_PATH_AND_REGRESSION.json
  05_FINAL_DISPOSITION.json
```

Production: `rawlsing_next/pre553_temporal_comparability.py` (+162)
Court: `rawlsing_next/tests/test_pre553_temporal_comparability.py` (+343)

**Terminal:** `HQ222_F7_FINAL_AUTHORITY_CLOSURE_RETURNED__HQ_FINAL_REREVIEW_REQUIRED`