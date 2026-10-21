# UR-B frozen TEST_ONLY oracle

Frozen before any target decode or execution. Generated `.sav`/`.dta` bytes only. These are synthetic mathematics and semantics, not original source authority. At most 32 operations per instrument and 96 total.

## S1 — SAV rectangular XOR/weights/all-missing/unadministered

16 rows `i=0..15`. `A=i mod 2`, `B=floor(i/2) mod 2`, `Y=A XOR B`, `G=floor(i/4) mod 2`, `WEIGHT=1+floor(i/8)`. `Z` is administered and all system-missing. `U` is explicitly unadministered and is not a physical variable or projection question.

| Cell | Rows |
|---|---|
| A=0 / A=1 | 8 / 8 |
| B=0 / B=1 | 8 / 8 |
| Y=0 / Y=1 | 8 / 8 |
| G=0 / G=1 | 8 / 8 |
| weight sum | 24 |
| weighted A, B, Y marginals | 12 / 12 each |
| A=1 → Y | 4 / 4 |
| B=1 → Y | 4 / 4 |
| (A,B) → Y | 8 joint cells, 2 each; Y identifies XOR |
| Z | all missing; typed no-support, not a substantive zero |
| U | excluded; no operation |

Admitted operations (10): DIST A raw; DIST B raw; DIST Y raw; DIST A weighted; DIST B weighted; DIST Y weighted; COND Y|A=1 raw; COND Y|B=1 raw; JOINT (A,B,Y) raw; ZERO-SUPPORT Z raw.

## S2 — DTA 8 households × 2 persons

Persons `p=0,1`, households `h=0..7`, `OUTCOME=(h+p) mod 3`, `HMEAS=h mod 2`, person weight `h+1`. `PITEM` is administered only to `p=1`; `PITEM_B` is a second form with the same display label and a distinct occurrence identity, also only `p=1`. Household universe is separate.

Person weighted OUTCOME counts: `0=21`, `1=27`, `2=24`; weighted denominator `72`. Person `PITEM` for p=1 weighted: `0=9`, `1=12`, `2=15`; `PITEM_B`: `0=15`, `1=9`, `2=12`; denominator `36`. Household `HMEAS` unweighted: `0=4`, `1=4`.

Admitted operations (12): OUTCOME weighted distribution; PITEM weighted distribution; PITEM_B weighted distribution; HMEAS household distribution; person OUTCOME by p; person OUTCOME by h-odd/h-even; PITEM eligibility contrast p=0 missing vs p=1 observed; form contrast PITEM vs PITEM_B; repeated display-label occurrence preservation; wrong-unit household→person query refused; same-name collapse refused; second occurrence distinct identity preserved.

## S3 — SAV 12 persons × 2 occasions

Persons `r=0..11`, occasions `t=0,1`. `SCORE=(r+t) mod 3`; `MR1=r mod 2`; `MR2=floor(r/2) mod 2`; `RANK` is ordered; `FORM=r mod 2`. MR1 and RANK1 are administered only at t=0; MR2 and RANK2 only at t=1. Repeated person/occasion keys and option topology must remain distinct; no flattening into 24 independent respondents.

Expected: repeated SCORE 24 rows, each of 0/1/2 appears 8 times; each occasion has 4 of each score; MR1 t=0 6/6; MR2 t=1 6/6; RANK t=0 and t=1 each 4/4/4; FORM 6/6.

Admitted operations (8): repeated SCORE distribution; per-occasion SCORE; MR1 t0; MR2 t1; RANK t0; RANK t1; FORM; wrong flatten-to-24-respondents refused.

## Bound

Total admitted operations = 30 (10+12+8), within 96. Deliberate omissions: U never eligible; S2 p=0 PITEM missing; S3 MR/rank off-occasion missing. No original respondent bytes, no original U/E_pre issuance, no synthetic scientific authority.
