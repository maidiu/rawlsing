# PSC03-A01 — AFROBAROMETER / ARAB BAROMETER BOUNDED DOCUMENTARY ADJUDICATION R1 — RETURN

Status: `PASS__PREV3_PSC03_AFRO_ARAB_RETURNED_CANDIDATE_ADJUDICATION_R1_COMPLETE`

Worker ID: `PSC03-A01`

Branch: `agent/rabochii-prev3-psc-w2-a01-afro-arab-documentary-adjudication-r1`

Commission tip: `5019473c181cc7a69f95378b9602be36cefe3904`

Commission base / HQ authority: `2e5e142700b87cc87934c337ef6d5b8ffcf3cfb7`

Accepted predecessor: L01 return `f50eb270ccba8ceca4fb07240e94c42dae1e1624`

Exact grain:

`PREV3_PSC03_AFRO_ARAB_RETURNED_CANDIDATE_ADJUDICATION_R1_ONLY`

## Result

All three and only the three commissioned items received one allowed exact disposition. No positive routing predicate, structural role, cross-source equivalence, learned product, mechanism body, topology, or person state was minted.

1. `J01A-R2-D-GAP-005` / Arab Barometer V / `Q851D`:
   `ADJUDICATED_SOURCE_CONFLICT__REMAINS_BLOCKED_PENDING_CORRECTION`.

   Exact source basis: the native Wave V questionnaire prints `COUNTRY != 9 OR 16` as the programmer scope across the Q851 block and prints Q851d as `COUNTRY != 9 OR 16 AND Q851a == 1 & Q851b == 1`. The source does not state how the bare `16` is to be interpreted as a Boolean comparison, and no source-issued correction/programming specification is present in the exact allowed evidence ceiling. The intended country predicate is therefore not repairable by inference.

2. `J01A-R2-D-GAP-006` / Arab Barometer VIII / `Q516B`:
   `ADJUDICATED_SOURCE_CONFLICT__REMAINS_BLOCKED_PENDING_CORRECTION`.

   Exact source basis: the native Wave VIII questionnaire labels the Q516B parent `[PROGRAMMER: SPLIT B]` while every one of its four printed member lines is labeled `SPLIT A`. No source-issued corrected instrument/programming specification is present in the exact allowed evidence ceiling. The split assignment remains blocked rather than guessed.

3. `J01A-R2-D-GAP-007` / Arab Barometer V↔VIII / `Q104B_TUN`:
   `ADJUDICATED_NEGATIVE_EQUIVALENCE_OR_NONCONTINUITY__EXACT_BASIS`.

   Exact source basis: in Wave V, Q104b is the multi-select question asking which country the respondent is thinking of emigrating to, with `Tunisia` printed as response option 12. The current wording-review row binds the Wave V `Q104B_TUN` implementation to the meaning `migration: destination country: tunisia`. In Wave VIII, `Q104B_TUN` is instead a Tunisia-gated yes/no question, `[PROGRAMMER: COUNTRY==21, IF Q104==1] And are you preparing to emigrate?`. The identical source code therefore does not preserve the same proposition/response role across V and VIII.

   This ruling is only a governed negative continuity ruling. It does **not** resolve the distinct Wave V destination-set carrier binding, which remains outside this adjudication proposition.

## Current-authority reconciliation

The commission base carries the L01 docket as two documentary conflicts plus one negative/nonapplicability candidate and explicitly states that documentary candidates are not automatically promoted. No same-grain current authority at the commission base resolves these three items. Therefore none qualifies for `CURRENT_AUTHORITY_ALREADY_RESOLVES`.

## Exact evidence ceiling consumed

Only the four Library objects authorized by the commission were used:

- `file_00000000f194722fa72b5189c011664d` — Arab Barometer V questionnaire;
- `file_00000000682c722f9ea8eb2e8830e790` — Arab Barometer VIII questionnaire;
- `file_000000004c4c822fa8519e7f333cfaf5` — wording revision review queue;
- `file_00000000eeac822f90e2a464b92acdf1` — current unresolved-row carrier.

No Library search-order authority and no family rediscovery were used.

## Return artifacts

- `00_RETURN.md`
- `01_THREE_ROW_ADJUDICATION_LEDGER.json`
- `02_EVIDENCE_CURRENT_AUTHORITY_MANIFEST.json`
- `03_VALIDATION_RECEIPT.json`

HQ owns final adoption.

Terminal:

`PASS__PREV3_PSC03_AFRO_ARAB_RETURNED_CANDIDATE_ADJUDICATION_R1_COMPLETE`
