# PAIRWISE FAILURE ORACLE

A complete learned world for this fixture cannot be recovered from global marginals, one flat determinicity score, or pairwise-only association.

## 1. Multi-label presence marginals are non-identifying

Actual pattern morphology:

`A+B=24, A_ONLY=14, B_ONLY=6, NONE=4`.

Presence marginals:

`A_present=38, B_present=30`.

A different morphology:

`A+B=22, A_ONLY=16, B_ONLY=8, NONE=2`

has the same presence marginals. Therefore presence-only branching erases exact response-pattern structure.

## 2. K-way XOR is pairwise invisible

For each of `XOR_A:XOR_B`, `XOR_A:XOR_C`, and `XOR_B:XOR_C`, the table is:

`00=12, 01=12, 10=12, 11=12`.

Each pairwise phi is exactly 0.

But the three-way law is exact:

`XOR_C = XOR_A XOR XOR_B`.

Only `000,011,101,110` occur. Pairwise null does not imply higher-order independence.

## 3. Global co-signature reverses the branch truth

For same respondents globally, C1/C2 phi is `-0.75`.

Inside the discovered P+not-M -> Q=1 branch, C1/C2 phi is `+1.0`.

Thus `PAIRWISE_ASSOCIATION != COMPLETE_BRANCH_COSIGNATURE_TOPOLOGY`. A global pairwise summary would erase the branch-local cotravel required by Authority 35.

## Acceptance consequence

Any harness that returns a single global pairwise graph, response-presence marginals, or one determinicity scalar while omitting these branch-conditioned and K-way structures fails this oracle.
