# PYAT HQ245 — F7 NATIVE STAGE A INDEPENDENT HOSTILE RUNTIME AND MEMORY-SAFETY REVIEW — R1

**DISPOSITION:** `F7_NATIVE_STAGE_A_INDEPENDENT_HOSTILE_RUNTIME_BLOCKED__MEMORY_SAFETY_OR_CUSTODY_INVALID`

**LANE:** `agent/reviewer-pyat-hq245-f7-native-stage-a-independent-runtime-r1`
**REVIEW HEAD:** `11d7114ca695cf2d2cbd1444cb4a5a4a6a405cc0`
**REVIEWED CANDIDATE:** `agent/space-bunny-pyat-hq244-f7-native-owner-stage-a-custody-resolve-r1 @ 85144216e9ceb58f306d5624620ee42df34d1718`
**WORKTREE:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq245-stagea-review` (isolated; Stage B / HQ244 worktrees untouched)
**INTERPRETER:** governed CPython 3.11.3, sha256 `11d6f541…` — no substitution
**MODE:** READ-ONLY / NO REPAIR / NO PRODUCTION OR COURT MUTATION / NO SELF-ADOPTION

---

## 1. Bottom line

The Stage A **build is genuinely reproducible and deterministic**, the source blobs match the
author's receipts, and the non-authorizing quarantine holds. But the type's own `__init__`
contains a **reachable out-of-bounds read that deterministically segfaults the governed
interpreter** — so the candidate cannot pass a memory-safety review, and Stage B candidacy is
blocked pending repair.

```python
class EvilList(list):
    def __len__(self): return 5        # true length is 1

StageAOwner.__new__(StageAOwner).__init__(
    relations=EvilList([Rel()]), authority_registry=object(),
    trusted_semantic_hash=lambda x: "f"*64)
# -> Segmentation fault: 11   (exit 139, 3/3 runs)
```

ASAN localises it: `SEGV on unknown address 0x8 (READ)` in `PyObject_GetAttrString`, called
from `StageAOwner_init _p07_native_owner_stage_a.c:265`, with the item pointer `rdi = 0x0`.

Two unbounded memory leaks were also found on public paths, and several advertised properties
(registry binding, trusted semantic-hash seam) are nominal at Stage A.

## 2. Build, ABI, source — reproduced

| Check | Result |
|---|---|
| native source sha256 | `9acd1e9a…f2` — matches author |
| Stage A court sha256 | `8230bdfb…7f` — matches author |
| production P07 blob | `8053d30d…` — unchanged |
| production F7 blob | `6f6b462b…` — unchanged |
| committed binaries | none |
| rebuild from scratch (no author `.so`) | exit 0, **no warnings** |
| rebuilt sha256 | `94683dd7…fd04` — **matches** author; 53048 bytes |
| determinism | built twice, byte-identical (`cmp` clean) |
| ABI | CPython 3.11.3, `cpython-311-darwin`, Mach-O x86_64 |
| `-undefined dynamic_lookup` | required; HQ242 finding reproduced |

## 3. Blocking memory-safety defect (HQ245-D1)

`StageAOwner_init` accepts **list/tuple subclasses** (`PyList_Check`/`PyTuple_Check`, not
`CheckExact`, line 236), takes `n = PySequence_Size(relations)` (line 241) — which invokes the
attacker-overridable `__len__` — then iterates `PySequence_Fast_GET_ITEM(fast, i)` for
`i ∈ [0, n)` (lines 259–265) over a `fast` sequence of the **true** length. An over-reporting
`__len__` reads past the end and hands garbage to `admit_one`; a NULL item segfaults.

- Over-report on a `list` subclass: **SIGSEGV, 3/3**.
- Under-report on a `list` subclass: silent truncation (3-element list, `n_relations = 1`).
- `tuple` subclass: OOB read too (raised from garbage), did not segfault in this run.
- The convenience factory `build_stage_a_owner` refuses subclasses (`PyList_CheckExact` at
  line 638) — but the type itself is public, and `__new__` + `__init__` is ordinary Python.

The author's court has a hostile-`__len__` test (line 150) but on a **non-list** duck type
that `PyList_Check` rejects before `PySequence_Size` is reached. So the author's 39/39 is real
for the cases it covers and does not cover this one.

## 4. Other defects and nominal claims

| ID | Finding |
|---|---|
| HQ245-D2 | `custody_diagnostic` builds `rows`, embeds it with `Py_BuildValue("…s:O…")` (which INCREFs) and never `Py_DECREF(rows)` → **unbounded leak**; 20 000 calls left 20 000 tracked lists alive |
| HQ245-D3 | `StageAOwner_init` INCREFs `trusted_semantic_hash` before validation; a later failure leaves the object unsealed, so a repeated failing `__init__` overwrites the field without DECREF → 2 000 failing calls grew the callable refcount by exactly 2 000, and leaked the `rels` array each time |
| HQ245-D4 | module-init second `PyModule_AddObject` failure path double-decrefs the static exception then frees the module → dangling global (OOM-only, source-inspected) |
| HQ245-D5 | no `Py_TPFLAGS_HAVE_GC` / `tp_traverse` / `tp_clear` while holding strong `PyObject*` refs → cycles leak |
| — | `authority_registry=42` is accepted (only `is not None` checked; only `tp_name` stored) → registry binding is nominal |
| — | `trusted_semantic_hash` is **never invoked** (0 calls) → the advertised TCB seam is dead code |
| — | identity re-verification is **string-only**: a stand-in whose `ref.key`/`content_hash` are unchanged but whose semantic payload flips `DENIED → AUTHORIZED_AFTER_SEAL` is still returned as trusted |
| — | `if (Py_TYPE(self) == NULL)` (line 221) is a dead reentrancy check |

## 5. Custody invariants that do hold (attacked, not assumed)

Non-subclassable; `__copy__`/`__deepcopy__`/pickle refused; unsealed `__new__` refuses resolve;
one-shot re-init refused; attribute assignment refused; an empty victim sharing the source's
registry refuses the source ref; feeding an owner as a relation is refused; `decide`/`require`
raise `NOT_IMPLEMENTED_NONAUTHORIZING_STAGE_A`; no positive-authority symbol exists. 300 000
valid resolves, 200 000 malformed resolves and 50 000 malformed constructor calls produced no
crash, and the resolve path shows no memory growth (50 k vs 500 k `maxrss` flat). Those
positives are real — they are simply not sufficient against the constructor bounds defect.

## 6. Fail capability and quarantine

- Standard build: **39/39** Stage A, production **24 + 163 = 187/187**.
- `-DSTAGE_A_FAULT_INJECT` build: **2 failed / 37 passed**, exactly
  `test_native_custody_detects_post_seal_substitute_object` and
  `test_native_custody_detects_post_seal_ref_swap`; restore → **39/39** again.
- The fault macro appears only inside its `#ifdef` in the C source; no committed recipe
  defines it. The binary is not committed.
- Production P07/F7 contain no reference to the native module, and `git diff` for production
  and accepted tests against the Stage A base is empty.

## 7. Broad regression and the digest discrepancy

Three independent runs (governed interpreter, no dependencies installed, nothing silently
excluded):

| Run | Command shape | Result | Normalized set |
|---|---|---|---|
| 1 | HQ244 exact, without Stage A test file | 45 failed, **2691 passed**, 16 errors | 63 lines, `52e07035…` |
| 2 | HQ244 exact, with Stage A test file | 45 failed, **2730 passed**, 16 errors | identical to run 1 |
| 3 | accepted 9-exclusion baseline at this tip | 45 failed, **2730 passed**, **7 errors** | 54 lines, `278854ee…` |

- Collection: **2743 → 2782 (+39)** tests and **9 → 9** errors with/without the Stage A file.
  Stage A adds **zero** errors and **zero** failures; it adds exactly its own 39 passing tests.
- The **accepted baseline digest `278854ee…` reproduces exactly** (run 3) once the same nine
  environmental exclusions are applied.
- HQ244's `16 errors vs 7` is fully explained: its command omitted the nine `--ignore` flags
  and added `--continue-on-collection-errors`, surfacing the nine unimportable files as nine
  collection `ERROR` entries on top of the seven pre-existing runtime errors.
- I could **not** reproduce HQ244's normalized digest `72d0a5ca…` under four natural
  normalizations (I get `52e07035…` for the same command). That is an evidence-documentation
  defect in the HQ244 artifact, **not** a hidden regression, and is named rather than smoothed.
- True ceiling: machine-local governed-interpreter evidence; the nine optional-dependency
  collection errors are real and remain unexcluded only under the HQ244 command shape.

## 8. Not claimed

No adjudicator, no native T2, no F7 four-forgery qualification, no closure of F7-RR-04G. Empty
victim checks are not F7-RR-04G closure. No production/adoption/merge and no repair.

## 9. Disposition

`F7_NATIVE_STAGE_A_INDEPENDENT_HOSTILE_RUNTIME_BLOCKED__MEMORY_SAFETY_OR_CUSTODY_INVALID`

The blocking condition is the reachable native segfault in the constructor; the two unbounded
leaks are named defects that must also be fixed before Stage B builds on this type. No repair
was performed by this lane.
