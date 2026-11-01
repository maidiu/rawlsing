# Faults, privacy and expression bounds

## R31E fault receipt

`evidence/faults.json`: **6/6 pass**.

| Trial | What was done | Result |
|---|---|---|
| `committed_utterance_tamper_refused` | Admitted A speech text changed without recomputing the event hash | C12 verifier refuses on reopen; `world_event:3:body_hash_mismatch` |
| `recomputed_utterance_identity_differs` | Text changed and internal hash recomputed | New hash differs from the original committed hash; original identity is detectable |
| `attention_surface_only` | Same occurrence set rendered focused vs distracted | Event ids/hashes identical; surface differs |
| `private_state_boundary` | User asks about cash | `PRIVATE_BOUNDARY`; no private value in speech |
| `unsupported_memory_refused` | User asserts a prior promise never in A's perceived history | `UNSUPPORTED_MEMORY`; no promise invented |
| `chronological_rewrite_refused` | Committed world event backdated in a copy | C12 verifier refuses on reopen |

Additional contrast rows in `evidence/contrasts.json` cover forced intimacy, coercion/guilt, unknown topic, B unobserved vs observed, and prior-help recall.

## Privacy / noncollapse

- The actor-side contract contains actual material fields and source custody for **admission**, not for user display.
- The user surface is composed only from admitted world events and U perception rows. It contains exact speech/gesture/observable action, not actor `cash`, `debt`, `free_hours`, `material_remaining`, projects, actor id or source/history hashes.
- `no_private_tokens` and `no_private_values` are hard admission checks.
- `EXPRESSION_ADMISSION` is stored in C12 for audit; the normal user surface never prints it.
- B's private state is not rendered; B appears only through public role/position/observed events.

## Expression bounds

This is a **structured deterministic baseline**, not open-ended language understanding:

- 60 templates and bounded strategy families;
- exact text is re-rendered from allowed slots; arbitrary prose is rejected;
- unknown/ambiguous input produces a defer/unknown response, not invented facts;
- motive status is `MOTIVE_UNDERDETERMINED` unless the reason is a material/time constraint; no trait, attachment or hidden psychological cause is authored;
- no external actor model is called.

## C12 local-custody residual

The R26E qualified verifier detects interior hash/sequence tamper. Local SQLite and any same-user witness remain within the same filesystem trust domain; trailing-row deletion may require an external witness/checkpoint archive for stronger detection. No production KMS or independent custodian is claimed.
