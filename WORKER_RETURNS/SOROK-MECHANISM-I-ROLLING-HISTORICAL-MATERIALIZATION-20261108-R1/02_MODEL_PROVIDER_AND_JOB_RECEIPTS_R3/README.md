# Actual model execution and honest failure cuts

These are actual runtime calls, not HTTP mocks. The endpoint/model came from the existing authenticated OpenCode provider registry; requests used the authorized local account credential via environment only. No credentials are present.

1. Attempt01 records Python CA failure, then an HTTP403 before application identification was fixed. Neither is model inference.
2. Attempt02 records HTTP400 (missing stable session header), not model inference.
3. Attempt03 records actual DeepSeek V4.1 Flash inference:1596 input/2706 output tokens,35.972s; unsupported tool_available proposal was SOURCE_HELD, not admitted depth.
4. Attempt04 records actual inference:1703 input/4096 output tokens,58.167s; reasoning consumed3635tokens and the answer truncated, so INVALID_JSON/FAILED_TERMINAL; no owner admission.
5. Attempt05 is actual inference→owner H0 admission→P4 inspection→cold readback at source f459744a2:1728 input/2904 output tokens (2675reasoning),47.937s; provider-reported list cost0.0020016 and Go allowance0.00120096, cost field0 (subscription billing, not a claim of no resource cost). Owner INDEX_READY, two accepted facts, condition=serviceable returned by the actual inspector; cold target bytes equal and no additional provider call. Raw request, response, usage, full job/admission and inspector readset are in the JSON files.

Three calls actually returned model output (attempts03–05). TLS/HTTP diagnostic requests did not return model output and are not counted as successful inference. Receipt counters count calls per invocation, not a fictional exactly-once network guarantee. Failed/source-held cuts are retained rather than overwritten.

This proves author-executed LIVE_PROVIDER_S2 H0/L2 pipeline only. It does not prove full L3/H1, generalized episode creation, original actor science, production suitability of this subscription endpoint, or independent final receiving. Keep those axes separate.

Reproduce with09_LIVE_HISTORY_RUN.py --state <fresh-local-state> --receipts <task-local-receipts> --endpoint <configured-chat-completions-endpoint> --model <authorized-model>. Set SOROK_HISTORY_MODEL_API_KEY privately and SSL_CERT_FILE to the runner's trusted CA bundle when required. --resume reuses an existing pending/retryable job and never resets a terminal failure. --max-output-tokens bounds reasoning plus emitted answer. No account/server/shared-permission changes are needed.
