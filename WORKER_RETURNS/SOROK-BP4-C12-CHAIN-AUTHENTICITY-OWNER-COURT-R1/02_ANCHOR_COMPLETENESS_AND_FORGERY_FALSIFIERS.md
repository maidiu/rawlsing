# BP4/C12 anchor, completeness and forgery falsifiers

## Scope and method

All probes were executed locally against the immutable BP2P4J return tree at `5b3e6577400ea1d88971ae6b48e41a118b8059ae`, overlaid only with the F2 candidate verifier and then with the `C12_GUARD_READER@1` candidate. The BP4 source was not edited. No native data, secret key, signer, source issuer or production database was used. The point of this document is to separate three questions that are often collapsed:

| Question | What answers it | What it cannot answer |
|---|---|---|
| Does the stored preimage hash to the stored hash? | content verification | who wrote the row |
| Does a child branch copy the parent prefix and perception set? | fork verification | whether the parent is authentic |
| Is a row missing, injected or fully rewritten? | an owner-issued authenticated anchor plus a monotonic counter | nothing by itself; lacks authority |

## 1. F2 preimage repair versus original BP4 verifier

Base: `WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1` at `5b3e657`. The F2 candidate overlays `bp2p4/c12_verify.py` blob `c1699c8d…` and adds the focused test blob `ebe1e828…`.

Exact positive row from the fresh SAY:

```json
{
  "episode_hash": "c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be",
  "episode_id": "TEST_ONLY_BP4_EP_c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be",
  "independent_verify_ok": true,
  "upstream_verify_ok": false,
  "upstream_errors": ["episode:0", "world_event:0", "world_event:1", "checkpoint:0", "checkpoint:1"]
}
```

The dependent test on the unmodified verifier fails exactly:

```text
FAILED tests/test_episode_verifier_regression.py::test_valid_say_episode_is_green_and_preserves_the_post_hash_id
AssertionError: episode:0:body_hash_mismatch
```

The cause is not a data defect. `append_episode` hashes the episode body and only then appends `episode_id`; the original verifier removes only `hash` and therefore hashes the post-hash id. The F2 verifier removes both and separately requires the body id to equal `TEST_ONLY_BP4_EP_` plus the body hash. The BP4 `C12Store.verify` remains self-referential and returns red on the same valid store. This is an independent reproduction of the F2I finding, not a transfer of its acceptance.

Test counts actually observed in this checkout:

- original suite: **32 passed, 1 skipped** (`BP2_ORIGIN_RUNTIME_ABSENT`, local-only literal cross-check);
- focused test on original verifier: **1 failed**, exit 1;
- F2 overlay: **37 passed, 1 skipped**;
- F2 plus guard candidate: **48 passed, 1 skipped**.

The F2/F2I documents report 33 and 38 because their runtime had the literal BP2 origin mounted. The skipped assertion is not a pass; it is a typed local-only HOLD.

## 2. Raw SQLite deletion

The attack closes the product, opens the same SQLite file directly, drops `episode_no_delete`, and deletes the only real episode. The remaining rows are internally intact.

Observed:

```json
{
  "deleted": 1,
  "content_verify_ok": true,
  "errors": [],
  "episode_count_before": 1,
  "episode_count_after": 0,
  "chain_digest_changed": true,
  "anchor_payload_changed": true
}
```

Interpretation: content verification cannot detect a missing row because there is no missing hash to recompute. The unkeyed chain digest changes only if a trusted copy exists. The guard exposes this as `OWNER_ANCHOR_REQUIRED`; with a prior owner anchor whose payload covered the old chain, the payload comparison returns `ANCHOR_PAYLOAD_MISMATCH`. Without an owner-issued anchor and protected copy, deletion is a HOLD, not a closed guarantee.

## 3. Self-consistent injected world event

The attack inserts a raw `world_event` at the next sequence with a body and hash the attacker computed:

```json
{
  "event_id": "INJECTED_WORLD_EVENT",
  "clock": 11,
  "kind": "POSITION",
  "summary": "raw injected event",
  "hash": "<attacker digest>"
}
```

Observed: `verify_branch_chain(...).ok == true`, errors `[]`, counts include `world_event: 3`. The verifier checks body/hash agreement and sequence contiguity only; it has no producer signature or world-owner anchor. The guard's anchor payload changes, but absent an owner anchor it is still HOLD.

## 4. Fully rehashed episode forgery

Given a valid SAY, the attack drops `episode_no_update`, rewrites `body.event_id`, recomputes the body hash, recomputes `episode_id = TEST_ONLY_BP4_EP_ + new hash`, and updates the row hash. The row is now fully self-consistent.

Observed:

```json
{
  "content_verify_ok": true,
  "errors": [],
  "old_event_id": "TEST_ONLY_BP4_WORLD_EVT_c78bec4240a980c4724272b88bff0637b2328846341a7e8ec8bbf0dfee1ee31b",
  "new_event_id": "FORGED_EVENT_ID",
  "new_episode_id": "TEST_ONLY_BP4_EP_6810b0911571a53106253f365433f982ea13d0297a13867bb41db31484b269c8",
  "chain_digest_changed": true,
  "anchor_payload_changed": true
}
```

A simple id-only tamper is refused (`episode:0:episode_id_mismatch`; legacy prefix refused). A fully rewritten row is indistinguishable from a legitimate row by content hashing alone. Only an external authenticated anchor can distinguish it.

## 5. Perception channel substitution

Perception rows have no hash. A raw update of `perception.channel` (after dropping the trigger) leaves content verification green. The guard's chain digest includes `actor_id`, `event_id`, `clock` and `channel`, so the anchor payload changes and an owner anchor would detect it; the unanchored read cannot. This is a residual completeness/authenticity fact, not a preimage defect.

## 6. Fork prefix, perception clocks and atomicity

Original BP4 fork defect:

- non-perception last clock: 10;
- perception rows at clocks 10 and 11;
- original fork clock: 10;
- copied rows: `clock <= 10`, so the perception at clock 11 is lost.

Observed on the original store: child has one perception. Observed on the guarded store: fork clock 11, child has both perceptions, `BP4_C12_FORK_ROOT@2` prefix, `VERIFIED` status. A failed copy after the world-event table leaves no branch row and no copied rows; the root still verifies. A tampered child perception yields `perception:prefix_mismatch`; a legacy root yields `LEGACY_HELD` and a subsequent fork raises `FORK_HELD`.

C9's `c12_fork_guard` (commit `1e99681f…`) was independently run against the same state:

- normal branch: `FORK_READY`, cut 10;
- perception-only suffix: `FORK_HELD / C12_PERCEPTION_ONLY_SUFFIX`, cut 11, `nonperception_last_clock=10`, `perception_last_clock=11`.

This guard remains fail-closed and is not silently relaxed by the store repair. The owner must decide whether to keep `FORK_HELD` or accept the repaired store's perception-inclusive fork. No old JOIN-V acceptance is transferred.

## 7. Source severance

The same named assertion `bp2p4.assertion.joined_downstream_a0_a2_assertion` was rerun over 7 primary and 3 supplementary cuts. Every trial was baseline `red=false`, cut `red=true`, restored `red=false`; `all_primary_proved=true`, `all_supplementary_proved=true`. The ten edges are the seven documented plus `BP2_OTHER_HISTORY_ALIASED`, `BP2_E2_NOT_PERFORMED` and `BP2_PRACTICE_NOT_MATERIALIZED`. No assertion was substituted and no test was weakened.

## 8. Checkable hashes versus authenticated source and completeness

- A **content hash** proves internal consistency of a preimage. It is not a signature and not a producer identity.
- A **derived episode id** proves conformance to the pinned writer code. It is not proof of who ran the writer.
- A **chain digest** is an unkeyed value. It detects a change only against a separately trusted copy.
- A **fork root** proves a copied prefix and perception identity. It does not authenticate the parent.
- An **authenticated anchor** is the only object that can bind a chain state to an owner. It must be signed over the exact payload and its sequence must be monotonic outside the database.

Concrete trust boundary required:

1. **Issuer:** original BP4/C12 owner or an owner-designated independent anchor custodian, distinct from the writer process and from this worker.
2. **Key custody:** owner-issued key/certificate or equivalent, pinned out of band; no key in the repository or SQLite file.
3. **Payload:** `SOROK_C12_EXTERNAL_ANCHOR@1` over `{reader_version, branch_id, chain, counts, fork_status}` plus a monotonic `sequence`.
4. **Replay protection:** the verifier holds the last accepted sequence outside the database and refuses an older signed anchor (`ANCHOR_ROLLBACK`).
5. **Coverage:** the anchor covers only the chain state at its sequence; later rows require a later anchor.
6. **Same-user HMAC:** explicitly not a security boundary. The 68b058 `ExternalCheckpointWitness` is `TEST_ONLY_SAME_USER_EXTERNAL_WITNESS_NOT_SECURITY_BOUNDARY` and retains `TRUST_CUSTODY_HOLD`.

This candidate implements the fail-closed verifier side only. It never creates a key or accepts a test fixture as an owner. Until the owner issues the trust root, every anchored claim is HOLD:

```text
OWNER_ANCHOR_REQUIRED
ANCHOR_MALFORMED
ANCHOR_SCHEMA_UNSUPPORTED
ANCHOR_PAYLOAD_MISMATCH
ANCHOR_ROLLBACK_WINDOW_UNPROVEN
ANCHOR_ROLLBACK
OWNER_TRUST_ROOT_ABSENT
ANCHOR_SIGNATURE_INVALID
```

## 9. FINDING / INTERPRETATION / HQ ACTION / OWNER

**FINDING:** The F2 episode-preimage repair is correct and independently green on a valid SAY. Raw deletion, self-consistent world-event injection, fully rehashed episode forgery and perception-channel substitution remain content-green; only a chain digest change is visible, and no owner anchor exists. The original BP4 verifier is separately self-referential. The original fork drops a perception-only suffix; the guarded fork preserves it atomically. C9's guard remains conservatively `FORK_HELD`.

**INTERPRETATION:** The repaired hash syntax is necessary but not sufficient for C12 custody. The remaining failures are authenticity and completeness, not hashing. They cannot be closed by sourcefree code alone; they require an owner-issued trust root and monotonic anchor, or an explicit owner HOLD.

**HQ ACTION:** Accept the bounded engineering evidence for the exact preimage/schema/fork cuts. Do not describe it as C12 authenticity, completeness, native C12 or adoption. Route anchor issuance to the original owner/custodian and keep deletion/injection/rehash as HOLD until a real anchor exists.

**OWNER:** Original BP4/C12 store owner; original BP2P4J verifier owner; C9-R3 owner; independent anchor custodian; incumbent HQ and a distinct source-qualified reviewer.

## 10. Commands actually run

```sh
# base checkout
git worktree add --detach /private/tmp/bp4c12-f2-base 5b3e6577400ea1d88971ae6b48e41a118b8059ae
cd /private/tmp/bp4c12-f2-base/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -v

# F2 focused RED and overlay
cp <f2-candidate-test> tests/test_episode_verifier_regression.py
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest \
  tests/test_episode_verifier_regression.py::test_valid_say_episode_is_green_and_preserves_the_post_hash_id -q
cp <f2-candidate-verifier> bp2p4/c12_verify.py
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -v

# independent adversarial probe
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 /private/tmp/bp4c12-probe.py

# guard candidate
cp <guard-candidate> bp2p4/c12_guard.py
cp <guard-test> tests/test_c12_guard.py
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_c12_guard.py -v
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -v

# 68b058 fork suite
cd /private/tmp/bp4c12-join68/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_c12_fork_integrity.py -q

# C9-R3 suite
cd /private/tmp/bp4c12-c9r3/SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_c9_r3.py -q -rs
```

Exact exit observations: RED focused test exit 1; all other listed suites exit 0 with the counts in `00_RETURN.md` and `04_...json`. The C9 suite has 4 typed skips and is not reported as 15 PASS.
