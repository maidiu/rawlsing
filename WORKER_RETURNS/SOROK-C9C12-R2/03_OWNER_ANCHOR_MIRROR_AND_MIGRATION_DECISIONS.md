# C9C12-R2 — owner anchor, mirror and migration decisions

Observed FINDING: the sourcefree C12 edge is now internally coherent at `BP4_C12_STORE@1`, but the external anchor, C9R durable store/version and mirror ACK contract remain owner decisions. Causal INTERPRETATION: the candidate can read and refuse correctly, but it cannot manufacture custody or decide whether C9 R3B's actor prefix is the canonical durable C9. Proposed HQ ACTION: hold canonical adoption and route the exact decisions below. Accountable OWNER: original C9R/BP4/C12 owners and incumbent HQ; separate reviewer.

## Required owner decisions

1. **External C12 anchor custodian.** Candidate `check_anchor(None, payload, None)` returns `OWNER_ANCHOR_REQUIRED`; a locally generated test key is not accepted. Owner must identify issuer/key/sequence/rollback window and independent verification. The candidate does not claim authenticity or completeness.
2. **Anchor preimage.** Candidate adds `branch_identity.actor_ids` and `created_clock` (plus fork clock/root hash) to the payload. Owner must confirm this is the intended anchor preimage and that mutation of branch identity is not a lawful migration. Old BP4R diagnostic remains the historical vulnerability.
3. **C12 writer schema.** `@1` is supported. `@2` is refused by the actual C9 consumer and C12 guard until the owner issues a migration/writer-version decision. No silent replacement.
4. **C9 writer version and old-count.** The candidate uses BP4R patched C9 `b9000cdb…`; historical C9 R3B `67f34f69…` preserves 14 PASS / 1 FAIL. Owner must decide the version split for the old-count C12 suffix conflict, not merge the two test expectations.
5. **C9 durable actor store.** `ActorAuthority` genesis and held state are readable by `read_actor_snapshot`; the actor store is not BP2P4J's C9R CandidateStore. Owner must decide whether a C9R adapter is required or the actor store remains separate.
6. **Mirror/outbox contract.** Candidate reads optional `C12_ACTOR_MIRROR_R3@1` and `projection_outbox`; PENDING and missing states are typed. Cross-database ACK/projected-hash equality, mirror fork state and atomic C9+C12 delivery remain NOT_RUN and require owner contract.
7. **E2 and Rule A/T.** Performed E2 vs offered-only remains a BP2P4J/R31J evidence distinction (2/2 tests pass); C9 R3B has no native E2 field. Held Rule A/T is test-only and must not be turned into a native NOCHANGE.
8. **First consumer.** `read_actor_snapshot` / `read_composite` is the sourcefree I1/CP-A5-compatible reader; it returns `OWNER_ANCHOR_REQUIRED`, not native acceptance. No production/C11/C12/A0–A5 adoption.

## Migration policy

- Do not overwrite `BP4_C12_STORE@1`; fork or version any `@2` migration.
- Do not rewrite historical episode body branch_id; origin is immutable, SQL location may change on fork.
- Do not convert old C9 14/1 RED into a green rewritten oracle; create a separately versioned test.
- Do not accept mirror metadata as external anchor custody.
- Do not use a test-generated signature/key as owner evidence.

## Candidate first consumer

`c9c12_reader.read_composite(c9_path, c12_path, actor_id=..., c12_branch_id=...)` returns actor head/version/outbox/mirror state plus C12 cold read and `OWNER_ANCHOR_REQUIRED`. It is sourcefree candidate code, not an owner-frozen contract.

DONE: exact owner decisions and migration boundaries. REMAINING: owner custodian/version/mirror decisions and independent review. CRITICAL BLOCKERS: external anchor absent, C9R version split, mirror ACK unproven. LARGEST MOVE: owner issues anchor and C9 writer version decision. FLIGHT: no merge/pre-MAIN mutation. DELTA: candidate separates sourcefree evidence from owner custody rather than inventing it.
