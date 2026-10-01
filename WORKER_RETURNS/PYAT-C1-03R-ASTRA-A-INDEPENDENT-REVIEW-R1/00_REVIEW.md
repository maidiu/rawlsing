# PYAT C1-03R — ASTRA-A GENERIC LIFECYCLE OWNER EXTENSION INDEPENDENT REVIEW — R1

Status: `CHANGES_REQUIRED`

Review branch:
`agent/reviewer-pyat-hq154-c1-03r-astra-a-r1`

Commission tip:
`8bac6d97ee61b552fd36dcb29b8d03f8f8306aee`

Implementation return under review:
`eb02332c93c6c3927303eefde9dd9ed768bb3480`

HQ151 implementation commission:
`9705742b3466e764d310f73b9bc3115073991e9f`

Astra E03 decision:
`b346bd9f7f18b582173a47ca337d468816270c84`

This is an independent documentary/code-forensic review. No implementation was modified, no merge/self-adoption occurred, no raw source was accessed, and no C4/C7/V3 work was performed.

## Executive disposition

The Astra-A implementation gets the **central semantic architecture mostly right**:

- one generic noncurrent meaning;
- no C1-specific sentinel;
- no DEFERRED/UNAVAILABLE/DELETED split;
- owner-computed affected/unaffected on the normal transition path;
- explicit grounded noncurrent rows rather than error-to-noncurrent conversion;
- positive-only receipt projection remains byte-compatible;
- promotion and rollback both route through the same owner outcome law;
- the sealed-successor defect is genuinely repaired at the declared single-authority transition grain;
- the mixed AT19 witness is coherent;
- AT18 replay grades remain distinct and the new fresh-process owner replay is correctly classified as lifecycle serialization replay, not fresh analytical recomputation.

However, the generic owner extension does **not yet fail closed at all of the owner boundaries Astra/HQ151 required**. Four exact counterexamples remain. Three are independently blocking even without the fourth:

1. duplicate **positive replacement** outcomes are silently collapsed rather than rejected;
2. serialized noncurrent rows can carry a forged/missing `replacement_ref`, and the negative receipt can carry a forged/missing `receipt_schema`, without deserialization rejection;
3. an arbitrary owner-unknown dependent ref is reported `CURRENT` by the public lifecycle path;
4. checkpoint replay verifies the affected set against the determinant graph but does not verify the unaffected set, so `A ∪ U = K` is not independently reconstructed at restore time.

These are generic lifecycle-owner contract defects, not fixture nits. They sit exactly at the acceptance grain of the Astra Option-A extension. Therefore C1-03R cannot be approved yet.

---

# 1. Generic noncurrent semantics

## Accepted

`NoncurrentDependentOutcome` owns exactly one disposition:

`NO_CURRENT_NO_LAWFUL_REPLACEMENT`

The constructor correctly requires:
- exact `old_ref`;
- the one fixed disposition;
- non-empty exact `supporting_refs`;
- a non-empty selector-free `reason_code`;
- `replacement_ref is None`.

No C1-specific product vocabulary was added. No separate deferred/unavailable/deleted lifecycle classes were added.

The normal owner transition does not convert:
- missing callback;
- callback exception;
- unchanged replacement;
- missing recomposition path

into a noncurrent outcome. An explicit grounded row is required.

## Blocking counterexample C1-03R-A-RVW-001 — duplicate positive outcomes are not rejected

In `AuthorityInvalidationReceipt.__post_init__`:

```python
pairs: dict[str, tuple[ExactRef, ExactRef]] = {}
for raw_old, raw_new in self.recompilation_pairs:
    old, new = exact_ref(raw_old), exact_ref(raw_new)
    if old == new:
        raise AuthorityMaintenanceError(...)
    pairs[old.key] = (old, new)
```

There is no duplicate-source check corresponding to the one implemented for `noncurrent_dependents`.

Therefore an input containing:

```text
affected = (A,)
recompilation_pairs = ((A, NEW_1), (A, NEW_2))
noncurrent = ()
```

is silently normalized to one pair, whichever assignment appears last. It does **not** raise.

This violates the Astra/HQ151 law:
- every affected ref has exactly one outcome;
- duplicate outcomes are rejected;
- malformed outcome sets are rejected rather than normalized.

The worker's court named `test_g_duplicate_affected_outcome_is_refused` covers only duplicate **noncurrent** rows:

```python
_receipt((a,), (), (_noncurrent(a), _noncurrent(a)))
```

It does not challenge duplicate positive replacement rows.

This is blocking.

---

# 2. Receipt / serialization / compatibility / atomicity

## Accepted

The positive-only compatibility mechanism is structurally sound.

At the pre-extension owner blob:
`ac7f3a013129bc148debf8f011597971a2c99442`

and the implementation owner blob:
`747a6eb5577ec007fe30caf2a358d2ad822f4b1a`

the positive-only `AuthorityInvalidationReceipt.semantic_projection()` preserves the original historical field set:
- `contract_id`
- `record_type`
- `changed_authority_refs`
- `affected_dependent_refs`
- `unaffected_dependent_refs`
- `recompilation_pairs`

The new `receipt_schema` and `noncurrent_dependents` fields are emitted only when noncurrent rows exist. This supports the worker's positive-only identity-preservation claim.

The `AuthorityCandidate` class section is text-identical pre/post extension, so no candidate hashing/identity change occurred.

Normal `promote_current` and `rollback_current` compute `_recompile(...)` before mutating releases/current pointers/events. On the inspected paths, malformed runtime outcomes therefore fail before owner state commit.

## Blocking counterexample C1-03R-A-RVW-002 — deserialization discards forbidden semantic fields instead of rejecting them

`NoncurrentDependentOutcome.from_dict` does this:

```python
return cls(
    old_ref=exact_ref(data["old_ref"]),
    disposition=_text(data["disposition"], "disposition"),
    reason_code=_text(data["reason_code"], "reason_code"),
    supporting_refs=...,
    replacement_ref=None,
)
```

It never reads or validates serialized `data["replacement_ref"]`.

Consequences:

### 2A. forged non-null replacement ref is accepted

Take a valid negative row, serialize it, then replace:

`"replacement_ref": null`

with an arbitrary exact replacement ref.

`NoncurrentDependentOutcome.from_dict(...)` silently discards the forged value and reconstructs a valid row with `replacement_ref=None`.

Because `AuthorityInvalidationReceipt.from_dict` validates the embedded `record_ref` **after** reconstruction, the forged field is invisible to the reconstructed semantic identity. A payload can therefore contain the forbidden replacement field while still reproducing the canonical original receipt ref.

### 2B. missing required replacement_ref field is accepted

The same deserializer also accepts a row with the `replacement_ref` field deleted entirely, again synthesizing `None`.

But HQ151's minimum row shape explicitly includes:
`replacement_ref: null`.

### 2C. negative receipt schema is not validated

`AuthorityInvalidationReceipt.from_dict` never inspects `receipt_schema`.

Therefore a serialized receipt containing noncurrent rows can:
- omit `receipt_schema`; or
- carry a forged `receipt_schema`

and still reconstruct as the canonical new-schema object, provided the other reconstructed semantic material yields the embedded ref.

This violates:
- canonical serialization/hashing must bind the negative row shape;
- the new schema is the explicit compatibility boundary;
- malformed/tampered serialized owner state must fail closed;
- checkpoint replay must validate rather than silently normalize semantic labels.

The existing tamper court changes `reason_code`, which does enter the reconstructed hash and therefore fails. It does not test discarded/ignored fields.

This is blocking.

## Blocking counterexample C1-03R-A-RVW-004 — checkpoint replay does not re-prove U = K \ A

During `AuthorityMaintenanceExecutor.from_checkpoint`, release replay computes:

```python
expected_affected = executor._graph.affected(
    invalidation.changed_authority_refs
)
if expected_affected != invalidation.affected_dependent_refs:
    raise ...
```

but it never computes and compares:

`executor._graph.unaffected(expected_affected)`

against:

`invalidation.unaffected_dependent_refs`.

The receipt constructor checks only that A and U do not overlap. It cannot prove coverage of K because it has no graph parameter.

Therefore restore-time validation does not independently reconstruct the required invariant:

`A ∪ U = K`.

A self-consistently rehashed checkpoint could shrink/alter the serialized unaffected set while preserving the correct affected set, and the replay path has no exact graph-derived U check to reject it.

The existing `test_g_tampered_graph_binding_is_refused` proves that stripping `known_dependent_refs` from the graph cannot erase an authority-edge dependent. It does **not** test a forged invalidation receipt whose unaffected set fails to cover the graph-known K.

This is blocking at the Astra checkpoint/replay requirement.

---

# 3. Current vs historical visibility

## Accepted

For an owner-known dependent explicitly recorded noncurrent:
- `dependent_lifecycle_status()` returns `EXPLICIT_NONCURRENT`;
- `resolve_current_analytical_product()` raises `ExplicitNoncurrentDependent`;
- cache/object presence is not consulted;
- a replacement outcome returns its exact `current_replacement_ref`;
- an unaffected known sibling remains current/identity-stable.

The release continues to select the authority, so dependent noncurrent status does not withdraw the governing authority.

## Blocking counterexample C1-03R-A-RVW-003 — unknown refs are declared CURRENT

`AuthorityMaintenanceExecutor.dependent_lifecycle_status(ref)` searches releases for a receipt that mentions the supplied ref. If none is found, it returns:

```python
{
    "dependent_ref": ref,
    "lifecycle_state": "CURRENT",
    "reason": "no governed transition has affected this dependent",
    ...
}
```

There is no prior check that `ref` belongs to:

`self._graph.known_dependent_refs`.

Therefore an arbitrary exact dependent ref never registered with the owner is reported `CURRENT`.

`resolve_current_analytical_product()` simply delegates to this method and returns the status unless it is explicitly noncurrent, so the public analytical current-product path inherits the same behavior.

This defeats the declared rule that currentness comes from the lifecycle owner rather than mere object/ref presence. The owner cannot positively know an unregistered dependent is current.

The correct behavior must distinguish:
- owner-known current/unaffected;
- owner-known replacement;
- owner-known explicit noncurrent;
- owner-unknown / not governed at this lifecycle grain.

This is blocking.

---

# 4. Astra sealed-successor defect

## Accepted at declared grain

The old defect is real and the repair is substantively correct.

The repaired `build_owner_recompiler`:
1. intersects the analytical registration's **exact consumed determinant refs** with the owner-supplied changed set;
2. requires exactly one consumed prior;
3. selects the unique **other** changed ref with the same `authority_id`;
4. rejects equality with prior;
5. requires the candidate successor to be an authority the owner knows;
6. hands that exact ref to the recomposer.

For `promote_current`, the changed set is built by the owner from:
- exact previous current ref; and
- exact snapshot resolved from the sealed candidate.

Thus the adapter is not selecting a successor by tuple position or version label.

The use of the private `_known_authority_ref` method is a coupling smell but does not weaken the proof at this grain: membership in the owner-generated changed set already carries transition provenance, and the extra registration check rejects unknown/future pre-binding. A later cleanup could expose a public predicate, but no semantic blocker is created by the private call here.

The fixture correction is also real:
- `unsealed_decoy_model_ref` and `sealed_successor_ref` are distinct;
- decoy shares the consumed prior's content hash;
- sealed successor has a different content hash;
- the model rule material binds the complete sealed successor ref;
- the rule hash therefore commits to that exact successor;
- `AuthorityCandidate` identity code is unchanged.

No remaining successor-binding counterexample was found.

---

# 5. Mixed AT19 witness

## Accepted

The one-release mixed witness contains four registered dependents:
- one affected dependent with a lawful replacement;
- one directly affected explicit noncurrent dependent;
- one transitively affected downstream explicit noncurrent dependent;
- one unaffected sibling bound to a different authority.

The determinant graph explicitly contains the noncurrent→downstream dependency when the positive witness is built.

The receipt demonstrates:
- R and N disjoint;
- R ∪ N = A for the normal owner-generated release;
- unaffected sibling stays identity-stable/current;
- downstream noncurrent row cites the required noncurrent input and receives no replacement.

The omitted-edge hostile is independently useful:
- the owner omits the downstream product from A when the edge is absent;
- the separate registry/recomposer closure witness re-evaluates registered products;
- it detects that the supposedly unaffected downstream product would reidentify under the successor.

That challenge does not rely on cache/object presence and does not infer an edge from the candidate receipt.

The blocking defects above are generic owner boundary defects; they do not invalidate the mixed witness itself.

---

# 6. AT18 replay grades

## Accepted

The four grades remain distinct:

1. `HISTORICAL_EXPLANATION_ONLY`
2. `SERIALIZATION_REPLAY`
3. `FRESH_PROCESS_PRODUCT_REPLAY`
4. `FRESH_EMPIRICAL_RECOMPUTATION`

The analytical replay owner enforces a mechanism→maximum-grade table and refuses fresh grades from non-fresh mechanisms.

The implementation return correctly classifies the new separate-process owner checkpoint round trip as:

`SERIALIZATION_REPLAY of lifecycle state`

and explicitly does **not** call it fresh analytical recomputation.

`pre553_replay_audit.py` is unchanged at blob:
`86e0b9c518633735f2527b89fb72fca1a40dc2cc`

`pre553_analytical_composition.py` is unchanged at blob:
`604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`

Runner-input/oracle separation remains in the existing AT18 courts. No grade collapse created by the Astra-A patch was found.

---

# 7. Execution/provenance reconciliation

Implementation diff:

`9705742b3466e764d310f73b9bc3115073991e9f -> eb02332c93c6c3927303eefde9dd9ed768bb3480`

is exactly one commit and is confined to:
- `rawlsing_next/pre553_authority_maintenance.py`;
- `rawlsing_next/pre553_analytical_replay_dependency.py`;
- `rawlsing_next/tests/c1_at18_at19_fixture.py`;
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`;
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`;
- the eight required worker-return files.

No replay-audit/composition owner changed.

The review commission is exactly one documentary commit above the implementation return:
`eb02332c... -> 8bac6d97...`.

The worker receipt reports exactly the commissioned four-suite court:

- analytical replay dependency: 35;
- authority maintenance: 42;
- replay audit: 54;
- analytical composition: 13;
- total: `144 passed, 0 failed, 0 errors, 0 skipped`;
- Python 3.12.14;
- pytest 9.1.1;
- exit 0.

Source comparison independently confirms:
- no pre-existing test function was deleted;
- 14 test functions were added to analytical replay dependency;
- 21 test functions were added to authority maintenance;
- exactly 35 new test functions were added total;
- replay-audit and composition test blobs are unchanged.

No GitHub Actions workflow run is associated with the implementation return SHA. This browser reviewer did not rerun the worker's local four-suite command; the 144-pass runtime is therefore reconciled as worker execution evidence, not independently re-executed evidence.

The source-level counterexamples above are nevertheless decisive because they are direct constructor/deserializer/public-resolver paths that the current tests omit.

---

# Required correction

A narrow repair is sufficient. No architecture warrant is needed.

At minimum:

1. `AuthorityInvalidationReceipt.__post_init__` must reject duplicate replacement-source rows before dict collapse.
2. `NoncurrentDependentOutcome.from_dict` must require and validate serialized `replacement_ref` as explicitly null, rather than replacing arbitrary/missing input with null.
3. `AuthorityInvalidationReceipt.from_dict` must validate the negative `receipt_schema` exactly when noncurrent rows exist and reject incompatible schema presence on legacy positive-only rows.
4. `dependent_lifecycle_status` / the public analytical resolver must fail typed for owner-unknown dependent refs rather than declaring them current.
5. `from_checkpoint` must independently recompute both A **and U** from the determinant graph and require exact equality with the receipt before applying the release.
6. Add hostiles for all five boundaries, including serialized/checkpoint forms.

Do not reopen:
- Astra's selected Option A;
- sealed-successor repair;
- AuthorityCandidate identity;
- AT18 grade law;
- analytical composition;
- replay audit.

## Final

`CHANGES_REQUIRED`

Terminal:

`C1_03R_ASTRA_A_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
