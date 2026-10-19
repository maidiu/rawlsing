# Court A — N9J Independent Reproduction and Adversarial Review

Target: `7628840c4c8e95b320cadc672743355afbe2958a`
(worker return `WORKER_RETURNS/PYAT-R37-N9J-SELECTED-WORLD-PROGRESSIVE-CONSUMER-R1`)
Pinned read-only worktree: `R38-N9TI-N9J-pin-7628840c4`.
Verdict: **REVISE (bounded)** — frozen-value grain ACCEPT, adapter-seam grain
REVISE (finding N9J-F1). See `00_INDEPENDENT_REVIEW_VERDICTS.md`.

## Custody

* Worker CI artifact independently downloaded and parsed: run `39173649313`,
  head `aa6eb4c96…`, artifact `pyat-r37-n9j-sourcefree-junit-39173649313`,
  20 tests, 0F/0E/0S, 8.466 s.
* Custody diff `aa6eb4c96..7628840c4` is documentation-only: `00_RETURN.md` +
  `04_NATIVE_EXECUTION_AND_DEVIATION_RECEIPT.json`. The tested head and the
  target therefore carry identical executable content.
* Frozen file `01_FROZEN_BEFORE_EXPERIMENT.json` is a separate precommit
  (`8c49333a7`, `execution_state: PRECOMMITTED_UNEXECUTED`) — the freeze is
  Git-order verifiable for this court.

## Reproduction (cold, reviewer's own run)

* Worker test suite `rawlsing_next/tests/test_pyat_r37_n9j_sourcefree.py`
  (test_00..test_17, parametrize → 20 runs): **20 passed**, 15.981 s
  (`evidence/n9j-repro-i2.xml`). Two fresh interpreters, exactly as the return
  claims.

## Reviewer adversarial suite (`evidence/test_i2_adversarial_n9j.py`)

Written from the frozen expectations, the staged native sources and the pinned
closure only; the worker suite is not imported. Tests and what they
independently establish:

* a01 values read originate from the named native producer (structural and
  empirical channels).
* a02 base progressive denominators/fractions recomputed from the 58-row cell
  counts: 9/16, 5/8, 3/4 with exact-fraction consistency on cell `1`.
* a03 changed-source chain: 19/32, 11/16, 7/8 recomputed and matched.
* a04 opposite-minority chain matches worker test_04 exactly:
  (26,{15,11}) → 15/26; (12,{6,6}) → 6/12; (6,{2,4}) → 4/6.
* a05 same-marginals rewrite preserves marginals, changes counts, differs from
  the changed chain.
* a06 zero-support is typed at the service layer
  (`PARTIAL_TYPED_EMPIRICAL_SUPPORT`, denominator 0, cells [], uncertainty
  `NO_SUPPORTED_EVIDENCE`).
* a07 forward-only denominators (no reverse conditioning).
* a08 three clocks remain distinct and explicit.
* a09 revocation is directional; archival receipts retained, dependents typed
  partial.
* a10 all three refusal classes: `UNREGISTERED_SELECTED_SNAPSHOT` (foreign
  config), `ACCEPTANCE_BINDING_MISMATCH` (foreign serve),
  `ACCEPTED_SNAPSHOT_SUBSTITUTION` (crossed snapshot).
* a11 cold replay: identical counts across two fresh subprocesses
  ([[32,{0:14,1:18}],[16,{0:6,1:10}],[8,{0:2,1:6}]]).
* a12 structural-only revision leaves empirical/native bytes untouched.
* a13 budget ladder/material-affordability semantics (fee > budget blocks,
  access TRUE preserved, proposal feasible).
* a14 **(red, deliberate falsifier)** — adapter seam must type the zero-support
  step; it does not.

Result: **13 passed, 1 failed** (11.635 s; `evidence/n9j-adversarial-i2.xml`,
timestamp `2026-10-18T21:03:28-04:00`).

## Finding N9J-F1 (reproduced defect, bounded REVISE class)

Red test: `test_a14_adapter_serve_must_type_zero_support_step_without_keyerror`.

Minimal reproduction: build the N9J adapter over
`GenericSelectedWorldService(support_loss=True)`, accept a standard request,
call `adapter.serve(...)`. Expected: a typed partial receipt (the service
already types this state). Observed:
`KeyError: 'binding_order'` raised from
`e05_n9_selected_world_adapter.py:462` (`binding_order=step['binding_order']`).
The R11 adapter's serve rebuilds each progressive step field-by-field and
assumes `binding_order` exists; the service's zero-support step does not carry
it.

Properties:

* Untyped crash — violates the adapter's declared refusal contract
  (`N9SelectedWorldRefusal`/`SelectedWorldInconsistency` subclasses of
  `ValueError`).
* Fails closed — no fabricated probability/completion escapes.
* Uncovered by the worker's 20 green tests: worker `test_05` exercises
  `service.possibilities` only; the adapter `serve()` seam on the zero-support
  path is untested.
* Fix exists upstream: R13 `690790e8…` at `84485d32c…` deep-copies steps and
  emits a typed partial receipt. Court B (t12) independently proves the same
  probe is typed under R13.

Required revision (scoped): adopt R13 step handling or add the missing key
contract to the R11 adapter, plus an adapter-level zero-support regression
test. No frozen value or numeric claim changes.

## Recorded preregistration-vs-delivery deviation

Frozen hostile `access_TRUE_fee_7_budget_5__nonparent_blocked__proposal_access_premise_only`
has no literal implementation (fee options are 2 and 6; no fee-7 exists). The
delivery operationalizes the intent via budget = 1 (fee 2 > budget 1 ⇒ blocked
while access TRUE and proposal feasible). Reviewer suite a13 reproduces the
intent semantics independently. Recorded as a deviation for custody
completeness, not as a defeat.
