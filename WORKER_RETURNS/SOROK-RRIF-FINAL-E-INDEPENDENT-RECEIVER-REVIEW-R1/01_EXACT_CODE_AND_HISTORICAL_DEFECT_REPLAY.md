# Exact code and historical-defect replay

## Candidate under review

```text
8d9585296ff264b947559f4a78f49f73ca45e53a
WORKER_RETURNS/SOROK-RRIF-FINAL-E-REPAIR-AND-FIRST-CONSUMER-R1/candidate
```

The candidate was materialized by `git archive` into the review worktree's
temporary `.review_tmp` directory, preserving source bytes. No author worktree
was executed or modified.

## Candidate court: 35 tests

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 candidate/run_courts.py
```

Actual:

```text
r2_original_20   20 passed
r3_extension_9    9 passed
rrif_e_repair_6   6 passed
first_consumer   exit 0
all_expected     true
source_manifest  7cfcb467...
```

The first-consumer receipt reports:

```text
PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT
help accepted, wait clock 40, cold return scene open
repaired C12 root/alt green; upstream defect reproduced RED
coordinated custody BOTH_GREEN on intact, guard red on tamper
C9 actor C9_SOURCE_MISSING (`no such table: actor_meta`)
CP-A5 separate root PASS, market UNKNOWN
OWNER_ANCHOR_REQUIRED, native_person=false
```

## T1 — repaired C12 verifier

Author test passed:

- intact root/fork GREEN under `RRIF_E_REPAIRED_C12_PREIMAGE@1`;
- old vendored verifier remains RED on intact episodes (`episode:0`,
  `episode:1 body_hash_mismatch`);
- body tamper RED, exact SQLite restore GREEN.

The repair is self-consistency only; `OWNER_ANCHOR_REQUIRED` remains.

## M1 — self-manifest hole found independently

Author test `test_source_preimage_excludes_itself_and_hashes_every_other_file`
passes, reporting 638 listed files and self-exclusion. Independent filesystem
audit of the same `rrif_r2` tree:

```text
actual regular files:                       640
listed in preimage:                         638
self:                                       1
unlisted:                                   1
unlisted path:                              first_consumer_cli.py
```

The preimage's self-exclusion is honest, but it does not cover the additive
`first_consumer_cli.py`. The test only checks listed rows, not actual unlisted
files. This is the M1 unverified-source-identity hole. The vendor manifest itself
has 444 rows and SHA-256 `7cfcb467...`; its bytes match.

On the **staged PRE-MAIN tree**, the defect grows: the preimage lists 638 files,
the staged tree contains 466 files, and the 174 `rrif_r3_extension` files are
absent. The preimage is not an audit of the receiving stage.

## C1 — coordinated SQLite tamper

Author test passed. Actual behavior:

- coordinated body/branch/perception edit is accepted by the repaired
  self-hash verifier (`Qualified` green);
- `GuardedC12Store` rejects it (`guarded` red);
- classification `SELF_HASH_ONLY__TRUST_CUSTODY_HOLD`;
- `external_owner_anchor=OWNER_ANCHOR_REQUIRED`;
- exact DB restore returns BOTH_GREEN.

This is a meaningful consumer guard, not authenticity. Independent external
custody remains absent.

## D1 — C9/C12/CP-A5 incompatibility

Author test and first consumer passed with the exact typed outcomes:

- C9 actor snapshot: `C9_SOURCE_MISSING`, missing `actor_meta`;
- C12 root: cold read `C12_COLD_READ_OK`, fork `VERIFIED`, anchor held;
- legacy first session: `C12_HELD`, `LEGACY_HELD`, unverified root;
- CP-A5 same-root: `BP2_ORIGIN_INVARIANT_MISMATCH`, no actor relabel;
- CP-A5 separate root: `PASS`, market answer `UNKNOWN`;
- no fabricated actor, owner key, anchor or native person.

## Old negative preservation

The candidate's own evidence and tests preserve the known old states:

- old `bp2p4.c12_verify` self-hash defect is intentionally reproduced RED;
- C9 actor/C12 incompatibility is not repaired by hash rewriting;
- C9 R3B `14/1`, BP4R `7/2`, B3 ghost, F1CI3, G17I, CAN3, OC5E and M04 are
  not re-authored or erased;
- no historical 294/97 recovery census was reopened.

## Verdict

The **candidate code** is a real sourcefree 35-test implementation. The
**receiving packet** fails on a clean PRE-MAIN stage because the R3 extension is
not included. The candidate's own 35-test pass is not a clean receiving proof.
