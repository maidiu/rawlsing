# J02 — UNIVERSAL EMPIRICAL SOURCE-STATE TO PRODUCT TARGET-DISPOSITION CONTRACT R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w8-j02-source-state-target-disposition-r1`

Commission parent: `4d511efe214a6810625e00d15b1e4689c027b94f`

Execute only:
`PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1_ONLY`

Library: `NO`

## Mission

Solve the general defect class exposed by I02 across coded empirical sources without hard-coding LiTS, q301, or any numeric source code.

Freeze a source-agnostic authority/execution contract for:

`RAW_SOURCE_STATE -> SOURCE_LOCAL_GOVERNED_STATE -> PRODUCT_TARGET_DISPOSITION -> DENOMINATOR_RESOLUTION_CHECK -> EMPIRICAL_RESULT`

The universal layer must never assign semantic meaning from a raw numeric/string code alone. It must consume content-addressed source-local semantic authority plus product/query target-domain authority.

At minimum adjudicate the typed disposition space required to distinguish, where competent authority exists:
- mapped substantive target member;
- resolved substantive state outside the requested target set, if product law permits such a resolved non-target state;
- typed missing/nonresponse state;
- not-applicable / structurally ineligible state;
- authorized denominator exclusion with explicit pre-query eligibility authority;
- unresolved source-specific special / unknown disposition.

Do not assume all of those classes are admissible. Derive the minimum lawful type system from accepted PRE553/I03 and source-authority law; if a class requires new authority that is unavailable, record it as an exact blocker rather than inventing it.

The contract must explicitly govern:
- denominator membership vs target membership;
- whether/when a non-target state can still count as `resolved`;
- when exclusion changes the denominator and what prior authority is required;
- prohibition on post-data denominator deletion, recoding, target expansion, or semantic substitution;
- complete accounting of every denominator member;
- deterministic provenance/replay identity for source-state and target-disposition bindings;
- fail-closed `UNRESOLVED` when no competent disposition exists.

Use the I02 LiTS q301 failure only as a hostile proving pattern. Do not decide what q301 codes 6/7 mean and do not write LiTS-specific branches in production logic.

## Implementation scope

You may implement a reusable candidate contract/schema/execution helper and targeted source-agnostic tests if needed. Any implementation remains producer/self-tested only unless separately qualified later.

## Hard prohibitions

No source-specific code tables.
No inference that `6`, `7`, `-1`, `99`, etc. have universal meanings.
No survey-family assumptions.
No post-outcome repair.
No structural/causal/person-state promotion.
No PRE-V3/V3 boundary weakening.
No OBL063 revival.

## PASS law

PASS requires a reusable source-agnostic contract with explicit authority inputs, typed resolution states, denominator accounting law, deterministic identity/replay law, and hostile tests showing unknown/unmapped source states fail closed.

If accepted authority is insufficient to define the reusable contract, return the smallest exact owner/semantic blocker.

## Return

Commit `00_RETURN.md`, exact contract/schema artifacts, any implementation/tests, and report their Git blobs plus successor gate for reconciliation with a separate source-local semantic authority lane.
