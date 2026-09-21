# FIABC-LM2-R1G — Minimal Local Q291 Physical Carrier Extraction

Status: `PASS__EXACT_FROZEN_Q291_CARRIER_PERSISTED__STOP`

Terminal:

`LOCAL_Q291_EXTRACTION_PASS__EXACT_FROZEN_CARRIER_PERSISTED__STOP_BEFORE_COMMON_C11`

Repository: `maidiu/rawlsing`

Exact base: `bed7d8b7c062e82ac28308905d755c80534cc8f0`

Worker branch: `agent/rabochii-premain-fiabc-lm2-r1g-local-q291-extraction-r1`

## Exact bounded execution

- Source: `/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`
- Source bytes: `185163494`
- Source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- Decoder: exactly one application-level `pyreadstat.read_sav` call
- Requested columns: `Q291G5`, `Q291P5`
- Ordered rows: `97220`
- Physical cells: `194440`
- Q291G5 ordinal: `388`
- Q291P5 ordinal: `394`
- Fresh missing declarations: exact frozen range `-5 .. -1` for both variables
- `pyreadstat`: `1.3.2`

Carrier:

`WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json`

- Bytes: `83340882`
- SHA-256: `1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e`
- Schema: `FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER@1.0.0`
- Candidate-neutral: `true`
- Contains candidate output: `false`

Execution receipt:

`WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/FIABC_LM2_R1F_Q291_EXTRACTION_RECEIPT.json`

## Invocation note

The first launcher process stopped at Python module import before entering `main()`. It performed zero source hash passes, zero source decoder calls, and wrote no output. The normative script remained byte-for-byte unchanged. The repository root was then supplied through `PYTHONPATH`, after which the single source-backed execution performed exactly one source hash pass and exactly one `pyreadstat.read_sav` call.

## Stop statement

No common C11 execution, oracle construction, Candidate A/B/C execution, I03, I05, measured P2X, WVS semantic inference, second source decode, retry with a different source, merge, rebase, or HQ/PR mutation was performed.
