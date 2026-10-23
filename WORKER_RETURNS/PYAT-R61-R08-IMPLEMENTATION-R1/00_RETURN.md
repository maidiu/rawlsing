# R61-R08 evidence binding — implementation return

**Verdict: REVISE (bounded).** The assigned callable boundary is implemented and
natively tested. Full J42/P41 progressive end-to-end adoption is **not** claimed:
those historical owner bodies are outside this write allowlist and still contain
the read-only trace/fallback defect. The exact external amendment is listed below.

## Startup and scope

- Sealed startup HEAD verified before work:
  `c84842e20e1d00d0b036977c9f5006aad5328ae9`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- Candidate commit: `f93cf87948ce092a9b8623b60c00722ae048bda2`
- Remote branch readback after first push matched that commit.
- Write allowlist only:
  - `rawlsing_next/pre553_universal_evidence_binding.py`
  - `rawlsing_next/tests/test_universal_evidence_binding.py`
  - own `WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/`
- No original survey read, credentials, external home directory, unrelated
  branch, provider change, subagent, actor/N11/N12, CI deployment or HQ edit.

## Plain-English function delivered

`pre553_universal_evidence_binding.py` turns one exact typed `EvidenceRequest`
identity K into one of:

1. an **actual canonical provider execution** through the existing accepted
   `provide_empirical_possibility_slice` -> C1 analytical composition path;
2. an **authenticated cache replay** whose sealed preimage binds the full K,
   producer receipt, evidence object, consumer query/model and consumer values;
3. a **typed refusal** (`UNKNOWN`, `ZERO_SUPPORT`, `UNSUPPORTED`, identity
   mismatch) with no exact evidence and no consumer values.

K binds schema/grade, source/dataset/wave/edition/byte digest, instrument,
item-option-form-repeat occurrence, units/links, risk/predicate, ordered targets,
ordered typed condition values plus domain/state version, operation/arity,
estimand/weights/design/uncertainty, direction/role/consumer use, grammar/model,
release/custody and observation/reference/as-of/publication clocks. Tagged
scalars keep `1`, `"1"`, `true` and null disjoint; floats are rejected.

`EvidenceResult` keeps **eligibility**, **execution** and **result** as separate
axes. `SupportSummary`/`reduce_required_support` preserves valid zero/null/empty
products separately from `ZERO_SUPPORT`, unsupported and unknown states, rejects
duplicate request keys, and retains unresolved denominator support.

`EvidenceConsumerReader` calls the unchanged
`evaluate_positioned_subject_possibility` with the actual producer-derived
evidence object, rechecks its result hash, and emits values-read plus an
E04-compatible step. It refuses when K, target, conditions/typed values,
direction or role do not match. There is no trace-only evaluator claim and no
target/depth fallback.

## Actual execution proof

Positive witness uses the real accepted AT07 source-free fixture and actual
provider call. Frozen independent arithmetic: forward 54/60 = 9/10
(`yes=54`, `no=6`), denominator 60. The result is `SUPPORTED`, eligibility
`ELIGIBLE`, execution `COMPLETED`, consumer state `EXACT_SUPPORTED`.

ZERO_SUPPORT witness uses the same actual provider with condition `POSITION=P3`
on the frozen AT07 law. Composition returns `ZERO_SUPPORT`, denominator 0, no
evidence object, and the consumer reader refuses. No positive/all-support
summary is produced.

Cold replay was exercised in a fresh Python process: cache exported from the
producer run, imported with no producer binding, resolved as
`AUTHENTICATED_CACHE`, and its consumer values-read reproduced denominator 60
and the same consumer result hash.

## Acceptance matrix (R08)

| Required behavior | Evidence | Outcome |
|---|---|---|
| Positive actual permitted provider call | `test_positive_actual_producer_consumer_values_read` | PASS |
| Actual consumer values-read, not trace | same test, `EvidenceConsumerReader.read` re-invokes evaluator and compares hash | PASS |
| `C=1/A=0` cannot reuse `A=1` / changed condition or typed value | `test_changed_typed_values_and_identity_axes_refuse_same_consumer`, `test_typed_encoding...` | PASS |
| Wrong source edition/digest, risk, direction/role, design, as-of clock, target | same test; each new K resolves `UNKNOWN` and reader refuses | PASS |
| ZERO_SUPPORT / missing structural state cannot become exact positive | `test_actual_zero_support...`, `test_missing_state_controls...` | PASS |
| Positive remains positive | positive test | PASS |
| Valid null / valid empty / observed-zero distinction | `test_missing_state_controls...`; zero/observed-zero mapping in module | PASS |
| Z `UNRESOLVED` denominator 16 retained, not exact support | `test_missing_state_controls...` | PASS |
| Cache invalidation/currentness and tamper refusal | `test_cache_cold_replay_and_authenticated_tamper` | PASS |
| Fresh-process cold restore of same assertion | `test_cold_process_cache_replay_preserves_same_consumer_values` | PASS |
| Targeted assertion mutation and restoration | `test_consumer_assertion_mutation_and_restoration`; mutations listed in proof witness | PASS |

## Exact tests and tooling

Command (exit 0):

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/junit.xml
```

- Python 3.11.3 (`/usr/local/bin/python3`), pytest 9.0.2, pyreadstat 1.3.2
  verified installed (not used by these source-free tests).
- Result: **21 passed, 0 failed, 0 errors, 0 skipped, 4.976 s** in the frozen
  JUnit receipt (8 new R08 tests + 13 unchanged C1 composition regressions).
- JUnit: `WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/junit.xml`.

## Exact changed paths and blob refs

| Path | Git blob |
|---|---|
| `rawlsing_next/pre553_universal_evidence_binding.py` | `464a2190a811816c52e9d9c244ab126dc950c564` |
| `rawlsing_next/tests/test_universal_evidence_binding.py` | `2512c29e7fa1b780e24a82d111e7c336fae506de` |

Key imported/native owners used unchanged:

| Module | Blob |
|---|---|
| `pre553_empirical_possibility_provider.py` | `23167aa25291fb148b1e3cf210ac33fe7769b783` |
| `pre553_analytical_composition.py` | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` |
| `source_backed_positioned_subject_possibility.py` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` |
| `pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` |
| `tests/n10e_empirical_slice_fixture.py` | `0e384f72fa615dc72a0dcb08a36472a64b7b1e4a` |

## Historical defect read, not edited

`WORKER_RETURNS/PYAT-R42-J42-.../runtime/j42_join.py::E41ProviderAdapter.step`
appends a trace entry named `evaluate_positioned_subject_possibility` and copies
the producer's consumer state/hash without calling the evaluator.
`WORKER_RETURNS/PYAT-R41-P41-.../runtime/p41_service.py::P41Service.progressive`
then consumes trace entries by index and falls back to
`CACHED_PRODUCTION_CONSUMPTION` with `same_evidence_object=True` when the trace
is absent. Separately, the historical E04 `product/nonparent.py::consume`
retains top-level success unless the empirical channel is nonproductive.

These files are outside the R08 allowlist and were not modified.

### Exact external owner amendment needed for end-to-end P41

1. `j42_join.py::E41ProviderAdapter.step`: accept an exact `EvidenceRequest`
   (or resolver + request), call `EvidenceResolver.resolve`, and return/record
   `EvidenceConsumerReader.read` output. Remove the synthetic evaluator trace.
2. `p41_service.py::P41Service.progressive`: replace trace-index association
   and `CACHED_PRODUCTION_CONSUMPTION` with the per-step exact request key,
   producer/cache provenance and actual consumer result hash returned from the
   boundary above. A cache fallback must carry an authenticated sealed entry.
3. Keep `product/nonparent.py::consume` unchanged; feed it only the resulting
   E04-compatible step material. A separately owned E04 consumer court must then
   prove ZERO_SUPPORT/UNKNOWN/absent state fails the same success assertion.

Until that amendment, this return does **not** claim full J42/P41 end-to-end
PASS. The callable boundary and its native proof are banked for independent
review.

## Limits and honest provenance

- `AUTHENTICATED_CACHE` means canonical SHA-256 seal over full K, producer
  receipt and consumer/evidence preimages. It is not secret-key issuer
  authentication and issues no permission or science grade.
- All fixtures are TEST_ONLY source-free. No original U/Epre, N11/N12, F6/F7/F8,
  production or CI status is changed.
- Author validation only. Independent reviewer branch
  `agent/opencode-pyat-r61-r08v-independent-review-r1` was not launched or
  self-adopted.
