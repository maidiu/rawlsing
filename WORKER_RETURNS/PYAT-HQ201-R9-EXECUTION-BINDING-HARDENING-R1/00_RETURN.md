# HQ201 — R9 execution-binding bounded hardening — R1

**Disposition: `EXECUTION_BINDING_HARDENED__READY_FOR_FINAL_INDEPENDENT_ACCEPTANCE`**
**Terminal: `HQ201_R9_EXECUTION_BINDING_HARDENING_RETURNED__HQ_REVIEW_REQUIRED`**

Source-free implementation lane. No real survey source, locator, warrant issuance,
live C4, C7 or actor/person work was performed. Nothing is adopted here.

## Identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq201-r1` |
| Startup SHA (exact) | `19f2588d860450eae9bf3fb41444d4d0b58a0c52` |
| Implementation base | `35ffa48204672e6c7180cd010a7c1adde9f18cd7` |
| Code-bearing candidate | `b8b4c99633c4aa849fd79614c5bffbd1321209b8` |
| Accepted session mechanism | `90ccbd54c549f67358d0c02ad18ff90b843cf3ee` |
| Authorities read | HQ201 adjudication `2dcc9a2ed7cf9e11ae91e01e9d8030c6ca4b85eb`; unsigned warrant successor `89054b882c04cf0541b6f9f4abdb555c808ad94d` |

All three commissioned SHAs were verified as ancestors of the startup SHA.

## Terrain

Exactly three files changed, all inside the commissioned write terrain:

- `rawlsing_next/pre553_execution_binding.py`
- `rawlsing_next/pre553_source_access_broker.py` (purely additive: one method, no line removed)
- `rawlsing_next/tests/test_pre553_execution_binding_court.py`

`pre553_source_session.py` was **not** required and is unchanged. The retry law was
established entirely in the binding layer plus one additive broker method, so the
accepted session mechanism was left exactly as accepted.

## Repair 1 — route-pass applicability

`RoutePassApplicability` is a typed enum bound **explicitly and immutably** by the
caller, defaulting to `NOT_APPLICABLE`. It is never inferred from a source key, a
file name, or from plan mode.

**Non-route execution.** The source plan executes normally and the outer observed
count is 0. A route-pass maximum of 0 means "this is not a route pass", never
"perform no source operation". Truthful typing: `route_pass_applicable=False`,
`route_pass_status="NOT_APPLICABLE"`, `full_route_passes_completed_successfully=False`,
`full_route_passes_observed=0`.

**Route execution.** `APPLICABLE` activates the outer account, with expected and
maximum enforced separately from every lower-layer account.

**Coherence fails closed at bind time.** A `NOT_APPLICABLE` spec may carry EXACT 0
or no expectation; binding EXACT 1 to a non-route spec is a contradiction and raises
`BindingError` before any access.

*Court proof that applicability is not derived from mode:* a FULL plan bound
`NOT_APPLICABLE` performs `full_reads=1` yet reports outer observed `0`, while the
SRC27-shaped FULL plan bound `APPLICABLE` reports `1`.

## Repair 2 — attempts, retries, completed passes

Three separate counters, never interchanged:

| Counter | Meaning |
|---|---|
| `route_pass_attempts` | every **admitted** wrapper attempt |
| `retries` | the lower-layer `SourceAccessAccount.retries` account |
| `completed_route_passes` | attempts that satisfied **every** postcondition |

A refused pre-operation gate is **not** an attempt: it moves all three counters and
every source account not at all.

With `retries` ceiling 0, a second `execute()` is refused **pre-operation** with
`RETRY_LIMIT_REACHED`, leaving every lower account byte-identical.

For a ceiling of 2, the measured progression is `attempts/retries` =
`1/0`, `2/1`, `3/2`, and the fourth attempt is refused with the retries account
still at 2. Each admitted retry increments the **existing** account under its own
budget ceiling before any source work.

### One exact retry binding law

The prior state was two divergent silent knobs: `SourceOperationPlan.max_retries`
was stored and reported but **never enforced**, and `SourceAccessBudget.retries` was
**never read at all**. The single law now is:

- owner: `SourceAccessAccount.retries`
- ceiling: `SourceAccessBudget.retries`
- `SourceOperationPlan.max_retries` must equal that ceiling **exactly**
- an unbounded (`None`) ceiling is refused so the retry law is always decidable

A mismatch raises `BindingError(RETRY_BINDING_MISMATCH)` at bind time. Divergence is
unrepresentable rather than merely discouraged. The untouched default path
(`0`/`0`) stays coherent, so no existing caller breaks.

## Repair 3 — completion ordering

`execute()` is ordered, and the order is load-bearing:

1. outer applicability ceiling (pre-operation)
2. retry ceiling, and the retries-account increment (pre-operation)
3. source operation
4. caller-supplied lower-layer exact/floor postconditions
5. outer expected rule, evaluated **prospectively**
6. **only then** the completion increment

Step 5 returns a prospective count without mutating anything, so a failure at step 4
or 5 cannot leave a completed pass behind. A postcondition-failed execution reports
`route_pass_attempts=1`, `completed_route_passes=0`, and the retry law then governs
whether another attempt is legal.

## Repair 4 — pyreadstat wiring

`pyreadstat_module` is stored on the execution and passed through to
`GovernedSourceSession`. `None` means "the session resolves the real pyreadstat".

Proof it is genuinely used, not stored and discarded:

- injecting the real module yields `session.broker.pyreadstat is pyreadstat` → `True`
- injecting a stub with `__version__ = "0.0.0"` raises
  `ReaderSeamViolation: READER_SEAM_VERSION_MISMATCH` at the seam, proving the
  object is actually consulted

## Courts

| Court | Result |
|---|---|
| `test_pre553_execution_binding_court.py` (hardening) | **34 passed**, deterministic over 3 consecutive runs |
| `test_pre553_source_session_court.py` | 15 passed |
| `test_pre553_source_access_broker_court.py` | 20 passed |
| R7 exact six-file court (collect-only) | 55 collected |
| R7 exact six-file court, run 1 | **55 passed** in 58.73s, exit 0 |
| R7 exact six-file court, run 2 | **55 passed** in 57.11s |

R7 environment: the governed R7 interpreter, `PYTHONHASHSEED=0`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONPATH` at the sparse worktree root,
`-p no:cacheprovider`.

The court grew from 21 to 34 tests. All fifteen required proofs are covered, and the
HQ201 adjudication's specific criticism is addressed directly: the former
`test_failed_first_attempt_is_not_reported_as_a_completed_pass` called the inner
session and never exercised the wrapper. It is replaced by
`test_failed_first_wrapper_attempt_with_retries0_blocks_second_preop`, which drives
`execute()` and asserts refusal at the wrapper boundary.

### Seven documentary plan shapes

Six non-route shapes each execute successfully with outer observed `0`,
`completed_pass=False`, `expected=0`, `maximum=0`, and the underlying work performed
(`selected_reads=1` or `metadata_reads=1`; the prefix shape records
`header_prefix_reads=1`, `header_prefix_bytes=176`).

The SRC27-shaped route gives outer observed/expected/max `1`, `full_reads` floor 1
met, `decoder_invocations` policy max 1 honoured, `retries` 0, `header_prefix_reads=0`,
and a second attempt refused pre-operation with every account unchanged.

## Source-agnostic proof

The AST court now scans **all three** production modules — binding, broker and
session — and asserts that no `SRC02`/`SRC06`/`SRC08`/`SRC12`/`SRC14`/`SRC26`/
`SRC27`/`SRC35` token and no documented variable name (`Q10B`, `Q101`, `Q2061B`,
`v372`) appears in any code string literal or identifier. A separate court asserts
that production contains no `.mode` → applicability derivation.

## Full-suite regression

| | HQ200 | HQ201 |
|---|---|---|
| failed | 333 | **333** |
| passed | 2550 | **2565** |
| skipped | 1 | **1** |
| errors | 62 | **62** |

Failures and errors are **identical**, so the additive broker change and the binding
repairs introduced no regression. The passed-count delta is fully accounted for:
HQ200's `2550` was measured while that court still had 19 tests; the final HQ200 tree
added 2 receipt-field tests, and HQ201 grew the court by a further 13
(`2550 + 2 + 13 = 2565`). Duration 477.85s.

## Holds preserved

- No real source access, locator discovery, or warrant issuance.
- No self-adoption; the disposition is a candidate for independent acceptance.
- The accepted seven-source authority was not changed. No source-specific production
  constants were introduced.
- The warrant successor's `second_pass_stop_law` is respected: a second pass is not a
  retry, and with the outer ceiling reached the refusal is pre-operation.
- SRC27's historical "multiple path-level opens" normativity remains undecided; a
  one-open ceiling stays typed `IMPLEMENTATION_POLICY`.

## Terminal

`HQ201_R9_EXECUTION_BINDING_HARDENING_RETURNED__HQ_REVIEW_REQUIRED`