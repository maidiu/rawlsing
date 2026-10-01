# PYAT C1-03R — GENERIC OWNER FAIL-CLOSED CORRECTION — R2 — RETURN

**Disposition:** `PASS_C1_03R_OWNER_FAILCLOSED_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
**Terminal:** `C1_03R_OWNER_FAILCLOSED_RETURNED__HQ_ADJUDICATION_REQUIRED`
**Branch:** `agent/opencode-pyat-hq155-c1-03r-owner-failclosed-r2`
**Base:** `eb02332c93c6c3927303eefde9dd9ed768bb3480` (R1 tip)
**Commissioned tip:** `88d94930179528ce37daac854a7f6a78f7f0f308`
**Independent review:** `agent/reviewer-pyat-hq154-c1-03r-astra-a-r1 @ 380a79cde63d9ee239e5812f89283e997e16da96` (`CHANGES_REQUIRED`)

No merge, no self-adoption. Nothing reopened: Astra Option A, the sealed-successor
repair, AuthorityCandidate identity, mixed-witness topology, AT18 grade law, replay
audit and analytical composition are all untouched.

---

## 1. Method: reproduce first

I ran the four-file court unmodified at the commissioned tip (**144 passed, 0 failed**,
102.56 s), then reproduced every review finding against that unmodified owner with a
standalone harness. **All eleven counterexamples reproduced exactly.**

### Reproduction, before repair

| Finding | Counterexample | Result |
|---|---|---|
| RVW-001 | duplicate positive rows, same target | **ACCEPTED** 2 rows in → 1 kept, silently collapsed |
| RVW-001 | duplicate positive rows, different targets | **ACCEPTED** — and the **forged successor won**; the owner's own target was discarded |
| RVW-002 | negative row missing `replacement_ref` | **ACCEPTED** — null synthesized from an absent field |
| RVW-002 | negative row forged non-null `replacement_ref` | **ACCEPTED** — forged target silently discarded |
| RVW-002 | negative receipt missing `receipt_schema` | **ACCEPTED** — schema ignored |
| RVW-002 | negative receipt forged `receipt_schema` | **ACCEPTED** — `...@9.9.9` accepted |
| RVW-002 | new-schema fields on positive-only legacy | **ACCEPTED** — silently reinterpreted |
| RVW-003 | owner-unknown dependent lookup | **ACCEPTED** — `lifecycle_state=CURRENT` |
| RVW-003 | cache/object presence | **ACCEPTED** — result unchanged, because it was already unconditionally CURRENT |
| RVW-004 | tampered U omits known sibling | **ACCEPTED** after a fully self-consistent rehash |
| RVW-004 | tampered U adds unknown sibling | **ACCEPTED** after a fully self-consistent rehash |

### Two things worth flagging about the reproduction

**RVW-001's second variant is worse than "duplicate rows are not rejected."** With
differing targets the dict's last-write-wins kept the **forged** successor
(`urn:test:c1-03r:forged:successor`) and discarded the owner's own. So the defect was not
merely a duplicated claim being collapsed — it was a **substitution of the replacement
successor** that then entered the receipt identity and every downstream hash. The refusal
is therefore unconditional on whether the targets agree.

**RVW-004 could not be demonstrated with a naive byte edit.** A tampered `U` changes the
receipt's hash, and the embedded `record_ref` check caught it. That is exactly why the
review said embedded record-ref validation is "necessary but not sufficient". To show the
real defect I built a **fully self-consistently resealed** checkpoint: the tampered
receipt, every release citing it, the entire event chain including subject refs and parent
linkage, the current-release pointers, and the checkpoint hash. Only an independent
re-derivation of A and U can reject that, and before the repair it was accepted.

---

## 2. Corrections

### RVW-001 — duplicate positive replacement rows

`AuthorityInvalidationReceipt.__post_init__` now refuses a repeated source `old_ref`
**before** the `pairs` dict assignment can overwrite one. Refusal is unconditional on
target agreement, with blocker id `C1-03R-OWNER-BLOCK-DUPLICATE-REPLACEMENT-001`.

### RVW-002 — serialized negative fields and schema

`NoncurrentDependentOutcome.from_dict` now **requires** `replacement_ref` to be present
and **exactly null**, and rejects a non-null value instead of overwriting it. That null is
the row's own evidence that no lawful replacement exists; inferring it from an absent field
would let a serialized row assert something the owner never emitted.

`AuthorityInvalidationReceipt.from_dict` now enforces a **mutual-exclusivity** boundary.
The owner emits the noncurrent schema only when at least one dependent is noncurrent, and
emits nothing beyond the historical field set otherwise — so declaring the new schema
requires the exact schema id **and** at least one row, and anything else is legacy
positive-only material. That single rule covers all four required behaviours: rows without
the exact schema reject; missing schema rejects; forged schema rejects; and new-schema
fields or schema presence on positive-only legacy material fails closed instead of being
silently reinterpreted.

The pre-existing embedded `record_ref` validation is retained everywhere and is explicitly
not treated as sufficient on its own.

### RVW-003 — owner-unknown is never CURRENT

New typed lifecycle state `DEPENDENT_LIFECYCLE_NOT_GOVERNED` and new typed adapter failure
`OwnerUnknownDependent`. A ref absent from the determinant graph's own
`known_dependent_refs` now resolves to `NOT_GOVERNED` with
`reason_code=OWNER_UNKNOWN_DEPENDENT`, and `resolve_current_analytical_product` raises.
**Absence of a recorded transition is absence of authority, not evidence of currentness** —
previously it was read as evidence of currentness, which turned every unknown ref into a
positive claim. Currentness is never inferred from cache or object presence.

### RVW-004 — replay must re-derive U

`from_checkpoint` now independently recomputes **both** `A = graph.affected(changed)` and
`U = graph.unaffected(A)` and requires exact equality with both serialized sets. Recomputing
only A made A and U disjoint and jointly exhaustive over K at *initial production* only;
a checkpoint whose serialized U had been shrunk or altered still replayed because nothing
re-derived U. Blocker id `C1-03R-OWNER-BLOCK-CHECKPOINT-TRUSTED-U-001`.

### RVW-003 and RVW-004 are interdependent

I want to be explicit about this rather than let it look like two independent tidies.
**Shrinking a serialized `U` converts an owner-*known* dependent into an owner-*unknown*
one.** So RVW-004's fix stops `U` being tampered with, and RVW-003's fix stops the
consequence from reading as `CURRENT`. Closing either alone leaves a live path, so I closed
them together and recorded the interdependence in `03_CURRENTNESS_AND_CHECKPOINT_RECEIPT.json`.

---

## 3. Execution — exact counts

`pytest -q` over exactly the four commissioned files, same interpreter
(`/tmp/c1-01-r8-release-spine-venv/bin/python`, Python 3.12.14, pytest 9.1.1):

| File | R1 | R2 | Δ |
|---|---|---|---|
| `test_pre553_analytical_replay_dependency.py` | 35 | 42 | +7 |
| `test_pre553_authority_maintenance.py` | 42 | 51 | +9 |
| `test_pre553_replay_audit.py` | 54 | 54 | — |
| `test_pre553_analytical_composition.py` | 13 | 13 | — |
| **total** | **144** | **160** | **+16** |

**160 passed, 0 failed, 0 errors, 0 skipped, 0 xfailed** in 55.64 s. Per-file counts
independently confirmed with `--collect-only` and sum exactly to 160. The historical R1
144 was verified passing *before* any edit and still passes. No existing court was deleted
or rewritten. No broader regression sweep is claimed; no configured lint or typecheck
command exists at the repo root, so no such run is claimed.

## 4. Required hostiles — all sixteen present

| # | Requirement | Court |
|---|---|---|
| 1 | duplicate positive rows, same target | `test_hq155_rvw_001_duplicate_positive_rows_same_target_are_refused` |
| 2 | duplicate positive rows, different targets | `test_hq155_rvw_001_duplicate_positive_rows_different_targets_are_refused` |
| 3 | negative row missing `replacement_ref` | `test_hq155_rvw_002_negative_row_missing_replacement_ref_is_refused` |
| 4 | negative row forged non-null `replacement_ref` | `test_hq155_rvw_002_negative_row_forged_non_null_replacement_ref_is_refused` |
| 5 | negative receipt missing `receipt_schema` | `test_hq155_rvw_002_negative_receipt_missing_schema_is_refused` |
| 6 | negative receipt forged `receipt_schema` | `test_hq155_rvw_002_negative_receipt_forged_schema_is_refused` |
| 7 | positive-only legacy hash compatible | `test_hq155_rvw_002_positive_only_legacy_receipt_is_hash_compatible` |
| 8 | incompatible schema on legacy fails | `test_hq155_rvw_002_new_schema_on_positive_only_legacy_fails_closed` |
| 9 | owner-unknown never CURRENT | `test_hq155_rvw_003_owner_unknown_dependent_is_never_current` |
| 10 | cache presence does not change result | `test_hq155_rvw_003_cache_presence_does_not_change_owner_unknown` |
| 11 | tampered U omits sibling, rehashed | `test_hq155_rvw_004_tampered_checkpoint_u_omitting_sibling_is_rejected` |
| 12 | tampered U adds unknown sibling | `test_hq155_rvw_004_tampered_checkpoint_u_with_unknown_sibling_is_rejected` |
| 13 | promotion mixed outcome passes | `test_hq155_promotion_normal_mixed_outcome_still_passes` |
| 14 | rollback mixed outcome passes | `test_hq155_rollback_normal_mixed_outcome_passes_and_laws_are_shared` |
| 15 | sealed-successor / decoy green | `test_hq155_sealed_successor_is_not_the_decoy_and_binds_exactly` |
| 16 | AT18 grade courts green | `test_hq155_at18_grade_courts_remain_green` |

Court 14 required one **addition** to the fixture module:
`build_mixed_outcome_rollback_transition`, which builds a genuine three-state sequence
(promotion v1→v2, promotion v2→v3, rollback v3→v2). No existing fixture could reach a
rollback whose transitions are genuinely mixed — the existing mixed graph binds products
only to the v1 authority, so a second transition would have produced an empty affected set
and proved nothing. The new helper reuses owner-native builders only, changes no existing
fixture, and asserts the shared owner law per transition: R and N disjoint and together
exactly A; A and U disjoint and together exactly K; no duplicate source row; every
negative row with the single generic disposition, nonempty reason and grounds, and
`replacement_ref is None`; and the schema claimed only because rows really exist.

## 5. Preserve list

Every item HQ listed remains accepted and is asserted: exactly one generic noncurrent
disposition; non-empty exact grounds; no DEFERRED/UNAVAILABLE/DELETED split; errors never
auto-converting to noncurrent; positive-only historical receipt identity (reproduces its
historical ref byte for byte); promotion/rollback shared owner law; current vs historical
exact distinction; sealed successor exact binding; decoy is not successor; mixed AT19
witness; omitted-edge hostile; AT18 replay-grade separation. `pre553_replay_audit.py` and
`pre553_analytical_composition.py` are **not in the diff**. AuthorityCandidate is untouched.

## 6. Write terrain

Modified, exactly as commissioned: `pre553_authority_maintenance.py`,
`pre553_analytical_replay_dependency.py`, `test_pre553_authority_maintenance.py`,
`test_pre553_analytical_replay_dependency.py`, `c1_at18_at19_fixture.py`, plus this return
directory. `git diff --stat`: 5 files, +1034 / −3. C1-03A, AT17, C5/C7, raw sources and V3
untouched.

## 7. Two readings I want rereview to confirm

Both are deliberate and both are defensible; I picked the fail-closed reading in each case
and am flagging them rather than burying them.

1. **A known-but-never-transitioned dependent still resolves `CURRENT`.** The approval law
   lists "known unaffected/current → CURRENT", and a dependent the owner genuinely knows
   about, with no release recorded yet, is correctly "known and ungoverned by anything".
   The stricter alternative is to treat it as `NOT_GOVERNED` too — but that would change
   behaviour for known dependents in executors that have recorded no release, which is
   outside what the review asked me to change.

2. **A receipt declaring the new schema with zero noncurrent rows is refused, not
   normalized.** Since the owner only ever emits `noncurrent_dependents` when rows exist,
   such a receipt is internally inconsistent, and "fail closed rather than silently
   reinterpret" points at refusal. Normalizing it instead would be the other reasonable
   reading.

## 8. Residual limitations

- `AuthorityInvalidationReceipt.from_dict` trusts the declared schema only as a
  **compatibility** boundary. It does not and cannot re-derive whether the R/N/U partition
  is semantically correct from the receipt alone; that remains the owner's transition law.
- `NOT_GOVERNED` and `OwnerUnknownDependent` are new public names. They are additive
  lifecycle vocabulary for a case the owner previously mislabelled `CURRENT` — not a new
  noncurrent disposition, and no split of the single generic disposition.
- The rollback court's per-transition registry rebinding is not incidental: the owner's
  recompiler law requires exactly one consumed determinant in the changed set, so a stale
  registry is itself refused. That is why the three-state sequence needs three registries.

```
C1_03R_OWNER_FAILCLOSED_RETURNED__HQ_ADJUDICATION_REQUIRED
```
