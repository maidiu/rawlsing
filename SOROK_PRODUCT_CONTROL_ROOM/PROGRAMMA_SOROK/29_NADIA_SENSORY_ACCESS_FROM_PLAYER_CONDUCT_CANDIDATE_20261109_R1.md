# PROGRAMMA SOROK 29 — Nadia's situated sensory access to player conduct

**2026-11-09. STATUS: USER-SUPPLIED CANDIDATE REQUIREMENT / DOCUMENTARY BANKING ONLY.**
**BOUNDARY:** Existing Sorok/P2/P3/P4/P5/P6 first consumers; proposed incremental sourcefree engineering proof, **not implemented here**. No new engine, architectural override, native CAN/ADP rule, privileged read, human authority, automatic P7 promotion, Mechanism I/II scope expansion or Mechanism III execution order follows from this record. Mechanism III has been announced as incoming; no authoritative Mechanism III specification has been furnished by this handoff. Do not preemptively relabel this requirement.

## Decision — do not confuse sensation, belief and action

**Observable consequences of the player's actual conduct should be eligible to reach Nadia through Nadia's own situated sensory access.** What reaches her depends on committed events, her actual location, facing/orientation, peripheral vision, hearing, divided attention, obstruction, environment and temporal overlap. What she *makes* of those cues is governed separately by her lawful acquired practices, relations, history, memories, current task and actor-local model of the player. Her own behavior/choice determines what happens next, subject to world material conditions.

Three necessarily distinct causal and epistemic links:

1. **Committed world conduct.** The player enters, stops, speaks, moves, turns head/body, interacts or leaves. Only a source-qualified P2/S46 action/world owner commits actual conduct. Private gaze selections or Nadia's suppositions cannot manufacture a world occurrence.
2. **Nadia's sensory access.** What she can hear, see peripherally or directly, sense of another's presence and notice at this time, given her own position, modality and attention. A physical event is not automatically perceived; mere room co-presence is not omniscience. An absent or unqualified cue must not be invented.
3. **Nadia's interpretation and response.** The same accessible cue may be read as reassuring, ordinary, awkward, intrusive or uncertain. An interpretation can be wrong about the player and still causally shape Nadia's later action. She may turn, continue working, move, speak or do nothing. A belief is not canonical world truth, nor a forced behavior or a statement of her secret real desire.

**Illustrative scene, not an imposed narrative:** Nadia faces a kitchen stove. The player enters and stops behind her. She might hear footsteps stop, register someone near her or glimpse motion at her periphery. She might wonder whether he is looking at her body despite him actually looking toward the refrigerator. Her suspicion may matter if her independently established histories, situation and responses warrant it. Equally, she may not notice or may interpret it in an ordinary, non-sexual way. No system grants automatic certainty to her speculation, infers sexual attention from silence, or claims direct access to the player's private attention. If a private shift of attention produces an actual visible head/torso movement, only that outward movement may become an eligible cue.

## Grounded current-source and adoption facts

- **P6 protected:** [PR #779](https://github.com/maidiu/rawlsing/pull/779), integrated head ea72ce582e7e3d3b27f6e04bd560dae14b228f75, protected merge 0232a28f519f56b45404c439f1cd2a007005d2f4; P5 [#775](https://github.com/maidiu/rawlsing/pull/775) at protected 5e266a80ccfc52da10741e15f6b9076138907758; exact protected documentary [#828](28_P5_P6_PROTECTED_SOURCEFREE_RECEIVING_20261108_R1.md) at 9253064bc9423a0f0ccda4fbdea43c2f54f800c6. These sourcefree engineering merges do not issue original human-science or production grants.
- **P6 house actual behavior:** WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py function perform commits GO as MOVE with changed world position and an action episode, INSPECT_OBJECT as INSPECT, under the actual P4/S46 session. The MOVE event uses _append_event with perceive=(user,), whereas INSPECT additionally calls _perceive_if_present for A and B. The existing presence hook is real but does **not** prove actor facing, audibility, peripheral vision or inferred player intentions. Do not claim that all Nadia perception is absent.
- **P6 runtime:** WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py composes P4 event owner, P6 house perform, S46 PACE and committed user-visible event IDs. P6 attention.py and p6_gaze.json shape **user-facing** exposure; attention.py expressly says no world or actor input is produced.
- **Already proven private gaze:** [P6 gaze proof at a075232f](https://github.com/maidiu/rawlsing/commit/a075232f56b55bcce138df755db20e77e3ec5f3c) changed user display selection under distinct user attention histories while keeping actual conduct, positions, world and Nadia actions identical. This is a scoped negative for private attention influencing actor/world, **not** proof of conduct reaching Nadia via hearing/facing.
- **T4/S46:** Mechanism I [PR #791](https://github.com/maidiu/rawlsing/pull/791), issue [#824](https://github.com/maidiu/rawlsing/issues/824). The material-depth admission determines whether a task's tool is serviceable. D8 remains partial pending a joint P6 gaze/ordinary dispatch comparison; D4 cold exact parent-event restore is separately held. Serviceability does not determine what Nadia senses or whether she chooses to work. Nadia's choice cannot bypass a failed material precondition.
- **Actor/gaze hypotheses:** [PR #776](https://github.com/maidiu/rawlsing/pull/776) and [PR #794](https://github.com/maidiu/rawlsing/pull/794) contain separate unadopted documentary hypotheses about Nadia's self-presentation, actor-local user model, user-facing attention and whole relational constitution. Do not leak the system's user profile or user-of-Nadia profile to Nadia.

## One-scene sourcefree proof through existing runtime — not a miniature replacement architecture

Trace one actual action through existing P2/S45/S46/P3/P4/P6 owners and the ordinary actor behavior path. Prefer existing P6 room/workshop source if sufficient; a kitchen is an example, not authorization to fabricate a new world/person engine. Before proposing a new schema, inspect existing source owners for orientation, hearing, ambient sound, attention, actor-access permissions and source gaps. If they are not present or qualified, expose that as HOLD, not as a made-up sensory fact.

The minimal proposed typed chain, subject to actual ABI reconciliation:

**committed world event + positions/geometry + Nadia's own posture, senses and attention + environment → provenance-bearing, actor-eligible partial sensory cue (or absence/uncertainty) → existing Nadia actor-local evaluation → lawful chosen/performed action or no response.**

A sensory cue must retain the world root, branch, source event ID, clock, actors, location, modality, eligibility reasoning, visibility/audibility and access ceiling. Actor interpretation must be a separately attributed proposition/hypothesis about the cue, never a replacement for it. Neither user renderer nor system-level psychological hypotheses may write actor perception as known. A new actor-local state is not silently constructed if an existing owner can serve the need; no duplicate time/world ledger, new narrator-motive voice, universal suspicion probability, fixed response, scripted sexual interpretation or teleological plot.

## Falsification court — ALL PROPOSED, NOT RUN

| ID | Experimental contrast | Required proof or refusal |
|---|---|---|
| S01 | Same actual player conduct, world and Nadia sensory conditions; change only private P6 gaze/selected surface | Nadia's actual cues and subsequent actor inputs remain identical; presentation alone is not an actor event |
| S02 | Keep private gaze fixed; change one actual perceptible entrance, footstep, turn or utterance through normal action ingress | Eligible Nadia cue may change; exact committed event and modality are traceable; response not compulsory |
| S03 | Identical conduct; Nadia faces/does not face, is nearby/elsewhere or senses are blocked | Sensory qualification varies where source-grounded; no same-room all-seeing model |
| S04 | Identical sound; Nadia is occupied with a competing material task versus free to attend | Detectability/notice may vary; if attention source is unqualified, HOLD instead of asserting a cue |
| S05 | Same qualified cue, different independently justified Nadia history/current relation | Actor-local interpretation can differ without replacing material fact or forcing a script |
| S06 | Real heard footsteps but no actual evidence of the player's gaze | Fallible suspicion is representable as Nadia's own uncertain hypothesis, not objective user motive |
| S07 | No lawful cue; user private gaze changes | Nadia sees no additional knowledge or response; renderer cannot inject user mind state |
| S08 | Same tool/material history, Nadia cues and actual conduct; different private P6 histories through ordinary Mechanism I dispatch | Same eligible actor sensory input and lawful material dispatch; independently satisfy D8/P6 N15 only on an actual combined cut |
| S09 | Hold tool serviceability fixed; vary one perceptible action/cue and Nadia's lawful uptake | Nadia's choice of whether to attempt work can change; physical admission still separately rules whether work succeeds |
| S10 | Forged event ID, stale branch, changed root, missing parent, duplicate replay, cold restore | Fail closed with no false actor memory, cross-branch leakage or duplicate committed action |
| S11 | Identical visible head/body turn with different internal attention, then distinct visible turn with same declared intent | First case invariant; second can influence cue if genuinely observable |
| S12 | Suspicion, denial, silence, apparent avoidance, actor self-presentation | Do not claim infallible mental diagnosis, hidden desire, sexual attention, moral lesson or narrator certainty |

Every executed case must supply exact source commit, real caller, root and branch, event/cue IDs, time/position witnesses, Nadia sensory eligibility and actor input/response receipts, user-privacy invariant, negative controls, test command/exit and independent readback. If not executed, mark NOT_RUN, not PASS.

## Separate receiving gates and Mechanism III boundary

**P6:** Already MERGED at scoped sourcefree engineering grade; do not retrospectively mark P6 unfinished solely because a later sensory capability is missing. Final-head independent S2 and native/source/human rights remain separate holds.

**Mechanism I:** T4 needs a joined P6 gaze + ordinary S46 material dispatch D8 proof. In that counterfactual both material conditions and Nadia sensory cues are fixed. A perceptible head/body turn belongs in a separate sensory proof, where her interpretation/response may legitimately change. This note does not touch the in-flight Mechanism I code.

**Proposed sensory-access tranche:** Future sourcefree engineering and qualified actor-science review, one real scene through existing machine; new, separate entry. No implementer dispatched or actual tests executed by this record.

**Mechanism III:** User says the architecture is incoming. Until the actual specification is supplied and source-reconciled, this candidate is **NOT** labeled Mechanism III and must not predetermine its scope, own implementation owner, or supersede Mechanism I/II. Subsequent architecture must preserve these separate owners and their epistemic boundaries.

The crucial human asymmetry is not a defect: **a real cue may support a mistaken Nadia-side interpretation that has real consequences.** Do not collapse the three histories into one omniscient voice.
