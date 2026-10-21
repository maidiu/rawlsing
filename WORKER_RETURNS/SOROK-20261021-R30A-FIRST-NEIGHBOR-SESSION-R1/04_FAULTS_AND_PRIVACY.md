# Source/actor faults, attention privacy and branch checks

Receipt: `evidence/faults.json` (8/8 trials pass) and `evidence/attention_contrast.json`.

All destructive trials are on temporary copies of a real session root. The committed/evidence C12 copies are not modified.

| Test | What changed | Actual result |
|---|---|---|
| `tampered_committed_utterance_refused` | Published A speech text altered without recomputing the event hash | `SessionRefusal: C12_VERIFY_FAILED`; exact body-hash mismatch |
| `recomputed_utterance_identity_differs` | Text altered and hash recomputed | New hash differs from the original committed hash; original identity is not silently preserved |
| `removed_b_offscreen_refused` | B's offscreen episode + world events + perceptions deleted from a copy | `C12_VERIFY_FAILED`; episode/world/perception sequence gaps |
| `removed_user_do_refused` | Admitted user DO episodes deleted from a copy | `C12_VERIFY_FAILED`; episode sequence gap |
| `retroactive_time_refused` | Backdated user episode at clock 1 | `RETROACTIVE_EPISODE` |
| `hidden_actor_state_not_leaked` | User surface/status scanned for private field names and actor identities | No private token appears |
| `attend_without_access` | User travels to market; A remains at workshop; ATTEND/SAY | No A response; no workshop event becomes user knowledge |
| `message_without_channel_refused` | Pressed session, no contact, message attempted | `NO_CONTACT_CHANNEL` |

## Attention contrast

Same sequence (`SAY "Hello. I just moved in."` → `DO help`) executed in two fresh sessions with `attention=focused` and `attention=distracted`:

- event IDs identical: **true**
- event SHA-256 hashes identical: **true**
- user surface differs: **true**
- both C12 verifications OK: **true**

Thus attention selects/omits phenomenal detail; it does not alter the actor/world occurrence.

## Branch/fork check

`tests/test_r30a_first_session.py::test_fork_shares_past_and_verifies_both_branches` forks `first_session` to `alt`, appends an independent post-fork user utterance, and verifies both branches. Shared past is equal; post-fork history differs; both C12 verifies pass.

## Privacy boundary

The user surface never reads actor A's `cash`, `debt_units`, `free_hours`, `material_remaining`, `projects`, practice label, nonmother relations, source hash or actor id. Actor B's private fields are likewise not rendered; `other()` exposes public role/position/completed units only.

`verify` and `custody` are evidence/audit commands, not normal diegetic surfaces. They intentionally expose source/custody identity for Sorok HQ inspection.

## Residual

The R26E qualified verifier detects interior row/hash/sequence tampering. Deletion of a trailing row can leave contiguous sequences unless an external witness/checkpoint archive is used; this is the same local-custody residual documented by R29P. No production KMS or independent witness is claimed.
