# G1-G5 matrix — SOROK #1037 B05 R3 independent G5

**Engineering verdict:** `ACCEPT_SCOPED_SOURCEFREE`
**Accepted code:** `cab1f2d6cdab6f6b653ed20e5b41afb90d9facbc`
**Reviewer:** `ses_e21caf5dfffeSywXGrQ6qw65oe`
**Scientific:** `HELD` · **Authority:** `HELD`

| Gate | Status | Evidence | Limits |
|---|---|---|---|
| G1 source/owner/custody | PASS_SCOPED_SOURCEFREE | exact candidate/base; only B05 read-side changed; B04 unchanged; no writer/ledger/schema/store/lock; exact probes byte-identical; product read-only | fully privileged checkpoint fabrication outside public threat model |
| G2 build/first consumers | PASS | zero 17/17; positive 34/34; #1027 63/63 with both defects false; cold ok; 4+5+6+3+43 tests; genuine zero/held/positive/historical | no full P6/MII/J1; timings under load |
| G3 falsification | PASS | own malformed ADMITTED no-decrease/wrong-debit -> B05_RENT_RECEIPT_INVALID; no-transition -> B05_RENT_OPERATION_UNPROVEN; same-period replay -> B05_RENT_OPERATION_NOT_UNIQUE; original positive and zero forgeries refused | no new in-scope false ADMITTED found |
| G4 boundaries/preservation | PASS_WITH_LIMITS | historical h1 true/h2 false; replay/retry; changed/severed/restored; B04; cold; no new ledger/psychology/native/protected | UNCHANGED/REFUSED no-debit statuses by design; provider/cost UNOBSERVED |
| G5 independent receiving | ACCEPT_SCOPED_SOURCEFREE | exact source `cab1f2d6`; frozen zero probe green, positive/#1027/cold/all suites pass, own negative witness 12/12 | no protected merge, no native/science/human/J1 acceptance |

## Exact RED -> GREEN

- Base RED (immutable R2 report at `6dc9218`, copied to `evidence/immutable_r2_red_report.json`): 17 checks, 16 pass, zero forged ADMITTED rent `READ`, cash 55.
- Final R3 GREEN: same unchanged probe blob `d5d41240...` -> 17/17, zero forgery refused `B05_RENT_RECEIPT_INVALID`.
- No product mutation was used to re-run the base; the immutable report and author R3 RED report are preserved.

## Own negative witness (not the author test)

`g5_r3_independent_probe.py` — 12/12:

- malformed ADMITTED no decrease -> `B05_RENT_RECEIPT_INVALID`
- malformed ADMITTED wrong debit -> `B05_RENT_RECEIPT_INVALID`
- well-formed ADMITTED no actual checkpoint transition -> `B05_RENT_OPERATION_UNPROVEN`
- genuine zero `UNCHANGED` -> READ
- genuine held `REFUSED` -> READ
- genuine positive `ADMITTED` -> READ, h1 historical true / h2 false
- same-period copied receipt -> `B05_RENT_OPERATION_NOT_UNIQUE`, genuine fail-closed, no second debit

## Nonclaims

No native science, human/actor authority, J1/Nadia G2 acceptance, motive/volition inference, protected PRE-MAIN merge, new ledger, R4, or isolated cost/performance claim. Provider and checkpoint/org/quota `UNOBSERVED`.
