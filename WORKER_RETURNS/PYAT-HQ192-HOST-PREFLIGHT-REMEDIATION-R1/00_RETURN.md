# PYAT HQ192 — Host preflight remediation — R1

Role: **RABOCHII / LOCAL-HOST OPERATIONS IMPLEMENTER — SPACE BUNNY**
Branch: `agent/rabochii-pyat-hq192-host-preflight-remediation-r1`
Commissioned startup SHA: `f4db1192c5dd2962c93cf9b726c8835f922ad6e7` — verified before any edit.

## Disposition

`HOST_PREFLIGHT_POLICY_THRESHOLD_REQUIRED`

Both bounded hazards are **closed**. The disk blocker is **reduced and precisely
characterised but not resolved**, and I did not invent a threshold to make it look
resolved.

| Item | Status |
|---|---|
| `LOCAL_COURTS/` not ignored | **CLOSED** |
| Dangling interpreter symlink | **CLOSED** |
| SHA-pinned execution preflight | **built and verified**, blocked pending policy threshold |
| `HOST-PREFLIGHT-F3-DISK-CAPACITY-VOLATILITY` | **not resolved** — measured and characterised, reduced |
| R7 | closed, **not reopened** |

## The threshold question, answered honestly

I could not derive a numeric live-run free-space threshold, so I am not supplying one.

The commission permits a number only if governed evidence supports it. I searched the
governed paths (`WORKER_RETURNS`, `HQ_HANDOFF`, `PYAT_CONTROL_ROOM`, `rawlsing_next`)
for declared sizes and write behaviour and found **none**:

- numeric byte magnitudes (`[0-9]{6,14} bytes|B`): **0 matches**
- any `MiB`/`GiB`/`TiB`/`MB`/`GB` magnitude: **0 matches across all governed paths**
- `peak disk usage`, `disk_require`, `minimum_free`, `workdir_size`, `output_size`: **0 governed files**

I checked the near-misses individually rather than waving them through: the two
`space_require` hits are prose about sharing a decoder and about parallel workers; the
one `bytes_required` hit is the boolean `"source_bytes_required": false` — a statement
that bytes are *not* required, not a magnitude; and the 32 `scratch_*` hits reference
scratch **paths**, with no byte figure in any of them. As a negative control the same
method finds 350 files for `sha256` and 38 for `worktree`, so the zeros are real
absences and not a broken query.

Any number I produced here would be invention. The preflight therefore takes the
threshold as a **required policy input** and fails closed without it.

## What the evidence *does* support — the volatility, quantified

Free space on `/System/Volumes/Data` over 20 samples at 4 s intervals:

- range **4.21 – 5.22 GiB**
- largest single-interval delta **1.00 GiB** (exactly 1048576 KiB)

That 1 GiB quantum appearing within one 4 s interval, repeatedly, with no action by me,
is APFS/container snapshot accounting rather than organic growth. **This is the design
constraint on any future threshold:** a margin materially below 1 GiB will produce false
passes. It is a constraint on the policy value, not the value itself.

## Cleanup: what I removed, and what I refused to remove

Free space went **3.68 GiB → 5.22 GiB**. I must be precise about attribution: **the items
I deleted totalled 499 MiB, not the 1.54 GiB the volume moved.** The residual ~1.07 GiB is
concurrent host activity — a background git auto-pack ran during the lane and other lanes
are active in the same repository and volume. I do not claim it as my saving. On a shared,
volatile volume the volume delta and the sum of deleted bytes are different quantities.

**Deleted (SAFE_AUTOMATIC, 2 items, 499 MiB):**

- `/private/tmp/hq191a2` — my own disposable fixture (5 MiB)
- git worktree `hq191a2` — my own completed HQ191-A2 lane (494 MiB). Verified 0 tracked
  modifications, 0 real untracked artifacts, HEAD contained in its origin branch *and*
  already an ancestor of the HQ192-A2 reviewer branch — so the work is durably returned
  and independently reviewed.

One honesty note: my first removal attempt **printed a false success** because a shell
pipeline masked git's exit status; git had actually refused the dirty worktree. I redid it
honestly — deleted only the three `.DS_Store` files, then removed without `--force`, and
checked the exit code explicitly. A false success in a cleanup ledger is precisely the
failure mode under review.

**Refused (`REQUIRES_USER_APPROVAL`, ~15.5 GiB) — the decision that is yours:**

- 23 other-lane worktrees (~11.1 GiB). All are clean with HEAD on a remote, which
  satisfies "clean and remotely returned" — but *stale* and *not an active lane* are not
  mechanically determinable from git, ten still carry real untracked entries, and the
  safety law forbids cleaning another active lane's work.
- 1.38 GiB git loose objects (`git prune` on the shared `.git` could discard objects
  another lane has not yet pushed).
- `deepseek-harness` (2.5 GiB) — large, but "do not infer disposable merely because large".

**Preserved:** the R7 qualification environment (332 MiB), the bound interpreter
toolchains, and every `LOCAL_COURTS` subtree cited by `HQ_HANDOFF` as a live working root
(≈6.9 GiB, including `Rawlsing-retry-r1/protected-execution`, `.../source-split-control`,
`python/fiabc-wvs7-retry-r1-3.11.3/bin/python`, and the `FIABC-P2X-*` run roots).

## Hazard 1 — `LOCAL_COURTS/` ignore

Added a root `.gitignore` (none existed) with exactly one rule: `/LOCAL_COURTS/`. The
leading slash root-anchors it so it cannot mask a same-named nested directory.

No conflicting law exists, and I checked rather than assumed: `git ls-files -- LOCAL_COURTS`
returns **0**, so the rule cannot orphan anything, and `HQ_HANDOFF/DECISION_LEDGER.jsonl`
already records that the interpreter "resolves under the untracked LOCAL_COURTS path so it
is genuinely uncommitted". The rule codifies existing law rather than overriding it.

Verified: `check-ignore` succeeds on the target paths; `HQ_HANDOFF`, `WORKER_RETURNS`,
`PYAT_CONTROL_ROOM`, `rawlsing_next`, `data`, `.gitignore`, `WORKER_COMMISSIONS` are all
confirmed **not masked**; `some/dir/LOCAL_COURTS/x` is not matched; tracked file count
unchanged at 6827.

I did **not** add an ignore for `deepseek-harness` despite it being 2.5 GiB of untracked
noise — only `LOCAL_COURTS/` was commissioned, and an ignore rule is not a licence to
ignore more.

## Hazard 2 — dangling symlink

Root cause: the link was **absolute**, pointing at `~/LOCAL_COURTS/...`, while the real
tree is at `~/Desktop/Rawlsing/LOCAL_COURTS/...`. It had never resolved on this host.

Repaired to a **relative** link, `cpython-3.11.3-macos-x86_64-none` — which matches the
commissioned repo-relative target and stays correct if the repository moves. An absolute
path is what broke originally.

Verified: target exists; interpreter SHA-256 is `11d6f541…` via **both** the short name and
the real name — bytes unchanged; the short name executes as CPython 3.11.3. The preflight
now asserts this independently, so a regression to a dangling link fails closed.

## SHA-pinned execution preflight

`…/ACTIVATION_RETURNS/HOST-PREFLIGHT-R1/host_preflight.sh` — source-free, executes no live
C4, discovers no locators, issues no warrant, opens no source data.

| Check | Expected | Observed | |
|---|---|---|---|
| freeze commit | `8ff40d37de69db2d8a6053a7c2242f481677f1a4` | exact | PASS |
| `rawlsing_next` tree | `b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0` | exact | PASS |
| R7 interpreter SHA-256 | `11d6f541…4c535f6` | exact | PASS |
| disk threshold | HQ policy input | absent | **BLOCKED, exit 3** |

All three paths demonstrated: no threshold → exit 3; threshold met → exit 0; threshold
unmet → exit 2. Capacity is judged against the **worst of three samples**, so a transient
dip cannot yield a false pass. A PASS authorises nothing; it is a precondition check.

## What HQ must decide

1. **Adopt a minimum free space in GiB** and supply `HQ_DISK_MIN_FREE_GIB`. It must include
   a margin strictly greater than the measured 1.00 GiB volatility quantum. I recommend no
   figure, because choosing one is the inventing the commission forbids.
2. **Authorise or decline the ~15.5 GiB** of `REQUIRES_USER_APPROVAL` reclamation.

Until (1) is supplied the preflight exits 3 by design, which is the correct fail-closed
behaviour rather than a defect.

## Holds

Zero raw-source access, source-directory inspection, locators, warrant, live C4, C7 or
actor work. No `sudo`, no system security change, no recursive `chmod`/`chown`, no user
documents deleted. R7 not reopened; R7 qualification environment and bound interpreter
toolchains preserved; no other lane's work cleaned; no broad recursive cleanup over shared
paths. R7's separately-recorded venv non-durability finding is left untouched and not
re-litigated here.

## Artifacts

| File | Contents |
|---|---|
| `01_DISK_INVENTORY_AND_ACCOUNTING.json` | full inventory, classification, exact accounting, attribution disclosure |
| `02_DISK_EVIDENCE_AND_THRESHOLD.json` | the threshold search, near-misses rejected, negative control, measured volatility |
| `03_LOCAL_COURTS_IGNORE_AND_SYMLINK.json` | both hazard closures with verification |
| `04_PREFLIGHT_VERIFICATION.json` | pinned identities and demonstrated preflight behaviour |
| `05_DISPOSITION.json` | disposition and why not the alternatives |
| `…/HOST-PREFLIGHT-R1/host_preflight.sh` | the preflight itself |
| `…/HOST-PREFLIGHT-R1/harness/` | worktree inventory, repeated free-space sampler |
| `…/HOST-PREFLIGHT-R1/evidence/` | volatility series, three preflight transcripts |

Terminal: `HQ192_HOST_PREFLIGHT_RETURNED__HQ_REVIEW_REQUIRED`
