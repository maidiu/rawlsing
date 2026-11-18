# R2 ENGINEERING LEDGER — SOURCE-PINNED FINDINGS

**Old 82d14 smoke preserved:** `evidence/*.json`, `fixture_contract.json`, `fixture_contract_600.json` are not overwritten by R2. R2 writes only `R2_PILOT/` plus additive handoff/return updates.

## Finding 1 — ref-only serializer defect in the prior harness

- Prior `fact_snapshot` used `canonical_json(result.facts)`.
- `rawlsing_next/pre553_empirical_objects.py` `canonicalize` lines 201–202:
  `if isinstance(value, CanonicalSemanticObject): return value.ref.as_dict()`.
- Therefore the old five-op `output_bytes = 1885` was **exact refs only**, not full fact/risk/denominator/replay/member payload. The label was wrong. This was a harness defect, not a product defect.
- R2 separately serializes `f.semantic_projection()`, `f.as_dict()`, exact fact refs, replay refs, risk/denominator/provenance member refs, and wrapper ABI bytes.
- Witness: first op ref-only 234 B vs full semantic 35,256 B / identity 35,458 B; five ops 1,170 B refs vs 148,727 B full semantic.

## Finding 2 — 600-slot geometry population

- `width_fixture.py` now adds 595 native question bindings to the accepted 5-role base, with substantial populated responses:
  - 7,616 valid substantive (80%),
  - 952 typed MISSING (10%),
  - 952 typed NOT_ASKED/routing (10%),
  - 8,568 added events, 54 base events, 8,622 total; 9,600 total routing; 16 weights.
- Pattern: `bucket = (respondent*595 + q_index) % 10`; deterministic. Extra events have unique occurrence identities and exact canonical bodies; no duplicate event refs; writer/I02 proof passed.
- Extra slots carry a separate TEST_ONLY source-geometry authority; they do not claim original eligible QUERY issuance.
- 600 columns are not dense events: 16 respondents produce 538–542 events/respondent, not 600.

## Finding 3 — exact pair and cost shape

- Fresh baseline vs fresh prepared on identical estate/catalog/five operations: full semantic/identity/refs/member/replay parity exact.
- Prepared S 5.498 s / 1 measured build vs baseline 14.378 s / 5 builds; Q remains dominant (60.176 vs 65.404 s); prepared RSS 200.8 MB vs baseline 185.3 MB. One pair only; no speedup claim.
- External supervision: 0.25 s sampling, build 33.18 s, baseline 80.62 s, prepared 78.05 s; combined 194.6 s; no abort; caps 300/180/720/2GiB/2GiB.

## Finding 4 — negative/restore

- Revoked CURRENT refuses before protected work; exact restore returns baseline selected identity `435262ba...`.
- Negative/restore is reported separately (1 index build, 1 evaluator call, ~14.8 s), not counted as a sixth timed operation.

## Reuse pins

- Product candidate `347baec...`; code/test `a13d69c...`; review `092bf29...`.
- Changed product blobs: `pre553_saved_workload_integration.py` `c568836...`/`54cf978...`; `pre553_batch_runner.py` `8320f28...`/`e8c110f...`; test `bf00eb5...`/`759a091...`.
- Fixture reuse: `fixture_1006.py` `1487ad2...`/`74cd928...`; `query_1006.py` `5a15272...`/`83054ca...`; `court_instrumentation.py` `5f2b424...`/`0bce33b...`.
- No product/test/source/R3 archive/peer edit; no original respondent/native/100k/science/actor data.

## Immutable R3

The 33 original R3 entries remain immutable. This ledger adds new engineering findings only; it does not rewrite any R3 entry.
