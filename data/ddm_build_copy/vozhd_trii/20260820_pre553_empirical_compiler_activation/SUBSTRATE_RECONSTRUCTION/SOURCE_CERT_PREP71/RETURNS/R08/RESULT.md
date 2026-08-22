# SOURCE CERT PREP71 — R08 SOUTH ASIA RETURN

**Status:** `RETURNED__NON_DISPOSITIVE__DO_NOT_CERTIFY`

**Worker branch:** `agent/vozhd-trii-srcprep71-r08-southasia`  
**Exact starting HEAD:** `0ac2a8c00ca5718f293e98f98be6685f67ea2445`  
**Write scope:** `SOURCE_CERT_PREP71/RETURNS/R08/` only

## Source identity

Library raw transport was materialized from the exact current `surveys.zip` object and independently hash-checked.

| Source | Size | SHA-256 | Identity |
|---|---:|---|---|
| South Asia Wave 1.sav | 595974 | `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571` | exact |
| South Asia Wave 2.sav | 894051 | `6a5329ea16f4546188167edd691e0e6adbeae0737a015470aa26df0e01206f22` | exact |

Bundle: `surveys.zip`, size `158180333`, SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`.

Only the two assigned South Asia substantive members were extracted for SHA verification. No local-source directory and no WVS70 source/member interaction was used.

## Dispositions

- **South Asia Wave 1:** `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED`
- **South Asia Wave 2:** `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED`

These are packet-preparation dispositions, not certification decisions.

## Hostile fixture compression

**23 proposed fixtures total: 10 W1 + 13 W2.**

The fixture set is deliberately smaller than the accepted SR09-PRE reconnaissance sentinel set while retaining every named R08 burden.

The decisive W1 coupled proof is:

1. `c12`, row 4, code `8`, label `No opinion` → `FORMAT_USER_MISSING_VALUE`, with variable-local missing declaration `[8]`;
2. `b7`, row 18, code `8`, label `No opinion` → `OBSERVED_STORAGE_VALUE`, with no missing declaration.

A future court fails if it classifies physical missingness from numeric code or label globally rather than from the source variable declaration plus cell state.

The decisive W2 identity proof is the collision pair `(ccode=1,resno=1)` at rows 54 and 90 with distinct row content, plus `resno` system-missing on the Pakistan block. `resno` therefore cannot replace exact source snapshot + zero-based row ordinal as universal replay identity.

## Documentary authority recovered

Library-first search recovered historical locators for the W1/W2 questionnaires, wave notes and codebooks, but not directly readable native W1 documentation in the current Library surface.

Browser fallback recovered official Lokniti/CSDS authority:

- Round I official project page: five-country baseline project and multi-method study context.
- Round II official project page: five-country 2013 study and change/continuity objective.
- Official 2013 **Questionnaire Set A**:
  - prints `Country Code` and `Resp. as in voter list` fields, but does **not** prove equivalence to SAV `resno` or injectivity;
  - prints Q31 as First/Second/Third ranked problem slots with `998` DK and `999` No Response;
  - prints Q32 as conditional **if answered for Q31**, with codes 1–4, 8 DK/Can't say, 9 N.A.

The official W2 instrument closes those printed documentary claims only. It does not erase the merged-SAV Nepal/Pakistan masks, does not define the ordinary `-1` blocks, does not prove `resno`, and does not establish weights/design.

## Named gaps

13 gap rows are carried forward, covering:

- respondent identity authority in both waves;
- exact cross-wave country mapping and W2 zero-row Maldives domain treatment;
- W1 c10ai routing;
- W2 country/module routing and the residual country-specific GBC32 implementation gap;
- per-variable semantic response-state authority, including W1 0/8/9/98/99, W2 8/9/98/99/998/999, and W2 ordinary `-1`;
- weight/design/estimand authority;
- questionnaire repeated/multiple-response topology;
- residual W2 Q31 open-ended coding/completion authority;
- cross-wave item/value equivalence authority.

## Cross-wave drift law

The packet explicitly records:

- rows `8442 → 10617`, variables `68 → 73`;
- zero exact or case-folded variable-name intersection;
- W1 no evident native ID vs W2 unsafe `resno`;
- country coordinate `v1 → ccode` and shifted numeric country meanings;
- W1 `6387` system + `14608` user-missing vs W2 `16263` system + `0` user-missing;
- W1 9 user-missing-declaration variables vs W2 0;
- variable/wave-specific code-state and label drift;
- W2-only ordinary unlabeled `-1`;
- W2-only ranked Q31 topology;
- source/country-specific routing masks;
- common `weight_index=0` / no evident design candidate as a physical negative fact only, never a common unweighted-design inference;
- shared UTF-8 reader surface with W2-specific Unicode round-trip burden.

## Frozen-contract contradiction check

`NO_POTENTIAL_FROZEN_CONTRACT_CONTRADICTION_IDENTIFIED`

No production runtime, database, C11 carrier, candidate architecture, or certification state was modified.

`PRE553_SOURCE_CERT_PREP71_R08_RETURNED`
