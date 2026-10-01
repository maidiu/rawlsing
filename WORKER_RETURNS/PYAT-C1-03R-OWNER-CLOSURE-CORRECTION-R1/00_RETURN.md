# PYAT C1-03R — OWNER-CLOSURE CORRECTION — R1 — RETURN

**Disposition:** `EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED`

**Terminal:** `C1_03R_OWNER_CLOSURE_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`

Branch: `agent/deepseek-pyat-hq149-c1-03r-owner-closure-correction-r1`
Commission tip: `f3a4e8e8a85967a9a0571f48c9aaf61fa3bbb391`
Defective return base: `1c2c0e4ba7f0f9a273b0387a887ed74871e981e9`

This is a correction, not a reimplementation. The original return packet is preserved
unchanged as forensic evidence. No merge, no self-adoption, no second lifecycle.

---

## 1. Bottom line

Four of five blockers are **corrected**. The fifth exposes a genuine, narrowly-scoped
**owner representation gap**, so the ordered typed blocker is returned rather than
patched around.

| Blocker | Status |
|---|---|
| `C1-03R-HQ-BLOCK-LIFECYCLE-OWNER-001` | **CORRECTED** — adapter delegates to the owner |
| `C1-03R-HQ-BLOCK-FUTURE-DETERMINANT-EDGE-002` | **CORRECTED** — only consumed determinants registered |
| `C1-03R-HQ-BLOCK-NONCURRENT-INVENTION-003` | **OWNER GAP CONFIRMED** — invented vocabulary removed, gap returned |
| `C1-03R-HQ-BLOCK-RETAINED-ANSWER-004` | **CORRECTED** — runner input vs oracle separated |
| `C1-03R-HQ-DOC-COUNT-005` | **CORRECTED** — one consistent final run |

## 2. LIFECYCLE-OWNER-001 — corrected

The adapter no longer performs the invalidation lifecycle. It does **not** compute
affected/unaffected sets, does **not** invoke recompilers on its own initiative, and
does **not** construct `AuthorityInvalidationReceipt`. It delegates:

```
transition_analytical_dependencies(...)
  -> AuthorityMaintenanceExecutor.promote_current(..., recompiler=<callable>)
  -> AuthorityMaintenanceExecutor.invalidation_receipt_for_release(release.ref)
```

A static court now asserts the adapter source contains no `def _recompile`,
`def promote_current`, `def rollback_current`, `def adjudicate_candidate`,
`def seal_revision`, `def intake_candidate`, and no `AuthorityInvalidationReceipt(`
construction — while *requiring* that it delegates via `promote_current(` and
`invalidation_receipt_for_release(`.

## 3. FUTURE-DETERMINANT-EDGE-002 — corrected, with a finding worth HQ's attention

The old product is now registered with **only the determinant it actually consumed**.
The future revised authority is never pre-bound, and the recompiler no longer guesses
from tuple position: it matches the owner-reported changed authorities against the
affected product's own consumed determinant **identity** (`authority_id` +
`authority_version`).

**I was wrong in the previous lane, and the correction is stronger than the blocker.**
I initially believed the owner could only reach the product if the future authority were
pre-registered. That is false: `promote_current` passes
`changed = (previous_current, new_snapshot)`, so the *prior* revision is in the changed
set and the **consumed-determinant edge alone** makes the real dependency reachable:

```
changed_authority_refs = [C1-AT07-MODEL-FORWARD 1.0.0, C1-AT07-MODEL-FORWARD 2.0.0]
affected   = urn:test:c1-03r:composed:forward
unaffected = urn:test:c1-03r:composed:reverse
```

Pre-binding was never necessary. The manufacturing of reachability is gone entirely.

## 4. NONCURRENT-INVENTION-003 — owner gap confirmed

`C1_03R_NONCURRENT_PRODUCT` and the `NO_CURRENT` sentinel are **fully removed**. Nothing
is fabricated. When an affected product has no lawful replacement the adapter raises
`NoLawfulReplacementRepresentable` and stops.

The gap is proven by an executable counterexample:

| Path | Call | Observed |
|---|---|---|
| A | `promote_current(seal, …, recompiler=None)` | `AuthorityMaintenanceError: affected dependents require an explicit deterministic recompiler` |
| B | `promote_current(seal, …, recompiler=identity)` | `AuthorityMaintenanceError: affected dependent recompilation must produce a new exact ref` |

`AuthorityInvalidationReceipt` requires `recompilation_pairs` to cover **exactly** the
affected set, and `_recompile` requires every affected dependent to move to a **new**
exact ref. So an honest "no replacement" answer has no lawful representation: the owner
either refuses outright or demands a fabricated ref. Extending the adapter would mean
inventing the vocabulary the commission forbids. **`EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED`.**

Scope is narrow and does **not** affect reaching real dependencies: the main transition
is lawfully expressible (section 3). What is missing is a lawful owner-level
representation for "affected but not replaceable".

## 5. RETAINED-ANSWER-004 — corrected

Runner input and oracle are now separate objects:

- `retained_determinants()` → `C1_03R_RETAINED_DETERMINANTS_INPUT@2`, containing only
  exact refs needed to reconstruct and re-execute the accepted path. No
  `expected_output_identity`, no result/evidence/fact ref, no denominator support, no
  geometry.
- `oracle_expected_output()` → `C1_03R_AT18_EXPECTED_OUTPUT_ORACLE@1`, held court-side
  and **never** handed to the runner.
- The runner calls `assert_runner_input_carries_no_answer()` on load
  (`RUNNER_INPUT_CARRIES_ANSWER`), and a static court proves its source never mentions
  `expected_output_identity`.

Fresh-process recomputation through `compose_positioned_subject_possibility` is
preserved and reproduces the identity exactly
(`7c92484d33d85caa993b767f9f2f31ee23e09d552c5a79449248bc1f3e662287`, 60 → {yes 54, no 6}).

## 6. DOC-COUNT-005 — corrected

This packet records one internally consistent final run. Every count, duration and
command agrees with `07_FINAL_PYTEST_OUTPUT.txt`.

## 7. Exact final run — 109 passed

```
python -m pytest \
  rawlsing_next/tests/test_pre553_analytical_replay_dependency.py \
  rawlsing_next/tests/test_pre553_authority_maintenance.py \
  rawlsing_next/tests/test_pre553_replay_audit.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py -v

109 passed in 17.18s
```

| Court | Tests |
|---|---|
| `test_pre553_analytical_replay_dependency.py` | 21 |
| `test_pre553_authority_maintenance.py` | 21 |
| `test_pre553_replay_audit.py` | 54 |
| `test_pre553_analytical_composition.py` | 13 |
| **Total** | **109 passed, 0 failed, 0 errors, 0 skipped** |

### Missing-edge hostile (salvage condition met)

The lawful graph contains only real consumed-determinant edges, then the edge is
omitted. The product ref remains **present** in `known_dependent_refs` while closure
fails with `MISSING_CROSS_OWNER_EDGE`: cache/object presence cannot restore authority,
and no dependency is inferred. A control confirms closure holds when the lawful edges
are present.

## 8. Owner preservation and write terrain

`pre553_authority_maintenance.py`, `pre553_replay_audit.py` and
`pre553_analytical_composition.py` are byte-identical to the commission tip (verified by
`git hash-object`). No accepted-owner change was made. C1-03A and N10E terrain untouched.

Modified/created (all inside the commission's write terrain):
`rawlsing_next/pre553_analytical_replay_dependency.py`,
`rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`,
`rawlsing_next/tests/c1_at18_at19_fixture.py`,
`rawlsing_next/tests/c1_at18_at19_fresh_process_runner.py`,
`WORKER_RETURNS/PYAT-C1-03R-OWNER-CLOSURE-CORRECTION-R1/**`.

## 9. Disclosed limitation (not papered over)

The AT19 transition proof is asserted at the **owner-graph level**. During correction I
found that `AuthorityCandidate` mints its `authority_content_hash` from *candidate*
material, not from the analytical model law, so a sealed synthetic revision does not
carry a distinct analytical law identity in this fixture. A sealed revision therefore
recomposes to the baseline analytical identity, and the owner correctly rejects it as
"not a new exact ref".

This is disclosed rather than hidden because it is **itself an instance of the returned
owner gap**: the owner's authority identity and the analytical law identity are not
coupled. HQ should read it as supporting evidence for the gap, not as a passing AT19
identity proof.

## 10. Not claimed

- No AT33 progressive multi-conditioner world conditioning; no real-source qualification or live occupancy.
- No structural-world or AT31/AT32 completion; no V3 actor/person state.
- No multi-conditioner or joint dependency closure.
- No new semantic/comparability/model authority; no second lifecycle owner; no merge, no self-adoption.

## 11. Next

HQ adjudication of the returned owner gap, and a decision on whether to extend
`AuthorityInvalidationReceipt` with a lawful noncurrent/deferred representation for
unreplaceable affected dependents.
