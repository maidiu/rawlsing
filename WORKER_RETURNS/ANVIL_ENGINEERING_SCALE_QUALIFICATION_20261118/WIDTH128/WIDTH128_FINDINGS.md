# WIDTH128 — 128 RESPONDENTS × 600 QUESTION BINDINGS

**Status:** `WIDTH128_F4_COMPLETE_EXPECTED_MATCH`  
**Integrated executable:** `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`; accepted S2C writer. One new build, one fresh prepared f4-only query. No 16R/R2 alteration; no 10k rebuild.

## Actual geometry

| Field | Actual |
|---|---:|
| Respondents | 128 |
| Native question bindings | 600 |
| RespondentEvent | **68,960** |
| RoutingEligibilityFact | **76,800** |
| WeightMeasureFact | 128 |
| Added valid / MISSING / NOT_ASKED | 60,928 / 7,616 / 7,616 |
| Events/respondent mean | 538.75 |
| Retained estate | **55,187,741 B** |
| Manifest SHA-256 | `4d9604dc886ff9655ad25941fdcad2e412d18de4ab07c813524068c1dad09eea` |

The added 595 slots use the existing response-populated R2 width pattern; only the five accepted base roles are queried. This is one **width+respondent** observation, not a 16R repeat, matrix, or full 600-item query workload.

## Build / query resources

| Phase | Actual |
|---|---:|
| Build wall | 293.956 s |
| Build RSS peak sampled | 200,609,792 B |
| Build scratch peak sampled | 826,683,762 B |
| Query external wall | 45.226 s |
| Prepared index S | 22.847 s |
| f4 Q | 21.239 s |
| f4 O | 0.0048 s |
| Query RSS peak sampled | 158,609,408 B |
| Query scratch peak sampled | 248,680,671 B |
| Build / query exit | 0 / 0 |
| Abort | none |

H admission for this width query was **not separately timed**; this is an explicit limitation, not a fabricated value. Caps: build 600 s, query 600 s, process-tree RSS 6 GiB, scratch 4 GiB, free ≥8 GiB; 0.25 s process-group supervision. Combined semantic closure + width build + query external wall = **106.187 + 293.956 + 45.226 = 445.369 s**, under 900 s cumulative.

## F4 result

- Fact state `SUPPORTED`; raw numerator/denominator **39 / 39**.
- Risk members **128**; denominator members **39**.
- Cells exact: `0` count 39 `OBSERVED_POSITIVE`; `1` count 0 `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`.
- Controlled base-role expectation matches cells, risk set, denominator set, raw denominator and state; full `as_dict` is `f4.payload.json.gz`.
- Full ref/replay and payload hash are in `RESULT.json`.

No old unoptimized baseline, profiler, test-only adapter, F4 rerun on 10k, or 100 distinct queries. No naive linear scale claim; this is one 128R width point, not 100k/full-width acceptance.
