# Source and C12 custody

## Immutable source

- R29P return: `WORKER_RETURNS/SOROK-20261021-R29P-ACTOR-C12-USER-PRODUCT-R1`
- R29P commit: `001b506fa26ae879ff5b6e57138fc2696e12b538`
- R30A startup: `ec7b651052e6e2f0b819b0e59e07d35ced8237f2`
- Vendored code: `vendor/r29p/` — `candidate/`, `r29p/`, `r26e/`, tests and N1 screen. No upstream byte was edited.
- Live pinned modules:
  - `rawlsing_next/m6_actor_safe_expression.py` Git blob `74d9701cdc7dabccf61eb5089498db290c1efd9c`
  - `rawlsing_next/v3_psepf_zero_positive_guard.py` Git blob `e0528d65215cb431196570c38bac4eae94217a1b`
- Exact vendor hashes: `evidence/source_manifest.json`.

## What is actually R29P

The product constructs a real R29P/BP2 joined source on first `start`:

- BP2 keyed C8 journal, external anchor, sealed C9 target, CAN008 response, separate CAN011 authorization, performed E2 and BP4 C10/C12/M6 are produced/verified by the R29P code.
- R29P `R29PProduct`/`JoinedProduct`/`QualifiedC12Store` are used unmodified.
- The `first_session` branch is a C12 fork of the actual R29P `root` branch at clock 10. The original root remains `actor_ids=["A","B"]`.
- Actor `U` (the visitor) is added only to `first_session`, with a product-shell arrival event, perception rows and checkpoints. This is a branch-local product extension, not a new native person.
- The world and actor A/B state are actual R29P snapshots (with the pressed scenario changing A's actual `free_hours` to zero in that branch).

## Persisted C12 evidence

| Artifact | Branch | Verify | Counts (episode/world/checkpoint/perception) | SHA-256 |
|---|---|---|---|---|
| `evidence/c12_available.sqlite` | `root` + `first_session` | both OK | 21 / 11 / 16 / 27 | `e9e054739f19dd50f4511b12d3968bbfa7dd512872ac4b02d4bc606b4e290e23` |
| `evidence/c12_pressed.sqlite` | `root` + `first_session` | both OK | 19 / 10 / 14 / 24 | `59a41d3f0416a14a51091c7e0c8bb7bbdb16dd652e70e1eaa100b7bb259ffdc8` |

Both are verified by the actual R26E qualified verifier: `TEST_ONLY_QUALIFIED_C12_NOT_NATIVE`, `verifier=R26E_QUALIFIED_C12_PREIMAGE`. See `evidence/c12_verification.json` and `evidence/SHA256SUMS.txt`.

Target/consumed custody in the available branch:

- target id: `2ee30a34c285cf794771b8a67bb0b8f26341e2114d0de4d64f2e6d68e64da348`
- compressed source/custody JSON in `evidence/session_available.json`

Target/consumed custody in the pressed branch:

- target id: `441dfe552a9f10b5913fade6a38797fb33081e3475304f757a7c9deeb47bcf15`

The actual A/B source hashes, C8 occurrence/digest, C9 target/consumed hashes, E1/E2, CAN008/CAN011, world snapshot and C12 counts are in `session_available.json` / `session_pressed.json` under `custody.source`.

## Event/utterance commitments

Every actor speech/gesture is a `world_event` with exact `body.text`, `body.gesture`, `body.tone`, `summary`, owner receipt where material, and a content-derived `event_id` + `hash`. The user surface is produced only after that event is written. Exact commitments for the primary session are in `evidence/event_commitments_available.json`.

Examples:

- A: `"Which side of the landing?"` — bound at clock 10.
- A: `"Hold the near edge. I'll check the seam."` — bound after the admitted repair.
- A: `"The seam held. I'm at the market until six."` — bound at clock 70 as a later message.
- A: `"The seam held. You came back."` — bound on reentry.

## Custody limits

This is **local logical custody**, not production KMS. The R26E verifier detects interior row/hash/sequence tamper; a same-user attacker who can rewrite both the SQLite DB and any external witness remains outside the trust boundary (`TRUST_CUSTODY_HOLD`). The qualified verifier alone does not detect deletion of the *last* row/event if sequences remain contiguous; an external witness/checkpoint archive would be required for that. This residual is not hidden.
