# Agent A — CG-A go-first substantive handoff to an independent adversary

**Status:** Author-built, S2 TEST_ONLY sourcefree candidate. Not an independent receiving, protected adoption, PYAT/CAN/ADP issuance, human grant, or full rolling-person-world implementation.
**Commission:** [#913](https://github.com/maidiu/rawlsing/issues/913), adversarial receiving [#914](https://github.com/maidiu/rawlsing/issues/914).
**Frozen author:** [PR #915](https://github.com/maidiu/rawlsing/pull/915) @ `8248711fb8ba4ac07c0b0e6e7dfc4decce9352b7`.
**Repair candidate:** [PR #917](https://github.com/maidiu/rawlsing/pull/917), branch `review/sorok-cga-causal-bridge-20261111-r1`, code and test cut `38ecf93c7b1ad6c57a5c420d753eaeac6bb643f4`. Later handoff-only commits do not change this code cut. Review the **actual live PR HEAD** and pin its immutable SHA independently before acceptance. PR #917 targets the frozen #915 author branch, NOT protected PRE-MAIN. Zero merges have been authorized or performed by this candidate.

## 1. Exact artifact and reproduction

Changed paths relative to original PR915 HEAD:
- `.github/workflows/sorok-cga-causal-bridge-r1.yml`
- `WORKER_RETURNS/SOROK-CG-A-OWNER-REUSE-R1/01_EXACT_CODE_CAPITAL_MATRIX.tsv`
- `WORKER_RETURNS/SOROK-CG-A-OWNER-REUSE-R1/02_SELECTED_ABI_AND_CG_BCD_CONTRACT.md`
- `WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/00_RESULT.md`
- `WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py`
- `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py`
- `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py`
- `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/sourcefree_p3_bridge.py`
- this handoff.

From an independent checkout at the **exact candidate SHA** (not the previous protected-base cut):
```sh
python3 -m pip install pytest
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py::test_performed_speech_reads_real_prior_p3_formation
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py::test_outward_conduct_supplies_only_qualified_cues WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py::test_silent_interval_reconsiders_and_commits_only_admitted_speech
```
The repository's own GitHub Actions workflow executes the same selected code families, verifying source Git object identities. CI must be checked at the **exact final HEAD**. A green Actions label alone does not substitute for inspecting assertions and evidence.

## 2. Governing contract, no quiet narrowing

Original [#913](https://github.com/maidiu/rawlsing/issues/913) assigns four CG-A obligations: `CGA-P3-ABI` (P2/P3 owner-root/actor/clock and boundaries), `CGA-POSITIVE-CAPITAL` (existing B1/B3A/HQ300/M01/C9RI capabilities and negative authority), `CGA-COLD-LATER-READ` (real subsequent consumer and source-severance), and `CGA-CGB-CD-CONTRACT` (minimum compatible material/actor/psychology interface, no second scheduler). The full original J1/J2 target (independent mother, dated home, child perception, changed/held actor state and later reader) is **not a delivered CG-A whole-world product**; CG-B/C/D/E remain separate.
The live owner code is: `developmental_recursion/{contracts,engine,model_cycle,p2_owner}.py`, P3 `p3/{p3_owner,state_store,test_rules,projections}.py`, P4 `response.py`, P6 `house.py`, `situated.py`, `run_p6.py`, and P6 actor-scene sensory/experience helpers. Relevant architecture reconstruction also resides in unmerged [PR #911](https://github.com/maidiu/rawlsing/pull/911), which is not protected adoption. `sourcefree` must not be laundered into native psychology or actor rights.

## 3. Strongest earned result (without inflating it)

- Actual existing P3 sourcefree owner formation, cold reopen and later record recruitment is already implemented in the inherited code. The repair did **not** invent a new P3 writer or second scheduler.
- The CG-A author's `MEDIATOR{room:kitchen}` toy uses a separate synthetic PsycheStore and local decision function; it does **not** prove a world write or actual P6 consumption.
- New bridge `qualified_p3_read` calls **existing P3 `test_rules._check_sources` and `projections.activate`**. It validates root/actor/branch/clock, source/registry, preceding B1 mediator time and sourcefree grade. It passes ONLY `ELIGIBLE` candidate identities to the P6 situated packet; wrong role/relation, absent actor observation, and incompatible modes do not get actionable candidates. It writes nothing.
- The P6 reader is actually invoked by `run_p6.experience`, behind an explicit `--sourcefree-p3-bridge` opt-in. A registered **outward/sourcefree actor cue** (rather than a silent invented-memory premise) produces the eligible P3 readset. An injected test interpreter can then select a P6 actor speech event admitted by the existing world writer; no prior mediator or withholding this reader yields no added speech, and restoration restores the effect. Same-world persistence, actual P4/P6 receipts and P3 store head preservation are asserted.
- `21/21` inspectable commit/path/Git-blob source identities in the corrected 23-row CG-A matrix were independently compared to the GitHub source; the two other rows are not fully pinned current-code source tuples. Rows 05/06 contained SHA-256-as-Git-blob mistakes and row 21 an abbreviated old commit; all three were corrected. This is source custody, **not** full functional historical conservation.
- The last *known successful* previous code cut before the activation hardening was `ff11d0e7...` (3 new tests + 1 P6 regression). The revised activation-aware code cut `ddccba7634784912a65d32ec26e532a5c1d3a19e` passed **4 new tests + 1 P6 regression** in [Actions #43159856355](https://github.com/maidiu/rawlsing/actions/runs/43159856355). The subsequent larger suite and strengthened quiet/actor-activity test must be checked at final HEAD before promotion; do not pretend they already passed here.

## 4. Agent A's hostile findings, including self-inflicted errors

1. Original author source matrix mislabeled two 64hex SHA-256 digests as 40hex Git blob SHAs; old S47 commit abbreviation was not a frozen identity. Corrected actual objects and compared all 21 inspectable source tuples.
2. Original `test_selected_common_readset` encoded kitchen/mother utterance inside a synthetic psychological mediator; rejected as a real world/mother writer. Kept P2/P6 world owner separate.
3. My initial bridge wrongly passed *raw* B1 candidate modes to P6 without the already accepted P3 activation/contradiction checks. A hostile agent could use an inhibited, unperceived or contradictory record to induce model behavior. Replaced with existing P3 projection activation, source check and fail-closed conflict handling.
4. My initial test made the model act during a quiet interval based on ungranted historical memory, with no actor-qualified current perception. Replaced primary positive with checkpointed P6 `approach` and actual `outward_cue`, preserving distinction between past disposition and current actor access.
5. I originally assumed two P3 records in the P4 opening because the separate P3 vertical fixture creates two. Actual P4 opening creates **one**. Corrected only after GitHub-hosted execution.
6. I originally compared complete speech event digests across two separately instantiated histories. Those histories have different legitimate source/provenance IDs. Corrected oracle to compare material/speech semantics and subsequently test **same-checkpoint** edge severance/restoration.
7. A user-quiet `wait` can contain **actor-owned self actions or perceived speech**. User silence is not equivalent to actor inactivity. The test must inspect actual actor-local receipts rather than assume no P3 activation.

## 5. Unresolved challenges—real technical gaps, not permissions theater

- No dated `HomePeriodResource`, independent mother actor, actual mother speech admission/child perception or joined multi-period developmental household scene exists in this repair. They are CG-B/C/D/E work, not untested `PASS` labels.
- `P3Owner` is currently focal actor/root/branch bound, with B1 sourcefree `test_rules`; no native ADP016/017/CAN011 state writer, generalized second-actor psychological owner, or multi-sidecar crash atomicity.
- Model-driven behavior is **injected TEST_ONLY**. The test proves that the actual P6 world event writer is reachable conditionally through a source-qualified actor decision. It does **not** prove that a real generated person's native model autonomously chooses that response, or that any psychological memory or long-term trait was issued.
- The bridge remains explicitly **opt-in**, not default runtime/production adoption. Its successful execution therefore does not establish that the canonical end-to-end generated product automatically uses it.
- The `actor_observed` predicate is sourced from P6 admitted self actions, actor-accessible speech or qualified current cues; this is a **coarse sourcefree actor-observation eligibility**, not proof of a scientifically validated causal match of historical mediator to current environmental trigger. Examine whether specificity must be increased before any non-demo integration.
- Historical B1/B3A/HQ300/M01/C9RI candidates have not been exhaustively executed against all current versioned interfaces by this repair. Source exactness alone is not full no-loss conservation. Protected PRE-MAIN source, human/actor consent, Pyat native-science issuer and separated independent receiving remain untouched.
- GitHub runner executes authored tests in an independent environment, **not a separately instantiated independent adversarial reviewer**; this handoff deliberately does not impersonate that court.

## 6. Likely adversarial attack surfaces

- Supply an older B1 record whose selector role/relation conflicts with current P6 scope; ensure P3 projection inhibits it, and even a capable model cannot see the rejected `mode`.
- Two source-correct `joint_check` and `private_check` records for the same eligible scope must produce `CONTRADICTION_HELD`, not nondeterministic adoption of one. Test with a real historical two-record fixture as well as the synthetic query fault.
- Spoof actor/root/branch/clock or mutate source and verify refusal before **any** world, P3 or external speech side effect. Confirm no accidental use of portal-user gaze, private analyst notes, demographic shortcuts or sourcefree registry fallback.
- Test real `P3Owner._effect` transaction phases during failure; inspect P6 state/ledger handling on model exceptions and crash after `session.product.say` but before receipt persistence.
- Test whether configured provider actually understands the `sourcefree_p3` packet and whether its output can hallucinate ungranted personal memories. In particular, source/history identifiers should not appear in public narration.
- Challenge the `--sourcefree-p3-bridge` opt-in as an end-to-end integration limitation rather than treating a configured demo as a production capability.
- Check that the selected existing P4 deterministic consumer already covers some of the asserted B1 causal behavior and that P6 bridge adds only a justified distinct first-consumer edge rather than duplicating the P4 response route.
- Test downstream CG-B material/period and CG-C second-actor compatibility against true P2 roster/snapshot semantics, not just the prospective contract text.

## 7. Significant rejected alternatives and why

- **Make PsycheStore the material-world writer:** rejected; actual P3 is B1 registry/actor-state-bound and can't issue world facts or mother events. The kitchen test was a separate mechanical toy.
- **Introduce a new scheduler or universal person/world/psychology store:** rejected; duplicates the accepted `BatchEngine/RecursionCycle`, P2 world owner and P3 atomic sidecar, creates avoidable conflicting authority.
- **Return raw prior record modes directly to the model:** rejected after inspecting P3 `projections.activate`; could promote inhibited/contradictory candidates.
- **Infer a durable psychological memory from historically qualified P3 records:** rejected; existing payload explicitly says `NOT_GRANTED_AS_MEMORY` and sourcefree B1 issuer remains `MISSING_RULE`.
- **Treat readset-hash intersection as sufficient first-consumer evidence:** rejected; sourcefree actor decision difference and exact same-world sever/restore tests were added.
- **Demand fully native independent-mother life engine within CG-A:** rejected as commission scope violation; CG-A can establish reusable sourcefree bridge/owner contracts without pretending later CG-B/C/D/E implementation already exists.
- **Freeze all work until native source/science authority:** rejected; lawful sourcefree engineering can proceed without conferring rights it does not possess.

## 8. Non-negotiable proof boundaries and next attack criterion

**Engineering:** a scoped sourcefree read-only P3→P6 candidate edge and bounded actual P6 speech/no-speech under injected sourcefree model conditions; test execution must be checked at immutable final HEAD. **Scientific:** native Rule A/Rule T, actual ADP actor memory and historical-developmental inference NOT_ISSUED. **Authority:** no protected acceptance/merge, independent review appointment, actor/human right, Pyat source grant or operated A5 alpha.

A superior successor should first try to falsify *actor access*, *selector inhibition*, *contradiction holding*, *crash replay* and *actual-world compatibility*, then remove or replace this bridge if the existing P4/P3 architecture offers a strictly simpler causally adequate route. They are licensed to improve it. This is an adversarial invitation, not an acceptance certificate.
