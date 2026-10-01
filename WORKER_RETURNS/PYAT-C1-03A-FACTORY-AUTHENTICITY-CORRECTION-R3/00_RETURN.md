# PYAT C1-03A — FACTORY AUTHENTICITY CORRECTION — R3 — RETURN

**Disposition:** `PASS_C1_03A_FACTORY_AUTHENTICITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
**Terminal:** `C1_03A_FACTORY_AUTHENTICITY_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`
**Branch:** `agent/opencode-pyat-hq153-c1-03a-factory-authenticity-correction-r3`
**Base:** `ad67be387fd9da350f07858b41729309e1c2e67f` (R2 tip)
**Commissioned tip:** `b885227b1b3f0ccaa8c892357dfc40251ab1d1cc`

No merge, no self-adoption. No semantic design reopened. No R1/R2 valid work regressed.

---

## 1. Method: reproduce first, then repair

I did not take HQ's word for any of the three blockers. Before touching a line, I ran
the ten-file court unmodified at the commissioned tip (**185 passed, 0 failed**) and
then ran a standalone reproduction harness against that unmodified owner.

**All twelve counterexamples reproduced exactly.** After the correction, the same
harness returns a refusal for every one of them.

### Reproduction, before repair

| # | Blocker | Counterexample | Result |
|---|---|---|---|
| E1 | E | duck-typed `EmpiricalFact` | **MINTED** `retained=SUPPORTED` |
| E2 | E | duck-typed `DiscoveryResultReceipt` | **MINTED** `retained=OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` |
| E3 | E | duck-typed `AdaptiveSearchResult` | **MINTED** `retained=UNVISITED`, caller-minted determinant ref |
| E4 | E | duck-typed `AdmissionEvaluation` | **MINTED** `decision=ADMITTED positive=True` |
| F1 | F | `owner=` on empirical projection | **MINTED** `rawlsing_next.not_a_real_owner.fabricate` |
| F2 | F | `owner=` on discovery projection | **MINTED**, differs from baseline |
| F3 | F | `owner=` on adaptive projection | **MINTED**, differs from baseline |
| F4 | F | `producer_ref=` on adaptive projection | **MINTED** — replaced the owner's own determinant ref |
| F5 | F | `required_supporting_refs=` into custody | **MINTED** — custody hash changed |
| G1 | G | real positive receipt + forged decision | **MINTED** — receipt said `ADMITTED`, obligation said `INTEGRITY_FAILURE` |
| G2 | G | real positive receipt + forged reason | **MINTED** `CALLER_CHOSEN_REASON` |
| G3 | G | forged blocking refs | **MINTED** — 1 receipt blocker became 2, injection accepted |
| G4 | G | ADMITTED receipt + contradictory `requested_use` | **MINTED** — `requested=COMPLETELY_UNRELATED_USE positive=True` |
| **G5** | **G** | **real NEGATIVE receipt + forged `ADMITTED`** | **MINTED** `decision=ADMITTED positive=True` |

### G5 is worse than anything HQ listed

HQ listed four G counterexamples. Reproduction found a fifth and more dangerous one:
wrap a **genuine negative** receipt in a hand-built `AdmissionEvaluation` that asserts
`ADMITTED`, and the factory mints a **positive** route obligation out of a refusal. G1
only mislabels a positive as negative — internally consistent-looking but inert. G5
manufactures positive authority where the owner produced none, and it would then pass
`require_positive_route`. It is now closed, and it has its own hostile.

I flag this explicitly because it was not in the commission: rereview should test G5
first, since a miss there is the most consequential available failure.

---

## 2. Corrections

### Blocker E — exact competent owner families only

One gate, `_require_exact_owner_object`, applied at every boundary. It uses **exact
type identity**, never `isinstance`, never duck typing.

| Factory | Required exact type |
|---|---|
| `from_empirical_fact` | `pre553_empirical_objects.EmpiricalFact` |
| `from_discovery_receipt` | `pre553_empirical_objects.DiscoveryResultReceipt` |
| `from_adaptive_result` | `pre553_discovery_adaptive.AdaptiveSearchResult` |
| `from_structural_admission` | `pre553_structural_admission.AdmissionEvaluation` + `StructuralEmpiricalAdmission` for the receipt |

Exact identity was chosen because it is the **narrowest** fail-closed check consistent
with current owner law, and because `isinstance` is demonstrably wrong in this codebase
already — R2 established that `Pre553AuthorityError` subclasses `Pre553IntegrityError`,
so an `isinstance` gate would silently collapse two mandatory states. The same trap
applies here. A court proves a caller-defined **subclass** of an owner family is
refused too, so the gate cannot be sidestepped by inheritance.

### Blocker F — owner labels and provenance are factory-fixed

- The `owner=` parameter is **removed** from all six projection/obligation factories
  **and both exact refusal factories**. Each hardcodes its own `OWNER_*_PROJECTION_LABEL`.
- `from_adaptive_result(producer_ref=...)` **removed**. The determinant ref comes only
  from `AdaptiveSearchResult.determinant_state_ref`. The exact owner checkpoint,
  visited and unvisited refs are still preserved — the R2 fix is kept.
- `RecursiveCoverageCustody.from_handoff(required_supporting_refs=...)` **removed**. The
  custody already binds the exact handoff ref, the exact evaluated frontier, and the
  handoff's own retained scope/frontier identity; every one of those is owner-derived, so
  admitting more would only ever add evidence the owner never produced.
  `supporting_refs` stays in the identity shape but is always empty, so custody hashes
  remain comparable with R2.

### Blocker G — the receipt dominates the envelope

Every authoritative route fact is now read from the canonical
`StructuralEmpiricalAdmission` receipt: decision, reason, target use, empirical fact
ref, admission authority, receipt ref, rule hash from the **positive** interpretation
payload, and blocking refs from the receipt's exact applicable
negative/denial/noncomparability refs.

The `AdmissionEvaluation` is admitted only as an **execution envelope** whose duplicate
`decision_state`, `reason_code` and `blocking_refs` agree with the receipt exactly.
Any disagreement fails closed rather than being stored. Blocking refs compare as exact
ref-key **sets**, so the receipt's canonical set re-ordering is not mistaken for a
discrepancy while an injected or dropped ref is.

For `ADMITTED`, contradictory requested-use metadata is rejected outright. For a
nonpositive unresolved receipt, the exact `UNRESOLVED_STRUCTURAL_USE` target is
preserved and the obligation gains no positive route authority.

---

## 3. Court rewrites — two, and why

**No R1 or R2 court was deleted.** Two were rewritten in place because their original
code depended on a channel HQ removed. Both rewrites are strictly stronger, and both are
recorded in the receipts so rereview is not surprised.

1. **`test_repair_blocker1_observed_zero_requires_the_real_cell_projection`** used a
   hand-rolled duck-typed `_NoCells` class — exactly the forgery blocker E forbids. It
   now builds a **real** `EmpiricalFact` from an owner-produced SUPPORTED fact with only
   the cell projection stripped. The type gate is satisfied, so the test now exercises
   the cell-projection law it was written for, on a genuine owner object.

2. **`test_at14_positive_recursive_handoff_is_not_the_coverage_record`** proved custody
   content was bound into the envelope identity by widening `required_supporting_refs`.
   That channel is gone, so the proof is inverted and made stronger: custody is now a
   **pure function of the handoff** — a second derivation over the same handoff yields an
   identical custody hash and an identical envelope identity hash, and the old widening
   keyword raises `TypeError`. There is no caller channel left to vary it.

---

## 4. Execution — exact counts

`pytest -q` over **exactly** the same ten files R2 ran, same interpreter
(`/tmp/c1-01-r8-release-spine-venv/bin/python`, Python 3.12.14, pytest 9.1.1):

| File | Count |
|---|---|
| `test_pre553_analytical_state_and_route.py` | 62 |
| `test_pre553_analytical_composition.py` | 13 |
| `test_pre553_analytical_composition_higher_order.py` | 35 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| `test_pre553_empirical_query.py` | 32 |
| `test_pre553_discovery_exact.py` | 14 |
| `test_pre553_discovery_adaptive.py` | 8 |
| `test_pre553_discovery_adaptive_admission.py` | 3 |
| `test_pre553_recursive_handoff.py` | 2 |
| `test_pre553_structural_admission.py` | 17 |
| **total** | **199 passed, 0 failed, 0 errors, 0 skipped** |

185 → 199: **14 new hostiles** (5 for E, 3 for F, 6 for G), no court removed. Per-file
counts were independently confirmed with `--collect-only` and sum exactly to 199.

The nine R2 trust-boundary courts were re-run by keyword as a preservation check:
**9 passed, 53 deselected, 0 failed.**

**No broader regression sweep is claimed.** No lint or typecheck command is claimed
either — there is no `Makefile`, `pyproject.toml`, `setup.cfg`, `tox.ini`, `.flake8` or
`AGENTS.md` at the repository root, so no configured linter existed to run. The claim
here is pytest evidence only.

## 5. Preserve list

Every item HQ listed is preserved and passing, including the AT16 54/6 SUPPORTED
witness, the eight distinct negative states, the real adaptive `UNVISITED` witness, the
genuine ADMITTED positive route (now additionally pinned by a new hostile), DENY and
failed no-laundering, real positive handoff exact custody, and the
producer → C1 composition → named consumer path. **C1-02 untouched** — no C1-02 module
exists in this tree and none was written.

## 6. Write terrain

Modified, exactly as commissioned:

- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-FACTORY-AUTHENTICITY-CORRECTION-R3/**`

`git diff --stat`: 3 files, +764 / −97. No existing owner was modified. No C1-02, AT17,
C1-03R, C5/C7, raw source or V3 terrain touched.

## 7. Residual limitations, stated plainly

1. **`AdmissionEvaluation` remains a plain constructible dataclass** in its owning
   module. C1-03A cannot make that type unforgeable and I did not modify it — that is
   outside this commission's write terrain. What C1-03A now guarantees is that a
   hand-built envelope can add **no** authority it did not already receive from a
   genuine receipt, because the receipt dominates and disagreement fails closed.
   Whether that is sufficient is precisely the rereview question.
2. **The two exact refusal factories still accept a caller-supplied `producer_ref`.**
   It names the refused owner object rather than choosing a retained state, and HQ
   blocker F did not enumerate it, so I did not change it unilaterally. Flagged for
   rereview rather than quietly widened scope.

## 8. Environment hazard for HQ

The shared working tree at `/Users/matthewsmith/Desktop/Rawlsing` is being moved by a
concurrent controller: mid-task it switched HEAD from my commissioned branch back to
`agent/opencode-pyat-hq151-c1-03r-astra-a-owner-extension-r1`, silently removing my
checkout's files from the worktree view. I completed this commission in an isolated
`git worktree` at `rawlsing-pyat-hq153-c1-03a-factory-authenticity-correction-r3`,
which is this repository's existing per-agent convention. All counts above were produced
in that worktree with `PYTHONPATH` set to its root. HQ should confirm the branch is read
from the worktree, not the shared tree.

## 9. Next required action

Narrow independent rereview of blockers E, F and G. Test **G5** first — the negative
receipt laundered into a positive route — since that is the most consequential available
failure and the one HQ did not list.

```
C1_03A_FACTORY_AUTHENTICITY_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED
```
