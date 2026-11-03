# 02 — Two actual-source transitions, cross-cut freshness and qualified negative control

**Review subject:** LIVE-01 guide `2aec26709fe1d28480de1109c0a52b460d9ed8b3`, descended from frozen W8-R `a9ebf71e62d84e5dcc599662e976eca7fcd0e623`. **Engineering candidate:** source `bbcc46bf3b7aadfc582e284daea61f99060e0fc3`, execution receipts `6a63d19e73ecc814661ffaec6410a2dce711665d`. The following is an **independent Git-source documentary replay of two real historical transitions**, not an independent Python test or native HQ transaction. LIVE-02 executor reports 35/35 and P0/P1 62/62, and a cold journal head and digest. These reports are not silently rebranded as independently run.

## Sequential transition A — reviewed sourcefree 7bf, exact same-root scope

Real issuer/subject: JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`, [return](https://github.com/maidiu/rawlsing/blob/7bf2da302996491ddf34b9a039fea47ac982d135/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md), source blob `9a185f7c03ac66056e366a2deecf4ea4dd2da188`. Independent JOIN-V exact cut `4387dc818a96fda2d5271672505fbd9da1059703`, [review](https://github.com/maidiu/rawlsing/blob/4387dc818a96fda2d5271672505fbd9da1059703/WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md), blob `52dfc715bed3ef14cc3dc4639132c409c4e99712`.

1. Existing scoped E021/JOIN-E 7bf source record acquires an exact **reviewed sourcefree fork/lineage/atomicity** receipt.
2. Existing first reader: `JoinedSession.start/open/fork_alt` at 7bf `joined/session.py`, as preserved by guide `15`, original E021. Positive/control: valid fork and cold reopen; invalid empty fork leaves no branch.
3. **Changed node:** `JOIN_E_7BF` reviewed 7bf scoped state, not the native C12 source/custody axis. **Changed edge:** E021@VERIFY 7bf exact-source reviewed candidate; reverse E008/C9/C12 work edges are candidates only, not all-member grants.
4. **Unchanged:** 38 full seam joins still pending; C9 original Rule A/T, C11 Pyat, selected C12 reader/root/anchor, C10 chronology, S14 operational rights and Gate5 all held.

## Sequential transition B — independent 598d negative on a different packet

Real subject `598d9e9eaba5143950c63317705fd09104fbf463` [RRIF R2 return](https://github.com/maidiu/rawlsing/blob/598d9e9eaba5143950c63317705fd09104fbf463/WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md), blob `9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53`. Independent negative `8090a1ea308ab17f302f55bb2639c3e4cd774c7a` [review](https://github.com/maidiu/rawlsing/blob/8090a1ea308ab17f302f55bb2639c3e4cd774c7a/WORKER_RETURNS/SOROK_RRIF_R2_INDEPENDENT_HOSTILE_FIRST_CONSUMER_REVIEW_R1/00_RETURN.md), blob `38c201199c3153ca58926b2f96b3ba0220d2b651`.

1. R2 author reports 20 tests; reviewer independently reproduces them but finds **R2-T1 false verifier positive control, M1 stale preimage self-entry, C1 weaker C12 coverage, D1 C9C12 incompatibility**. The 598d source cut is **REVISE_MATERIAL_DEFECTS**.
2. **Changed node:** `JOIN_C12_HOLD@598d` exact negative/reviewer grade. **Changed edge:** new tuple's C12/C9 reader and root compatibility cannot be accepted from 598d. Work-now changes toward exact joint owner tuple, source/clock/root, independent new-candidate tests.
3. **Unchanged:** 7bf JOIN-V accepted scoped fork evidence remains genuine **only for 7bf**; 598d RED does not revoke it, and 7bf review does not heal 598d.

## Negative and counterfactual documentary probes

| Mutation | Expected truthful result | Source-checked result / limitation |
|---|---|---|
| Transfer old 7bf review to 598d reader/root | Refuse full new-root C12/reader acceptance | W8-R `G-C12-SF-VERIFY` requires NEW_TUPLE proof; LIVE-02 `_positive_join_e` pins subject/source/review/root 7bf |
| Remove 7bf qualified independent review | `PENDING_REVIEW`, no `SCOPED_SOURCEFREE_ACCEPTED` | In pinned replay code `_positive_join_e` demands exact 4387 review; independent destructive execution **NOT_RUN** |
| Withhold R2 negative | Do not infer acceptance; R2 independently unreviewed | Exact reviewer receipt absence cannot become a positive member; independent journal mutation **NOT_RUN** |
| Add sourcefree S35 T_NO_CHANGE | Does not satisfy original O07 evaluated no-change or Rule T | W8-R `G-C9-NATIVE-INTEGRATE` **AND** `G-C9-T-ANY` still held |
| Complete selected C9/C12 sourcefree adapter only | Permit exact tuple testing, not C12 native READY | C11, C10, C9 original, external C12 anchor remain independently held |
| Remove operational S14 receipt | A5 human Gate5 remains blocked | `G-A5-RUN-COMMON` and `G-S14-CONTROLS-VERIFY` require actual operated rights |
| Request S10@SPECIFY without E021 review | Continue source-based specification | `G-S10-SPECIFY` `READY_TO_SPECIFY_FROM_EXISTING_SOURCE_NO_E021_BLOCKER` |

## Cold/currentness boundary

LIVE-02 [executed cold evidence](https://github.com/maidiu/rawlsing/blob/6a63d19e73ecc814661ffaec6410a2dce711665d/WORKER_RETURNS/SOROK_PROGRAMMA_LIVE_UPDATE_ADAPTER_20261103_R1/06_COLD_REPLAY_AND_SEVEN_VIEW_RECEIPT.md) reports revision 4, matching warm/cold digest `a3f84a2afb21546e023f30d69bfdd36e44f85395fccf874218de076968c4dba6`, seven views and sourcefree readback. **This reviewing session did not execute pytest or cold-rebuild from an independent checkout.** The reviewed adapter's `freshness` view explicitly says no daemon/background fetch; it does not prove that a newer HQ guide or worker branch was autonomously observed. Its `GUIDE_SHA` remains frozen W8-R, not LIVE-01 `2aec`, and does not incorporate the COVER-01/-02 returns or the final LIVE-02 receipt. No actual HQ source→current guide transition after these four inputs was independently observed; do not fabricate one.

**Decision:** documentary sequential cross-cut semantics and negative/nontransferability are source-supported; exact new-root acceptance, independent cold Python proof, and post-all-returns automatic living-guide freshness are **HELD**. The missing proof should be repaired at its exact component/root, not converted into a new management architecture.
