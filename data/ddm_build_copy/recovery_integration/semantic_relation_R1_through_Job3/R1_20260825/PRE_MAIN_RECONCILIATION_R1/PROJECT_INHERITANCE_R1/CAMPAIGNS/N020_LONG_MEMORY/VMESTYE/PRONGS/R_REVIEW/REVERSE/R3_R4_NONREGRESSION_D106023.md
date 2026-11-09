# ZL-17 R3 independent nonregression court — ZL-15 R4 exact HEAD

**Verdict:** `ACCEPT_SCOPED_S0_S1_REVERSE_DOCUMENTARY_REAFFIRMED_AT_R4__ZL16_RECEIVING_SEPARATE__NO_MERGE`.

Exact author candidate: [PR #864](https://github.com/maidiu/rawlsing/pull/864), HEAD **`d10602355c77564b2b6d50601ebba4fed4ac7d58`**. Direct comparison from previously received ZL-17 author cut `ffd994045319db496e642cd797b01b615cc85a24`: **one** additional commit. Protected PRE-MAIN remains `256d46bf425cc37e114465cddbe3c60e535766ab`; author PR draft/open/unmerged. This is the *same independent ZL-17 reviewer*, auditing R4 nonregression, not authoring ZL-15 corrections or passing ZL-16's separate D05/D06 court.

## Comparison, not author assertion

Nine changed paths: `DATA/IMPLEMENTATIONS.tsv`, `DATA/RELATIONS.tsv`, `PRONGS/J_JOIN/GENERATION_STAGE_COURT.tsv`, `REVERSE_NAVIGATION.md`, `00_RETURN.md`, new `E001_SOURCE_RECIPIENT_BRIDGE_R4.tsv`, `BUILD_ZL15_R4_RESIDUAL_REPAIR.js`, `VALIDATE_ZL15_R4.js`, `R4_ZL16_D05_D06_AUTHOR_RETURN.md`.

**All previously received ZL-17 core data blobs are byte-for-byte unchanged** from R3:

| Source | Git blob (same at both heads) |
| --- | --- |
| `DATA/OPERATION_TRACES.tsv` | `7fff7cf589f52d385dc1ecc9e03545cd3881eb9e` |
| `DATA/CONSUMER_EDGES.tsv` | `a7c09ff0ebe8faa92357232725ce0a1adbb907af` |
| `DATA/AUTHORITY_APPLICATIONS.tsv` | `bd833fd5d6e8a6f1cf54a691ef1df6316cdfdce8` |
| `DATA/EVIDENCE.tsv` | `75d6e2d29425b5f6438cd7808b1487bfd4e2691c` |
| `PRONGS/J_JOIN/SEAM_DEPENDENCIES.tsv` | `fe3efed2061c410984601067986a381e5cd73c2a` |
| `PRONGS/J_JOIN/CANDIDATE_TRANSFERS.tsv` | `1b3f7483f2a05f13d54e82e9adee84e8a0406de9` |

These source cuts already passed the independent R2 ZL-17 82-condition/332-consumer/332-negative/370-authority qualification court, including 12/12 hostile mutation refusals, recorded in `R2_INDEPENDENT_REREVIEW_FFD994.md` at reviewer commit `61f35102cdd301785a6dc6618f7060d23b91db02`.

## Independent exact delta readback

I fetched full old/new Git blobs, parsed each normalized record ID and compared every field.

- `IMPLEMENTATIONS`: **884 → 884**, no added/dropped IDs; **884 rows change only `code_symbol`**. The 883 without verified code evidence now read `NOT_PROVED_CODE_SYMBOL`, with `code_sha=NOT_PROVED_CODE`. The one verified N10E record `J-IM-ZL12-F-N10E` uses exactly `rawlsing_next/pre553_empirical_possibility_provider.py#provide_empirical_possibility_slice` in `code_symbol` and `underlying_code_path_symbol`, code commit `256d46bf...`. Prior report locators and provenance fields stay separate. No code presence→execution inference.
- `RELATIONS`: **8,502 → 8,503**. The **only added ID** is `JR-R4-E001-FINDING-TO-RECIPIENT`: `J-F-ZL12-F-E001` → `J-SEAM-NODE-5fb36fd14859ce80d2` whose node literal is `SOROK:E001`. Type is `HISTORICAL_E001_IDENTITY_TO_SOROK_RECIPIENT_CANDIDATE__OWNER_HELD`. Its exact existing evidence `J-EV-R3-SOROK-E001` resolves to historical original source commit `37915a47ed3e33a71ad8334c0aa505f5d65796ca` / blob `d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47`. Five E001 stage relation rows change only `evidence_id`, `grade`, `comment` to identity-only source witness; **zero other preexisting relations modified or lost**. No implicit empirical-Pyat-C11→Sorok-actor-C11 conflation.
- `GENERATION_STAGE_COURT`: **4,420 → 4,420**, only the five `J-STAGE-ZL12-F-E001-{DVA,TRII,CHETIRI,LONG_MEMORY,PYAT_CURRENT}` rows modified, only `corroborating_evidence_id`, `join_disposition`, `next_falsifier`. All now cite the same historical E001 identity/recipient witness and explicitly retain **`SEMANTIC_SUCCESSION_UNJOINED`**, not stage-functional proof. The other unresolved stage records are untouched.
- Cold reverse E001 at R4: source finding `J-F-ZL12-F-E001` → exact `SOROK:E001` recipient ← separate Pyat N11 and N12 owner-held candidate transfers; N11 ← N10W by original `ASTRA:REQ:N10W:N11` **MUST** source seam. The Sorok native C11 first reader remains `NONE_PROVEN`; N11/N12 actual release, consent and actor readset remain unproved.
- Revalidated at R4: **332/332** operation producer-edge IDs resolve and all consumer status `OPEN_PROOF_GAP`; **332/332** negatives reference valid EVIDENCE IDs; **370** authority records have direct/same-finding/typed unresolved evidence with **zero** affirmative applied-rule or enforced-refusal claims. All 82 original condition-bearing seam rows remain untouched.

## Independently implemented hostile R4 delta tests

Read-only in-memory baseline audit: PASS. Individual tamper cases, **12/12 refused**:

1. Report locator injected into unverified `code_symbol`.
2. Fake underlying symbol substituted for verified N10E.
3. Original report locator erased.
4. E001 finding→recipient bridge deleted.
5. E001 recipient changed to wrong node.
6. E001 bridge evidence replaced with generic marker.
7. E001 bridge relabeled as currently native.
8. E001 stage evidence cleared.
9. E001 stage falsely declared succeeded.
10. N10W→N11 MUST changed to IF.
11. Actual consumer false-green.
12. Authority applied-rule false-green.

This is our independent table-structure court on fetched immutable Git blobs, **not** execution of the author's Node validator, project sourcefree suite, native/S2/S3 or protected merger. No new affirmative functional proof is drawn.

## Terminal bounds / handoff

**ZL-17 R2 scoped acceptance survives unchanged at R4 exact author HEAD `d106023...`.** The new source-qualified finding→recipient bridge improves cold navigation without changing current consumer/authority/negative ceilings. Historical R1 REVISE and R2 acceptance remain separately preserved, not overwritten.

This is **not an independent ZL-16 acceptance** of its own D05/D06, though relevant R4 changes were checked for ZL-17 regression. ZL-16/#815/PR #866 must independently adjudicate the latest head; ZL-18/#817 is governed by its own receiving prerequisites. No actual native original35 run, Sorok actor import, first non-test reader, applied rule/refusal, S2/S3, zero-loss or merge is proved/authorized.

Terminal: `ZL17_R3_R4_NONREGRESSION_ACCEPT_SCOPED_S0_S1__ZL16_INDEPENDENT_GATE__NO_MERGE`.
