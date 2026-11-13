# C03 parent lock composition and typed purchase-history ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; A relay construction on frozen start `01b2d2d23259969778ce996f5527037d666f46f8`.
**Implementation SHA:** `61f2918ec947e44dd7ecff8fd3359734469e9a90`.
**B return:** `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34`; B implementation `255fd4905990e3c0cab3e2d95ba91b851ea701a8`.
**Contract:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`; protected baseline `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. Parent lock composition

Observed at the frozen start: `parent_decision.perform_parent_decision` held
`parent_activity._parent_write_lock`, then called B04
`material_operations.purchase_drum_kit`, whose public wrapper acquires
`material_operations._purchase_lock` **then** `_parent_write_lock` again. A
bounded subprocess probe timed out after 120 s; the composed path did not
complete. This was a real same-process `flock` deadlock, not a test artifact.

Repair in `parent_decision.py`:

```text
perform_parent_decision
  -> require B04 module + _purchase_lock + _purchase_drum_kit
  -> with b04._purchase_lock(session):
       with parent_activity._parent_write_lock(session):
           _perform_parent_decision_locked(...)
             -> revalidate admitted decision source
             -> b04._purchase_drum_kit(...)   # actual unlocked writer
             -> write the C12 parent action receipt
```

This matches B04's public lock order (`market/material` lock then parent lock),
keeps decision revalidation and the actual B04 write inside one lock
composition, and avoids recursive parent locking. No no-lock adapter,
monkeypatch, second controller or new lock framework was added.

Exact required B04 hook if Pair1 changes the current private names:

```text
material_operations.purchase_drum_kit_under_parent_lock(
    session, parent_id, *, operation_id, owner_actor_id, request=None,
    expected_clock=None)
```

must be the actual unlocked purchase writer while the caller already holds
`_purchase_lock` then `_parent_write_lock`, or expose the exact current
`_purchase_lock`/`_purchase_drum_kit` pair deliberately. Missing pair refuses
`PARENT_DECISION_B04_UNLOCKED_WRITER_UNAVAILABLE`.

P4's foreground lock remains outside this composition. B05's rent lock is
separate and does not call the parent lock; no conflicting nesting was found in
the composed path. Normal P4 operations serialize the whole background unit.

## 2. Typed B04 purchase consumption

`parent_activity._parent_material_history` recognizes the exact B04
`P2_PARENT_PURCHASE` episode and no generic unknown kind. It validates:

- episode body/receipt schema, grade, root, branch, parent ID/alias, status;
- `parent_material_source_before/after` hashes and strict before→after chain;
- admitted purchase `possession=OBJECT_STOCK_AND_OWNERSHIP_WRITTEN`,
  `event_effect=NONE`, event clock;
- `purchase_source`, market before/after, owned before/after, object ID/kind,
  owner, unit price, currency, request currency;
- recomputed `purchase_source` equality and current parent currency equality.

The suspended B04 post-purchase `P2_PARENT_MATERIAL_ANTECEDENT` bridge is **not
adopted as history**. It is tolerated only when it exactly duplicates an
already admitted `P2_PARENT_PURCHASE` row (same operation/source/before/after/
purchase source); any other bridge refuses
`PARENT_MATERIAL_BRIDGE_NOT_ADOPTED`. Removing the bridge changes no reader
result. `read_parent_history` exposes the typed purchase row and omits the
duplicate bridge, with object/owner/currency/unit price/market/owned/purchase
provenance and `purchase_episode_count`.

## 3. B04 currency boundary — exact required writer ABI

The real remaining conflict is B04-owned, not a C02 reader fault. B04 currently
debits a parent whose material currency differs from the market/request and
declares equivalence. Required before debit/stock/ownership:

```text
parent_currency == request.currency_unit == market.currency_unit
```

On mismatch: durable B04 `REFUSED` receipt (`CURRENCY_MISMATCH`), parent before
== after, no debit/stock/ownership, `possession=NONE`; receipt carries
`parent_currency_unit_before`, `market_currency_unit`, `currency_match`; remove
the equivalence declaration; `read_purchase` validates the same equality;
B04/B05 fixtures use matching parent currency for lawful purchases or exercise
the refusal. B04/B05 code was not edited by this return.

C03 refuses a currency mismatch before B04. Same-unit fixtures
(`parent_sourcefree_currency_unit == sourcefree_currency_unit`) are declared at
construction to exercise the lawful sourcefree path; no parent/market facts are
mutated after admission to bypass the writer.

B04/B05 current default tests: **3 failed, 1 passed** in 40.85 s
(`evidence/b04_b05_currency.log`), all at this real currency boundary. C03
matching-currency purchase, history acceptance, replay and lock composition pass
in the B 11-test suite and A C03/C04 suite.

## Explicit limits

- Full P3 `BatchEngine` 3–5 event interleave across B02 periods is not proved.
- B04 writer currency guard/B05 rent integration remain Pair1 work.
- E03 crash/SIGKILL composite recovery is not proved.
- No native/MIII parent psychology, source/use rights, actor/human authority or protected merge.
