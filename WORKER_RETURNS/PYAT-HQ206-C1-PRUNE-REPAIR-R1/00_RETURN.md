# HQ206 — C1 over-import prune repair — R1

**Disposition: `C1_PRUNE_REPAIR_COMPLETE__READY_FOR_FINAL_ACCEPTANCE`**
**Terminal: `HQ206_C1_PRUNE_REPAIR_RETURNED__HQ_FINAL_REVIEW_REQUIRED`**

Prune-only, as commissioned. No analytical semantics redesigned, no production code
touched, no self-adoption.

## Identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq206-c1-prune-r1` |
| Original commission tip | `32d86985b8af3f2ee175f5a170ee21c7101785b6` (verified exact) |
| Repair base | `88f262b94bbe94cd3e2a8113c8b17d0872c5089c` |
| Independent review | `7f33fdd7964ed9cd4d2a85aaafec79903395a304` |
| HQ206 adjudication | `ee8e7a1aef1b1eba19b8ca0304186636c6f874e` |

## Repair 1 — OVERIMPORT-01 (blocking)

Removed **exactly 54** `UNNECESSARY_OVERIMPORT` files, per
`02_IMPORT_NECESSITY_AUDIT.json` at the review commit:

| Directory | removed |
|---|---|
| `PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1` | 38 |
| `PYAT-C1-00-CONTRACT-CORRECTION-R2` | 4 |
| `PYAT-C1-00-CONTRACT-CORRECTION-R3` | 6 |
| `PYAT-C1-00-CONTRACT-CORRECTION-R8` | 6 |

The partition is exact and closed: the four directories held **63** files before the
prune = **54 removed + 9 preserved**, with **0 unclassified strays**, and exactly **9**
files remain afterwards (4 + 3 + 1 + 1). Nothing else was imported or removed.

## Repair 2 — the five production owners untouched

Blob-identical before and after the prune:

| Owner | blob |
|---|---|
| `pre553_analytical_state_and_route.py` | `3a5e3db8` |
| `pre553_empirical_possibility_provider.py` | `23167aa2` |
| `pre553_authority_maintenance.py` | `547e6bf2` |
| `pre553_analytical_replay_dependency.py` | `47e65aad` |
| `pre553_analytical_composition.py` | `604c8d59` |

## Repair 3 — COURT-RECORD-01 and NECESSITY-WORDING-01 (documentation)

The HQ205 review proved the HQ204 "unreconstructed record" claim **false**. Both
authorities do record all 15 court filenames in machine-readable per-file maps:

- `063ee8b77fc4e05c37456ff0168e946247f919ef` —
  `PYAT-AT17-SUCCESSOR-REQUAL-C1-03-JOIN-RERUN-R1/08_EXECUTION_RECEIPT.json`, field `per_file`
- `c8ce0ea81a2165f37d566f37de788fecedf85051` —
  `PYAT-C1-03-SUCCESSOR-JOIN-FINAL-INTEGRATION-REVIEW-R1/05_TEST_AND_REPLAY_REVIEW.json`,
  field `section8_count_audit.per_file_independently_collected`

Corrected in `00_RETURN.md`, `01`, `03` and `04` of the HQ204 return. The false claim
is withdrawn (original text retained for audit), the residual-arithmetic
justification is marked superseded, and both maps are cited. Necessity is now stated
at **FILE grain** with the explicit nine-file table, replacing the directory-level
"without them the courts fail closed".

## Qualification

| Stage | Result |
|---|---|
| pre-prune baseline | **454 collected, 454 passed**, exit 0 |
| post-prune collect-only | **454 collected** |
| post-prune run 1 | **454 passed**, exit 0 |
| post-prune run 2 | **454 passed**, exit 0 |

### The 54 are provably never opened

An open-audit instrument (patching `builtins.open` and `io.open` via
`sitecustomize`, since `pathlib` routes through `io.open`) recorded every
`WORKER_RETURNS` path the court touches:

- pre-prune: **9** opened, matching the review's `required.txt` **exactly**
- post-prune: **9** opened, equal to the preserved nine
- **0** of the 54 opened, before or after
- **0** opened files outside the nine

The first audit attempt produced an empty log because the shim never loaded. I caught
it, verified the instrument against a probe target, and re-ran — the recorded runs
are the instrumented ones.

### Zero regression, exact-ID

Identical full `rawlsing_next/tests` suite, same worktree and interpreter, before and
after:

| | failed | passed | skipped | errors | unique IDs |
|---|---|---|---|---|---|
| before prune | 178 | 2652 | 1 | 50 | 228 |
| after prune | 178 | 2652 | 1 | 50 | 228 |

**0 new failure IDs, 0 fixed, 228-ID sets byte-identical.** The 178/50 pre-exist at
the repair base in this environment and are identical in both arms.
`--continue-on-collection-errors` was used in both arms, so nothing hides behind an
aborted collection. No failure was retried away.

### Bounded sensitivity check

Removing one preserved required file
(`AT07/.../FORWARD_SUCCESSOR_CANONICAL.json`) breaks the court:
**3 failed, 451 passed**, exit 1 — the expected fail-closed break. It was then
restored and verified byte-exact (`hash-object` == index blob `8143c96e`). The tree
was left clean. The review's collective evidence (all nine removed: 108 failed, 336
passed, 10 errors) covers the remaining eight.

## Environment

The governed R7 venv the review used is **absent from this machine**. Per instruction
I did **not** recreate anything: no clone, no new worktree, no new environment. I
reused the already-disclosed HQ204 reconstruction.

- interpreter: `/var/folders/.../T/opencode/hq204-r9-env/bin/python`
- Python **3.11.3**, matching the disclosed governed base
- exact **13-package** freeze, matching the disclosed governed lock

These are **reconstructed matching-environment evidence, not governed-environment
certification**. The vanished environment is not pretended to exist.

## Holds

No source access, no locator discovery, no warrant issued, no self-adoption, no
analytical redesign, production owners unmodified.

## Terminal

`HQ206_C1_PRUNE_REPAIR_RETURNED__HQ_FINAL_REVIEW_REQUIRED`
