# PYAT HQ199 — R9 scope and operation-plan independent review — R1

**Disposition:** `PER_SOURCE_SESSION_OWNER_REQUIRED__SEVEN_SOURCE_PLAN_DETERMINATE`

**Terminal:** `HQ199_R9_SCOPE_PLAN_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq199-r1`
Commissioned startup SHA: `ed9d186aa7ab8ebd2f70cdae0240ef3a2b9f1917` — **verified equal**
Documentary base: `dbf3287084b547226a401fd0bde2da46610f2b9b`
Code reviewed: `4b6335ca5fc485108b0ffb1d682a29a02e1eee51` (broker blob `635f8bb38`, verified at review time)
Checkout mode: `SPARSE_REQUIRED` — honored; no clone, no full worktree, sparse checkout not widened.
Neither parallel HQ199 Space Bunny return was inspected.

---

## Headline

**A per-source session owner IS required**, and the seven-source operation plan is otherwise
**determinate** from the frozen law. I found **four material gaps**, all verified on the
accepted code rather than inferred: the missing owner, the unconditional header-prefix read,
the missing route-pass account, and the missing `decoder_invocations` counter.

I also **cleared SRC27 of the suspected one-open conflict**: the hardened note's governing
minimum is met over a single open.

## 1. The scope gap is real (GOV-SCOPE-001)

`SourceAccessBroker` is instantiated *inside* `_decode` and kept alive on the incidence — so its
natural scope is one decode call. That is correct design for the broker. But nothing binds one
**bound source entry** to one governed lifecycle across decodes. Verified:

```
decode #1: path_opens=1 hash_passes=1 metadata_reads=1 header_prefix_reads=1
decode #2: path_opens=1 hash_passes=1 metadata_reads=1 header_prefix_reads=1
AGGREGATE: path_opens=2 hash_passes=2 metadata_reads=2   -- second decode NOT refused
```

Each decode built its own broker with its own budget, so each looked individually compliant
while the aggregate is not. Against the frozen law that matters directly: SRC27 requires
`expected_full_route_passes=1` (max 1) and states that *"a second pass is not a retry; it is a
separate run requiring new HQ-bound authority"*, and SRC02/SRC06/SRC14 require
`expected_selected_reads=1`. Per-decode budgets cannot enforce per-source expectations.

**This is a missing owner, not a broker defect.** The accepted broker mechanics are untouched.

## 2. Header-prefix is over-admitted (GOV-HDR-002)

`_decode` calls `broker.header_prefix(176 if SAV else 512)` **unconditionally** for every source
and format. Only **SRC26** has a frozen `expected_header_prefix_bytes` (176) and the only class
naming a header prefix. Verified: a decode of a source whose class admits no header-prefix
operation still reported `header_prefix_reads=1, header_prefix_bytes=176`.

So **yes** — SRC02/SRC06/SRC14 must have zero header-prefix reads, **yes** — SRC26 is the only
source with an admitted header-prefix operation, and the **512-byte DTA header read is invented**:
it appears nowhere in the freeze.

## 3. Metadata-only classes can drift into a full read (GOV-…)

SRC08/SRC12 are `FRESH_METADATA_ONLY_DECODER_ADMISSION` with `expected_metadata_reads: 1`,
`expected_full_reads: 0`, and the retry law says *"a metadata-only reader probe"*. But with no
selected set and `encoding != None`, `_decode` takes the `elif encoding is not None` branch and
calls `broker.full_read(...)` — and SRC08/SRC12 *are* declared-encoding lanes. Verified on a
carrier registered as a declared-encoding lane: `metadata_reads=1` **and** `full_reads=1`.

The gate is not broken: supplying `full_reads=0` **does** refuse
(`SOURCE_ACCESS_BUDGET_EXCEEDED`). The defect is that **no per-source operation plan** sets it —
`_decode` derives its only default from whether a selected set was passed.

## 4. SRC27: descriptive, not binding — and no conflict

The disputed text is the `SRC27.critical_note`: *"The pass will involve multiple path-level
opens…"*. I built both cases in `03_SRC27_MULTIPLE_OPENS_REVIEW.json`. **The descriptive reading
wins**, and the decisive reason is the later, narrower `hardened_note_on_the_SRC27_single_pass`:

> *"The run will require **at minimum**: one existence/access check, one full SHA-256 hash pass,
> one metadata read, and one full compatibility read. Each is a separate account under O1-C07."*

That governing minimum is a list of **logical operations**, not of physical opens — and it never
mentions multiple opens. O1-C07's principle is *"separately accounted at every distinct layer"*,
a requirement about **accounting granularity**, not descriptor counts. *"Will involve"* is
predictive mood; the normative sentences in the same law use *must* / *is required* / *fails
closed*. And the phrase describes the implementation that existed when it was written (a hash
open, a metadata open, a read open).

**Verified on a declared-encoding DTA carrier:** `existence_checks=1, hash_passes=1,
metadata_reads=1, full_reads=1` over `path_opens=1`. **The hardened-note minimum is met over one
open. There is no SRC27 conflict.**

## 5. The layers, kept strictly separate

| Layer | Owner today |
|---|---|
| outer full Route-B pass | **none** (no counter) |
| decoder invocation | **none** — absent from account and budget |
| metadata read | `metadata_reads` |
| full read | `full_reads` |
| chunk read | `chunk_reads` |
| reader invocation | `reader_invocations` |
| physical source-path open | `path_opens` |

SRC27's one pass requires **exactly one full read and exactly one decoder entry** — and **not**
one reader invocation. Verified SRC27-shaped run: `reader_invocations=2` (metadata + full read).
Capping reader invocations at 1 would forbid the metadata read the hardened note requires.

## 6. `decoder_invocations` and the MAX 1 ceiling

O1-C07 lists `decoder_invocations` as its own mandatory account. **It is absent from both
`SourceAccessAccount` (15 fields) and `SourceAccessBudget` (14 fields).** It cannot be relabelled
from `reader_invocations`: one decoder entry performs several reader invocations.

**MAX 1 decoder invocation is lawful as a typed AUTHORIZATION ceiling** — provided it is labelled
a policy ceiling, not filed under an `expected_`/`observed_` key, and carries a stated rationale.
The accounting law already uses exactly that pattern (budgets that *"STOP a run"* and are *"not
claims about expected behaviour"*; retries frozen at 0 with a rationale disclosure). It must be
applied to the **decoder-entry** account only.

## 7. Minimum contract to close GOV-SCOPE-001

Specified in full in `05_SESSION_OWNER_MINIMUM_CONTRACT.json`: constructed **once per bound source
entry**; owns path/identity/format/**operation plan**/budget; owns **one** broker lifecycle;
enforces the plan pre-operation; carries a **decoder-entry counter and ceiling**; keeps a
**route-pass account** distinct from lower layers; **deterministic close + aggregate receipt**;
**refuses a second session/decode** where the frozen expectation is exactly one; and **no silent
legacy-path fallback**.

**What it still would NOT solve** (stated honestly): **cross-process / cross-run uniqueness** — an
owner object cannot stop a second *process* or a restarted run from building its own first
session, so a warrant-grade "exactly one pass" guarantee also needs an authority-held durable
mechanism or an operational control; **numeric byte ceilings** — it can enforce a ceiling but not
invent one, and no real-source numeric reader-byte ceiling is source-free frozen; **source-size
dependent ceilings**; **header-prefix re-admission** for classes that omit it (authority); and
whether a metadata-only admission counts as a decoder invocation at all (authority).

## 8. Why not the other dispositions

`CURRENT_BROKER_SCOPE_ALREADY_SUFFICIENT` — refuted by the two-decode experiment.
`SRC27_ONE_OPEN_BROKER_CONFLICT` — refuted; the hardened-note minimum is met over one open.
`SPECIFIC_AUTHORITY_AMBIGUITY` — the seven-source plan is determinate; only the session boundary
and two counters are missing.
`MATERIAL_CONTRACT_CONFLICT` — no authority contradicts another; the multiple-opens phrase is
descriptive and superseded by the narrower hardened note.

I did **not** reopen the accepted broker mechanics or interpretation A, and found no
contradiction requiring it.

## 9. Holds observed

Zero real survey/source access; zero locator discovery; zero warrant issuance; zero live C4; no
production mutation; no C7 or actor/person work. Synthetic carriers only. Nothing written outside
the commissioned return directory.
