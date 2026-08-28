# G05 — Current Discovery Control Flow

Status: \`AUDIT_ONLY__NO_IMPLEMENTATION\`

## Current exact I05

\`\`\`text
CALLER / GOVERNED AUTHORITY
  |
  | supplies:
  | - DiscoveryAuthority
  | - exact candidate_universe_definition
  | - exact predicate_catalog
  | - exact query_template_catalog
  | - source/release refs
  v
_verify_discovery_authority
  |
  | requires EXACT_BOUNDED_AUTHORIZED
  | requires COMPLETE_FOR_EXACT_DECLARED_FRONTIER
  | rejects adaptive/exploratory mode
  | rejects ranking/pruning that controls frontier
  v
_catalog_atoms + _catalog_templates
  |
  | resolves only declared exact predicate/query refs
  v
_compile_frontier
  |
  | expands only declared rules/pools/forms
  | completes before first I03 query
  v
FIXED CANDIDATE FRONTIER
  |
  +--> candidate 1 -> _evaluate_candidate -> typed result/facts
  +--> candidate 2 -> _evaluate_candidate -> typed result/facts
  +--> ...
  +--> candidate N -> _evaluate_candidate -> typed result/facts
  |
  | every candidate gets terminal coverage
  v
DiscoveryResultReceipt[]
  |
  | exact refs + support + ancestry + replay
  v
ExactBoundedDiscoveryResult
\`\`\`

Binding negative fact:

\`\`\`text
EMPIRICAL RESULT
   X
   | no current feedback edge
   v
NEW ATOM / NEW QUERY TEMPLATE / NEW RULE / NEW FRONTIER MEMBER
\`\`\`

Results affect validation outcomes only. They do not alter frontier reachability.

## What _compile_frontier can do

It can mechanically generate declared combinations:

\`\`\`text
declared atom pool
 + declared baseline
 + declared query template
 + declared family/form
 + declared validation
     |
     v
combination / cartesian / XOR / joint / reversal expansion
     |
     v
candidate identities
\`\`\`

That is lawful grammar expansion.

It is not a controller that asks:

- which coordinate should become a predictor;
- which response state is modal;
- which nonmodal group is a meaningful minority;
- what residual group remains;
- which supported child should become the next parent;
- which other question should be queried inside that branch.

## Caller-knowledge path in current tests

Representative recursive fixture:

\`\`\`text
test fixture
  |
  +--> constructs parent branch membership R1/R2/R3
  +--> constructs H1 child predictor
  +--> constructs target query Y
  +--> declares RECURSIVE_SUBGROUP_FORK rule
  v
I05 evaluator
  |
  +--> validates child
  +--> preserves ancestry
\`\`\`

This proves exact evaluation, not autonomous discovery of parent/child search direction.

## Accepted MX01 R2 handoff

Authority 34 adds a distinct accepted seam:

\`\`\`text
I05 discovered child receipt
   |
   v
resolve exact compiled child predicate
   |
   v
persist DiscoveryBranchReplayBinding + exact membership/replay
   |
   v
fresh process
   |
   v
N+1 role-bearing parent
   |
   v
declared next-generation I05 evaluation
\`\`\`

Positive theorem:

\`DISCOVERED_CHILD -> PERSISTED EXACT CHILD -> N+1 ROLE-BEARING PARENT\`

Still absent:

\`\`\`text
supported child results
   |
   X  no current controller law chooses/generates next search
   v
new secondary predictor / new other-question target / new residual branch rule
\`\`\`

## Current I07

\`\`\`text
SourceUniverseRelation + exact AuthoritySnapshot
   |
   v
SourceRelationResolver / operation guard
   |
   v
authorized or blocked source composition/query relation
\`\`\`

I07 protects source plurality and \`NO_IMPLICIT_POOLING\`. It is not a discovery controller.

## Historical I08 only

At historical ref \`686b511...\`:

\`\`\`text
accepted I05 candidate grammar
   |
   v
_compile_frontier
   |
   v
fixed remaining candidates
   |
   +<----------------------------------+
   |                                   |
 choose_next                           |
   | canonical/seeded/diagnostic/      |
   | supported-family priority         |
   v                                   |
 evaluate one candidate                |
   |                                   |
 update support state -----------------+
   |
 stop on exhaustion / budget / supported-count
\`\`\`

Historical I08 can make later **ordering** depend on earlier results. It still cannot create a candidate outside the precompiled grammar, and its contract expressly rejects diagnostic-driven semantic widening.

That historical branch is not in the current worker lineage.
