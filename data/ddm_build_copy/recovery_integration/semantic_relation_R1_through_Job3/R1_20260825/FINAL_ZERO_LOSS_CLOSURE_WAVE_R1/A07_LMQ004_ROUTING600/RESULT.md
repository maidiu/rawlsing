# A07 — LMQ-004 EXACT 320+280 ROUTING CLOSURE / GOVERNED-KNOWN-ABSENCE R1

Status:

`FAIL_CLOSED__EXACT_600_ROW_IDENTITY_AND_LATER_SOURCE_NODE_CROSSWALK_RECOVERED__0_POSITIVE_ROUTING__0_GOVERNED_KNOWN_ABSENCE__600_STILL_UNRESOLVED`

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-a07-lmq004-routing600-r1`

Verified exact starting HEAD:

`0502c942d683dc3aad107d2b04c4b9e307cfa9be`

Governing authority:
- Authority 41 at the launch HEAD.
- Z03 exact prior return: `0c0e0704be91a5e19c9c524e3f29cd081495b721`.

## 1. Holding

A07 materially improves LMQ-004 evidence but does **not** close LMQ-004.

The historical 600-row denominator is now fully recovered at exact row grain and crosswalked one-to-one to later governed source-native/deep question-node rows:

- historical `FAIL_CLOSED_NO_SOURCE_ROW_MATCH`: **320**
- historical `FAIL_CLOSED_UNRESOLVED`: **280**
- target rows: **600**
- unique historical closure hashes: **600**
- exact one-to-one later source-node matches: **600**
- unmatched: **0**
- multimatch: **0**

But the row-level later evidence does not supply either:
1. an exact executable positive routing predicate/instruction; or
2. an exact governed source-level known-absence/nonapplicability ruling.

Therefore A07 adjudicates:

- `EXACT_LATER_POSITIVE_ROUTING_AUTHORITY`: **0**
- `EXACT_GOVERNED_KNOWN_ABSENCE_OR_NONAPPLICABILITY`: **0**
- `STILL_UNRESOLVED`: **600**

`LMQ004 = OPEN_FAIL_CLOSED`

## 2. Exact historical wrapper recovery

A07 positively recovered the exact Library archive that Z03 could identify only by wrapper identity:

`Rawlsing_R3_Routing_Applicability_Retrieval_Delta_20260808.zip`

Library file id:

`file_000000003dd4822f96b9fea78fb5565b`

Exact size:

`1,791,065`

SHA-256:

`e27ceb340eac5d7124e44b80081e5c0309a342326c045df6d6f6d0cd71910c46`

The archive contains the exact executable-era routing/applicability surfaces:
- `authority/question_applicability_predicate_authority_full_v1.json`
- `phase_readiness/routing_provenance_ledger.csv`
- `phase_readiness/routing_authority_compile_summary.json`
- `phase_readiness/routing_unresolved_ledger.csv`
- producer/compiler and validators.

Direct byte checks match the internal manifest.

Critical exact member identities:
- applicability authority: `71cec3a5084601f890db9ba5439fd31c5f9cd300d3953bb4f584685fa5a77dda`; 18,518 rows.
- routing provenance: `ce10e4c9ed9b5128329a093beaf266ea775031a11b47e43ca6edd25eb2937fbb`; 700 rows.
- routing unresolved ledger: `b4aef414eb7230e9c710b4fc5fdb5263f7d75f8c69a1a91526f51167deacce99`; 699 rows.
- compile summary: `b75f7b98a5357cd8c6d73e4c25d077f225406ab41e804d14f48a99cf4ef0979d`.

Captured historical validators report:
- applicability: `PASS`, 18,518 rows, all fail-closed, no duplicate keys;
- routing: `PASS`, 700 rows, 699 unresolved.

The historical partition directly replays as:

`1 universal + 99 source-signaled + 320 no-source-row-match + 280 unresolved = 700`

No aggregate reconstruction is used.

## 3. Historical row identity law

The 600 target rows each have a unique exact `closure_hash`.

The 280 historical `FAIL_CLOSED_UNRESOLVED` rows also carry exact historical `question_implementation_id`.

The 320 historical `FAIL_CLOSED_NO_SOURCE_ROW_MATCH` rows deliberately have an empty historical `question_implementation_id`: that emptiness is part of the historical failure state, because no source-routing row matched.

A07 therefore does **not** fabricate implementation IDs for those 320 rows.

Their exact historical identity is preserved by:
- closure hash;
- source family;
- wave;
- country/module scope;
- source variable code;
- exact source hash/locator;
- original status and reason.

A later recovered implementation ID is stored only in a separate `later_question_implementation_id` field.

## 4. Later governed source-node crosswalk

A07 used the Library `LAYER1_GOVERNED_35WAVE_CATALOGS.zip`:

- Library id: `file_000000006f64822f8ac5e0b134e6976b`
- SHA-256: `b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d`
- exact active implementation rows: **18,276**
- exact active scopes: **35**
- source families: **9**

The companion `87_PRE_V553_LAYER1_35WAVE_CONTRACT_AUDIT.zip` is:
- Library id: `file_00000000c458822fbe27f0151bf6fd4b`
- SHA-256: `fc7e687829a8f5cae175609761d7605b1cb541fc9fdc47bdf9ec2b17ebf5659f`

That audit records governed-selection-input sufficiency as `PASS` while explicitly not asserting perfect raw external-codebook completeness.

Crosswalk law:
- 280 historical unresolved rows: exact `question_implementation_id` match.
- 320 historical no-source-row-match rows: exact `(source_family, wave, source_variable_code)` match, because the historical implementation-ID field is blank by construction.

Result:
- `600 / 600` exact one-to-one later source-node matches.
- zero inferred/fuzzy/theme joins.
- zero duplicate matches.

The complete 600-row ledger is returned as four ordered 150-row shards:

- `LMQ004_ROUTING600_ROW_LEDGER_001_150.csv` — SHA-256 `4a0cb8f2eab6eb809ec64b17c1b0ba489790045ff865ac7b833f115118d421cb`
- `LMQ004_ROUTING600_ROW_LEDGER_151_300.csv` — SHA-256 `3936553981195fa54703106376418d5738621a2ee33d94838e58534b8dce0e56`
- `LMQ004_ROUTING600_ROW_LEDGER_301_450.csv` — SHA-256 `16700a0088f11849a7ff4cbb35bf015d767d9136da2ae89eed1c8361586e08c6`
- `LMQ004_ROUTING600_ROW_LEDGER_451_600.csv` — SHA-256 `b0a5bf6a6cb6ef4fd8de51be6a2c42a6acba2bbf8670aee42b748642e06b172c`

Ordered shard-set SHA-256:

`ed39860434a509e9b234beb01e0297ae4decb19ee7d73c882f252dd3d4fd41c6`


The row ledger shards use a compact lossless encoding to keep the governed return bounded. The historical `closure_hash` and later `exact_identity_sha256` are encoded as unpadded base64url of their exact 32-byte SHA-256 digests; single-character codes preserve historical state, match rule, routing status, and respondent-universe status. `DENOMINATOR_PROOF.json` carries the exact decoding codebook. Every ledger row has the A07 adjudication `STILL_UNRESOLVED`.

## 5. Why later node recovery does not close routing

The later catalogs preserve source text, response authority, routing signals, respondent-universe status, country coverage, and exact source-node identity. That is materially stronger evidence than Z03 had.

But the statuses remain fail-closed at routing authority grain.

Exact row-state combinations are:

- `FAIL_CLOSED_NO_SOURCE_ROW_MATCH` → `ROUTING_OR_INAPPLICABILITY_SIGNAL_PRESENT` / `EXACT_ROUTING_INSTRUCTION_NOT_RECOVERED_SIGNAL_ONLY`: **297**
- `FAIL_CLOSED_NO_SOURCE_ROW_MATCH` → `NO_ROUTING_SIGNAL_IN_RESPONSE_AUTHORITY` / `EXACT_UNIVERSE_NOT_ASSERTED_NO_ROUTING_SIGNAL`: **14**
- `FAIL_CLOSED_NO_SOURCE_ROW_MATCH` → `NO_ROUTING_SIGNAL_IN_RESPONSE_AUTHORITY` / `COUNTRY_INSTRUMENT_AVAILABILITY_VARIANT_EXACT_UNIVERSE_NOT_ASSERTED`: **9**
- `FAIL_CLOSED_UNRESOLVED` → `NO_EXPLICIT_ROUTING_SIGNAL_IN_PACKET` / `WAVE_OR_RELEASE_GENERAL_UNIVERSE`: **124**
- `FAIL_CLOSED_UNRESOLVED` → `NO_EXPLICIT_ROUTING_SIGNAL_IN_PACKET` / `EXPLICIT_PACKET_RESPONDENT_SCOPE`: **50**
- `FAIL_CLOSED_UNRESOLVED` → `NO_EXPLICIT_ROUTING_SIGNAL_IN_AVAILABLE_MERGED_METADATA` / `ROUND_GENERAL_RESPONDENT_UNIVERSE`: **41**
- `FAIL_CLOSED_UNRESOLVED` → `NO_ROUTING_SIGNAL_RECOVERED` / `EXACT_RESPONDENT_UNIVERSE_NOT_ASSERTED`: **26**
- `FAIL_CLOSED_UNRESOLVED` → `ROUTING_UNRESOLVED_RESPONSE_AUTHORITY_GAP` / `EXPLICIT_PACKET_RESPONDENT_SCOPE`: **14**
- `FAIL_CLOSED_UNRESOLVED` → `ROUTING_UNRESOLVED_RESPONSE_AUTHORITY_GAP` / `WAVE_OR_RELEASE_GENERAL_UNIVERSE`: **13**
- `FAIL_CLOSED_UNRESOLVED` → `NO_ROUTING_SIGNAL_RECOVERED` / `CONDITIONAL_UNIVERSE_SOURCE_SIGNAL_PRESERVED`: **4**
- `FAIL_CLOSED_UNRESOLVED` → `ROUTING_UNRESOLVED_RESPONSE_AUTHORITY_GAP` / `ADMINISTRATIVE_OR_DERIVED_UNIVERSE`: **3**
- `FAIL_CLOSED_UNRESOLVED` → `ROUTING_UNRESOLVED_RESPONSE_AUTHORITY_GAP` / `ROUND_GENERAL_RESPONDENT_UNIVERSE`: **3**
- `FAIL_CLOSED_UNRESOLVED` → `NO_EXPLICIT_ROUTING_SIGNAL_IN_AVAILABLE_MERGED_METADATA` / `ADMINISTRATIVE_OR_DERIVED_UNIVERSE`: **2**

The crucial distinctions are:

`SOURCE_NODE_RECOVERED != EXECUTABLE_ROUTING_PREDICATE`

`ROUTING_OR_INAPPLICABILITY_SIGNAL_PRESENT + EXACT_ROUTING_INSTRUCTION_NOT_RECOVERED_SIGNAL_ONLY != POSITIVE_ROUTING_AUTHORITY`

`NO_ROUTING_SIGNAL_RECOVERED != GOVERNED_KNOWN_ABSENCE`

`NO_EXPLICIT_ROUTING_SIGNAL_IN_PACKET != SOURCE_LEVEL_NONAPPLICABILITY`

`OBSERVED_COUNTRY_COVERAGE != ROUTING_NONAPPLICABILITY_AUTHORITY`

The 297 rows with a routing/inapplicability signal are especially important: the later catalog itself says the exact routing instruction was **not recovered**. A07 may not decide whether that signal means a positive gate or an inapplicability gate.

The rows with no recovered routing signal are likewise not known absences. Absence from a packet, response-authority surface, or merged metadata is not a governed assertion that no routing condition exists.

## 6. NO_SOURCE_ROW_MATCH and UNRESOLVED remain distinct

A07 explicitly preserves:

`FAIL_CLOSED_NO_SOURCE_ROW_MATCH != FAIL_CLOSED_UNRESOLVED`

The 320-row class means the historical routing compiler had no source row to join for that source coordinate.

The 280-row class means a source row/implementation identity existed but exact routing remained unresolved.

Later source-node recovery does not retroactively erase those historical meanings. Because no exact later routing/absence authority supersedes them, the final A07 ledger carries both:
- original historical status;
- current A07 disposition `STILL_UNRESOLVED`.

There is no common generic `NULL`, `UNKNOWN`, or `ABSENT` replacement state.

## 7. Current-line installation check

At the A07 launch HEAD, the canonical historical paths:
- `data/ddm_build_copy/authority/question_applicability_predicate_authority_full_v1.json`
- `data/ddm_build_copy/phase_readiness/routing_provenance_ledger.csv`

are not materialized in the current branch.

That absence does **not** prove routing absence. It only prevents claiming that the recovered historical executable authority was silently installed as the current successor.

Later governance also continues to identify complete normalized question-level routing/applicability as an unresolved preservation/runtime substrate rather than a closed current authority.

## 8. What this court closes

A07 closes the **identity/recovery uncertainty** around LMQ-004:

- exact historical wrapper recovered;
- exact 600 row identities recovered;
- exact 320/280 partition replayed;
- exact later governed source-node crosswalk established for all 600;
- exact later routing/universe statuses recorded per row;
- no row lost or aliased;
- no `NO_SOURCE_ROW_MATCH` / `UNRESOLVED` collapse.

A07 does **not** close the underlying routing-authority debt.

Minimum lawful future closure remains row-level:
- exact positive routing predicate/instruction, or
- exact governed known-absence/nonapplicability,
for each affected row, with exact source authority and replayable provenance.

## 9. Scope ceiling

A07:
- consumed Authority 41, Z03, the exact historical Library wrapper, and later governed source-native/deep catalogs;
- did not consume A06 or any A01-A10 sibling return;
- did not infer routing from source-column presence;
- did not create source authority;
- did not modify production/runtime/source data;
- did not select architecture;
- did not perform V3 work.

Machine-readable denominator proof:
`DENOMINATOR_PROOF.json`
SHA-256:
`8d4379da4cc29cfbda2a60f78d162bc79bca104dbff19fd1800f0ad3a231719f`

Terminal:

`A07_LMQ004_ROUTING600_R1_COMPLETE__EXACT_600_ROW_CROSSWALK_RECOVERED__LMQ004_REMAINS_OPEN_600_UNRESOLVED`
