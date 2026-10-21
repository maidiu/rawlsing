# B53H R2 — TRUSTED PREFILTER ATTACK WITNESS

**Source:** commit `026a6ba3075817b7f0370619843ee7227967bc8e`
**Verifier:** `09_trusted_oracle_prefilter.py`, blob `c7eea07999752a5101cacd8c3ede68fb24f061e7`
**Published tests:** `10_test_trusted_oracle_prefilter.py`, blob `df073d1a3ac01e3009699c14022d60f70dae790f`

## Published controls actually executed

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest \
  tests/_pinned/b53h/10_test_trusted_oracle_prefilter.py \
  -q -o python_files='10_test_*.py'
```

Result: **8 passed, 0 failed, 0 errors, 0 skipped** (`receipts/pytest_b53h_published.xml`, `receipts/pytest_b53h_published.log`).

Published positive controls confirmed: output-operation swap, duplicate topology collapse, policy-pin mutation, missing fixture, false original zero, missing I05 declaration, and fake scientific completion are rejected. The happy structural case is explicitly not an execution certificate.

`tests/test_b53h_trusted_prefilter.py` also calls all eight published tests in-process and adds six probes; the combined suite reports 7 passed (the wrapper plus six probes). The wrapper asserts that all eight published functions exist and pass.

## Attack A — self-attested native claims pass

Input: a policy and result accepted by the published happy path. The result is edited only in candidate-controlled fields:

- `actual_native_c11 = True`
- `actual_native_i03 = True`
- `actual_native_i05 = True`
- `public_call_trace_id = "claimed-without-replay"`
- the published metamorphic events remain candidate booleans with `real_consumer_id = "E04"`

Observed: `analyze()` returns `failures=[]` and `status=STRUCTURAL_CROSSWALK_READY_FOR_INDEPENDENT_NATIVE_VALIDATION`. The output's own `limit` correctly says `NO_NATIVE_EXECUTION_OR_ATTESTATION_VALIDATED_HERE`.

This does not contradict B53H's own disclaimer. It falsifies any downstream use of a green result as proof that native C11/I03/I05 ran, that a consumer ran, or that a replay exists. The verifier checks a boolean claimed by the candidate, not an authenticated runner event. A string `public_call_trace_id` is sufficient; no replay object, signature, command, stdout digest, or process identity is required.

## Attack B — caller can self-pin a forged policy

Input: the caller supplies both `--trusted-policy` and `--expected-policy-sha256`. The test forges an operation expectation, rewrites the candidate result to match, computes the digest of the forged policy, and passes that digest.

Observed: `analyze()` returns `failures=[]` and the structural-ready status. The function cannot establish that the pin came from a protected ref or an independent CI checkout.

This is an operational boundary, not a cryptographic break of a correctly deployed environment. It is sufficient to reject "the Python verifier is trusted CI." A protected policy ref, an authenticated runner result, and a workflow that does not take the pin from the candidate are required and were **NOT_RUN/NOT_INSTALLED** here.

## Positive control — independent expected set rejects operation swap

Input: the same happy policy plus an externally retained pin; the candidate result replaces the expected operation states with `{"fake_op":"NATIVE_PRODUCED"}`.

Observed: `OPERATION_STATE_ANTI_JOIN:fx0` and `status=REVISE`.

Thus the anti-join works when the expected set is genuinely independent. The distinction is:

| Condition | Result |
|---|---|
| Protected expected operation set, candidate changes operations | rejected |
| Protected operation set, candidate invents native booleans/trace/consumer event | accepted structurally |
| Candidate supplies policy and pin together | accepted structurally |

## What the verifier does not check

- No actual C11 repository, I03 query, I05 discovery, or Batch receipt.
- No process invocation, stdout/stderr digest, executable identity, or command transcript.
- No signature or attestation over the runner result.
- No replay object, cold restore object, or consumption trace.
- No check that `public_call_trace_id` resolves to anything.
- No check that `real_consumer_id` names an executable consumer or that it ran.
- Mutated candidate commit and mutated source roster are rejected, but only as claimed strings against the pinned policy; no commit object or source edition is resolved.
- No check that protected fixture semantics are sourcefree or scientifically admissible.
- No source right, source edition, original35 measurement, scientific meaning, or N11/N12 issuance.

## Minimum requirements for a later independently executed trusted CI

1. Protected policy and expected operation/fixture sets live at an immutable ref outside candidate write authority; the workflow pins the policy by an independently authorized SHA.
2. The runner result is produced by the protected workflow, not candidate content, and carries an authenticated job identity, exact candidate commit, command, timestamps, and artifact digests.
3. The verifier consumes an authenticated result envelope, not candidate booleans; a forged `actual_native_*` field must not be accepted.
4. Real C11/I03/I05/Batch/consumer events, sourcefree fixture roots, and positive/negative controls are linked by exact refs and digests.
5. A separate reviewer and owner decision remain required for scientific meaning, source rights, universal promotion, N11, and N12.

No CI, required check, protected ref, signature root, production adoption, or repair was installed by this work.
