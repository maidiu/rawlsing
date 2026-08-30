# W26 INTEGRATION DAG

This is a dependency-aware partial order for the later Wave-3 physical reconciliation campaign. It is a plan, not an execution record.

## Authority rule

No node may gain authority merely because it is integrated. Each node is bounded by its source authority ceiling. Selective reconstruction is the default unit. Whole-branch merge is forbidden unless a later court explicitly proves branch-wide identity with the lawful unit.

## Nodes

| node | depends_on | source exact SHA/artifact | allowed operation | authority ceiling | required gates | forbidden collateral imports | rollback/checkpoint |
|---|---|---|---|---|---|---|---|
| A0_BASE_CUT | — | `daffee545fc60a8cd635aee9aafbe77a920f4c19` | cut future `integration/pre-main-reconciliation-r1` only | GLOBAL_HQ_BASE | verify exact SHA; clean tree; record base | all off-tree deltas | abort if cut SHA differs |
| B1_GOVERNANCE_INDEX | A0 | W22 `3157d330...`, W24 `c2c41446...`, W25 `2d059667...` | create canonical authority/current/preservation/open/anti-resurrection indexes | documentation/index only | schema completeness; exact-ref validation | authority promotion by prose; live-ref refresh | revert node if any row lacks scope/grain/ceiling |
| C1_BINDING_SEMANTIC_SURFACE | B1 | binding source paths already on `daffee545fc60a8cd635aee9aafbe77a920f4c19` | add canonical pointers/read order; no semantic rewrite | existing HQ law only | source-path existence; no contradictory current doc | copying superseded mechanisms as law | revert if any theorem is widened |
| D1_R4 | A0,B1 | `20cfc676...` | selectively reconstruct `pre553_r4_compaction.py` + dedicated proof | accepted R4 functional grain | Authority49/W05 parity; input-contract parity | unrelated R4 branch files; R5 promotion | checkpoint before/after unit; revert on parity failure |
| D2_MX01R2 | A0,B1 | `1773c9a...` | selective code reconstruction | Authority33/34 helper grain | 14-pass + fresh-process | MX01 history; carrier winner claims | revert unit on any common-contract drift |
| D3_MX02R2 | A0,B1 | `e3a05fc...` | selective code reconstruction | component-vector helper grain | 46-pass + hostile/reload | MX02 history; physical architecture claims | revert unit on vector/inverse mismatch |
| D4_Z06 | A0,B1 | `7a96397...`, admitted `a3d8c2d...` | selective code reconstruction | Authority41 lifecycle/runtime grain | 21 hostile lifecycle tests | unrelated Z06 artifacts | revert unit on authority-ceiling regression |
| D5_Z07 | A0,B1 | `e635d64...`, admitted `7903da0...` | selective code reconstruction | Authority41 discovery-policy grain | exact final-base `pre553_empirical_objects` API compatibility + 27 tests | speculative/post559 material | if API proof fails, leave Z07 unintegrated and record node blocker; base remains valid |
| D6_Z08 | A0,B1 | `125bf28...`, admitted `090a935...` | selective code reconstruction | Authority41 positioned-walkback grain | 14 core + 7 regression; evidence-ceiling checks | any bypass of evidence/authority ceilings | revert unit on deterministic-walkback/proof loss |
| E1_J01A_INDEX | B1 | `44e97e420...` + payload `42cd266...` | canonical current-authority index + immutable hashes/counts | delegated current source/candidacy grain | 1,879/1,411; 9/9; 35/35; carrier hashes | historical J membership mutation; reopening discovery | revert if denominator/hash changes |
| E2_C06_CONTRACT2 | B1 | `d94ee962...` through `66295cb...` | LOSSLESS REEXPRESSION on final base | delegated current routing grain only | exact 18,276 rows; exact 14,386 unresolved; carrier hashes; 22/22 + 8/8; C05 nonfabrication | C02-C05 readjudication; Contract@1; row-level invention | revert node if one identity/disposition/hash changes |
| F1_INACTIVE_CAPITAL_INDEX | B1 | R5 V4 `55d4bae...`, Audit69 `d6206cd...`, Z02 `cf3b376...` | exact-ref/inactive-capital preservation and optionally inert copy if needed for self-contained gate | preservation only; NO serving effect | ref/hash/proof identity; selector absence | R5 V1; Parallel-12; Auth67/68; Auth70 serving; Z02 current selector | revert if any preserved code becomes import-selected/serving |
| G1_FIELD_FORGE_PRESERVE | B1,C1 | corpus `3065c22...`, induction `a68fd5a...` | selective exploratory corpus preservation + canonical pointer | EXPLORATORY_NONBINDING | exact corpus inventory; prominent status banner; link validation | POSITION_ROLE_AUTHORITY or prospective grammar/crosswalk promotion | revert if fresh-agent test interprets proposal as current law |
| G2_HISTORY_RESERVOIR_INDEX | B1 | 3fdb/403297/75aac/3e216/VT3/SWID worker exact refs | exact-ref history/preservation index | evidence only | refs resolvable; status exact | whole-branch imports; maximality/currentness inference | revert on any live-authority leakage |
| H1_GLOBAL_VALIDATION | C1,D1,D2,D3,D4,D5,D6,E1,E2,F1,G1,G2 | W10 gate map | compose actual tests + manual/semantic courts | admission only; does not mint authority | PM-G1..PM-G8 | invented omnibus cold-validation script | candidate cannot advance on any BLOCK |
| I1_CANONICAL_ENTRYPOINT | H1 | W24 fresh-agent requirements + W10 | create/synchronize one canonical entrypoint | documentation only | no contradictory current docs; all links/refs valid; isolated fresh-agent court | oral-history dependencies; ambiguous current/exploratory labels | revert if fresh agent materially misclassifies project state |

## Parallelism

After A0 and B1, D1-D6, E1-E2, F1, and G1-G2 can proceed in collision-aware lanes. H1 is the first mandatory global convergence point. I1 is terminal and must describe the validated candidate actually produced, not a forecast.

## Nonblocking node failures

D5/Z07 compatibility failure blocks only Z07 integration. It does not invalidate the selected canonical base. C01 readmission and J01-B completion are not nodes because neither is required to establish the current pre-main candidate under the frozen authority set.
