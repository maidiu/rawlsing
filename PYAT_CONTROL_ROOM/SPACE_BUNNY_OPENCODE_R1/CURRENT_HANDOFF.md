# HQ188 active two-slot wave — 2026-10-03

Current dispatch supersedes the older "bind repair / consolidate C4" pending wording below as an action item: both jobs are now issued.

- Lane A: `agent/rabochii-pyat-hq188-a-opencode-dispatcher-runtime-repair-r1 @ 2817711c7a1c7129a5c2352fcf604f49bf467286`
- Lane B: `agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1 @ 83c0b9cd538d3e0d7e9dcb8fd183dcc9044be447`

Run both simultaneously. Do not launch a third implementer while both are active. On the first return, route it to HQ for adjudication and immediate slot refill. Lane A requires hostile independent end-to-end acceptance after candidate freeze. All source/warrant/live-execution holds below remain unchanged.

See `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/DISPATCHES/HQ188_TWO_SLOT_RABOCHII_WAVE_R1/`.

---

# Current remote-machine handoff — 2026-10-03

Status: GITHUB_HANDOFF_COMPLETE__CONTINUE_EXISTING_HQ__C4_ADOPTION_HELD.

This is the current operational entry for the user's Space Bunny/OpenCode HQ on another machine. Everything needed to understand these instructions is in this repository. No chat transcript, local Desktop file, or remembered assistant response is a required input.

## Independent publication/runtime audit — current priority

Read [the HQ181–HQ187 review](REVIEWS/HQ181_187_AUDIT_20261003/REVIEW.md) and its [bounded repair plan](REVIEWS/HQ181_187_AUDIT_20261003/REPAIR_PLAN.md). Project Git state is preserved, but the dispatcher has reproduced fail-open/recovery defects and its helper-test PASS is insufficient for unattended operation. Use supervised source-free work while HQ binds a focused runtime repair and separate acceptance. The review also resolves the static 30-versus-32 test-count concern and scopes SRC27's accounting gap. Do not treat the earlier recommendation to use the “qualified dispatcher” as current acceptance.

## Reconcile before acting

Publication baseline: `ef160e9769f9c411c41dfe6afa7ef5fc37defb08`; sealed technical decision HQ187 at `5eb17ffaedb02402f645d8c34d270bc45e49183a`. Read live `HQ_HANDOFF/LATEST.json` and verify the immutable checkpoint it names. A later valid decision supersedes this baseline. Preserve the existing HQ, worktrees, runtime, returns and local changes. Do not rerun activation or re-launch the completed re-check merely because FIRST_TASKS.json or an older LATEST field says pending.

OPS-01 is recorded reconciled, OPS-02 implemented, OPS-03 PASS_WITH_DECLARED_SKIP (23 passed, one skipped: OS-level raw-directory denial). This is inherited status, not proof those capabilities are installed on every host. On the active machine, verify the actual scoped configuration and session bindings without duplicating completed setup. Procedural role restrictions are not OS-enforced isolation. No source runner may launch from this packet.

## Corrections and supersession — read together

1. The original OPS-04 `00_C4_CONSOLIDATED_DECISION_CLAIMS.md` is historical. Its claim that Sol's named four-file byte-identity comparison is false was withdrawn by HQ186. The successor `01_CORRECTED_DECISION_CLAIMS.md` records that withdrawal, but HQ187 subsequently narrows several of its broader assertions. Neither document alone is current consolidated truth.
2. [Exact independent comparison evidence](evidence/C1_EXACT_COMPARISON_20261003.json) and [correction details](CORRECTIONS_AND_EVIDENCE_20261003.md) publish the previously chat-only findings. Four named blobs match. This is not a claim that their whole transitive dependency closure is unchanged.
3. HQ187 records a real dependency difference: physical decoder and codec changed with accepted C3. Its current basis is accepted C3 evidence plus C4C3, while preserving M01's narrower named-file result. Inherit that recorded adjudication; do not turn this delivery into a fresh technical ratification.
4. HQ187 also corrects R7 to include reproduction drift as well as fingerprints, and the R9 accounting count to six of eight sources. Carry the SRC27 full-pass gap explicitly. Read its CURRENT.md/JSON at the sealed commit, not a summary alone.
5. The old HQ184/HQ185 mismatch was observed at `e24d78bd3ad1a10ac099ba67362d305ed559e4bd`. It is historical: current baseline LATEST points to HQ187, and records HQ185 retro-sealed. Do not ask HQ to repair an already superseded snapshot.

Independent re-check return: `afb1eb49bbd2ba49c1cb1c4f0501a35908d161d3` on `agent/opencode-pyat-hq183-c4-disputed-claims-recheck-r1`, path `WORKER_RETURNS/PYAT-C4-DISPUTED-CLAIMS-RECHECK-R1/`. HQ187 has adjudicated it. The stale `BOUND_NOT_LAUNCHED` summary must not cause duplicate dispatch.

## Immediate work — one consolidated outcome

The operating HQ owns this continuation. Produce `ACTIVATION_RETURNS/OPS-04/02_CURRENT_CONSOLIDATED_DECISION_CLAIMS.md` plus a compact machine-readable claim/evidence map, unless a later current successor already exists. Combine HQ186's C1 withdrawal and HQ187's dependency/R7/R9 corrections, keeping historical returns unchanged. Use exact SHAs and distinguish named-file identity, dependency identity, tested composition, accepted authority and live-runtime proof. Do not infer pytest case counts from test-function counts.

Reuse the completed independent re-check. Ask a fresh reviewer only to check the consolidation against those exact findings and any genuinely unresolved consequential assertion; do not commission another full C4 audit. The reviewer checks an immutable candidate, not a moving branch. If the candidate changes materially, invalidate only the affected acceptance.

Prepare one compact external-Astra decision packet containing the consolidated claims, exact sources, any remaining counterexample, stage-separated blockers, proposed disposition and the exact downstream work each decision would unlock. External adjudication remains required by the existing hold. Do not silently mark this delivery as that decision. Continue independent already-authorized work while it is pending.

Then update the operating decision ledger and immutable checkpoint, advance LATEST, verify all published pointers, and return the GitHub entry point and exact remaining decision. A user message or local file alone is not delivery.

## Division of labor, Git and communication

Use one integrating HQ, up to two independent worker slots and one fresh review slot. One task = one bounded commission, exact base, isolated checkout/branch, declared write terrain, acceptance inputs and return identity. Preserve the review branch's historical commission anchor; classify all intervening movement and explicitly bind any successor commission without force-pushing history. Do not synchronize unrelated worker branches merely to make their tips match.

Use the existing supervised HQ workflow until the dispatcher repairs and independent acceptance in the current review pass. Then use the qualified dispatcher and durable task/session/result records for routine messages and completion. GitHub holds commissions, returns, decisions and handoffs; sessions and local queues are operational aids. No shared writable checkout across workers. Only HQ publishes integration state, checking the expected remote parent immediately before a fast-forward update. If another writer advances, reconcile before publishing. A local lock cannot protect a second machine.

See [operating design](OPERATING_DESIGN.md), [activation and qualification runbook](ACTIVATION_RUNBOOK.md), [role prompts](roles/hq.md), [commission template](templates/COMMISSION.md) and [forward trajectory](FORWARD_PROGRAM.md). These remain the complete supporting instructions.

## Forward trajectory and boundaries

Prioritize accepting completed critical work, exact C4 readiness decisions, then authorized independent downstream work. Reuse accepted C5/N5 and N10E. C5/N6, C6/N7, C7 temporal comparability and C8 world/possibility products progress on their actual dependency and authority edges. Maintain the C9 F1–F8 declared-estate evidence ledger; C10 decides seam wake or deferral. C11 is conditional on a real consumer. Do not resurrect accepted C1 repairs or make a canary the whole program.

HQ187's recorded stage register is 0 freeze blockers / 1 warrant-issuance blocker / 1 live-execution blocker / 9 advisory / 1 counterexample. This delivery preserves, rather than independently re-adjudicates, those counts. Freeze adoption, locator discovery, warrant issuance, raw access, live C4, held C7 implementation and actor work remain held until their respective competent decisions.

## Safe refresh on the other machine

From an existing verified `maidiu/rawlsing` checkout, fetch origin and inspect `origin/integration/pre-main-reconciliation-r1`. Read this file directly from that ref with `git show`; a branch switch, reset or clean is unnecessary. If no suitable checkout exists, make an ordinary clone into a new directory. Validate host capabilities there; this packet does not assume either machine's absolute local paths.
