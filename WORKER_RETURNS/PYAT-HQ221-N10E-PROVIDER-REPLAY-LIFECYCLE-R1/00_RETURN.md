# PYAT HQ221 — N10E PROVIDER → CONSUMER → LIFECYCLE / REPLAY CLOSURE — R1 RETURN

**DISPOSITION:** `N10E_PROVIDER_REPLAY_LIFECYCLE_COMPLETE__READY_FOR_HOSTILE_REVIEW`
**AGENT:** Space Bunny semantic-sensitive source-free integration worker
**MODEL / INTELLIGENCE:** Space Bunny Max
**BRANCH:** `agent/rabochii-pyat-hq221-n10e-provider-replay-lifecycle-r1`
**EXACT STARTUP TIP:** `c0dd265e3bd590050fc0283bccaf62ba5454a7fa`
**RAW SOURCE ACCESS:** FORBIDDEN — NOT USED
**LIVE C4 / C7:** FORBIDDEN — NOT USED
**SELF-ADOPTION:** NOT PERFORMED

---

## 1. Headline

The named C1 residual is closed. One accepted owner path now carries, **in a fresh
process, from exact determinants**:

```
EXACT DETERMINANTS
  -> provide_empirical_possibility_slice        (N10E provider seam)
  -> compose_positioned_subject_possibility     (accepted analytical producer)
  -> producer-derived PossibilitySliceEvidence
  -> evaluate_positioned_subject_possibility    (named positioned-subject consumer)
  -> provider receipt (exact identity bound)
  -> AnalyticalProductRegistration / determinant graph   (dependency registration)
  -> AuthorityMaintenanceExecutor.promote_current        (accepted lifecycle owner)
  -> resolve_current_analytical_product          (currentness resolution)
```

The slice is **actually recomputed** from competent empirical determinants and then
consumed. No precomputed probability geometry is deserialized or injected as
authoritative input anywhere. No production module was mutated.

**`production_mutation_required = false`.** The current seam was sufficient.

---

## 2. What was actually built

Exactly two new files, both court-side:

| File | Role |
|---|---|
| `rawlsing_next/tests/test_pre553_n10e_provider_replay_lifecycle_court.py` | bounded court, 32 tests |
| `rawlsing_next/tests/n10e_provider_replay_lifecycle_runner.py` | fresh-interpreter runner (single file, dual role) |

The runner is deliberately **one file with two roles** rather than a separate module,
so the commission's write terrain ("one new bounded court") is respected exactly. It
is invoked as `python -m rawlsing_next.tests.n10e_provider_replay_lifecycle_runner`.

**Court result: `32 passed`.**

---

## 3. Startup truthfulness (per the sparse worktree law)

The commission named `CHECKOUT: SPARSE_REQUIRED` but supplied **no prepared worktree
path**. Per `SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md` a worker must not infer
authorization to clone. It did not clone. It resolved its own commissioned branch with a
single minimal `git fetch` (the local object store lacked the tip) and created an
isolated shared-store worktree:

- worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq221-n10e`
- branch / HEAD verified against the commission exactly before any mutation
- `git status --short` clean at startup

The governed **R7 interpreter** (not reconstructed) was used and SHA-256 verified
against the pinned value `11d6f541…f535f6`, carrying pytest 9.1.1.

---

## 4. Mandatory positive proof — all 12 items

| # | Requirement | Result | Court |
|---|---|---|---|
| 1 | runner input contains only exact determinants/authority/release/query/model/witness | PASS | `test_01` |
| 2 | no answer fields (probability, geometry, precomputed evidence, expected identity, fact/evidence ref, denominator oracle) | PASS | `test_01`, `test_02`, `test_h02` |
| 3 | provider invokes the accepted analytical composition path | PASS — **exactly 1** composition call | `test_03` |
| 4 | slice evidence identity is producer-derived | PASS — **object identity**, not hash equality | `test_04` |
| 5 | named consumer actually invoked on generated evidence | PASS — **exactly 1** consumer call, `EXACT_SUPPORTED` | `test_05` |
| 6 | receipt binds query, predicate, releases, model rule, witness, evidence, consumer | PASS | `test_06` |
| 7 | exact product/determinants registered through current replay/dependency machinery | PASS | `test_07` |
| 8 | fresh process reconstructs at the claimed replay grade | PASS — `FRESH_EMPIRICAL_RECOMPUTATION` | `test_08`, `test_08b`, `test_08c` |
| 9 | lifecycle distinguishes current / explicitly noncurrent / unknown dependent | PASS — three distinct states | `test_09`, `test_09b` |
| 10 | invalidating a consumed determinant reaches the exact dependent | PASS — all **and only** affected | `test_10`, `test_11b` |
| 11 | changed determinant cannot replay to the old product identity | PASS — owner rejects a returning recompiler | `test_11` |
| 12 | fresh recomputation proves execution, not stored receipt deserialization | PASS | `test_12` |

### The discriminating core of item 4

Identity is asserted by **Python object identity**:

```python
result.generated_evidence_or_null is result.composition_result.possibility_slice_evidence_or_null
result.consumer_result_or_null      is result.composition_result.consumer_result_or_null
```

A re-wrapped, substituted or caller-supplied slice cannot satisfy this. Equal hashes
would not have been sufficient evidence.

### The discriminating core of item 12

The fresh runner is handed an oracle that **contradicts** a genuine recomputation. It
exits `3` and does **not** echo the stale identity. The matching-oracle control is
accepted. A runner that deserialized a stored receipt could not do either.

Static proof is separate and additional: the runner source contains no
`EmpiricalPossibilitySliceProviderReceipt(`, no `AnalyticalReplayClaim(`, no
`pickle`/`marshal`/`shelve`, and `payload = run(determinants)` provably precedes the
`--expect` oracle read.

---

## 5. Mandatory hostile witnesses — all 12, all discriminating

Both failure modes count as discrimination, and the artifact says which is which:

| # | Attack | Discriminating mode | Observed |
|---|---|---|---|
| H01 | handwritten/precomputed slice geometry | unrepresentable by contract | no geometry channel in the public API; live guard |
| H02 | answer fields in runner input | failed closed | 13 field names + nested + fresh process exit ≠ 0 |
| H03 | stale release ref | failed closed | `AnalyticalCompositionError: SOURCE_RELEASE_MISMATCH` |
| H04 | changed predicate/query determinant | **re-identified** | identity moves; an unrebuilt custody witness fails closed |
| H05 | changed model authority | **re-identified** | product *and* consumer identity both move |
| H06 | changed conditioner-binding witness | failed closed | `CONDITION_VALUE_RELATION_MISMATCH` |
| H07 | missing dependency edge | failed closed | `MISSING_CROSS_OWNER_EDGE` despite object presence |
| H08 | unknown dependent | failed closed | `OwnerUnknownDependent` |
| H09 | explicitly noncurrent dependent | failed closed | `ExplicitNoncurrentDependent` |
| H10 | stale stored receipt as fresh proof | failed closed | `REPLAY_GRADE_OVERCLAIM` + exit 3 |
| H11 | mismatched consumer result identity | failed closed | `receipt/composition identity mismatch` |
| H12 | lifecycle/cache presence restores currentness | failed closed | old product fully recomputable, still not current |

**No witness passes vacuously.** H04/H05 discriminate by genuinely moving the product
identity rather than by raising; H01 is unrepresentable by contract.

---

## 6. Productive adequacy (HQD-216)

`REFUSAL_CORRECTNESS != N10E_COMPLETION`. This lane travels the **positive** path:

- fresh-process provider state `EXACT_SUPPORTED_SLICE_PRODUCED`
- consumer state `EXACT_SUPPORTED`
- lifecycle state `CURRENT`
- **no refusal reached anywhere on the positive path**
- substantive empirical product: denominator **60**, cells **yes 54 / no 6** (exact
  `9/10` and `1/10`), computed *in the fresh process*
- the product **genuinely moved** under the governed authority revision

Safety correctness and positive capability are reported separately, as
information-preserved / information-discarded / refusal-indicating-unfinished-work /
source-intrinsic-nonapplicability.

---

## 7. Owner discipline

**No production file was mutated.** `git diff --stat -- rawlsing_next/*.py` is empty.

Untouched, as required: `pre553_learned_product_lifecycle.py`,
`pre553_learned_product_release.py`, `source_backed_positioned_subject_possibility.py`,
`pre553_analytical_composition.py`. The empirically-correct seam required **no** change
to either permitted-mutation file either.

No new public semantic owner was invented. The adapter is still not a lifecycle owner
(`promote_current(` delegated; `AuthorityInvalidationReceipt(` never constructed), and
the provider is still a seam (`compose_positioned_subject_possibility(` delegated;
no private geometry computation).

---

## 8. Regression check

Full `rawlsing_next/tests` collection was run **twice** — with and without this lane:

- baseline (lane removed): **54** failures/errors
- with lane: **54** failures/errors
- `diff` of the sorted FAILED/ERROR lists: **IDENTICAL**

**Zero regression introduced.** The 54 are pre-existing at the startup tip, lie outside
this commission's write terrain, and were neither fixed nor masked. Nine further files
fail to collect at the tip (they reference files absent from this tree); also pre-existing
and also verified identical with the lane removed.

---

## 9. Honest limits

1. **Source-free.** Synthetic AT07 fixture law plus frozen synthetic C1-00 authority
   snapshots. This lane does **not** establish live survey-source occupancy.
2. **Local-stage acceptance only.** AT17/AT18/AT19 are
   `PROPOSED_ACCEPTANCE_CASE__NOT_EXECUTED` in the atlas. This is evidence toward
   adoption, not adoption.
3. The 54 pre-existing suite failures are outside this lane's terrain and remain open.
4. No `UPSTREAM_REAL_ESTATE_OCCUPANCY` is claimed; per the commission, competent
   source-free retained fixtures are sufficient for local-stage acceptance.
5. `RAW SOURCE ACCESS` and `LIVE C4 / C7` were forbidden and were not used; the run is
   label-accurate reconstructed-source-free evidence, not live occupancy.

---

## 10. Return artifacts

All under `WORKER_RETURNS/PYAT-HQ221-N10E-PROVIDER-REPLAY-LIFECYCLE-R1/`:

- `00_RETURN.md`
- `01_FRESH_PROCESS_INPUT_AND_RECOMPUTATION.json`
- `02_PROVIDER_CONSUMER_IDENTITY_CHAIN.json`
- `03_DEPENDENCY_LIFECYCLE_REPLAY_COURT.json`
- `04_PRODUCTIVE_ADEQUACY_AND_HOSTILE_WITNESSES.json`
- `05_FINAL_DISPOSITION.json`

Court blob identities:
`test_pre553_n10e_provider_replay_lifecycle_court.py` → `44f85296eefff08c977a6dd1021d68f7fb546339`
`n10e_provider_replay_lifecycle_runner.py` → `2343750bcbabfb8773af9ac05922ecbcbcfee53b`

---

## 11. Recommended next step

Independent hostile review of this lane, specifically attacking:

- whether the object-identity assertions in items 4–5 can be satisfied by any
  substitution the accepted owners permit;
- whether `test_12`'s static + behavioural pairing genuinely forecloses a runner that
  recomputes *and* echoes;
- whether the pre-existing 54 failures hide a lane-relevant defect that the frozen
  C1-00/AT07 fixture hides.

HQ decision required.

`HQ221_N10E_PROVIDER_REPLAY_LIFECYCLE_RETURNED__HQ_DECISION_REQUIRED`