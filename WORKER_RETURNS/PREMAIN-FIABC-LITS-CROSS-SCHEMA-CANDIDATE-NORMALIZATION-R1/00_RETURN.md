# FIABC LiTS Cross-Schema Logical Candidate Normalization — R1

## Disposition

**PASS — source-free repair qualified; independent acceptance still required.**

Exact audit base:

`b5737718cc2d3fd4eb5d3737c99fa7de0341e651`

Exact semantic implementation head:

`1882662f861e93e33bb956e015b984458074e9bc`

Exact qualification-binding branch tip:

`2b328a6451305bdcb49273bd12bdacf408fbcf82`

GitHub bounded court:

- run: `35889692534`
- job: `107278727156`
- protocol self-check: **20 passed**
- governed source-free court: **100 passed**
- conclusion: **success**

## Closed blocker

The prior direct cross-schema equality gate between historical G02 `execution_candidate_hash` and current PRE553 I05 candidate hash has been removed from parity law.

The repair introduces a third identity:

`CROSS_SCHEMA_LOGICAL_CANDIDATE_KEY`

derived independently from historical G02 candidate semantics and the actual current PRE553 compiled frontier.

Historical G02 and current PRE553 native hashes remain distinct provenance identities and are independently verified from their native preimages.

## Exact frontier proof

The current PRE553 materializer compiles the real frozen 50-candidate / 77-role frontier and emits 50 unique logical bindings.

Historical ASTRA/G02 candidate semantics independently yield the same 50 logical keys.

All 50 native provenance identities are preserved. P0-P3 historical native G02 hashes are recomputed from the immutable G02 preimage; PRE553 native hashes for all 50 candidates are recomputed from current PRE553 candidate preimages.

## P2

All 18 P2 logical candidates bind exact:

- `q301_2`;
- `q310`;
- `q311`;
- CONDITION predicate ref;
- CONDITION query ref;
- BASELINE predicate ref;
- BASELINE query ref.

Hostile tests hold empirical witnesses fixed while mutating parameters or exact refs and require fail-closed behavior.

## WVS7 conservation

Source-free regression confirms the accepted WVS7 successor stream remains:

`{"COVERAGE_LIMITED":46}`

with accepted successor Lock2, DiscoveryAuthority, oracle and truth identities conserved and zero candidate processes / outputs.

## Prohibited activity

No raw LiTS/WVS source was opened or decoded. No real-source I05 was run. No Candidate A/B/C, measured P2X, P3, architecture selection, or governed execution-branch mutation occurred. The banked LiTS checkpoint/oracle was not consumed or altered.

## Terminal

`PREMAIN_FIABC_LITS_CROSS_SCHEMA_CANDIDATE_NORMALIZATION_R1__G02_AND_PRE553_NATIVE_HASH_DOMAINS_SEPARATE__CROSS_SCHEMA_LOGICAL_CANDIDATE_KEY_EXACT__P2_PARAMETER_CONDITION_BASELINE_IDENTITY_CONSERVED__REAL_CURRENT_PRE553_FRONTIER_PROVEN__WVS7_CONSERVED__SOURCE_FREE_GREEN__NO_CANDIDATES_RUN`
