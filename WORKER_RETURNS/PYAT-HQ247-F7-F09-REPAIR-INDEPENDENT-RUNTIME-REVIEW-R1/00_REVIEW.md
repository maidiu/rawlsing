# PYAT HQ247 — F7 HQ246 F09 REPAIR FROZEN INDEPENDENT HOSTILE REVIEW — R1

**DISPOSITION:** `F7_F09_FROZEN_INDEPENDENT_HOSTILE_BLOCKED__NAMED_DEFECT`

**LANE:** `agent/reviewer-pyat-hq247-f7-f09-repair-independent-runtime-r1`
**REVIEW HEAD:** `37932e02a3cc2fabba012defb5315ac7cfed5ad6`
**FROZEN SUBJECT:** `agent/space-bunny-pyat-hq246-f7-native-ab-memory-boundary-repair-r1 @ f09bc827c1a4d77dd2b51834cd5eeeb8969f5b96`
**CONCURRENT R2 REPAIR:** not read, not merged, not certified
**WORKTREE:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq247-f09-review` (isolated)
**INTERPRETER:** governed CPython 3.11.3, sha256 `11d6f541…`, pytest 9.1.1
**MODE:** READ-ONLY / NO REPAIR / NO SELF-ADOPTION / NO BINARY COMMIT

---

## 1. Bottom line

The f09 repair is **real where it claims to be real, and the author was honest about being
partial — but the frozen candidate is still BLOCKED**. D1 (constructor out-of-bounds),
D2/D3 (leaks), D5 (GC), D6 (Stage A registry custody), D7 (Stage A seam) and D8 (payload
drift) are independently confirmed fixed. However the **positive and replay paths still
crash** (B2 `PyObject_Call` misuse, B3 `PyErr_Fetch(NULL)`, B4 null `strlen`) and **positive
parity still fails** (P1: native `DISTINCT_BY_DEFAULT` where Python returns `AUTHORIZED`).
The named `decide()` leak is confirmed and I localise it to a specific line.

## 2. Build / blobs / courts — reproduced

| Check | Result |
|---|---|
| Stage A source sha256 / blob | `12a03d06…` / `a1d70d3c…` — matches |
| Stage B source sha256 / blob | `66f9ad9f…` / **`586f859a…`** — matches the commission-watched blob |
| repair court sha256 / blob | `933cc41d…` / `b5e1f01c…` |
| rebuild from committed C | Stage A **`1712abb6…`**, Stage B **`44b4e329…`** — **match author**, no warnings |
| fault macro strings | 0 in both normal binaries |
| courts | A 39 · B 41 · repair 59 · P07 24 · F7 163 = **326 passed** |

## 3. Repairs independently confirmed

- **D1 — genuinely fixed.** Both modules now use `PyList_CheckExact`/`PyTuple_CheckExact` and
  derive every bound from `PySequence_Fast_GET_SIZE`. Every lie variant I wrote (list/tuple,
  over/under/raise/negative, relations and authority snapshots) is refused with a typed
  exception, **exit 0**, and **zero ASAN reports**. Silent truncation is unreachable.
- **D2** Stage A `custody_diagnostic`: **0.0003 blocks/call** (author <0.01).
- **D3** failed `__init__` over 20 000 iterations: Stage A refcount growth **0**, Stage B
  pinned-callable growth **[0,0,0]**.
- **D5** owner is GC-tracked; **300/300** owner→relation→holder→owner cycles collected.
- **D6** Stage A refuses `authority_registry=42` (TypeError).
- **D7** Stage A's spy seam is invoked once at admission and again at resolve (1 → 2 calls).
- **D8** an attacker stand-in with an inconsistent projection is refused at `resolve_exact`.

## 4. Still-open blocking defects

| ID | Site | Measured |
|---|---|---|
| **B2** | `stage_b.c:1206` `PyObject_Call(self->t_require_positive, S->snap, kw)` (non-tuple args) | forced genuine positive → **SIGSEGV exit 139**; ASAN `PyObject_Call ← validate_positive ← stb_decide` |
| **B3** | `stage_b.c:1210` and `:1592` `PyErr_Fetch(&pt,&pv,NULL)` | same crash family; NULL `p_traceback` write |
| **B4** | `stb_validate_replay:1752-1755` → `build_replay_preimage:1249` `PyUnicode_FromString(NULL)` | malformed decision dict → **SIGSEGV exit 139**; ASAN `strlen ← PyUnicode_FromString ← build_replay_preimage` |
| **P1** | `admit_relation:663-666` hardcoded `effective_scope='DISTINCT_BY_DEFAULT'`, `directionality='SYMMETRIC'` | Python `AUTHORIZED` vs native `DISTINCT_BY_DEFAULT`, `parity_holds=false` |
| **T1** | caller-chosen callables/classes | attacker owner seals (counts `(1,1)`, 64-hex custody); only a TCB-assumed test seam |
| **OPEN-001** | `stage_b.c:1517` `sources = PyList_AsTuple(sources);` | **17.0 blocks/call** (author ~15), fully confined to the ordering block (0.0008 before it) |

`AUTHORIZED`, the `validate_positive`-derived ladder states and multi-positive
`CONFLICTING_AUTHORITY` are therefore **unreachable without crashing** and are not PASS.

## 5. Memory notes

- `resolve_exact` shows a sub-linear residual (0.13 → 0.02 blocks/call as N grows) consistent
  with interpreter lazy state; I do **not** call it a leak and do not falsify the author's
  0.000 claim for that path.
- D4 (module-init OOM) remains source-justified only, as the author disclosed.

## 6. Baseline / digest — the 61/54 conflict fully reconciled

| Run | Command | Result |
|---|---|---|
| A author-exact (9 exclusions + 3 native-court ignores) | `-p no:randomly --continue-on-collection-errors` | 45 failed, **2691 passed**, 7 errors |
| B nine-exclusion baseline (native courts included) | the nine `--ignore` flags | 45 failed, **2830 passed**, 7 errors |

- Run A reproduces HQ242's headline exactly, and **the same run yields both digests**:
  raw stripped lines (54 items) = **`278854ee…`** (the accepted value) and deduped node ids
  (52 items) = **`ab74b05d…`** (the author's value).
- The "residual two items" the author could not resolve are **exactly the two nested-subprocess
  lines leaked by two unrelated failing tests** (a duplicate `FAILED` line and an
  `ERROR: file or directory not found:` line). It is a normalisation convention difference,
  not a failure-set difference.
- Run B: 2830 = 2691 + 139 (39 + 41 + 59); the failure/error set is byte-identical; neither
  native module appears in any failure or error; collection rises 2743 → 2882 (+139, +0 errors).
  **Zero regression from the repairs.**
- Ceiling: machine-local governed evidence; no dependency installed.

## 7. Negative ceiling preserved

Quarantined; no production import; production P07/F7 blobs unchanged; no binaries committed;
no F7-RR-04G closure; no four-forgery or five-positive F7 integrated proof; no F8/actor
authority; no Stage C authorisation. This review does not authorise production cutover and
does **not** transfer to any later repaired SHA.

## 8. Disposition

`F7_F09_FROZEN_INDEPENDENT_HOSTILE_BLOCKED__NAMED_DEFECT`
