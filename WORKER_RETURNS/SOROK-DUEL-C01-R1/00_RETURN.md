# SOROK C01 Agent A return

- **Task:** C01 stable supporting-actor identities and dynamic participation without changing Nadia root.
- **Branch:** `codex/sorok-duel-c01-a-20261112-r1`.
- **Implementation SHA:** `9229698c5ded4e8c77801398d4d0ecc3e7c9ccb3`.
- **Contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
- **Grade:** `SOURCEFREE_S2_ONLY`.
- **Result:** a parent can be registered as a distinct stable supporting ID in the existing C12/P2 root; Nadia stays focal; the parent participates in the same performed world event with a separate C12 perception receipt; ghost/reserved/absent/private-leak cases refuse; duplicate registration is unchanged; cold process read and replay re-verification pass.
- **Not implemented:** C02 parent antecedent/activity, C03 parent-authored decision/action, C04 utterance/uptake, C05 relations, D02 situated field, J1/J2; native ADP-015/C4 or other authority.
- **Known break:** `p2_owner.py` byte change alters P3 `code_pins`; pre-C01 roots need recreation or deliberate migration.
- **Evidence:** `test_c01_supporting_actor.py` 5 passed; P2 owner 5 passed; P3 owner 9/1 skipped; B01 4/4; engine/model-cycle/integration 66/66; P6 actor scene 2/2; selected P3 cold/view 2/2; full P3 vertical slice timed out after 3 passes.
- **Handoff:** `AGENT_A_HANDOFF.md`, `C01_ABI.md`, `PROGRAMMA_DELTA.json`, `impact.json`.
