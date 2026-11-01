# ACCEPTED TEST CONFLICT AND NEGATIVES

## Unfiltered result is not green

```text
179 passed, 14 failed, exit 1; no skips/errors
```

The 14 failures are exactly:

- **2** unchanged accepted M2 tests: `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release`.
- **12** unchanged S06FR `OBSERVED` defect-presence assertions.

A separate filtered selection using `-k 'not OBSERVED and not test_17... and not test_18...'` gives:

```text
179 passed, 14 deselected, exit 0
```

That selection is reported as a selection, not as a green full suite.

## Accepted M2 conflict — exact remaining failure

Both accepted tests are **byte-unchanged**; their current PRE-MAIN test blob is preserved. They fail at fixture setup:

```text
M2ReleaseError: RELEASE_UNAVAILABLE: requested exact release is unavailable
```

- `test_17_binding_cannot_resolve_different_release` builds a foreign release/representation in a second repository, then registers the foreign binding into the first repository to attack a later resolution path.
- `test_18_endpoint_failover_only_among_same_release` builds a foreign binding in another repository and registers it into the first repository to attack the failover list.
- Patched `register_representation`/`register_binding` now call `release_exact` and refuse the unregistered foreign release before the original later oracle.
- This is a **compatibility change at the accepted test fixture contract**, not a permissive-resolution regression and not evidence of a security hole.

**New reconciled tests** (S06G test module, both pass):

- `test_reconciled_m2_17_early_refusal_and_lawful_downstream_mismatch`: asserts `RELEASE_UNAVAILABLE` on the unregistered foreign release, then lawfully imports/registers the foreign release/representation and preserves the original `PUBLICATION_BINDING_MISMATCH` oracle.
- `test_reconciled_m2_18_early_refusal_and_lawful_failover_mismatch`: same early refusal, then lawful foreign registration, then the original cross-release failover `PUBLICATION_BINDING_MISMATCH`.

**Owner choice:** decide whether the two accepted fixtures are invalid setups for the stricter native boundary. If yes, authorize a new fixture-update review that adds lawful foreign registration to the accepted scenario. Do not weaken `release_exact` or edit the accepted tests in place. If no, reject the S06G `register_binding` change and retain the current local defects.

## S06FR historical defect-presence negatives

All 12 original S06FR `OBSERVED` tests remain present and executable. They fail on repaired code because the defect they demonstrated no longer reproduces. They are **not** demanded to pass and were not edited:

- direct saved B5 `_append_events` (RECERTIFIES, CURRENT_SELECTED, PRODUCT_PUBLISHED) — now `EXTERNAL_ISSUER_HOLD` / transaction refusal;
- direct saved M2 `_insert` — now `EXTERNAL_ISSUER_HOLD` / transaction refusal;
- rehashed publication `replay_root_ref`, `determinant_set_hash`, `producer_permission_ceiling` — now checkpoint semantic replay conflict;
- torn publish after append — now rolls back to `PRODUCT_REGISTERED`;
- M2 check/insert race — now direct helper refuses outside transaction;
- concurrent B5 stale-predecessor selection — now serialized one winner/one conflict;
- public event payload identity drift — now `TypeError` on frozen mapping;
- cross-release rebuild receipt — now checkpoint receipt/state conflict.

The exact per-case verdicts and exceptions are in the E2 return’s `DEFECT_BY_DEFECT_VERDICTS.jsonl`; the same historical test bytes are used here. The old findings remain preserved as RED reproduction history.

## Other courts

| Court | Result |
|---|---|
| Accepted B5 | 39/39 pass |
| Accepted M2 | 26/28 pass, 2 fixture failures |
| S06G new repair court | 42/42 pass |
| E2 independent court | 10/10 pass |
| Adjacent EE14 asof + world composition | 45/45 pass |
| S06FR overlay | 17/29 pass, 12 obsolete defect-presence failures |

## What was not done

- No accepted test was edited, skipped, xfailed or deselected inside the unfiltered run.
- No failure was relabeled green.
- No external issuer, protected CURRENT, OS-kill durability, multiprocess/cross-process custody, native source, actor, N11/N12, C11/C12 or production adoption was claimed.
- S06G remains `LOCAL_UNAUTHENTICATED`; `require_external_issuer` holds.
