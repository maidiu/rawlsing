# PREMAIN receiving packet, CAS, rollback and holds

## 1. Candidate location and source identity

```text
Candidate: SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/
Sourcefree closure: JOIN-E 7bf2da302996491ddf34b9a039fea47ac982d135
JOIN-V review:      4387dc818a96fda2d5271672505fbd9da1059703
PREMAIN reference:  8e44ca9c751049d65e6def47600b5c073ee04b29
Source manifest:    444 vendored files, SHA-256 7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126
RRIF candidate manifest: RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json
Sourcefree tests:   20 passed
Grade:              TEST_ONLY_SOURCEFREE_NOT_NATIVE
```

The candidate must not be described as a native person, a PRE-MAIN merge, or
an owner-adopted implementation. It is an actual sourcefree first-consumer
root: `JoinedSession.start/open`, `do_help`, `wait`, `return_session`, and
`JoinedSession.verify` read persisted C9/C12 and actor-limited M6 state.

## 2. Selective receiving diff

The receiving diff is additive and bounded:

```text
SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/
  joined/                      10 modules
  vendor/j/                    J closure (R31J, BP2, BP4, R29P, R26E, BP3, C9R)
  vendor/e/                    E closure (R30A, R31E)
  SOURCE_MANIFEST.json         444 source/evidence entries
  RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json
  tests/test_join.py           exact JOIN test with repository-root adaptation
  tests/test_rrif_r2_c12.py    new C12 preimage tamper/restore test
```

No current PREMAIN file is edited. No existing worker branch is merged,
rebased, cherry-picked or reset. The closure is not a wholesale union of all
Sorok branches; it is a single reviewed JOIN-E sourcefree closure with exact
vendor manifest identity.

## 3. CAS / receiver procedure

A qualified receiver should:

1. Read the final return SHA and candidate manifest.
2. Verify `audit_manifest()` = 444 files, no missing/blob mismatches.
3. Run the exact test command in `03_SOURCE_FAULT...` on a clean checkout.
4. Compare `SOURCE_MANIFEST.json` and `RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json`
   against the final commit.
5. Decide whether to keep this as `SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`
   or selectively copy only the `joined`/`vendor` closure behind a new owner
   decision. No default merge.
6. Use PREMAIN CAS only through the receiving owner; do not mutate
   `8e44ca9c...` or O-LIVE/Programma.

## 4. Rollback

```text
Delete: SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/
Delete: WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/
No PREMAIN/source/native/database state to revert.
No original worker branch changed.
```

The sourcefree test databases are under pytest temporary paths; no tracked
database/key/anchor state is part of the candidate.

## 5. Native and scientific holds

| Hold | Status | Owner |
|---|---|---|
| C4/ADP actor/genealogy/memory | `NOT_ISSUED` | ADP/C4 owners |
| CAN008 Rule A | `NOT_ISSUED` | CAN008 issuer |
| CAN011 Rule T/grant | `NOT_ISSUED` | CAN011 owner |
| C8 D1/D2 writer/key/anchor | `TEST_ONLY_ONLY` | C8 security/custodian |
| C9 native CAS/mirror/outbox | `TEST_ONLY_ONLY` | C9 owner |
| C12 production anchor/custody | `OWNER_ANCHOR_REQUIRED` | C12 owner |
| C11 weld | `HELD` | Pyat/C11 owners |
| Pyat world/N11/N12 | `EXTERNAL` | Pyat HQ |
| Human A5 | `NOT_PROVEN` | Sorok alpha/product owner |
| PREMAIN/owner adoption | `HOLD` | independent reviewer + receiving PREMAIN owner |

The candidate preserves `native=false`, `LIVE_ACTOR_MODEL_NOT_RUN`, and the
targetless/NO_CHANGE behavior. It does not import the original V3 0–100
defaults, Enneagram inference, pseudo-random life events, LLM practice or
sixteen held annual steps.

## 6. Review and adoption

- **Independent reviewer:** distinct I3 hostile sourcefree first-consumer
  reviewer at the final SHA. Must rerun the 20 tests and attack C12/source
  mutation, cold/fork, root allocation and actor knowledge.
- **Receiving owner:** Sorok/PREMAIN owner decides selective adoption; this
  worker cannot self-review or merge.
- **Required reviewer questions:** Does `JoinedSession` consume the intended
  source rather than a vendored lookalike? Is the C12 verifier independent of
  the author state? Does the B source/refusal path remain distinguishable? Is
  the targetless/NO_CHANGE path free of fabricated C9/E2/practice? Are all
  native holds still explicit?

Until that review/adoption, status is
`SOURCEFREE_FANIN_CANDIDATE__OWNER_HELD_WITH_IMMUTABLE_PACKET`.
