# F6L Phase B — independent review receipt

**F6K return reviewed:** `537cb5195bf4f51ee4abc0ce097155c3a3a69291`
**Phase-A freeze:** `f1dfcc5363aed5c4eef42f938ea1a90971d49175` (pushed before
F6K content was read)
**Native producer:** `fc5e37fa5b2f0eb689593b42d95479d1327cb94c` at
`1428c2e92bce1a49efd87378cb23df936d646dc5`

## A. F6K return audit

`03_PHASE_B/00_F6K_RETURN_AUDIT.json` records:

- F6K tip `537cb5195`, status `F6K_TYPED_HOLD__SIX_DEFECTS_LOCATED_AND_MAPPED__NO_REPAIR_CODE_SHIPPED`.
- F6K return files: `00_REPAIR_STATUS.md`, `01_DEFECT_REPAIR_MAP.json`; no
  Python files.
- `repair_code_shipped=false`, `suites_executed=false`, no native producer
  changes.
- F6J `825b2d80` is delta-only (`05_REMOTE_VERIFICATION.json`); its freeze
  `e476ccc` is an ancestor.
- Native producer is absent at the F6L sealed startup and present as the
  pinned blob in the F6C tree.
- Code-site attribution: decision defect at producer line 343; baseline and
  transport admission bypass at lines 210/221; mapped-node ceiling omission at
  lines 259–262; total-stratum support gate at line 282; author path-suffix
  control at author-court line 69.
- F6K's map points defects 1–5 at `f6c_worlds.py`/vague "consumer" rather than
  the producer. Defect 6 is correctly the author court's custody assertion.

## B. Executed courts (real commands, real JUnit/logs)

| Court | Command (abridged) | Result | JUnit/log |
|---|---|---:|---|
| F6J 82 rational | `python3 -B 03_SCRIPTS/execute_native_vs_frozen.py` | **82/82** | `01_SOURCE_TRANSPORT/F6J_RUNTIME/07_EVIDENCE/native_vs_frozen.json`; `05_LOGS/f6j_native_vs_frozen_82.log` |
| F6J 53 adversarial | pytest on F6J `04_TESTS/test_f6j_adversarial.py` | **53/53** | `04_JUNIT/f6j_adversarial_53.xml` |
| Inherited S03FO | pytest on F6J `04_TESTS/run/.../test_pre553_heterogeneous_synthesis.py` | **24 tests + 11 subtests = 35/35** | `04_JUNIT/inherited_s03fo_35.xml` |
| F6C author 57 | pytest on `F6C_RUNTIME/02_TESTS/test_f6c_frozen_court.py`, `PYTHONPATH=F6C_RUNTIME/05_NATIVE_STAGE` | **57/57** | `04_JUNIT/f6c_author_57.xml` |
| F6C author 57, foreign stage | same court with `PYTHONPATH=01_STAGED_NATIVE` | **56/57**; only path-suffix control fails | `04_JUNIT/f6c_author_57_foreign_stage.xml` |
| F6L Phase A | pytest on `02_PHASE_A/04_TESTS/test_f6l_phase_a.py` | **15 passed / 11 failed** (expected unsafe defects) | `04_JUNIT/f6l_phase_a_attacks.xml` |
| F6J falsifier script | `python3 -B 03_SCRIPTS/falsifier_attacks.py` | 7 findings | `05_LOGS/f6j_falsifier_attacks.log` |
| F6J admission script | `python3 -B 03_SCRIPTS/admission_and_consumer_attacks.py` | 7 findings | `05_LOGS/f6j_admission_consumer_attacks.log` |

The F6C author court is run from **relative byte-pinned copies** at the
candidate-shaped `05_NATIVE_STAGE` path. This proves the pinned blob can be
tested without the original machine-absolute symlink. It does **not** repair
the author test's path-suffix assertion: at a foreign stage the same court is
56/57, and the single failure is exactly that assertion. F6L did not edit the
author test or the frozen expectations.

## C. Phase A actual results

The 11 failures are the preregistered unsafe behaviours:

1. P1 original uncovered world: `SYNTHETIC_CANDIDATE` with `distribution=None`.
2. P2 novel 2×2 uncovered third: same.
3. P3 novel 3×2 uncovered quarter: same.
4. P4 forged `admit=True`: real-use ceiling from an unverified boolean.
5. P5 `test_origin=True`: callback skipped; test-only nodes still claim real use.
6. P5B mixed origin: unverified declared-test source included in a real-looking
   output with real-use ceiling.
7. P7 `mapped:*` nodes missing `authority_ceiling`/`value_hash`.
8. P7 mapped/target authority hierarchy cannot be established.
9. P7 test-only graph contains real-use ceiling.
10. P8 threshold 150 excludes S1, silently renormalizes to S2-only `1/4`, and
    the consumer returns `SUPPORTED_MODEL`.
11. P9 decision-only consumer consumes a null distribution as complete.

The passes preserve what must survive: P1/P2/P3 exact arithmetic and bounds,
P4 callback-seam observation, P5 admission bypass fact, P6 fail-closed,
P10 source substitution, P11 complete positive and conditional, and Fréchet
limits.

## D. Changed / unchanged receipt

Because F6K shipped no code:

- **Changed worlds:** none.
- **Unchanged:** all confirmed arithmetic (F6J 82/82; P1/P2/P3/P10/P11 exact)
  and all six defects.
- **No World-B-changed / World-A-stable repair pair exists.** F6K did not
  produce one.

This is a Phase-B **non-acceptance**, not a failure of the arithmetic. The
arithmetic is confirmed; the candidate's decision/admission/authority contract
is not safe, and no repaired artifact was submitted.
