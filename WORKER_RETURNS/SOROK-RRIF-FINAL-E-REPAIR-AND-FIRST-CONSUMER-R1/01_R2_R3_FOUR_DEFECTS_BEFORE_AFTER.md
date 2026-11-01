# RRIF-E — R2/R3 four material defects before/after

## T1 — the independent C12 verifier was red on intact state

**Before.** On the intact R2 root, `QualifiedC12Store.verify('root')` was green,
but `bp2p4.c12_verify.verify_branch_chain('root')` was already red:

```text
episode:0:body_hash_mismatch
episode:1:body_hash_mismatch
```

The upstream helper hashed the episode body including the post-hash
`episode_id` field. The original test only asserted false after tamper, so its
“independent verifier” claim had no positive control.

**After.** `joined.c12_verify_repair.verify_branch_chain_repaired` applies the
actual write preimage:

- episode: `digest(body without hash and without episode_id)`;
- world/checkpoint: `digest(body without hash)`;
- stored column hash must equal body hash; sequence must be contiguous.

Same-assertion test `test_repaired_independent_c12_verifier_green_intact_red_tamper_restore`:

| State | Upstream vendored verifier | Repaired verifier |
|---|---|---|
| Intact root | RED (known defect preserved) | **GREEN** |
| Forged episode body | RED | **RED** |
| Exact restore | RED | **GREEN** |

The vendored bytes remain unchanged for source closure; the repair is additive.

## M1 — manifest self-entry impossible self hash/size

**Before.** `RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` listed itself with
`sha256 9b045ac…` / `size 89022`; actual bytes were
`sha256 641165d…` / `size 89341`. A file cannot contain its own content hash and
size without an impossible fixed point.

**After.** The repaired preimage:

- excludes exactly `RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` from `files`;
- records `self_exclusion: {path, content_addressed: false, rationale}`;
- content-addresses **638** other files with exact SHA-256 and size;
- pins `source_manifest_sha256 = 7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`;
- pins `source_candidate_commit = 598d9e9e…` and `dispatch_commit = e0d81695…`;
- preserves the 444 vendor manifest rows and bytes unchanged.

Test `test_source_preimage_excludes_itself_and_hashes_every_other_file` asserts
the exclusion, count, manifest digest and every other file hash.

## C1 — coordinated raw SQLite tamper versus self-hash

**Before.** `QualifiedC12Store` verifies preimage hashes but does not cover
episode column identity, perception actor membership or immutable origin
branch. A coordinated raw-DB attack can change the episode body `branch_id`,
recompute the body hash, keep the column hash consistent, and change a
perception `actor_id`; `QualifiedC12Store` remains green.

**After.** The consumer reports both readings on the same store:

```json
{
  "classification": "SELF_HASH_ONLY__TRUST_CUSTODY_HOLD",
  "qualified": {"ok": true},
  "guarded": {"ok": false, "errors": ["...branch_id_origin_mismatch...", "...actor_not_in_branch..."]},
  "external_owner_anchor": "OWNER_ANCHOR_REQUIRED",
  "authenticity_claimed": false
}
```

Exact restore returns both to green:

```text
BOTH_GREEN__SELF_HASH_PLUS_GUARDED_ROWS__NO_OWNER_ANCHOR
```

This is not cryptographic owner custody. The guard is a sourcefree row/fork
reader; an external owner-issued anchor remains absent.

## D1 — C9 actor / C12 root / CP-A5 actor incompatibility

**Before.** R2 called the R3 C9C12 comparison a “compatible sourcefree candidate
unintegrated.” The exact source cuts disagree:

- R2 C9 is BP2P4 `CandidateStore`, not `C9_ACTOR_AUTHORITY_R3@1`;
- R2 C12 root has no `actor_meta` table; `read_actor_snapshot` returns
  `OperationalError: no such table: actor_meta`;
- R2 fork `first_session` has a legacy root; the C9C12 guard reports
  `legacy_root_unverified`;
- CP-A5 expects `TEST_ONLY_BP1_ACTOR_A`; R2 uses
  `TEST_ONLY_BP1_R26V_ACTOR_A` → `BP2_ORIGIN_INVARIANT_MISMATCH`.

**After.** `joined.c9c12_compat.read_c9c12_compatibility` returns exactly:

```text
INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED
```

with `owner_migration_required=true`, `external_owner_anchor=OWNER_ANCHOR_REQUIRED`,
and `native_person=false`. The C12 half is genuinely read; the C9 actor snapshot
is missing; the fork is held; CP-A5 is consumed on its own root, not welded.

## Honest trust limits

- Sourcefree TEST_ONLY only.
- No external C12 owner key, anchor, mirror, outbox ACK or production custody.
- No native C9/C12 actor, CAN/ADP/SCI05 rule, Pyat world/N11/N12/C11 or human A5.
- No PRE-MAIN merge, owner adoption or self-review.
