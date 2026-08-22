# SOURCE CERT PREP71 — R07 LiTS packet return

Status: `COMPLETE__NON_DISPOSITIVE__PACKET_PREPARATION`

Worker branch: `agent/vozhd-trii-srcprep71-r07-lits`  
Exact starting HEAD: `0ac2a8c00ca5718f293e98f98be6685f67ea2445`  
Scope: LiTS I / II / III / IV only.

## Holding

All four frozen raw transports were independently materialized from the ChatGPT Library and matched their frozen ZIP and extracted source-member byte sizes/SHA-256 values exactly.

No G-SR08 execution was performed. No source was certified. No WVS70 material was read or modified. The user's local Rawlsing directory was not used.

All four packets bind the same governed DTA compatibility execution:

`decode_dta(source_path, encoding="latin1")`

with authority status:

`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

That execution rule is deterministic physical compatibility law only. It is **not** intended source-text encoding authority.

## Packet dispositions

| Source | Disposition | Holding |
|---|---|---|
| LiTS I | `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED` | **Packet-ready for the future DTA proving court.** It is the designated future G-SR08 proving source. The packet freezes ordinary semantic-looking codes as ordinary values, the all-system-missing repeated slot, source-row replay identity, and all three weights including the accepted 29,000 ordinary + 2 system-missing incidence for each. |
| LiTS II | `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED` | Packet-ready with localized Stata-missing, ordinary negative-code, country/identity, ranked-slot and democratic/federal weight fixtures. Official LiTS-II methodology strengthens respondent/routing and weighting documentation without authorizing a default weight. |
| LiTS III | `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED` | Compound court required: 308 PR + 308 SR namespaces, sparse/noninjective `hhid`, mixed ordinary/system-missing states, three weights and cross-reader text provenance must all survive together. |
| LiTS IV | `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED` | Compound court required: governed reader path + negative reader regression + unresolved source-text authority + 134 skip variables + 10 visit blocks + four base/pop/top-up weights. |

## Frozen Library transport verification

- `LiTS_I.dta.zip`
  - Library ID: `file_000000000328820caec35ca18aeca59a`
  - bytes: `7,686,379`
  - SHA-256: `b2e90ee7ceefc230572e89687de28186544308949f8fd33c32b1d0ffb14b8feb`
  - extracted `LiTS_I.dta`: `139531180` bytes; `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- `surveys.zip`
  - Library ID: `file_0000000036e0822f963b9604cb2bad49`
  - bytes: `158,180,333`
  - SHA-256: `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`
  - `surveys/LiTS_II.dta`: `199716969` bytes; `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9`
  - `surveys/LiTS_III.dta`: `170487994` bytes; `368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8`
  - `surveys/LiTS_IV.dta`: `110465945` bytes; `14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c`

Only these four substantive members were extracted for this worker. No raw source bytes were modified.

## Library source-document search

The bounded Library search located source-native questionnaires for:

- LiTS I — `LiTSI_Questionnaire.pdf`, Library `file_00000000f30c722fbb7e49e6c854897f`, SHA-256 `b94bdcf4a9f2e2e025bf35e5364f79acf0b1f5fa05c035064e674fa58a921eae`;
- LiTS III — `LiTS-III-Questionnaire.pdf`, Library `file_00000000171471f9b12c8ec6c54b8a80`, SHA-256 `7d42c71445f5f23d3dd318b857f7d2f0d0bda7efd4d7859a4ef103355f591203`;
- LiTS IV — `LITS-IV-Questionnaire.pdf`, Library `file_00000000ca1871f5b09fbdab297ebe0c`, SHA-256 `4f1516dbf59fd1c05153bd2954d17c619e70b04e8cc5535c474c3560a6165ea9`.

The current Library also contains `final_codebooks(5).zip` (`file_000000003de8820c911e9ab7e73a9f1c`, SHA-256 `36a09da6c9216cfdee96bf7dd33af48b5b18c7aeff8514f20e42af58d3fc4f5c`) with all four LiTS codebooks used as repository-governed supporting metadata.

No standalone LiTS-II questionnaire/technical-report file was recovered by the bounded Library search. Under Authority 71's fallback rule, official EBRD and World Bank LiTS-II documentation was then used. It explicitly documents respondent/routing structure, multi-stage sampling, and democratic-versus-federal weighting. This closes those named documentary questions but does not establish a universal default weight or DTA source-text encoding.

## LiTS I — future proving packet

LiTS I is **packet-ready** for the later G-SR08 proving court.

This preparation does not execute that court. The future court receives:

- exact transport/source identity;
- exact governed decoder/config;
- accepted SR03 anchor: 29,002 × 1,198, zero extended missing;
- accepted weight law: `weight_0`, `weight_1`, `weight_2` each have exactly 29,000 ordinary values and 2 Stata system-missing cells;
- ordinary DK/N/A source values frozen as ordinary physical values;
- exact repeated/ranked hostile fixtures;
- explicit source-row replay-identity law;
- questionnaire evidence for respondent selection and question topology;
- unresolved default-weight and source-text authority carried forward rather than guessed.

## LiTS III — mirrored respondent modules

The packet freezes the accepted physical fact that LiTS III contains 308 `PR*` and 308 `SR*` variables. The Library questionnaire independently establishes primary and secondary respondent roles, and the repository codebook explicitly labels corresponding PR/SR variables. This is enough to preserve namespace/role topology in the future court, but not permission to infer every variable's applicability from its missingness.

`hhid` remains disqualified as replay identity: 28,625 rows are physically missing and present country+hhid tuples are noninjective. The injective `ID` field remains a source attribute; universal replay identity is source hash + row ordinal.

## LiTS IV — compound reader/routing/weight court

The packet carries all P0 terrain forward together:

- DTA format 118 under the frozen `latin1` compatibility execution;
- accepted pandas negative reader interaction (`convert_missing=True`, `convert_dates=True` -> elapsed-date `TypeError`);
- independent pandas UTF-8 metadata observation retained only as provenance;
- unresolved intended source-text encoding;
- 134 `*_skip` variables;
- ten visit blocks;
- four weight candidates: `weight`, `weight_pop`, `weight_trt`, `weight_pop_trt`;
- complementary base/top-up weight missingness;
- official questionnaire routing/sampling-approach rules;
- official technical-report design/post-stratification/population-weight law.

The codebook says `TR with top up sample`; the technical report documents a Türkiye sample adjustment. This packet does **not** infer that `TR` is an authoritative token for Türkiye or that the two top-up fields have a universally lawful default domain. That remains a named documentary boundary.

## Raw-read economy

R07 performed **no new DTA cell scan**. That is deliberate: accepted SR03 plus accepted SR09-PRE R07 already close every named physical burden needed for packet construction. The only current raw-source operations were Library materialization, frozen ZIP hash verification, selective extraction of the four assigned members, and exact source-member hash/size verification.

## Required return token

`PRE553_SOURCE_CERT_PREP71_R07_RETURNED`
