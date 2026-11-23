# Mandatory source-recovery method, proof ceilings and finite stop

## The user's specific recovery rule
When an old/current operation is **posited to exist somewhere in the repository** but the expected `path@commit` cannot be retrieved, do not pronounce it nonexistent. **Search the wider repository, relevant historical commits, branches, PRs and archived worker candidate trees until the actual material is located or a bounded, reproducible search is exhausted.** Then log exact recovered location, or enough neighboring clues that the next competent investigator can continue efficiently.

This is **commissioned substantive source archaeology**. The user-supplied pre-work primer's "no ambient broad archaeology" rule applies only to *preliminary grounding*, not to the substantive task of recovering missing source.

### Source-location algorithm
1. **Capture the assertion, not just the failure:** claimed symbol/module/output, expected `path@commit`, source generation, assertion origin, relevant manuscript/PR, intended input→output effect and first reader. Record exact 404/empty-index query result as one bounded negative lookup only.
2. **Search same-cut full repository tree:** recursively enumerate tracked files with `git ls-tree -r <sha>` or equivalent authenticated Git tree, not just a restricted indexed search; basename/stem/snake-to-camel variants, likely `data/ddm_build_copy/`, `rawlsing_next/`, `candidate/rawlsing_next/`, `WORKER_RETURNS/`, `WORKER_COMMISSIONS/`, archive and historical branch directories.
3. **Search by semantics, not only filename:** exact function/class/constant, distinctive output columns/status/exception, emitted parquet/JSON/table basename, known importer/callsite, positive/negative text, source registry/manifest, prior reviewer/source receipt.
4. **Search relevant other source cuts:** `git log --all -- <path>`, commit/PR/branch history and trees, versioned candidate source bundles and predecessor/descendant writers. Make the search finite and source-targeted; don't scan everything endlessly without a hypothesis. Check whether an apparent relocated file has identical Git blob, a modified implementation, or only similar name.
5. **Inspect recovered content and role:** exact `commit::path#blob:line-range`, source year/generation, whether ancestor/candidate/protected, actual input/output/guards/negative semantics, named producer and named importing first consumer, whether it is still in a current reachable chain. A candidate found on a 2026 branch MUST NOT be relabeled historical operational at an earlier commit or current adopted just because its name matches.
6. **Record in R1:** `SOURCE_SEARCH_LOG.tsv` with all positive/negative bounded queries and search boundary; `EVIDENCE.tsv` claim+SHA+blob+lines; relevant `OPERATION_TRACES.tsv`, `UNJOINS.tsv`, `COVERAGE.tsv` and case narrative. Preserve failed expected locator and corrected locator both, rather than erasing the original mistaken assertion.
7. **If still not found:** `UNRESOLVED_LOCATOR_AT_DECLARED_SEARCH_SCOPE`, not `FUNCTION_ABSENT`. Record nearest related code and consumer, known era, earliest/later dated citation or creation evidence, likely commit range/branch/worker packet, alternate names/output artifacts, permission/access limits, and the smallest concrete next search. Mark NOT_FOUND only when truly bounded exact asset search supports that *scoped* finding. Never infer machine-wide absence from search failure.

### Verified demonstration: F6M misleading expected location
The path `rawlsing_next/pre553_heterogeneous_synthesis.py` at an asserted earlier historical cut may fail. It was **actually retrieved** at:
`1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa::WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py#2df811d76db258d98d89ffb43c830cb221ff9a7d` (symbol `synthesize`, near L186).

This is a **candidate/sourcefree** artifact, not proof that that exact file or code existed at a previous historical SHA, or that the protected current N9 is executing its numeric partial-identification calculation. Preserve historical cut lineage and source rights separately. A named current composition guard is not equivalent to numeric synthesis. The R39 sourcefree F6P reader is another distinct consumer and needs its own real-source/sourcefree proof grade.

### Another demonstration: Sorok file expected at root
A missing repository-root `p3/`, `p5/`, or `p6/` does not mean absent Sorok behavior. Search actual `WORKER_RETURNS/SOROK-...` directories, owner branches and their first readers. Report exact code or document copy and whether it is sourcefree implementation, test only, adopted source or actor-native, instead of falsely promoting any local fixture into psychology.

## Proof and future-use grades
For each material old/current edge keep five independent values:
- `SOURCE`: immutable code/documentary identified / branch candidate / protected / not found within specified source.
- `EXECUTION`: NOT_RUN / separately witnessed test-only receipt / source-native if independently evidenced; this commission never runs a new pipeline.
- `SEMANTIC`: old/new exact T + S/M invariants, differing input/data/denominators/rules/statuses and refusals.
- `CONSUMER`: named interface / actual static importer / observed bounded test reader / actual qualified non-test first reader; do not count physical writer as scientific reader.
- `AUTHORITY`: available / selected / actually applied / negative enforced / competent issuer and rights granted; historical line of code can't issue current source/science/actor permission.

`SOURCE_RETAINED`, `FOUND_CANDIDATE`, `STATIC_READER`, `TEST_ONLY`, `OPEN_PROOF_GAP`, `OPEN_FUNCTIONAL_GAP`, `PARTIAL`, `SUPERSEDED`, `PURPOSEFUL_RETIREMENT` must not be conflated.

If no equivalent is found, investigate plausible composed/current alternatives. A specific old calculation absent in the inspected modern guard can be `NUMERIC_FUNCTION_UNPROVED_AT_THIS_INTERFACE`, not `GLOBALLY_LOST`. Recommend a separate future engineering/scientific investigation with smallest falsifier; do not implement it.

## Honest completion at finite bounded scope
A worker can truthfully finish a finite historical/source stratum with open global T discovery **if**:
- enumerated source estate actually searched or exact holds;
- old/modern T/S/M data journey and actual readers or first-reader holds recorded, including relevant negatives;
- at least one original-function omitted-class search and current-first reverse-consumer source search;
- aliases and upstream/downstream owner handoffs complete;
- source/branch status, R1 referential integrity, counterevidence and future utility documented;
- no remaining **accessible, materially relevant unsought lead inside that declared tract**. Outside/new strata become explicit queue items.

A campaign cannot declare global function conservation or scientific native completeness merely because every allocated source stratum is documented: distinct authorized original-native S2/scientific/actor/issuer work remains for separate future commissions. A qualified independent reviewer challenges the documentary boundaries once per material tranche rather than once per one-line correction.

## Source-first method > ledger theater
Remember: the purpose is preserving and understanding historically valuable empirical and computational knowledge, not maximizing rows, proving a PR has many files, or reimplementing old functions. Every extra source search and case must answer something materially new or close a bounded known unknown.
