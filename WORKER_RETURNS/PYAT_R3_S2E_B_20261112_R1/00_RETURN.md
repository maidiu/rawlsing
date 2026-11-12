# PYAT R3 S2-E — Agent B adversarial construction and reciprocal handoff

## Actual frozen mission, not the predecessor's title

The supplied heading says **S1-C/P1-04 (issue #918)**, but the predecessor's immutable artifact PR #951 is **S2-E/P2-06 (issue #919)**. These are not interchangeable. S1-C source-qualified U/E_pre operation/fate anti-joins remain entirely unclosed by this S2-E descendant. R3C/R3S (#909) govern scoped G1–G5, the stop condition, nonauthor G5, and limited A/B exchange. This return repairs only S2-E at a sourcefree grade.

## Exact lineage and changed files

- PRE-MAIN comparison: `6a5c12f04323d74001f9632063ec907f4fc4468e` (not changed).
- Isolated combined ancestor PR #948: `7064daa14d93109211629e72d08f3a6e705a0d57`.
- Agent A immutable tested code: `d7af5b8df922caa86bcd36a7baa0bbb55b43742d`, A return HEAD `4357675fc13cc933134bd3303e7efead7aeba4ea`, draft #951.
- B source/test cut: `0bc69faa4058bc97db760f711f4e193837501220` on `agent/pyat-r3-s2e-b-public-output-conservation-20261112-r1`, draft PR #958 targeting A branch.
- Original A `pre553_issued_workload.py` blob: `6356d6639a5af65b9e4e7f86f4e3b495905e9d2c`. Existing native consumer `pre553_universal_workload.py` blob: `8e7fe00a3ed008361d9f3c501e7782b2de3a636e`.
- B changes: `rawlsing_next/pre553_issued_workload.py`, `rawlsing_next/pre553_universal_workload.py`, B regression test file, isolated CI workflow, return/receipt only.

## What Agent A got right (independently source-checked; test evidence inherited)

A reused exact I03/I05/Batch rather than inventing another scientific engine. Its `pre553_s2e_exact_conservation.py` audits completed Batch receipt/result-ref closure, complete I03 query domains when given the original runtime catalog, I05 candidate-fate and fact provenance, typed negative states and per-unit canonical preimages. It has an exact 5-unit 12-respondent sourcefree Batch witness, including distinct forward/reverse F2 denominator sets and an 8-cell F4 joint, with a shared-vs-ungrouped parity assertion and manual F4 oracle. A's GitHub CI #43275018294 succeeded on a real allocated runner (78 + 19 tests reported PASS). A was correct not to claim original35 native science, speedup, saved-store S2-D, or G5.

An initial B accusation that I05 receipt-to-fact preimages could be removed without detection was **refuted**: `ExactBoundedDiscoveryResult.__post_init__` already requires `tuple(f.ref for f in self.empirical_facts) == self.empirical_fact_refs`. I do not count that as a defect.

## One material source-exact omission — S2E-B-01

At A source `NativeWorkloadResult.exact_s2e_output_census` only forwards `outputs_by_unit` and Batch receipts to `census_native_batch`. It never examines the same result's `native_outputs` or `output_refs`. Yet the actual first consumer `rawlsing_next/pre553_universal_workload.py::execute_universal_workload` iterates `result.native_outputs` when deriving published `fact_refs` (original source line 258). The current constructor usually derives all fields from the same map; this is specifically a **post-execution published-view severance** risk, not an allegation that ordinary native evaluation already drops results.

Concrete falsifier: build a genuine `NativeWorkloadResult` using the existing sourcefree `_full_query_run`; `dataclasses.replace(result, native_outputs=())` preserves the valid `outputs_by_unit` and completed receipt. Before B's correction, the optional census method did not read `native_outputs`, so its private-domain completion would not by itself detect the public view loss. A corresponding `replace(result, output_refs=())` similarly escapes that specific check. The real `execute_universal_workload` reads `native_outputs` for `fact_refs`; it also lacked a closure check before treating the operation as executed. This violates the existing S2-E G3 conservation obligation at an existing reader, not a newly invented hardening requirement.

**Source-level proof:** fetched A/B exact files and mechanically verified that A's method references neither public field, while B's tests both and preserves the original `census_native_batch` invocation.

## Correction made in the same lineage

1. Add `NativeWorkloadResult.assert_published_output_closure()`: public `native_outputs` must equal the canonical unit-hash-ordered actual output map; public `output_refs` must exactly match receipt result refs. Typed `S2EOutputConservationError` on either mismatch. No scientific computation, source authority or durable store change.
2. Call the check before Agent A's existing exact census, so private completeness cannot be represented as public output completeness.
3. Invoke the same *O(unit-count) check* in `execute_universal_workload`, immediately after its existing native issuer execution and before appending executed IDs or collecting fact refs. The existing `except` records a typed ERROR and leaves the affected operation unexecuted; no counterfeit positive.
4. Add three sourcefree adversarial tests: (i) missing public native outputs, (ii) missing public result refs, (iii) real universal first-reader sourcefree execution, injected lost public native output, failure/anti-join, restoration to identical fact and receipt refs.

## Proof, limitations and honest G1–G5

- **Independently source-proved:** A's census omitted both public output surfaces; the actual first reader consumes `native_outputs`; B's changed method and consumer check guard that mismatch.
- **Not run:** B's new tests, A's original regressions at B SHA, and resource measurements. GitHub Actions runs #43278658811 (before repair), #43278864485, and latest #43280064658 (after repair) all completed FAILURE **before runner assignment**; GitHub jobs show `runner_id=0` and zero steps. A's preexisting CI success is not B's test success. A sourcefree 97-pass suite is inherited evidence only.
- **G1:** PARTIAL; exact localized consumer/ABI accounted for, no all35 science/authority.
- **G2:** A sourcefree native pass inherited; B modified SHA S2 NOT_RUN.
- **G3:** source-exact breach and repair candidate, runnable hostile controls committed, execution NOT_RUN.
- **G4:** resource scale unchanged in architecture; the new mirror check is bounded by units in its intended normal path but has no measured peak RSS/100k result, and the S2-D saved-store dependency remains.
- **G5:** NOT_RUN, must be independent of both duel authors.

The B first-consumer fix deliberately does **not** call the full canonical output census at each operation, avoiding an unmeasured extra full-output proof serialization in the ordinary serving path. The existing explicit census remains available for full S2-E exact-output comparison. It neither reissues CURRENT permission nor independently authenticates an external producer.

## Self-adversarial assessment

**Attack against my new code:** A fully coherent attacker could rewrite `outputs_by_unit`, `native_outputs` and Batch refs together. My mirror check would not authenticate that rewritten result; full native census, source/authority verification, and independent expected oracle remain necessary. Direct equality may also incur cost if objects are separately rehydrated (rather than the current same-object normal execution). The new exception becomes a recorded per-operation ERROR, not a global Python exception; consumers must observe `anti_join.no_drop_ok` and failures. No hidden scientific or original35 issuer rights were created.

**Highest-priority action for Agent A:** Obtain a functioning test runner, run the committed B tests and A regressions on the exact B code SHA; try to disprove the public-view loss using the real normal consumer; test legitimate partial native result and cold restored complete result for a false refusal; if a counterexample invalidates B's repair, report exact input/expected/observed and fix it in the one allowed response. Preserve A's unrelated native code and the existing S2-F tests.

**Challenge refuted:** Removing `ExactBoundedDiscoveryResult.empirical_facts` while retaining refs is already rejected by its constructor. Do not turn this false criticism into a review demand.

**Separate surviving obligation:** S1-C/P1-04 remains a distinct scientific operation/fate-census task; PR #951 and this S2-E repair cannot close it.

**STOP:** `HOLD_EXECUTION_ENVIRONMENT` for B's S2 proof; no G5 self-acceptance, no protected merge, no optional broad hardening. Continue only the exact tests needed to establish or falsify this frozen repair, then A's bounded counterattack and independent G5.
