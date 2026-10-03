# PYAT HQ191-A2 — Dispatcher unattended hardening after hostile review — R1

Role: **RABOCHII / LOCAL-MACHINE IMPLEMENTER — SPACE BUNNY**
Branch: `agent/rabochii-pyat-hq191-a2-dispatcher-unattended-hardening-r1`
Commissioned startup SHA: `0d65e325e73be0bb4b5e873308bed1a8f10b5cc4` — verified before any edit.
Substantive result SHA: `50829fd0fba24eefd457abeb3cba4cd365460296`
Governing review: `agent/reviewer-pyat-hq190-a-dispatcher-hostile-acceptance-r1 @ 1aae86c8`

## Disposition

`CANDIDATE_READY_FOR_UNATTENDED_HOSTILE_REVIEW`

This is **not** a claim that unattended operation is safe. No claim is made beyond the
supervised ceiling, and the independent-reviewer-identity control that the governing
review requires (see `L-1`) remains unmet and outside this lane's authority.

## What the previous lane got wrong

The reviewer's central complaint was not a missing feature but a **false claim**:

> the worker's own evidence claimed "four distinct processes racing a cap of 2 yielded
> exactly 2 queued" — that result is **timing-dependent luck**, not an invariant.

I reproduced the defect against the adopted blob `f3067208` using the reviewer's own
unmodified harness: **4 of 8 trials admitted 3 tasks against a cap of 2.** The
advertised concurrency property was simply false, and the evidence that "proved" it was
a single lucky trial. R-2 was equally direct — appending `RETURNED` at a reused sequence
returned `{appended:false, dedup:true}`, so the transition was silently swallowed and the
task's final state was wrong.

Both are now closed and both are demonstrated with real OS processes over many trials,
because the original defect was timing-dependent and simulated interleavings would not
have found it.

## The six mandatory repairs

| ID | Repair | Status |
|---|---|---|
| MR-1 | Atomic admission: dedup + capacity + append in **one** writer-lock transaction | repaired, verified |
| MR-2 | Un-droppable transitions via **sequence ownership**, not key widening | repaired, verified |
| MR-3 | Blanket `--auto` eliminated; scoped permission profile | repaired, verified |
| MR-4 | Genuine kernel-enforced containment (`sandbox-exec` seatbelt) | repaired on this host |
| MR-5 | Commission delivery integrity: byte binding **+** dispatcher-generated authority | repaired, verified |
| MR-6 | Lock reclaim by proven-dead owner; state directory fsync | repaired, verified |

### MR-1 — atomic admission

`submitTask()` previously took the writer lock **twice**, with the capacity decision
outside both, so two processes could each observe a free slot and both append. Admission
is now one `store._withLock` scope over a new `_appendLocked` primitive: read records →
decide duplicate → enforce capacity → append, with no window between the decision and the
append.

- reviewer's unmodified harness: **0/8 over-capacity** (was 4/8)
- independent stress, not derived from the reviewer's: **24 processes against cap 2, 40
  trials → exactly 2 admitted every trial, 0 over-capacity**
- 24 processes submitting the *same* task id, 40 trials → **always exactly 1 record**

### MR-2 — sequence ownership, deliberately not key widening

The commission warned against merely appending `state` to the event key. That warning is
correct: under key-widening a buggy caller replaying one logical transition under a
different state produces **two competing truths for a single attempt**. Instead the store
now *owns* the sequence — `nextSeqFor()` derives a monotonic per-`(task_id, attempt)`
sequence from records already read under the writer lock, and `recordTaskEvent()` allocates
it. Collisions become structurally impossible, exact replays still deduplicate, and
distinct attempts never collide.

### MR-3 — no blanket `--auto`

`--auto` is now refused outright (`BLANKET_AUTO_REFUSED`). I inspected the real permission
surface on the installed CLI (1.18.34) rather than guessing: `permission.{edit, bash,
webfetch, external_directory, doom_loop}` with `ask|allow|deny`, **pattern-scoped `bash`**,
plus `tools{}` toggles. The profile is injected per-process via `OPENCODE_CONFIG_CONTENT`,
and `OPENCODE_CONFIG` is **deleted from the child environment** so no global config can
widen it.

The load-bearing evidence is the **control experiment**: the *identical* insisting prompt
under `external_directory: allow` **did** write the out-of-terrain file; under `deny` the
runtime emitted `permission=external_directory … action.action=deny` and the tool call
failed *before* the write. So the denial is the permission layer doing the work, not model
reluctance — which is exactly the distinction MR-3 asks for.

### MR-4 — containment that is actually containment

The review was blunt that worktree separation is not containment. This host has
`/usr/bin/sandbox-exec` (macOS 13.7.8), so `launch()` now wraps the child in a seatbelt
profile where the worktree is the only writable location: writes inside succeed, writes
outside **and writes into the real user repo** fail with `Operation not permitted`.

The decisive test: containment was re-run with OpenCode configured **fully permissively**
(`external_directory: allow`, `bash: * allow`). The kernel still refused the escape and the
tool call physically failed. The boundary is host-enforced, not advisory.

One honesty note that belongs in the record: an early seatbelt result was a **false pass**
because the profile failed to compile and the write simply never happened. It looked like
containment working. It was caught and corrected, and the profile now compiles before any
result is claimed. A containment claim that was never enforced is precisely the failure
mode this lane exists to prevent.

### MR-5 — delivery integrity

A hash alone cannot solve interpretation: binding bytes proves *which* document was
delivered, not that its contents lack authority. So there are two independent halves.

- **Integrity** — sha256 of the exact bytes is checked before launch; drift aborts with
  `COMMISSION_DELIVERY_DRIFT`.
- **Authority** — the governing instruction block is generated by the dispatcher from
  dispatcher-held values only, **never from the commission**, and states an explicit
  precedence rule under which the whole attachment is DATA that cannot widen permissions,
  terrain or holds.

The attached rendering additionally defangs faux tool-call markers. Exercised against a
benign fixture commission carrying a `<TOOL_CALL>` write probe, an `IGNORE ALL PRECEDENCE
RULES` override, a `../INJECTED_ESCAPE.txt` instruction and a forged `<|im_start|>system`
block: **the legitimate task completed, nothing injected was written anywhere**, and the
injection was not obeyed.

### MR-6 — durability

Lock reclaim now requires the owner pid to be **provably dead** (`process.kill(pid,0)`;
`EPERM` counts as alive). A live-but-slow writer whose lock mtime is 10 minutes old now
correctly produces `WRITER_LOCK_TIMEOUT` instead of being robbed. A dead owner's lock is
still reclaimed. The state directory is fsynced on log creation, and release removes the
lock only if the token is still ours, so a successor's lock is never evicted.

## Two further defects my own regression caught

I want these on the record because both were real and neither was in the commission:

1. **Return redelivery was not idempotent.** `deliverReturn` allocated a fresh sequence
   every call, so an at-least-once redelivery appended a *second* `RETURNED` record and HQ
   would see two competing returns for one attempt. Return identity is now
   `(task_id, attempt, candidate_sha)`.
2. **My defang regex had a hole.** The first pattern failed to match `<TOOL_CALL>` — a
   zero-width space in the literal plus a word boundary that cannot fire before an
   underscore. So the exact shape named in the review's finding survived rendering. Found
   only because the regression asserted on the real rendered artifact rather than on my
   intent. Now 13 adversarial shapes are defanged and benign lines pass untouched.

## Verification

- **Full regression: 44/44 passing** (`harness/full_regression.mjs`) across every
  commissioned gate — missing/placeholder identities, commission drift,
  review/candidate/adjudication mismatch, arbitrary `ACCEPTED`, Git-derived terrain, stale
  expected parent, corruption/torn log, duplicate submission, capacity stress,
  state-transition preservation, return delivery/recovery.
- The stale-parent gate runs against a **real local bare remote**, and the publication gate
  is also shown to **accept** a non-stale parent — so it is not merely always-refusing.
- **Live end-to-end** against a real OpenCode 1.18.34 process under containment, exit 0,
  session `ses_efc97c276ffefuFRBYcxTDKqOP`, no `--auto` in the contained command.

## What I did not close

Eight residual limitations are itemised in `02_CAPABILITY_AND_LIMITATIONS.json`. The ones
that matter most:

- **L-1** independent reviewer identity is **not** established — an organizational control
  outside my terrain. Unattended operation stays unqualified by this return.
- **L-2** seatbelt does **not** scope network egress by destination here; filesystem write
  containment is the enforced boundary.
- **L-3** the child's own OpenCode session/cache dirs stay writable, so containment is not
  hermeticity.
- **L-4** `sandbox-exec` is deprecated by Apple. The launcher probes for it and **refuses
  to run** rather than silently degrading to advisory-only.
- **L-5** `--agent worker` does not resolve (live run: `agent "worker" not found. Falling
  back to default agent`). Role separation must not be credited to `--agent`; it rests on
  the scoped permission profile and the terrain gate.

## Holds

Zero raw sources, locators, warrant, live C4, production-semantic mutation, C7 or
actor/person work. No `HQ_HANDOFF/**` edits, no historical returns modified, no
self-adoption, no merge into control. All fixtures disposable under `/private/tmp`; only
the commissioned return directories were written inside the repository. Host-safety law
observed: no `sudo`, no system/`/etc`/launch-agent/global-security change, seatbelt
profiles are disposable lane-owned fixtures applied only to the child under test, no global
OpenCode configuration modified, no recursive ownership or permission changes, no global
package installs.

## Artifacts

| File | Contents |
|---|---|
| `01_MANDATORY_REPAIRS.json` | MR-1…MR-6 with root cause, change, and before/after evidence |
| `02_CAPABILITY_AND_LIMITATIONS.json` | residual limitations L-1…L-8 and explicit non-claims |
| `03_DISPOSITION.json` | disposition, why not the alternatives, what to attack first |
| `…/OPS-02-03-HARDENING-R2/harness/` | stress, full regression, live E2E, refusal diagnostic |
| `…/OPS-02-03-HARDENING-R2/evidence/` | `regression_results.json`, `live_e2e_result.json` |
| `…/OPS-02-03-HARDENING-R2/harness/dispatcher.PRE-HARDENING.mjs` | byte-exact pre-hardening baseline (`f3067208`) for reviewer diffing |

Terminal: `HQ191_A2_DISPATCHER_HARDENING_RETURNED__HQ_REVIEW_REQUIRED`
