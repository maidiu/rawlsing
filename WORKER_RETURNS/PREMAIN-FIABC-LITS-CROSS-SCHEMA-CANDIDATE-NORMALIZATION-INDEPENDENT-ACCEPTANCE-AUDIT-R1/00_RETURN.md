# FIABC LiTS Cross-Schema Candidate Normalization — Independent Acceptance Audit R1

## Holding

**ACCEPTED.**

Subject worker return:

`fddb356c69d2bcaf64351869aecbb9cec66dd36f`

Blocking audit base:

`b5737718cc2d3fd4eb5d3737c99fa7de0341e651`

Qualified semantic implementation:

`1882662f861e93e33bb956e015b984458074e9bc`

Independent audit source-free court:

- successful run: `35891886613`
- job: `107286105997`
- protocol self-check: **20 passed**
- independent governed court: **106 passed**
- conclusion: **success**

The first independent run `35891524452` failed only because the Actions checkout was shallow and the audit-specific `git merge-base` / `git diff` assertions had not fetched the exact historical commits. That audit-harness defect was repaired by explicitly fetching the immutable worker base/implementation/return commits. No worker production code changed. The rerun passed all 106 tests.

## Accepted law

- Historical G02 and current PRE553 native candidate hashes remain distinct provenance domains.
- Neither native hash domain is equality-gated against the other.
- `CROSS_SCHEMA_LOGICAL_CANDIDATE_KEY` is the shared comparison identity.
- The exact logical frontier is 50 unique candidates: 5/1/18/1/25.
- All 50 current PRE553 native identities are independently verified from exact PRE553 preimages.
- Historical P0-P3 G02 native identities are independently verified from immutable G02 preimages.
- P2 conserves exact `q301_2/q310/q311` and exact current CONDITION/BASELINE predicate/query refs.
- Hostile mutation, hash injection, key collision, role-ref drift, selector drift, empirical witness drift, and freeze-order regressions fail closed.
- WVS7 remains exactly conserved at `{"COVERAGE_LIMITED":46}` with accepted successor Lock2, DiscoveryAuthority, oracle and truth identities.

## Checkpoint boundary

This acceptance does **not** yet certify the banked LiTS checkpoint/oracle under the repaired parity law. The banked source-backed evidence remains downstream retained evidence pending a separate checkpoint-consumption/finalization court.

No source bytes were opened, no real-source I05 ran, no Candidate A/B/C, measured P2X, P3, architecture selection, or governed execution-branch mutation occurred.

Terminal:

`PREMAIN_FIABC_LITS_CROSS_SCHEMA_CANDIDATE_NORMALIZATION_INDEPENDENT_ACCEPTANCE_AUDIT_R1__ACCEPTED__106_SOURCE_FREE_TESTS_GREEN__WVS7_CONSERVED__CHECKPOINT_CONSUMPTION_REMAINS_SEPARATE__NO_CANDIDATES_RUN`
