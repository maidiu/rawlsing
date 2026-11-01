# SOROK RRIF FINAL E — exact defect repair and first receiving consumer

## Identity and terminal

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `research/sorok-rrif-terminal-a-b-fanin-commission-20261031-r1` |
| Dispatch | `e0d816953e97625e8176f0a16e722927bc786d2c` |
| Worktree | `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-final-e` |
| Observed PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Host / model | oldMac, macOS 13.7.8; local OpenCode / `opencode-go/deepseek-v4.1-flash`; actual MAX effort not independently verified |
| Python / pytest / Git | 3.11.3 / 9.1.1 / 2.39.1 |

**Terminal:** `RRIF_E_REPAIR_AND_SOURCEFREE_FIRST_CONSUMER_EXECUTED__C9_ACTOR_AND_OWNER_ANCHOR_HELD__NO_NATIVE_PERSON_OR_PREMAIN_MERGE`

## What the code actually does

The candidate is the exact RRIF-R2 same-person sourcefree root plus additive
repairs. It performs one real material event, C9 target, C12 continuation,
cold/fork return and read-only encounter for actor A/B:

- source operation `SHARE_TOOL`, B performed, actual C9 target and C8 digest;
- encounter `say` -> `RECIPROCATE`, `do_help` -> `HELP_ACCEPT`, `attend` ->
  `NO_CHANGE`, `wait(30)` -> clock 40, cold `return_session` -> scene open;
- repaired C12 verifier green on intact root and fork, red on tamper, exact
  restore green;
- coordinated SQLite column/branch/perception tamper: `QualifiedC12Store` stays
  green, `GuardedC12Store` red, exact restore green; external owner anchor always
  `OWNER_ANCHOR_REQUIRED`;
- R3 C9C12 reader genuinely reads the R2 root C12 but returns exact
  `C9_SOURCE_MISSING` for `actor_meta`; legacy first-session fork is
  `LEGACY_HELD`; CP-A5 is consumed on its own sourcefree root and its market
  answer remains `UNKNOWN`;
- no actor relabeling, no synthetic C9 row, no forged owner key/anchor.

## Four exact defects corrected

| Defect | Before | After |
|---|---|---|
| R2-T1 C12 verifier | `bp2p4.c12_verify` rejected intact rows because `episode_id` was added after the hashed preimage; the original test had no positive control. | Vendored defect preserved as known source; additive `joined.c12_verify_repair` drops `episode_id` only for episode preimages. Same test now asserts intact GREEN, tamper RED, exact restore GREEN. |
| R2-M1 manifest self-entry | Candidate preimage declared impossible stale self hash/size. | Repaired `RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` explicitly excludes itself from content addressing, records the rationale, pins `source_manifest_sha256` and source/dispatch commits; 638 other files are hashed. The 444 vendor manifest remains exact SHA `7cfcb467…`. |
| R2-C1 raw SQLite trust | Coordinated body/branch/perception tamper could evade the self-hash verifier. | Adopted the R3 guarded reader at the consumer: positive/tamper/restore test proves `SELF_HASH_ONLY__TRUST_CUSTODY_HOLD` when Qualified stays green. No external authenticity claim; `OWNER_ANCHOR_REQUIRED` preserved. |
| R2-D1 C9/C12/CP-A5 weld | R2 C9 store is BP2P4, not C9 actor authority; R2 root has no `actor_meta`; CP-A5 origin actor differs. | Exact typed `INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED`; no relabel, hash rewrite or fabricated provenance. Same-root consumer remains valid for R2 C9/C12; C9 actor and CP-A5 same-root remain owner-held. |

## Three distinct courts

- **ENGINEERING: PASS SCOPED.** R2 original 20/20, R3 extension 9/9, RRIF-E
  repair 6/6, first consumer executed. Receiving patch applies to a clean R2
  base and passes 26/26. This is not independent review or owner adoption.
- **SCIENTIFIC: HOLD.** Sourcefree TEST_ONLY actor/rule/C8/C9/C12 only. No
  CAN008/011 Rule A/T, ADP/SCI05, native B, native C8/C9/C12, Pyat world/N11/N12,
  C11 or human A5. No psychological law is issued.
- **AUTHORITY: HOLD.** No original C9/C12 owner anchor, CP-A5 owner adoption,
  PRE-MAIN merge, production DB, human participant or self-review. Owner key is
  never fabricated.

## FINDING / INTERPRETATION / ACTION / OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| R2 JOIN-E is a real same-person C9/C12 consumer; 20/20 reruns. | It is the strongest bounded sourcefree same-root substrate. | Keep exact R2 vendor closure; use additive repaired consumer. | JOIN-E/C9/C12 owners; independent reviewer. |
| R2's independent verifier was red on intact rows and its manifest self-entry was stale. | The original packet was not acceptance-grade. | Repaired verifier and honest self-exclusion preimage with positive/tamper/restore. | RRIF-E engineer; reviewer. |
| Raw DB coordinated tamper evades self-hashing. | Self-hash is not owner custody. | Guarded reader at consumer; external anchor remains owner-required. | C12 owner/custodian. |
| R2 C9 store lacks `actor_meta`; CP-A5 actor origin differs. | Actor/root/clock cannot be casually welded. | Typed incompatibility hold; no synthetic actor. | C9R/BP4/C12/CP-A5 owners. |
| 444 vendor files are exact, but not a new integration by copy. | Source closure is real; consumer delta is the additive code. | Minimal receiving patch references exact vendor prerequisite and adds only repaired consumer files. | PRE-MAIN receiving owner; reviewer. |

## DONE

- Verified R2/R3 source preimages and reran original suites.
- Repaired T1/M1/C1/D1 at the additive source layer.
- Executed same-root C9/C12/JOIN first consumer with cold/fork, material event,
  encounter, refusal/NO_CHANGE and CP-A5 separate-root read.
- Produced receipt, JUnit, patch, dependency map, rollback and exact owner holds.
- No PREMAIN/Pyat/Programma/other-worker mutation.

## REMAINING

- One independent hostile review of this exact SHA.
- Competent Sorok/PREMAIN owner selective receiving or explicit owner-held packet.
- C9 actor store placement/migration and external C12 owner anchor.
- CP-A5 same-root actor/origin decision.
- Native CAN/ADP/SCI05/Pyat/C11/human A5.

## CRITICAL_BLOCKERS

- External C12 owner anchor/custodian absent.
- R2 C9 is not the C9 actor authority schema.
- CP-A5/R2 BP2 origin actor mismatch.
- No native actor, rule, world or human A5.
- Independent review and owner adoption absent.

## LARGEST_MOVE

The Sorok/PREMAIN owner can apply the minimal additive packet over the exact R2
base, run the 26-test receiving court and the first-consumer receipt, then choose
either the bounded self-consistency consumer or the C9C12 guard plus a real
owner anchor. Do not synthesize an actor or external key.

## FLIGHT

One exclusive S2 worktree, one branch, sourcefree local Python/SQLite/pytest.
No changes to PREMAIN, Pyat, Programma, O-LIVE, owner branches, production DB or
active worker worktrees.

## DELTA

From four independent RED/ceiling findings to repaired positive/tamper/restore
tests, an executed same-root first consumer, exact C9/C12 incompatibility, CP-A5
separate-root read, and a minimal receiving packet with rollback. No native
person, science, authority or merge is claimed.

## NOT_RUN

- The entire 294/97 historical inventory was not reopened, per commission.
- C9 R3B 14/1, BP4R 7/2, B3 ghost, F1CI3, G17I, CAN3, OC5E and M04 original REDs
  were not rerun; they remain preserved owner/court evidence.
- Native CAN/ADP/SCI05/Pyat/human A5 and external anchor issuance.
- PREMAIN merge, production DB, provider calls and independent review.
