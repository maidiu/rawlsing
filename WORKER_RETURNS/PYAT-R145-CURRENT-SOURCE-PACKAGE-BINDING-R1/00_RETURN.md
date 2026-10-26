# R145 — current source-package prerequisites (metadata-only)

**Status:** `METADATA_PACKAGE_PREPARATION_COMPLETE__SOURCE_ACCESS_AND_SEMANTICS_PENDING`
**Base:** `44e7ace44d9e1b023a15d14ee1ead9b176d0e522` (native engine read-only)
**Scope:** GSS2024 (SRC23) first, then independent GSS2016 (SRC22) and LiTS-IV (SRC30) dictionaries. Survey files were not opened, stat'ed, hashed or decoded.

## Built capability

`runtime/source_package_binder.py` is a reusable, source-parameterized metadata-only package binder. It:

- verifies staged dictionary SHA-256 and byte pins before parsing;
- retains every codebook row with exact row hash, row identity, full question/option/note fields, classification evidence and `retained=True`;
- classifies administrative/weight/design/household/person-repeated/ranked-or-MR/text/unknown-measure/substantive-question candidates from row evidence, never module guess alone;
- produces a pending canonical package preparation record rather than a fabricated `NativePreimageBundle`;
- carries exact source/host/purpose/freeze/extent metadata in a `SourceReadRequest` **template**, with edition SHA explicitly pending and `survey_file_touched=false`;
- names prospective source-role/U/Epre status (`UNASSIGNED/PENDING`), native owner refs and the producer -> empirical -> learned/product -> FF/V553 consumer sequence;
- preregisters F1 empirical closure, F2 discovery/no-drop, F3 M1 disposition and F4 FF/V553 confrontation outputs with exact owners;
- provides `runtime/bind_authorized_metadata_receipt.py`, which refuses missing/foreign/unauthorized metadata receipts and returns a typed `NativeSourceIdentity` mapping, never a response-read grant.

## Actual dictionary accounting

| Source | Rows | Unit | Dictionary SHA-256 | Role summary |
|---|---:|---|---|---|
| SRC23 GSS2024 | 980 | person respondent | `e0f83b61…b01d7` | 874 substantive candidates, 9 weight/design, 21 household/roster, 20 person/repeated, 7 admin identity, 30 admin metadata, 4 rank/MR, 15 held |
| SRC22 GSS2016 | 1018 | person respondent | `0cd58f71…ed36b` | 817 substantive candidates, 11 weight/design, 120 household/roster, 28 person/repeated, 7 admin identity, 18 admin metadata, 1 rank/MR, 16 held |
| SRC30 LiTS-IV | 1319 | household id with respondent items | `c88ab0ec…83d07` | 1015 unknown-measure held, 184 admin metadata, 94 household/roster, 18 text/non-numeric held, 5 weight/design, 3 admin identity |

Total: **3317/3317 rows retained**, zero duplicate native codes, full JSONL row accounting in `records/`.

No `NativePreimageBundle`, source grant, semantic role, U/Epre, query/fact/discovery, M1/B5/I4, learned/FF/V553 or current-source product was created. LiTS rows with `measure=unknown` remain held rather than assigned a scalar proxy.

## Verification

- Focused binder checks: **6 passed** (`evidence/focused.log`).
- Verified: dictionary pin/byte tamper and missing-column refusal; row hash/identity tamper; all-row conservation; no decoder/survey transport call; authorized metadata receipt roundtrip; wrong/missing receipt refusal; F1–F4 consumer preregistration.
- CLI receipt probe (synthetic fixture, **not an actual grant**) is in `evidence/CLI_PROBE.json`; it binds a typed `NativeSourceIdentity` and still reports `response_decode_authorized=false`.
- `records/SUMMARY.json` and `evidence/PROOF_RECEIPT.json` record source pins, rows, role counts and limits.

## Exact next prerequisites

1. User-authorized survey identity/header metadata receipt for GSS2024: exact edition SHA-256, format, row count, header variables. This is **metadata only**, not response access.
2. Separate applicable source-read grant/resolver for whole-file response decode; a metadata receipt must never be relabeled as decode permission.
3. Match physical header to codebook, then bind exact source roles/topology, U/Epre, country/population/time/design/weight authority and native grammar.
4. Run the existing source-native package -> projection -> query/discovery -> no-drop -> M1/M2/FF/V553 sequence only after the above and required use authority.

`next_call`: `python3 runtime/bind_authorized_metadata_receipt.py --scope .r61/r145-current-source-packages/inputs/METADATA_INPUTS.json --source-id SRC23 --receipt <authorized_metadata_receipt.json>`

## Limits

Metadata documents only; no actual survey access, source grant, scientific decision, all35/1890/F1–F8/global, learned/FF/V553, actor/V3, R09/CI/prod, N11/N12, Sorok/J52/W52 or current-source production claim. Full R134 goal and holds remain. The native engine and all core files are read-only.
