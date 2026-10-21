# R30G tests and custody

## Executed

| Court | Tests | Receipt |
|---|---:|---|
| R30G GM01 material product | 8 | `receipts/r30g_8.xml` |
| R29M original GM01 | 29 | `receipts/r29m_29.xml` |
| R29M actual BP2 ports (previously NOT_RUN) | 2 | `receipts/r29m_ports_2.xml` |
| R29P own | 9 | `receipts/r29p_9.xml` |
| R27P stable | 7 | `receipts/r27p_7.xml` |
| R26V historical producer | 10 | `receipts/r26v_10.xml` |
| R26E/B2P4J/N1 union | 129 | `receipts/r26e_*.xml` |

R29P 155 = 9 + 7 + 10 + 129. R26E 129 = 33 + 50 + 15 + 21 + 2 + 8. R30G adds 8 new integration tests; R29M adds 31 (29 + 2 ports). No overlap is counted twice: 194 distinct executed tests at their stated scopes.

## Actual BP2 ports

`r29m/tests/test_bp2_actual_ports.py` now runs against the actual `bp2_joined.ports` from BP2P4J commit `5b3e6577400ea1d88971ae6b48e41a118b8059ae`, blob `38751f36785fd935a7817483e2ef019c746e818a`.

`evidence/bp2_ports.json` records:

- rule A and rule T are TEST_ONLY;
- distinct issuer refs;
- `grant=None`;
- `native_issuer=None`;
- `actual_target_mutations=0`;
- production response/target registry counts remain 0/0.

## Source custody

`evidence/source_manifest.json` records the exact R29M source blob `d8aac69144610e1a546bbeb02f239e10682ca857`, the actual port test blob `65873440e596b323431c12083c207a078882c6c8`, R29P `001b506f…`, R26E `eb0a2b90…`, BP2P4J `5b3e6577…`, and full SHA-256 of every R30G-owned file.

`evidence/source_ledger.json` binds GM01 resource/result hashes, the four case records, BP2 C8/E1/C9/E2 identities, C12 episodes, material product result and the clock boundary.

## Security boundaries retained

- C8 D1/D2/D3 protected writer/key/anchor: HOLD.
- C12 same-user raw SQLite deletion and same-user witness compromise: `TRUST_CUSTODY_HOLD`.
- GM01 native grant, CAN008/CAN011 issuance, ADP actor/event, Pyat N11/N12/C11: HOLD.
- Sourcefree only; no original respondent data.
