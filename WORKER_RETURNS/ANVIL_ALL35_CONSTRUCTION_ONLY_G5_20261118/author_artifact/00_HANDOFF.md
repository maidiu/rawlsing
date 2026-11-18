# Construction-only C11 candidate — native-child proof repair

## Result

**PASS — evidence repaired only; candidate production code unchanged from the frozen first patch.**

- Exact accepted baseline: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- Frozen first candidate: `2b139250eae19a04ce2778f7db9f2d2b025071a8`
- First patch (preserved): `candidate_original_9da2a368.patch`
- Final scratch commit: `9a2d5bc4d9e41ba5a4e02042f02ce9d33bbc6c6e`
- Final patch: `candidate.patch`; applies cleanly to `aee954` (`git apply --check` exit 0).
- Final patch includes the unchanged production refactor plus the repaired focused test and native child harness.

## Evidence gap repaired

The first test reopened in the producer pytest process with an unconditional
`current_authorizer=lambda _roots: True`. The repaired focused test now follows
the `b7acf7aacd6abe3fdc9e4c5a968fc2e71e6e4570` pattern:

1. A separate native producer child performs exactly one tiny sourcefree
   construction and exits.
2. The pytest parent waits for and reaps it.
3. A separate fresh native reader child checks the producer PID is gone, then
   opens `VerifiedDirectEstate` with the exact held-root callback
   (`current(roots) = roots == held_i02`).
4. Positive cold reopen compares every family count and canonical object
   payload digest, including full `RespondentIdentity` and
   `RoutingEligibilityFact` payloads, against the producer's recorded exact
   bodies; it also proves roots, manifest and source metadata are exact.
5. Negative children prove exact wrong-current and revoked refusal before estate
   open. A wrong-root child also refuses with the exact held-root mismatch.

The original-mode pre-read denial test is retained. The existing governed Q2
source-i02 regression court is retained.

## Native evidence

- `proof/build.json`: producer child PID, exact roots/manifest, all family
  counts, producer payload digests, source metadata, unresolved Q2/issuance
  states, and absence of operation/census fields.
- `proof/reopen_positive.json`: producer exited first; all family payloads,
  identity and routing payloads equal; roots/manifest equal.
- `proof/refusal_wrong_current.json`: `current source/operation authority refused`.
- `proof/refusal_revoked.json`: `current source/operation authority refused`.
- `proof/refusal_wrong_root.json`: `estate source/replay/universe/logical/physical roots mismatch`.
- `proof/producer_exit_probe.txt` and `proof/APPLY_CHECK.txt`.
- `tests_native_child.txt`: focused test **2 passed in 9.27 s**.
- `tests.txt`: focused candidate + existing Q2 regression court **13 passed in 10.38 s**.

No original source was opened, hashed, decoded or statted. No new grant,
protected write, product edit, benchmark, config join or separate experimental
matrix was created. The production handoff refactor is unchanged from the frozen
first candidate; this repair is confined to focused proof/evidence.
