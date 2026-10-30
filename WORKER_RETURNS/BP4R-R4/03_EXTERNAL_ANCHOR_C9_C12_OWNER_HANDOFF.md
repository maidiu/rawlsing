# BP4R external anchor and C9/C12 owner handoff

## Status

This is a sourcefree engineering candidate, not an adoption, not a native C12
receiver and not an authenticated anchor. The original BP4/C12 writer/schema
owner, C9-R3 actor/mirror owner, BP2P4J verifier owner and a separate I3
security reviewer must decide the exact contracts below.

## Decision A — episode immutable origin vs child location

**Candidate implemented:** the sealed episode body `branch_id` is the immutable
origin; the SQL `branch_id` column is the current storage location. A copied
child row keeps the parent body and hash; its location changes to the child.
Origin is resolved from exact fork prefix counts. A child-local row's origin is
the child. No hashed body is rewritten.

**Observed positive:** `JoinedProduct.say` → guarded fork → `alt` now reports
`content_ok=true`, `fork_ok=true`, `schema_ok=true`; the child body remains
`branch_id=root`, SQL location is `alt`, and cold reopen preserves both.

**Observed negative:** moving a child-local episode to a foreign branch is
refused with `branch_id_origin_mismatch` at the same read.

**Owner choice required:**

- **A1 (implemented candidate):** ratify immutable origin + explicit location
  projection under `C12_GUARD_READER@1`; define whether origin is the immediate
  parent or the original author for nested forks.
- **A2:** instead issue a versioned child reissuance/migration with new lawful
  bodies/hashes/IDs. Do not rewrite sealed history under the old version.

Legacy roots/fork IDs remain held unless an authorized migration exists.

## Decision B — C9 supported writer versions and the old-count conflict

**Candidate implemented:** the actual C9 `c12_fork_guard` reads `meta.schema`
before any fork decision and refuses anything outside
`SUPPORTED_C12_WRITER_SCHEMAS = {"BP4_C12_STORE@1"}`. It also refuses nonzero
`PRAGMA user_version` and `application_id`. The helper handshake/readiness
functions no longer accept two matching unsupported `@2` strings.

**Observed:** `@2` returns `FORK_HELD / C12_WRITER_SCHEMA_UNSUPPORTED`; `@1`
returns `FORK_READY`; source severance reproduces the old `@2 → FORK_READY`
result and restoration returns HOLD.

**Preserved RED:** the C9-R3 suite is **14 passed, 1 failed** at
`tests/test_c9_r3.py:476`: parent perceptions=2, child=3. The repaired C12
writer preserves the formerly dropped suffix; the old test assumes it is
dropped. This is a true version incompatibility, not a source-intrinsic
negative and not a test to weaken.

**Owner choice required:**

- confirm the exact supported writer schema set and whether SQLite
  `user_version`/`application_id` are part of the C9 receiving contract;
- split the test contract into (a) an exact old-writer fixture that still drops
  the suffix and (b) a separately versioned repaired-writer consumer case;
- decide whether C9 `c12_fork_guard` may ever return `FORK_READY` for a
  perception-inclusive repaired fork, or must remain `FORK_HELD` until a new
  owner-issued acceptance rule exists.

## Decision C — external C12 anchor and completeness

No owner-issued trust root, key, signer, custodian or monotonic ledger exists.
The candidate does not invent one. Current `check_anchor` behavior remains
fail-closed: `OWNER_ANCHOR_REQUIRED`, malformed schema, rollback window
unproven, rollback, trust-root absent and signature invalid all hold.

**Observed residuals:**

- changing root actors and `created_clock` to 999 leaves the entire
  `anchor_payload` unchanged;
- global writer chronology still accepts perception clock 11 followed by
  episode clock 10;
- raw SQLite deletion, self-consistent injection, fully rehashed episode
  substitution and perception-channel substitution remain content-green and
  change only the unkeyed chain digest/anchor payload.

**Owner choice required:**

- **C1:** name an independent anchor custodian, exact issuer/key identity,
  signed canonical envelope and out-of-DB sequence authority; extend the exact
  finite payload to cover branch ancestry, actors/created_clock, ordered
  histories/counts and the exact checkpoint, or explicitly declare excluded
  claims.
- **C2:** retain content-only use with authenticity/completeness `UNKNOWN` and
  no production claim.

No key or fixture callback may substitute for C1. A same-user HMAC witness is
not an independent security boundary.

## Decision D — global writer chronology

The current writer still accepts an episode at clock 10 after a perception at
clock 11 and reports `last_clock=10`. The repaired fork uses the
perception-inclusive cut, but global four-table monotonic writer chronology is
not established. This is a separate HOLD; the candidate does not fix it by
fiat.

## Exact candidate and source custody

| Item | Ref |
|---|---|
| Base | BP2P4J `5b3e6577400ea1d88971ae6b48e41a118b8059ae` |
| F2 verifier | `0636d257…`, blob `c1699c8da5e944ed079708e272c3af50d5a30a44` |
| Author guard | `790f793…`, blob `a6a8de75ad92967e9fde354d76adce8b9572217e` |
| C9-R3 | `1e99681f…`, blob `67f34f699220ec1407e7e8f0d58ed328e88a36af` |
| C12 repair | `68b058656…`, candidate store blob `c94cd131f6d24737e43a2f3dd192ac2a7569eb18` |
| BP4R guard patch | `candidate/patches/01_c12_guard_episode_origin_and_version.patch` |
| BP4R C9 patch | `candidate/patches/02_c9_actual_consumer_writer_version.patch` |
| BP4R test court | `candidate/tests/test_bp4r_candidate.py` |

## Independent review and protected intake

The worker is not the reviewer. A separate I3 C9/C12 security reviewer must
re-run the exact cut, attack the origin/location projection and C9 schema gate,
and decide whether the preserved RED/HOLDs are correctly classified. Original
owners must ratify the contracts. Protected PRE-MAIN CAS and canonical registry
append remain with the PRE-MAIN owner; this candidate does not touch them.
