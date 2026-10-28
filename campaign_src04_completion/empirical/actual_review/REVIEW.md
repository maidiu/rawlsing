# SRC04 actual issuer/carrier independent review — REVISE

## Scope and custody

- Existing distinct C/D reviewer; not a C/D author.
- Branch: `agent/pyat-src04-actual-carrier-review-20261028`
- Sealed review HEAD: `91e267f11c91a89023c836a8667a99dca1a17019`
- Candidate: `d48ddf93f6642b80e8d9f0399dbc0abd5ec66742`
- Implementation: `f704441a6594730de82da4596efd64df87a2a73d`
- Accepted D dependency: `39c713a1396c7184afec5cb81519b151357c4a8e`; current `consumers/consumer.py` hash `728fbc9a09291ae9c9d578fbed7641acd4499a2ff4158b7588e1cc5afa18f8ae` (exact match).
- Prior C boundary `44aaf2be06e026547e9b32d880ac588e84acc9e4`, prior focused review `9b66083f89a6881f296be7fd1a8ff04c9718951b`, and historical RED evidence (`test_cd_boundary_review.py` `4385981d...`, `REVIEW.json` `331b43ca...`, `TEST_RUN.txt` `f294e01c...`) remain read-only and unchanged.

Only `campaign_src04_completion/empirical/actual_review/**` was written. No author/native/consumer code or original source product was modified or opened.

## Verdict

**REVISE** — the changed actual-carrier/issuer path cannot execute the required labelled nonrespondent fixture through issuer, executor, and accepted D consumer. The actual carrier adapter itself rehydrates the fixture correctly, but the issuer rejects it at the original-source/7,337-row gates; a subsequent source-literal topology validation also finds no fixture-qualified targets. Separately, malformed/truncated carrier streams and missing pinned receipt files escape as raw Python exceptions instead of typed `ActualCarrierRefusal` records.

No original SRC04 source was read; no original product or workload was run. The fixture evidence is engineering evidence only.

## Exact defect 1 — fixture issuer/executor/D path absent

Owner: `campaign_src04_completion/empirical/authorized_execution.py`

Measured path:

1. Build labelled SRC04 nonrespondent fixture release: `9026fa33...d47f42`, source stream `506d9217...e5d51b`, 8 respondents.
2. Write actual-carrier receipt and native pickle streams; adapter rehydrates successfully.
3. Authenticate the exact human grant: `757ee9e0...0130f`.
4. Call `issue_authorized_execution(...)` with the fixture release and fixture contract.
5. **Refused before executor** with `AuthorizedExecutionRefusal: RELEASE_SOURCE_IDENTITY_MISMATCH` at the hardcoded original-source gate (`authorized_execution.py:362`).
6. Even if that gate were bypassed, `EXPECTED_ROWS = 7337` (`authorized_execution.py:370`) rejects the 8-row fixture.
7. `_topology_valid_targets` on the fixture contract also returns `NO_SOURCE_QUALIFIED_TARGETS` (`authorized_execution.py:293-294`); the fixture therefore supplies no source-literal target for executor/D.

Consequence: the required fixture → **new adapter** → **authenticated issuer** → **executor** → **accepted D consumer** path has no positive execution. The author suite tests the adapter and original issuer separately; it does not close this boundary. The D bridge is also hardcoded to `SOURCE_LOCAL_CERTIFIED` / `SOURCE_LOCAL_STATISTIC` with `fixture_only=False` (`consumer_bridge.py`), so a fixture-only bridge mode is absent.

Smallest repair, without weakening the original route:

- Add an explicit, separately named nonrespondent-fixture issuance path (or an explicit opt-in fixture mode defaulting off) that requires an authenticated fixture-scoped grant/contract, exact fixture source/row/stream pins, and constructs `NONRESPONDENT_FIXTURE_ONLY` source-literal/topology/target-use authorities and a fixture-only authorized contract.
- Keep `issue_authorized_execution`'s original source/7,337-row gate unchanged for source-local science.
- Add a fixture-only consumer-bridge mode (`fixture_only=True`, `SUPPORTED_COMPONENT_ONLY`) or a distinct fixture bridge; do not relabel fixture results as source-local.
- Add one end-to-end fixture test through adapter, issuer, executor, and accepted D consumer.

The fixture source-literal topology must be validated from actual event kinds/topology refs, not caller assertion; the current fixture contract has no target that passes that validation.

## Exact defect 2 — carrier refusal typing missing

Owner: `campaign_src04_completion/empirical/actual_carrier.py`

Measured with receipt pins updated to match the malformed/truncated streams (so SHA/count checks do not mask the failure):

| Case | Actual result | Required result |
|---|---|---|
| Malformed public pickle | `pickle.UnpicklingError` (no code) | `ActualCarrierRefusal` with stable code |
| Truncated public pickle | `pickle.UnpicklingError` (no code) | `ActualCarrierRefusal` with stable code |
| Missing local receipt with a pin | `FileNotFoundError` (no code) | `ActualCarrierRefusal` with stable code |

The relevant code is `_sha_file` (`actual_carrier.py:56-61`), `_iter_pickle` (`:100-106`), and the pinned receipt/loading path (`:167-189`). SHA mismatch, wrong source, and mutated-stream controls do return typed `ActualCarrierRefusal`; the gap is specifically file-open and pickle decode failures.

Smallest repair:

- Wrap receipt/stream file access (`OSError`/`FileNotFoundError`) and pickle decode (`pickle.UnpicklingError`, `EOFError`, `ValueError`) in `ActualCarrierRefusal` with explicit stable codes.
- Preserve the existing SHA/source/count/type checks.
- Add malformed, truncated, and missing-file regression cases.

## Preserved positive/control evidence

- Fixture actual-carrier adapter: **SUCCESS**; release/source identities and stream counts preserved.
- Exact human-grant authentication: **SUCCESS**; wrong grant SHA → `AuthorizedExecutionRefusal: GRANT_SHA256_MISMATCH`.
- Wrong receipt pin → `LOCAL_RECEIPT_SHA256_MISMATCH`.
- Wrong expected source → `LOCAL_SOURCE_MISMATCH`.
- Mutated stream without receipt update → `LOCAL_RECEIPT_PUBLIC_OBJECTS_SHA_MISMATCH`.
- Changed native condition-count path: 44 operations, 44 executed, 38 conditionals, condition ledger/counts equal; accepted C boundary remains executable on the labelled fixture.
- Accepted D dependency is present and byte-exact.

The candidate author test run was also observed as `20 passed, 1 skipped` for the authorized/carrier and observed-response suites; those tests do not exercise the missing fixture issuer→executor→D path or the untyped carrier cases above and are not independent acceptance.

## Exact review command

```sh
PYTHONPATH=. python3 -m pytest campaign_src04_completion/empirical/actual_review/test_actual_carrier_review.py -q -o addopts=''
```

**10 passed in 17.85s** (exit 0). The passing suite includes explicit `_DEFECT` discriminators that assert the current missing/refused behavior; it is not a scoped PASS. Relevant hashes are in `MEASUREMENTS.json` and `REVIEW.json`.

## Limits

- SRC04 repository nonrespondent fixture only; no original SAV stat/hash/open/decode/read, no original respondent rows, and no original workload.
- The actual original release `9ddec985...97ae1`, its 177 responses + 3 coordinates, and the 7,337 respondent product were not processed or qualified here; that is the separate original-source reviewer's work.
- No population, weighted, causal, structural, Field Forge, N11/N12, actor, or source-local claim is made.
- No new engine, worker, provider, model, permission, or unrelated source investigation.
