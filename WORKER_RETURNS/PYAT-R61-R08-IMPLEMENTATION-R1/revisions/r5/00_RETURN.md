# R61-R08 R5 implementation return

**Verdict: REVISE for full-progressive reach only. R5 closes the two R4 review defects: productive readers/cache now serve only the complete signed envelope projection, and live execution is fail-closed without a configured producer pin. Positive native/evaluator/cold and status controls remain.**

## Custody

- Startup: `48a2eaf6d3c653e2efe40643c427f28c47cd744b`
- R5 amendment commit (banked before code commit): `5cdbaaecdcd3a1ecfee62025e4a0ca7f99e9b469`
- R5 code commit: `cfe3297e8962b3a11a62e9e89d26d7de50fadba5`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- R4 review preserved: `d1baa92cb457c30bf6dffb91f23f8cee351de4f6`
- Writes only the two allowlisted code/test paths plus this `revisions/r5/` root.

## Missing functions repaired

### 1. Complete authenticated served-result projection

`ExecutedEvidenceEnvelope` is now the sole authority for productive output.
`_envelope_result_projection` enumerates the complete signed result relation
(K, eligibility/execution/result axes, denominator, cells, evidence ref, producer
receipt/fact/state, consumer query/result, consumer values, uncertainty).

- `EvidenceConsumerReader.read`/`e04_step` verify the envelope and rebuild output
  from `envelope.consumer_values_read`; they never return supplied unsigned
  result values.
- A supplied result differing in any signed field/value category is refused
  (`EvidenceAssociationError`), not silently served.
- Evidence/query/rule objects must match envelope content digests; matching
  unsigned labels on a different object are insufficient.
- Cache export refuses a mutated unsigned result and writes only the signed
  projection. Cache import requires the public result material to equal the
  signed projection. Replay rebuilds only from the signed envelope.

This covers denominator/cells/state/evidence ref, producer receipt/fact/state,
uncertainty, query/model/provenance, axes, K/context/source/clock/policy/grade/
version and nested consumer values — generically, not named 999 fields.

### 2. Fail-closed live producer pin

`EvidenceResolver.bind` now admits producer execution only when
`admitted_producer` is non-null and `binding.producer is admitted_producer`.
Omitting the pin disables live execution; it no longer means "accept any
callable". A substituted callable with a copied legitimate owner admission is
refused before invocation (call count 0). A verifier-only resolver can still
import/read already-authenticated cold cache entries; it cannot execute a new
producer. Imported data/cache cannot choose or rotate the producer/root.

## Preserved positives and status

- Actual AT07 provider: 54 yes / 6 no / denominator 60, actual unchanged
  evaluator `EXACT_SUPPORTED`; signed envelope and same-consumer read.
- Changed native `CHANGED_SOURCE_LAW`: 54/16/70 remains its own value.
- Actual observed zero: denominator 60, `no=0`, supported.
- Actual ZERO_SUPPORT: denominator 0, no evidence/values, non-productive.
- VALID_NULL/DIFFUSE/VALID_EMPTY/OBSERVED_ZERO distinct productive states;
  Z UNRESOLVED denominator 16 retained, never exact.
- Typed A0/A1, condition/order/currentness, wrong-root, attacker-issuer,
  forged-context/cache controls remain.

## Tests

Command (exit 0):

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r5/junit.xml
```

**34 passed, 0 failed, 0 errors, 0 skipped, 9.70 s** (21 R08 tests + 13 unchanged
C1 composition regressions).

Immutable R4 review probe replay: **7 passed, 2 failed as expected old defect
probes**. Both failures are the probes that asserted the old defective behavior
(`read` serving unsigned 999 values) by calling `read` and expecting a returned
denominator; the repaired path now raises `EvidenceAssociationError`. Successor
R5 tests assert the lawful refusal/signed projection for the same field classes.
All other R4 positives/no-config/wrong-root/attacker-issuer/changed-native/cold/
cache-forgery controls pass. No archived probe was edited.

## Reach and limits

Covered at the callable grain: signed trusted-host admission, actual
provider/evaluator/consumer values-read, complete signed projection, cache
replay, fail-closed live pin, status reduction. NOT_REACHED: live J42
`E41ProviderAdapter.step`, live P41 progressive and repaired live E04 terminal;
archived returns remain immutable and unedited.

No original data/source/science, production/CI, N11/N12, F6/F7/F8, actor, Sorok,
J52/W52 or protected-capture authority is issued. Same-UID host/key compromise,
ptrace/root and dishonest competent issuer remain outside the scoped threat
model. Author validation only; distinct R5 hostile reviewer has not been launched
or self-adopted.
