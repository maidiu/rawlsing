# G07 — TEST / RUN IDENTITIES

## Commission identity

- branch: `agent/rabochii-prev3-w5-g07-second-canary-independent-qual-r1`
- commission tip: `0266f148cf4ace3f68065f7eb57f1524281fa3d2`
- commission blob: `74451c7b38e6f9865171d447e0e4a79dfc6dc907`
- exact grain: `PREV3_SECOND_CANARY_ADMISSION_AND_M1_V554_INDEPENDENT_QUALIFICATION_R1_ONLY`
- Library: `NO`

## Frozen F07 candidate / authority identities

- `rawlsing_next/f07_second_canary_prev3_admission.py` — blob `06c312209148ab5bdd2c2077f3c887bdc9f948c8`
- `rawlsing_next/tests/test_f07_second_canary_prev3_admission.py` — blob `7772e9cd4726e6b513a2e2a809ecb9f02ea30f28`
- `rawlsing_next/wave1_ff_prev3_relation_admission.py` — blob `c5fb675fd6f95cb7dc9e0ad505224803839cc645`
- `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py` — blob `0aeacd9e66c7e4340b36e1b622bb5c9bf2865fd5`
- `rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py` — blob `09e38c324a4f6711709255c6d8d7da3ba75cf04f`
- F07 `00_RETURN.md` — blob `c07c88ac182646ec5f9633e0ccd5562a8ceb7293`
- F07 `01_SECOND_CANARY_ADMISSION_RECEIPT.json` — blob `fe3f776dd0c07dae67f2e41373368961fa55bb0c`
- F07 `02_M1_V554_INGRESS_AND_REPLAY_RECEIPT.json` — blob `a975dd774a22e9d1a2f9e1378c10fa6533280df3`
- F07 `03_HOSTILE_TYPED_STATE_PRESERVATION_RESULTS.json` — blob `d62897b7d1436bc65b7ca7810c764a0f0581153e`
- E10 `01_SECOND_CANARY_RELATION_ADMISSION_AUTHORITY.json` — blob `48168c4ed96ab34c906db74cf96054e765f57d7a`
- E10 `02_PERMISSION_NEGATIVE_STATE_REPLAY_LEDGER.json` — blob `69719830dbff2f752a373ab961bf6e05d05edd2d`

## G07 durable qualification evidence

- `01_INDEPENDENT_QUALIFICATION_PROBE.py` — blob `4346cc53e5876cac7c4c7cd4ec98d364faedc013`
- `02_INDEPENDENT_QUALIFICATION_RESULTS.json` — blob `2068a1d0a5efa091d3556a84c8e08f994f97b5db`

## Governing clean run

- GitHub Actions run: `34780188481`
- job: `103785661994`
- tested head: `7a1589577b3480fa4658fa68384ac04820f84a63`
- runner: Ubuntu 24.04.5
- Python: 3.12.14
- conclusion: `success`

### Independent G07 qualification probe

Command:

```text
PYTHONPATH=. G07_RESULTS_PATH="$RET/02_INDEPENDENT_QUALIFICATION_RESULTS.json" python "$RET/01_INDEPENDENT_QUALIFICATION_PROBE.py"
```

Outcome:

- result: `PASS`
- cases: `20 / 20 PASS`
- positive exact-identity / replay / typed-state cases: `7 / 7 PASS`
- authority/relation/claim/operand/roster/permission/provenance mutation cases: `13 / 13 PASS` by failing closed as required

### Frozen F07 candidate court

Command:

```text
python -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_f07_second_canary_prev3_admission.py
```

Outcome: `15 passed in 0.22s`.

### Parent admission + M1/V554 regression court

Command:

```text
python -m pytest -q -p no:cacheprovider \
  --deselect rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py::test_m4_binding_accepts_exact_relation_contract_and_keeps_v554_producer_family \
  rawlsing_next/tests/test_f07_second_canary_prev3_admission.py \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py \
  rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py
```

Outcome: `63 passed, 1 deselected in 0.51s`.

Exact governed deselection:

`rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py::test_m4_binding_accepts_exact_relation_contract_and_keeps_v554_producer_family`

The exact deselected M4 node was then executed independently both at the G07 commission tip `0266f148cf4ace3f68065f7eb57f1524281fa3d2` and at the qualification head `7a1589577b3480fa4658fa68384ac04820f84a63`. Both fail identically with:

`M4IntegrityError: relation M1 producer uses may not be caller-selected at the shared boundary`

Therefore the M4 regression is inherited at the commission tip and is separate from this exact G07 grain. It was not repaired or treated as G07 authority.

## Exact qualified semantic identities

- claim: `FFR2_R5_Q73A_Q86A_EXACT_JOINT_CONDITIONED_DIRECTIONAL_HETEROGENEITY_CANARY@1`
- relation identity SHA256: `1a3b1d28cecdb5b06c7b8ac927848249693324da733d1ee9649a94e50d4322ee`
- authority key SHA256: `33c6f8b2e33758ef91d57d3eb3fa8bab7c65dfb7a6498495fb08d5261dc3a5fd`
- replay key SHA256: `0615a8668d87c5641c8a7bba4b144011d297c653a5369d6db2bd979e824fd19d`
- source SHA256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- risk-set rows: `19210`
- risk-set member-set SHA256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- full-roster artifact SHA256: `1cc810979eb80d52d1e5efcd1a916e309be1b60e8d5cc4eed1575bce30f38814`
- second-canary admission content hash: `05456f3d21ab3426af6a6c924843fecb8417c11620dce7213a36c8a819e8dd2c`
- second-canary admission id: `urn:rawlsing:prev3:f07:second-canary-admission:sha256:05456f3d21ab3426af6a6c924843fecb8417c11620dce7213a36c8a819e8dd2c`
- M1/V554 decision: `ELIGIBLE`
- canonical basis id: `urn:rawlsing:v554:basis:sha256:a34deb4ba5d52990b966ac67cb1e0e51ab76ba05fbfae4c3f8db996d26b1d81b`
- F1 id: `urn:rawlsing:v554:f1:sha256:06f96892b9d7cad5a2d506345203b3634509d2492997326031a98b44d83973f8`
- M1 replay SHA256: `5d6e26ef30210ad7766c95d660c99cb6b91e38ebc291dd025e154201fdeec25b`
- typed-state partitions: `812 = 441 + 371`; `441 = 185 + 130 + 126`
- permission ceiling: exact singleton `STRUCTURAL_MEDIATION_INPUT`

## Non-governing setup/probe run transparency

- run: `34779923946`
- job: `103784938018`
- observed independent probe result before harness correction: `19 / 20 PASS`
- only failing probe case: the committed JSON-form M1 evaluation was compared directly against an in-memory Python representation containing tuples; the exact semantic values and all mutation checks were already satisfied.
- correction: JSON-normalize the in-memory value before artifact equality comparison.
- production/runtime files changed by this correction: `NONE`.
- governing result is the later clean run `34780188481` / job `103785661994` above.

## Scope statement

No runtime/production repair was made. No Library evidence was used. MAIN and PRE-MAIN were not mutated. No GT2 widening, publication promotion, M3/V3/person-state promotion, causal promotion, or quarantined OBL063 driver/type/person-terminal semantics were admitted.
