# B01C — Deployment, custody and acceptance holds

## 1. Custody

| Item | Value |
|---|---|
| Sealed startup (verified before mutation) | `923e2c1d0ff27961233c52c385f672bbd1a4f23c` |
| Branch | `agent/rabochii-pyat-hq280-pv3-b01c-durable-checkpoint-candidate-r1` |
| B01 grounding return | `2e317aa5fbabac8a8fa78bf85069ab30f69d3db7` |
| Interpreter | Python 3.11.3 (`.pv3-venv`), macOS-13.7.8-x86_64 |
| Raw `.sav`/`.dta` in worktree | **0 files** (`find . -name '*.sav' -o -name '*.dta' \| wc -l` → 0) |
| Source read | **none** |
| New source-use permission | **none claimed or requested** |
| Canonical / semantic PRE-MAIN | **unmutated** |
| Self-adoption | **none** |
| ZIP relay | **none** — all evidence is modest text/JSON pushed to the branch |

The source-free posture is **structural**, not merely asserted: there is no raw
file in the worktree for the candidate to read.

## 2. Safe hosted bounded resource record

Measured on this host, 4-unit manifest, real subprocesses (`02_...json` →
`resource_measurement`):

| Measure | Value |
|---|---|
| Peak RSS (recorder process) | **25.918 MiB** |
| User CPU | **0.248 s** |
| System CPU | **0.147 s** |
| Total wall for the whole kill/restart + hostile record | **~1.4 s** |

Per-subprocess wall: ~118–148 ms per real worker phase.

**These are bounded development-scale numbers only.** They are **not** a capacity
forecast, **not** a 35-wave extrapolation, and **not** a universal threshold. No
unbounded stress was run.

## 3. Acceptance holds — what this candidate does NOT establish

1. **Exactly-once external execution is NOT proven.** Only the *safe* behaviour
   (HOLD on unknown outcome) is proven. A write-ahead intent before execution is
   not an exactly-once guarantee, and this packet asserts none.
2. **REAL_EXECUTION protocol approval is NOT granted.** The candidate satisfies
   the `WRITE_AHEAD` / `durable_checkpoint_ref` vocabulary but does **not**
   relax, reimplement or supersede `rabochii_execution_protocol`. A
   source-free PASS is explicitly **not** protocol approval.
3. **No idempotence of any external executor is verified here.** `RERUN_SAFE`
   depends on a **caller-supplied** proof keyed by exact unit key. The candidate
   cannot itself establish that an arbitrary owner is idempotent.
4. **Single-writer only.** Exclusivity is an advisory `fcntl.flock` on one host
   and filesystem. It is **not** distributed consensus, and it is not a
   multi-host guarantee. NFS or similar filesystems may not honour `flock`.
5. **No crash-consistency guarantee beyond the measured phases.** `fsync` on file
   and directory is the correct primitive, but hardware/FS lies (or a lying
   storage device) are outside this envelope.
6. **Scale is bounded.** 4 units / 4-row manifests only. No large-manifest
   checkpoint cost, no fsync-throughput characterisation, no disk-exhaustion
   behaviour was measured.
7. **B01 F-04/F-05/F-06 remain open** and are not addressed here (slow tests,
   uncollectable modules, unexplained failures). This worker made no claim about
   them.
8. **B01 P17 is inherited unchanged.** A rewritten adaptive checkpoint yields an
   equal work set and equal terminal state but a **different** `checkpoint_ref`
   because identity is visit-order sensitive. Safety holds; identity determinism
   does not converge. This candidate does not alter adaptive semantics.

## 4. Competent-owner decisions required before any governed launch

| Decision | Owner |
|---|---|
| Accept or reject this candidate | HQ / competent owner |
| Whether `WRITE_AHEAD` + durable ref satisfies `REAL_EXECUTION` | protocol owner |
| Per-executor idempotence proofs, or accept permanent HOLD | execution owner |
| Whether single-host `flock` is an adequate concurrency model | runtime owner |
| Larger-scale fsync/disk-cost characterisation | runtime owner (B01-class work) |

## 5. Scope of files changed

**Exactly two new source/test files plus this return packet.** Verified:
`git diff --name-only 923e2c1d… -- rawlsing_next/` → **empty**. No accepted
batch runner, no protocol module, no canonical file was modified. No `.pyc` or
test residue is staged.

**Terminal:** `HQ280_PV3_B01C_SOURCEFREE_DURABLE_CHECKPOINT_CANDIDATE_RETURNED__NO_REAL_SOURCE_ADOPTION__GITHUB_PUSHED`.