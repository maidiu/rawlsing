# Execution, tests, NOT_RUN and environment

## Executed in this return

| Court | Tests | Result | Receipt |
|---|---:|---|---|
| R29P new integration | 9 | 9 PASS | `evidence/r29p_tests.xml` |
| R27P stable actor | 7 | 7 PASS | `evidence/r27p_7.xml` |
| R26V historical producer | 10 | 10 PASS | `evidence/r26v_10.xml` |
| BP2P4J joined product | 98 | 98 PASS | `evidence/bp2p4j_98_rerun.json`; JUnit `bp2p4j_33`, `bp2_50`, `bp4_15` |
| R26E qualified C12/N1/live | 8 | 8 PASS | `evidence/r26e_8.xml` |
| N1 method | 21 | 21 PASS | `evidence/n1_21.xml` |
| N1 actual BP2 ports | 2 | 2 PASS | `evidence/n1_ports_2.xml` |

`R26E 129` is the union 33 + 50 + 15 + 21 + 2 + 8, all executed. It is not double-counted with the BP2P4J 98 or N1 receipts. Unique additional tests are R27P 7, R26V 10 and R29P 9: 155 distinct executed tests at their graded scopes.

## Commands

```sh
cd WORKER_RETURNS/SOROK-20261021-R29P-ACTOR-C12-USER-PRODUCT-R1
python3 -m pytest -q tests/test_r29p.py
python3 tools/run_evidence.py
```

Inherited suites were executed from their exact pinned returns/worktrees as reported above; their JUnit is copied into `evidence/`.

## NOT_RUN

- Native ADP007/ADP010/ADP015/ADP019 source, encounter or E1.
- Concrete CAN008 RULE_A or separate CAN011 RULE_T/grant.
- Native independent E2 actor/occurrence authority.
- C8 D1/D2/D3 protected writer, key and monotonic anchor.
- Pyat N11/N12, original35 source execution, world grant or C11 weld.
- Native C12 person, A4/A5 human product evaluation.
- Raw original respondent data and original survey execution.
- Production installation or production KMS.
- R26E/R27P/R26V code cutover into upstream owners.

## Environment and economics

- Harness: OpenCode local session.
- Model id: `opencode-go/deepseek-v4.1-flash`.
- Reasoning: MAX as commissioned; exact metered effort is not independently observable from the harness.
- Python: 3.11.3.
- pytest: 9.1.1.
- SQLite: 3.40.1.
- Platform: macOS local filesystem, Git worktree, real subprocess cold reopen.
- Cost/quota/spend: UNKNOWN.
- No model, provider, harness or subagent switch.

## Residual security and scientific limits

- Raw SQLite deletion and same-user external witness compromise remain.
- The C12 store is not a production trust boundary.
- The actors are sourcefree simulator entities, not observed humans.
- H0 remains live: role, source selection, fixture and simulator construction may explain the observed behavior.
- R28S conditional synthetic-generation permission does not establish empirical process validity.
- The product is technical alpha; it is not a native person or a human A5 experience.
