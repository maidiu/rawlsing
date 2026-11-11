# VC4 C03 — NATIVE SOURCE EXECUTION CAPABILITY RECONNAISSANCE

Status: `PREPARED__NOT_LAUNCHED`
Branch: `agent/vozhd-chetiri-c03-native-source-access`
Write scope: `.../VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C03/`
Runtime writes: `FORBIDDEN`
Raw source probing: `YES__EXACT_HASH_MATCHED_ONLY`
Launch prerequisite: `G0_PASS`

## MISSION

Measure what the frozen SAV/DTA decoder stack can actually do as a compiler execution substrate. Produce terrain, not architecture preference.

## REQUIRED ACCEPTED INPUTS

Consume accepted C02/C06 findings only where they define information that must be preserved. Do not reinterpret them.

## ADDITIONAL READ-FIRST

- exact source inventory;
- decoder implementation and tests;
- all frozen compatibility-reader exceptions;
- prior native metadata reconnaissance receipts;
- source-specific hostile returns relevant to SAV/DTA reader behavior.

## PROVING SOURCE CLASSES

HQ shall pin exact SHA-matched representatives for:

1. ordinary SAV path;
2. SAV compatibility override path if behavior differs materially;
3. ordinary DTA path if available within CLOSED_35;
4. LiTS DTA compatibility path;
5. LiTS III known chunk/full-read hostile case.

Do not broaden source scope unless a named physical reader property requires it.

## MEASUREMENT MATRIX

For each source/path measure when supported:

- metadata-only open;
- full variable metadata extraction;
- one selected variable;
- 2/5/10/25/50/100 selected variables;
- repeated selected-variable sessions;
- sequential full read;
- chunked/row-range read;
- repeated chunked read;
- source setup/open latency;
- decode normalization latency;
- peak RSS;
- transient frame size where observable;
- scratch use;
- failure mode;
- whether reader forces full-frame allocation;
- whether selection occurs before/after decode;
- whether temporary conversion would avoid repeated parser work.

Repeat enough times to distinguish setup noise from stable cost; record run count and aggregation method.

## SEMANTIC GUARDRAILS

C03 measures execution only. It may not:

- reinterpret encodings semantically;
- infer missing-state meaning;
- alter decoder contract;
- recommend dropping metadata because reader access is expensive;
- claim a source-family semantic branch from a physical-reader difference.

Compatibility `latin1` remains execution compatibility only.

## REQUIRED OUTPUTS

- `NATIVE_SOURCE_ACCESS_CAPABILITY_MATRIX.csv`
- `NATIVE_SOURCE_COST_MODEL.md`
- `READER_FAILURE_AND_LIMITATION_LEDGER.csv`
- `C03_RESULT.json`
- common return files.

## REQUIRED COST-MODEL QUESTIONS

- Is column selection genuinely selective in I/O/memory or merely API-level selection after full decode?
- What setup cost is paid per open?
- Can one compiler session amortize full-frame decode across many predicates?
- Which sources defeat bounded chunking?
- Is ephemeral Arrow/DuckDB/Parquet conversion likely to be cheaper than repeated native reparse?
- What operations are impossible, merely slow, or efficient?

## FINAL DISPOSITIONS

- `C03_PASS__NATIVE_ACCESS_SUPPORTS_SELECTIVE_OR_AMORTIZABLE_COMPILATION`
- `C03_PASS__NATIVE_AUTHORITY_REQUIRES_SESSION_MATERIALIZATION_FOR_NAMED_SOURCES`
- `C03_BLOCK__NATIVE_READER_PATH_OPERATIONALLY_UNUSABLE_WITHOUT_FULL_TRANSFORM`
- `C03_RETURN__NAMED_SOURCE_READER_AMBIGUITY`
- `C03_BLOCK__SOURCE_IDENTITY_OR_READER_CONTRACT_FAILURE`

STOP token: `VC4_C03_RETURNED`
