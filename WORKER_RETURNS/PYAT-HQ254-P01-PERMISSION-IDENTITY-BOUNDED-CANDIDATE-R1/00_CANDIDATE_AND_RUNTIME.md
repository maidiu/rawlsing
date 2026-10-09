# HQ254 P01 — bounded candidate for F8 binding–receipt permission identity coherence

**DISPOSITION: `CANDIDATE_BANKED_AWAITING_INDEPENDENT_REVIEW__NOT_ADOPTED`**
**Terminal:** `HQ254_P01_RETURNED_FOR_HQ_REVIEW__NOT_ADOPTED`

**Branch:** `agent/space-bunny-pyat-hq254-permission-identity-candidate-r1`
**Commission tip:** `428be7595fce3ecf6ae3cb37852bee884d9ce2e1` — verified against live origin ✅
**Candidate is quarantined. No merge, no cutover, no adoption.**

---

## 1. Startup verification

| item | value |
|---|---|
| remote branch head | `428be7595fce3ecf6ae3cb37852bee884d9ce2e1` — **exact match to commission** ✅ |
| startup HQ control | `b986a6ab36312ccff72309f69c45fbbdfd2eb6b6` (present, = `HEAD^1`) |
| semantic PRE-MAIN | `1f47063c3205a45888b3c55e81e7485943ed1390` (unchanged) |
| machine | macOS 13.7.8 x86_64 |
| interpreter / runner | Python 3.11.3 · pytest 9.1.1 (pre-existing local venv, stdlib only) |
| raw SAV / DTA / Library | **not used** |
| production cutover | **none** |

### ⚠ Truthful discrepancy — HQ254 is not yet sealed in `LATEST.json`

The commission says *"resolve `HQ_HANDOFF/LATEST.json` for HQ254 before claiming
authority."* I did, and report the result honestly:

- **No HQ254 checkpoint exists.** The newest checkpoint is
  `20261008-PYAT-HQ253-R01-R02-INTAKE-AUSTRIA-Q59C-PRIMARY-T0-ISSUED-R1`.
- `LATEST.json` `handoff_commit` = `85f2835dc…`, `next_action` =
  `LAUNCH_HQ253_T01_SOURCE_FREE_T0_TEST_ONLY_ON_GOVERNED_LOCAL_HOST__REVIEW_AFTER_RETURN`.
- Pointer law: `LATEST_IS_MUTABLE_POINTER_ONLY__CHECKPOINT_AT_HANDOFF_COMMIT_IS_IMMUTABLE_SEALED_HQ_AUTHORITY`.

So HQ has issued HQ254 but has **not yet sealed an HQ254 checkpoint**. I proceeded under the
sealed commission's own bounded authority, because this lane is explicitly a *quarantined,
non-adopted candidate* that merges nothing and adopts nothing. Flagged rather than papered
over; HQ may wish to seal the HQ254 checkpoint before intake.

## 2. Independent reproduction — T01's court was **absent** here

T01's test file and return directory are **not present at this tip**, so the defect was
reproduced from the adopted owners directly rather than reused. That satisfies the
commission's independence requirement.

**Baseline confirmed unchanged:** binder blob at this tip is
`4ba00b8ecf73f70ad0f6481e255fd0117744418a` — **identical to the baseline T01 recorded**.

### Positive schema verification (not assumed)

- receipt class `CandidateClassApplicabilityReceipt`; `request_key` genuinely contains
  `target_use_permission_refs`
- the receipt itself declares `target_use_permission_refs_are_bound_input_not_a_grant: True`
- outcome `ADMISSIBLE_SOURCE_INDEXED_SET`, coverage `COMPLETE`

### Observed defect

| input | result |
|---|---|
| honest, permissions agree | **BOUND** |
| receipt `perm-A`, binding `perm-B` | **BOUND — DEFECT** |

The divergent `perm-B` was copied **verbatim into the binding's canonical `material()`**, where
downstream attestation would read it as the admitted set.

## 3. The candidate — smallest fail-closed correction

One check, **+33 lines, 0 deletions**, placed immediately after its natural sibling
`BINDING_TARGET_USE_GRAIN_MISMATCH` at refusal site **line 723**:

```
BINDING_PERMISSION_IDENTITY_MISMATCH: binding bound_target_use_permission_refs
['urn:hq254:target_use_permission:p01-perm-B'] do not equal the receipt's
target_use_permission_refs ['urn:hq254:target_use_permission:p01-perm-A']; a binding
may never re-describe applicability that was decided under a different bound
target-use permission set
```

Comparison is **set equality of `ExactRef.key`** (order-insensitive), using the module's own
existing idiom (`{s.key for s in admitted}`).

**Why this is a coherence check and not a widening:** the binder *already* refuses on every
other binding↔receipt grain — request set identity, service id, candidate class, target use,
release. Permission identity was the single field in that family with **no check at all**. This
adds the missing sibling and nothing else. It **grants no permission**, widens no source-scope
power, demands no F8 producer custody, and adds no model use.

| identity | value |
|---|---|
| baseline blob | `4ba00b8ecf73f70ad0f6481e255fd0117744418a` |
| candidate blob | `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` |

## 4. Banked execution

| run | exit | result |
|---|---|---|
| baseline courts, **before** candidate | 0 | **199 passed** |
| new P01 court | 0 | **16 passed** |
| baseline courts, **after** candidate | 0 | **199 passed** ✅ unchanged |
| combined | 0 | **215 passed** |
| wider sweep (f8/applicability/service/C1/source-backed) | 1 | **380 passed**, 9 pre-existing collection errors |
| **negative control**: new court vs unmodified baseline | 1 | **9 failed / 7 passed** |

The 9 negative-control failures are the candidate's genuine discriminators. The 7 that still pass
are positive, schema, back-compat and confinement guards asserting *unchanged* behaviour — so
passing them pre-patch is correct.

The 9 collection errors are missing `pandas`, missing `pyarrow`, and one missing unrelated
harness module — pre-existing on this tree and untouched by this lane.

## 5. Hostile coverage

Refused with the exact named code: unrelated permission · **superset** (invents a permission) ·
**subset** (silently drops one) · partial substitution within a set · dropping one of three.

Controls keeping the finding honest: target use still outranks the new code (sibling not
shadowed); release still fires on its own; mismatch refuses **before any binding object exists**;
the binding still declares permissions as *inputs not grants*.

## 6. Retained hostile counterevidence (for the reviewer)

1. **Order-insensitive comparison is a deliberate choice.** If HQ intends *ordered* equality, the
   check must change. Flagged rather than assumed.
2. **Disclosed precedence change.** The new check sits between target-use and release, so a request
   wrong on several grains reports permission *first*. Honest inputs are unaffected — the check only
   fires on genuine divergence — but this is a real behavioural ordering change the reviewer should
   ratify rather than inherit by accident.
3. **Scope is one field.** This does **not** address the separate provenance/authority custody gap
   banked in the HQ253 T01 return (`e609be4f6…`). That gap remains open and unaddressed.
4. **The receipt's permission set is trusted** as the applicability authority's own decision; this
   candidate does not independently re-derive or re-authorise it.

## 7. Changed terrain — exactly two source paths

| path | change | authorized |
|---|---|---|
| `rawlsing_next/pre553_service_f8_source_scope_binding.py` | +33 / −0 | "Only candidate source edits" |
| `rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py` | new, 16 tests | "one narrowly named test file" |
| `WORKER_RETURNS/PYAT-HQ254-P01-PERMISSION-IDENTITY-BOUNDED-CANDIDATE-R1/` | 4 return files | "own return folder" |

**No other production or test path was modified.**

## 8. No self-adoption

Quarantined candidate only. No merge, no adoption, no cutover, no T1 claim, no EE14 grant, no
custody demand. Stopping for separate sealed HQ intake and an independent post-candidate reviewer.