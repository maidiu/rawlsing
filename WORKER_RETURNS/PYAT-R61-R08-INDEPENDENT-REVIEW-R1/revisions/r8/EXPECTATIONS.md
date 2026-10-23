# R61-R08V R8 independent review — frozen EXPECTATIONS

Frozen and committed **before** reading R8 candidate code, candidate test code,
or author R8 conclusions. UTC freeze: 2026-10-23T23:33:34Z.

Reviewer: existing DISTINCT session `ses_e962f7b5effeIc4B6gtfbZNHvh` (not author
`ses_e98c8dfe6ffewNYOqJpvqK21a6`), OpenCode DeepSeek V4.1-Flash MAX/Global,
same account. No new session, Codex worker, subagent, provider or model.
Same-account roles are not credential, institutional or OS independence.
Python `/usr/local/bin/python3`.

Stable worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
branch `agent/opencode-pyat-r61-r08v-r8-independent-review-r1`. Write only
`WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/`.

## Custody pins

- Sealed R8 commission: `d5e9d097966401eee88005bba87084d6339e2685`;
  blob `3f2d522e19bfc80f83fc3a85ab7472d98450292e`.
- Candidate/startup: `be1133391d91b5c2bf69299188e6f011162f269b`.
- Code commit: `80bb8c182`; module blob
  `3ca860e409f1d063da4cd03dd1691a89c67333f6`; test blob
  `5832ce0598fa02df93fcd200010a0076921e6cbe`.
- Frozen precode R8 correction contract `3f45fc9bc`;
  `revisions/r8/CORRECTION_CONTRACT.md` blob
  `49f3734feff8a7be1a48fa849f9cede12751533a`.
- Binding R61AF `e349da0d886d8e365648afccf40a2e6b8e105ff7`; R61Q
  `99222514afbac4fc1671dbc90f02b210e6c1f6ce`.
- Prior R7 review `fc4597fb8398b8012367d8d9d1fa36502b3d798e` is primary
  regression evidence; R7 oracle/EXPECTATIONS and R6/R5/R4 artifacts preserved.
- Native owner pins unchanged: provider `23167aa2...`, composition
  `604c8d59...`, positioned evaluator `62e5eced...`, empirical objects
  `a61365b9...`, AT07/n10e fixture `0e384f72...`.
- R7 fixtures/harness remain inherited and were previously verified
  byte-for-byte; no new extraction is assumed. Candidate delta must be exactly
  the two R08 code/test paths plus the R8 author return root.

## R8 scope — exact remaining defect only

R8 is a limited correction of R7-AF-01, not a new architecture. The only
productive change expected is `EvidenceResolver._replay_cache` preserving the
explicit cache-configuration refusal raised by `_check_cache_configuration` /
`_check_descriptor_pin`:

- nonempty legacy `trusted_binding_hashes` on a primary resolve cache hit ->
  typed `UNKNOWN` / `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`;
- wrong/missing `trusted_descriptor_hashes` on a cache hit -> typed `UNKNOWN` /
  `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`;
- missing verifier -> `NO_CONFIGURED_TRUST_ROOT` preserved;
- genuine stale/unauthoritative cache state -> `STALE_OR_UNAUTHENTICATED_CACHE`;
- import/export explicit limits remain; no schema, security, ownership,
  envelope, positive-path or native-owner change.

## E1 — Custody and scope

- Candidate/startup, code commit, module/test blobs, contract and native owner
  blobs must equal the pins; branch must be the R8 reviewer branch at candidate
  `be113339`; worktree clean at freeze.
- Candidate delta exactly two R08 code/test paths plus author `revisions/r8/`
  root; no native/archived/HQ/other-node/config/source edit.
- Author R8 manifest independently recomputed, explicit self-exclusion; any
  mismatch/omission is a defect.
- Final reviewer commit non-force-pushed on the R8 branch; exact remote SHA
  read back.
Falsifiers: wrong startup/branch/blob/delta, false manifest, unreachable remote.

## E2 — Target refusal-code matrix

Test through the SAME configured public resolver/consumer:

1. `trusted_binding_hashes=("a"*64,)`, live first resolve -> `SUPPORTED` 60;
   cache-hit second resolve -> `UNKNOWN` with exactly
   `LEGACY_BINDING_PINS_REQUIRE_MIGRATION` (not generic stale).
2. `trusted_descriptor_hashes` wrong/missing on a resolve cache hit -> `UNKNOWN`
   with exactly `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`; correct pin -> 60.
3. No verifier -> `NO_CONFIGURED_TRUST_ROOT` (not a support/`SUPPORTED` result).
4. Genuine stale/unauthoritative cache state still
   `STALE_OR_UNAUTHENTICATED_CACHE`.
5. Import/export retain `LEGACY_BINDING_PINS_REQUIRE_MIGRATION` and
   `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`; no silently ignored configured pins;
   no support on any refusal.
Falsifiers: wrong code, collapse to stale, support served, pin ignored, crash
counted as refusal.

## E3 — Retained R61AF normal form and native positives

- Cache @5, descriptor @1 six fields, 13 owner classes, no admission/duplicate
  producer transport, descriptor hash distinct from binding hash, unknown/
  legacy refusal, deep detachment, descriptor pins.
- Independent native 54/6/60, changed 54/16/70, observed zero 60/no=0,
  ZERO_SUPPORT 0, typed bool/int/null, currentness, Z UNRESOLVED16.
- Live producer pin counter 0; verifier-only import/read/re-export/second import
  and fresh-process cold chain 60, original envelope signature/provenance, no
  producer invocation, no unsigned local delivery label.
- Prior R7/R6/R5/R4 applicable probes and semantic adapters; removed-transport
  tests accounted, no blanket dismissal. Targeted R8 successor plus retained
  applicable regression, not wholesale redundant exploration.
Falsifiers: normal-form/native/cold regression, setup crash as refusal,
all-refuse success.

## E4 — Same-consumer fault/restore and evidence

- Live first positive -> mutated/refused -> restored 60; evidence cell original
  6 (not 60), query/rule isolated.
- Exact commands/exits/JUnit; author passes not independent proof; no
  TypeError/import/setup failure counted as integrity.
- Fixture/harness invariants inherited and verified; no new broad repo sweep.

## E5 — Verdict and artifacts

Return `ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING` only if
E1-E4 fully justify the scoped grain. Otherwise return `REVISE` with the exact
minimal missing function/repro. Full live J42/P41/E04 remains NOT_REACHED; no
source/science/CI/prod/N11/N12/Sorok/J52/W52/R03/R09, adoption, author wake or
candidate edit. Original35/1890/globalF6F7F8 holds unchanged.

Required artifacts in the new R8 ownroot: `EXPECTATIONS.md`, `00_RETURN.md`,
`defects.md`/`limits.md`, probes, outcomes, JUnit, commands/exits, witness,
explicit self-excluded manifest, RESUME, logs.
