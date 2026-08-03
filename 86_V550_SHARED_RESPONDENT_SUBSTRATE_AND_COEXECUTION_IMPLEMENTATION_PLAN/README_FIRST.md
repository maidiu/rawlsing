# Section 86 — V550 shared respondent substrate and V550J co-execution implementation plan

## Status

`PASS_IMPLEMENTATION_PLAN_READY`

This section is an implementation work order, not a completed code change and not an empirical V550/V550J run.

It packages the complete bounded V550J authority adapter from Section 85 together with precise instructions for eliminating the duplicate respondent-database scan.

## Governing architectural decision

V550 and V550J remain separate semantic contracts, but they must execute inside one physical V550 shard envelope:

```text
live respondent database
        ↓ one unioned source/wave/country extraction
immutable harmonized respondent substrate
        ├── ordinary V550 question-level outputs
        └── V550J joint-response patterns
```

V550J must not independently query the production respondent database when a governed shared substrate is required.

## Read order

1. `ARCHITECTURE_DECISION.md`
2. `SOURCE_CODE_AUDIT.md`
3. `CODEX_IMPLEMENTATION_INSTRUCTIONS.md`
4. `contracts/SHARED_RESPONDENT_SUBSTRATE_CONTRACT.md`
5. `contracts/CLI_STORAGE_AND_RESUME_CONTRACT.md`
6. `EXACT_IMPLEMENTATION_SEQUENCE.md`
7. `ACCEPTANCE_GATES.md`
8. `manifests/FILE_CHANGE_MAP.csv`
9. `validation/TEST_AND_MUTATION_MATRIX.csv`
10. `CURRENT_STATE.json`

## Authority boundaries

Frozen and not to be rewritten:

- P3 R184 proposition-family authority;
- Section 85 bounded joint-configuration authority;
- existing V550 and V550J semantic outputs and identity formulas, except where an actual failed invariant requires a narrowly documented correction.

This section authorizes only execution-contract work:

- one database extraction;
- shared respondent-substrate persistence;
- local reuse by V550 and V550J;
- no-database V550J mode;
- deterministic resume and recovery;
- validation and mutation tests.

## Prohibited next actions

Do not:

- run the full 35-wave respondent universe;
- generate full canonical production files;
- run the nine real-data canaries before the structural implementation passes synthetic and checkpoint-only tests;
- package respondent-level data into Git or a cumulative handoff;
- infer joint responses from aggregate V550 outputs;
- reopen R184 or Section 85 merely because execution plumbing changes.
