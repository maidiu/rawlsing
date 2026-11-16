# FIABC LiTS R5B successor repair continuation handoff

Date: 2026-09-22

## Mission and present position

The immediate mission is to close the LiTS-I candidate-neutral oracle producer
against the exact adopted source/runtime authority before any A/B/C execution.
The producer had progressed through a sequence of real, fail-closed defects:

1. decoder-native float tokens did not match the accepted historical LiTS
   physical-key representation;
2. current I03 operation and D03 risk-set authority were absent from the live
   binding;
3. retained constituent-I03 fact preimages were missing;
4. current and historical learned-product hashes were incorrectly compared
   across different schemas;
5. terminal counts were accidentally projected from one field for every
   source, regressing frozen WVS7 truth;
6. the accepted base C11 release lacked q310/q311 and therefore could not
   satisfy the adopted runtime binding, which names the R5B successor release.
7. the adopted successor stores q310/q311 response events as exact Decimal
   witnesses while the frozen F02 predicate dialect retains integer
   source-native tokens.

Items 1–7 are repaired and source-free tested on the branch. Commit
`152c4885...` reconstructs the exact adopted R5B successor without a second
source decode. Commit `e4faa552...` binds the D03 risk sets to exactly the base
and adopted successor releases. Commit `8ea52e74...` adds the exact, opt-in F02
event-representation successor authority. A third live source pass must now
prove the expected 49 supported / 1 valid-empty envelope or expose the next
concrete terminal.

This is still a **pre-candidate court**. It is not A/B/C execution, measured
P2X, performance selection, promotion, or certification.

## What the current producer does

`rawlsing_next/fiabc_final_oracle_freeze_producers.py` now performs this exact
LiTS path:

1. verifies the canonical source SHA and 29,002 × 1,198 shape;
2. calls `decode_dta(..., encoding="latin1")` once;
3. builds the accepted banked LiTS projection;
4. verifies the adopted runtime catalog, active binding, and runtime release;
5. replays the exact historical base candidate through the exact legacy facade
   and bounded LiTS representation authority;
6. verifies the base candidate projection, base C11 release, and base replay;
7. deploys the exact R5B driver and four support blobs from commit
   `648a39ad...`;
8. verifies the frozen F02 q310/q311 closure and real-source summary;
9. reuses the already-decoded incidence to build only the exact q310/q311
   extension;
10. builds and validates the complete successor candidate;
11. verifies the successor projection, release, replay, and exact repository
    resolution;
12. binds the adopted runtime authority to that successor repository and runs
    the common carrier-neutral I05 path;
13. requires 50 candidates, 77 query roles, and the accepted LiTS coverage
    envelope of 49 supported plus 1 valid-empty;
14. materializes the candidate-neutral oracle while recording zero candidate
    processes and zero candidate outputs.

The historical base is not replaced or relabeled as the successor. Both
identity layers are checked separately.

## Exact Git state

- Repository: `https://github.com/maidiu/rawlsing.git`
- Continue branch: `agent/rabochii-premain-fiabc-lits-representation-authority-repair-r1`
- Source-free code checkpoint: `8ea52e744aeb238f503d62ddc030380ff31aa84e`
- Continue from the fetched repair-branch tip containing this handoff and its
  adjacent continuation pointer receipt; the branch tip must descend from the
  source-free code checkpoint.
- Diagnostic-line head: `a8d4faac8912e9c03840d3f72a4f2ca8c83d6903`
- Governed P2X execution head: `78caf7eb4396dd576cf478c860372b7e26455cd9`
- The governed P2X execution branch has not been advanced by this repair.

Fetch and fail closed before continuing:

```bash
git fetch origin \
  agent/rabochii-premain-fiabc-terminal-readiness-r1 \
  agent/rabochii-premain-fiabc-lits-representation-authority-repair-r1 \
  agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1
git merge-base --is-ancestor 8ea52e744aeb238f503d62ddc030380ff31aa84e origin/agent/rabochii-premain-fiabc-lits-representation-authority-repair-r1
git show origin/agent/rabochii-premain-fiabc-lits-representation-authority-repair-r1:WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/20_LITS_R5B_SUCCESSOR_REPAIR_CONTINUATION_HANDOFF.md >/dev/null
test "$(git rev-parse origin/agent/rabochii-premain-fiabc-terminal-readiness-r1)" = a8d4faac8912e9c03840d3f72a4f2ca8c83d6903
test "$(git rev-parse origin/agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1)" = 78caf7eb4396dd576cf478c860372b7e26455cd9
```

## Completed and pushed

The repair branch contains these consecutive checkpoints:

1. `3e4fad869e1b4fbfb410ec4812147d5c44bdc60f` — typed LiTS authority repairs.
2. `b52a990b00e296a7d133b38b212a4f96d4da311f` — source-specific terminal-count domains; LiTS uses `coverage_state`, WVS7 preserves frozen `typed_state`, unknown sources fail closed.
3. `152c48852937ed112e1de9ef5d390c79f2fca610` — exact adopted R5B successor construction from the already-decoded LiTS incidence, with historical base candidate/release/replay verification retained as an intermediate.
4. `e4faa55207c5a29bc2e2484dc0e7ae1fd535da21` — exact D03
   R2/R7/R27 risk sets carried onto the adopted R5B successor under an explicit
   two-release preservation authority; no other release or target is admitted.
5. `8ea52e744aeb238f503d62ddc030380ff31aa84e` — exact F02
   q310/q311 runtime-event representation authority. It binds only six frozen
   question/value pairs on the adopted successor release from integer
   source-native tokens to exact Decimal event witnesses; generic numeric
   coercion and every other source/release/scope/question/value/state remain
   forbidden.

The focused source-free court at `8ea52e74...` is green:

```text
71 passed
```

The exact test command was:

```bash
/private/tmp/fiabc-runtime-venv.nW65x5/bin/python -m pytest -q \
  rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py \
  rawlsing_next/tests/test_fiabc_t5_live_terminal_control.py \
  rawlsing_next/tests/test_fiabc_lits_i_i03_operation_authority.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_pre553_independent_parity_oracle.py
```

The canonical qualification pytest body, extended with the new LiTS authority
tests, is also green:

```text
207 passed, 28 subtests passed in 27.49s
```

The historical `test_fiabc_w3_i04_runtime_packaging_rebind.py` still asserts an
obsolete WVS lock and the pre-successor materializer blob. It is not silently
rewritten here. The eventual full qualification wrapper must explicitly rebind
the current materializer identity and preserve current WVS successor truth.

## Exact adopted identities

- LiTS source SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- Historical base C11 release: `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`
- Historical base replay: `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`
- Historical base candidate projection: `7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c`
- Adopted successor release: `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`
- Adopted successor replay: `30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`
- Adopted successor candidate projection: `23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb`
- Adopted R5B commit: `648a39ad5bed42f66e066410af5869604d29c12d`
- Active runtime binding: `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`

## Source-backed evidence and current unresolved boundary

A fresh common LiTS source pass from `152c4885...` completed after about 46
minutes with no A/B/C candidate process. It successfully reconstructed and
validated the exact base and successor candidate/release/replay layers, then
reached common I05. Its terminal was:

```text
candidate_count = 50
query_role_count = 77
candidate_processes_started = 0
coverage_state_counts = {"EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY": 50}
fact_state_counts = {"UNRESOLVED": 36, "ZERO_SUPPORT": 24}
```

The emitted facts exposed full-source denominators of 29,002 instead of the
accepted D03 R2/R7/R27 denominators 24,897 / 28,325 / 24,630. The exact cause
was a release-scope mismatch: the D03 overlay authority named only base release
`e6c954...`, while I05 correctly executed adopted successor `192926...`.

Commit `e4faa552...` repaired that boundary source-free. A second fresh common
LiTS source pass then completed after about 46 minutes with no A/B/C candidate
process. It proved the exact D03 repair and emitted:

```text
candidate_count = 50
query_role_count = 77
candidate_processes_started = 0
coverage_state_counts = {"EVALUATED_SUPPORTED": 31, "EVALUATED_VALID_EMPTY": 19}
fact_state_counts = {"SUPPORTED": 36, "ZERO_SUPPORT": 24}
```

All five P0 positive controls, the P1 joint-dependence candidate, and all 25 P4
joint-cell candidates were supported. The single P3 conditional-reversal
candidate was the expected valid-empty. All 18 P2 higher-order candidates were
incorrectly valid-empty because their q310/q311 conditioner events never
matched.

The exact cause was representation, not missing data or risk-set authority:
the adopted R5B `exact_cell()` path turns source floats into `Decimal(str(x))`,
and the exact legacy facade stores canonical `{"$exact_decimal":"1"}` event
witnesses. The frozen F02 dialect correctly retains integer
`source_native_value` tokens. Predecessor code compared those exact objects
directly, so all q310/q311 predicates selected zero respondents.

Commit `8ea52e74...` repairs only that boundary. Authority content hash
`96f32bef2d098ae67debd3487cc0f30d8fe4b2a3aacb775c037b854ef499b688`
binds the exact six q310/q311 question/value pairs on successor release
`192926...`; it adds no generic int/float/Decimal equivalence. The required next
evidence is a third fresh common LiTS source rerun. The accepted source-backed
49/1 terminal is therefore **not yet claimed green**.

Failed-run evidence root on this host:

```text
/private/tmp/fiabc-lits-successor-source.JN5rJj
/private/tmp/fiabc-lits-d03-successor-rerun.oN1nb1
```

That path is not portable. On this or another machine, rerun exactly:

```bash
repo="$PWD"
diagroot="$(mktemp -d /private/tmp/fiabc-lits-successor-source.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$repo" \
  /private/tmp/fiabc-runtime-venv.nW65x5/bin/python -u \
  -m rawlsing_next.fiabc_final_oracle_freeze_producers produce-lits \
  --repo-root "$repo" \
  --source "/Users/matthewsmith/Desktop/Rawlsing/data/Data/LiTS_I.dta" \
  --work-root "$diagroot/work" \
  --output "$diagroot/lits_oracle_freeze.json"
```

Required runtime gate: CPython 3.11.3, `pyreadstat==1.3.6`, `pyarrow==25.0.1`.

## Parameters and non-negotiable invariants

- Canonical LiTS source path used on this host:
  `/Users/matthewsmith/Desktop/Rawlsing/data/Data/LiTS_I.dta`.
- Source identity and shape must be exact; no equivalent filename or inferred
  source is accepted.
- One source hash pass and one decoder call are the intended physical-source
  accounting for this producer.
- The exact pinned runtime must pass `verify_runtime_gate`; do not relax or
  monkeypatch the gate.
- The legacy numeric representation bridge applies only to the authorized
  LiTS-I variables/tokens and explicitly grants no authority to other sources,
  waves, variables, values, labels, frequencies, or missingness inferences.
- The adopted successor is not inferred from the runtime constant. It must be
  reconstructed from exact R5B bytes and independently match all frozen
  successor identities.
- Expected truth remains candidate-neutral and must exist before any candidate
  output.
- WVS7 uses `receipt.typed_state` for its frozen terminal-count domain. LiTS-I
  uses `receipt.coverage_state` for its accepted 49/1 envelope. Unknown sources
  fail closed.
- The new I03-operation successor, D03 risk-set overlay, historical snapshot
  fallback, and q310/q311 scalar-token machinery remain opt-in through
  `Pre553RuntimeAuthoritySet`; absent runtime context retains predecessor
  behavior.

## Known concerns and how to adjudicate them

1. **Source pass may fail before successor identity.** Treat the first stack
   trace as the next bounded defect. Do not bypass a blob, F02, source-summary,
   projection, candidate, release, or replay check.
2. **Source pass may reproduce the successor but fail I05.** Inspect the emitted
   `current_i05_precheck.json` and distinguish authority, coverage, typed-state,
   and fact-preimage failures. Do not collapse those domains.
3. **A repair may accidentally broaden representation authority.** Preserve the
   LiTS source/variable/type/token allowlist and its negative limits. A generic
   int/float/Decimal equivalence rule is forbidden.
4. **A repair may regress WVS7.** Always rerun the WVS-anchored terminal-control
   regression against
   `WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json`.
5. **A repair may turn wave-specific law into generic code.** The universal seam
   may carry source/wave authority, but it may not invent it. Keep dispatch
   explicit and fail closed for unknown sources.
6. **A long silent run may look stalled.** Confirm PID state, CPU, elapsed time,
   and memory before intervening. The full LiTS base materialization is
   CPU-heavy and previously ran for many minutes without stdout.
7. **Ephemeral evidence is not portable.** `/private/tmp` roots and a running PID
   do not transfer to another machine. Bank every code/test/document change and
   exact terminal receipt in Git before relying on it.

## Ground already covered

- Exact remote-head discipline and isolated repair branch.
- Correct pinned Darwin runtime established.
- Candidate-neutral LiTS representation diagnostic completed.
- Bounded LiTS typed-representation authority implemented with hostile tests.
- Exact legacy facade/blob replay installed without weakening the current typed
  facade globally.
- Current I03 operation authority and D03 exact risk-set overlay integrated.
- Historical authority snapshot fallback bounded to exact adopted evidence.
- q310/q311 scalar-token and exact event-representation machinery made
  runtime-authority opt-in.
- Retained I03 fact-preimage closure repaired.
- ASTRA cross-schema hash-domain defect repaired while preserving the immutable
  historical product identity.
- WVS7 source-specific terminal-count regression repaired and anchored to its
  frozen oracle.
- Exact R5B driver/support deployment and successor constitution added.
- First successor-backed source pass proved exact base/successor construction
  and isolated the D03 release-scope mismatch before the accepted terminal.
- D03 R2/R7/R27 overlay extended to exactly the adopted R5B successor with
  explicit preservation and negative limits.
- Second successor-backed source pass proved the D03 repair and isolated the
  exact F02 event-representation mismatch at 31 supported / 19 valid-empty.
- Exact six-binding F02 representation successor authority added with hostile
  negatives for wrong release, response ref, witness, and unadopted/tampered
  authority.
- Focused source-free court green at 71 tests on `8ea52e74...`; canonical
  qualification pytest body green at 207 tests plus 28 subtests.
- No A/B/C process and no measured P2X run by this repair.
- Governed execution branch preserved at `78caf7eb...`.

## Ground left to go

Proceed in this order and stop at the first failure:

1. Run the third fresh common LiTS source pass from `8ea52e74...`.
2. If it fails, make the narrowest authority-preserving repair, add a hostile
   source-free regression, rerun the focused court, commit, and push.
3. Repeat until the source pass emits the accepted 49/1 LiTS envelope and a
   verified frozen oracle with zero candidate processes.
4. Run the full canonical source-free qualification, not only the focused 67
   tests. Preserve its static cross-lane assertions and required subtests.
5. Run the governed pre-candidate preflight only after the new code is
   source-free green. It must remain candidate-neutral through the T3/oracle
   boundary.
6. Independently recheck WVS7 frozen truth and static noninterference after the
   final LiTS repair.
7. Prepare an exact promotion/transition receipt that names the qualified
   repair SHA. Do not move the execution branch merely because a local source
   pass succeeded.
8. Only after the governing promotion authority explicitly permits it may the
   execution branch advance and the A/B/C/P2X sequence resume.

## Banking for the 35-wave program

The existing universal carrier→C11→I03/I05 seam is structurally calibrated
against exactly 35 governed source-family/wave pairs. That calibration is a
contract/authority/failure-behavior check, **not** 35 physical carrier runs.
The controlling law is:

```text
WAVE_SPECIFIC_AUTHORITY_AND_OUTPUTS != WAVE_SPECIFIC_GENERIC_CODE
```

This LiTS work must therefore be banked in two distinct layers:

### Reusable generic layer

Bank once, with cross-source hostile tests:

- runtime-authority injection through `Pre553RuntimeAuthoritySet`;
- exact repository/release resolution;
- retained fact-preimage closure;
- separation of coverage state from typed state;
- source-explicit terminal projection with unknown-source failure;
- cross-schema identity-domain discipline;
- one-decode/reused-incidence mechanics;
- candidate-neutral provenance and zero-candidate-process accounting.

These are generic mechanisms only. They must remain free of LiTS/WVS wave
literals and semantic defaults.

### Wave-specific bank

For every governed source-family/wave pair, separately bank:

- canonical source identity, format, rows/variables, and currentness;
- exact decoder configuration and observed native representation classes;
- source-universe and respondent/event topology;
- variable/qid and response/special-state authority;
- routing/applicability/risk-set authority;
- measure/weight authority;
- predicate/query/discovery grammar;
- C11 release, replay, and projection identities;
- optional accelerator applicability;
- frozen oracle/output identities and typed terminal-count domain;
- negative limits proving what the wave authority does not grant;
- source-free hostile regressions plus the governed source-backed receipt.

LiTS-I-specific numeric-token authority must never be copied to another wave.
WVS7-specific typed-terminal truth must never be projected onto LiTS or another
wave. The generic seam carries each wave's exact banked authority and fails
closed when that bank is absent.

Counting the 35-wave registry: this repair directly qualifies LiTS-I only.
That leaves 34 other governed pairs requiring their own wave-specific evidence.
If the separately conserved WVS7 work is counted as the second covered pair,
33 further pairs remain. Neither count is a claim that those remaining waves
have been physically executed or semantically closed.

### Required banking cadence

After every concrete defect closure:

1. add a hostile regression that would reproduce the defect;
2. record the exact source/authority/release/replay/blob identities;
3. record whether the change is generic mechanism or wave-specific authority;
4. run the relevant cross-source conservation test;
5. commit with a bounded message and push the repair branch;
6. verify the remote SHA by `git ls-remote`;
7. update this handoff or a successor handoff with the new terminal and next
   unresolved boundary.

Do not accumulate important repairs only in `/private/tmp`, an uncommitted
worktree, terminal scrollback, or one account's conversation context.

## Continuation law

- Inspect and repair the first concrete source-pass failure in place.
- Preserve the one-decoder path; the R5B extension must reuse the already-decoded incidence.
- Do not run Candidate A, B, or C.
- Do not run measured P2X.
- Do not advance the governed P2X execution branch until the production repair has passed the required source-free qualification and the LiTS common source pass.
- Preserve WVS7 noninterference and the frozen WVS typed-terminal-count domain `{"COVERAGE_LIMITED": 46}`.
- Fail closed on any remote-head, source, runtime, blob, release, replay, projection, or authority mismatch.
