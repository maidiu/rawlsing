# R61-R08V R4 independent review — defects

## D1 (review finding 1) — the SAME consumer serves unsigned result fields

Severity: decisive for the scoped D3/D4 verdict.

Location: `rawlsing_next/pre553_universal_evidence_binding.py`

- `EvidenceConsumerReader._assert_association` (lines ~2400-2451) verifies the
  signed envelope and checks `result.consumer_result_hash`, `denominator`,
  `cells`, `result_state`, `eligibility_state` and `execution_state`.
- It does not compare `result.consumer_values_read` with the signed
  `envelope.consumer_values_read`.
- It does not compare `result.evidence_ref`, `producer_receipt_ref`,
  `producer_fact_ref`, `producer_fact_state`, `uncertainty_state` or
  `consumer_query_ref` with the envelope.
- `read()` (lines ~2453-2470) returns `dict(self.result.consumer_values_read)`
  and only overwrites the replay hash/state/material at the end.
- `e04_step()` (lines ~2472-2493) reads `denominator`, `cells`, `evidence_ref`
  and `result_state` from that unsigned dictionary.

Reproducer (independent public API only; no reflection, monkeypatch, ptrace or
attacker-owned verifier):

1. Build the canonical positive through the pinned native fixture and the
   configured trusted host; `resolver.resolve(request)` returns a signed
   `EvidenceResult` with denominator 60 and `SUPPORTED`.
2. `values = dict(result.consumer_values_read)`; set
   `values["denominator"] = 999`,
   `values["cells"] = [{"cell":"yes", ... "raw_numerator_support":999}]`,
   `values["evidence_ref"] = {"kind":"FORGED_EVIDENCE", ...}`,
   `values["result_state"] = "ZERO_SUPPORT"`.
3. `mutated = dataclasses.replace(result, consumer_values_read=values)`.
4. `EvidenceConsumerReader(request, mutated, verifier=<same configured
   verifier>).read()` returns denominator 999, forged cells and forged evidence
   ref. `.e04_step()` returns state `ZERO_SUPPORT`, denominator 999.

Observed JSON is `outcomes/r4_observations.json` under
`forged_consumer_values_read`; the probe is
`probes/test_r08v_r4_independent_boundary.py::test_forged_consumer_values_read_must_refuse_or_serve_signed_values`
(assertion fails, recording the defect). The signed envelope still says 60 /
`SUPPORTED`.

A second probe,
`::test_mutated_result_metadata_must_refuse`, replaces
`producer_fact_state`, `uncertainty_state`, `producer_receipt_ref` and
`producer_fact_ref` with forged values after signing; the same reader accepts
the result. This is the required E6.5 "mutate result fields after signature"
route.

Why this is not a harness artifact: the envelope signature verifies under the
configured verifier; the evaluator replay hash is genuine; only the unsigned
result copy is altered. The defect is the missing envelope-to-result equality,
not a forged signature.

## D2 (review finding 2) — optional producer pin admits a substituted callable

Severity: conditional on a trust configuration that omits `admitted_producer`;
the author's own fixture passes it and therefore does not exercise this path.

Location: `EvidenceResolver.__init__` line ~1647 (`admitted_producer=None`), and
`bind` lines ~1676-1688:

```python
self._admitted[key] = bool(
    self._admission_verifier is not None
    and binding.admission is not None
    and self._admission_verifier.verify_producer(...)
    and (self._admitted_producer is None or binding.producer is self._admitted_producer)
)
```

When `admitted_producer` is omitted, the final conjunct is true for any callable.
The producer admission covers owner material, not the callable. A caller can copy
a legitimate binding/admission and replace `binding.producer`.

Reproducer (`probes/...::test_substituted_producer_without_optional_pin_must_not_execute`):

1. Construct `EvidenceResolver(admission_verifier=<configured verifier>,
   executor=<configured authority>)` (no `admitted_producer`).
2. Build a legitimate binding, then `dataclasses.replace(binding,
   producer=forged_producer)` where `forged_producer` raises
   `SUBSTITUTED_PRODUCER_EXECUTED`.
3. `resolver.bind(binding)` then `resolver.resolve(request)` executes
   `forged_producer` (observed call count 1, exception
   `SUBSTITUTED_PRODUCER_EXECUTED`).

The missing function is a mandatory fail-closed producer pin (or a default-deny
admission rule when no callable is configured).

## What did not fail

- Independent positive: 54/6/60 and same consumer hash; changed native case
  54/16/70; cold replay same hash.
- No-config default resolver/reader/import refusal; wrong-root reader refusal;
  attacker issuer with the same id refused; cache missing-envelope and
  forged-evidence-999 refused.
- Author suite replay: 31 passed, no failures/errors/skips.

These positive results are preserved in `proof_witness.json` and
`outcomes/r4_observations.json`.
