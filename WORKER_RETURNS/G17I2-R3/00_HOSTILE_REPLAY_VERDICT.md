# SOROK G17I2 — independent forged-material and C9 repair replay

**Verdict:** `SOURCEFREE_ACCEPT_SCOPED__ENGINEERING_SAME_ASSERTIONS_GREEN__C9_DURABILITY_HOLD__NO_ADOPTION`.

The G17 target return’s three original REDs are real and are repaired under their unchanged assertions. The three candidate blobs are sourcefree and pass the original reviewer and author courts, cold-process replay, and independent deeper-nested/owner-canonical/C9 hostiles. The patch is not a durable C9/C12 integration and does not transfer original source, scientific or adoption authority.

## Identity and custody

- Repository: `maidiu/rawlsing` (private).
- Return branch: `review/sorok-r3-g17-source-security-independent-replay-20261030`.
- Sealed startup: `187fdd11963163dab03c7b061e20067ea1f99134`.
- Prompt head: `c69369408e5fd410d89f717cdd4ae7b4520f097a`.
- Target author repair: `8b9a39da552a224bddf486603179f565003f38bb`.
- Original G17 author: `90d0eb7925de54635559a879ee76fc1b97b9ff61`.
- Original G17I reviewer: `156b84cc8481b65c4196b42574010eb7920d6f44`.
- F3I prior: `97dbe712e4cce8fedd1632d9ac64b4e57a0ac25e`.
- PRE-MAIN pin: `299f41e97a43c67be9cc76a79fa49b48f4e12e54` (read only; not modified).
- Host: `oldMac`, verified locally by `scutil --get ComputerName=oldMac` and `LocalHostName=oldMac`; hostname `Matthews-MBP.lan`.
- Harness: OpenCode (`OPENCODE=1`, process comm `opencode`). Model: `opencode-go/deepseek-v4.1-flash`; MAX requested, actual effort `UNVERIFIED`.
- Session UI title/ID/URL: not exposed to this process. See `SESSION_LOCATOR.json`; status `SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION`.
- Worktree: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/g17i2-return`; test base at `.../g17i2`.
- No original author/reviewer branch, PR #514/#516/#519/#521, PRE-MAIN or incumbent worktree was modified. No original source/native data was executed.

## FINDING — exact reproduction and repair

Original reviewer test `test_g17i_independent.py` blob `83f17006b22271f17c87f4563608de08395d7a1c`; author test `test_g17_material_history_consumer.py` blob `ab422636ef4a0d51f58049275b0fc4d19a609448`.

| Court | Actual result |
|---|---:|
| Original reviewer against original author source | **11 PASS / 3 RED** |
| Patched reviewer, same test | **14 / 14 PASS** |
| Patched reviewer, fresh process | **14 / 14 PASS** |
| Patched author positive | **13 / 13 PASS** |
| Patched author positive, fresh process | **13 / 13 PASS** |
| Independent additional hostiles | **3 / 3 PASS** |

The three original REDs were:

1. `test_forged_material_event_supplying_cash_must_be_refused` — original accepted forged material with cash **100058**; patched `continue_person` returns `None`.
2. `test_future_child_nested_alias_must_be_refused` — original returned `COMMITTED` with nested `metadata.future_child_personality`; patched returns `FUTURE_CHILD_INFORMATION_LEAK`.
3. `test_c9_forged_material_event_must_be_refused` — original returned `ACCEPTED` with cash **100055**; patched raises `C9Refusal("MATERIAL_SOURCE_NOT_AUTHENTIC")`.

The candidate overlay is exactly:

- `candidate/lab_sgi1/continuation.py` blob `705ef1a4568ec84020638b3cf32d348066945e86`, SHA-256 `80823bde…`.
- `candidate/lab_sgi1/pipeline.py` blob `d07bb06c7a44cd337a43c387f55a17906c5307e3`, SHA-256 `b5d19758…`.
- `candidate/c9_handoff_consumer.py` blob `bd7a179e846e4067e324360fc3411806b2a537d4`, SHA-256 `2c043034…`.

Original blobs remain `c9318dcf…`, `fc954993…`, `47e59c12…`. No original test or assertion was changed.

## Independent additional hostiles

I added three reviewer-authored cases against the patched target:

1. **Deeper nested future-child alias** under `joint_material_opportunity.metadata.nested[0].future_child_personality` — refused as `FUTURE_CHILD_INFORMATION_LEAK`; the recursive guard sees list/dict nesting, not just one level.
2. **Owner-canonical material forgery** — canonical material event with `owner_id` changed to `FAKE_CANONICAL_OWNER`, passed to the same `C9.receive_handoff` consumer — refused as `MATERIAL_SOURCE_NOT_AUTHENTIC`.
3. **Genuine canonical material control** — same `receive_handoff` returns `ACCEPTED` with `e2_later_authority = HOLD_UNISSUED`.

The additional test source is embedded in `01_ORIGINAL_NEGATIVES_AND_PATCH_REPLAY.json` (SHA-256 `10f9250a…`). These are separate reviewer tests, not modifications of the original reviewer or author oracles.

## C9 R3B / C12 durability boundary

The target patch is a pure Python material-handoff function. It writes no C9 actor SQLite store, no outbox, no mirror and no C12 branch. “Cold process” replay re-executes the same source in a fresh Python process; it is **not** a durable C9 reopen.

The original C9 R3B branch at `fac064c9c3370d598e9b7469af652ae3504bc4ba` is an **unlaunched test-only actor/mirror harness**, not a G17 handoff consumer. Its writer `c9_actor_r3.py` (Git blob `67f34f69…`, SHA-256 `ee4765e2…`) accepts `PublishRequest`/Rule T/world-receipt fields; its reader `actor_reader.py` (Git blob `5ef6a278…`, SHA-256 `331cdae8…`) reads actor SQLite and exact C12 fork/mirror state. Neither accepts `SOROK_G17_C9_MATERIAL_HANDOFF@1`, none of the G17 candidate files import them, and no adapter exists. C9 R3B tests were **NOT_RUN** here because the branch is unlaunched and its full S36/C12 source closure is not the G17 handoff cut.

**C9/C12 interoperability: HOLD.** A future durable consumer must bind the G17 material handoff to an owner-frozen C9 actor schema and a selected C12 source/fork, with a mirror/outbox and cold reopen. That is not demonstrated by this patch. The original C9 R3B C12 perception/fork RED and source-owner decisions remain open.

## Three courts

- **ENGINEERING:** `ACCEPT_SCOPED` — original 11/3 reproduced, three same-assertion repairs, 14/14 reviewer, 13/13 author, cold replay, 3/3 additional hostiles. No durable C9/C12 claim.
- **SCIENTIFIC:** `TEST_ONLY_MATERIAL_METHOD__NATIVE_ACTOR/PRACTICE/RULE_HELD`. The sourcefree material/conservation result does not prove a native person, independent B actor, acquired practice, Rule A/T or original survey source. M2/MP remain typed HOLDs.
- **AUTHORITY:** `HOLD` — original G17 author, C9 owner, C12 owner and separate reviewer retain all grant/adoption rights. No merge, PRE-MAIN, PR or self-adoption.

## FINDING / INTERPRETATION / HQ ACTION / ACCOUNTABLE OWNER

**FINDING:** The three candidate blobs close the three original G17I REDs without changing the original assertions, preserve author positives, and survive deeper nested/owner-canonical/C9 hostiles. The patch remains an in-memory handoff with no durable C9/C12 consumer.

**INTERPRETATION:** Owner-canonical material authentication and recursive embargo partitioning are the real missing capabilities. The C9 material handoff is bounded E1/E2-adjacent material custody, not full C9 E1/RULE_A/RULE_T/E2 and not a durable C9 store.

**HQ ACTION:** Refer the three candidate blobs to the original G17 author and C9 owner for replay/acceptance; refer the C9 R3B/C12 durability question to the C9/C12 owners. A separate source-qualified reviewer must reproduce this cut before any adoption. Do not merge or promote science.

**ACCOUNTABLE OWNER:** Original G17 author; original C9 handoff owner; C9 R3B/C12 owners for durability; incumbent Sorok HQ for intake and separate reviewer assignment.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** pinned original 11/3, patched 14/14, author 13/13, cold-process replays, deeper nested/owner-canonical/C9 hostiles, exact blobs/JUnit, C9 R3B source read, session custody manifest.
- **REMAINING:** original owner replay/acceptance; durable C9 actor/C12 adapter and cold reopen; C9 R3B source-owner decisions; M2/MP; native Rule A/T.
- **CRITICAL BLOCKERS:** no durable C9/C12 consumer; C9 R3B is unlaunched and interface-incompatible with the G17 handoff; no native actor/practice/source authority.
- **LARGEST PRODUCTIVE MOVE:** original G17 author applies `705ef1a4…`, `d07bb06c…`, `bd7a179e…` at `90d0eb79…` and replays; C9/C12 owners decide whether to commission an adapter, not merge this pure function as a durable store.
- **FLIGHT:** sourcefree local Git/Python only; no original/PRE-MAIN/PR mutation, no self-adoption.
- **DELTA:** the three original G17I REDs are closed under unchanged assertions with preserved author positives and explicit C9 durability HOLD.

## First actual consumer

`lab_sgi1.continuation.continue_person` / `forward_continuation` for the material action; `run_pipeline` `FutureChildPartitionGuard` for nested visible input; `c9_handoff_consumer.receive_handoff` for the bounded C9 material receipt. No production or native consumer.

## Final remote SHA

The ordinary push binds this return. The exact 40-hex SHA is verified by direct `ls-remote` and reported in the final response; it is not embedded self-referentially. No force-push, no PRE-MAIN mutation, no self-review.
