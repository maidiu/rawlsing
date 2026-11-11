# GT3/GT4 N2 — Q69B EXACT SOURCE TRANSPORT + MATERIALIZATION R1 — RETURN

Terminal disposition:

`PASS__GT34_N2_Q69B_EXACT_SOURCE_TRANSPORT_AND_BOUNDED_C11_CANDIDATE_MATERIALIZED__NO_ADOPTION`

Exact working-ancestry start:

`bca519e3d39b7c3886210958800a4b47ecb50440`

The immutable instruction ref was evidence only. Working ancestry began from the exact start above.

The exact terminal branch SHA is reported by final branch readback after this return is committed; a Git commit cannot content-address itself without changing its own SHA.

---

## Holding

N2 closes the M1B physical-byte/materialization blocker.

The exact already-accepted Afrobarometer R5 SAV bytes were recovered from the official Afrobarometer resource as **byte recovery only**, verified against the absolute accepted byte identity before any row-semantic read, and were never committed.

A deterministic repo-native Q69B transport is now committed and reconstructs a new bounded PRE553/C11 Q69B candidate release without source reacquisition.

The predecessor:

`R5_GT12_Q86A_Q86B_FROZEN`

remains immutable.

No authority is adopted.
No comparator predicate is executed.
No PSEPF is created.
No actor state is read or mutated.
No GT1/GT2 identity is altered.

---

# 1. Exact source recovery

Accepted source identity:

`Data/Afro Barometer Round 5.sav`

Official byte-recovery resource:

`https://www.afrobarometer.org/wp-content/uploads/2022/02/merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav`

Verified byte count:

`49,689,458`

Verified SHA-256:

`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

Verified rows:

`51,587`

Parser/runtime at source court:

- CPython `3.12.14`
- pyreadstat `1.3.6`
- source columns `348`

Required parser ordinals, zero-based:

- `COUNTRY = 0`
- `RESPNO = 4`
- `DATEINTR = 36`
- `Q69B = 226`

Checkpoint-1 source-byte verification occurred before row-value execution.

No different R5 source version was selected.

---

# 2. Write-ahead checkpoint 1

Durable checkpoint:

`N2_Q69B_SOURCE_TRANSPORT_MATERIALIZATION_R1/01_CHECKPOINT1_EXACT_SOURCE_VERIFIED.md`

Persistence commit:

`e5c5ef4cbadfabd3ae9776fba786111744c63c45`

Checkpoint-1 court:

- run: `33997340315`
- job: `101390055906`
- result: `1 passed, 1 warning in 7.50s`

The machine checkpoint proved:

- exact byte count;
- exact accepted SHA;
- exact metadata row count;
- required variable inventory;
- parser/runtime identity;
- `row_values_read = false`;
- `row_values_committed = false`.

An earlier byte-only write-ahead record is also retained as:

`00_WRITE_AHEAD_SOURCE_BYTE_IDENTITY.md`

because the very first court proved byte identity before a parser-output dependency failure. It contains no row-value claim.

---

# 3. Exact authorized source read

N2 read only:

- source row ordinal;
- COUNTRY;
- RESPNO;
- Q69B;
- DATEINTR;

plus parser metadata required to verify labels/types.

No unrelated survey response entered the source read or the committed transport.

## Physical Q69B metadata

Physical SAV variable label:

`Q69b. Problems with public clinic: lack of medicine/supplies`

Physical variable-label SHA-256:

`dde1209298f540807c76b4df0131ef3defdbfab954523d51cf88bc105569c656`

Parser type:

`double`

Original SAV type:

`F3.0`

User-missing ranges:

`[]`

Exact physical SAV value dictionary:

| code | physical SAV label |
|---:|---|
| -1 | Missing |
| 0 | Never |
| 1 | Once or Twice |
| 2 | A Few Times |
| 3 | Often |
| 7 | No experience with public clinics in past year |
| 9 | Don't Know |
| 998 | Refused |

Physical label-string SHA-256 values:

| code | SHA-256 |
|---:|---|
| -1 | `6be36ca49ee85210c5d1ad9c377d90a9859c66d889110a2a5b0dccd390d12e20` |
| 0 | `6300ef800bb884295b0b4b35682b75cecd7cc550d202db56d04a0643b8fb873f` |
| 1 | `10ee594fbc8b5fdbbd6c8f0cbace445f29d4c1ea8f5ad3bc43499269207a3aaa` |
| 2 | `a4239167b9d496b19db9ca3aeed65b173e8b0e5799dac86b7d4aef577c1c744b` |
| 3 | `6f6f6b4ab1bd157aa91c23a7431ca3fba2fd776bd21ea5889cb499f2be455d10` |
| 7 | `deb6b0aa72a2ff65d4cb2bcbcf12336f70ab6e8f8106bcd748f1883291bed304` |
| 9 | `1739decca1909c0ab754009313b5df6ee59c44d2c3493aa7df327a25fe953fd1` |
| 998 | `66b873543aebf01b33f9a69013d6ba1291d31dafbdcd29051e9dd94fe90b7245` |

Accepted codebook-normalized variable-label hash remains:

`78750307701922ed45ff5df4c7d83c57ffb7cb1b273134ef6594fe777f1e5ff0`

Accepted Q69B question-text hash remains:

`d235a464e0b36db851134fe2ced54f9ccade94370c719ebdafe89cc14ab4ff9d`

Accepted B-F routing-note hash remains:

`62823c05f73b724d96fba327511bf1e82b4c3afd17ad0ad54dd36fe0e4c4cb20`

Accepted codebook SHA-256:

`7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`

The SAV carries shorter/case-different physical label strings than the codebook-normalized prose at several codes. N2 preserves those two identity layers separately.

There is no semantic contradiction:
- the exact native code set is the expected eight-code set;
- no undocumented code occurs;
- code 7 remains the explicit no-public-clinic-experience branch for the source lookback;
- code 9 remains nonknowledge;
- code 998 remains refusal;
- -1 remains missing;
- 0-3 remain the experienced-clinic branch and are not used as a downstream metric.

Therefore:

`FAIL__GT34_N2_Q69B_PHYSICAL_SOURCE_CONTRADICTS_ACCEPTED_CODEBOOK_SEMANTICS`

does not apply.

## DATEINTR metadata

Physical label:

`Date of interview`

Parser type:

`double`

Original SAV type:

`EDATE8`

User-missing ranges:

`[]`

DATEINTR counts:

- valid: `51,587`
- missing: `0`
- invalid: `0`

Exact observed ISO span:

`2011-10-20` through `2013-06-04`

No query-time, wall-clock, or actor-current-time substitution is authorized.

---

# 4. Exact physical counts

Native Q69B counts:

| native code/state | count |
|---:|---:|
| -1 | 79 |
| 0 | 12,951 |
| 1 | 8,213 |
| 2 | 10,822 |
| 3 | 10,670 |
| 7 | 8,554 |
| 9 | 298 |
| 998 | 0 |
| physical system missing | 0 |
| **total** | **51,587** |

Typed endpoint counts:

| typed endpoint state | count |
|---|---:|
| PUBLIC_CLINIC_EXPERIENCE_PRESENT | 42,656 |
| PUBLIC_CLINIC_EXPERIENCE_ABSENT | 8,554 |
| UNKNOWN | 298 |
| REFUSAL_NOT_LAWFULLY_CONDITIONABLE | 0 |
| MISSING | 79 |
| PHYSICAL_SYSTEM_MISSING | 0 |
| **total** | **51,587** |

No frequency order is used downstream.

---

# 5. Source execution / transport court

Exact source-to-transport successful court:

- run: `33997931508`
- job: `101391606286`
- result: `1 passed, 22 warnings in 8.22s`

The warnings are deliberate machine-readable evidence:
- one stage-2 manifest;
- one transport chunk-count receipt;
- nineteen deterministic transport chunks;
- exact physical-label evidence.

That court verified:

- source bytes `49,689,458`;
- source SHA `c920...b651`;
- rows `51,587`;
- exact physical Q69B dictionary;
- exact DATEINTR physical metadata;
- `51,587 / 51,587` unique respondent bindings;
- no undocumented Q69B native code;
- all DATEINTR anchors valid;
- deterministic canonical transport replay.

---

# 6. Repo-native transport

Committed transport:

`N2_Q69B_SOURCE_TRANSPORT_MATERIALIZATION_R1/transport/q69b_exact_source_transport.json.gz`

Transport seal commit:

`07eb6aed4e0fdb3607cc7f6fa54618e053cd5179`

Schema:

`GT34_N2_R5_Q69B_EXACT_SOURCE_TRANSPORT@1.0.0`

Canonical semantic bytes:

`5,275,419`

Transport semantic SHA-256:

`c90ef7eaeea4b1536d3153beb344ce22156bf15bf835a3182c1b5784b8f238c5`

Deterministic gzip bytes:

`332,746`

Deterministic gzip SHA-256:

`bbf256e01beef96d29a0a00517348d983ebfa718a320acc16787a9a3c59ab719`

Git blob SHA:

`0837cd9b748544a01e8fa97f233fa41e10544d79`

The committed transport contains only:
- exact row ordinal;
- exact respondent binding;
- Q69B native code + typed state;
- DATEINTR exact raw token + ISO anchor + typed state;
- exact source/parser/codebook/value-label/semantic provenance.

The raw SAV is absent.

The production loader accepts no caller-selected source path, authority, release, or current identity.

---

# 7. Respondent identity court

R5 respondent namespace:

`FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`

Respondent carrier SHA-256:

`6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`

Source-structure identity:

`cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`

Source-structure SHA-256:

`ea9614b69e63a8e5bc87e65c944d67445082639fe45262da626bd6aa1a4d9e99`

Exact N2 reconstructed respondent identities:

`51,587`

Unique identities:

`51,587`

Exact current GT2 respondent refs matched:

`19,210 / 19,210`

The current GT2 respondent subset is therefore exactly compatible with the new full-source Q69B respondent namespace.

No fuzzy respondent linkage is used.

---

# 8. New bounded C11 candidate release

Production implementation:

`rawlsing_next/wave2_r5_q69b_conditioner_projection.py`

Retained repo-native verification:

`rawlsing_next/tests/test_wave2_r5_q69b_conditioner_projection.py`

Candidate release ID:

`R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1`

Final release semantic SHA-256:

`2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec`

Source-release-manifest SHA-256:

`15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4`

Replay manifest:

- kind: `C11Internal:ReplayManifest`
- content hash: `8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539`
- object ID: `urn:rawlsing:pre553:c11:ReplayManifest:sha256:8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539`

Candidate logical counts:

- EmpiricalUniverse: `1`
- RespondentIdentity: `51,587`
- QuestionVariableBinding: `1`
- RespondentEvent: `51,587`
- RoutingEligibilityFact: `51,587`
- EmpiricalCoordinateFact: `51,587`
- AuthoritySnapshot: `8`
- ReplayManifest: `1`

The existing I02 atomic C11 validator accepted the candidate and closed M01-M18.

A second reconstruction produced the exact same:
- release ref;
- source-release-manifest hash;
- replay-manifest ref.

---

# 9. Endpoint / semantic hashes

Canonical endpoint coordinate:

`Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS`

Coordinate hash:

`7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937`

Repaired coordinate authority candidate:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY@1.0.0`

Repaired authority hash:

`cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`

Rejected overbroad authority hash:

`3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a`

The rejected hash is absent from the candidate package.

Crosswalk:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_STATUS_CROSSWALK@1.0.0`

Crosswalk hash:

`fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095`

Time rule:

`R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR@1.0.0`

Time-rule hash:

`4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2`

Measure basis:

`R5_Q69B_RAW_CONDITIONER_MEMBERSHIP_BASIS@1.0.0`

Measure-basis hash:

`f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3`

Every final coordinate fact explicitly binds:
- source snapshot;
- codebook;
- empirical universe;
- respondent;
- native Q69B coordinate/question material;
- exact raw Q69B value;
- physical domain fingerprint through the native coordinate/question refs;
- exact crosswalk authority;
- exact respondent DATEINTR anchor;
- exact time-rule authority;
- repaired coordinate authority;
- currentness;
- measure basis;
- committed N2 transport.

The sealed C11 replay manifest binds every produced coordinate ref/hash and the release hash.

---

# 10. Write-ahead checkpoint 2

Durable checkpoint:

`N2_Q69B_SOURCE_TRANSPORT_MATERIALIZATION_R1/02_CHECKPOINT2_TRANSPORT_AND_C11_CANDIDATE_VERIFIED.md`

Final checkpoint-2 persistence commit:

`cbee4664b6de78ceccd80f9570f81893650438de`

Final provenance-complete focused seal court:

- run: `33999047513`
- job: `101394521336`
- result: `11 passed, 1 warning in 164.49s`

The warning is the machine-readable C11 identity receipt.

---

# 11. Regression court

Final provenance-complete inherited regression court:

- execution commit: `4b222815913cd217649b406469de689ffb2fc45a`
- run: `33999269473`
- job: `101395104942`
- result: `122 passed, 1 warning in 174.82s`

Executed suites:

- `test_wave2_r5_q69b_conditioner_projection.py`
- `test_wave1_r5_q86_c11_projection.py`
- `test_pre553_c11_repository_ingest.py`
- `test_pre553_empirical_objects_authority.py`
- `test_pre553_replay_audit.py`
- `test_pre553_repo_native_current_rehydration.py`

This proves the final N2 implementation remains compatible with:
- inherited Q86 projection law;
- C11 package-atomic ingest;
- PRE553 exact authority closure;
- replay hostility;
- current GT2 repo-native query/fact transport.

A superseded broader regression attempt included:

`test_pre553_source_backed_c11_facade.py`

and stopped during collection because the governed runner does not install pandas. That run executed no failing N2 assertion and is not used as regression evidence. The final executable inherited subset above is green.

---

# 12. Hostile conditions

N2 explicitly rejects/fails closed on:

- wrong committed transport gzip SHA;
- wrong canonical transport semantic SHA;
- wrong source SHA;
- wrong source row count;
- wrong Q69B physical variable label;
- wrong Q69B physical value dictionary;
- wrong Q69B physical type;
- undocumented Q69B code;
- physical system-missing Q69B state not present in the sealed transport;
- wrong DATEINTR physical label/type;
- missing/invalid DATEINTR in the sealed candidate;
- respondent-key collision;
- current-GT2 respondent exact-ref mismatch;
- crosswalk typed-state mismatch;
- transport provenance drift;
- source/current/path selector override;
- rejected overbroad coordinate authority;
- Q69B frequency-order use as metric;
- query-time/wall-clock/actor-current-time substitution;
- mutation of the Q86 predecessor.

Typed nonpositive Q69B states remain nonpositive:
- code 9 -> UNKNOWN;
- code 998 -> NOT_LAWFULLY_CONDITIONABLE;
- code -1 -> MISSING.

No source response becomes actor history.

---

# 13. Immutable predecessor / no-adoption boundary

Predecessor:

`C11LogicalRelease / R5_GT12_Q86A_Q86B_FROZEN / 8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`

N2 does not mutate it.

N2 does not alter:
- Q86 query identity;
- Q86 fact identity;
- Q86 replay identity;
- `GT12-A-R5-COUNTRY-ALPHA3@1.0.0`;
- GT1/GT2 adoption/currentness;
- any actor fact;
- any V3 state.

The new release and repaired Q69B authority remain **candidate material only**.

No comparator authority is created or executed.

---

# Terminal

`PASS__GT34_N2_Q69B_EXACT_SOURCE_TRANSPORT_AND_BOUNDED_C11_CANDIDATE_MATERIALIZED__NO_ADOPTION`

Physical-source blocker:

**closed**

Exact-source recovery:

**verified**

Repo-native transport:

**sealed**

New bounded C11 candidate:

**materialized and deterministically rehydratable**

Checkpoint 1:

**persisted**

Checkpoint 2:

**persisted**

Inherited regression:

**green — 122 passed**

Raw SAV committed:

**no**

Authority adoption:

**no**

Comparator execution:

**no**

PSEPF:

**no**

Actor mutation:

**no**
