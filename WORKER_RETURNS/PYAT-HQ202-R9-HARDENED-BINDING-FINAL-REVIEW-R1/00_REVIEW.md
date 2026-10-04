# PYAT HQ202 — R9 hardened execution-binding final independent review — R1

**Disposition:** `ACCEPT_HARDENED_EXECUTION_BINDING__SOURCE_FREE_R9_RUNTIME_COMPLETE_AT_BINDING_GRAIN`

**Terminal:** `HQ202_R9_HARDENED_BINDING_FINAL_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq202-r1`
Commissioned startup SHA: `217f96b5d9f7b767a7cfb11e5c2c3c7c75d77b4f` — **verified equal**
Review target: `deea40541cda0627d129dcb7d30e06e0682e0fed`; pre-hardening `35ffa4820…`
Checkout mode: `SPARSE_REQUIRED` — honored; no clone, no full worktree, sparse checkout not widened.

---

## Headline

**All four HQ201 defects are repaired, and I verified each by constructing the exact failure the
old candidate exhibited.** I found no new material defect. The warrant successor's seven plan
shapes are now executable without reinterpretation.

**Courts:** hardened binding **34/34** (grown from 21), session **15/15**, broker **20/20**, R7
**55 collected then 55/55 twice**. 179 tests, zero failures.

## The four repairs

### A — route-pass applicability: REPAIRED

Applicability is now an explicit, caller-bound `RoutePassApplicability` (default
`NOT_APPLICABLE`), and `_gate_route_pass()` is **inert for a non-route execution**. Verified:

| Case | Result |
|---|---|
| METADATA_ONLY non-route, outer EXACT 0 | `NOT_APPLICABLE`, **observed 0**, `metadata_reads=1` — the operation ran |
| SELECTED non-route, outer EXACT 0 | `NOT_APPLICABLE`, **observed 0**, `selected_reads=1` |
| FULL plan marked NOT_APPLICABLE, outer EXACT 0 | **observed 0**, `full_reads=1` |
| APPLICABLE + max 0 | `ROUTE_PASS_LIMIT_REACHED` with `_session is None` — refused **before session creation** |
| non-route max 0 | underlying source work **still runs** |
| incoherent NOT_APPLICABLE + EXACT 1 | refused **at bind time** |

**Not inferred:** a production grep finds no mode→applicability derivation, the court proves it
by AST walk, and the receipt declares `route_applicability_is_explicitly_bound: True`.

### B — attempts/retries/completions: REPAIRED

There is now **one retry binding law**: `SourceAccessAccount.retries` is the count,
`SourceAccessBudget.retries` the ceiling, and `SourceOperationPlan.max_retries` **must equal** it
(a divergent pair is unrepresentable — my own test tripped `RETRY_BINDING_MISMATCH`).

- failed first attempt + `retries=0` → second `execute()` **refused pre-operation**
  (`RETRY_LIMIT_REACHED`), and the account diff across the refusal is **NONE**;
- counters are distinct: `route_pass_attempts=1`, `retries_observed=0`, `completed_route_passes=1`;
- retries advance exactly and stop: ceiling 2 (both knobs = 2) → sequence
  `[SOURCE_BYTES_UNAVAILABLE ×3, RETRY_LIMIT_REACHED ×3]`, final `attempts=3, retries=2, completed=0`;
- the gate records a retry by touching **only** the retries account — it does not create source
  activity to account a retry.

### C — completion semantics: REPAIRED

Ordering is now: gates → attempt admission → source work → lower-layer postconditions → **outer
rule evaluated prospectively** → `self._completed = prospective`. Because the outer check returns
without mutating, a failure cannot leave a completed pass behind. Both constructions — a
lower-layer `FLOOR 999` failure and an outer `EXACT 5` failure — left **`_completed=0`**.

### D — dependency injection: REPAIRED

The module is stored (`self._pyreadstat_module`), forwarded (`pyreadstat_module=self._pyreadstat_module`),
and **demonstrably consulted**: a seam-valid but poisoned stub whose `read_sav` raises produced
`RuntimeError: STUB_READ_SAV_CONSULTED` out of `execute()`. A missing-reader stub is refused at the
seam, a wrong-version stub is refused at the seam, and omitting the parameter still resolves the
real module.

## Seven-source warrant compatibility

All **six non-route shapes** execute with outer EXACT 0 **while doing their admitted work**:

| Shape | observed | metadata | selected | full | prefix |
|---|---|---|---|---|---|
| SRC02 SELECTED | 0 | 1 | 1 | 0 | 0 |
| SRC06 SELECTED | 0 | 1 | 1 | 0 | 0 |
| SRC08 METADATA (big5) | 0 | 1 | 0 | 0 | 0 |
| SRC12 METADATA (cp1252) | 0 | 1 | 0 | 0 | 0 |
| SRC14 SELECTED | 0 | 1 | 1 | 0 | 0 |
| SRC26 METADATA + 176 prefix | 0 | 1 | 0 | 0 | **1** |

**SRC27-shaped route:** pass 1 completes (`observed=1`, `full_reads=1`, `chunk_reads=0`,
`prefix=0`); pass 2 is refused pre-operation. `full_reads` FLOOR 1 is satisfied by `full_reads`
and **explicitly not** by `chunk_reads` — a CHUNKED_FULL execution with that floor was refused.
`decoder_invocations`/`path_opens` remain policy-only lower-layer fields, no byte ceiling is
invented, and expected/floor/maximum/observed stay distinct.

## Test coverage was genuinely repaired

The two tests HQ201 identified as locking in defects are **gone**. The binding court grew 21 → 34
with adversarial coverage driving the **public** `execute()` path (17 call sites), including the
non-route/exact-0 cases, retry pre-operation refusal, counter distinctness, retry-knob
disagreement, injection consultation, and the chunk-vs-full floor.

## Advisories (non-blocking)

1. A retry ceiling of N admits **N+1 total attempts** (1 initial + N retries). Self-consistent,
   but the warrant-facing reader should be told `SourceAccessBudget.retries` counts *retries*, not
   attempts.
2. An **admitted** retry calls `_ensure_session()` to reach `record_retry()`; the physical open
   stays lazy so no source I/O occurs, and the refused path raises before any source operation.
   Worth noting if a future layer asserts "no session object unless a source operation ran".
3. Unchanged boundaries from HQ200/HQ201: an in-process owner cannot enforce cross-process/cross-run
   uniqueness, and no real-source numeric reader-byte ceiling is source-free established.

## Holds observed

Synthetic carriers only; zero real survey/source access; zero locator discovery; zero warrant
issuance; zero live C4; no production mutation; no C7 or actor/person work. No adoption or
self-adoption. Nothing written outside the commissioned return directory.

---

## Disclosure — an unattributed file appeared in this return directory

While preparing the packet I found a file I did **not** author in
`evidence/`: `01_independent_proofs.py` (984 lines, 44 400 bytes, blob
`11381084b976c8083c17f37e1d728e4c4cc10b86`). Its own docstring says *"Written by the HQ202
reviewer from the commission text alone."*

**How I established I did not create it:**

- my five evidence files are **byte-identical** (`cmp`) to the scripts I actually ran from
  `/tmp` (`hq202_attack.py`, `hq202_attack2.py`, `hq202_inject.py`, `hq202_warrant.py`,
  `hq202_court.log`);
- that file has **no** counterpart in `/tmp` — nothing I copied in;
- its mtime (`09:06:16`) is ~8 s **after** my own evidence files (`09:06:07–09:06:08`);
- it appears in **no commit** in any ref.

**What I did about it:** I ran it out of caution (with `PYTHONPATH` set). It exits 0 and its
`D2–D6` round independently reproduces the same conclusion I reached in Attack D — the supplied
module is genuinely consulted, not merely stored — which **corroborates** my finding.

**I nevertheless excluded it from my commit.** I cannot attest to authorship of a file I did not
write, and my acceptance must rest only on evidence I produced and verified. Every claim in this
review is carried by my own attested evidence files.

**Why this is recorded rather than quietly deleted:** a file appearing mid-review in a reviewer's
own return directory, asserting reviewer authorship, is a provenance hazard for an unattended
pipeline. Whoever produced it should account for it. It did **not** alter any conclusion here.
