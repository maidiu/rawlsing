# PYAT C1-03R — R3 FINAL INDEPENDENT REREVIEW — R1

**Disposition:** `APPROVE_AT_DECLARED_GRAIN`

**Terminal:** `C1_03R_R3_FINAL_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Reviewed implementation return:
`c690bb0b1e6f071c9a640a6825769b96f30dd79a`

R3 commission base:
`b77937f7f2c79e9007ff7d8cd19061d1758f7f15`

Prior independent rereview:
`08b53e8b62ce4dbd04bd47dc2798229ea7dbe0c4` — `CHANGES_REQUIRED`

Reviewer issue tip:
`1dc84acb924b08420b94dde39fa1ac67daa9efeb`

## Bottom line

The sole remaining F-1 boundary is corrected.

A dependent that is present only in `SemanticDeterminantGraph.known_dependent_refs`, with zero governing releases, is no longer treated as CURRENT. The owner now returns:

- `lifecycle_state = NOT_GOVERNED`;
- `reason_code = NO_GOVERNING_RELEASE`;
- `governing_release_ref = None`.

The current-product adapter then fails closed instead of serving the historical ref as current.

Cache/object/evidence residency cannot change the result because `dependent_lifecycle_status()` derives currentness exclusively from:
1. the lifecycle owner's release/invalidation records; and
2. the determinant graph's declared known set.

It does not read snapshot, evidence or product caches when deciding lifecycle currentness.

After a real release, the previously accepted law is preserved: every known dependent is in A or U at the declared graph grain, and therefore receives exactly one recorded lifecycle branch. Replacements remain CURRENT with their exact replacement ref; unaffected dependents remain CURRENT identity-stable; explicit noncurrent outcomes remain typed noncurrent refusals.

All previously approved R2/Astra boundaries remain preserved. No concrete regression was found.

## 1. F-1 zero-release known dependent — PASS

The decisive implementation branch is now fail-closed.

`dependent_lifecycle_status()` first scans governing releases for a receipt whose affected or unaffected set contains the dependent.

If no such release exists:

- absent from `known_dependent_refs` → `NOT_GOVERNED / OWNER_UNKNOWN_DEPENDENT`;
- present in `known_dependent_refs` → `NOT_GOVERNED / NO_GOVERNING_RELEASE`.

The old positive branch:

`known + no release -> CURRENT`

is gone.

The owner documentation in the same function now states the correct rule: CURRENT requires a governing release and recorded owner outcome and cannot be inferred from graph membership, cache residency or absence of transition.

### Structural proof that this is the right boundary

`SemanticDeterminantGraph.unaffected(A)` is literally the complement of A over `known_dependent_refs`.

`AuthorityMaintenanceExecutor._recompile()` always computes:

- `affected = graph.affected(changed_authority_refs)`;
- `unaffected = graph.unaffected(affected)`;

and writes both into the invalidation receipt.

Therefore, after any real governed release:

`A ∪ U = K`

for the graph's known-dependent set K.

A known dependent with no governing receipt is therefore the zero-release/no-governing-release case, not an implicit-current case.

## 2. Residency hostiles — PASS

The source decision path never consults:
- `_snapshots`;
- `_snapshot_exact_refs`;
- `_evidence`;
- product/object cache presence.

The worker's snapshot/evidence hostiles use real owner-resident artifacts and remain `NOT_GOVERNED`.

The tests do not alias the analytical dependent's ExactRef into the authority/evidence caches, but this does not weaken the proof: those caches are structurally absent from the lifecycle-status decision. Creating an invalid cross-type alias is unnecessary to prove nonparticipation.

## 3. Post-release law — PASS

After a real release, `dependent_lifecycle_status()` preserves the accepted ordering:

1. exact noncurrent row → `EXPLICIT_NONCURRENT`;
2. exact recompilation pair → `CURRENT` with `current_replacement_ref`;
3. exact unaffected membership → `CURRENT`, identity stable;
4. otherwise → owner conflict.

The added post-release court exercises all three lawful branches.

The owner still refuses to infer a replacement or noncurrent outcome. The existing R/N/A/U coverage laws are untouched.

## 4. Previously approved R2/Astra boundaries — PRESERVED

R3's production diff changes only the zero-release branch and its explanatory docstring inside `pre553_authority_maintenance.py`.

The following approved laws remain source-identical outside that branch and/or are exercised by unchanged preserve courts:

- duplicate positive replacement rejection;
- cross-table replacement/noncurrent overlap rejection;
- explicit negative `replacement_ref: null` law;
- exact negative receipt schema law;
- historical positive-only field/hash compatibility;
- strict refusal of new-schema receipts with zero noncurrent rows;
- owner-unknown `NOT_GOVERNED`;
- checkpoint independent A/U re-derivation;
- one generic noncurrent disposition;
- DEFERRED/UNAVAILABLE/DELETED not invented as lifecycle meanings;
- error→noncurrent prohibition;
- sealed-successor exact binding;
- decoy distinction;
- omitted-edge hostile;
- mixed promotion and rollback courts;
- AuthorityCandidate identity;
- AT18 replay-grade separation.

No approved R2 boundary is reopened by the R3 correction.

## 5. Inaccurate NOT_GOVERNED exception prose — NONBLOCKING

`resolve_current_analytical_product()` raises `OwnerUnknownDependent` for both NOT_GOVERNED reasons.

Its message says:

`the lifecycle owner does not know this dependent ... absent from the owner's known dependent set`

which is false for the new zero-release-known case.

The residual is slightly broader than prose:
- the exception class is named `OwnerUnknownDependent`;
- its class-level `code` remains `OWNER_UNKNOWN_DEPENDENT`;
- its docstring describes only the truly owner-unknown case.

### Why this does not block acceptance

The semantic owner is `AuthorityMaintenanceExecutor.dependent_lifecycle_status()`, and it already distinguishes the two cases correctly:

- owner unknown → `NOT_GOVERNED / OWNER_UNKNOWN_DEPENDENT`;
- owner known but zero governing release → `NOT_GOVERNED / NO_GOVERNING_RELEASE`.

The adapter does not overwrite that state with a positive state. It raises before returning any current product.

No release receipt, checkpoint, product identity, lifecycle identity or authority decision is derived from the exception prose/class code in the commissioned path.

The commission explicitly permits use of the existing typed not-governed failure for the zero-release case. The exception is therefore a coarse legacy adapter surface, not the authoritative lifecycle reason vocabulary.

**Adjudication:** nonblocking message/API residual. A later one-line/message-or-exception cleanup would improve accuracy, but it is not required to close F-1 and must not be conflated with a currentness leak.

## 6. F-2 — remains nonblocking

The prior F-2 finding—unknown extra top-level receipt field is dropped/unhashed—was not modified by R3 and no authority-laundering path was found in this rereview.

Its previous classification remains valid: strict unknown-field closure is an owner/versioning decision, not part of the zero-release fail-closed repair.

## 7. Diff / provenance

`b77937f7f2c79e9007ff7d8cd19061d1758f7f15 -> c690bb0b1e6f071c9a640a6825769b96f30dd79a`

is exactly one commit ahead, zero behind.

Changed production/test terrain:
- `rawlsing_next/pre553_authority_maintenance.py`;
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`;
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`;
- `WORKER_RETURNS/PYAT-C1-03R-ZERO-RELEASE-CURRENTNESS-R3/**`.

The two modified test files only add F-1 courts; no prior tests are deleted.

Verified unchanged blobs:
- `rawlsing_next/pre553_analytical_replay_dependency.py` — `47e65aad5e0a8df7af6fda72fc8807a002e556ce`;
- `rawlsing_next/pre553_replay_audit.py` — `86e0b9c518633735f2527b89fb72fca1a40dc2cc`;
- `rawlsing_next/pre553_analytical_composition.py` — `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`;
- `rawlsing_next/tests/c1_at18_at19_fixture.py` — `cc0015ce9c7e05224ec499f66e893a7ffda1bbe3`.

`rawlsing_next/pre553_analytical_state_and_route.py` is absent from both the R3 base and R3 return trees. The accurate provenance statement is therefore that no C1-03A state/route terrain is present or introduced on this branch, rather than that a blob was modified or reverified.

## 8. Court reconciliation

Recorded exact four-suite court:

**167 passed, 0 failed, 0 errors, 0 skipped.**

Independent static reconciliation:

- analytical replay dependency: 40 test functions, with one 4-case parametrized court → **43**;
- authority maintenance: 54 test functions, with one 4-case parametrized court → **57**;
- replay audit: 23 test functions, with two 12-case selector courts, one 3-case provenance court and one 8-case nonpositive-state court → **54**;
- analytical composition: 12 test functions, with one 2-case AT07 court → **13**.

Total:

`43 + 57 + 54 + 13 = 167`.

No fresh runtime execution was available in this Browser/GitHub rereview lane. The decision-critical F-1 behavior is directly established by the committed branch logic; execution provenance is supported by the reconciled worker receipt.

## Scope ceiling

This approval is only for the declared C1-03R R3/Astra source-free lifecycle grain.

It does not authorize:
- merge or self-adoption;
- C1-03 join;
- raw-source execution;
- broader schema-version redesign;
- any reopening of C1-03A/C5/V3 work.

## Final

F-1 is closed. Post-release lifecycle law remains intact. All previously approved R2/Astra boundaries survive the R3 change.

The inaccurate `OwnerUnknownDependent` message/class-code surface is explicitly **NONBLOCKING** because the owner state and owner reason code are correct and the adapter fails closed; it cannot produce a current product or alter governed lifecycle identity.

**Disposition:** `APPROVE_AT_DECLARED_GRAIN`

**Terminal:** `C1_03R_R3_FINAL_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
