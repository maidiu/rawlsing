# R56-R02V — INDEPENDENT REVIEW HANDOFF AND OPEN CHALLENGES

**Candidate branch:** `agent/rabochii-pyat-r56-r02-occurrence-projection-repair-r1`
**Candidate startup:** `6d95a78bf6b7bcf70022e303a151255e65edc38a`
**Author:** this R02 session only. R02V must be a distinct native session/owner and must not reuse this author's session.
**Author boundary:** scoped candidate and author qualification only. This file is not reviewer acceptance.

## What to reproduce independently

1. Check out the exact candidate commit in a fresh worktree. Do not trust this author's test count or expected tuples.
2. Run `rawlsing_next/tests/test_universal_source_projection.py` from a cold interpreter with `PYTHONDONTWRITEBYTECODE=1`.
3. Independently generate or inspect the synthetic 12×2 repeated source. Verify:
   - 24 physical SCORE cells;
   - 24 C11 `RespondentEvent` objects, not 48;
   - each source `(PID, OCCASION)` maps to exactly one `(respondent key, occurrence index, value)` tuple;
   - the unchanged I03 repeated-query consumer returns `SUPPORTED` with denominator 12 and no fabricated support.
4. Vary respondent count, occasion count, equal repeated values, row order with a corresponding governed map, missing values and labels. Confirm the same invariant.
5. Confirm S1 one-row-per-respondent scalar behavior is unchanged and S2 separate-unit packages are refused rather than pooled.
6. Confirm wrong/duplicate/ambiguous row and occurrence maps fail before a C11 release or fact exists.
7. Mutate one source value and run the same frozen repeated query/assertion. Confirm the named downstream result changes. Restore the source and confirm a fresh process recovers.
8. Run the retained facade and empirical-query suites; author observed 42/42 passing.

## Open challenges the reviewer should attack

- **Binding-envelope choice:** repeated-cell occurrence identity is carried inside the existing `source_missing_declaration` binding envelope, with the original declaration nested. Raw value witnesses are unchanged, but the reviewer should decide whether this is an admissible adapter-level use of the existing physical binding key or requires a different facade-compatible route.
- **Event-ID domain:** the I03 repeated-query domain is built from the corrected release's event identities after exact tuple assertions already ran against independently computed source expectations. This is a downstream consumer test, but it is not a fully prospective query domain. The reviewer should determine whether a frozen event-ID oracle is required and whether the query would be better qualified with a source-independent target-domain construction.
- **Administration/form scope:** scalar FORM repeated across physical rows is refused as ambiguous rather than collapsed. Confirm that refusal is the correct supported-scope boundary and that no form semantics were lost.
- **S2 scope:** this candidate tests a cross-unit refusal, not a positive separate-unit projection. Confirm that is the intended preservation boundary for R02 and that no cross-unit pooling or positive relation was introduced.
- **Source identity stability:** the synthetic SAV writer adds metadata, so source byte hashes vary per generated fixture. The receipt records one exact run. Decide whether a committed deterministic synthetic fixture is required for review replay.
- **No R00E gate:** gate implementation was intentionally not used. R02 development used the admitted frozen R00 contract only. Any claim of gate-qualified integration remains NOT_RUN.

## Non-claims

This is not original35 science, not N11/N12, not protected CI, not production adoption, not a full R01/R03 compiler/lowering, not R04 custody, and not a replacement for R02V.
