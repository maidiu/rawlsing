# OBL059 — EXACTLY ONE FRESH INDEPENDENT HOSTILE REVIEW R1

## Reviewer separation

Reviewer role:

`RABOCHII_INDEPENDENT_HOSTILE_REVIEWER_OBL059_R1`

Review ordinal:

`1`

Repair authority:

`NONE`

Frozen target commit:

`8f209b52f81a5c1bf5ed158782f25f56153ac68e`

The reviewer attacked the frozen target only. It did not modify `positive_applicability_authority.py` or `governed_bounded_court.py`, did not repair the candidate, and no second reviewer was commissioned.

Freeze identity verified before attack:

- authority SHA-256: `20a0bce78f290da4e47146e7a06c478d1f483133cc0a47eb8b1060bbf19a27b2`
- court SHA-256: `2851a5407dbdc9cab71f776cd5327b6262d576da776fba4d3f6032a2306b028b`

Review harness SHA-256:

`5ca8fbf565c3b9dd78a62474d1edf9f4787b1e4bb5f0f661ff3b7a5d6e148dd2`

## Attack result

Attack families executed: `19`

The reviewer confirmed the expected behavior for baseline exact synthetic applicability and ordinary attacks covering missing/wrong scope, ADP-010 self-authorization, V554/CAN-001/CAN-003/routing alias attempts, stale actor evidence, wrong phase actor/world/time, classification self-ownership, and project-current scope.

Three required malformed-binding attacks failed the fail-closed contract:

1. `malformed_actor_bytes`
   - input required binding: non-string `bytes`
   - observed terminal: uncaught `TypeError`
   - message: `Object of type bytes is not JSON serializable`

2. `malformed_world_set`
   - input required binding: non-string `set`
   - observed terminal: uncaught `TypeError`
   - message: `Object of type set is not JSON serializable`

3. `malformed_opportunity_id_object`
   - input required binding: arbitrary object
   - observed terminal: uncaught `TypeError`
   - message: `Object of type object is not JSON serializable`

## Smallest exact blocker

`_check_exact_scope()` correctly detects these required identifiers as malformed, but `_deny()` builds a negative receipt through `_base_receipt()`, which unconditionally computes `proof_sha256 = _sha256(packet)`. `_sha256()` uses `json.dumps()` without a total malformed-input representation. Therefore the rejection path itself throws for non-JSON-serializable malformed packets.

This violates the commissioned requirement that malformed bindings **fail closed**.

No broader semantic or jurisdictional defect is needed to establish this FAIL.

## Hostile terminal

`FAIL__OBL059_FROZEN_CANDIDATE_HOSTILE_REVIEW`

Per command, the worker performs no silent repair and obtains no second hostile review.
