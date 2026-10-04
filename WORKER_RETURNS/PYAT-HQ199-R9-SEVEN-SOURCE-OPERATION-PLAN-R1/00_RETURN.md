# HQ199-R1 Return — seven-source operation-plan authority reconstruction

**Disposition:** `SEVEN_SOURCE_PLAN_DETERMINATE__ONE_OPEN_BROKER_COMPATIBLE`
**Branch:** `agent/rabochii-pyat-hq199-r2`
**Startup SHA (verified exact):** `fdf78c71b4523ab6a7c6d817ff4315ddf77db489`
**Documentary base:** `dbf3287084b547226a401fd0bde2da46610f2b9b`
**Checkout mode:** `SPARSE_REQUIRED` — sufficient. No clone, no full checkout.

Documentary authority forensics. No production code, no source access, no invented numbers.

---

## The plan

| source | row_data_mode | encoding | selected_reads | full_reads | header prefix |
|---|---|---|---|---|---|
| SRC02 | SELECTED | null | 1 | 0 | not admitted |
| SRC06 | SELECTED | null | 1 (Q101@20, Q2061B@19) | 0 | not admitted |
| SRC08 | METADATA_ONLY | BIG5 | 0 | 0 | not admitted |
| SRC12 | METADATA_ONLY | WINDOWS-1252 | 0 | 0 | not admitted |
| SRC14 | SELECTED | null | 1 (v372@466) | 0 | not admitted |
| SRC26 | METADATA_ONLY_PLUS_HEADER_PREFIX | null | 0 | 0 | **admitted, 176 bytes** |
| SRC27 | FULL (outer Route-B pass EXACT 1) | latin1 | *none exists* | FLOOR 1 | not admitted |

`retries = 0` for all seven. Every value typed `FROZEN_AUTHORITY` / `IMPLEMENTATION_POLICY_CANDIDATE` /
`UNBOUND`.

---

## SRC27: "multiple path-level opens" is DESCRIPTIVE

This was the central question, and it resolves cleanly against the one-open broker. Six grounds:

1. **Origin.** `git log --reverse -S` puts it at the C4 freeze fan-in. **Zero** occurrences in the C4B
   workload freeze; **zero** in the operative C4 warrant candidate. It was never carried into the instrument.
2. **Field kind and verb.** It sits in a field named `critical_note`, uses the predictive *"will involve"*, and
   its binding clause is *"These must each be counted separately"* — a **separation** requirement, not a count.
3. **The normative statement omits it.** The same artifact's `hardened_note` is the only text using
   *"at minimum"*, and it enumerates **four** floors — existence, hash, metadata, full — pointedly **not**
   including any path-open floor.
4. **The operative candidate drops it.** Its `accounting_warning` lists the same four accounts and never says
   "multiple opens".
5. **It was accurate.** The pre-broker decoder genuinely did multiple opens per source: hash (`:483→:407`),
   metadata (`:496`), compatibility full read (`:502`), per-chunk (`:155`), prefix (`:211`).
6. **The dedicated grading lane said so.** HQ190-C graded SRC27 `ACC-03_path_opens` as **"—"** — no floor, no
   ceiling, not even a floor of 2 — while grading the other four `F1` with `ceiling: null`.

**One-open broker: compatible.** No frozen artifact supplies any SRC27 path-open value, so reducing to 1
breaches no floor. The broker still reports pass, opens, hash, metadata and full read as five separate
quantities, which is exactly what the warning was protecting against.

I deliberately did **not** numify it in either direction — `path_opens` stays `UNBOUND`, so this determination
creates no conflict.

## Does one pass imply MAX 1 decoder entry, or exactly one full read?

**Neither.** Frozen authority supplies no decoder count (HQ190-C: `ACC-06` = "—"), and `full_reads` is a
**FLOOR** of 1 with no ceiling — HQ190-C noted explicitly that "no `expected_full_reads` exists for SRC27; the
hardened note establishes a FLOOR, not an exact count."

Both may be introduced as conservative **policy** ceilings. **Chunked reading cannot substitute** for the full
read: the floor is on a full compatibility *read*, and `chunk_reads` is a different account — substituting
would change which account is satisfied rather than satisfy the same one. That is `GOV-ROUTE-004`.

## `decoder_invocations = MAX 1`: permissible as policy

It **cannot** be `FROZEN_AUTHORITY` (no count exists) and there is **no counter** in the candidate. But it
**may** be introduced as `IMPLEMENTATION_POLICY_CANDIDATE` **without higher authority**, because frozen
authority imposes no constraint — so any finite ceiling is strictly tighter and can only stop a run earlier.
It must sit in a **maximum** slot, never an expected slot, and it implements an already-accepted requirement:
the session owner must *"prevent a second decode/session when the source budget permits only one."*

---

## Two findings against the accepted candidate — both are frozen-authority violations

**SRC08/SRC12 perform a full row-data read.** This is a **frozen hard-zero violation**, not a missing feature.

`_compatibility_config` **admits** the declared encoding via `DECLARED_ENCODING_ALLOWLIST` for the exact source
SHA, so `encoding is not None`. Then `decoder.py:633-634` fires `elif encoding is not None: broker.full_read(...)`
because a metadata-only route has no `selected_variables`.

**Root cause: the candidate conflates reader configuration with row-data mode.** It therefore *cannot express*
"declared encoding + no row data" — precisely what SRC08/SRC12 require. Against: frozen zero
`row_data_reads = 0`, `expected_full_reads = 0`, `full_source_decode = false`, and the C4B D01 ceiling
*"row-data decode/full-read path is outside the frozen SRC08/SRC12 witness."* Zero-budget discipline makes a
single non-zero count a **STOP**, not a variance.

**To answer the commission's question directly: yes — a full row-data read is forbidden for SRC08/SRC12.**
Encoding configuration is independent of row-data mode.

**Unauthorized header-prefix reads on six sources.** `decoder.py:639` calls `header_prefix` unconditionally.
Only SRC26 admits it. For SRC27 the DTA **512** constant has *no* authority basis — `expected_header_prefix_bytes`
occurs **exactly once** in the frozen law (SRC26, 176), and the string `512` occurs **zero times**. So **the
176-byte prefix operation is unique to SRC26**, and 512 must not be inferred from implementation behaviour.

**SRC26 is the only conforming source** — its sequence (existence, hash, metadata, prefix 176, no row data)
matches the plan exactly.

I also flagged a **latent** risk: for SRC08/SRC12/SRC26 the candidate yields `_frame=None` with a retained
broker, so a consumer calling `iter_batches` would emit `chunk_reads` — a row-data read those plans do not admit.

---

## One judgement call worth surfacing

I rejected `PLAN_PARTIAL__SPECIFIC_AUTHORITY_GAPS_REMAIN`, which was the closest alternative. It would apply if
some source's *plan* were undeterminable. Every source's plan **is** determinate. What stays unbound are numeric
counts for path opens, decoder invocations and bytes — accounts the governing record never valued at all, which
the commission itself asked to have reported as `UNBOUND`. A determinate plan may contain typed-unknown budgets.

## Status

Nothing issued, signed or authorized. `signed/issued/authorizes_access/execution_authorized` all false. No
locators filled, no production mutation, no source access.

## Artifacts

`00_RETURN.md` · `01_SEVEN_SOURCE_OPERATION_PLAN.json` · `02_SRC27_MULTIPLE_OPENS_ADJUDICATION.json` ·
`03_DECODER_INVOCATION_POLICY.json` · `04_CURRENT_CANDIDATE_MISMATCHES.json` ·
`05_IMPLEMENTATION_CONTRACT_FOR_SESSION_OWNER.json` · `06_AUTHORITY_VS_POLICY_VS_UNBOUND.json` ·
`07_FINAL_DISPOSITION.json`

## Recommended next step for HQ

Two candidate corrections must precede the session-owner work, because both are frozen-authority violations
rather than missing features:

1. **Decouple row-data mode from reader configuration**, so SRC08/SRC12 can carry a declared encoding with zero
   row-data reads.
2. **Gate `header_prefix` on the per-source operation plan**, so only SRC26 performs one.

Then implement the per-source session owner (`GOV-SCOPE-001`) with a decoder-entry counter (`GOV-DEC-003`) and
the MAX 1 policy ceiling, and resolve the Route-B-to-chunk mapping (`GOV-ROUTE-004`).

`HQ199_R9_SEVEN_SOURCE_PLAN_RETURNED__HQ_ADJUDICATION_REQUIRED`
