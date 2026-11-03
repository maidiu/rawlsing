# LIVE-02 — HQ integration and exact candidate-patch contract

**Decision requested:** review **one narrowly scoped adapter** to the existing P0/P1 living reference, not a new architectural/platform proposal. **Status:** RETURNED SOURCE/CODE CANDIDATE; tests NOT_RUN; independent acceptance/production adoption NOT_ISSUED.

## 1. Baseline, exact sources and custody

Authorized starting P0/P1 SHA: `fa8a2b1f75cd2ee2153a813215f51dea88e16a4b`; exclusive implementation branch `agent/sorok-programma-live-update-adapter-20261103-r1`. Immutable W8-R guide input `a9ebf71e62d84e5dcc599662e976eca7fcd0e623`, existing `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00/06–15`, especially `14` all phase gate members and `15` actual seams. **No edits** to guide, Sorok/Pyat code/science, previous actual P0/P1 journal/state snapshot, HQ or protected PRE-MAIN.

The only mutually consistent authority chain is: original source owner issues scientific/rights/native claim **separately** → source-qualified P0/P1 candidate receipts enter append-only journal → scoped reviewer accepts/refuses only exact subject/cut/root and specific member → the same reference computes work-now/remaining conditions → HQ reviews any proposed guide patch and explicitly chooses adoption/authorization. This branch stops before the owner/reviewer/adoption arrows.

## 2. Candidate patch payload, never silent guide write

`python3 live_update_adapter.py --state <isolated-journal-state> candidate-patch` returns JSON:

```json
{
  "status": "HQ_REVIEW_PATCH_CANDIDATE_NOT_APPLIED",
  "base_guide_sha": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
  "patches": [
    {
      "guide_ref": "E021@VERIFY",
      "source_return_receipts": [
        {
          "id": "JOIN_E_7BF_SCOPED_REVIEW",
          "kind": "SCOPED_REVIEW",
          "grade": "SOURCEFREE_SCOPED",
          "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
          "code_reader": "class JoinedSession",
          "owner": "JOIN_E_OWNER"
        }
      ],
      "proposed_current_stage_gates": [],
      "reverse_edges": []
    }
  ]
}
```

The two empty arrays in this **illustrative schema sample** are placeholders; live candidate output derives their actual rows from the pinned W8-R file, preserving ALL/ANY/IF and exact root/status, and may contain several related gate/edge records. A receipt is only evidence **about** a stage. It cannot silently change that target's own original rule, native source, owner grant, or human acceptance.

Each proposed changed target should carry: original exact `X@stage`, actual parent gate/member IDs, source SHA/path/blob and text locator, code SHA/path/first actual reader (or NONE), editor/owner slot, reviewer subject/scope/root and prior independent RED, stage evidence grade, current missing Y/Z/W with genuine alternative, parallel lawful work, and conditional reverse unlocks. The receiving HQ should reject inconsistent or stale proposals and edit the **same original** 07/08/09/10/14/15 records only after a named source/owner decision.

## 3. Intakes safe to consider now

**JOIN-E@7bf exact reviewer PASS:** `E021@VERIFY` scoped fork/cold, original JOIN-V reviewer `4387dc...`, original 7bf writer/reader root. Appropriate result: `SOURCEFREE_SCOPED` evidence attached to the matched member only; sourcefree C9/C12 new-tuple and native C12 still pending.

**S35 authored P1 return:** `O05@ACCEPT` source-present test-only; `CAN011_RULE_T_MISSING` still missing actual positively acquired practice Rule T. S35 `T_NO_CHANGE` synthetic evaluation is **not** a genuinely independently adjudicated CAN011 O07 and cannot turn positive `O05@ACCEPT` READY. No native consumer: NONE. Next source owner: CAN011; existing P1 sourcefree code should be reused, not regenerated.

**RRIF-R2 independent negative:** subject `598d...`, review `8090a1...`, T1/M1/C1/D1 `REVISE_MATERIAL_DEFECTS`, applies only to its sourcefree cut at `C12@VERIFY`. Does not erase JOIN-E@7bf scoped acceptance or independently adopt newer F2/c784 root. Exact replacement would need a separate selected reviewer+first reader+owner/anchor claim.

**Genuine native C9/C12 owner receipt (future):** no such receipt is admitted by LIVE-02. It would require a separate changed authorization schema/court, original scientific issuer, exact selected writer/reader/root/branch/epoch/ACK/external monotone anchor, source-first reader positive+cold+severance/restore, independent review and consumer adoption. Do not upgrade SOURCEFREE_SCOPED or a handwritten principal into this chain.

## 4. Required S2 court and rejection checklist before any HQ adoption

A different test runner must fetch all six exact source commits (W8-R, JOIN-E, JOIN-V, P1/S35, RRIF 598d, RRIF review 8090), run `test_live_update_adapter.py` and the P0/P1 regression suite, then preserve command/host/Python/pytest details, passed/failed/skip counts and exact head/rebuild digests. Explicitly reject altered source object/blob, invented caller owner/reviewer, absent code first consumer with positive-review claim, duplicate different content, stale CAS, unselected IF vacuous acceptance, Rule T ghost, one-of-N FALSE READY, 7bf review transferred to c784, source withdrawal erasure and RRIF negative contamination of unrelated sourcecuts.

The existing engine's node-wide `axes` cannot truthfully represent multiple distinct reviewed roots as one global PASS. LIVE-02 therefore writes the cut-qualified review state under **`scoped_transition_states[node_id][subject_sha][guide_ref]` within that same canonical P0/P1 state** while preserving base axis fields. The derived `programma_live` projection references those exact cut-specific statuses, affected typed edges/gates, and pending owner actions. This is not a separate graph; it prevents a source-specific R2 RED from rewriting unrelated historical acceptance.

If a test finds incorrect CAS, source verification, evidence-scoped propagation or cold replay, repair the exact function under the same allowlist; do not broaden the project. Do not mark **S2 PASS**, **independently reviewed**, **native-person verified**, **privacy operational**, **human-alpha accepted** or **HQ-adopted** until each separate original authority actually returns evidence.

## 5. Future operating envelope after independent court

- HQ must explicitly authorize first use on a working state, install/preflight sourcecut, and ensure backup/lease/recoverable journal before writing any actual delta. Until then use a disposable `/tmp` state.
- No automatic source monitoring or claim that overnight returns were ingested. Every exact source transition requires deliberate verified intake and expected journal head. A missing event is visible as pending, not silently resolved.
- No agent launch/dispatch, process scheduler, web service, live daemon, paid key, provider switch or native science issuance.
- The source-qualified `candidate-patch` is advisory only. Any authorized future guide edits should update the same existing member and reverse-link records incrementally; no second reference engine.
- Stop after a scoped cold proof and independent receiving verdict. Native actor, Pyat source grant, C9/C12 first reader, S14 operating rights and human A5 remain **Sorok product** work outside the finite adapter and guide acceptance.

**Minimum next action:** authorized S2 runner executes exact tests and returns real proof/failures; a different reviewer checks it; HQ explicitly accepts or requests one minimal code correction. This is not a proposal to redo W1–W8 source census.
