# SOROK REMONTATHON R3 R7 — sourcefree reproduced defect repairs

**Date:** 2026-11-19 (New York local)  
**Frozen parent:** draft PR #1171 at `a14003df55ed63c9257a8f9bbb2a3501d36bf7dc`.  
**R3 builder:** PR #1167 at `3dba91136870ab5e766ca14faacd847531dea075`.  
**Boundary:** independent sourcefree research owners only, no protected PRE-MAIN, no CAN/ADP native issuer, no SOROK HQ rights.

## Concrete first faults, observed red before code repair

- **SR-P058: String-based grant escalation** — malformed `members='joann'`, `admitted='joann'`, or `material_use_grants='joann'` granted actor `ann` authority by substring. Repair: shared exact typed list-of-actor-identifiers guard at `world.py`; no implicit entitlement. Normal list grants still work.
- **SR-P059: Phantom coactor performance** — independent partner plan was invoked and partner was recorded as willingly completing `JOIN` despite the principal's bodily impossible initiating `SING`. Repair: no joint invitation/voluntary reply solicited until principal is physically eligible. A separate, independently authored response remains possible in a real later world event.
- **SR-P060: Misaddressed partner authorization** — the trusted coactor planner's `Attempt.target` could be some third person yet the system recorded it as cooperation with principal. Repair: exact addressee match before world mutation; no externally supplied coactor override was enabled.
- **SR-P061: Invalid recipient body laundered by CARE** — care to a target whose stored bodily nutrition was NaN mutated invalid state into apparently normal state. Repair: pre-validate the affected Other's body before changing its physiology.
- **SR-P062: False permission / form recruitment via untyped scope** — `actor_access` claimed `SITE_ACCESS` for `ann` under `admitted='joann'`; form `scope.locations='househome'` or malformed counterpart and string cue lists could be admitted, manufacturing spatial/counterpart matches. Repair: same exact world admission guard; typed `locations` and `counterpart`, list-of-string form cues, and typed development scope change.
- **SR-P063: False historical cue/context activation** — relational `contexts='househome'`, activity link string contexts, project cue string and trace cue string passed admission and were later treated as character-wise/substring matches. Repair: typed string-list validation at the existing development/admission owner, including project reorganization and trace/memory production. Valid typed links remain admissible.

## Execution and causality

- Before R7 code patch: 6 of 9 first adversarial tests **FAILED** as expected; existing positive tests passed. After first material/coactor fixes, 8 further psychic/access negative tests **FAILED** before their respective repairs. The red logs remain separate and unmodified.
- Final regression additions: **22 tests** in `tests/test_remontathon_r7.py` (R6 parent 131 → R7 153).
- Complete `python -m unittest discover -s tests -v`: **153 PASS, 0 FAIL**. Complete `python -O -m unittest discover -s tests -q`: **153 PASS, 0 FAIL**. Final run log and exact changed Git object hashes attached.
- The R6 archive's original world/constitution/psychodynamics/development blobs were checked byte-identical with published `a14003df...` before patching. All changed files have new exact Git blob identities in `R7_FILE_IDENTITIES.json`.

## Research limitations / transfiguration compatibility

These are typed integrity and independent-world authorization repairs, **not** a new account of human consent, unconscious inhibition, affective formation, or psychological genesis. They do not preinstall new motives or constrain the intended future Constitutive Organism theory. Malformed legacy R3 candidate scopes or grants may now fail closed and require explicit owner-qualified migration; silent string coercion is not authorized. SR-P004/P005/P012/P018 and deeper open developmental mechanisms remain partial/open at their existing scopes. The R7 six new P rows are **author-repaired candidates requiring independent review**. No native P2/P3/P6, privileged owner/actor rights, protected merge, real PYAT joint-source qualification, or scientific validation is claimed.
