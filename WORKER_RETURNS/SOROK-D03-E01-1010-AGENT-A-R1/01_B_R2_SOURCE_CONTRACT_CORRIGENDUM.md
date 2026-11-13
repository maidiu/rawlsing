# SOROK #1010 — A source-exact correction to B R2 and terminal prospective owner disposition

**Status:** `B_R2_REAL_POST_J1_FAIL_FAST_PRESERVED__PREEXISTING_PENDING_TEST_CORRECTED__V3_PROSPECTIVE_OWNER_MAPPED__G2_HELD__FULL_NATIVE_NOT_RUN__STOP`

**Read grades:** source-inspected original J1/D03/P2/P3 and B #1025 at `42fc7178dee968ee642943e31c0830dee9cfe988`; exact changed test syntactically executed against matching Git blob. No production event, actor, native scientific or independent receiving proof is claimed here.

## 1. Exact reciprocal ancestry

- Original J1 PR #996 author `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`, composed code `c724d1a89626f3e177acd004c0be20029dc7ade4`.
- Original A #1016 `6248547b2ad98002245b69cec9e399277d090f12`.
- B #1019 `6bfdc3b91b1c77577fdf5545e16ed866016213d4`.
- A #1022 `9e8b219bb1136a2c6fbe33e4903e850d7816b62a`.
- B R2 #1025 `42fc7178dee968ee642943e31c0830dee9cfe988` — **parent of this exact optional final source correction**.
- Original protected PRE-MAIN read-only `6a5c12f04323d74001f9632063ec907f4fc4468e`.
- A R3 branch `agent/sorok-d03-e01-1010-a-exact-source-corrigendum-r3`; no other branch/owner edited. This is **not** a new reciprocal duel or G5.

## 2. B's true improvement and false scope attribution

**Concede B's valid repair:** `d03_e01_performer.run_d03_e01_first_batch` now calls the existing `precommit_custody()` before constructing `BatchEngine` or `RecursionCycle`. It can reject a pending P3 reservation **arising after J1 has established the D03 readset but before the external provider is invoked**, avoiding a needless provider call and durable cycle HOLD. Preserve that line.

**Correct B's exact test and advertised original defect:** B R2's `test_preexisting_p3_pending_refuses_before_provider_and_cycle` injected `owner.store.pending()` **before** `_invoke`, then expected `E01_POSTPROVIDER_P3_PENDING_OPERATION`. But the original, read-only `p3/immediate_uptake.py:build_immediate_uptake` calls:

```python
store = getattr(owner, "store", None)
if store is not None and hasattr(store, "pending") and store.pending():
    _refuse("D03_PENDING_OPERATION")
```

This precedes qualified uptake, prior P3 query and provider call. `j1_join.compose_j1` calls that function for **both** perceived and held child-uptake paths; the new B preflight is later in the caller. Thus **preexisting pending already failed before A's provider**. The original B test was authored but NOT_RUN and would expect the wrong error. That is a real test-oracle defect, not evidence B introduced a behavioral regression.

**Repair:** replace the original one-case test with two independent full-fixture negatives in the same file:

1. `test_preexisting_p3_pending_is_already_rejected_by_d03` — original early D03 refusal, no model call or files; exact `D03_PENDING_OPERATION`.
2. `test_pending_first_appears_after_real_j1_before_provider` — run the real `j1_join.compose_j1` and only then inject a pending reservation; the newer B preflight must refuse `E01_POSTPROVIDER_P3_PENDING_OPERATION` with zero model/world writes and no cycle/journal. This is the actual incremental B R2 advantage. It uses a monkeypatch after a real J1 receipt; it does not claim a persisted native reservation.

**Source-exact local verification:** `python -m py_compile /tmp/test_b_final_preflight_exact.py` PASS; `git hash-object /tmp/test_b_final_preflight_exact.py` matches the new GitHub blob `5f9b4b3acadb2f384c0eae56b45b7fd621758bf0` (94 lines). All J1/P2/P3 integration assertions **NOT_RUN**.

## 3. Recovered original V3 proposal mechanism — direct qualified source disposition

A/B's deeper unresolved issue is real: `RecursionCycle._parse_proposals` requires 3–5 document entries and `BatchEngine.run_batch` executes **each** in order. That is a scheduling/execution contract, **not** an actor-conditioned alternatives court. `P2Owner._realize` then executes `session.admit_event(case=self.case, source=self.source,...)` for a prebound generic `case/source`, not a P3 historical activity selector. No `eligible_modes` to action promotion is legitimate. Original G2 still HOLD.

The source recovery provides a more exact competent **candidate design** than generic claims that a new chooser is missing:

| Original retained source/evidence | Actual function or jurisdiction | Missing E01 proof / authority |
|---|---|---|
| `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/recalibration/TD_R05_V3_DEVELOPMENTAL_RUNTIME/LATEST_EXTANT_V3_V2_BASELINE.md` — source archive SHA256 `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086` | Historical V3 Pass 1 event proposal → code selection/scoring → bounded causal state effects → separate Pass 2 render | Historical **design evidence**, not directly imported into current P2/P3; needs exact live-source custody, actor context adaptation and admission. |
| Legacy `v3/engine/run_llm_band.py` SHA256 `120e177462219e8ccd5d5e0d7fdb23de993639f5af8be6c40a06db36e0b37a38`; `v3/engine/scoring.py` SHA256 `36833287c72ffa40d0ece1ebc66fb0d685a92fc71aab1d211be9b21bfd0a82cb` from retained recovery manifest | Historical propose/score/select machinery; **distinct** from modern `RecursionCycle` batch | Both direct paths `v3/engine/{run_llm_band,scoring}.py` return 404 at #1025 source cut; recovery docs identify archived code but do not make it a callable qualified module. Historical first-candidate fallback and ambient RNG cannot be adopted as authority. |
| `.../schematics/release/W0_AUTHORITY_FOUNDATION/ADP_019_V3_EXTERNAL_ADMISSION/AUTHORITY.md` | V3 **external interaction admission**: `ADMIT/REJECT/DEFER/INVALID`, exact actor/root/history and event identity; candidate is not event | This ingress court is **not** proposal generator, event selector or automatic P2 performer. Cannot convert LLM chosen text into an admitted event by bypassing rule. |
| `.../schematics/release/W0_AUTHORITY_FOUNDATION/ADP_020_V3_CAUSAL_RNG/AUTHORITY.md` | Versioned **named** causal randomness for an already-lawful finite candidate set, with rule/version/candidate hash/replay receipt | No ambient `random.Random()`, top-ranked/first-candidate rescue or stochastic selection absent an issued semantic rule. Zero lawful candidates produce zero draws. RNG is not a motivation rule. |
| `.../schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/CAN_008_V3_PRESSURE_FLOW_RESPONSE/AUTHORITY.md` | Typed V3 multistream response transactions, exact generated parent/target rule provenance, atomic effects/rollback | Multiple pressures and contradictions can be preserved, but CAN-008 alone is not an action chooser; missing cross-stream/target/numeric rule authority must remain explicit. |
| Frozen `p3/p3_owner.py:validate_proposal/_plan/realize`; `p3/state_store.py:pending`; `p2_owner.py:validate_proposal/_realize` | Actual existing P3 pinned-plan and P2 world-owner ABI | `P3Owner._plans_by_event` requires already bound `event_id + proposal_hash` and source/registry/rule identity. An unforeseen provider event has no lawful P3 plan by default; direct P2 execution cannot silently claim historical Nadia activity. |

Recovery hierarchy is explicit: historical V3/V2 is **reuse evidence**, subordinate to the newer accepted V550+/CAN/ADP runtime, with continuity preference only where lossless. Do **not** treat the absence of `v3/engine/run_llm_band.py` at the current root as proof that no copy exists in a historical ZIP/vendor branch; it proves only **not directly importable at this exact source path**.

## 4. Minimum exact competent next seam — no new psychological engine

An authorized **V3 actor-prospective candidate/selection owner** must provide, without backsolving Nadia's biography:

1. **Actor-access input:** exact focal root/actor/branch/logical-clock and admissible C04/P6 speech; P3 acquired, active and latent multistream records and contradictions; objective world conditions and separate actor-perceived subset; immutable source closure and canonical material state hash.
2. **Proposals:** multiple actual, causally and materially possible **alternative** act/outcome candidates (including ordinary unrelated action, no recruitment and possible inaction) with exact proposer provenance, source rules, event identity, candidate hashes and authority-relevant constraints. A sourcefree provider candidate is not already a realized event.
3. **Event/outcome court:** versioned actor-source rule either explicitly chooses one lawful candidate or returns a typed unresolved/deferral/inaction evaluation; no dominant motive scalar, hidden screenplay, automatic drumkit confrontation or default-first/random selection. An actual NO_ACTION must have a competent **evaluation** receipt; missing owner stays `MISSING_RULE`, not `NO_CHANGE`.
4. **Performance custody:** link exactly the selected, admitted candidate to the original P3/P2 owner via lawful **prebound P3 plan/proposal hash**, or obtain an explicit narrow owner handoff for the missing lawful plan creation rule. P2's prebound `case/source` does not suffice to prove an independently motivated Nadia act. No second world/actor writer.
5. **Downstream proof:** a later ordinary P4/P6/world actor consumer reads the exact admitted event and actual consequences; alter/sever/restore historical/actor/material source, assert changed legitimate outcomes where warranted; cold reopen/replay and anti-duplication; no private mother reason or future biography leaked into Nadia.

**Exact missing authority/interface:** `V3_ACTOR_PROSPECTIVE_ALTERNATIVE_EVALUATION_AND_EVENT_ADMISSION` from preserved historical proposal/scoring/separate-render design to the live `P3Owner` plan/proposal ABI and actual P2 world write, under ADP-019/020 and CAN-008. This label is an **investigation/interface requirement, NOT an issued rule ID or newly claimed native jurisdiction**. Naming this missing seam does not authorize creating it on the completed #1010 duel branch.

## 5. Source proof boundaries and stop

- B valid preflight improvement **preserved**; original D03 existing prepending refusal **recognized**; B's unrun test oracle **repaired**; actual source-specific post-J1 race **newly covered, NOT_RUN**.
- Historical V3 candidate pipeline **found in retained source-recovery evidence**, not executable/qualified at current #1025 source path. ADP-019/020/CAN-008 **authority contracts** inspected, not proof a corresponding installed runtime exists.
- No native P2/P3 performed event, cold actor first consumer, alternate-history actual choice, genuinely evaluated inaction, actor-source rights, scientific approval or G5 performed in this correction.
- Original 12 isolated tests remain inherited prior evidence; **not rerun in this turn**. One amended test is exact-byte syntax-checked. Total test-suite/CPU/RSS not measured; no green claim.
- **G1:** precise source/authority audit with test-oracle correction; integrated NOT_RUN. **G2:** HOLD competent actor prospective election+performance. **G3:** two exact new negatives authored NOT_RUN. **G4:** full cold world evidence NOT_RUN. **G5:** independent reviewer NOT_PERFORMED.
- One finite A→B→A + B optional round was already completed. This source-error corrigendum is **not** another adversarial duel, not another lock-court commission, and not an invitation to repeat. **STOP.** Productive next execution is the separately governed V3 prospectives-to-P3/P2 source seam under an explicit source-owner lease and one real first-consumer demonstration.
