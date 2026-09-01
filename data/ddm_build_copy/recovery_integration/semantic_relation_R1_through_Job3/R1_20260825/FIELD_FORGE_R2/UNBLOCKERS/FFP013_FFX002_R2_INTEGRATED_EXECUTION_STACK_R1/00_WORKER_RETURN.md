# FFP013 — FFX002-R2 INTEGRATED EXECUTION STACK R1 — WORKER RETURN

Status: \`PASS__FFX002_R2_INTEGRATED_SOFTWARE_STACK_READY_PENDING_FROZEN_EMPIRICAL_AUTHORITY_BINDINGS\`

## Grounding

- Repository: \`maidiu/rawlsing\`
- Worker branch: \`agent/rabochii-field-forge-r2-ffp013-ffx002r2-integrated-execution-stack-r1\`
- Exact starting HEAD: \`729c569f869f8f6c0dc0123f384cce2409e1c9b2\`
- Common sibling base: \`9611a9067ab28e17eb45b565398c7e604a24e77b\`
- Governing FFX002-R2 design: \`5343862783959a1455735c0a5eb7b330c76f42d5\`
- Full sibling-history merge commit: \`649e2dbcf527e80ac89cc0c763945797aa71fd4a\`
- Genuine empirical canary executed: \`FALSE\`
- Production respondent data accessed: \`FALSE\`
- PRA/CIM/CITC minted: \`FALSE\`
- Semantic authority changed: \`FALSE\`

## Complete sibling histories consumed

The integration merge has the FFP009 starting history as first parent and the exact Core A/B/C terminals as additional merge parents. This preserves every post-\`9611a906...\` commit in the three sibling histories rather than copying only their terminal validation snapshots.

### Core A — FFP010

Range: \`9611a9067ab28e17eb45b565398c7e604a24e77b..862279e95100bc1c57acb0ead0695eb8c27cbcd7\`

1. \`4190a841257e873aabacc63e7bc639d2c877f0df\` — FFP010 implement Core-A exact configuration producer
2. \`d8e9f520fb51632097de6351abee0a115d422822\` — FFP010 add Core-A exact configuration CLI
3. \`fae42665cf8de3f27010dcf1fc7123c6018c3644\` — FFP010 add synthetic Core-A contract tests
4. \`24cf89576c88c0f14e3384161e1854a5517064e0\` — FFP010 record Core-A EXE002 closure
5. \`d98e390a12e959f61147da8f767bc46376e0df64\` — FFP010 map Core-A contract coverage
6. \`862279e95100bc1c57acb0ead0695eb8c27cbcd7\` — FFP010 add Core-A validation receipt

### Core B — FFP011

Range: \`9611a9067ab28e17eb45b565398c7e604a24e77b..db912242e0f6bfefa61a2a83e11f701d17947af4\`

1. \`4e5f626d22365f1b827f4ebdfbdeab20d8a886a4\` — FFP011 implement bounded Core-B local geometry producer
2. \`078d572a0aff00a664667ff839a58342dc3ae1b8\` — FFP011 add Core-B local geometry CLI
3. \`53479bd52077e353ee9c1ca8a822484f9b8ed12b\` — FFP011 add hostile synthetic Core-B geometry tests
4. \`8cad322064629d78cbe8a9aaf106dadbe7624879\` — FFP011 record Core-B EXE003 closure
5. \`b5f9d3d76003e39ec0ae597fb8724eb3aa995e18\` — FFP011 add Core-B validation receipt
6. \`8956872bf1edde4298d542b0183897673f48bf49\` — FFP011 normalize closure receipt formatting and validation wording
7. \`db912242e0f6bfefa61a2a83e11f701d17947af4\` — FFP011 refine synthetic validation receipt

### Core C — FFP012

Range: \`9611a9067ab28e17eb45b565398c7e604a24e77b..38bc815d3edc8d8c75c8d8240de1da24cc588e5b\`

1. \`38bc815d3edc8d8c75c8d8240de1da24cc588e5b\` — FFP012 implement FFX002-R2 Core-C direct redistribution

## EXE005 empirical runner/scoring closure

\`EXE005_EMPIRICAL_RUNNER_AND_SCORING\` is closed at the software-stack level.

The integrated executable now provides:

- one common preflight over the FFP009 \`COMMON_SEMANTIC_INPUT_MANIFEST\`;
- one FFP009 canonical common-manifest hash implementation for all three arms;
- A/B/C independent hash attestations against that same frozen manifest;
- exact design-partition respondent-set equality gates across A/B/C;
- exact risk-set-ref, estimand, weight-design, PRA-binding, post-transform-state-registry, response-state, and special-state echo checks;
- active position/disposition measurement-role agreement between A and B and role-compatible C queries;
- frozen state-catalog coherence across A/B/C;
- pre-execution rejection of post-fork merge/collapse/rebin/recode/reorder/re-role/semantic-transform overrides;
- pre-execution rejection of cross-arm learned-output consumption;
- top-level A/B/C producer execution;
- common query routing with typed \`DOES_NOT_REPRESENT\` / \`ABSTAIN__NO_DECLARED_ARM_QUERY_ADAPTER\`;
- hostile orchestration plus an executable \`FORK_SEMANTIC_TAMPER__COMMON_MANIFEST_HASH_DIVERGENCE\` court;
- explicit \`SUBSTRATE\`, \`C\`, \`A+C\`, \`B+C\`, \`A+B\`, \`A+B+C\` ablation packages;
- weaker-baseline / target-added / full-admitted / target-removed rows for A, B, and C;
- arm input/output/code/replay receipt collection;
- raw distribution scoring with state-universe equality protection;
- externally supplied CITC rule consumption with no built-in materiality threshold, master score, winner, or preferred view;
- PRE-V3 P0/P1/P2/P3 downstream-ablation packets with actor interpretation explicitly prohibited;
- deterministic output-file materialization.

## Mechanical conflict resolution

The principal integration conflict was common-manifest canonicalization:

- Core A had an arm-local set-array canonicalizer;
- Core B interpreted declared set paths as dotted paths;
- Core C looked for \`set_valued_paths\` rather than FFP009 \`set_array_paths\`.

All three now recompute through the single FFP009 canonical contract. The arm code still performs its own attestation call, but it cannot define a different canonicalization rule.

No risk-set, estimand, role, state, or special-state convenience transform was introduced.

## Combined synthetic validation

The complete FFP009–FFP013 synthetic stack was executed together in one GitHub Actions checkout:

- Workflow: \`FFP013 Integrated Synthetic Stack\`
- Successful run: \`33560895833\`
- Tested code HEAD: \`ef52f0790ad8408d534b613bef0ee77d7c65ee62\`
- Python compile: \`PASS\`
- Combined pytest result: \`71 passed in 0.63s\`

The combined command includes:

- FFP009 harness tests;
- FFP010 Core A tests;
- FFP011 Core B tests;
- FFP012 Core C tests;
- FFP013 integrated-stack tests.

Integrated tests prove:

1. A/B/C independently attest one identical common-manifest hash.
2. A self-rehashed semantic tamper in one arm is rejected before any producer executes.
3. risk-set divergence fails preflight.
4. estimand divergence fails preflight.
5. post-fork merge/rebin/re-role fields fail preflight.
6. cross-arm learned-output consumption fails preflight.
7. minority destination states remain represented in A and C.
8. unsupported queries return typed abstention / \`DOES_NOT_REPRESENT\`.
9. replay collection binds exact code/input/output/common/holdout/query identities.
10. fork-semantic-tamper hostile execution rejects A/B/C.
11. CITC thresholds are consumed externally and changing the supplied threshold changes the ruling without changing stack code.
12. no preferred view or master score is produced.
13. PRE-V3 plumbing prohibits actor interpretation.
14. special-state semantics cannot be redefined by one arm.
15. target-removed ablations are explicit, including \`A+B\` for full-minus-C.
16. the top-level CLI runs the complete synthetic bundle and writes deterministic receipts.
17. execution mode is explicit: `SYNTHETIC_FIXTURE` versus `FROZEN_EMPIRICAL_CANARY`.
18. the synthetic suite proves no genuine empirical execution is mislabeled, while a future lawfully supplied empirical-mode bundle is explicitly marked as such.

## Exact runnable top-level entrypoint

\`\`\`bash
python data/ddm_build_copy/ffx002_r2_integrated_stack.py \
  --input-json <FROZEN_FFX002_R2_EXECUTION_BUNDLE.json> \
  --output-dir <FFX002_R2_OUTPUT_DIR>
\`\`\`

The input bundle must already contain exact frozen common-manifest/holdout/query bindings, A/B/C arm inputs, code identity refs, and an externally supplied CITC binding.

## Residual executable blockers

There is no remaining FFP009–FFP013 software-stack gap for A/B/C orchestration/scoring.

Genuine empirical execution remains correctly gated on exact frozen external authority/binding artifacts, including as applicable:

- CURRENT governed respondent entity/carrier binding;
- exact source/release/wave/context/form/module/split scope;
- CURRENT qimpl -> CURRENT empirical measurement bindings;
- exact respondent predicate-input binding;
- deterministic routing predicate execution/spec receipt;
- governed positive exposure/risk-set materialization;
- independent response binding;
- measurement/carrier/qimpl/predicate/response ancestry and supersession replay;
- exact authorized TTAR sequence or explicit governed NONE;
- accepted bounded PRA / analytic-role authority;
- active position/disposition ancestry-disjointness receipt;
- exact claim scope;
- exact estimand and weight/design refs or governed NONE;
- source-native response and special-state semantics;
- frozen post-transform state manifest;
- approved canary measurement set;
- exact code/version identities;
- externally supplied CITC.

These are authority/input gates, not missing execution-stack implementations.

No genuine canary was executed in FFP013.
