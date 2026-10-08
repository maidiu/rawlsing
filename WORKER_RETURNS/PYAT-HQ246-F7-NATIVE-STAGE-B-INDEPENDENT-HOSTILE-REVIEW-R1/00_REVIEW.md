# PYAT HQ246 — F7 STAGE B FROZEN NATIVE P07 INDEPENDENT HOSTILE REVIEW — R1

**DISPOSITION:** `F7_NATIVE_STAGE_B_FROZEN_HOSTILE_BLOCKED__NAMED_MEMORY_OR_TRUST_DEFECT`

**LANE:** `agent/reviewer-pyat-hq246-f7-native-stage-b-independent-hostile-r1`
**REVIEW HEAD:** `aca358d62e657c6d55369b86aadf85884b2402b6`
**FROZEN CANDIDATE:** `agent/space-bunny-pyat-hq245-f7-native-stage-b-full-p07-parity-r1 @ 0dd0a503882ef777141092d7678285462214a600`
**WORKTREE:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq246-stageb-review` (isolated; the concurrent repair branch was never read, merged or certified)
**INTERPRETER:** governed CPython 3.11.3, sha256 `11d6f541…`, pytest 9.1.1
**MODE:** READ-ONLY / NO REPAIR / NO SELF-ADOPTION / NO BINARY COMMIT

---

## 1. Bottom line

The frozen Stage B candidate is **BLOCKED**. Its build, ABI and custody plumbing reproduce,
its 41-test court passes, and its fail-capability red control works — but the candidate
carries the **inherited HQ245-D1 constructor out-of-bounds read (now measured to segfault in
both dimensions)** plus **three new reachable memory-safety defects on the positive and
replay paths**, and its headline **"byte-exact parity" does not hold for positive decisions**:
native `decide` returns `DISTINCT_BY_DEFAULT` where the Python owner returns `AUTHORIZED`.

## 2. Build / ABI / source — reproduced

| Check | Result |
|---|---|
| C source blob | `2d8ffc68…` @ 1802 lines — matches commission |
| source sha256 | `5563a753…` — matches author |
| rebuild from committed C (no author `.so`) | exit 0, **no warnings**, sha256 **`e7454992…88e7`**, 87 824 bytes — **matches** |
| normal binary fault symbols | 0 |
| ABI | CPython 3.11.3, `cpython-311-darwin`, Mach-O x86_64 |
| Stage B court / Stage A court / P07 / F7 | **41 / 39 / 24 / 163 = 267 passed** |
| fault-inject `-DSTAGE_B_FAULT_INJECT_RESOLVE` | **1 failed / 40 passed** (`…rehash_catches_post_seal_projection_mutation`); restore → **41 passed** |
| committed binaries | none; production P07/F7 blobs unchanged |

## 3. Blocking memory-safety findings (measured, not assumed)

**HQ246-B1 — inherited constructor OOB (HQ245-D1), now reproduced in Stage B.**
`StageBOwner_init` accepts list/tuple **subclasses** (827–829), takes `n`/`m` from the
overridable `PySequence_Size` (850–851) and indexes `PySequence_Fast_GET_ITEM` up to those
counts (863–876).

- relations dimension, real=8 / `__len__`=9 → **SIGSEGV, exit 139, 4/4 runs**; ASAN: `SEGV … 0x9 (READ)` in `admit_relation:453` ← `StageBOwner_init:866`.
- authority-snapshots dimension → **SIGSEGV exit 139** at 8/9 and 16/17.
- other over-reports read out of bounds and then raise `relation[N] must be exact …` (still UB); under-report **silently truncates** custody (3 relations → counts `[1,1]`); raise/negative `__len__` propagate cleanly.
- The author's receipt claims "exact list/tuple admission so no hostile `__iter__`/`__len__`/`__getattribute__` drives admission" — **false at the type `__init__` level**; the court never tests a subclass.

**HQ246-B2 — malformed `PyObject_Call` on the trusted authority callback.**
`validate_positive:1141` calls `PyObject_Call(self->t_require_positive, S->snap, kw)` with an
`AuthoritySnapshot` where a positional **tuple** is required. Forcing a genuine candidate
crashes: ASAN `SEGV (WRITE) in PyObject_Call ← validate_positive:1141 ← stb_decide:1518`.

**HQ246-B3 — `PyErr_Fetch(&pt, &pv, NULL)`.**
`validate_positive:1145` and `stb_decide:1521` pass NULL for `p_traceback`; CPython 3.11 writes
it unconditionally. ASAN shows `SEGV 0x0 (WRITE) in PyErr_Fetch` from both sites.

**HQ246-B4 — `validate_decision_replay` NULL `strlen`.**
A decision dict whose `relation_kind`/`target_use` is a non-str reaches
`build_replay_preimage:1184` `PyUnicode_FromString(NULL)` → **SIGSEGV**; ASAN: `strlen` ←
`PyUnicode_FromString` ← `build_replay_preimage:1184`.

Together B2/B3 mean the native positive path and the `validate_positive`-derived ladder
states are **unreachable without crashing**. `AUTHORIZED` is never produced.

## 4. Named leaks

- Repeated failing `__init__`: callable refcount **+2000 over 2000 iterations** (the five pinned refs and the rels/snaps arrays are overwritten without free).
- `validate_positive` leaks the strdup'd `op` on three early returns (1080/1090/1093).
- `admit_relation` leaks `proj` when the trusted hash fails (485).
- `compute_custody_hash` applies `Py_XDECREF` to a `PyMem_Calloc`'d array (762).
- No GC tracking / `tp_traverse` / `tp_clear`; `ref_dict_copy` calls `as_dict()` twice.

## 5. Parity — the headline claim fails on positives

With a **genuine production relation** and the production callables/classes:

| Request | Python owner | Native owner |
|---|---|---|
| relation's real `effective_scope` | **AUTHORIZED** | **`DISTINCT_BY_DEFAULT`**, reason "no exact positive relation receipt…" |
| `effective_scope="DISTINCT_BY_DEFAULT"` | — | candidate selected → **crash (exit 139)** |

Root cause: `admit_relation` seals the object key from **hardcoded** `effective_scope =
'DISTINCT_BY_DEFAULT'` and `directionality = 'SYMMETRIC'`, ignoring the relation's real values,
so the request key never matches. The author's court misses this because its `require` test is
conditional (`if state != AUTHORIZED: assert require raises`) and its parity test never reaches
the candidate loop. **Multi-positive `CONFLICTING_AUTHORITY` is therefore not merely untested;
it is unreachable in the frozen candidate.** A negative-path divergence also exists: for an
unknown kind plus an unresolvable `relation_ref`, Python raises "unknown P07 relation kind"
while native returns the resolve error.

## 6. Trusted-callback provenance

The three callables and two classes are **caller-supplied**; the constructor only checks
callable-ness/`PyType_Check`, then pins them. Pinning prevents later swapping but does not make
them trusted code. Demonstrated: an owner built entirely from attacker classes and callables
seals, reports a 64-hex custody hash and returns the attacker's relation from `resolve_exact`.
This is acceptable only as a **TCB-assumed test seam**; production adoption needs a
production-owned sealed construction gate.

## 7. Regression / digest

| Run | Command shape | Result | Normalized |
|---|---|---|---|
| author-exact (both native courts ignored) | `-p no:randomly --continue-on-collection-errors` | 45 failed, **2691 passed**, 16 errors | deduped node ids, 61 items, **`72d0a5ca…`** |
| accepted 9-exclusion baseline | the nine HQ230/HQ242 `--ignore` flags | 45 failed, **2771 passed**, 7 errors | raw stripped lines, 54 items, **`278854ee…`** |

- The author's digest **is reproducible** with `grep -E '^(FAILED|ERROR) ' | sed 's/ - .*$//' | sort -u`
  (61 unique node ids). I note this as a **correction to my prior Stage A review**, which had failed
  to dedupe; both digests are internally consistent and the set difference is exactly the nine
  optional-dependency collection `ERROR` entries.
- Stage B adds **zero** failures and **zero** errors; collection goes 2743 → 2823 (+80 = Stage A 39 +
  Stage B 41) with 9 → 9 errors; neither native module appears in any failure or error.
- True ceiling: machine-local governed-interpreter evidence; no dependency was installed and nothing
  was silently excluded.

## 8. Not claimed

No native T2, no four-forgery pass, no five lawful positives qualification, no closure of
F7-RR-04G (remains OPEN), no production integration. The candidate is quarantined and this
lane neither adopts nor repairs it.

## 9. Disposition

`F7_NATIVE_STAGE_B_FROZEN_HOSTILE_BLOCKED__NAMED_MEMORY_OR_TRUST_DEFECT`
