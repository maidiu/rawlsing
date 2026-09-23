# FIABC LiTS R5B successor repair continuation handoff

Date: 2026-09-23

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
8. the historical I04 packaging test still pinned pre-successor asset bytes
   and WVS identities, so it could not qualify the active LiTS authority overlay.

Items 1–8 are addressed and source-free tested on the branch. The packaging
boundary is explicit now: the historical W3 manifest and original materializer
remain byte-pinned, while a separate overlay binding pins the active LiTS
materializer and its adopted authorities. WVS7's successor package, oracle,
and `COVERAGE_LIMITED × 46` domain are tested against R1M. Commit
`152c4885...` reconstructs the exact adopted R5B successor without a second
source decode. Commit `e4faa552...` binds the D03 risk sets to exactly the base
and adopted successor releases. Commit `8ea52e74...` adds the exact, opt-in F02
event-representation successor authority. A third live source pass proved
that the authority activates, but exposed an over-strict nonmatch path. Commit
`c3733e31...` repairs that exact path. A fourth pass reached the expected
49/1 I05 envelope, but did not leave a final oracle receipt; a fifth full pass
must complete and persist the oracle document.

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
- Source-free code checkpoint: `13f2eaebb76b407e7509d156cc0745901792f9bd`
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
git merge-base --is-ancestor 13f2eaebb76b407e7509d156cc0745901792f9bd origin/agent/rabochii-premain-fiabc-lits-representation-authority-repair-r1
git show origin/agent/rabochii-premain-fiabc-lits-representation-authority-repair-r1:WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/20_LITS_R5B_SUCCESSOR_REPAIR_CONTINUATION_HANDOFF.md >/dev/null
test "$(git rev-parse origin/agent/rabochii-premain-fiabc-terminal-readiness-r1)" = a8d4faac8912e9c03840d3f72a4f2ca8c83d6903
test "$(git rev-parse origin/agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1)" = 78caf7eb4396dd576cf478c860372b7e26455cd9
```

### Pickup from another machine or account

The repair code, partial I05 evidence, continuation pointer, and this
instruction set are banked on the repair branch. The LiTS source and the pinned
runtime are not in Git and do not transfer with the branch. The other machine
must have authorized access to this repository, an independently supplied
copy of the exact LiTS source, and the required runtime. Do not upload the
source file to this repository.

After cloning or entering the intended checkout, fetch the three named refs
and apply the remote-head and ancestry checks above. Continue on the repair
branch only; do not switch to or advance the governed execution branch. Confirm
that the source supplied on the new machine is the same canonical source by
letting the producer's enforced source-identity check validate it. Its expected
SHA-256 is `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
the host-local pathname below is only an example and may differ. The producer
must run under CPython 3.11.3 on the qualified Darwin x86_64 host with
`pyreadstat==1.3.6` and `pyarrow==25.0.1`. The prior venv pathname is ephemeral;
recreate or obtain that exact approved environment and pass
`verify_runtime_gate` before source access. Do not substitute current system
Python or relax the gate.

The partial fourth-pass precheck is portable and its exact bytes are stored as
`22_LITS_R5B_SUCCESSOR_I05_PRECHECK_PARTIAL.json`. The fourth pass's `/private/tmp`
work roots and missing final producer terminal are not portable evidence. A
new machine must run the fifth fresh pass below and preserve its final oracle,
stdout receipt, checksums, and exit status.

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
6. `c3733e311c467a6130ba69cc49144b2afb9d6bc4` — exact same-question
   nonmatch semantics. A requested leaf matches its one declared witness,
   another declared witness in the same six-binding question domain is a
   legitimate false result, and an undeclared or malformed witness still fails
   closed.
7. `a50a708f81aaefbdf6e4500bb92d11e783e0a4d5` — explicit live LiTS runtime
   authority overlay binding, while preserving the immutable original I04
   packaging manifest and its historical materializer bytes.
8. `13f2eaebb76b407e7509d156cc0745901792f9bd` — source-free qualification
   rebind to the exact successor code/assets and the R1M WVS typed-terminal
   count domain.

The focused source-free court at `c3733e31...` is green:

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

The canonical qualification pytest body, extended with the LiTS authority and
runtime-overlay tests, is green:

```text
214 passed, 28 subtests passed in 28.50s
RAWLSING_RECONCILED_FIABC_STATIC_CROSS_LANE_ASSERTIONS_PASS
RAWLSING_CANONICAL_REINTEGRATION_SOURCE_FREE_QUALIFICATION_GREEN__READY_FOR_PRE_CANDIDATE_FREEZE
```

The W3 packaging test checks the original materializer at its source commit,
the separate active LiTS overlay blob, and the current WVS successor package
and projection identities. `RUNTIME_PACKAGING_BINDING.json` itself remains
unchanged.

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
`192926...`; it adds no generic int/float/Decimal equivalence.

A third fresh common LiTS source pass from `8ea52e74...` completed after about
30 minutes with no A/B/C candidate process. It emitted:

```text
candidate_count = 50
query_role_count = 77
candidate_processes_started = 0
coverage_state_counts = {"EVALUATED_SUPPORTED": 31, "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY": 19}
fact_state_counts = {"SUPPORTED": 36, "UNAVAILABLE": 24}
fact failure = MISSING_REQUIRED_AUTHORITY: runtime event witness differs from exact adopted representation
```

The authority was active, but the first implementation treated a legitimate
same-question event for a different declared value as malformed. For example,
while evaluating q310 = 1, an exact q310 value-2 witness must be a false match,
not an authority failure. Commit `c3733e31...` now returns false for another
declared witness in the same exact question domain while continuing to raise
for undeclared/malformed witnesses. The focused 71-test court is green.

The fourth fresh common LiTS source pass from `629343c6...` reached the
expected I05 precheck after about 30 minutes. Its exact source-derived
precheck is preserved as
`22_LITS_R5B_SUCCESSOR_I05_PRECHECK_PARTIAL.json` with SHA-256
`1ffbcb0f02e0c6b89a09cb255ce9342cbcb162ab2a1302de0ca8ade24990eed6`. It
records:

```text
candidate_count = 50
query_role_count = 77
candidate_processes_started = 0
coverage_state_counts = {"EVALUATED_SUPPORTED": 49, "EVALUATED_VALID_EMPTY": 1}
typed_state_counts = {"DISCOVERED_RESULT_SUPPORTED": 49, "VALID_EMPTY": 1}
empirical_fact_state_counts = {"SUPPORTED": 60}
```

All 18 P2 higher-order candidates are now supported; the single P3
conditional-reversal candidate is valid-empty. The final output
`lits_oracle_freeze.json` is absent, however, and the producer's final process
status and traceback were not persisted when its session ended. This proves the
I05 envelope only; it does not prove final oracle construction, identity, or
serialization. The complete source-backed court is **not yet green**.

The full source-free qualification is green at `13f2eaeb...`, including the
runtime overlay and WVS conservation binding. Run a fifth fresh source pass
from that qualified code checkpoint, require the producer PASS receipt and
final oracle document, verify the receipt's oracle identity and document SHA,
and capture the actual process exit status. Then stop before promotion or
candidate work. The pre-candidate script currently requires the governed
execution branch by name and regenerates a LiTS oracle from source; do not run
it on this repair branch or advance the locked execution branch to satisfy it.
After the LiTS pass is green, a governing promotion authority must explicitly
authorize the next transition or provide a separately authorized pre-candidate
route against the qualified repair code.

Prior source-pass evidence roots on this host:

```text
/private/tmp/fiabc-lits-successor-source.JN5rJj
/private/tmp/fiabc-lits-d03-successor-rerun.oN1nb1
/private/tmp/fiabc-lits-f02-successor-rerun.f45wvz
/private/tmp/fiabc-lits-f02-nonmatch-rerun.vTuCsn
```

That path is not portable. On this or another machine, rerun exactly:

```bash
set -euo pipefail
repo="$PWD"
: "${LITS_SOURCE:?set this to the exact supplied LiTS-I source file}"
: "${FIABC_PYTHON:?set this to the qualified CPython 3.11.3 executable}"
litssource="$LITS_SOURCE"
pythonbin="$FIABC_PYTHON"
diagroot="$(mktemp -d /private/tmp/fiabc-lits-f05-qualified.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$repo" \
  "$pythonbin" -u \
  -m rawlsing_next.fiabc_final_oracle_freeze_producers produce-lits \
  --repo-root "$repo" \
  --source "$litssource" \
  --work-root "$diagroot/work" \
  --output "$diagroot/lits_oracle_freeze.json" \
  | tee "$diagroot/producer_receipt.json"
test -s "$diagroot/lits_oracle_freeze.json"
test -s "$diagroot/producer_receipt.json"
shasum -a 256 "$diagroot/lits_oracle_freeze.json" "$diagroot/producer_receipt.json"
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
- Third successor-backed source pass proved the bridge activates and exposed
  the over-strict handling of another authorized same-question witness.
- Exact nonmatch semantics repaired: target witness true, another authorized
  same-question witness false, undeclared/malformed witness fail closed.
- The source-free I04 overlay binding preserves the original packaging manifest
  and exact historical materializer while pinning the current LiTS authority
  modules and current WVS7 package/projection identities.
- Full canonical source-free qualification green at `13f2eaeb...`: 214 passed,
  28 subtests, WVS oracle conservation and static cross-lane assertions pass.
- Fourth source-backed I05 precheck records the accepted LiTS 49/1 coverage,
  60 supported facts, and zero candidate processes; its exact partial JSON is
  banked, but the final oracle receipt/document is absent.
- No A/B/C process and no measured P2X run by this repair.
- Governed execution branch preserved at `78caf7eb...`.

## Ground left to go

Proceed in this order and stop at the first failure:

1. Run the fifth fresh common LiTS source pass from the source-free qualified
   checkpoint `13f2eaeb...`; tee the final PASS receipt, require the oracle
   file, verify both checksums, and bank both exact outputs.
2. If it fails, make the narrowest authority-preserving repair, add a hostile
   source-free regression, rerun the focused court, commit, and push.
3. Repeat until the source pass emits the accepted 49/1 LiTS envelope and a
   verified frozen oracle with zero candidate processes.
4. Independently recheck WVS7 frozen truth and static noninterference after the
   final LiTS source pass.
5. Stop at the repair-branch boundary. The existing governed pre-candidate
   script pins the execution branch name and launches its own LiTS source
   producer; do not use it from this repair branch or treat it as approval to
   advance the protected branch.
6. Prepare an exact promotion/transition receipt naming the qualified repair
   SHA. Advance the execution branch or resume A/B/C/P2X only after explicit
   governing promotion authority permits that transition.

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
