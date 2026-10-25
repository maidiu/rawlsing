# R111 independent review — three R110 binding repairs

**Scoped verdict: `REVISE` repair 1; scoped accept repairs 2 and 3. Whole
R107/R06 remains incomplete because the fourth world-value→N10W gap is held.**

The candidate accurately stops and reports the fourth P41 world-value gap, and
the empirical-revocation and actual N10E→N10W positioned repairs hold under
independent replay. The world/prefix identity repair is incomplete: world
`rows_hash` agreement is never checked, a world source repository can be
omitted, and mixed-prefix repository identity is not checked. Those mismatches
still serve a concrete `PROGRESSIVE_WORLD_SELECTED_VIEW`.

## Exact identity

- R111 commission: `ac6a26809d8cb94cf806d15936f68a96cacd29c6`.
- R110 candidate: `359ffcef4c2dbde0bea7233bdb8901e8ed28e9be`; code
  `b6acb241366b1a940c613a779037f97351bd0d85`.
- R110 baseline: `22280a3f43e751bab1bbebe0a9d8c601b3160120`; contract
  `53981ac013755407ebf7de88f894add2f1dc2858`.
- Prior R109 review/oracle:
  `e38a6a8c07ea6535a0d4de38053c15e4278934d7`.
- R107 contract `bb4ad106af69eae197251d8c0d54f7162901fd5e`; P41
  `f27d1101048638bba395143a48efb7ef00bfcda4`.
- Reviewer branch:
  `agent/opencode-pyat-r111-r06-binding-repair-review-r1`; writes only
  `WORKER_RETURNS/PYAT-R111-R06-BINDING-REPAIR-REVIEW-R1/`.
- Gate passed at exact cwd/branch/HEAD; only generated untracked runtime
  material. Oracle frozen at `ef3cf0167` before successor code inspection.
- Candidate code blobs:
  `pre553_universal_world_binding.py` `fe167820246ace0881d33870442064f85a04da10`;
  `test_universal_world_binding.py` `f78b983b514f1a0a78bf16c5f05ddc2adfaf2bc8`.
  Only the two R06 code paths changed from baseline (plus the author contract).

## Independent results

| Suite | Result | Evidence |
|---|---|---|
| Author R110 suite | 26 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Exact R109 probe replay | 6 passed | `replay/r109_probes_junit.xml`, `.log` |
| R111 successor controls | 2 passed, 3 failed | `replay/successor_junit.xml`, `.log` |

### Repairs 2 and 3 — verified

- **Empirical revocation/currentness:** `revoked_scope="empirical"` returns
  `PROGRESSIVE_WORLD_UNAVAILABLE` / `WORLD_EMPIRICAL_REVOKED_OR_UNAVAILABLE`,
  carries `n9_world.empirical.state="REVOKED"`, and a clean context restores.
  R109 empirical-revocation probe and field-revocation/restore pass.
- **Actual N10E→N10W binding:** `_progressive_step` calls the actual
  `evaluate_positioned_subject_possibility` on the actual composition evidence
  and requires its `result_hash` to equal the producer/extension consumer hash.
  P41 positioned entries are `LIVE_TRACE` with those actual hashes. R109
  positioned-hash probe passes. An independent monkeypatch of the evaluator to
  return a false hash refuses `PROGRESSIVE_ACTUAL_CONSUMER_MISMATCH`, confirming
  actual call/value use rather than label echoing.
- Condition-value mutation, unlike target shape, N10E cells/minority/zero,
  uncertainty, T0/T1 route change, field revocation/restore, cold replay and
  actor `NOT_TOUCHED` remain.

### Repair 1 — not complete

`_progressive_world_identity` checks world universe/release/risk and a *present*
source repository, and `_progressive_prefix_identity` checks prefix source/
release/risk. It does **not** check:

1. world `rows_hash` against the actual prefix/source rows;
2. a required world source repository (omitted source repo bypasses the
   conditional identity check);
3. all prefix repository identities (a mixed-prefix repository copy is
   accepted).

Independent witnesses, each returning `PROGRESSIVE_WORLD_SELECTED_VIEW` and
concrete routes:

- `_progressive_fixture_parts()` world with `rows_hash="f"*64` -> selected.
- Same world with `source["repo"]` removed -> selected.
- Second prefix `repository=copy(prefix.repository)` -> selected.
- The already-fixed foreign release/universe/risk case correctly refuses
  `PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH`.

Minimal fix: extend `_progressive_world_identity`/
`_progressive_prefix_identity` to compare the exact world `rows_hash` and
require a present source repository, and compare every prefix's repository
identity to the first. Refuse with the existing typed identity code before
registering/serving. No new architecture or engine.

### Fourth gap — correctly stopped, not accepted

The author correctly reports that pinned P41
`P41Service.progressive` lines 133 and 149–171 derive `steps` from
target/ordered conditions, compute `n9_world` separately, and do not include
world/snapshot in `n10w.progressive_update_identity`/positioned consumption.
The exact smallest owner amendment is stated: extend the P41
provider/`progressive` call or add a world-conditioned provider contract and
include the selected world binding in the consuming assertion.

T0/T1 still changes actual N9/E04 routes and the view correctly remains
incomplete for full N10W world-value consumption. This review does not reject
repairs 2/3 because that upstream gap remains, and does not accept the whole
R107/R06 function.

## Preserved limits

Sourcefree TEST_ONLY finite-shape release; no original source, original
35/1890/global F6/F7/F8, F5/F6/F7 issuance, actor/person, R09/CI/prod,
N11/N12, Sorok/J52/W52 or production adoption. Missing-cell/low-support was not
independently expanded. No candidate repair, self-adoption, new worker/provider
or broader court.

## Artifacts and remote

`ORACLE.md`, this review, `COVERAGE_AND_LIMITS.md`, `RESUME.md`, `probes/`,
`replay/` JUnit/logs, `evidence/commands.txt`, `evidence/remote_readback.txt`,
`proof_witness.json`, and self-excluding `manifest.json` with SHA256 and byte
sizes. Push is non-force; final remote SHA is reported separately.
