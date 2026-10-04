# PYAT HQ205 — R9 fan-in independent adjudication — R1

**Disposition:** `R9_FANIN_ADJUDICATED__BOUNDED_REPAIR_AND_R7_RESTORE_REQUIRED`

**Terminal:** `HQ205_R9_FANIN_INDEPENDENT_ADJUDICATION_RETURNED__HQ_DECISION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq205-r9-r1`
Commissioned startup SHA: `74e7c6ad56f5a436325c0b950ce8ad4e8216cbab` — **verified equal**
Exact base: `0e8d5bcd98e5aba63cd7312f778dedbfe8b6b646` · Candidate: `dfdf5659fd78e9bc996b07383349094059a5553d`
`SPARSE_REQUIRED` honored — no clone, no full worktree, **no code modified**.

---

## A — R7 denominator: `R7_GATE_SHOULD_BE_REBASED_TO_CURRENT_CONTROL_COURT_SET`

I measured the denominator myself in the **governed** R7 interpreter: **25 collectable, 30 absent**
(exactly the candidate's claim). Passing all six paths aborts with *"file or directory not found"* —
the three files are missing paths, not a collection shortfall.

**The decisive finding is not the missing tests; it is a missing production module.**
`test_closed35_g01_sav_numeric_representation_authority.py` imports
`rawlsing_next.closed35_g01_sav_numeric_representation_authority` — a **production** module that
**does not exist on control at all**. Restoring the courts therefore *cannot* be a court-file-only
act; it would require backporting accepted-C3 production modules into control.

**Lineage:** control and the accepted lineage **diverged at `87029d349`** (2026-10-01; 258 commits
control-side, 212 accepted-side). The C3 court definition `1df64cc59` (2026-10-02) is on the
**accepted lineage only** and is *not* an ancestor of control. Control carries its **own** sanctioned
court set in `.rabochii/court_spec.json`, which **excludes all six R7 files**.

**Conclusion:** the 55-test denominator is a property of the accepted C4C3 tree, not a control
obligation. Requiring it on control imposes a foreign denominator. `RESTORE` is rejected (impossible
at court grain, out of scope at production grain); `MATERIAL_AUTHORITY_CONFLICT` is rejected (no two
authorities contradict — the conflict dissolves once the gate is attributed to its own lineage).

## B — SR06: a **porting gap**, not a decoder regression

The candidate **ported the accepted decoder but kept the old test**:

| | blob |
|---|---|
| candidate decoder / accepted decoder | `b406d45fae419c02` (identical) |
| candidate SR06 test / control SR06 test | `b2c279e6ad85d695` (identical) |
| **accepted** SR06 test | `dfd063227e4a0897` |

The accepted lineage pairs `b406d45f` with `dfd06322`. The candidate did **not** touch the test. So
the two failures are the expected result of an incomplete port.

- **Test 1 — STILL BINDING; update, do not retire.** It asserts source identity is hashed once
  *before* reader decode. The old test patches `decoder._sha`; the accepted decoder exposes
  `_governed_source_sha(broker)` (line 271). **The invariant is preserved**: `_governed_source_sha`
  is called at line **615**, `metadata_read` at **623**, `selected_read`/`full_read` after — hash
  still precedes every decode. Retiring it would destroy live coverage of the identity gate.
- **Test 2 — MIXED; update both halves, do not retire.** The chunk-path and
  compatibility-routing halves are binding and preserved by the accepted revision. Only the
  `read_file_in_chunks`/`chunksize == 2` helper assertion is stale — and abandoning that helper is
  independently corroborated (HQ196: it reuses one object and ReadStat rejects the reuse for DTA).
  The accepted revision legitimately drops the chunk-size assertion; I verified in HQ197 that the
  underlying chunk-sizing behaviour **is** correct, so this is a coverage weakness, not a defect.

**I did not retire anything.** The commission warned against retiring tests because the new stack
passes its own courts; the accepted stack's 34/34 + 15/15 + 20/20 says nothing about these two, and
I adjudicated them on their own authority and lineage.

## C — Environment: the reconstruction was **unnecessary**

The candidate's receipt says the governed R7 interpreter was **absent**. **It is present and runs on
this host:**

```
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python
  -> python 3.11.3, pyreadstat 1.3.6, pandas 2.3.3, numpy 2.4.6, pyarrow 25.0.1
```

The governed C4C3 base interpreter and the `c4c3-env` are present too. The environment the candidate
actually used (`/var/folders/…/hq204-r9-env`) is **deleted**, so its court results are not
re-runnable from its own receipt — an **evidence-durability** defect.

**Where the candidate was right, and I was wrong:** I suspected its 14-package freeze omitted a
package. Set comparison against the governed `01_ENVIRONMENT_LOCK.json` shows **14 vs 14, no
difference**. The `narwhals` off-path claim also holds (`git grep narwhals` over `rawlsing_next` →
nothing). And its refusal of the ambient **pyreadstat 1.3.2** by the accepted seam was **correct
fail-closed conduct** — the pin was not relaxed.

**No reconstitution is required.** The requirement is that governed courts be *run in the governed
interpreter*, not in an ephemeral substitute.

## Verified strengths of the candidate

Accepted runtime placed **8/8 paths byte-identical to `0deb6478`**; R9 courts **69/69** matching
accepted counts; reachable R7 subset **25/25 twice, deterministic**; import/compile smoke PASS; no
self-adoption; the pyreadstat pin held under a hostile ambient reader.

## Required repairs (specified, NOT performed — this lane may not touch code)

1. **Rebase the R7 gate** onto control's own court set; record the 55-test court as an
   accepted-lineage qualification. Do **not** satisfy it by importing accepted production modules.
2. **Adopt the accepted SR06 test revision** (`dfd06322`) alongside the accepted decoder — a
   bounded, one-file test adoption. Not a retirement; not a decoder change.
3. **Re-run the governed courts in the governed interpreter** and have receipts name that
   interpreter plus observed package versions.

## Confidence and honesty notes

I did **not** independently verify the candidate's aggregate 109-test regression sweep (14 → 16
failures); I adjudicated the two named tests directly from blob lineage, which is stronger evidence
than the aggregate. I could not re-run the candidate's ephemeral environment because it is deleted;
I used the governed interpreter instead.

## Holds observed

No code modified; no test modified; no source access; no locator discovery; no warrant issuance; no
live C4; no C7 or actor/person work; no self-adoption.
