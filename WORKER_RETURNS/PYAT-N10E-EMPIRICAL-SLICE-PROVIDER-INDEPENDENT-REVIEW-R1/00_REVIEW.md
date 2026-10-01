# PYAT N10E — EMPIRICAL POSSIBILITY-SLICE PROVIDER CORE — INDEPENDENT REVIEW R1

**Disposition:** `CHANGES_REQUIRED`

**Terminal:** `N10E_EMPIRICAL_SLICE_PROVIDER_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`

Reviewed exact return:
`58ba4320635162e8103ed38681ea5ae3e3bac014`

Issued reviewer tip:
`610f949a7646cbdedea770816e245fa58cb6d7e4`

Governing provider commission:
`b631e1c40fc9078cf6473004c28532a99308c5db`

Accepted C1-01 base:
`5fafb499d53dddadaf8a7b4fd46506e91a09d270`

## Bottom line

The N10E provider implementation is structurally sound at the declared R1 grain. It is a seam over the accepted C1-01 analytical composition, not a second empirical calculator. The public provider does not accept handwritten slice evidence or precomputed geometry, the exported low-level evidence helper cannot mint an N10E provider receipt/result, forward and reverse AT07 slices are produced through the accepted path, the receipt identity is non-recursive, fail-closed context checks are inherited without coercion, replay is genuine provider replay, and the authority ceiling correctly excludes AT33, real-source qualification, structural-world admission, actor/person state, smoothing, and new proxy authority.

I am **not** approving the return packet yet because two evidence-integrity defects are material to an independent acceptance review even though neither presently demonstrates a provider-code defect.

### REV-N10E-001 — vacuous P6 changed-source test

`test_p6_geometry_is_recomputed_not_fixed_when_the_empirical_slice_changes` creates `narrowed_rows`, but never rebuilds or passes a repository/query/case from those rows. It simply calls `_provide(case)` again on the unchanged canonical case.

The test passes because the original canonical forward denominator is already 60 and `len(narrowed_rows)` is also 60. Therefore it does **not** prove that geometry changes when the empirical source law changes.

The return packet upgrades this test into executed evidence in `05_HOSTILE_AND_REPLAY_AUDIT.json` (H13), which is unsupported by the test body.

This does not by itself show hardcoded geometry: static inspection independently shows the provider obtains `possibility_slice_evidence_or_null` from `compose_positioned_subject_possibility` and performs no probability arithmetic. P1/P2 also exercise two distinct computed slices. But the claimed H13 proof must be corrected rather than accepted as executed evidence.

### REV-N10E-002 — final execution receipt does not match final pytest output

`06_EXECUTION_RECEIPT.json` records the final court as `88 passed` in **20.01s**, and `00_RETURN.md` repeats that duration.

The committed `08_FINAL_PYTEST_OUTPUT.txt` at the reviewed return ends with:

`88 passed in 19.09s`

The test names and counts otherwise agree: 13 analytical + 32 empirical query + 13 possibility consumer + 30 provider = 88, with no failures/errors/skips.

The executable provenance itself transfers cleanly: `e3bcbbb4faf7ce700828d15899a3a07f7038bc71` is the implementation commit, and the three commits after it through `58ba4320...` modify only return documentation / pytest-output artifacts, not provider/test/fixture/runner files. The final output was recorded after the rebase onto the issued commission tip. No broad rerun is needed to settle current executable ancestry; the packet simply needs one internally consistent final-run record.

### Documentary note — stale commission-tip limitation

`07_FINAL_DISPOSITION.json` still lists as a limitation that commission tip `b631e1c...` “was not obtainable in the local clone” and that work was performed from `5fafb499...`. That is historically true of the worker's earlier phase, but the same final packet later records that credentials became available, the branch was rebased onto `b631e1c...`, and the court was rerun. In a final limitations section the sentence is stale and can mislead provenance readers. This is a documentary correction, not an ancestry failure.

## Independent findings

- **Ancestry / allowlist:** PASS. `58ba4320...` is four commits ahead of `b631e1c...`, behind by zero. The commission-to-return diff contains only the 13 allowed added files; no pre-existing file was modified or deleted.
- **Owner preservation:** PASS. At the reviewed return, `rawlsing_next/pre553_analytical_composition.py` is blob `26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`; `rawlsing_next/source_backed_positioned_subject_possibility.py` is blob `62e5eced47b64512f47b004e3e13a6ef3fe21de7`.
- **Live grounding:** PASS / no mechanical rebase required. Live `integration/pre-main-reconciliation-r1` rechecked at `9a176c9a0a000978a3fc6f1779c9a849315116ca`; it is 130 commits ahead of `b3b2fa13049513078c301a1f6574b661fcf390c5` with zero changed `rawlsing_next/` files in that comparison.
- **Provider seam:** PASS. The provider calls the accepted composition owner and consumes only the composition's generated evidence / consumer result; it contains no local probability calculation.
- **P4 handwritten substitution boundary:** PASS. The main provider signature has no evidence/geometry/probability channel. `evaluate_generated_slice_directly` returns only the already-public consumer result and cannot create an N10E provider receipt/result.
- **P1/P2:** PASS at source-free R1 grain. Forward 54/60 = 9/10 and reverse 54/62 = 27/31 are exercised through the provider and bind denominator/member support, target topology, evidence identity, and consumer identity.
- **P3:** PASS. Conditioner-time and model-rule determinant changes reidentify the provider result; unconsumed authority material does not.
- **Receipt identity:** PASS. `identity_material()` excludes the receipt's own ref/hash and no circular digest remains.
- **P5:** PASS. Source universe, release, target/topology, and model-scope hostile cases fail closed under owner law; no bridge/coercion was found.
- **P6 implementation law:** PASS statically and for the exercised owner paths, subject to correction of the false H13 proof claim. Exact evidence remains exact/unweighted; the real zero-support predicate mutation is stopped by custody before evidence; the provider's non-supported branch emits no evidence/consumer geometry when reached.
- **P7:** PASS. Fresh-process runner reconstructs the fixture, invokes the provider, and compares provider/composition/evidence/consumer identities; it does not merely load a stored expected-output blob.
- **Authority ceiling:** PASS. AT33/full progressive world conditioning, real-source qualification, structural-world admission, actor/person/V3 state, and new smoothing/proxy authority are explicitly not claimed.

## Exact correction required

1. Correct `test_p6_geometry_is_recomputed_not_fixed_when_the_empirical_slice_changes` so it actually changes the empirical input consumed by the provider **or** remove/rename the unsupported H13 claim and stop presenting that test as changed-source evidence.
2. Make `00_RETURN.md`, `06_EXECUTION_RECEIPT.json`, and `08_FINAL_PYTEST_OUTPUT.txt` identify one consistent final run (including duration).
3. Rewrite the stale commission-tip limitation in `07_FINAL_DISPOSITION.json` as historical pre-rebase context, not a current final limitation.
4. If the provider test file is changed, run the exact commissioned four-file court once on the corrected branch and replace the final execution receipt/output consistently. If only documentary claims are corrected and the executable test file is not changed, no ceremonial re-execution is required.

No provider implementation change is required by this review's present evidence.

**Terminal:** `N10E_EMPIRICAL_SLICE_PROVIDER_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
