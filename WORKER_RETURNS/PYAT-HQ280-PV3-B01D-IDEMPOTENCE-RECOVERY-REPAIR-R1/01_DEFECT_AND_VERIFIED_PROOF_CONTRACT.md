# B01D — Defect and verified-proof contract

## 1. The exact defect (B01CR W6)

Location: `rawlsing_next/pre553_batch_durable_checkpoint_candidate.py`,
`plan_recovery`, pre-B01D lines 662–665:

```python
# START intent without a durable COMMIT: side effect may have landed.
if unit_key in proofs:
    dispositions[unit_key] = RecoveryDisposition.RERUN_SAFE
    rerunnable.append(unit_key)
```

Failure mode: membership test on caller-supplied keys. The proof *value* is
never read, never schema-checked, never issuer-checked, never verified
against anything. Consequences, all demonstrated live:

- `idempotence_proof={key: ""}` → `RERUN_SAFE` (empty string promotes).
- `idempotence_proof={key: <any junk>}` → `RERUN_SAFE`.
- `idempotence_proof={other_key: ...}` for the crashed unit → the crashed
  unit stays HELD (correct by accident), but the *named* key would promote
  if it had an intent — key presence is the whole rule.
- A crash after an external side effect but before COMMIT therefore yields a
  rerun proposal over an effect that may already have landed. The duplicate
  was demonstrated tangibly: durable counter 1 → 2 under the old rule.

This contradicts the module's own contract comment ("reachable ONLY with a
declared idempotence proof") because *declaration* was implemented as *mere
utterance*.

## 2. The repaired rule

```python
presented = dict(idempotence_proof or {})
disregarded[key] = (...; see IDEMPOTENCE_ISSUER_HOLD)   # recorded, never honored
...
# START intent without a durable COMMIT: side effect may have landed.
# Fail closed: caller proofs are recorded above and never honored.
dispositions[unit_key] = RecoveryDisposition.UNKNOWN_OUTCOME
held.append(unit_key)
```

Properties:

- The `idempotence_proof` parameter is retained keyword-only so existing
  callers do not crash, but it is **semantically inert**: it cannot change any
  disposition.
- Every presented key is recorded in `RecoveryPlan.disregarded_caller_proofs`
  (and `summary()`), with the value's type noted — the attempt is evidence.
- `RERUN_SAFE` remains a valid enum member for a future verified credential,
  but no code path in this candidate assigns it. Source audit in the recorder
  asserts `'if unit_key in proofs' present: False`.
- `checkpoint_effect_flags()` includes `honors_caller_idempotence_proof:
  False`, so the flag vector itself testifies to the repair.

## 3. Why no verified credential exists (repo-wide search)

Searched `rawlsing_next/*.py` for `idempot`:

- `ExecutorBinding(executor_ref, execute)` — identity + callable, **no effect
  classification, no idempotence declaration**.
- `BatchUnitSpec` / `UnitExecutionReceipt` — job identity, attempt index,
  result/provenance refs; the receipt proves an attempt completed, **not**
  that re-executing its side effect is safe.
- I03/I05/Route B owners — deterministic pure computation over sealed
  releases at development scope; determinism of *computation* is not a
  credential about *external* side effects, and none of these owners issues
  one.
- Unrelated `test_*idempotent*` hits — replay/registry determinism in
  adp010/GT34 modules; none binds a unit key + release + executor to a
  side-effect claim, none carries an issuer or signature.

Conclusion: **no already-accepted, demonstrably competent existing owner
supplies a verifiable attestation**, so per the commission the automatic
upgrade is **disabled entirely** rather than re-pointed at a new trust root
(which would itself be an invented authority).

## 4. The verified-proof contract (future, held)

`IDEMPOTENCE_ISSUER_HOLD` (exported, in `__all__`) requires, before any
future `UNKNOWN_OUTCOME → RERUN_SAFE` path may exist:

| field | meaning |
|---|---|
| `exact_unit_key` | the precise `unit_ref.key` covered |
| `exact_release_refs` | the `C11LogicalRelease` refs covered |
| `exact_manifest_hash` | the `BatchManifest` covered |
| `executor_identity` | the exact executor whose side effect is claimed idempotent |
| `side_effect_classification` | a verifiable statement of what the side effect is |
| `issuer` | an already-accepted, demonstrably competent existing owner |
| `verification` | signature/schema check against that owner's accepted contract |

Forbidden substitutes (each demonstrated refused in the attack table): caller
mapping key presence; any caller string including non-empty strings; caller
dict/object shape; content hash alone; claimed issuer name alone; dataclass
type alone.

## 5. What `RERUN_SAFE` means while the hold stands

It is a **reserved disposition with no producer**: the enum member exists so a
future verified credential has a lawful target, but the candidate contains no
assignment to it. Any test or audit can assert `"RERUN_SAFE" not in
dispositions` and it will hold for every caller input of any shape
(demonstrated over 8 attack variants plus 6 hardening inputs).

## 6. Non-goals (explicitly not repaired here)

- Crash-consistency beyond the measured phases; hardware/FS lies.
- NFS/distributed locking (B01CR hold 4, inherited unchanged).
- B01 F-04/F-05/F-06 (unchanged, out of scope).
- Adaptive checkpoint visit-order identity (B01 P17, unchanged).