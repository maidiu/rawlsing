# SOURCE CERT PREP71 — R01 AFROBAROMETER RETURN

Status: `COMPLETE__NON_DISPOSITIVE__PACKET_PREPARATION_ONLY`

Required token: `PRE553_SOURCE_CERT_PREP71_R01_RETURNED`

## Scope and source identity

Worker branch: `agent/vozhd-trii-srcprep71-r01-afrobarometer`

Exact starting HEAD: `0ac2a8c00ca5718f293e98f98be6685f67ea2445`

Assigned exact sources:

| Source | SHA-256 | Packet preparation disposition | Hostile fixtures |
|---|---|---|---:|
| Afro Barometer Round 1 | `6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2` | `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED` | 7 |
| Afro Barometer Round 5 | `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651` | `PACKET_READY__DOCUMENTARY_AUTHORITY_REQUIRED_BEFORE_CERTIFICATION` | 9 |
| Afro Barometer Round 9 | `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8` | `PACKET_READY__DOCUMENTARY_AUTHORITY_REQUIRED_BEFORE_CERTIFICATION` | 10 |

All raw input came from the frozen Library `surveys.zip` transport. The ZIP and all three extracted members were hash-verified before packet work. No local Rawlsing source directory or Authority-70/WVS7 run was accessed.

No source is certified by this return.

## Evidence layers kept separate

### Measured/accepted physical facts

This packet reuses the accepted SR03 census and accepted SR09-PRE R01 reconnaissance at commit `a9fb5b57e79627a2ecd23973878156778b78a37b` after re-establishing exact source identity from Library bytes. No blind current-turn source-wide cell scan was performed.

Key hostile physical facts retained:

- **R1:** `REFNUMB` injective; `CASENUMB` noninjective; no declared/user/system missing cells; ordinary `SUPDEM` special-looking codes; 12-country raw coordinate; five weight carriers.
- **R5:** 84 variables declare user-missing `997`, all exercise it; 1,342,300 user-missing cells; 4,336 system-missing cells; injective `RESPNO`; distinct routing/filter carriers; exact `WITHINWT`/`COMBINWT`.
- **R9:** Q78F alone declares user-missing `-1` but has zero incidence; 583,491 system-missing cells; injective `RESPNO`; eleven Q118 physical slots; ordinary `9996`; distinct old/new weight carriers.

### Source-native documentary authority newly brought into the packet

**Round 1 — `merged_r1_codebook2.pdf`**

- The codebook explicitly warns that the 12-country merged release comes from nonstandardized national instruments and that merged variables can combine identical, similar, or conceptually equivalent national questions.
- `REFNUMB` is explicitly a unique MSU case reference; the separately named `RESPNUMB` is only unique within a country.
- The R1 `COUNTRY` map is explicit.
- `SUPDEM` meanings and country-specific response/applicability caveats are explicit.
- The roles of `WITHINWT`, `ACROSSWT`, `COMBINWT`, `AFRICAWT`, and `AFCOMBWT` are explicit.

**Round 5 — `merged_r5_codebook_2.pdf`**

- `RESPNO` and its country-prefixed domain are documented.
- Q41D_ARB provides a positive source-native routing control: it is asked only in ALG/EGY/MRC/SUD/TUN and explicitly uses `997=Not asked`.
- R5 sampling technical forms and `WITHINWT`/`COMBINWT` roles are documented.
- The same source document exposes important exact-release gaps: Q10B and Q47C entries omit `997` even though the exact SAV physically declares it; the documented `COUNTRY_ALPHA` coordinate cannot be silently substituted for the exact SAV `COUNTRY` coordinate.

**Round 9 — `AB_R9.MergeCodebook_25Jun24.final_.pdf`**

- `RESPNO` and exact `COUNTRY` are documented as data-manager-assigned carriers.
- Q118 is documented as a spoken-language multiple-response surface; documented slots reach `Q118_10`, use ordinary `9996=No further reply`, and are followed by `Q118OTHER`.
- The Q78 section documents Q78A-E and then proceeds to Q84A; **Q78F is absent at the bounded family boundary**.
- The exact raw source nevertheless contains Q78F and its unexercised `-1` user-missing declaration. That declaration remains physical truth.
- The exact raw source contains `Q118_11`; the codebook documents `Q118_10` and then `Q118OTHER`, so slot-11 semantics remain unresolved.
- The codebook documents old/new within-country weight concepts, but does not directly bind raw `V397_A`/`V399_A` carrier names.

## Documentary authority blockers

### Round 1

No named documentary blocker prevents a source-specific future hostile court if the court stays fail-closed on `CASENUMB`/codebook-`RESPNUMB` equivalence and respects the codebook's national-instrument heterogeneity. Those remain explicit bounded unknowns, not invented semantics.

### Round 5

1. `R5-G01` — exact SAV `COUNTRY` versus documented `COUNTRY_ALPHA` carrier binding.
2. `R5-G02` — Q10B `997` semantics: exact source declares/exercises it, Q10B codebook entry omits it.
3. `R5-G03` — Q47C `997` semantics: exact source declares it while Q47C codebook entry omits it; system missing must remain separate.
4. `R5-G04` — exact administrative filter carrier semantics (`WEST.AFR`, region filters, `R1.ONLY..R4.ONLY`) remain opaque unless exact processing documentation is supplied; this gap is nonblocking if future certification preserves them as raw metadata only.

### Round 9

1. `R9-G01` — Q78F documentary definition absent.
2. `R9-G02` — Q118_11 documentary definition absent.
3. `R9-G03` — Q47C ordinary raw code94 documentary binding absent from the Q47C codebook entry.
4. `R9-G04` — exact `V397_A`/`V399_A` weight carrier-to-role binding absent.
5. `R9-G05` — Q118 slot order has physical authority only; rank/priority semantics remain forbidden absent specific source authority.

## Potential frozen-contract contradiction

`NONE_OBSERVED`

The codebook/source discrepancies above do **not** contradict the frozen SAV decoder or source-native constitution. Those contracts already rank exact source bytes/native metadata above documentation and already require declaration, incidence, semantic status, and physical missingness to remain separate. No decoder-law change is proposed.

## Hostile fixture accounting

- R1: 7
- R5: 9
- R9: 10
- **Total: 26**

Every accepted SR09 hostile burden is represented in `HOSTILE_FIXTURES.csv`; additional fixtures make R5 question-specific `997` routing and R9 eleven-slot topology directly executable.

## Read economy

Current Authority-71 raw work was limited to:

1. Library bundle identity verification;
2. extraction of only the three assigned SAV members;
3. exact source SHA verification before and after packet preparation.

No current-turn source-wide cell scan was performed. Accepted SR03/SR09 counts/sentinels were reused because they already close the physical census burden. Current-turn investigation concentrated on source-native documentary authority.

## Terminal preparation disposition

All three packets are execution-ready in the Authority-71 sense: a future executor knows exactly which bytes/config/fixtures/documentary claims/unknowns/fail-closed conditions apply. R5 and R9 require the named documentary authority before semantic certification; R1 can proceed to a source-specific hostile court under its explicit bounded unknowns.

`PRE553_SOURCE_CERT_PREP71_R01_RETURNED`
