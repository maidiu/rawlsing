# PYAT HQ202 — R9 hardened execution-binding final independent review (R1)

- Repository: `maidiu/rawlsing`
- Commissioned startup SHA: `217f96b5d9f7b767a7cfb11e5c2c3c7c75d77b4f`
- Review target: `deea40541cda0627d129dcb7d30e06e0682e0fed`
- Pre-hardening candidate (control only): `35ffa48204672e6c7180cd010a7c1adde9f18cd7`
- Warrant successor under test: `89054b882c04cf0541b6f9f4abdb555c808ad94d`
- HQ202 adjudication read by exact object: `329a37455151f479886bd3cbb40d4d98d016fb13`
- Checkout mode: SPARSE_REQUIRED (honoured: existing sparse worktree, manifest exactly as commissioned, not widened)
- Model: DeepSeek V4.1 Flash — DeepSeek Harness

## Disposition

`ACCEPT_HARDENED_EXECUTION_BINDING__SOURCE_FREE_R9_RUNTIME_COMPLETE_AT_BINDING_GRAIN`

## 0. Concurrency disclosure (read this first)

A **second agent ran the identical commission concurrently**, in the same sparse worktree, on the
same branch, and **pushed first**: `origin/agent/reviewer-pyat-hq202-r1` moved from the
commissioned `217f96b5d9f7b767a7cfb11e5c2c3c7c75d77b4f` to `0deb64784829661780ee3957f8070ccc2c241722`
while this review was running. That packet carries the same disposition.

Neither agent destroyed the other's work. The first return excluded an unattributed file that
happened to be this reviewer's evidence script; this reviewer found the first return's files
appearing in its own return directory and isolated its own work instead of overwriting.

Actions taken:

- `origin/agent/reviewer-pyat-hq202-r1` was **left untouched** at `0deb6478`, by explicit HQ
  instruction, so any adjudication pinning is undisturbed.
- This review is published on
  **`agent/reviewer-pyat-hq202-r1-independent-corroboration`**, based on the commissioned startup SHA, so the return
  directory on that branch contains exactly this reviewer's packet.

Substance: every claim below rests on this reviewer's own executions and its own evidence logs.
The other packet's disposition **was** read before these proofs finished, and that is disclosed as
a possible anchoring influence. The two reviews agree, and they are independent corroborations
rather than one artifact reused twice.

## 1. What was reviewed

Six blobs at the review target were pinned by SHA-256-bearing Git object id before any execution:

| file | blob |
|---|---|
| `rawlsing_next/pre553_execution_binding.py` | `0e11af2205a01dcf32aca3e462540040a62e9a29` |
| `rawlsing_next/pre553_source_session.py` | `ac1390b861f69d21b65d9af25af9fa49cd217e08` |
| `rawlsing_next/pre553_source_access_broker.py` | `090d978bbd631820938f6f76252e09674f44ff99` |
| `rawlsing_next/tests/test_pre553_execution_binding_court.py` | `67492110a1485eed44c88d1bb9cd0ac27ecebd2a` |
| `rawlsing_next/tests/test_pre553_source_session_court.py` | `8b45e3f9ac144077b1f3c7c057dd33f0c96aafae` |
| `rawlsing_next/tests/test_pre553_source_access_broker_court.py` | `c1bc827329846ab8ded9ee0a4307cd1680bbdf08` |

Nothing outside those blobs and the two warrant JSON objects was treated as candidate behaviour.

## 2. Method

Four independent evidence programs were written from the commission text, not from the candidate's
court, and are committed under `evidence/`:

1. `01_independent_proofs.py` — rounds A, B, C, D. **29/29 claims pass.**
2. `02_warrant_compatibility.py` — reads the accepted warrant and **derives** every constraint from
   it. **9/9 checks pass.**
3. `03_adversarial_observations.py` — bounds the claim with the residual edges.
4. `04_prehardening_control.py` — reproduces the four HQ-bound defects at
   `35ffa48204672e6c7180cd010a7c1adde9f18cd7` to prove the proofs are discriminating.

All candidate execution was driven through the public `BoundSourceExecution.execute()`. Synthetic
SAV/DTA carriers only. No real source was opened, no locator was discovered, no warrant was issued.

## 3. A — route-pass applicability

**Verdict: CALLER_BOUND_AND_EXPLICIT.**

- Metadata-only non-route execution with outer EXACT 0: runs, outer observed 0, `metadata_reads=1`.
- Selected non-route execution with outer EXACT 0: runs, outer observed 0, `selected_reads=1`,
  `full_reads=0`.
- FULL plan marked NOT_APPLICABLE: runs, outer observed 0, `full_reads=1`.
- APPLICABLE route MAX 0: refused with `ROUTE_PASS_LIMIT_REACHED` **before any session existed** —
  `session_created=false`, `route_pass_attempts=0`, empty account snapshot.
- Non-route MAX 0: does not block the underlying source work.
- NOT_APPLICABLE + EXACT 1: refused with `BindingError` at spec construction, on a path that does
  not exist, so nothing was accessed.
- Decisive non-inference test: **the same `source_entry_key` (`SRC27-SHAPED`) and the same FULL
  plan** behaves differently purely as a function of the caller's bound applicability. Applicability
  follows the binding, not the key and not the mode.
- The default applicability is `NOT_APPLICABLE`; a defaulted spec with EXACT 1 is refused at bind.

## 4. B — attempts, retries, completions

**Verdict: SINGLE_OWNER, PRE_OPERATION, CEILING_BOUND, EXACT.**

- The first admitted attempt is not a retry (`retries=0`).
- Failed first attempt + `retries=0` ⇒ the second `execute()` is refused **pre-operation** with
  `RETRY_LIMIT_REACHED`, and the full account dict is **byte-identical** before and after the
  refusal.
- `route_pass_attempts`, `retries` and `completed_route_passes` are three distinct counters. In one
  measured run: **attempts=3, retries=2, completed=1** — all three pairwise distinct.
- The retry count **is** the existing `SourceAccessAccount.retries`: the session account, the
  outcome receipt and the execution property all agree.
- `SourceAccessBudget.retries` owns the ceiling, measured for ceilings 0, 1, 2, 3: exactly `N+1`
  attempts are admitted and the `N+2`-th is refused with `RETRY_LIMIT_REACHED`.
- `SourceOperationPlan.max_retries` cannot silently disagree: plan>budget, budget>plan, an
  unbounded (`None`) ceiling, and a disagreeing `with_plan()` swap are all refused at bind time.
- **Failure before session creation** (a seam-invalid injected module): the first attempt is
  admitted and fails; with `retries=0` the second is refused and **no session is ever created**.
- **Failure after session creation** (SHA-256 mismatch): with `retries=0` the second is refused
  with an unchanged account; with `retries=1` the retry is charged **before** the second source
  operation, and the third attempt is refused.
- **A retry gate must not create source activity merely to account the retry**: admitting a retry
  moves the retries account by exactly 1, adds exactly 1 decoder entry and exactly 1 reader
  invocation — the one real operation — and leaves `path_opens` at 1. Accounting itself issues no
  reader call.

## 5. C — completion semantics

**Verdict: COMPLETION_ORDERED_LAST.**

- Source success + **lower-layer postcondition** failure: `POST_EXECUTION_CONSTRAINT_FAILED`,
  `completed_route_passes=0`, `full_reads=1` (the source operation really did succeed first).
- Source success + **outer exact** failure: `POST_EXECUTION_CONSTRAINT_FAILED`,
  `completed_route_passes=0`, `full_reads=1`, and a following attempt is still refused by the retry
  gate — so no completion leaked anywhere.
- Positive control: once every postcondition succeeds, completion **does** occur (`completed_pass=true`,
  outer observed 1).
- The outer count advances only after all lower rules; a lower-rule failure leaves it at 0.
- A non-route execution never manufactures a phantom completion.

## 6. D — dependency injection

**Verdict: SUPPLIED_OBJECT_REACHES_THE_SEAM_AND_IS_CONSULTED.**

- The exact supplied object is retained on the execution and is the object held by the broker:
  `ex.pyreadstat_module is stub` and `ex.session.broker.pyreadstat is stub`.
- It is genuinely consulted: the stub recorded `metadataonly=True`, `apply_value_formats=False`,
  `user_missing=True`, `encoding='BIG5'`, and received a `_GovernedView` exposing `fileno()`.
- Exclusivity: the real `pyreadstat.read_sav`/`read_dta` were replaced with a raising poison for the
  duration and were **never called**.
- The parameter is load-bearing, not merely stored: with a supplied inventory of
  `[alpha, beta, gamma]`, a SELECTED read of `gamma` bound ordinal **3**.
- Fail-closed: a wrong-version stub and a stub missing `read_dta` are both refused at the seam;
  omitting the parameter resolves the real pinned module (1.3.6).

## 7. Seven-source warrant compatibility

**Verdict: COMPATIBLE.** The warrant was read, not transcribed. FROZEN expectations became runtime
`EXACT` constraints, FROZEN floors became `FLOOR`, `PENDING_HQ200_RUNTIME_ACCEPTANCE` maxima became
`IMPLEMENTATION_POLICY` `MAXIMUM` ceilings, `PENDING`/null expectations produced no number, and
`UNBOUND_SOURCE_DEPENDENT` byte accounts produced no ceiling.

- All six non-route shapes (SRC02, SRC06, SRC14 SELECTED; SRC08, SRC12, SRC26 METADATA_ONLY) execute
  and observe outer **0**, with every FROZEN expectation satisfied.
- The SRC27-shaped route executes once with outer EXACT/MAX 1, then refuses the second attempt
  pre-operation with an unchanged account.
- `full_reads` FLOOR 1 is satisfied by `full_reads` and is **not** satisfiable by a chunk-only route.
- Decoder and path-open maxima remain **policy only**, and are genuinely enforced (both produce a
  budget refusal when tripped); no frozen expected count exists for either.
- `retries` max 0 works for all seven.
- **No prefix on the SRC27-shaped route**; the 176-byte prefix is SRC26's alone.
- Source-dependent byte ceilings remain **uninvented**: no numeric `reader_bytes`/`hash_bytes`
  ceiling appears in the binding, every budget leaves them `None`, and observed byte use is still
  reported.
- Production carries no `SRCxx` token, no row-data-mode reference, and every applicability decision
  reads `self.spec.route_applicability`.

Warrant accounts with no runtime counterpart are reported rather than silently dropped:
`metadata_reads` where the warrant leaves it PENDING, `row_data_reads`, `selected_columns`,
`raw_nominal_case_size`, `decoded_dictionary_data_width`, and the source-dependent byte account.

## 8. Qualification

| run | result | exit |
|---|---|---|
| hardened binding court | 34 passed in 1.28s | 0 |
| session court | 15 passed in 1.05s | 0 |
| broker court | 20 passed in 1.17s | 0 |
| R7 six-file collect-only | 55 tests collected in 1.06s | 0 |
| R7 six-file run 1 | 55 passed in 69.36s (0:01:09) | 0 |
| R7 six-file run 2 | 55 passed in 74.55s (0:01:14) | 0 |

Environment: `LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python` — Python 3.11.3,
pyreadstat 1.3.6, `PYTHONHASHSEED=0`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONPATH=<worktree root>`,
`pytest -p no:cacheprovider`. Every exit code was recorded.

No fixture workaround was required: the commissioned sparse manifest already names the only
repository-committed fixture the six-file court reads.

## 9. Pre-hardening control — the proofs are discriminating

Run against a read-only `git archive` of `rawlsing_next` at `35ffa48204672e6c7180cd010a7c1adde9f18cd7`,
the same four defects the HQ201 review bound are **all reproduced**:

- **A**: no `RoutePassApplicability` exists; a metadata-only non-route execution with outer MAX 0 is
  refused `ROUTE_PASS_LIMIT_REACHED` — the outer zero really did mean "no source operation".
- **B**: with `retries=0`, a second attempt after a failed first attempt still reached real source
  work (`metadata_reads` 1 → 2); the retry ceiling is never consulted and `record_retry` does not
  exist.
- **C**: `_passes_completed` is incremented **before** the constraints, so a failed attempt leaks a
  completion. With an outer EXACT 2 / MAX 3, the second attempt reports observed **2** although only
  one attempt satisfied everything.
- **D**: the supplied module is discarded — the broker holds the real pyreadstat and the stub is
  consulted 0 times.

Every one of these is repaired at `deea40541cda0627d129dcb7d30e06e0682e0fed`.

## 10. Advisories

See `06_FINAL_DISPOSITION.json`. In short: ADV-1 retry semantics is N+1 attempts; ADV-2 only the
outer MAXIMUM is a pre-operation gate; ADV-3 an unknown account name is not refused at bind;
ADV-4 the public `session` accessor bounds the claim to in-process governance; ADV-5 no real-source
byte ceiling is invented.

None of these is material to the commissioned disposition, and each is either unreachable from the
accepted warrant or already placed outside this grain by the HQ202 adjudication.

## 11. Scope

No locator discovery, no real-source access, no warrant issuance, no live C4, no C7, no actor/person
work. Synthetic carriers only. This review does not adopt the candidate, does not close R9, and does
not issue anything.
