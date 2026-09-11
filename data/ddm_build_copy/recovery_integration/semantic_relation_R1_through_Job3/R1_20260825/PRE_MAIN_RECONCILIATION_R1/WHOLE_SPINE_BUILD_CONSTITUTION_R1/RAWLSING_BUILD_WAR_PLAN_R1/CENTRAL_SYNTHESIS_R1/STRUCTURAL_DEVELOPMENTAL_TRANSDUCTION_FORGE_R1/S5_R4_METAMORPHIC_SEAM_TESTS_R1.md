# S5 R4 METAMORPHIC SEAM TESTS R1

STATUS: `30_SINGLE_MUTATION_SEMANTIC_RELATIONS__COMPLETE`

These tests pair canonical vectors and mutate exactly one semantically relevant input. They are designed to expose hidden category/title shortcuts, overbroad invalidation, witness leakage, and context smearing. The oracle labels are test-only.

| MT | BASE | ONE INPUT MUTATION | EXPECTED EXACT CHANGE | MUST REMAIN UNCHANGED | FAILURE SIGNATURE |
|---|---|---|---|---|---|
| MT-01 | TV-002 authority operative | remove operative authority record; keep class/title/job fixed | P2 authority falls from constitutive current to unknown/not-proven | class label, job identity, P3 task facts | class/title shortcut |
| MT-02 | TV-015 authority operative | replace operative delegation with explicit revocation | current authority becomes explicit negative; prior authority remains history | unrelated wage/task/channel facts | global actor reset or stale carry-forward |
| MT-03 | TV-003 complex task | change only actual task content to scripted repetition | P3 task-quality consequence changes | class, occupation title, authority relation | occupation/category shortcut |
| MT-04 | TV-027 formal autonomy/scripted | add one valid observed episode of exercised discretion | exercised-discretion result changes from unproved to realized | formal P2 scope, title, unrelated task facts | P2-only autonomy inference |
| MT-05 | TV-028 exercised discretion | remove actual participation witness | exercised discretion drops to unknown/qualified only | formal decision scope remains | qualification→realization leakage |
| MT-06 | TV-008 eligibility | add valid application witness only | application stage becomes realized; eligibility unchanged; approval/receipt remain unproved | criteria, entitlement absent, V3 state | P4/P1 stage leakage |
| MT-07 | TV-009 approved not received | add current payment witness | P1 receipt becomes realized | approval history and eligibility | approval→receipt shortcut if base already realized |
| MT-08 | TV-010 benefit received | expire only payment witness while rule remains valid | current receipt becomes unknown/not-proven; historical receipt remains | rule validity, entitlement if separately current | stale witness carry-forward or stale→negative |
| MT-09 | TV-013 no current record | add explicit denial witness | status changes unknown→explicit negative | eligibility rule, actor binding | missing-evidence treated as already negative |
| MT-10 | TV-061 no evidence | change source semantics to authorized closed-world complete scope, still zero record | exact nonoccurrence becomes explicit negative | actor/context/rule inputs | closed-world scope not honored or generalized too broadly |
| MT-11 | TV-030 P4 applicable | add gate encounter only | encounter becomes realized; decision/treatment remain unknown | eligibility/applicability | encounter→decision leakage |
| MT-12 | TV-032 encounter/no decision | add valid decision witness | P4 decision becomes realized; downstream access changes only if exact consequent rule applies | encounter history, unrelated contexts | P4 stage collapse |
| MT-13 | TV-033 hidden classification | make cue visible but not recognized | presentation may become realized; treatment still unchanged | underlying category, gate rule | visibility→treatment shortcut |
| MT-14 | TV-034 presented not recognized | change only recognition witness to recognized; keep neutral decision | recognized stage changes; differential treatment remains false/unproved | gate encounter and decision neutrality | recognition→discrimination shortcut |
| MT-15 | TV-035 recognized neutral | change only treatment decision to differential | differential-treatment D1' fact appears | cue recognition, actor binding | category prior rather than decision witness |
| MT-16 | TV-039 tie/no contact | add contact witness only | contact becomes realized; transfer remains unknown | tie existence | tie/contact→transfer leakage |
| MT-17 | TV-040 contact/no transfer | add information-transfer witness | information delivery becomes realized | tie/contact; perceived knowledge remains downstream | transfer→belief leakage |
| MT-18 | TV-042 support transfer | change only actor appraisal to “not supportive” in V3 | D1' objective transfer does not change | transfer provenance, P5 result | private psychology→social-world write |
| MT-19 | TV-044 counterpart unreachable | restore reachability only, no transfer | reachability becomes current; transfer still unknown | tie relation | reachability→transfer shortcut |
| MT-20 | TV-047 linked job-loss propagation | remove exact household resource/task relation; keep parent job loss | child-target D1' consequence disappears/rejects missing binding | parent external job-loss fact | relationless linked-life propagation |
| MT-21 | TV-049 care obligation | remove operative care obligation while retaining kinship and care need | A1 care duty/time allocation disappears or becomes unknown | care need, kinship label | kinship shortcut |
| MT-22 | TV-051 work→household schedule carrier | revert work schedule only | dependent household time constraint rederives/reverts | household relation, school/care contexts not dependent on schedule | cross-context generic spillover / over-invalidation |
| MT-23 | TV-054 job exit | remove termination witness but leave no current positive employment witness | current job facts become unknown/not-proven, not explicit negative | historical employment | missing→negative leakage |
| MT-24 | TV-054 job exit | keep job exit but mutate household relation only to remain current | job facts cease; household relation persists | actor identity and unrelated contexts | global reset |
| MT-25 | TV-059 stale recurrence | add fresh recurrence coverage only | current recurrent activity becomes realized | rule validity, historical episodes | freshness ignored |
| MT-26 | TV-064 population risk only | add actor-specific institution-issued denial outcome | actor denial becomes realized/negative at exact gate | population rate remains calibration evidence only | D1' stochastic self-sampling or prior group→actor collapse |
| MT-27 | TV-068 hypothetical promotion | replace hypothetical assumption with competent actual promotion record | consequences move counterfactual→current constitutive/realized as supported | prior counterfactual remains noncurrent history | counterfactual leakage |
| MT-28 | TV-070 same work/different age | cross legal-age threshold while keeping work rule age-invariant | no D1' work consequence changes | objective job conditions | age-as-generic-cause leakage |
| MT-29 | TV-071 legal-age eligibility | cross threshold by one day only | exact eligibility flips according to social rule; no psychological fact changes | actor/world/context, downstream uptake | phase ignored where socially constitutive or used as trait proxy |
| MT-30 | TV-082 outage chain | restore only upstream infrastructure capacity | dependent service-capacity/access/time facts rederive; unrelated P2/P5 facts persist | actor identity, unrelated relations | stale descendants or global invalidation |

## Metamorphic invariants

The suite must satisfy all of these across the 30 pairs:

```text
SAME CATEGORY + DIFFERENT OPERATIVE RELATION => DIFFERENT D1' WHERE RULE USES RELATION
SAME TITLE + DIFFERENT TASK/AUTHORITY => DIFFERENT D1' WHERE EXACT FACT CHANGES
SAME RULE + STALE WITNESS => REALIZATION DROPS WITHOUT BECOMING NEGATIVE
SAME GATE + REMOVE CUE VISIBILITY/RECOGNITION => ONLY DEPENDENT P4 STAGE CHANGES
SAME TIE + REMOVE TRANSFER => RELATION MAY REMAIN WHILE TRANSFER DISAPPEARS
SAME HOUSEHOLD + REMOVE CARE OBLIGATION => KINSHIP DOES NOT PRESERVE DUTY
SAME ACTOR + JOB EXIT => JOB-DEPENDENT FACTS CHANGE, OTHER CONTEXTS DO NOT RESET
SAME WORLD + V3 APPRAISAL CHANGE => OBJECTIVE D1' FACT DOES NOT CHANGE
SAME POPULATION RATE + ADD ACTOR OUTCOME => ONLY ACTOR-SPECIFIC WORLD RESULT AUTHORIZES D1'
SAME COUNTERFACTUAL + ADD CURRENT WORLD TRANSITION => MODALITY CHANGES ONLY AFTER COMPETENT FACT
```

`METAMORPHIC_TEST_COUNT = 30`