# Acceptance gates

The implementation is accepted only when every gate passes.

## A. Authority preservation

- R184 artifacts unchanged byte-for-byte.
- Section 85 authority files unchanged byte-for-byte unless only documentation is updated.
- No new response portability authorization.
- No new production-completeness claim.

## B. Base fixture preservation

- Ordinary V550 base question selection is unchanged.
- Joint-only extraction items do not appear in ordinary V550 question outputs.
- Legacy V550 outputs for a controlled base fixture are hash-equivalent after excluding allowed audit/manifest additions.

## C. One-query contract

Fresh synthetic run:

- one respondent-data query per country;
- zero V550J respondent-data queries;
- union query includes every base and joint-required item exactly once at the selection level.

Resume/rerun:

- zero respondent-data queries when an exact complete substrate is supplied.

## D. Substrate integrity

- required columns complete;
- no substantive row lacks normalized respondent, variable, or response identity;
- source/wave/country exact;
- selection set equations exact;
- schema and logical hashes match after reload;
- stale authority or response hashes reject reuse;
- incomplete writes reject reuse;
- no CSV respondent artifact exists.

## E. V550J no-DB execution

- explicit substrate path accepted;
- `prepared_required` used;
- database connection functions are not called;
- registry applicability exact;
- missing joint item fails closed;
- V550J output passes its existing validator.

## F. Resume and recovery

- checkpoint-only V550 finalization uses local artifacts;
- V550J rerun uses local substrate;
- bridge/cloud recovery uses local substrate where respondent state is required;
- any legacy DB reload is explicitly labeled non-promotable.

## G. Mutation rejection

Every mutation listed in the matrix must fail for the expected reason and leave no promoted/complete artifact.

## H. Downstream structural canary

Tiny synthetic chain passes:

```text
V550 → V550J → V551J → V552J
```

No real respondent data and no full-wave production output are generated.

## I. Package portability

From a fresh extraction:

- package hashes pass;
- Git bundle clones at expected commit;
- worktree clean;
- Section 85 reproduction passes;
- Section 86 documentation manifest passes;
- synthetic implementation tests pass;
- no respondent substrate is present in the package.
