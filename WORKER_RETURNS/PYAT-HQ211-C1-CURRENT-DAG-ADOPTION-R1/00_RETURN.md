# HQ211 — C1 current-DAG surgical adoption join — R1

**Disposition: `C1_CURRENT_DAG_ADOPTION_JOIN_READY__HQ_REVIEW_REQUIRED`**
**Terminal: `HQ211_C1_CURRENT_DAG_ADOPTION_RETURNED__HQ_DECISION_REQUIRED`**

The HQ168/HQ206-accepted C1 analytical capability is grafted onto the **current** control
DAG at byte-exact accepted blobs. **Zero merges, zero side-branch commits, zero
production code authored.** No source access, no locator discovery, no warrant, no live
C4, no C7, no actor/person work, no F7 or V556 import, no H-D/F8 pending-branch import,
no self-adoption.

## Identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq211-c1-current-dag-adoption-r1` |
| Commission tip (exact, verified) | `1f05964479be110345472fc5239acefa9ea4775d` |
| Current control | `b722f2e7373ad833d5f63833b1d6fe426d3dc55d` |
| Accepted C1 repair return | `0574e095c4676680e671806febb7a76b35343389` (`agent/rabochii-pyat-hq206-c1-prune-r1`) |
| Merge base | `ff4f06954824a3a5699bc5c1c9bd68cb3c5b4146` |

**Current control has moved since HQ204** (`ff4f0695` → `b722f2e7`), so the
reconciliation was redone from scratch rather than reused.

### Execution law

`SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1` requires an HQ-prepared worktree path
or an already-authorized shared-store worktree. The commission supplied no prepared
path, so I used the **existing** canonical object store and created one isolated
**worktree** — the law's default topology. **No clone was created.** All historical
evidence was read from the shared object store via `git show` / `ls-tree` /
`cat-file`; sparse scope was never broadened to inspect history.

## The decisive finding on the one replaced owner

The commission said not to replace `pre553_authority_maintenance.py` wholesale and not
to choose by recency. The fact that settles it:

> **Current control's blob is byte-identical to the merge-base blob.**

So current control made **zero** semantic changes to that owner after the divergence.
There were no "later current-control semantic changes" to reconcile, and conservation
reduced to a superset proof rather than a three-way merge. I then proved it:

| Evidence | Result |
|---|---|
| Public symbols | 122 control → 137 accepted; **zero lost** |
| Refusal messages | **118 of 121 verbatim** |
| "requires an explicit deterministic recompiler" | preserved and generalized |
| "must produce a new exact ref" | preserved and strengthened (also forbids same-ref) |
| "recompilation pairs must cover exactly the affected set" | subsumed by a **strictly stronger** invariant |

The subsumed invariant was case-analysed, not waved through: where control refuses,
accepted refuses; where control passes (`affected={A}, pairs={}`) accepted also
refuses; and accepted is **strictly stricter** in two cases — an affected dependent
carrying both a replacement *and* a noncurrent disposition, and an outcome naming a
dependent outside the affected set.

**Verdict:** strict semantic **superset**, not a successor, not a conflict. No STOP.
`ACCEPTED_OWNER_COLLISION` was never triggered, and the decision was made by superset
proof, **not by recency**.

## The paired-test trap

`test_pre553_authority_maintenance.py` had also diverged (21 collected vs 57). I checked
whether it needed replacing: the current-control blob exercises **none** of the 11
symbols the accepted owner adds — `NoncurrentDependentOutcome`,
`NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT`, the three `DEPENDENT_LIFECYCLE_*`
states, `INVALIDATION_RECEIPT_NONCURRENT_SCHEMA`, `dependent_lifecycle_status`,
`noncurrent_old_refs`, `replacement_old_refs`, `preserves_legacy_identity`.

Adopting the owner without its paired test would have shipped the **entire
negative-lifecycle layer untested** and could not have collected 454. Owner and test
were adopted as one unit.

## Court identity recovered, not inferred

Recovered from the two machine-readable maps the commission named — **not** residual
arithmetic:

- `063ee8b7…/08_EXECUTION_RECEIPT.json -> per_file` — 15 entries, sum 454
- `c8ce0ea8…/05_TEST_AND_REPLAY_REVIEW.json -> section8_count_audit.per_file_independently_collected` — 15 entries, sum 454

The two agree exactly after key-name normalisation (the review map uses short stems
like `positioned_subject_consumer`; the implementation map uses `test_` stems). This
also **corrects my HQ204 method**: there I inferred the court by residual arithmetic
and it happened to be right; here it is read from the record.

**Measured: 454 collected, 454 passed — three times** (108.03s / 86.66s / 96.39s), with
every per-file count matching the accepted map.

## Overimport audit: exactly nine

The four authority directories at the *pruned* accepted state contain exactly
4+3+1+1 = **9 files**, so directory-level sparse import is provably identical to
importing only the required nine.

The open-audit instrument was **verified against a probe target before use**, so a
zero-result run could not be an artefact of a dead shim. Result: **9 unique files
opened, exactly equal to the nine, 0 of the 54 pruned over-imports ever opened, 0 files
opened outside the nine, 0 of the nine unopened.**

## Regression: exact failure-ID delta

Measured against a manifest-identical detached worktree at the commission tip, then
removed.

| | before | after |
|---|---|---|
| failure/error IDs | 280 | **280** |
| failed / errors | 227 / 53 | **227 / 53** |
| passed | 2336 | **2626** |

**New: 0. No longer failing: 0.** The ID set is byte-identical. `passed +290`
reconciles exactly: 254 from the six newly adopted court files (13+35+43+43+92+28) plus
36 from `authority_maintenance` growing 21→57.

Blast radius is also provably confined: the only production importer of the replaced
owner is `pre553_analytical_replay_dependency` (inside the adopted set), and **no
current-control test outside the adopted set** touches that owner.

## Terrain

30 paths: **28 additions, 2 modifications** (the owner and its paired test), 14 of them
blob-pinned by the commission. **Zero** production files authored or edited. Every
production path is a byte-exact copy of an accepted blob — this lane introduced no new
semantics.

## Limits

- This is a **join candidate for HQ review**, not adoption into control.
- The accepted C1 nonblocking limitation is unchanged and still open: no accepted single
  owner contract carries `provider recomputation → named consumer → lifecycle restore`
  in one fresh process.
- Whether the now-present analytical capability discharges H-A or H-D is an HQ question,
  not a finding of this lane.
- The 227 pre-existing failures and 53 errors are unrelated fixture/environment
  artifacts; neither fixed nor in scope.

## Terminal

`HQ211_C1_CURRENT_DAG_ADOPTION_RETURNED__HQ_DECISION_REQUIRED`