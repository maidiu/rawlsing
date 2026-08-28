# G-SR07-R3 WVS7 DOCUMENTARY RECOVERY — W3

Status: `RETURNED__W3_FRESH_DOCUMENTARY_PASS__POSITIVE_IDENTITIES_AND_METADATA_RECOVERED__UNIVERSE_AND_ROUTING_CONTENT_GAPS_FAIL_CLOSED`

Repository: `maidiu/rawlsing`  
Worker branch: `agent/vozhd-trii-gsr07r3-wvs7-doc-w3`  
Exact start HEAD: `d643edc4d4a0be155e92c374b8d1d4b560140fbb`

## Holding

This is the fresh W3 documentary pass authorized after the prior unpersisted return. It is documentary recovery only. It does not certify WVS7, alter the frozen 613-slot ownership, adjudicate D03/D11/D12, mutate C11/I03/I05/I04 or V553+, launch C05R2B, or select architecture.

The exact W3 batch is:

- Iraq 2018
- Japan 2019
- Jordan 2018
- Kazakhstan 2018
- Kenya 2021
- Kyrgyzstan 2020
- Lebanon 2018
- Libya 2022
- Macau SAR 2019
- Malaysia 2018
- Maldives 2021

## Authority and command identity

The worker branch was verified at the authorized start HEAD before recovery.

Read on the worker branch:
- `00A_READ_BEFORE_ANY_TRII_ACTION.md`
- `78_TRII_ROUTE_A_COMMAND_IDENTITY_AND_ANTI_DRIFT_LAW.md`
- `83_GSR07R2_ABC_ACCEPTANCE_AND_WVS7_DOCUMENTARY_RECOVERY_WAVE_AUTHORITY.md`

Accepted R2 inputs were bounded to:
- Lane A `a06f2bced8677453cf77fec5e622cb334a9810a5`
- Lane B `a07f449221256e0c52cffd3f85812d30c0f047fc`
- Lane C `930d89b8930c21c9a8f1180093ee15ed10c495e4`

### Authority-84 exact-ref mismatch

The requested control commit `04a0109aa170c6041b199e5c6130a39a8e0f6029` exists, but its exact tree exposes no file/path/content identifiable as “Authority 84” or a G-SR07-R3/WVS7 documentary-recovery authority. The exact commit tree and repository search were checked. No later/current control authority was silently substituted.

This pass therefore records `GOV-A84-REF-MISMATCH` as `DOCUMENT_NOT_LOCATED` and acts only under the explicit W3 relaunch instruction plus Authority 83 and the accepted R2 refs.

## Documentary recovery

The official WVSA Wave-7 country documentation index positively lists all 11 assigned country-years:

https://www.worldvaluessurvey.org/AJDocumentation.jsp?CndWAVE=7

The authorized IHSN deposit exposes WVS provenance and exact study references for all 11. Exact producer-authored questionnaire/methodology/sample-design resource identities were recovered for nine countries: Japan, Jordan, Kazakhstan, Kenya, Kyrgyzstan, Lebanon, Macau SAR, Malaysia, and Maldives.

For Iraq, the exact WVS study identity was recovered, but exact country questionnaire/methodology/sample-design resource identities did not surface in the accessible source pages and remain `DOCUMENT_NOT_LOCATED`.

For Libya, the authorized deposit study metadata positively states that Libya 2022 sample-design documentation exists and supplies country/producer/fieldwork metadata, but the related-material resource list was not retrievable; the sample-design document is therefore `DOCUMENT_IDENTIFIED_CONTENT_NOT_RECOVERED`, while exact stable questionnaire/methodology identities remain `DOCUMENT_NOT_LOCATED`.

No country-specific target population, sample frame, actual design regime, or PSU/strata/cluster/route detail is promoted from the deposit’s generic WVS preference for a full-probability 18+ sample. Authority 83 makes that wave-level baseline non-substitutive for country-specific actuality.

## Positive source-owner metadata recovered

Where the authorized deposit HTML positively supplies country-specific metadata, it is retained as such (not as a sampling-design inference), including:

- Japan: mail questionnaire; Japanese; fieldwork `2019-05-09..2019-09-26`.
- Jordan: CAPI; Arabic; `2018-06-14..2018-07-06`.
- Kazakhstan: PAPI; Kazakh/Russian; `2018-01-10..2018-11-30`.
- Kenya: CAPI; Swahili; `2021-05-22..2022-06-22`.
- Kyrgyzstan: CAPI; Kirghiz/Russian; `2019-05-12..2020-01-28`.
- Lebanon: CAPI; Arabic; `2018-04-06..2018-06-18`.
- Libya: CAPI; Arabic; `2021-12-12..2022-01-26`.
- Macau SAR: CAPI; Chinese; `2019-03-10..2019-12-17`.
- Malaysia: the study metadata says face-to-face while its collection note says CAWI/CAPI; both source-owner statements are preserved without inventing a reconciliation; Malay/Chinese; `2018-05-04..2018-05-21`.

Kyrgyzstan’s authorized-deposit country-document titles use `2019` while the accepted study identity is Kyrgyzstan 2020 and fieldwork spans 2019-2020. This is retained as an identity oddity, not escalated to contradiction without conflicting substantive source-owner claims.

## Lane-B documentary harvest

Only D01-D02 and D04-D10 were harvested.

Accepted Lane-B country/module scope is used only for lawful `NOT_APPLICABLE_TO_CLAIM` determinations:
- D04 Q294 form assignment is applicable in this W3 batch only to Kenya, Kyrgyzstan, and Libya under RB06.
- D05-D06 MENA internal routing are applicable in this W3 batch only to Iraq, Jordan, and Lebanon under RB09.
- D07 WEE is India-only under RB11, therefore not applicable to all W3 countries.
- D08-D09 Gender version/target recovery is applicable in W3 only to Kenya under RB12.
- D01, D02, and D10 remain documentary-content claims and are not inferred from released data.

No D03/D11/D12 HQ join was performed.

## Anti-inference receipt

No design or routing fact was inferred from:
- incidence,
- `I_PSU`,
- weights,
- missingness,
- neighboring waves,
- standard survey convention,
- variable-name resemblance,
- response-column population.

No raw survey bytes or large document binaries are included.

## Files

The package contains exactly the Authority-83 W3 return surface:
- `RESULT.md`
- `RESULT.json`
- `COUNTRY_DOCUMENT_AUTHORITY.csv`
- `COUNTRY_UNIVERSE_RECOVERY.csv`
- `ROUTING_DOCUMENTARY_RECOVERY.csv`
- `DOCUMENT_IDENTITY_AND_PROVENANCE.csv`
- `UNRESOLVED_GAPS.csv`
- `CHANGED_FILES.txt`
