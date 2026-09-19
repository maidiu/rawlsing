# FIABC-B05 — P2X Succession Failure Falsifier

## Scope and execution identity

- Repository: `maidiu/rawlsing`
- Branch: `agent/rabochii-premain-fiabc-b05-p2x-succession-failure-falsifier-r1`
- Base: `integration/pre-main-reconciliation-r1` at `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`
- Authorized surface used: GitHub/browser repository surface only
- Library: not used
- Production/HQ/authority/test files modified: none
- Return-only path: `WORKER_RETURNS/FIABC-B05/`

This return tests, rather than assumes, the hypothesis that recent P2X blockers disproportionately arose because accepted functions/authority were not actually consumed by the executable graph.

## Result

**The disproportionate-succession-failure hypothesis survives hostile testing, but its universal form is falsified.**

The diagnostic ledger contains 22 blocker/repair episodes. They are not an independent statistical sample, so the counts are descriptive rather than inferential. Still, the pattern is strong: 17/22 episodes are classified as `PARTIAL_SUCCESSION`, `PRESERVED_BUT_DISCONNECTED`, `AUTHORITY_EXISTS_RUNTIME_INTEGRATION_MISSING`, or `SUPERSEDED_IMPLEMENTATION_FUNCTION_PRESERVED`; 5/22 are classified `GENUINELY_MISSING`.

The integration/succession pattern is therefore real and recurrent, not an unfalsifiable story. It is also not sufficient as a master explanation.

## Strongest evidence for succession/integration failure

1. **WVS F0 looked like missing authority, then F1 falsified that reading.** HQ adopted 14/14 required live rows as `B__SEMANTIC_AUTHORITY_EXISTS__PRE553_ISSUANCE_OR_BINDING_ONLY`, with 0 rows in `D__GENUINELY_MISSING_SEMANTIC_OR_ROUTING_AUTHORITY`. The defect was exact PRE553 authority form/binding, not absent WVS meaning. See `HQ_HANDOFF/EE_P2F0_BLOCKER_ADJUDICATION_20260917.md` and `HQ_HANDOFF/EE_P2F1_ADOPTION_20260917.md`.

2. **The original LiTS A/B terminal blockers were composition failures across already-accepted surfaces.** Candidate A already had an accepted owner, R5B adapter boundary and D04 evidence; Candidate B already had a cacheless C11 owner plus partial runtime refs. What was absent was the executable owner-to-common-runner binding. R6O later requalified both accepted owner seams without rerunning their preserved first-build/cacheless preparatory stages. See the P2X blocker JSONs at commit `29e434a385719f9835e0bcd252fb24bc37675a99` and `HQ_HANDOFF/EE_P2R6O_AB_OWNER_SEAM_ADOPTION_20260918.md`.

3. **R6I is a direct producer/consumer mismatch.** All required facts existed, but thirteen of seventeen R5A/R6A-required fields were outside the exact `identity_material` structure read by production R6A. HQ explicitly classified it as `R6B_INTERNAL_VERIFIER_PASS__BUT_NOT_DIRECTLY_R5A_R6A_RUNTIME_CONSUMABLE`. See `HQ_HANDOFF/EE_P2R6I_RUNTIME_COMPATIBILITY_CORRECTION_20260918.md`.

4. **Later measured-execution stops were unmistakably packaging/orchestration defects.** The P2X branch lacked an already-adopted R6A runtime substrate; the WVS wrapper recursively called itself instead of the accepted binder; S17 lifecycle ordering contradicted the verifier contract; common infrastructure failures were serialized as candidate-local failures. HQ explicitly classified these as infrastructure, not candidate semantics. See `HQ_HANDOFF/EE_P2X_INFRASTRUCTURE_STOP_ADOPTION_20260919.md`.

5. **The AS2A path blocker is the cleanest path-drift example.** Exact accepted ledger/package blobs existed at the pinned commit, but the backend addressed a directory name that did not exist. R6T changed only the path to `banked_as2a` and preserved authority bytes. See `HQ_HANDOFF/EE_P2X_LITS_AS2A_PATH_BLOCKER_ADOPTION_20260919.md` and `HQ_HANDOFF/EE_P2R6T_PASS_ADOPTION_20260919.md`.

## Counterexamples that falsify a universal “it was always disconnected” theory

The hostile search found genuine absences:

- **LiTS Candidate C production realization:** accepted lineage had only synthetic B20 determinants/test refs and partial role bindings; no accepted real-source `RouteCDeterminants`, `Cacc2Determinants`, or complete 19 atom-binding preimages existed. This remained a typed Candidate-C nonqualification.
- **WVS Candidate C portability:** the frozen C owner was LiTS-specific; there was no WVS-specific accelerator and no lawful zero-accelerator fallback. R6S still preserves that portability failure with no backend path.
- **Mixed predicate-composition successor authority:** base/F02 semantics existed, but the exact authority permitting mixed composition did not. R4A had to create and HQ adopt a new successor relation.
- **F02-scope → I02-runtime realization authority:** both endpoint identities existed, but no lawful directional realization relation existed until R5A.
- **WVS `B_COUNTRY` coordinate-use authority:** FQRA source meaning existed, but the bounded downstream proposition “use this slot as `CURRENT_SURVEY_OR_INTERVIEW_COUNTRY` position coordinate for frozen P2 routing” did not. R6Q explicitly proved it absent, and HQ then adopted new authority `9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d`.

These counterexamples matter: underlying semantic capital can exist while a *new relation/use authority* is genuinely missing, and a candidate-specific executable realization can genuinely be absent.

## Structural invariants indicated by the evidence

The recurring prevention law is not “add another adapter.” It is to make succession mechanically unavoidable at the consumption boundary:

- exact content-addressed dependency closure before court wake;
- end-to-end producer-output → production-consumer qualification, not producer-local verification;
- path-independent governed refs for historical authority;
- persistence contracts that preserve rehydratable bodies when downstream public validation needs them;
- one authoritative lifecycle state machine with typed common/candidate failure scope;
- explicit semantic-relation authority for cross-dialect composition, identity realization and downstream role promotion;
- explicit source×candidate capability certification so real candidate nonportability is not confused with integration drift.

No repair is proposed here; these are falsifier-derived invariants that distinguish failure classes.

## Terminal

`FIABC_B05_P2X_SUCCESSION_FAILURE_HYPOTHESIS_HOSTILELY_TESTED`
