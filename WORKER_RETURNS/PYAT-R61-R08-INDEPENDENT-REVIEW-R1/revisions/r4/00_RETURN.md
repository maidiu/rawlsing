# R61-R08V R4 independent review — return

Verdict: **REVISE.** The configured trusted-host path does serve a genuine
independent native positive, cold replay and several typed refusals, but the
SAME public consumer still accepts an unsigned result mutation. A caller can
take a legitimately signed `EvidenceResult`, replace `consumer_values_read` and
several result metadata fields with public `dataclasses.replace`, and
`EvidenceConsumerReader.read()`/`e04_step()` serve the forged denominator,
cells, evidence ref and result state while the signed envelope still says
60 / SUPPORTED. This is the D3 "internal identities must agree with the
envelope" and D4 "close the direct-reader route" obligation, at the accepted
public interface, without reflection, monkeypatching, ptrace or an
attacker-owned resolver.

The second, narrower defect is that the admitted-producer pin is optional:
`EvidenceResolver(admission_verifier=..., executor=...)` without
`admitted_producer` admits a copied legitimate producer admission whose binding
carries a substituted public callable, and the substituted callable executes.
The author's configured fixture always supplies `admitted_producer`, so its own
callable-substitution test does not cover this fail-open configuration.

## Custody actually checked

- Exact root/worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`.
- Branch: `agent/opencode-pyat-r61-r08v-r4-independent-review-r1`.
- Candidate/startup: `48a2eaf6d3c653e2efe40643c427f28c47cd744b`.
- Frozen reviewer EXPECTATIONS: `4cf30eee34891f269bed95294e3f31ef80c0b2d5`
  (unchanged; HEAD at review start).
- Candidate code commit: `3c69a13e64dd2bca65858906a367347e895f9d82`.
- Code blob `c3b039fd908c20b6494a2bcf37b89d878dfaf6c6`; test blob
  `1f72a428283eb35d7bcedf5391528dbcbd22a489` (working tree matches both).
- Native owner blobs independently re-hashed and equal to the frozen pins:
  provider `23167aa25291fb148b1e3cf210ac33fe7769b783`, composition
  `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`, positioned evaluator
  `62e5eced47b64512f47b004e3e13a6ef3fe21de7`, empirical objects
  `a61365b994e5c3c50de0f598fcf40e90abf757b6`, AT07/n10e fixture
  `0e384f72fa615dc72a0dcb08a36472a64b7b1e4a`.
- Candidate delta is exactly the two allowlisted code/test paths in
  `3c69a13e6` and the six author r4 report artifacts in `48a2eaf6d`; the precode
  API contract was already banked in `07d94592a`. No native-owner, evaluator,
  archived-return, HQ or workflow path changed.
- Author r4 manifest recomputed independently: all six listed artifacts match
  byte-for-byte and the manifest explicitly self-excludes `manifest.json`.
- Direct remote readback at start: `origin` branch
  `agent/opencode-pyat-r61-r08v-r4-independent-review-r1` was at
  `48a2eaf6d3c653e2efe40643c427f28c47cd744b`.

## Positive and preservation evidence

The reviewer used the pinned source-free AT07/n10e fixture authority and the
unchanged provider/evaluator, not an author assertion, for the oracle:

- Independent response-table count: `POSITION=P1, ANSWER=yes` 54,
  `POSITION=P1, ANSWER=no` 6, denominator 60. The actual provider produced the
  same cells; the SAME configured public consumer read denominator 60,
  `EXACT_SUPPORTED`, and consumer hash
  `47b51a3b6df4ec051b5b9fb04a92760c791f4ac761f20a157966cbe1b481a4be`.
- Changed native source law (`CHANGED_SOURCE_LAW`): independent count 54 yes /
  16 no / 70 denominator; the SAME consumer served 70 and 54/16, not the
  canonical 54/6/60.
- Cold fresh process with the verifier key delivered separately on stdin
  reproduced `AUTHENTICATED_CACHE`, denominator 60 and the same consumer hash.
- No-config resolver/reader/import refused with `NO_CONFIGURED_TRUST_ROOT`; a
  wrong-root reader and an attacker issuer with the same authoritative id were
  refused; cache missing-envelope and forged-evidence-999 records refused.
- Author suite replay: 31 passed, 0 failed, 0 skipped (`junit/author_suite_replay.xml`).
  This replay is regression evidence, not a fresh court and not a substitute for
  the independent hostile probes.

## Decisive defects

### R4-D3/D4-01 — reader serves unsigned result fields and values-read

`EvidenceConsumerReader._assert_association` verifies the signed envelope, the
request K, and a subset of result fields (evaluator hash, denominator, cells,
eligibility/execution/result axes). It never compares
`result.consumer_values_read` with `envelope.consumer_values_read`, and it never
compares `result.evidence_ref`, `producer_receipt_ref`, `producer_fact_ref`,
`producer_fact_state`, `uncertainty_state` or `consumer_query_ref` with the
signed envelope. `read()` then returns the unsigned `consumer_values_read`
dictionary verbatim (apart from adding the genuine replay hash/state/material),
and `e04_step()` consumes its `denominator`, `cells`, `evidence_ref` and
`result_state`.

Independent observation (`outcomes/r4_observations.json`, probe
`test_forged_consumer_values_read_must_refuse_or_serve_signed_values`):

- signed envelope denominator: 60; signed envelope result: `SUPPORTED`;
- caller replaces `consumer_values_read.denominator = 999`,
  `cells = [{yes, 999}]`, `evidence_ref = FORGED_EVIDENCE`,
  `result_state = ZERO_SUPPORT`;
- SAME `EvidenceConsumerReader(request, mutated_result, verifier=<configured>)`
  returns denominator 999, forged cells and forged evidence ref, and
  `e04_step()` returns state `ZERO_SUPPORT`, denominator 999;
- the original signed envelope and original result are untouched, and restoring
  them returns 60 again.

A second observation (`test_mutated_result_metadata_must_refuse`) replaces
`producer_fact_state`, `uncertainty_state`, `producer_receipt_ref` and
`producer_fact_ref` after signing; the SAME reader accepts the result. This is
the exact E6.5 result-field mutation route, not a cache import edge.

### R4-D2-02 — producer callable pin is fail-open when omitted

`EvidenceResolver.__init__` defaults `admitted_producer=None`; `bind()` treats
`self._admitted_producer is None` as "accept any producer" provided the copied
legitimate admission verifies. Observation
(`test_substituted_producer_without_optional_pin_must_not_execute`): a resolver
constructed with the configured verifier and executor but without
`admitted_producer` binds a binding whose owner material and admission are
copied from the legitimate owner and whose `producer` raises
`SUBSTITUTED_PRODUCER_EXECUTED`; `resolve()` executes it. The author's configured
fixture passes `admitted_producer=provide_empirical_possibility_slice`, so the
author test exercises only the pinned configuration. The missing function is a
mandatory fail-closed producer pin, not a new architecture or service.

## Exact minimal missing function

1. In the accepted reader path, either reconstruct the served consumer output
   only from the signed `ExecutedEvidenceEnvelope`, or compare every envelope
   field to the supplied result: at minimum full `consumer_values_read`
   equality plus evidence ref/content, producer receipt/fact/state, uncertainty,
   consumer query ref and the result axes/provenance. A mutation after signing
   must refuse or be replaced by the signed value.
2. Make `admitted_producer` mandatory (or default to deny) whenever producer
   execution is configured, so a binding without the configured callable cannot
   be admitted.

No candidate code, test, native owner, archived return or HQ file was edited by
this review. This is not a repair, self-adoption or author wake.

## Retained limits

Full live J42/P41/E04 integration remains NOT_REACHED; no source/science,
original-35/1890, F6/F7/F8, production/CI, N11/N12, Sorok, J52/W52 or
protected-capture authority is claimed. Same-UID host/key compromise,
ptrace/root, monkeypatching and a dishonest competent issuer remain outside the
scoped threat model. The prior failed reviewer session is terminal
FACILITY_CWD_MISMATCH and produced no product verdict; see
`FACILITY_HISTORY.md`.

Artifacts: `defects.md`, `limits.md`, `EXPECTATIONS.md` (frozen), `RESUME.md`,
`FACILITY_HISTORY.md`, `proof_witness.json`, `SHA256manifest.json`,
`outcomes/r4_observations.json`, `probes/`, `junit/`, `logs/stdout-replacement1.jsonl`.
