# PYAT HQ200 — governed source-session independent acceptance — R1

**Disposition:** `ACCEPT_GOVERNED_SOURCE_SESSION_MECHANISM__WARRANT_BINDING_LAYER_NEXT`

**Terminal:** `HQ200_R9_SESSION_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq200-r1`
Commissioned startup SHA: `f10b35a0e013695f598e6fe951c5282e0aa480a2` — **verified equal**
Clean tip: `76970cfdfc8968e975595ea288cf44b448205e30`; code-bearing candidate `90ccbd54c549f67358d0c02ad18ff90b843cf3ee`
Checkout mode: `SPARSE_REQUIRED` — honored; no clone, no full worktree, sparse checkout not widened. The parallel HQ200 implementation branch was **not** reviewed.

---

## Headline

**All fifteen criteria pass.** `GovernedSourceSession` is genuinely an owner *above* one decoder
call, and the strictest criterion — a `decoder_invocations=1` refusal — leaves **every account
exactly unchanged**, proving a strictly pre-operation gate rather than a partial abort.

**Courts:** session **15/15**, broker **20/20**, R7 **55 collected then 55/55 twice**. 145 tests,
zero failures.

## 1. The owner is real (C1, C11, C12)

`__init__` constructs exactly one `SourceAccessBroker`; measured across two `run()` calls the
broker object identity is **the same** and `path_opens=1`. `aggregate_receipt()` is rebuilt from
the broker on each access — measured `chunk_reads` in the receipt went **0 → 6** after a later
`CHUNKED_FULL` run, so the per-source receipt stays live. `close()` is idempotent and refuses
`run()` afterwards with `SESSION_CLOSED`.

## 2. `decoder_invocations` is a genuinely separate account (C2, C3, C4)

Both counters exist as independent account **and** budget fields with independent `check()`
projections. The divergence is measurable on a single `FULL` plan:
**`decoder_invocations=1` while `reader_invocations=2`** — they cannot be the same quantity.

`run()` calls `admit_decoder_entry()` as its **first** action, before `existence_check()`,
`hash_pass()` and `metadata_read()`. With `decoder_invocations=1`:

- first run succeeds; second run raises `SOURCE_ACCESS_BUDGET_EXCEEDED`;
- **accounts changed on refusal: NONE** — including `existence_checks`, `hash_passes`,
  `metadata_reads`, `path_opens`, `reader_invocations` and `reader_bytes`.

That is the strongest possible form of the criterion: nothing at all happened.

## 3. Plan modes are exact and never conflated (C5–C10)

| Mode | metadata | selected | full | chunk |
|---|---|---|---|---|
| `METADATA_ONLY` (encoding=`latin1`) | 1 | 0 | 0 | 0 |
| `SELECTED` | 1 | 1 | 0 | 0 |
| `FULL` | 1 | 0 | 1 | 0 |
| `CHUNKED_FULL` | 1 | 0 | **0** | 3 |

**C5 matters most:** `METADATA_ONLY` with a non-null encoding performs metadata and **nothing
else** — this closes the HQ199-identified hazard where a declared-encoding source (SRC08/SRC12)
drifted into a full row-data read. Encoding is now strictly reader configuration.

**C8 matters for the count law:** `CHUNKED_FULL` does **not** increment `full_reads`, so
`chunk_reads` cannot silently satisfy SRC27's full-read **floor** (HQ200's explicit rule). A plan
that must satisfy the floor must use `FULL`.

Header prefix: `None` → **zero** operations; `176` → **exactly one 176-byte** operation. This
closes the second HQ199 defect (unconditional prefix reads, including an invented 512-byte DTA
read).

## 4. Production hygiene (C13–C15)

No `SRCxx` policy appears in production **code** (the single session-module hit is a comment
stating nothing there encodes such policy). The reader always receives a `_GovernedView`, and the
`RawSourcePathEscape` guard is retained. The accepted `reader_bytes` limiter is **intact**: cap
200 refused with `READER_BYTES_LIMIT_EXCEEDED` consuming exactly 200; a generous cap succeeded.
The broker delta is **purely additive** (account field, budget field, check projection, basis
entry, `admit_decoder_entry`) — nothing removed or altered.

## 5. Count semantics — the HQ199 overstatement corrected

I adopt HQ200's semantics exactly and **do not repeat** the earlier claim that frozen authority
requires exactly one full read or exactly one decoder entry:

- `full_route_passes` = **exact/max 1** — frozen;
- `full_reads` = **floor ≥1**, ceiling historically **unbound**;
- `decoder_invocations` historical expected value = **unbound**; **MAX 1 is permissible
  implementation policy**;
- `path_opens` historical numeric value = **unbound**;
- `retries` = max 0.

So the candidate's default of `decoder_invocations=None` is **correct for a generic owner** — it
fabricates no historical count and lets a binding layer impose MAX 1 as policy.

## 6. Generic owner boundary

With no ceiling, three sequential `METADATA_ONLY` runs give `decoder_invocations=3`,
`metadata_reads=3`, `path_opens=1`. **Not a defect** — and once `decoder_invocations=1` is
supplied, the identical second run becomes a zero-side-effect refusal. So the generic owner **is
sufficient as a mechanism for a stricter bound layer**.

**Carry-forward (next layer, by design):** the session does **not** own or enforce
`full_route_passes`. `SourceOperationPlan.outer_account_token` is recorded but is not an account
and has no ceiling. The binding layer must add a **separately typed** outer route-pass account
(expected 1 / max 1 for SRC27) without collapsing it into `decoder_invocations`, `full_reads`,
`chunk_reads` or `reader_invocations` — matching HQ200's "missing route-pass owner".

**Honest limitations:** cross-process/cross-run uniqueness (an owner object cannot stop a second
*process* from building its own first session — needs an authority-held durable mechanism or an
operational control); the session does not memoise the first observed SHA (not reachable today,
advisory hardening); and byte ceilings can be enforced but not invented.

## 7. Error paths fail closed

Identity mismatch → `hash_passes=1, metadata_reads=0` (refused before any reader access).
Absent selected variable → `metadata_reads=1, selected_reads=0` (row read never issued). Byte
breach mid-run → accounts coherent and cumulative, and a retry is **refused** with the same typed
error. A failed run does not auto-close (advisory), but release via `close()`/context manager is
deterministic and idempotent.

## 8. Why not the other dispositions

`SESSION_MECHANISM_MATERIAL_DEFECT` — all 15 criteria pass; the broker delta is purely additive.
`R7_REQUALIFICATION_FAILURE` — 55 collected, 55 passed twice.
`SESSION_OWNER_SCOPE_STILL_INSUFFICIENT` — the mechanism demonstrably supports the stricter bound
behaviour; the outstanding route-pass account is a next-layer addition, not an insufficiency.

## 9. Holds observed

Synthetic carriers only; zero real survey/source access; zero locator discovery; zero warrant
issuance; zero live C4; no production mutation; no C7 or actor/person work. No adoption or
self-adoption. Nothing written outside the commissioned return directory.
