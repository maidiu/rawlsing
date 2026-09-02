# FFP021 — exact profile-quotient proof

Status: `PASS__EXACT_REVERSIBLE_PROFILE_QUOTIENT_IS_MATHEMATICALLY_EQUIVALENT__JACOBI_GENUINE_SCALE_EXECUTION_STILL_UNPROVED`

This proof concerns computational representation only. It does **not** identify two semantic states as equivalent and does not remove a respondent.

## 1. Setup

Let the frozen respondent count be `N`. For one Core-B side, let there be `K` distinct **exact frozen state-vectors** actually present among those same `N` respondents.

Define:

- `Z` — the `N x K` membership matrix, one `1` per respondent, identifying its exact state-vector profile;
- `m = Z^T 1` — profile multiplicities;
- `M = diag(m)`;
- `Q = Z M^(-1/2)`, so `Q^T Q = I_K`;
- `Delta` — the exact `K x K` Hamming or authorized weighted-Hamming distance matrix between exact profiles;
- `J_N = I_N - 11^T/N`;
- `s = sqrt(m)`;
- `H = I_K - ss^T/N`.

No row of `Z` is discarded. Profile membership retains the governed respondent ID, so expansion is reversible.

## 2. Exact distance preservation

For respondents `i,j` in profiles `a,b`,

`D_N[i,j] = Delta[a,b]`.

This is exact because a profile is defined by equality of the complete frozen state-vector for the side. No state is pooled across profiles.

Therefore the respondent distance matrix is represented exactly by `(Delta, profile_membership)`.

## 3. Exact classical-MDS quotient

The expanded classical-MDS Gram operator is

`B_N = -1/2 J_N Z (Delta ⊙ Delta) Z^T J_N`.

Because `Z = Q M^(1/2)` and `J_N Q = Q H`,

`B_N = Q B_R Q^T`

with

`B_R = -1/2 H M^(1/2) (Delta ⊙ Delta) M^(1/2) H`.

Consequences:

1. every nonzero eigenvalue of `B_N` is a nonzero eigenvalue of `B_R`, with the same multiplicity;
2. if `B_R u = lambda u`, then `Q u` is the expanded respondent eigenvector;
3. a respondent in profile `a` receives MDS coordinate `u[a] * sqrt(lambda) / sqrt(m[a])`;
4. the orthogonal complement of `range(Q)` supplies exactly `N-K` duplicate-point zero eigenvectors, in addition to zero modes already present in `B_R`.

Thus duplicate profiles do not change the positive classical-MDS eigensystem. They only create explicit zero structure.

## 4. Exact respondent-level order reconstruction

For a respondent in source profile `a`:

1. sort target profiles by exact `Delta[a,b]`;
2. for each equal-distance tie group, expand all governed member respondent IDs;
3. exclude the focal respondent from its own zero-distance group;
4. sort member IDs by the frozen respondent-ID tie rule.

The result is exactly the same logical order as sorting all expanded respondent peers by `(distance, respondent_id)`. The first `k` entries are the exact neighborhood. The farthest equal-distance group is the exact metric-opposition peer set.

## 5. Exact stress and sensitivity aggregation

Any sum over unordered respondent pairs can be evaluated without enumerating respondent pairs:

- distinct profiles `a != b` have pair multiplicity `m[a] * m[b]`;
- within-profile zero-distance pairs have multiplicity `m[a] * (m[a]-1)/2`.

Therefore normalized stress and distance-based sensitivity summaries can be accumulated exactly from profile-pair quantities and multiplicities. No pair is sampled.

FFP011's leave-one-respondent-out neighborhood diagnostic does not recompute MDS; it removes one peer from the exact fixed metric order. Its Jaccard distribution is therefore exactly reconstructible from the baseline exact order and respondent membership. Bounded fixture tests cover `k=1`, intermediate `k`, and `k=n-1`.

## 6. Boundary

The quotient proves that respondent-scale `N x N` Python materialization is not part of Core-B semantic meaning.

It does **not** prove that `CLASSICAL_MDS_JACOBI_R1` itself is genuinely executable on the resulting `K x K` operator. FFP021 therefore may not use a successful non-Jacobi eigensolver as a substitute and may not bank genuine Core-B output until the frozen Jacobi coordinate executes or is lawfully revised.
