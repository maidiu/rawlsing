# PYAT N10E — EMPIRICAL POSSIBILITY-SLICE PROVIDER CORE — R1

Status: ISSUED__DEEPSEEK_HARNESS_PARALLEL_SOURCE_FREE_LANE

**LAUNCH IN: DeepSeek Harness — DeepSeek V4.1 Flash — Standard mode**

Role: long-running source-free implementation owner for the early-developable N10E provider core.

Repository:
`maidiu/rawlsing`

Branch:
`agent/deepseek-pyat-hq140-n10e-empirical-slice-provider-r1`

Exact branch base:
`5fafb499d53dddadaf8a7b4fd46506e91a09d270`

That base is the accepted C1-01 source-free integration line.

## Why this lane is parallel-safe

This job is intentionally independent of the active C1-02 correction work.

Do not edit:

`rawlsing_next/pre553_analytical_composition.py`

Do not edit C1-02 tests, C1-02 fixtures, or the C1-02 return directory.

The provider must consume the already-accepted C1-01 public analytical seam from the exact branch base. Later C1-02 integration may extend that producer, but this lane must not depend on unfinished AT08-AT13 work.

Astra authority:

`PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/nodes/N10E.md`

C8 draft context:

`PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/commissions/C8.md`

Acceptance cases used at this declared grain:

- `AT07`
- `AT17`

AT33 progressive multi-conditioner/world-conditioned proof is explicitly **not** claimed by this R1 core and remains downstream of competent higher-order/world inputs.

## Exact objective

Create a public source-free empirical possibility-slice provider that:

1. accepts exact empirical producer inputs and governed possibility-consumer inputs;
2. obtains the slice from the accepted current analytical producer path;
3. never accepts a caller-supplied handwritten `PossibilitySliceEvidence` as substitute for empirical production;
4. preserves exact source universe, release, target, conditioners, denominator/risk support, measure, provenance, authority and replay dependencies;
5. feeds the existing public positioned-subject possibility consumer;
6. exposes an auditable provider receipt showing the producer input, generated evidence identity, consumer identity and result identity;
7. fails closed on mismatched source/release/target/dependency context;
8. introduces no smoothing, independent-trait draw, stereotype default or actor/person state.

This is a service/provider seam over competent C1-01 production.
It must not duplicate empirical calculation by manually constructing probabilities.

## Current owners to reuse unchanged

Accepted analytical producer:

`rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility`

Accepted possibility consumer:

`rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility`

Current possibility owner blob at base:

`62e5eced47b64512f47b004e3e13a6ef3fe21de7`

Accepted C1 analytical owner at base:

`26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`

Do not modify either owner in this job.

If the provider cannot be built without changing one of those existing owners, stop with:
`EXISTING_OWNER_CHANGE_REQUIRED`
and preserve an exact reproducer.

## Recommended implementation terrain

Create:

`rawlsing_next/pre553_empirical_possibility_provider.py`

Use a narrow typed public contract. Exact names may vary if justified, but the implementation must clearly separate:

- provider request;
- generated analytical composition;
- generated evidence;
- consumer result;
- provider receipt/replay identity.

A provider request must carry or bind every determinant required by the accepted C1-01 producer/consumer path.

The provider must not accept precomputed probability geometry as authoritative input.

The provider may return the underlying accepted `AnalyticalCompositionResult`, generated `PossibilitySliceEvidence`, and `PositionedSubjectPossibilityResult` alongside a provider receipt if that is the cleanest nonduplicative design.

## Acceptance court

Create:

`rawlsing_next/tests/test_pre553_empirical_possibility_provider.py`

Freeze independent source-free fixture/oracle material before using candidate output as expected truth.

### P1 — actual computed forward slice

Use the accepted AT07 synthetic source law or an exactly equivalent independently frozen fixture.

Prove actual public path:

`empirical query → accepted C1 analytical composition → generated slice evidence → public possibility consumer → provider receipt`

For the canonical forward grain, verify the exact 54/60 = 9/10 distribution and exact denominator/member support.

The provider test must prove the geometry came from the empirical producer/composition result rather than a handwritten evidence object.

### P2 — actual computed reverse slice

Prove the accepted reverse 54/62 = 27/31 direction through the same public provider.

Preserve target topology, risk support and exact fraction semantics.

### P3 — identity/dependency closure

Changing an identity-bearing producer determinant must reidentify the appropriate provider receipt/result.

At minimum test one legitimate source-free determinant mutation.

Unconsumed irrelevant material must not silently become a determinant.

### P4 — no handwritten slice substitution

The provider public API must not permit a caller to satisfy the provider by supplying an arbitrary `PossibilitySliceEvidence`.

If a low-level helper necessarily accepts evidence internally, prove the public provider cannot bypass the empirical producer path.

### P5 — fail-closed context mismatch

At minimum independently exercise:

- source-universe mismatch;
- release mismatch;
- consumer target mismatch or equivalent exact dependency mismatch.

The provider must fail closed or return the existing typed refusal state according to owner law. It may not coerce or bridge implicitly.

### P6 — no unauthorized smoothing / proxy laundering

Exact supported evidence should remain exact supported.

An unresolved/missing exact slice must not be replaced by invented probability geometry.

Any existing governed proxy/walkback behavior remains owned by the current possibility model rule and must be explicit. The provider creates no new proxy authority.

### P7 — replay

Provider receipt/result identity must be deterministically reproducible from the same exact frozen inputs in a fresh invocation.

If a fresh-process replay is cheap and natural, include it. If not, deterministic same-process replay plus exact dependency closure is sufficient at this R1 core grain; document the proof grade honestly.

## Original C1-01 regression

Run the accepted C1-01 analytical court unchanged.

At minimum the final court must include:

`rawlsing_next/tests/test_pre553_analytical_composition.py`

`rawlsing_next/tests/test_pre553_empirical_query.py`

`rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

plus the new provider test.

Do not import or depend on the unfinished C1-02 higher-order test file.

## Write allowlist

You may create/edit only:

1. `rawlsing_next/pre553_empirical_possibility_provider.py`
2. `rawlsing_next/tests/test_pre553_empirical_possibility_provider.py`
3. optional `rawlsing_next/tests/n10e_empirical_slice_fixture.py`
4. optional `rawlsing_next/tests/n10e_empirical_slice_fresh_process_runner.py`
5. `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/**`

Do not edit any existing production owner.
Do not edit any existing test file.
Do not edit C1 generic packets.
Do not edit C1-02 terrain.
Do not edit HQ/control files.

## Execution/economy law

Use the local DeepSeek Harness terminal/runtime.

Start with the smallest meaningful provider test before broad execution.

Do not spend time on broad archaeology once the exact current owners above are verified.

Do not repeatedly run the full court after every small edit. Use targeted tests during development, then run the complete required court once the patch is coherent.

Preserve materially informative failure output, but do not create documentary ceremony for every mechanical iteration.

## Required return

Under:

`WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/**`

create:

- `00_RETURN.md`
- `01_SCOPE_AND_GROUNDING.json`
- `02_PROVIDER_CONTRACT.json`
- `03_FIXTURE_AND_ORACLE_FREEZE.json`
- `04_PRODUCER_CONSUMER_TRACE.json`
- `05_HOSTILE_AND_REPLAY_AUDIT.json`
- `06_EXECUTION_RECEIPT.json`
- `07_FINAL_DISPOSITION.json`
- final pytest output text.

Every proof claim must distinguish:
- static inspection;
- source-free executed producer;
- generated evidence;
- consumer execution;
- deterministic replay.

Do not cite nonexistent tests or upgrade documentary fixture definitions into executed proof.

## Allowed dispositions

- `PASS_SOURCE_FREE_PATCH_READY__INDEPENDENT_REVIEW_REQUIRED`
- `FAIL_SOURCE_FREE_QUALIFICATION__PATCH_RETURNED_FOR_HQ`
- `EXISTING_OWNER_CHANGE_REQUIRED`
- `AUTHORITY_GAP`
- `COUNTEREXAMPLE_TO_N10E_CORE_CONTRACT`

A branch-local PASS is not adoption.

## Absolute prohibitions

No raw survey files.
No Candidate A/B/C.
No measured P2X.
No real-source C11 execution.
No C4 execution.
No C1-02 or C1-03 implementation.
No structural-world claim.
No actor/person/V3 implementation.
No AT33 full progressive-world completion claim.

## Git completion

When finished:

1. verify diff from `5fafb499d53dddadaf8a7b4fd46506e91a09d270` is entirely inside the write allowlist;
2. commit all completed work;
3. push exactly this assigned branch to origin;
4. report:
   - final commit SHA;
   - disposition;
   - terminal token;
   - changed files;
   - final test counts;
   - concise blocker if not PASS.

Do not merge.

Terminal:

`N10E_EMPIRICAL_SLICE_PROVIDER_RETURNED__HQ_ADJUDICATION_REQUIRED`
