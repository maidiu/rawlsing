# Construction-only C11 candidate

## Result

**PASS — narrow executable construction-only entry implemented and tested; Q2 gates preserved.**

- Exact accepted baseline: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- Isolated scratch baseline: `e3f79397ac51f1f6fc5ed998577bca90f855e483`
- Candidate scratch commit: `3b48fa355ee85ab0b7854301b275fde29dabbe44`
- Patch: `candidate.patch` (2 files: `pre553_source_i02_handoff.py`, focused test)

## Candidate design

A shared private `_construct_source_bodies` now owns the existing exact source
decode, projection/spooling, manifest and `SourceSavedBodySink` publication,
guards, target invalidation and cleanup. Existing `build_source_i02_handoff`
uses it with the unchanged census/frontier `_operation_source_antijoin` hook.

New public `build_source_i02_construction_only`:
- accepts exact `SourceConfig` plus existing source-read inputs;
- accepts no census, inventory, policy or scientific frontier;
- returns `SourceI02ConstructionOnlyResult` with source metadata, roots,
  manifest/counts/stats, body transport and explicit unresolved states;
- has no operation-fate/census fields and explicitly reports `joined_q2=False`,
  `authorized_executable_q2=False`, `issued_workload=False`;
- preserves exact current/resolver/request checks before source bytes.

The governed Q2 entrance keeps its exact census/frontier verification and
operation-fate anti-join hook; no writer, S2-C physical format, decoder, source
authorization or product-format semantics were changed.

## Native evidence

- Candidate focused test: one tiny sourcefree construction + independent fresh
  `VerifiedDirectEstate` reopen; exact roots, body family counts, respondent
  identity/events, routing presence, source metadata, and unresolved Q2/holds.
- Pre-read denial: original-mode fixture with `DenyResolver`; destination absent,
  decoder call count zero, refusal before bytes.
- Existing Q2 source-i02 regression court: passed with candidate.
- Combined result: **13 passed in 3.43 s**.

No real source was opened or decoded; no product branch edits were made; no
configuration join, historical grant adapter, or separate experiment matrix was
used.
