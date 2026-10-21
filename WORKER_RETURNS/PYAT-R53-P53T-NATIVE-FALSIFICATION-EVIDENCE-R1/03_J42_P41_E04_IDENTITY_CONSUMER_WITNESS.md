# J42 / P41 / E04 — CONDITIONED IDENTITY AND PROMOTION WITNESS

**Sources (unchanged):**

- J42 `runtime/j42_join.py` commit `f53cb0d2bce52640268c844c398bbd8007d28edc`, blob `40f1e9f69fafff37f6bc44474b0189543d4997b3`.
- P41 `vendor/p41/runtime/p41_service.py`, same commit, blob `7d428106c79bcc56973f7c0044fc273a2b354554`.
- E04 `vendor/p41/runtime/vendor/product/nonparent.py`, blob `2181b832d3c4376d4b9428e13f4354f273be8f32`.
- Fresh E41 driver `runtime/e41_driver.py`, blob `3b739d79e54d904af76b1c34482e215bad9eeb77`.
- P41 fixture/prepare, P41 vendor modules, and startup `rawlsing_next` dependencies are imported from the same packet/worktree; no source edits.

## Actual execution surface

`tests/test_j42_p41_e04.py` runs six tests. The session fixture executes the unchanged E41 driver in a fresh subprocess with `PYTHONHASHSEED=0`; it writes `receipts/e41_fresh_run.json`. The J42/P41 tests then use that exact fresh result. P41 `prepare()` creates a real sourcefree synthetic E04 selected world and lifecycle; `J42P41Service` is constructed normally with that prepared object. E04 `consume` is the unchanged nonparent consumer.

Command:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest WORKER_RETURNS/PYAT-R53-P53T-NATIVE-FALSIFICATION-EVIDENCE-R1/tests \
  -q -rA --junitxml=receipts/pytest_all.xml
```

Result: 23 passed, 0 failed, 0 errors, 0 skipped. The J42 file alone: 6 passed.

## Positive control — fresh E41 is real and exact

`receipts/e41_fresh_run.json`:

| Slice | Denominator | Cells | Route |
|---|---:|---|---|
| `Y/1` | 32 | `{0:14, 1:18}` | `DIRECT_VIA_ACCEPTED_PROVIDER_FUNCTION` |
| `Y/2` | 16 | `{0:6, 1:10}` | `DIRECT_MULTI_CONDITIONER_VIA_ACCEPTED_COMPOSITION` |
| `Y/3` | 8 | `{0:2, 1:6}` | `DIRECT_MULTI_CONDITIONER_VIA_ACCEPTED_COMPOSITION` |
| `A/1` | 29 | `{0:11, 1:18}` | `DIRECT_VIA_ACCEPTED_PROVIDER_FUNCTION` |

The normal request `Y|(A=1)` returns `conditioners=[["A",1]]`, denominator 32, and the A evidence ref. This proves the witness is not a blanket consumer failure.

## D11 — requested C reads A evidence

Input: fresh E41 source has `Y|(A=1)` at depth 1. Request is `Y|(C=1)`.

Observed through unchanged `E41ProviderAdapter.step()` (`j42_join.py:182-221`):

- `_validate` accepts target Y without checking conditions (`j42_join.py:171-176`).
- Source selection uses only `self.e41["steps"][f"{target}/{len(ordered)}"]` (`j42_join.py:188`), so depth 1 selects `Y/1`.
- Returned `conditioners` are `[["A",1]]`; returned `evidence_ref` is the A evidence; denominator is 32.
- The adapter cache key includes the requested conditions, but the cached value still carries A identity, so repeated C requests remain wrong.

Request `Y|(A=0)` at the same depth returns the same A=1 cells and evidence. Both `C=1` and `A=0` are wrong-condition requests; neither is refused.

`JoinedService.possibilities()` returns the same A-conditioned step for a C-conditioned call because it selects only by target and depth (`j42_join.py:97-132`).

Observed through unchanged `P41Service.progressive()` / `J42P41Service`:

- `receipt["query"]["ordered_conditions"] == [["C",1]]`.
- `receipt["query"]["query_identity_hash"] == semantic_hash(["Y", (("C",1),)])`, so the query identity names C.
- `receipt["n10e_steps"][0]["conditioners"] == [["A",1]]`.
- `receipt["n10e_steps"][0]["evidence_ref"]` is the A evidence.
- `receipt["n10e_steps"][0]["denominator"] == 32`.
- `receipt["structural"]["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"`.

The P41 receipt therefore joins a requested-C query identity to A empirical evidence. The fault is a provider-adapter identity omission plus P41's trust in provider-returned step identities. The normal A request is correct.

## D12 — unsupported step promoted by J42 and accepted by E04

Fixture mutation: `Y/2.fact_state = "ZERO_SUPPORT"`, `Y/2.consumer_state = None`, other steps supported.

Observed:

- `JoinedService.possibilities().state == "PRODUCTIVE_TEST_ONLY"` (`j42_join.py:127-132`).
- Steps: `EXACT_SUPPORTED`, `ZERO_SUPPORT`, `EXACT_SUPPORTED`.
- E04 `consume()` emits `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED` (`nonparent.py:24`).
- `source_balance_reads[1].support_state == "ZERO_SUPPORT"` is preserved inside the receipt, but the top-level named output is success.

All-supported control also emits `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED` with no negative step. The defect is not that the consumer cannot represent a negative step; it is that the negative step does not change the top-level acceptance state.

## D13 — P41 contradiction for non-zero unsupported state

Fixture mutation: `Y/1.fact_state = "ROUTING_UNKNOWN"`, `Y/1.consumer_state = None`.

Observed through `P41Service.progressive()` (`p41_service.py:163-186`):

- `n10e_steps[0].state == "ROUTING_UNKNOWN"`.
- `n10w.progressive_chain_state == "TYPED_PARTIAL_OR_UNKNOWN"`.
- `unknown.zero_support_steps == []`.
- `unknown.evidence_state == "EXACT_SUPPORT_ON_CONDITIONED_RISK_SET"`.

Positive control with `ZERO_SUPPORT` yields `unknown.evidence_state == "NO_SUPPORTED_EVIDENCE"`. The contradiction is specific to non-zero unsupported states. A consumer reading only `unknown.evidence_state` receives an exact-support label alongside a typed partial chain.

## D14 — absent structural state defaults to supported

Input: structural `training_access` has a value and field ref but no `state`.

Observed:

- `JoinedService.structural()` applies `value.setdefault("state", "SUPPORTED_TEST_ONLY")` (`j42_join.py:87-95`).
- E04 training route is `ELIGIBLE`.
- E04 top-level state is `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED`.

Positive control with explicit `state="UNAVAILABLE_AUTHORITY_OR_CLOCK"` yields route `UNAVAILABLE_AUTHORITY_OR_CLOCK` and top-level `PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT`. The failure is absence-to-supported, not the handling of explicit unavailable.

## E04 original/unchanged assertion

The E04 consume used here is the exact byte-identical J42 candidate copy at blob `2181b832d3c4376d4b9428e13f4354f273be8f32`. It consumes a J42 `JoinedService` built from the fresh E41 result and a sourcefree synthetic structural view. It does **not** consume original35 microdata, original W41, or a source-licensed E04 release.

`E04_NOT_RUN` for: original35 source-backed N11 consumer, original W41 84-view join, and production acceptance.

## Consequences and limits

- Downstream effect is a request/evidence identity mismatch and false top-level success inside the sourcefree J42/P41/E04 candidate path.
- The normal A/B/C supported path remains coherent; no claim is made that all J42 behavior is wrong.
- No repair is proposed or implemented.
- No original source, scientific meaning, FF/F6/F7, rights, N11/N12, actor, or production status is issued.
