# SOROK C01 AGENT B — adversarial construction handoff

**Relocation note:** this return was originally committed at immutable B HEAD `0fd303e2af23d71b51b068393cfaa6f62d40fe38` under top-level `C01/`. The A relay moved the return artifacts into this directory and fixed only path/import references; the B implementation, evidence and historical SHA are unchanged.

**Packet:** C01, `Stable other-actor identities and dynamic participation without changing Nadia root`, CG-C.
**Grade:** `SOURCEFREE_S2_ONLY`. No native C4/ADP-015, CAN/ADP/Pyat, actor/human/source right or protected merge is issued.
**Opponent:** SAME Pair3 A, session `ses_e31295836ffeW9bYwX9iiMMcXS`.
**Attacked artifact:** A HEAD `7e347c45d991df322b987c4fdc70558b1857d9f6`, implementation `9229698c5ded4e8c77801398d4d0ecc3e7c9ccb3`.
**Branch:** `codex/sorok-duel-c01-b-20261112-r1`.
**B implementation commit:** `0e526f043027e4256b353d42240e80d85ad39265` (parent `7e347c45d`, exact A HEAD).
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a` (programme PR #938).
**Frozen start / B01 cut:** `edbb4b344d54731a527fd415a965bc848ed964e1`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. Exact revised artifact and provenance

Changed product code at B implementation commit `0e526f043`:

| Path | SHA256 | Change |
|---|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/supporting_actor.py` | `35e43d8c924d6ea30b4376ef8bed4a8af5b68dd81d636e1cf9033da4320b9c5a` | Atomic registration/participation writes; cold partial recovery; namespace reservations; actual-store event binding; participation-receipt-qualified actor access. |
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | `baa3d5673d40a73da06620a111c7284340db2721233c95ca8c119fc8a734ef4a` | `P2Owner.__init__` binding invariant; `validate_proposal` private-leak precheck; supporting-actor import. Module-level material functions, `material_fact`, `_realize` admission body, P3 and `house.py` untouched. |
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/test_c01_b_supporting_actor.py` | `ced299462e40ea24e45f5141bbe614acb7377d50fb3a079a99a0e52baaa0e7a7` | 8 discriminating B tests. |

Return artifacts: this handoff, `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/AGENT_B_RECONSTRUCTION.md` (recorded before opening A's handoff/diff), `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/C01_B_ABI.md`, `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/PROGRAMMA_DELTA.json`, `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/impact.json`, `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/evidence/*.log`. A's `WORKER_RETURNS/SOROK-DUEL-C01-R1/` records are preserved unchanged.

**Independent reconstruction first.** `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/AGENT_B_RECONSTRUCTION.md` records the mission rebuilt from the frozen programme (`01`–`05`, the 20261111 user requirement, and owner reconciliation `32` at #911 `b50b1282…`, verified byte-identical here). Core demand: a parent becomes a persistent independent participant in the *same* P2 world while Nadia stays the focal root; registration/admission binds actual registered identities and sources, not format-valid strings; objective co-presence is not an unqualified percept; private parent state does not become child/user knowledge; registration/retry/cold cannot create a ghost or partial actor; C02/C03/C04 must not be faked.

**Governing sources actually read:** the frozen programme files, the 20261111 rolling person–world requirement, reconciliation `32`, B01 A's frozen handoff/ABI/code at `edbb4b344`, and the actual P2/P3/C12/S42/S45 code. The two full ChatGPT Library architecture records remain **NOT_INSPECTED locally**; no contents are claimed from them.

## 2. Independently verified strengths of A

These survive hostile examination and are preserved:

- **Real same-world writer, not test-local state.** Registration uses the actual C12 branch metadata, world `actor_state`/`positions`, an actual `P2_SUPPORTING_ACTOR` episode and `_checkpoint`. Participation uses actual `C12Store.record_perception` and a `P2_SUPPORTING_PARTICIPATION` episode. A's C01 tests pass unchanged (6/6) under B's corrections.
- **Nadia remains focal.** Root `actor_ids`, `P2Owner.actor` and `StateIdentity.actor` stay on the generated focal actor; the parent is a new stable ID. A's and B's tests both assert this.
- **Private state custody was materially improved during A's own turn.** The secret is absent from `world.snapshot()`, the committed event, `RealizedEvent.objective`, `RealizedEvent.accessible` and both public access reads; it lives in the C12 registration episode. A honestly disclosed raw-C12 developer access.
- **Actual C12 perception receipts, not a narrated co-presence.** For a performed focal event, the parent gets its own `co_present` receipt and a public participation receipt; `read_actor_access` returns `NOT_PERCEIVED` with no event for a prior event the parent did not perceive.
- **Duplicate registration idempotence and replay severance.** Identical re-registration returns `UNCHANGED` with unchanged counts; replay re-verifies the perception and participation episode.
- **Honest limitations.** A disclosed the P3 code-pin break, fork/copy non-proof, parent-not-author, non-string leak-scan limit, private C12 developer visibility, and the full P3-slice timeout. Those disclosures are correct and preserved.
- **A's own hostile rework was real.** Moving private state out of `world.actor_state` after discovering it in the event objective is genuine self-correction, not a claim.

## 3. Defects established by execution against A's artifact

All five were reproduced on `7e347c45d` before correction; each is now refused/corrected and covered by `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/test_c01_b_supporting_actor.py`.

### D1 — Owner binding lockout prevents the actual P2/P3 composition (high)

A removed the baseline root-participant invariant from `P2Owner` and made the stored `binding.participants` a mutable declared tuple with a one-way `old ⊆ new` test. On one root:

```text
root-scoped owner (A,B) bound
  -> P2Owner(participants=(A,P))     => P2_OWNER_BINDING_MISMATCH
parent-scoped owner (A,P) bound
  -> P2Owner(participants=(A,B))     => P2_OWNER_BINDING_MISMATCH
```

The ordinary P3 reopen path (`p3_fixture_support/reopen_owner`, `test_p3_owner.py`) constructs exactly `tuple(root["actor_ids"])`. Once a C01 parent-scoped owner opens the same root, that working path is locked out. A's test used a fresh root and never composed the two scopes, so A's "compatible additive" claim is false for the actual consumer chain.

### D2 — Alias/stable-ID namespace collisions conflate parent, root and user (high)

On A's code, `register_supporting_actor(alias=root_actor_stable_id, actor_id=…)` succeeded. `read_actor_access` then resolved that string as the root actor (`viewer.alias="A"`), not the parent. Likewise `actor_id="U"` succeeded, and `read_actor_access("U", …)` resolved the portal user (`actor_id="TEST_ONLY_R30A_USER_U"`), not the parent. This directly violates "no parent/user identity conflation" and the ghost/conflation negative oracle. A's negative tests only covered alias `"A"` (the root alias), not the root stable ID or the user stable ID.

### D3 — Registration is not atomic; cold reopen leaves a permanently reserved ghost alias (high)

The C12 store uses sqlite `isolation_level=None`. A's registration committed the branch `actor_ids` update, then appended the episode, then checkpointed the world. A process death after the branch update leaves:

```text
branch actor_ids: ["A","B","P","U"]
world.actor_state: {"A","B","U"}          # no P
registration episodes for P: none or one
```

Cold re-registration then fails `SUPPORTING_ACTOR_ALIAS_RESERVED` forever. A's own handoff §6 listed this attack surface ("crash between branch update and checkpoint, concurrent registration, orphan episode reuse, cold reconciliation") but did not test or repair it. Cold read tests do not exercise cold retry.

### D4 — Participation writer trusts a format-valid event mapping and writes partially (high)

`record_supporting_participation(session, event=<mapping>, …)` accepted a detached event with a forged hash, clock and kind, and wrote a participation episode and public receipt with the forged values. It never resolved the event from the branch store. Separately, the per-participant loop wrote a perception and episode before validating the next participant; a second-participant failure could leave the first actor partially recorded. This is exactly the "actual registered source/event vs merely format-valid event input" distinction C01 must hold.

### D5 — Actor access is granted by a bare perception row, not actual participation (medium-high)

`read_actor_access` returned `PERCEIVED` for a supporting actor with only a manually inserted C12 perception row and **no** participation episode. Severing the participation episode did not change the read. The reader therefore did not enforce the participation receipt that A's ABI claimed was the boundary, and a forged/bare perception row could expose event content to a non-participant.

## 4. Corrections implemented

### C1 — Root-invariant binding with explicit legacy migration (`p2_owner.py:120-176`)

The binding now stores `{root, branch, source, root_participants}`; `root_participants` must equal the actual root actor tuple. Declared owner participants are validated live at construction and per proposal; they are no longer a second invariant. Legacy rows from the baseline or A's cut are migrated when root/branch/source match and the stored participant list still names the focal actor. Result: root-scoped and parent-scoped owners coexist on one root; the ordinary P3 reopen shape remains valid before and after C01 participation.

### C2 — Disjoint alias/stable-ID namespaces (`supporting_actor.py:252-335`)

Registration refuses: alias equal to a root stable ID, root alias, user alias, or any existing actor stable ID; stable ID equal to an existing alias, root alias, or user alias. Existing cross-space collisions still fail closed in `read_actor_access` (`ACTOR_ACCESS_IDENTITY_AMBIGUOUS`).

### C3 — One C12 transaction for registration, plus cold partial recovery (`supporting_actor.py:79-136, 252-413`)

`_StoreWrite` uses `BEGIN IMMEDIATE` (or a savepoint inside an outer transaction). Branch metadata, private-state episode, world row/position and checkpoint commit together; a failure rolls all of them back. Recovery on cold reopen handles the exact A-era partials:

- branch alias + matching registration episode + no world row → `RECOVERED` from the episode;
- branch alias only, no episode/world row → label reclaimed, full registration written (`RECOVERED`);
- orphan matching episode with no branch/world row → branch restored and row written;
- multiple registration episodes, mismatched episode identity/private hash, or a conflicting live row → fail closed.

Duplicate registration episodes are now detected on the normal idempotent path too.

### C4 — Actual-store event binding and all-or-none participation (`supporting_actor.py:583-685`)

The writer resolves `store.world_event(branch, event_id)`, compares hash/clock/kind/location, and uses the stored event for receipts/episodes. It validates every participant's registration, co-presence and private leak **before** the first write, then commits all perception rows and participation episodes in one transaction. A detached body, forged hash/clock/kind/location, duplicate participation episode, or a second non-co-present participant leaves no receipt or episode. `validate_proposal` also pre-scans the caller-controlled proposal document for supporting private values before an operation is reserved or an event admitted (`p2_owner.py:232-251`).

### C5 — Participation-receipt-qualified access (`supporting_actor.py:725-817`)

For a supporting actor, `read_actor_access` now requires a live registration **and** the participation episode **and** the matching `co_present` receipt at the event clock. A bare perception row, a severed episode, a forged receipt clock/channel, or a receipt without a participation episode refuses `P2_SUPPORTING_PARTICIPATION_SEVERED`. Root-actor access keeps the pre-existing perception-receipt semantics. `verify_supporting_participation` applies the same receipt/episode checks on replay.

## 5. Proof of improvement

All commands were run in the exact checkout with `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider`; logs are in `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/evidence/`.

| Suite | Result | Evidence |
|---|---|---|
| B C01 tests (`WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/test_c01_b_supporting_actor.py`) | **8 passed** in 23.08 s | `evidence/c01_b_supporting_actor.log` |
| A's C01 tests + P2 owner + B01 | **15 passed** in 69.44 s | `evidence/a_c01_p2_b01_regression.log` |
| P3 owner suite | **9 passed, 1 skipped** in 31.75 s | `evidence/p3_owner_regression.log` |
| Engine + model-cycle + recursion-integration + P6 actor scene | **68 passed** in 192.98 s | `evidence/engine_p6_regression.log` |
| Selected P3 vertical-slice cold-reopen/idempotent-replay and actor/user-view tests | **2 passed** in 347.05 s | `evidence/p3_vertical_selected_regression.log` |

Discriminating before/after executions (reproduced interactively against A's code, then re-run after correction):

- **D1:** root owner then parent owner now both open; parent owner then root owner both open; the root-owned admission of a `(focal, parent)` event is replayed byte-identically by the parent-scoped owner and after cold reopen.
- **D2:** all four collision shapes now refuse with `SUPPORTING_ACTOR_ALIAS_RESERVED` / `SUPPORTING_ACTOR_ID_COLLISION`; no branch/world/episode mutation.
- **D3:** injected failure at checkpoint leaves branch/world/episode unchanged; cold re-registration succeeds. A manually created branch+episode partial cold-recovers to one registration episode; a branch-only partial cold-recovers to one live actor row.
- **D4:** forged hash/clock/body and a private-leak detached event refuse with unchanged episode/checkpoint/world-event/perception counts; a two-participant non-co-present call leaves no first-participant receipt.
- **D5:** a bare perception row refuses; after a real participation event the parent is `PERCEIVED`; severing the participation episode refuses; restoration returns `PERCEIVED`.

Preserved behavior: A's six tests pass unchanged; Nadia's root actor list and `P2Owner.actor` are unchanged; the secret is absent from world/event/objective/accessible/public reads; cold subprocess registration is `UNCHANGED` with unchanged counts and a root-participant `P2Owner` opens.

**Actual first consumer demonstrated:** the ordinary root-scoped `P2Owner` (the P3 reopen shape) admits a real S47/S42 event naming `(focal, parent)`; the parent receives its own C12 perception plus a public participation receipt; `read_actor_access` returns distinct focal and parent views of the same event; the parent-scoped owner and cold process replay the same result; `read_supporting_actor` remains public-only. This is the same-world two-actor admission / separate actor-relative perception the packet names.

## 6. Challenges investigated and refuted (including attacks on myself)

- **"A's binding is additively compatible because existing tests pass."** Refuted: fresh-root tests miss the cross-scope lockout. Existing P3 fixture roots use the root tuple; one parent-scoped owner breaks that path.
- **"Moving private state to C12 is sufficient."** Partly valid: the public/child/objective paths are clean in A and remain clean. It is not a confidentiality proof against raw C12 store access; A disclosed that and I preserve the limit.
- **"Cold read proves cold registration."** Refuted: A's cold test only reads. Retry and crash-partial behavior were untested and broken.
- **"Unique actor IDs are enough to prevent ghost participants."** Refuted: alias/stable-ID cross-space collisions and branch-only aliases were ghost/conflation paths even with unique requested IDs.
- **"The P3 code-pin break is the only regression."** Refuted: the binding lockout is a second, composition-level regression; both are disclosed, neither is migrated.
- **"Record function input can be trusted because only the adapter calls it."** Refuted: it is an exported writer boundary; it accepted a detached/forged event and wrote durable receipts. Trusting callers is not an owner check.
- **My own first binding fix** initially ignored legacy participant names. I tightened migration to require the focal actor and to store the root invariant, and added a legacy-row migration test. I did **not** make the legacy participant list an authority.
- **My own participation fix** initially compared only hash/clock/kind/location; A's leak test mutates only the body. I preserved the leak refusal by scanning the supplied document before canonical event equality, so A's legitimate severance/leak test semantics still hold while a non-secret forged body refuses.
- **My own transaction helper** would be wrong if the store already had an outer transaction and the caller never committed; in this codebase the store is autocommit and callers do not open an outer transaction. The savepoint branch preserves the outer unit rather than silently committing it.

## 7. New attack surfaces and remaining incompletions of this B cut

1. **Post-admission participation failure remains ambiguous by inheritance.** The P2 event is admitted before supporting participation is written. If participation then refuses (e.g., an event location inconsistent with co-presence, or a source event containing the caller's private string), the operation reservation is left `NULL` and `P2_AMBIGUOUS_PRIOR_OPERATION_HOLD` applies. The participation rows themselves are all-or-none. E03 owns composite event+participation crash atomicity; C01 must not claim it.
2. **Fork/copy is still not supported, now with an explicit test.** A C12 fork copies the branch actor list, registration episode, participation episode and world row, but `read_supporting_actor` refuses `SUPPORTING_ACTOR_ROOT_OR_BRANCH_MISMATCH` because the registration binds the origin branch. This is preserved as an exact incompatibility, not weakened. Pair1 B's verified-lineage helper `branch_is_ancestor` at `362719b40…` is a future composition input; it is **not** copied, rebased or presumed received here.
3. **P3 code pin moved again.** `p2_owner.py` bytes feed `P3Owner._code_pins()`/config hash. Same-code roots reopen (P3 owner suite green); pre-B01/pre-C01 roots still refuse. No migration was invented.
4. **Registration recovery reclaims a non-root/non-user branch label with no world row and no episode.** That label has no live actor state and no registration evidence; reclaiming it cannot erase a live actor. A foreign actor that exists only as a branch label would be claimed by an explicit registration. This is a metadata assumption, not a live-identity overwrite.
5. **Binding migration ignores stale names in a legacy participant tuple** once root/branch/source and focal presence match. No authority is granted: every actual proposal participant is resolved live against root/registration, and the binding no longer encodes participant scope.
6. **Private-state leak scan is still string-containment based.** Non-string private values are not scanned (A's disclosed limit). My pre-admission scan reduces the committed-event exposure to source-generated collisions, but a typed confidentiality boundary is not implemented.
7. **Self-read authorization is caller-asserted.** `read_supporting_actor(..., as_actor=actor_id)` is an in-process capability convention, not an authenticated actor session. Raw C12 access also remains developer-visible.
8. **No actual SIGKILL test.** Crash atomicity rests on SQLite `BEGIN IMMEDIATE` transaction semantics plus fault injection at the checkpoint; I did not kill a process mid-transaction.
9. **No parent-authored action/utterance, no parent antecedent, no decisions, no relations.** C02/C03/C04/C05 remain open; C01 is identity/participation/perception only.
10. **No full-estate run.** Bounded affected suites only; the prior P6 chronology-proof failure and the full P3 vertical-slice timeout are untouched.
11. **Controller/provider cost is UNKNOWN.** No token/latency/RSS instrumentation was available or invented.

## 8. Surviving disagreements and decisions requiring further authority

- **Participant scope semantics.** I kept `P2Owner.participants` as a declared opening scope and validate every proposal participant live (root IDs, registered supporting IDs, focal present, co-present). C02/C05 must decide whether a later consumer needs a hard per-proposal scope or a relationship/eligibility policy; the binding should not become that policy again.
- **Binding migration acceptance.** HQ/C02 should confirm no downstream consumer relied on A's mutable `binding.participants` equality. The ordinary P2/P3 fixtures did not; the root invariant restores the baseline contract.
- **Fork-aware C01.** Whether C01 registration/participation should follow verified C12 ancestry (Pair1 B's `branch_is_ancestor`) or whether C05 owns fork/relationship lineage is a material ABI decision. I preserved the exact refusal and did not silently adopt Pair1 B's code.
- **Private-state custody.** C12 episode custody is developer-visible; C04/C09/C12 external trust/actor-rights ownership must decide whether a stronger self-read/confidentiality capability is required. Sourcefree engineering cannot issue it.
- **Objective co-presence for existing root actor B.** C01 enforces co-presence for registered supporting actors, not for pre-existing root actors. C05 should decide whether all dynamic participants need the same rule without breaking the received P2 fixture.
- **Private-leak post-admission residual.** If a trusted source event contains the caller's chosen private string, the writer refuses after admission. The caller-controlled proposal path is pre-scanned; the residual is a composite-commit/E03 question.
- **P3 old-root migration.** Deliberately not invented; old roots need recreation or an owner-authorized migration.

## 9. Challenge to SAME Agent A

The strongest unresolved problems I could not finish inside C01, in order:

1. **Make C01 fork-lawful without weakening branch provenance.** Compose with the verified C12 lineage direction Pair1 B built at `362719b40a35a66fa2fb1c3490db8eb5b8e9167c` (do not copy it): a fork of `first_session` currently copies the parent's branch actor list, registration episode and participation episode, but `read_supporting_actor` refuses `ROOT_OR_BRANCH_MISMATCH`. Prove that a forked branch can read the same stable parent ID and its participation while a non-ancestor branch still fails closed, and keep the fork's own new registrations separate.
2. **Close the post-admission participation ambiguity.** Pre-bind the participation plan to the actual event's source location or integrate with E03's composite commit so a refused supporting participant cannot leave the P2 operation `NULL` after the event is durable, and an actual retry reconciles exactly once.
3. **Prove real cold crash atomicity at the branch/episode/checkpoint boundaries**, not just in-process fault injection (e.g., SIGKILL in a subprocess between instrumented writes, then cold reopen and exactly one registration).
4. **Attack the private-state boundary with structured values**: make a typed or path-based non-leak proof, not string containment; show a non-string secret cannot enter any outward/child projection.
5. **Then, and only then, add the next actual actor-authored operation** (C03 direction) through the same stable identity and a real downstream consumer, without a second owner/scheduler and without changing Nadia's root. A registration/reader-only improvement cannot defeat a real parent-authored event.

**Hardest concrete falsifier for my cut:** on one actual root, construct the ordinary P3 `reopen_owner` shape and a C01 parent-scoped owner in either order around a real `(focal, parent)` event, cold-reopen, then fork the branch and prove the parent identity/participation is either lawfully readable through verified lineage or refused for every non-ancestor, with no duplicate registration, no ghost alias and no private value in any outward read. If A can do that while keeping the P3 owner suite and A's six C01 tests green, A has genuinely surpassed this return.

## Measured cost and limits

Test wall time above; controller/provider token, latency, process RSS and retry cost are `UNKNOWN` (no instrumentation available; none invented). The two full Library architecture records remain NOT_INSPECTED locally. This is a sourcefree engineering candidate, not native actor identity, actor/human/source authority, independent acceptance or a protected merge.
