# SOURCE CERT PREP71 — R04 EVS RETURN

Status: `PRE553_SOURCE_CERT_PREP71_R04_RETURNED`  
Authority: packet preparation only; **NO SOURCE CERTIFICATION WAS PERFORMED**.

## Exact execution anchor

- Repository: `maidiu/rawlsing`
- Worker branch: `agent/vozhd-trii-srcprep71-r04-evs`
- Exact starting HEAD: `0ac2a8c00ca5718f293e98f98be6685f67ea2445`
- Raw Library transport: `surveys.zip`
- ZIP size: `158180333` bytes
- ZIP SHA-256: `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`
- Five extracted source members were SHA-verified before probing.
- Local WVS70 process: **untouched**.

## Packet dispositions

| Source | SHA-256 | Rows × cols | Native encoding declaration | Native MR sets | Fixtures | Packet disposition |
|---|---|---:|---|---:|---:|---|
| EVS 1981.sav | `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2` | 19,378 × 370 | `windows-1252` / character code `1252` | 0 | 5 | `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED` |
| EVS 1990.sav | `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec` | 38,213 × 390 | `windows-1252` / character code `1252` | 0 | 5 | `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED` |
| EVS 1999.sav | `6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a` | 41,125 × 513 | `UTF-8` / character code `65001` | 0 | 8 | `PACKET_READY__DOCUMENTARY_AUTHORITY_REQUIRED_BEFORE_CERTIFICATION` |
| EVS 2008.sav | `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379` | 66,280 × 477 | `UTF-8` / character code `65001` | 13 | 9 | `PACKET_READY__DOCUMENTARY_AUTHORITY_REQUIRED_BEFORE_CERTIFICATION` |
| EVS 2017.sav | `95096c2474b81ef12004726e4ed5b0919b1ea7bb672baff676ae40fb1b629bd2` | 59,438 × 474 | `UTF-8` / character code `65001` | 2 | 9 | `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED` |

## Encoding finding that changes the pre-recon question

Targeted source-byte inspection found an SPSS **type-7/subtype-20 character encoding record** in every assigned SAV. EVS 1981/1990 declare `windows-1252`; EVS 1999/2008/2017 declare `UTF-8`. The associated machine integer records agree (`1252` and `65001`). Thus the intended encoding declaration for EVS 1999/2008 is **not unknown**: the source itself declares UTF-8.

The hostile fact is instead an internal contradiction in the frozen files: EVS 1999 and EVS 2008 contain exact human-language metadata byte sequences that are invalid UTF-8 while other sequences are valid UTF-8-shaped text. This explains the governed default-reader failure. The explicit `latin1` reader remains lawful only for deterministic physical extraction and retains authority status `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`. It does **not** supersede the source-native UTF-8 declaration.

## Exact documentary blockers

### EVS 1999

The source-native encoding declaration is closed as UTF-8, and official GESIS ZA3811 v3.0.0 variable/study documentation is externally locatable. What remains unclosed is a producer-authoritative, exact-release **field-level repair/alignment rule for malformed human-language strings in this exact SHA**. No such source-native or Library document was found. Therefore label-dependent certification must not choose Latin-1, mixed decoding, replacement characters, or text normalization heuristically.

### EVS 2008

The same blocker applies to the UTF-8-declared ZA4800-era source. Official ZA4800 v5.0.0 variable/method documentation is externally locatable, but no exact byte-to-authoritative-text repair map for the malformed SAV metadata was found in Library/source-native material. The 13 native MR sets are separately complete as **physical topology**: set names, type, counted value, and member lists are fixtures independent of compatibility-decoded label semantics. Duplicate-member aliases and overlapping sets are intentionally retained.

## Other packet burdens

- **EVS 1981:** positive discrete user-missing value `3` on `v308`; ranked `v460/f460/v461`; release-specific coordinates; `weight_g`; native IDs remain non-authoritative for replay identity.
- **EVS 1990:** `q745` is physically all user-missing; two ranked triplets; split-up coordinate family; `weight_g` + `weight_s`; native IDs remain non-authoritative for replay identity.
- **EVS 2017:** 11 system-missing cells must remain distinct from user missing; `dweight=-4` user-missing declaration; native MR sets `Q4` and `Q11`; mixed-mode/matrix/follow-up coordinate block; expanded weight/calibration family.

## Library/document search disposition

The Library raw transport and accepted SR03 checkout were found and hash verified. Additional Library codebook/project archives were materialized and searched, but contained only derived EVS review/ETL/structure surfaces, not the source-native ZA4438/ZA4460/ZA3811/ZA4800/ZA7500 documentation needed to authorize text repair. Official GESIS wave/variable/method documentation was located externally and is recorded only as `EXTERNAL_OFFICIAL_SUPPORTING`; it does not silently outrank source bytes. A GESIS DDI2 example for ZA3811 declaring `ISO-8859-1` is explicitly treated as **XML export encoding only**, not as SAV encoding authority.

## Scope / negative findings

- No certification disposition was issued.
- No C11 or source promotion was performed.
- No decoder contract was widened.
- No guessed encoding or text repair was performed.
- No substitute SAV reader was used.
- No database or production runtime was touched.
- No local WVS70 state was inspected or modified.
- All prepared write paths are restricted to `SOURCE_CERT_PREP71/RETURNS/R04/`.

Required token: `PRE553_SOURCE_CERT_PREP71_R04_RETURNED`
