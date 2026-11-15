# ZL-16 R1 — independent scope/coverage, adversarial no-drop and falsifier receipt

Review cut: `maidiu/rawlsing` ZL-15 PR #864 exact `6be7a62535f12e83628018b1942767371e842cac`. Protected static sourcecut: `256d46bf425cc37e114465cddbe3c60e535766ab`. Independent S0–S1 GitHub source/blob readback, **no project runner**.

## Exact read artifacts (immutable Git blob identity)

| Artifact | Blob | Parsed rows |
| --- | --- | ---: |
| Accepted P0 `CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv` | `65c1bbe4a602341c5caacca2d58dced31a23f382` | 6,125 |
| ZL-15 `DATA/FUNCTION_ATLAS.tsv` | `98df0d9642a3c3f5fa1ecbf7a9cf7251e32b9fa0` | 1,740 |
| ZL-15 `DATA/RELATIONS.tsv` | `3a4d51819858e51d4abc1d9431b56c0727540e8e` | 3,662 |
| ZL-15 `DATA/OPERATION_TRACES.tsv` | `4e903c2f3bc5ecae1b73c20982f30c27499af79d` | 332 |
| ZL-15 `DATA/AUTHORITY_APPLICATIONS.tsv` | `cf6a61c30f60c0fbb450454d7933ca3a1aedabae` | 370 |
| ZL-15 `DATA/CONSUMER_EDGES.tsv` | `03529cf44ff30aeb843e05651483c887b1be1309` | 332 |
| ZL-15 `DATA/EVIDENCE.tsv` | `c401cd18ebed7fec2d712e3798a092cf56f20607` | 2,718 |
| ZL-15 `DATA/IMPLEMENTATIONS.tsv` | `d8caad082b23cef140a145abe144c7bdaea5b3bc` | 884 |
| ZL-15 `J_JOIN/CONFLICTS_AND_REPAIR_ORDER.tsv` | `c27cd5d5db2291fbe81646e27b74f186396ce3e8` | 1,536 |
| ZL-15 `J_JOIN/FULL_ID_ANTI_JOINS.tsv` | `1833bd435cf4a126a0bfd75de847be0995dc9ccf` | 2,607 |
| ZL-15 `J_JOIN/HISTORICAL_AUTHORITY_58_INDEX.tsv` | `b0e225892f7df075ca18409c6c78390940cd8f9a` | 58 |

Read method: immutable GitHub blob content at the exact SHA; parse line-oriented TSV by literal tab and row headers. The P0 match key is `(estate_id, source_commit_sha, source_path, source_composite_id, record_grain)`; the prong observation key uses `source_grain` as the fifth member. Exact tuple membership, not fuzzy names or alias inference. Recounted `P0=6,125 unique`, prong observations `2,607`, matching `1,962`, distinct matching `1,869`, nonmatching `645`, distinct nonmatching `627`, matched repeated keys `88` and surplus observations `93`; both P0 ambiguity and asserted census-ID mismatch `0`. **PASS for the author's stated prong-observation→P0 right join arithmetic only.**

## P0-left remainder — separate denominator, no invented lost functions

Of the 6,125 accepted P0 identity rows, **4,256 do not occur as a matching exact tuple** in the joined prong observation sidecar. They still exist in P0 and must not be called deleted or equivalent by name. Exact independently checked estate group remainder:

| Estate | P0 total | Exact covered by prong sidecar | P0-left remainder |
| --- | ---: | ---: | ---: |
| `PYAT_SR01_2416` | 2,416 | 6 | **2,410** |
| `SOROK_SR01_1314` | 1,314 | 0 | **1,314** |
| `PYAT_SR01_UNRESOLVED373` | 373 | 0 | **373** |
| `SOROK_SR01_UNRESOLVED51` | 51 | 0 | **51** |
| `PROG_GAP49` | 49 | 0 | **49** |
| Commission/flight/section/gate source identities (21+18+11+9) | 59 | 0 | **59** |
| **P0-left total** | | | **4,256** |

The remaining source estates are exact-covered at their respective source tuples, including `LMX44`, `LMQ30`, `C6_F29`, `C6_AR58`, `C6_AUX7`, `C777_CASE55`, `PROG_COMPONENT62`, `PROG_SEAM82`, `PROG_OWNER345`, `R157_SOURCES35`, `RECENT_CAMPAIGN30`, `SOROK_ASSETS304`, `SOROK_FUNCTION144`, `SOROK_W1_INPUT100`, `SOROK_VERSIONED_SEAM38`. That means core named source identities survive the prong court, but the separate SR-01 classification overlays and administrative identity estate need an explicit master outside-graph disposition. Do **not** add 4,256 to a function count.

## Referential/path checks at exact candidate

- Canonical node table: 884 prong findings, 753 label hubs, LMX44, LMQ30, F29 = 1,740. All 332 operation IDs, 370 authority application IDs, 332 consumer-edge IDs, 1,536 conflict primary keys and AR58 indexed identities were loaded as separately allowed endpoint namespaces; no invented AR absence.
- Relationship types: `ASSIGNED_TO=1,312`, `REQUIRES_AUTHORITY=452`, `HELD_BY=1,868`, `ALIAS_OF=30`. A precise source→stage successor or conditional-loss relation type is **absent**.
- `J-UJ-...` held targets: 1,536/1,536 fail exact resolution against the above namespaces; corresponding actual court rows are `C-...`. These are documented questions, but the asserted edges are not key-resolvable.
- `from_id=UNRESOLVED`: 241 ZL08 `HELD_BY` rows for historical `D02_EMPIRICAL_SUCCESSION/CURRENT_PROOF_REFS.csv` source-grain proof records. They have `census_id`, such as `ZL01-005757`, in conflict/source tables; source anchoring is missing from graph edges.
- Dva/Trii/Chetiri fate: 566/884 finding rows all `UNRECONCILED`; remaining 318 are their own 151 Dva, 105 Trii, 62 Chetiri source returns, **not explicit stage-to-stage joins**.
- Underlying code provenance: `IMPLEMENTATIONS.code_sha=PRONG_REPORT_AT_*` in 884/884; `OPERATION_TRACES.code_symbol_at_sha` links to a prong TSV record in 332/332. Sourcecode locations sometimes survive in other fields, but these exact named fields are report provenance, not code provenance.

## Five hostile cold navigations (expanded to eight in `SOURCE_AT_SHA_TRACE_CASES.tsv`)

1. F03 QREL under W6/ambiguous/missing versus five-guard QUC row-none exception: direct original static code was read; proper conditional negative is *described*, but Dva/Trii/Chetiri/LM/current applied-rule and first-reader path is not a typed resolvable chain. **REVISE mapping; do not declare current loss.**
2. F08 GSS/1973/uswar `allowed_as_v551_relation_evidence=false`: direct override-selection code and P1 documentary case read. ZL09 source/C11 combined `F03F08` candidate has no link to F03/F08 old semantic-grain nodes; required refusal still not verified on a real current consumer. **REVISE mapping, HOLD native effect.**
3. Original F19 V550J same respondent and signed component: direct old `ddm_v550j_joint_patterns.py` was read; current F4 same-person sourcefree candidate and historical carrier losses are documented separately, but no original-source sign/denominator/negative parity plus first non-test reader is verified. **Open proof, no false green.**
4. Current recursion/invalidation and weights/null/zero: direct current `pre553_recursive_handoff.py`, `_pre553_query_eval.py` and `pre553_analytical_composition.py` were read. Static consumer possibilities exist but no original35 selected source, proper statistical issuer, negative replay or exact non-test terminal receipt. **Open proof, not proved missing.**
5. Pyat N11/N12 to Sorok E001: candidate/versioned recipient is identifiable, but no accepted licensed payload, owner readset, actor source grant or first consumer. 1,314 SR-01 overlay classifier rows remain outside the prong-exact crosswalk; they are not 1,314 actor tasks. **Open recipient and explicit no-drop.**

## Review-specific falsifiers/negative controls to rerun after author correction

- Delete or rename one `C-ZL08-...` conflict court row: the referential validator must fail rather than accept the `J-UJ-...` alias or a generic `UNRESOLVED` origin.
- Swap F03 QUC rule scope, `BLOCKED_EXCLUDED_ASIAN_W6` status or a single one of five predicates: typed exception and denial must diverge at a qualified output/consumer or remain explicit `NOT_RUN`.
- Change F08 GSS/1973/uswar allowed-use from `false` to `true`: no source- or scope-agnostic label join may silently promote it to accepted relation evidence.
- Add a fake cross-stage link with identical string label but different wave/risk/respondent/source authority: it must remain conditional/unjoined, not be counted as semantic equivalence.
- Remove a P0 record only from the prong-observation table: the P0-left ledger must still cover 6,125 with explicit nonjoined disposition, not report a false no-drop green.
- Substitute a prong report SHA into `underlying_code_sha`: structural provenance validation must reject it, while report provenance stays separately valid.
- Substitute a synthetic sourcefree N10/Sorok result for actual first non-test native read: current proof grade must remain held.

**No S2 negative test was run here.** These are bounded correction acceptance controls. Existing FIABC `144 reported PASS / 3 FAIL`, D05 F06/F11 authority holds, 49 alternate-cut GAP identities and all source permissions remain at their prior separate grades.
