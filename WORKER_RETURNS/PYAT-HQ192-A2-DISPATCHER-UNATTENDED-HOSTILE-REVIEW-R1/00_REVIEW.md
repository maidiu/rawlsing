# PYAT HQ192-A2 — DISPATCHER UNATTENDED HOSTILE REVIEW — R1

**Disposition:** `ACCEPT_UNATTENDED_WITH_BOUNDED_RESIDUAL_LIMITATIONS`

**Terminal:** `HQ192_A2_HOSTILE_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq192-a2-dispatcher-unattended-hostile-review-r1`
Commissioned startup SHA: `ce1574030e1136e29b093e2743d8b8e77f465f03`
Target worker tip: `4b0b33102998abf9ce29fc0e584e278c85a44fe7`
Substantive implementation: `50829fd0fba24eefd457abeb3cba4cd365460296`
Dispatcher blob: `2db72c887b032622e09da6a5bd7723f7fb7055ee`

**Reviewer identity (actual, observed):** DeepSeek Harness, **DeepSeek V4.1 Flash** — a
different model/authority from Space Bunny, satisfying the independence requirement.
Host: macOS 13.7.8 (Darwin 22.6.0) x86_64; Node v22.23.3; git 2.39.1; installed OpenCode
CLI **1.18.34** at `/Users/matthewsmith/.opencode/bin/opencode`.

---

## 1. Bottom line

MR-1, MR-2, MR-3, MR-6, **both** worker-found defects, and the bounded MR-5 property are
**independently verified** by reviewer-authored attacks. The two load-bearing claims the
governing review falsified — the phantom capacity invariant and silently-swallowed state
transitions — are genuinely fixed, and I could not re-break them.

I could **not** independently verify MR-4's kernel enforcement, because **my own review
sandbox refuses `sandbox-exec` entirely** (see §5). That is a limitation of this review's
context, not evidence of a candidate defect — and I state clearly which parts I verified
statically versus did not observe at all.

One material residual is **worse than the worker's framing**: the seatbelt profile is built
on `(allow default)`, so **network egress is completely unscoped**, not merely "not scoped
by destination". For unattended source-free orchestration — where no model call can succeed
without egress anyway — this is a limitation on isolation strength, not a blocker.

## 2. Mandatory startup (all verified before substantive review)

| # | Check | Result |
|---|---|---|
| 1 | `git fetch origin`, no blind pull | OK |
| 2–3 | review branch == `ce1574030…` | **MATCH** |
| 4 | target tip == `4b0b33102…` | **MATCH** |
| 5 | `50829fd0f…` substantive ancestor of tip | **VERIFIED** |
| 6 | dispatcher blob at **both** == `2db72c887…` | **MATCH (both)** |
| 7 | isolated clean review worktree | `review-hq192a2` |

Candidate untouched by me: dispatcher still hashes `2db72c887b032622e09da6a5bd7723f7fb7055ee`.

## 3. MR-1 — atomic admission: **VERIFIED**

I re-ran the **prior reviewer's reproducer unmodified**, pointed at the new blob:
**0/12 over-capacity** (previously 7/12 and 3/12). Then I ran my own structurally different
stress (`evidence/mr1_stress.mjs`) with 32 processes and a mixed wave design:

| Wave | Design | Result |
|---|---|---|
| A | 32 OS processes, 32 **distinct** tasks, cap 2, 10 trials | **exactly 2 admitted every trial; 0/10 over-capacity; 30/32 clean `SLOT_CAPACITY` refusals** |
| B | 32 OS processes, **all the same** task id, 10 trials | **exactly 1 record every trial; 31/32 idempotent acks** |

The implementation now performs read → dedup → capacity → append inside a single
`_withLock`/`_appendLocked` transaction. No liveness defect observed: every trial terminated
well inside the 15 s lock deadline.

## 4. MR-2 — sequence/state ownership: **VERIFIED** (and the worker's design choice was right)

| Attack | Result |
|---|---|
| `QUEUED → RUNNING → RETURNED` via `recordTaskEvent` | **all three recorded** (`1:QUEUED, 2:RUNNING, 3:RETURNED`), none swallowed |
| caller supplies `seq: 1` on a second transition | **ignored**; store allocated `2` |
| distinct attempts `1` and `2` | independent sequences, no collision |
| legacy `append()` with a reused seq | still deduped (no silent overwrite) |

The commission warned against merely key-widening, and the worker's reasoning is correct:
`recordTaskEvent` strips the caller's `seq` and allocates a monotonic per-`(task_id, attempt)`
sequence under the lock, so collisions are structurally impossible rather than filtered.

**Residual (NOTE, not a defect):** the public `append()` remains a caller-supplied-sequence
path (`allocateSeq` defaults false). Any new caller that uses `append()` for lifecycle
transitions reintroduces the original hazard. The safe constructor is `recordTaskEvent`.

## 5. MR-4 — kernel containment: **NOT INDEPENDENTLY VERIFIED (review-environment blocker)**

**Definitive evidence that the blocker is mine, not the profile's:**

```
/usr/bin/sandbox-exec -f trivial.sb  /bin/echo      -> sandbox_apply: Operation not permitted
/usr/bin/sandbox-exec -f deny.sb     /bin/echo      -> sandbox_apply: Operation not permitted
/usr/bin/sandbox-exec -p '(version 1)(allow default)' /bin/echo -> Operation not permitted
```

**Every** profile fails, including `(allow default)` and `(deny default)`. A malformed
profile yields a *parse* error, not `sandbox_apply: Operation not permitted`; so this is the
review sandbox refusing profile application, not a syntax defect in the candidate's profile.
Consequences:

- I could **not** execute the worker's containment control experiment (in-worktree write
  succeeds / out-of-worktree write fails at OS level / escape still denied under permissive
  OpenCode config).
- I therefore credit MR-4 **0% from live observation**. What I verified is **by inspection**:

| MR-4 sub-claim | Reviewer status |
|---|---|
| containment is on by default (`cfg.containment !== false`) | **verified (source)** |
| absence of `sandbox-exec` → `CONTAINMENT_UNAVAILABLE` refusal, no silent fallback | **verified (source)** |
| profile is written to a file and passed via `sandbox-exec -f` | **verified (source)** |
| only the worktree + OpenCode state dirs + TMPDIR are writable | **verified (source)** |
| **actual kernel enforcement of those denies** | **NOT OBSERVED** |

**Material residual found by inspection:** the profile begins `(allow default)`, which grants
network egress unconditionally. The worker states only that seatbelt "does not scope network
egress **by destination** here". The accurate statement is stronger: **egress is entirely
unrestricted**, and the filesystem write deny is the only enforced boundary. A source-free
orchestration agent nevertheless *needs* egress to reach the model, so this is a genuine
limitation rather than something a fix would trivially remove.

## 6. MR-3 — no blanket `--auto`, scoped permissions: **VERIFIED (static)**

- `--auto` is absent from `buildLaunchArgv`; supplying `auto_approve: true` throws
  `BLANKET_AUTO_REFUSED`. **Grep of every launch path found no `--auto` argument.**
- The scoped profile denies by default and allow-lists exactly: `edit: allow`,
  `external_directory: deny`, `webfetch: deny`, `bash` per-pattern (only `git status/diff/
  log/rev-parse/add/commit/cat-file/ls-tree/show`) and `tools.webfetch: false`.
- `launch()` injects the profile per-process via `OPENCODE_CONFIG_CONTENT` and **deletes
  inherited `OPENCODE_CONFIG`**, so a global config cannot widen it. **Verified (source).**
- **NOTE:** `launch()` accepts a caller-supplied `permission_profile` and uses it in place of
  the scoped default. The dispatcher does not validate that a supplied profile is
  *narrower*. A hostile or careless caller can therefore widen permissions without any
  dispatcher gate noticing. Within this lane the caller is the dispatcher's own harness, so
  it is not an active escape, but it is the weakest link in MR-3 and should be constrained
  (e.g. reject profiles that allow `external_directory`).
- **Not verified live:** the worker's load-bearing control (identical insisting prompt
  succeeding under `external_directory: allow` and failing *before write* under `deny`),
  because the CLI cannot run under my sandbox.

## 7. MR-5 — commission delivery integrity: **bounded property established**

**Verified structurally (the strong half):**

- `commissionAuthorityFrame()` is generated **only** from dispatcher-held values
  (`commission_path`, `commission_sha256`, `terrain`, `role`, `worktree`, `holds`). It never
  reads the commission, so **no attachment text can reach the authority frame**. The claimed
  property is not merely asserted — it is structural.
- Exact delivered bytes are SHA-256 bound before launch; drift raises
  `COMMISSION_DELIVERY_DRIFT`.
- The **rendered, defanged** document is what `--file` attaches; the untouched bytes remain
  as the integrity anchor. So defang is genuinely load-bearing, not decorative.

**Defang attack — I went well beyond the worker's 13 shapes** (40 adversarial lines across
mixed case, whitespace/tab, zero-width, fullwidth unicode, XML/CDATA/entity forms, nested
fences, pipe delimiters, JSON `function_call`/`tool_calls`/`tool_use` payloads, fake
`### SYSTEM ###`/`[[USER]]` delimiters, and precedence-redefinition text). Result:

| Band | Result |
|---|---|
| Line-anchored tags (`<TOOL_CALL>`, mixed case, `</tool_call>`, `<tool_calls>`, `<tools>`, `<function_results>`) | **defanged** |
| Line-anchored fences and `[[TOOL…]]` / `[TOOL…]` | **defanged** |
| Zero-width inside the tag | **defanged** |
| **Mid-line** forms (`Note: <TOOL_CALL> here`, `see ```bash here`, `   text <TOOL_CALL>`) | **survive** |
| Markup/JSON (`<!-- <TOOL_CALL> -->`, `{"function_call": …}`, `"tool_calls": …`, `{"type":"tool_use"}`) | **survive** |
| Fake role delimiters, entity-obfuscated, fullwidth, namespaced (`<ns:invoke>`, `<goog_function_call>`) | **survive** |
| Precedence-redefinition text (`IGNORE ALL PRECEDENCE RULES`) | **survive** |

**Bounded property actually established:** the defang is a **line-anchored presentation
guard**, not an injection filter. It reliably stops the attachment from *looking like* a tool
call at line start. It does **not** sanitise arbitrary instruction-looking content.

**Why this is not a soundness break:** the security property does not rest on defang. It
rests on the dispatcher-generated precedence frame plus byte integrity. Defang is defence in
depth for one presentation family. **I do not claim prompt-injection immunity**, and neither
should the return. The honest statement is: *the attachment cannot become higher-priority
instruction authority via the dispatcher-generated frame, and cannot reach the frame at all;
residual risk is the model's own instruction-following, which no dispatcher-side transform
eliminates.*

I could not run the live "legitimate task still completes" half, since the CLI is blocked
for me; that half remains worker-reported.

## 8. MR-6 — lock ownership and durability: **VERIFIED** (after correcting my own test)

My first attempt reported a false failure because I wrote the lock file as JSON while the
parser expects `pid=N token=HEX`. Corrected and re-run (`evidence/lock_retest.mjs`):

| Scenario | Result |
|---|---|
| **dead** owner, correct format | reclaimed in **35 ms**, write proceeds |
| **live** owner (own pid), mtime **900 s old** | **not** reclaimed; `WRITER_LOCK_TIMEOUT` after 15 s |
| **legacy token-only** lock (owner unprovable) | **not** reclaimed; `WRITER_LOCK_TIMEOUT` |

So the mtime-based robbery the prior review flagged is gone: ownership is now decided by
`process.kill(pid, 0)` with `EPERM` counted as alive, and unprovable ownership fails safe.
Release is token-guarded, so a predecessor cannot evict a successor's lock. The state
directory **is** fsynced on log creation (I initially mis-flagged this; the directory
`openSync(dir,"r")` + `fsyncSync(dfd)` is present).

## 9. Worker-found defects, independently attacked

| Defect | Attack | Result |
|---|---|---|
| return redelivery not idempotent | sequential redelivery | 1 `RETURNED` record; second call reports `dedup:true, idempotent:true` |
| return redelivery (race) | **8 concurrent processes delivering the same logical return, 14 trials** | **exactly 1 `RETURNED` record in all 14 trials; max = 1** |
| `<TOOL_CALL>` defang hole | exact shape | **now defanged**; plus the wider family in §7 |

**Honest residual on redelivery:** `deliverReturn` performs its idempotence check with
`store.all()` **outside** the writer lock, then appends under it. That is a check-then-act
window. I attacked it hard (8-way concurrent, 14 trials) and could **not** produce a double
delivery — the window is narrow because the check reads the whole log synchronously — but the
code shape is not atomic and the fix is not structurally guaranteed the way MR-1's is. This
is a **bounded residual, not a demonstrated failure**.

## 10. `--agent worker` fallback — correctly *not* credited

`buildLaunchArgv` still emits `--agent <role>`, and the worker's live run observed
`agent "worker" not found. Falling back to default agent`. The worker explicitly states that
role separation must **not** be credited to `--agent` and rests on the scoped permission
profile plus the terrain gate. I agree, and no claim in the return relies on it. Since the
fallback is to the OpenCode *default* agent — not to an unsandboxed build — this is a
**limitation on role separation strength**, not a containment bypass.

## 11. Acceptance questions answered

**1. Are MR-1…MR-6 independently verified?** MR-1 ✅, MR-2 ✅, MR-3 ✅ (static; live control not
runnable here), MR-5 ✅ **bounded property only**, MR-6 ✅. **MR-4: not independently
verified** — review-environment blocker (§5); source inspection only.

**2. Qualified for unattended source-free orchestration on this exact host?** Mechanically
yes for the state/identity/permission layers; **MR-4's enforcement rest on inspection rather
than independent observation at this grain**, and the worker's own **L-1** (independent
reviewer identity) remains unmet and is outside a worker lane's authority to satisfy. So:
**bounded accept, not clean accept**.

**3. Residuals that constrain without blocking:**
- **network egress unscoped** (`allow default`) — real, and unavoidable for any agent that must reach a model;
- **writable OpenCode state dirs** (~/.local/share, ~/.cache, ~/.config/opencode) — writable by design; containment is not hermeticity; a compromised agent can persist config/session state there;
- **`sandbox-exec` deprecated by Apple** — the launcher probes and refuses rather than degrading, which is the right failure mode, but the mechanism is on borrowed time;
- **`--agent` fallback unresolved** — role separation rests on the profile + terrain gate;
- **`LOCAL_COURTS` disk pressure persists** (99% capacity, 5.66 GiB free at review time) — a live multi-gigabyte run precondition, carried from HQ191.

**4. Any residual still a material unattended blocker?** At this grain, **no demonstrated
material blocker inside the dispatcher**: the state-machine, admission, permission, lock and
authority-frame properties all held under reviewer attack. The unresolved items are
isolation-strength and environmental preconditions. A clean unattended qualification should
still wait on **L-1** (third-party reviewer identity) and an independent MR-4 observation on
a host where `sandbox-exec` can actually be applied.

## 12. Capability ceiling

Qualified for **unattended source-free orchestration on this host with bounded residual
limitations**, where the enforced boundary is **filesystem write containment + scoped
permissions + dispatcher-generated instruction precedence**, and explicitly **not**:
hermetic process isolation, network egress scoping, destination-filtered egress, role-level
agent separation, or prompt-injection immunity.

## 13. Holds observed

Zero raw-source access, zero locator discovery, zero warrant issuance, zero live C4, zero
C7/actor work. No `sudo`, no system/`/etc`/global-security modification, no system profile
edits. Candidate unmodified (`2db72c887…`). All fixtures disposable under `/tmp`. Only the
commissioned return directory written inside the repository.
