# R61-R08V R8 independent review — return

Verdict: **ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING**
for the bounded R8 correction and the retained R61AF/R7 scoped callable grain.
No remaining scoped defect found.

R7-AF-01 is closed: a primary `resolve` cache hit now preserves the explicit
configuration refusal codes instead of collapsing them to generic stale cache.
The limited code/test delta (9 module lines, 13 test lines) changes only
`EvidenceResolver._replay_cache`; no schema, owner descriptor, envelope,
admission, live-producer, native-owner or positive-path change is present.

## Custody

- Exact stable root: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r61-r08v-r8-independent-review-r1`; preflight
  `pwd`/toplevel/branch/status matched and the tree was clean.
- Candidate/startup: `be1133391d91b5c2bf69299188e6f011162f269b`.
- Code commit: `80bb8c182`; module blob
  `3ca860e409f1d063da4cd03dd1691a89c67333f6`; test blob
  `5832ce0598fa02df93fcd200010a0076921e6cbe` (working tree matches).
- Frozen R8 EXPECTATIONS:
  `cb018e1011fca433c9a8132fbbe3a75879429fe9`, committed before R8 candidate
  code or author conclusions.
- Precode correction contract `3f45fc9bc`; candidate delta is exactly the two
  R08 code/test paths plus the seven author R8 artifacts. No native/archived/HQ/
  other-node edit.
- Author R8 manifest independently recomputed: all six listed artifacts match
  byte-for-byte; `manifest.json` explicitly self-excludes.
- Prior R7 review `fc4597fb8398b8012367d8d9d1fa36502b3d798e` and R7/R6/R5/R4
  oracle artifacts preserved. R8 reviewer wrote only this ownroot.

## Target correction actually observed

- Legacy `trusted_binding_hashes=("a"*64,)`: live first resolve `SUPPORTED` 60;
  cache-hit second resolve `UNKNOWN` / exact
  `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`; no support served.
- Wrong `trusted_descriptor_hashes` on a cache hit: `UNKNOWN` / exact
  `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`; correct descriptor pin imports/reads 60.
- Missing verifier on a cache hit: `UNKNOWN` / `NO_CONFIGURED_TRUST_ROOT`.
- Genuine stale/unauthoritative cache state remains `UNKNOWN` /
  `STALE_OR_UNAUTHENTICATED_CACHE`; no support.
- Import/export retain the explicit `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`
  limits; configured pins are not silently ignored.
- No setup/import exception was counted as typed refusal.

## Retained qualification

- Author suite: 126 passed, 0 failed/errors/skipped (113 R08 + 13 C1), with the
  inherited, independently verified fixture/harness bytes.
- Independent R7 successor probe replay under R8: **76/76 passed**, including
  the former failing legacy-pin resolve probe. This retains the 13-owner-class
  normalized descriptor inventory, no-admission transport, unknown/legacy
  refusal, descriptor pins, live-pin counter 0, verifier-only import/read/
  re-export, cold process, and exact 54/6/60, changed 54/16/70, observed zero,
  ZERO_SUPPORT, typed/currentness and Z UNRESOLVED16 controls.
- R8 targeted probes: 5/5 passed (legacy code, descriptor-pin code, genuine
  stale, missing verifier, import/export limits).
- R7 semantic adapters: 3/3 passed, preserving the removed-transport/local-label
  invariants under the canonical descriptor.
- R6 immutable replay: 9 passed / 2 removed-transport/local-label superseded
  expectations; R5: 6/2 old grade/import superseded; R4: 7/2 lawful
  `EvidenceAssociationError`. All outcomes accounted; no blanket dismissal.
- Fixture Git bytes/identities and the harness path-only redirection were
  inherited from the R7 verification; no new fixture extraction or broad repo
  sweep was performed.

## Limits

- Full live J42 `E41ProviderAdapter.step`, live P41 progressive and repaired
  live E04 terminal integration remain **NOT_REACHED**; future-owner work, not
  waived.
- No original data/science, source rights, production/CI, N11/N12, F6/F7/F8,
  actor, Sorok, J52/W52, R03/R09 or protected-capture authority is claimed.
- The missing-verifier cache-hit check exercises the internal `_replay_cache`
  configuration path; it changes no candidate state and serves no support.
- No candidate edit, adoption, self-repair, author wake, new session, Codex
  worker, provider or account change.

Artifacts: `EXPECTATIONS.md`, `00_RETURN.md`, `defects.md`, `limits.md`,
`RESUME.md`, `FACILITY_HISTORY.md`, `proof_witness.json`,
`SHA256manifest.json`, `outcomes/*`, `probes/*`, `junit/*.xml`, `logs/stdout.jsonl`.
