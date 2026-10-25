# R109 independent review — R107 R06/C8 progressive world integration

**Verdict: `REVISE`.** The declared sourcefree positive is real and the author
suite passes 23/23, but the candidate does not bind the governed world identity
to the producer prefixes, silently serves an empirically revoked world, and its
N10W positioned consumption is a cached placeholder rather than an actual N10E
binding. The required reusable operation class is therefore not independently
qualified as delivered.

## Exact identity

- R109 commission: `40b784671f555cd716a3afe9b86318a1dc99d66c`.
- Candidate: `22280a3f43e751bab1bbebe0a9d8c601b3160120`; code
  `98f9d136176af856185eb9fa7ac8e08afeb2deeb`.
- Accepted baseline: `b2cfe93cee854b7aff2081a7a223ada75295332a`.
- Inherited R107 commission: `2b50b54de`; R107 contract
  `bb4ad106af69eae197251d8c0d54f7162901fd5e`.
- Prior R06 review: `fbe7ffc00a021aeacce3b15a2ef74cd8657d9d56`.
- P41 packet: `f27d1101048638bba395143a48efb7ef00bfcda4`.
- Reviewer branch:
  `agent/opencode-pyat-r109-r06-progressive-independent-review-r1`; writes only
  `WORKER_RETURNS/PYAT-R109-R06-PROGRESSIVE-INDEPENDENT-REVIEW-R1/`.
- First TOOL gate passed at the exact worktree/branch/HEAD; only generated
  untracked runtime material existed. The frozen oracle is `ORACLE.md`,
  committed at `095fac4e8` before candidate code inspection.
- Candidate code blobs:
  `pre553_universal_world_binding.py` `c6d33e4780b61668bf7fbbc2b82aec31a9144a0d`;
  `test_universal_world_binding.py` `4d5a7d93b482482562ff3065acd8f2208652db0a`.
  Only the two R06 code paths changed from baseline (plus the author contract).

## Independent results

| Suite | Result | Evidence |
|---|---|---|
| Author R107 suite | 23 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| R109 independent probes | 3 passed, 3 failed | `replay/independent_probes_junit.xml`, `.log` |
| Cold fresh-process replay | pass, matching view/receipt/routes | `replay/cold_replay.log` |

Positive witnesses (passing):

- Actual producer prefixes: base target Y / X=1 then O=AB gives denominator
  40 then 30, cells 10/30 then 0/30; observed zero and minority retained.
- Condition VALUE mutation X=0 / O=AB changes actual denominators to 40/20,
  actual cells, and N10W update identities; not a variable rename.
- Semantically unlike target `X` with conditions `Y=1,O=BA` returns a selected
  view with two steps and a distinct view hash.
- T0/T1 actual E04 routes change
  (`ELIGIBLE/WITHIN_MODELED_BUDGET` -> `BLOCKED_BY_MODELED_RULE/RESOURCE_CONSTRAINED`);
  world `training_access` revocation returns typed unavailable and a clean
  context restores.
- Actual N10E steps and N10W update identities are present; `actor_state` is
  `NOT_TOUCHED`; cold replay matches `fb4b1710…4850` / receipt `8be29670…d28a`.

## Blocking findings

### 1. World source/release identity is not bound to producer prefixes

`configure_progressive_world_context` validates target/order and non-null prefix
release, but never compares `world_empirical["source"]["universe"].ref`,
`world_empirical["release_ref"]`, source risk/rows or source release with the
prefix consumer/query identities, nor checks that all prefixes share one
source/release. The candidate's own `world_dependency_graph.json` claims
`same_source_world_empirical_identity: true`.

Witness: take `_progressive_fixture_parts()`, replace the world release with
`C11LogicalRelease REL-r109-foreign` (and its source release), call
`configure_progressive_world_context`, then `progressive_world_view` for T0.
The candidate returns `PROGRESSIVE_WORLD_SELECTED_VIEW` and concrete E04 routes
instead of a typed source/release refusal.

Minimal fix: in `configure_progressive_world_context`, derive the expected
universe/release/risk identity from the prefixes (and require all prefixes to
agree) and compare the world source/release/risk/rows hash before registering
the context; refuse mismatch. No new architecture or engine.

### 2. Empirical permission revocation is ignored

`revoked_scope="empirical"` is a valid `SelectedWorldCatalog` revocation scope,
but `_progressive_world_receipt` reads only field structural values through
`StructuralService`; `_world_block` does not include the snapshot's empirical
state. A revoked empirical scope therefore still serves
`PROGRESSIVE_WORLD_SELECTED_VIEW` with the same routes and progress.

Witness: `_progressive_fixture(revoked_scope="empirical")`, T1/AS_OF returns
`PROGRESSIVE_WORLD_SELECTED_VIEW`; `n9_world` has no empirical state. Expected
a typed unavailable/refused result. The same test for `training_access`
correctly returns `PROGRESSIVE_WORLD_UNAVAILABLE`.

Minimal fix: propagate the selected snapshot empirical state/permission into
`n9_world` and the view availability check, or refuse before serving when the
empirical scope is revoked. Preserve the existing field revocation/restore
behavior.

### 3. N10W positioned consumption is not bound to actual N10E results

`ProgressiveProvider.progressive` appends only
`R107_PRODUCER_PREFIXES_CONSUMED`; the actual pinned P41 code looks for
`call == "evaluate_positioned_subject_possibility"` to build
`n10w.positioned_consumptions`. Consequently every positioned entry is
`CACHED_PRODUCTION_CONSUMPTION` with `consumer_result_hash: null`, while the
actual `n10e_steps` carry real content hashes. The receipt therefore has a
N10W trace that is not bound to the producer-computed slices.

Witness: the base positive has two N10E step hashes but both positioned
consumptions have null consumer hashes. Expected actual consumer result hashes
matching the N10E step content hashes, or an explicit typed non-qualification
instead of an `ACTUAL_N9_N10E_N10W` selected view.

Minimal fix: emit the actual `evaluate_positioned_subject_possibility` trace
entries (or use the actual E03 provider) so N10W positioned consumptions bind
the N10E/consumer result hashes; add a positive assertion for that binding.

### Additional scope gap (non-primary)

T0/T1 world changes alter `world_routes` and `n9_world`, but
`n10w.progressive_update_identity`, `positioned_consumptions` and `alternatives`
are byte-identical; the world dependency is a sibling N9 eligibility block, not
an N10W value dependency. This is consistent with a declared N9-route scope but
does not independently demonstrate the R107 claim that N10W itself consumes
world content. If the required N10W assertion must include world refs/effect,
this needs the same repair as finding 3 plus a world-binding assertion; if not,
record the limitation explicitly rather than claiming N10W world consumption.

## Preserved positives and authority

- Actual producer/composition values are not handwritten final probabilities;
  the author suite and independent probes show real denominator/cell and
  condition-value changes, minority/zero/uncertainty retention, two target
  shapes, cold replay, and field-revocation/restore.
- P41 runtime is pinned; the candidate does not expose a caller runtime there.
  The author suite retains the prior R06 17-test owner/boundary controls.
- No actor state, person generation, route probability, dyad/cross-unit pooling,
  original source/science, F5/F6/F7/F8, CI/prod, N11/N12, Sorok or J52/W52
  claim. Original 35/1890/global obligations remain held.
- No candidate repair, self-adoption, new worker/provider or replacement
  engine was performed by the reviewer.

## Limits / NOT_REACHED

Sourcefree TEST_ONLY finite-shape release, not original source measurement.
Missing-cell/low-support behavior was not independently exercised beyond the
author fixture's observed zero/minority; full required world-family closure,
selective full-estate invalidation, original temporal pairs, actor realization
and production adoption remain held. The fixed T0/T1 calendar pair is a declared
sourcefree scope limitation, not an original temporal claim.

## Artifacts

`ORACLE.md`, this review, `COVERAGE_AND_LIMITS.md`, `RESUME.md`, `probes/`,
`replay/` (JUnit/logs/cold), `evidence/commands.txt`,
`evidence/remote_readback.txt`, `proof_witness.json`, and self-excluding
`manifest.json` with SHA256 and byte sizes. The reviewer branch was pushed non-force. Evidence commit
`860c36b987c0f7f868c4cbcd0f562a683cb63132` was directly read back at the
remote, as recorded in `evidence/remote_readback.txt`; the final branch tip is
also directly verified and reported to the coordinator.
