# R31J tests and custody

| Suite | Tests | Result | Receipt |
|---|---:|---|---|
| R31J pre-C9 source/product | 8 | 8 PASS | `receipts/r31j_8.xml` |
| R30G GM01 material product | 8 | 8 PASS | `receipts/r30g_8.xml` |
| R29M original GM01 | 29 | 29 PASS | `receipts/r29m_29.xml` |
| R29M actual BP2 ports | 2 | 2 PASS | `receipts/r29m_ports_2.xml` |
| R29P own | 9 | 9 PASS | `receipts/r29p_9.xml` |
| R27P stable | 7 | 7 PASS | `receipts/r27p_7.xml` |
| R26V historical producer | 10 | 10 PASS | `receipts/r26v_10.xml` |
| R26E/BP2P4J/N1 union | 129 | 129 PASS | `receipts/r26e_*.xml` |

R29P 155 = 9 + 7 + 10 + 129. R30G adds 8; R29M adds 31; R31J adds 8. **202 distinct executed tests** at their stated scopes, with inherited overlap reported rather than inflated.

`evidence/source_ledger.json` records B/E1/E2/C8/C9/target/product identities and the C9 governed payload. `evidence/r31j_chain.json` records positive/refusal/omission/cold receipts. `evidence/clock_mapping.json` records the three clock domains. `evidence/bp2_ports.json` records the real port A/T no-grant state.

`receipts/r31j_8.xml` includes source-bound positive, refusal C9, omission, restoration, cold reopen, fork, actual ports and label-only/E1-missing controls.
