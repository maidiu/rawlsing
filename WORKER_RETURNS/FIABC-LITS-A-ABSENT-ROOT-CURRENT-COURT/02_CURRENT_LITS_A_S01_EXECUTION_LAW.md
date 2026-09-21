# Current LiTS-I / Candidate-A S01 Execution Law

## Scope

This law applies only to the current final-P2 LiTS-I / Candidate-A cell after the local court proved the historical R5 root absent.

It does not authorize a prebuild.

## Entry

Current first unfinished stage:

`LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD`

Required state at stage entry:

- canonical LiTS-I source identity fixed to `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- candidate-owned current target `cells/LITS_I/A/durable/lits_a_r5` absent;
- no historical R5 substituted;
- no historical S01 numeric credit consumed;
- frozen upstream/oracle and ordinary final-P2 preflight gates already satisfied.

If a target already exists before the cold current S01 action, fail closed. Do not silently treat it as the missing historical root and do not let it suppress the measured build.

## Single build

S01 performs exactly one:

`BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE`

using:

- builder: `R5CompactLongShardedBuilder`;
- owner commit: `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`;
- builder blob: `92e364b31eaf27be1bca2081eff65f6ffb779c3d`;
- candidate owner/adapter semantics: unchanged;
- canonical source SHA: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- exact live reader/config law;
- builder-emitted exact R5 build config.

The generic S01 meter records this as `COLD_FIRST_REALIZATION`, cost class `C2`, metric `build_or_open_wall_ns`.

There is no second "R35 build."

## Contemporaneous parentage

The same S01 state emits:

1. source-verification receipt under operation
   `VERIFY_CANONICAL_LITS_I_RAW_SHA_FOR_CURRENT_S01_BUILD`;
2. derivative receipt for class
   `LITS_A_PRESERVED_R5_CARRIER` — "preserved" here means the current S01 output is persisted for downstream stages, not that an old root was reused;
3. parentage bundle connecting that derivative receipt to the contemporaneous source receipt;
4. exact R5 root metadata including build config, release identity, member inventory, logical stream digest, row count, and embedded source artifact ref;
5. a physical-realization seed binding Candidate A, current root identity, source/derivative receipt identities, and bundle identity.

The seed must state:

- `physical_equivalence_claimed = false`;
- `semantic_parity_claimed = false`;
- `r35_i03_status = PENDING__MUST_USE_SAME_S01_STATE__NO_SECOND_BUILD`;
- performance admission blocked pending R35-I03 and parity.

## Downstream reuse

S02 and subsequent LiTS/A stages consume the candidate-owned current S01 R5 and verify its exact bundle/seed. They do not require a historical-root environment variable.

A parentage failure stops the cell.

The current S01 result may be reopened/read downstream; reopening the same result is not a second build.

## Physical and semantic admission

R35-I03 remains a distinct physical court. It must construct/verify the Candidate-A physical realization from the same S01-root/parentage state against the candidate-neutral LiTS physical expectation.

No physical PASS is implied merely because S01 built successfully.

Independent semantic/parity gates likewise remain separate.

Downstream performance is inadmissible until the required physical-equivalence and independent semantic/parity gates pass.

## Nondisplacement

This succession changes current realization/control law only. It does not change Candidate A's meaning, source identity, R5 format, workload, R35 schema, semantic oracle, or ranking/selection law.
