# Authenticity negatives and exact owner decisions

Disposition: **ENGINEERING_REVISE__AUTHENTICITY_COMPLETENESS_HOLD__NO_ADOPTION**. Full measured observations are under `independent_probe.observations` in 01; diagnostic assertions passing means the described behavior was reproduced, including candidate defects.

## Source coordinates

BP4 author: `790f793ea85c8aba914970b7d9c3c25f81bf8a01:WORKER_RETURNS/SOROK-BP4-C12-CHAIN-AUTHENTICITY-OWNER-COURT-R1/03_BOUNDED_SOURCEFREE_CODE_OR_EXACT_OWNER_HOLD.md`. Part B contains exact `bp2p4/c12_guard.py` blob `a6a8de75ad92967e9fde354d76adce8b9572217e`, SHA-256 `7fd5dd55912e5d8a16ece9eb47909728fc69ca5031064c809b6d2673232a8021`, and test blob `8ca11491af25b98825c88f1355e391ce82659ab7`, SHA-256 `fa4b6d8e347be254a40bdf9e0aaa8ee077c8a4ea3fdd11fb8bf5422df91ca82a`.

Original writer: `5b3e6577400ea1d88971ae6b48e41a118b8059ae:WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/vendor/bp4/bp4/store.py`, blob `69a58f43dc70d320f2fc476eeac324c82c37ee59`. Repaired C12: `68b058656254234f0af02df2a592aa6f8c6a8bd2:WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j/candidate/vendor/bp4/bp4/store.py`, blob `c94cd131f6d24737e43a2f3dd192ac2a7569eb18`. These stores are different source cuts, not interchangeable labels.

C9: `1e99681f58086f2784834df1186cfba71a2c50b9:SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL/c9_actor_r3.py`, blob `67f34f699220ec1407e7e8f0d58ed328e88a36af`. Tests at the same prefix, `tests/test_c9_r3.py`, blob `c796524cde49306d4e7456b3e30f942323c0fd41`.

## Negative and positive observations

| Witness | Observed result | Interpretation |
|---|---|---|
| Valid SAY on original verifier | RED: `episode:0:body_hash_mismatch` | Original preimage defect independently reproduced |
| Same assertion with exact F2 | GREEN; body/hash/ID tamper negatives remain RED | Scoped F2 repair supported, no completeness grant |
| Raw deletion after dropping trigger | Content GREEN; digest changes; no-anchor HOLD | Triggers are not protection against raw DB owner |
| Raw self-consistent world insertion | Content GREEN; digest changes | Hash consistency cannot establish event provenance |
| Fully rehashed episode + derived ID | Content GREEN; digest changes | Public hashing does not authenticate the author |
| Perception channel substitution | Content GREEN; digest changes | Digest notices a difference only against a trusted prior value |
| SQL episode-ID-only substitution | F2 GREEN, guard RED | Guard adds a real column identity check |
| Legacy body/column episode IDs | Guard RED; migration required, no migration performed | Original issuer must decide permitted forms |
| Unknown metadata/user_version/application_id | Direct guard RED | Narrow declared-schema refusal works |
| Valid episode-bearing fork | Product returns OK; fork structure GREEN; episode content RED | BP4I3-01: origin branch and storage branch conflated |
| Empty-episode perception-only fork | Clock 11, both perceptions retained; author test passes | Does not falsify episode-bearing counterexample |
| SQLite trigger fails child checkpoint copy | Exception; cold readback has no child branch/history rows | Scoped savepoint rollback independently supported |
| Root actors/creation clock changed | Content GREEN, entire anchor payload unchanged | BP4I3-03: payload omits branch authority/chronology metadata |
| Perception 11 then episode 10 | Writer accepts; guard root GREEN | BP4I3-05: fork clock fix does not fix all append chronology |
| Matching unsupported C9 writer/domain `@2` | Helper READY; actual C9 fork reader FORK_READY | BP4I3-02: no supported-version gate on downstream path |
| Actual C9 actor/mirror/outbox | Held → projected/held → ACK/CLEAN; one receipt after replay | Local transactions/idempotency supported; no cross-DB ACID |
| Actual hard-coded S36/C12 cases | S36 passes; C9 same-count case fails, total 14/1 | BP4I3-04: repaired writer invalidates old defect fixture assumption |

Fail-closed anchor codes independently observed: `OWNER_ANCHOR_REQUIRED`, `ANCHOR_MALFORMED:schema`, `ANCHOR_ROLLBACK_WINDOW_UNPROVEN`, `ANCHOR_ROLLBACK`, `OWNER_TRUST_ROOT_ABSENT`, `ANCHOR_SIGNATURE_INVALID` (false result and thrown exception). Replayed guard tests also reject a prior payload after deletion as `ANCHOR_PAYLOAD_MISMATCH`. No accepted real signature was exercised. A caller-provided verifier callback is an unfulfilled trust precondition; this review does not turn a fixture callback into an owner.

## Decision A — issuer and finite anchor coverage

FINDING: no admitted owner-issued trust root or independently monotonic anchor service exists in this evidence. The candidate can refuse absent authority; it cannot supply it. Its present payload also misses mutable branch actors/creation metadata.

INTERPRETATION: the missing function is a competent issuer mapping a verified history cut and branch identity to an externally custodied, monotonic attestation consumed by the C12 reader. An unkeyed digest, repo-local secret or same-user test witness does not perform that function independently. An anchor proves at most its named finite cut; it cannot prove absence of deletion after that cut.

ACTION/CHOICES: original C12 owner must either (A1) name an independent anchor custodian, exact issuer/key identity, signed canonical envelope and out-of-DB sequence authority, or (A2) explicitly retain content-only use with authenticity/completeness UNKNOWN. A1 must bind reader/writer/fork policy versions, branch ancestry/root identity and relevant actor/chronology metadata, ordered histories/counts and the exact finite checkpoint. If metadata is intentionally excluded, the resulting claim must say so. Required negatives are deletion, injection, full rehash, stale anchor, wrong branch/schema/issuer and metadata substitution. No real key is created here.

OWNER: original BP4/C12 owner plus separately accountable anchor custodian; original scientific issuers still own source meaning. This return proposes the contract and does not issue it.

## Decision B — episode identity, forks and writer versions

FINDING: the writer seals episode body `branch_id=root`, then fork preserves that body/hash/ID while changing only SQL location to `child`. The guard requires equality between those two branch fields. Guard fork tests contain no episode row, so their positive is insufficient.

ACTION/CHOICES: original writer/schema owner chooses (B1) immutable origin body and explicit ancestry-qualified storage location, or (B2) a versioned child reissuance with new lawful body/hash/IDs and explicit migration. Do not rewrite sealed history under the old version merely to make the check pass. Decide whether to reuse the already pinned `68b` four-table fork implementation or retain the additive guard; either choice must pass the real episode-bearing product fork and cold reopen. Keep legacy fork roots held unless an authorized migration exists. Define append chronology separately: perception 11 followed by episode 10 is currently accepted even though the fork cut becomes 11.

For BP4I3-04 retain an exact old-writer fixture for the dropped-row negative and a separately versioned repaired-writer consumer case. Preserve same-count substitution as an actual adversarial identity change, not as an assumption that repaired code still drops data. No tests or writer code were corrected in this review.

OWNER: original BP4/C12 writer/schema and BP2P4J owners, with C9 owner agreeing the cross-version receiving contract; independent reviewer evaluates the resulting exact cut.

## Decision C — named C9 target reader and synchronization

FINDING: C9 `ActorAuthority.publish` commits actor receipt/head/outbox in one local transaction; mirror receipt/watermark and outbox projection updates use later local transactions. No distributed ACID exists. `MirrorStore.status(authority, receipt_hash)` checks matching receipt/projection/watermark/ACK. The BP4 helper only compares caller-supplied metadata and status strings and is not integrated into the C9 reader. `c12_fork_guard` ignores writer schema; it conservatively holds a perception-only suffix even on a repaired store.

ACTION/CHOICES: C9 owner chooses (C1) its exact receipt-specific `MirrorStore.status` as the first sourcefree materialized-read acceptance function, preceded by a validated supported-writer/fork-domain gate, or (C2) keeps that consumer SYNC_HELD until another named reader is issued. `project().state=CLEAN` alone and `two_store_readiness` alone must not authorize an authenticated read. Unsupported `@2` must refuse rather than pass because two unvalidated strings match. Pin the actual C12 branch/root/perception cut and exact mirror domain/version, and state whether repaired perception suffixes remain held or have an owner-issued acceptance rule.

The exercised input was a sourcefree held C9 receipt, its durable outbox, matching mirror branch/root and projection; outputs were `SYNC_HELD/MIRROR_RECEIPT_MISSING`, `SYNC_HELD/PROJECTED`, then `CLEAN/CLEAN` after ACK. This is an actual existing consumer replay with synthetic sourcefree facts. It supplies no Rule T, actor, native C12 or scientific grant.

OWNER: original C9 and C12 receiver owners. Canonical intake and central session-registry append belong to the protected PRE-MAIN owner through its own CAS path, not this reviewer.

## Terminal hand-back

DONE: exact sources, bounded independent execution and concrete falsifiers. REMAINING: the three owner choices and narrowly scoped corrections, then separate HQ/reviewer intake. CRITICAL BLOCKERS: BP4I3-01/02 and unissued anchor; BP4I3-03/04/05 limit payload, test and chronology claims. LARGEST PRODUCTIVE MOVE: choose the episode/fork and C9 receiving contracts using the existing code; do not commission another generic census. FLIGHT: one independent review, no new worker or QF2. DELTA: empirical compatibility RED and incomplete anchor coverage are now explicit. SCIENTIFIC/AUTHORITY HOLD persists. STOP after this return.
