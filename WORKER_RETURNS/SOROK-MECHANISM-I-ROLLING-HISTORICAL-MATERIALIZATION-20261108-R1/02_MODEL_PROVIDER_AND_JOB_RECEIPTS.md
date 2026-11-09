# Model provider and job receipts

**Evidence grade `SOURCEFREE_MOCK_HTTP`.** The P4 subprocess made one HTTP
request to a one-request loopback fixture. The fixture returned a controlled
candidate. The adapter receipt records `live=true` and `mode=LIVE` because
the endpoint transport performed HTTP. Those fields do not establish that
the endpoint ran a model. Actual runtime LLM evidence is
`LIVE_PROVIDER_NOT_RUN`.

Observed on the published mock transport cut
`b9880a4568605ccce703a611acdf428dccaa925f`.

| Receipt field | Value |
|---|---|
| Schema | `SOROK_HISTORICAL_MODEL_RECEIPT@1` |
| Provider contract | `SOROK_HISTORICAL_MODEL_PROVIDER@1` |
| Model reported by fixture | `test-endpoint` |
| Model identity digest | `61d711ad5b740ff352c41a4ef65509e9aea0776f1b1a8ba861739139187c293a` |
| Job | `history-job:8f4915f970a76262630952c25143f5fe57e34a527cfdf6d62e189670007331e8` |
| Owner packet digest | `a947b16ca9a3730ef48976e951b3f18026cb9b0e386192291f9d2afad090332c` |
| Request digest | `bb5a975d8dbfd97d0ed633802ee2fb7adb77d6a8968cbcbc5e68884b56b75a19` |
| Raw response text digest | `a1c9fbd256506c1bf0da5a142a68e06e3f4890b394f7d586a7cefdac8317e0a4` |
| Normalized candidate digest | `2e6166edf88ddc60a8f4f06531eae7f87d2e27491bee501727deb60ce151f5a2` |
| Requests and retries | 1 and 0 |
| Fixture transport elapsed | 12.37 ms |
| Input, output and total tokens | Unknown. The fixture supplied no usage. |
| Model cost | Not measured. |
| Authority and writes | `issues_authority=false`, `writes_world=false` |

The default transport requests at most 4,096 output tokens per call, checks
a 64,000-byte model-text ceiling, and permits at most two transport attempts
with a 30-second timeout per attempt. The HTTP envelope is bounded separately.
The owner maintains its own durable lease and rejects superseded results.

Reproduce with
`rawlsing_next/tests/test_sorok_history_wake.py::test_p4_wake_completes_through_a_mock_http_endpoint`.
Keep the test state and reopen it through `run_p4.open_owner`. Use the target's
`job_id` to read `HistoricalWorld.job`, including its receipt and admission.
Request hashes may differ between loopback runs because the endpoint port is
assigned per fixture.
