# HQ181–HQ187 publication and orchestration audit

Disposition: REPAIRS_REQUIRED_FOR_AUTONOMOUS_DISPATCH__PRESERVE_PROJECT_WORK.

Audit baseline: `051908ebb780e8cec643b71a1992e7ff04d6480e` on `integration/pre-main-reconciliation-r1`. Space Bunny's reported work tip is `ef160e9769f9c411c41dfe6afa7ef5fc37defb08`; the baseline includes the later remote-handoff publication. This is a bounded review of published state, executable dispatcher checks and disputed supporting claims. It is not a full C4 acceptance, a source-access authorization, or certification of either machine's unobserved local activity.

## Result that matters

No production-tree damage was found in the reviewed Git state. The important remaining defects are in orchestration readiness and evidence/control hygiene. Keep accepted project work. Repair and independently qualify the dispatcher before relying on it for unattended multi-agent operation or publication. Existing supervised source-free work with explicit Git/commission checks can continue. Do not reset history or restart the whole Pyat program.

## Verified intact

- The Space Bunny/OpenCode subsection was published in original packet commit `52f0c00890c336abf6921c64d7c0d737d3a75215`, sealed at `55ba382dccb88494d219a945c17efc166e456bd2`. The claim that it was absent from GitHub is false. Searching for VOZHD/SUBSECTION or an Astra-named branch was not a valid test of its documented exact path.
- Both OPS activation/re-check branches currently resolve to `ef160e9769f9c411c41dfe6afa7ef5fc37defb08`; ALT-B reviewer branch resolves to `3a5b2cbc7f1978384268376f3ee493c7c095780b`. Control has subsequently advanced. Worker branch tips need not match control.
- `rawlsing_next` subtree is `2a1ac8e2e4a6769eb953170761453f4ba0c0b7b2` at HQ181 checkpoint commit `9cb9200251088f50be0d89e5b52f8e81cb4b8e87`, original workflow delivery and current audit baseline. The 31-commit comparison from `55ba382d` to `ef160e97` has 35 changed paths, confined to control/handoff and the re-check return; no production paths. This confirms net Git conservation, not absence of unrecorded activity on another host.
- All 193 current ledger rows parse as JSON. The seven HQ181–HQ187 manifests each use `files[].path` and `blob_sha`; all fourteen referenced current-file blobs match the audited tree. The latest delivery checkpoint's two blobs also match, including direct retrieval at its exact handoff commit.
- HQ186 withdraws the erroneous C1 allegation. HQ187 preserves the narrower four-file identity result and records the dependency-closure distinction. Preserve those corrections; do not revive the original OPS-04 draft.

## P1: dispatcher gates can pass without the evidence they claim to require

Audited dispatcher Git blob: `23b1fcc3c9e52838b4738efa3d6266b61f60df7a`. Independent disposable probes demonstrate:

- `validateTask` accepts literal UNBOUND acceptance and commission values. It does not establish a bound commission, allowed role, real commit, existing worktree, or frozen acceptance inputs.
- `publicationGate(task, undefined, 'arbitrary-review-label', undefined, [])` returns true. Two missing candidate identities compare equal; the purported review is not resolved or checked for an approving disposition. Caller-provided paths are not an independently computed Git diff.
- A directly appended ACCEPTED event becomes accepted state without a reviewed candidate or adjudication record. This is a trusted-input event store, not an authority enforcement boundary.

Fix: fail closed on placeholders, missing/non-full identities and missing decision records; resolve actual candidate and review objects, derive the diff from Git, validate disposition and exact candidate binding, and reserve acceptance/publication for the integrating HQ. Test missing values and contradictory evidence, not only different nonempty strings. Do not treat this helper as proof that a real publication was safely gated.

## P1: queue/recovery/concurrency claims exceed the implementation

`submitTask` persists only task ID, attempt, sequence, state, role and base; it drops worktree, commission, acceptance, terrain and session. Reopening that queue cannot reconstruct a runnable commission or stable session. `Store.all` silently drops malformed log lines. A repeated submission at a full slot cap throws SLOT_CAPACITY before deduplication. Deduplication and slot checks are separate read-then-append operations with no lock/transaction. fsync provides durability for a write, not transaction isolation.

The expected-parent helper compares two caller-supplied strings; it does not fetch remote state or atomically publish. The CLI can submit/status/event/print argv but does not orchestrate the process lifecycle. `launch()` spawns and returns a child without durable session extraction, completion capture, recovery reconciliation or HQ notification.

Fix: persist complete immutable task bindings and session/process receipts; use a single enforced writer or transactional store; recover torn writes explicitly, never erase their significance; deduplicate before capacity accounting; bind launch and return transitions to observed process/Git events; publish only with an actual expected-parent race check. Test two real processes racing, interrupted launch, restart and completion delivery.

## P1: OPS-03 does not qualify autonomous OpenCode operation

Audited qualifier blob: `831845ab79f84fcf211ca993aab670a41e401ab5`.

- Q08 creates lowercase result keys, then checks uppercase state names. Every lookup is undefined, so even all-wrong results pass. The independent probe reproduces this vacuous acceptance.
- Q01 checks two queued IDs in the same fixture directory, not two actual workers in disjoint checkouts. Q07 compares strings, not competing publications. Q10 reloads a RUNNING event, not a delivered completion. Q13 counts IDs, not restored commissions/sessions.
- Q11 returns a descriptive success string even when Python is unusable. The output also hardcodes the historical host-repair narrative regardless of what the current probe observes.
- Q09 inspects an argv array. It never verifies that OpenCode accepts it or runs the intended agent/model/commission. Importing an implementation as a module does not by itself establish reviewer independence.

The observed 23-pass/1-skip record remains historical evidence of those assertions; it is not adequate acceptance for the advertised end-to-end workflow. This review identifies additional unqualified capabilities beyond the already-disclosed OS-isolation skip.

Official OpenCode CLI documentation distinguishes `--model provider/model` from `--variant` reasoning effort and provides `--file` for attachments. The dispatcher defaults `--variant` to `space-bunny-free`, supplies no explicit model and passes a prompt pathname as a message. That does not demonstrate the selected Space Bunny/Max configuration or that commission contents were delivered. Verify installed-version behavior on the user's operating host; do not guess a provider ID. Source: https://opencode.ai/docs/cli/ (checked 2026-10-03).

## P2: authority provenance must not become a universal Astra gate

Commit `33d554fd30464ba2c1ea77de1e7030ee98e22bb1` adds the external-adjudicator pointer fields; its parent HQ181 checkpoint already names Astra in comparison metadata. That proves recorded routing, not the human authorization behind it and not a constitutional restriction on every future routine adoption. The supplied report says the user wanted a temporary non-adoption hold. Preserve that actual hold until explicitly disposed of; do not expand it into a standing requirement that all HQ decisions go to Astra.

The publishing assistant also propagated the recorded gate too categorically in earlier handoffs. Correct the distinction: ordinary already-authorized HQ adjudications remain HQ work; model comparison and genuinely reserved decisions get the narrow named review. This audit is not a complete C4 adoption decision and does not silently lift the current C4 hold.

## P2: pointer/schema hygiene needs a bounded migration, not deletion

At this baseline LATEST has 506 top-level keys and the tree has 199 checkpoint directories. Those supersede the report's earlier counts. Historical pending flags coexist with newer completed fields. The latest sealed checkpoint lacks the protocol's explicit dependency graph and complete active-work reconciliation; the publishing assistant's last checkpoint inherited that limitation too.

Compact LATEST to pointer/routing fields only after material current facts have been moved into a complete immutable CURRENT packet and consumers are checked. Record completed versus pending lanes explicitly, including exact full return SHAs. Preserve old checkpoints. The seven inspected HQ181–HQ187 manifests all use a compatible binding shape; a claim that any automation over all historical schemas must break is unproved. Use version-aware adapters, require recognized schemas/nonempty fields, and test current plus representative legacy manifests. Never allow missing-field equality to count as verification.

## Technical claims: retain the evidence at its actual scope

**M01 61/61:** the stated 30 test functions versus 32 pytest cases is not a defect by itself. At exact qualified candidate `46f3bec824c1c9da7037bacf94ec08923bc33506`, `test_pre553_empirical_query.py` has 30 test functions, one parameterized over DENY, OUT_OF_SCOPE and SUPERSEDED_NOT_REPLAYABLE. That accounts for two additional cases: 32. The final court spec at `74a067742a370d4f6296c56140c28cc8acc53e63` binds that candidate and the four named suites. GitHub run 36302391261 and its Execute bounded court step are successful. This review did not rerun the court or retrieve its full execution log (the connector rejected the logs endpoint). Retain recorded 61/61 with that evidence ceiling; do not label it a discovered false count merely from function counts.

**SRC27/R9:** artifact 07 has explicit `expected_full_reads`/`expected_selected_reads` for six sources, not eight. But SRC27 has `expected_full_route_passes: 1`, `expected_full_route_passes_max: 1`, zero retries and a requirement to account separately for opens/hash/metadata/full reads. SRC35 has `fresh_reads: 0` plus a global zero fresh-open budget. Therefore “no budget/constraints” would overstate the gap. The remaining issue is explicit per-layer measurement/limit binding in the eventual issued warrant. Preserve the one-pass/zero-fresh-read laws; do not guess missing counters or equate one route pass with one file open.

**Named files versus dependency closure:** the four M01 files match. That finding does not claim decoder/codec transitive closure equality. HQ187's later dependency qualification must stay separate. No broader C4 safety or execution acceptance follows from this audit.

## Disposition and next work

Follow [REPAIR_PLAN.md](REPAIR_PLAN.md). Publish a corrected capability statement now; keep supervised source-free work available. Bind one runtime repair commission and one separate acceptance review on the operating machine. In parallel, consolidate C4 wording without new source access. Avoid another broad audit or repeated model-comparison campaign. Final technical C4 adoption remains a distinct bounded decision, not a consequence of fixing the dispatcher.
