# B01 — Integrated Fracture-Map Independent Admission R2

## Verdict

`FRACTURE_MAP_INDEPENDENT_ADMISSION = NOT_ADMITTED__I08_SELECTIVE_INVALIDATION_FAILURE`

The candidate is **not admitted**. The decisive mandatory-gate failure is I08 AC11: under the frozen controlled `SYN-R035` determinant mutation (`R: 0 -> 1`), the semantic change is correctly localized to the R surface, but exact dependency-addressable identities over-invalidate unrelated topology. The I08 validator therefore returns:

`IRRELEVANT_DETERMINANT_INVALIDATED_UNRELATED_TOPOLOGY`

Unexpectedly invalidated unrelated identities include `ROOT`, the four P branches, `Q_CHILD`, `S_CHILD`, `COSIG`, and `J3`. The R-dependent identity does invalidate as required; the failure is excess invalidation, not failure to notice R.

## Ordered admission record

1. Exact Wave-VIII source recovered and hash-bound: SAV `a5e83a...f998`; questionnaire `d72c3a...c2fb`; codebook `328bbb...4fc`. Pure-Python SAV decoder closes the A01 environment blocker and consumes the entire 12,275,728-byte file.
2. Answer-blind autonomous A/B execution was frozen before I05/I06/I07 expected-answer artifacts were opened. A/B observations are byte-identical (`cbbded...2d98`) and semantic-identical (`0e04f8...d6b8`).
3. I05 hostile semantic parity: PASS.
4. I06 Lebanon real-data parity: PASS, including the 2,339-row substantive universe, 1,334 SES branch, 1,005 non-SES branch, support/stop distinctions, 370-row pattern census (`8a642a...ed9`), and corrected routed Wave-VIII weighted SES share `47.287269199071936%`.
5. I07 source-backed pair/direct-J3 parity: named source witnesses reproduce, including H01/H02/H03 direct raw tensor hashes. Exact Z02 J3 executor/composer blobs are independently hash-verified and expose direct same-respondent J3 rather than pairwise reconstruction. This evidence does not cure the later I08 failure.
6. I08 anti-cheat / replay / determinant-mutation gate: **FAIL (AC11)**.

## Candidate identity

- Z02 tested candidate: `d164f14dd6edd63a30b02639ed93cfb90c51ee92`
- Z02 sealed return: `cf3b376710e61695ab37a24269728152bd58f53e`
- Answer-blind freeze commit: `ef800907a43e01e83357abce97aa5d3fc8eb5b4c`
- Mandated B01 starting HEAD: `ed77f229f9ce3eb910b7a74738fa42c14d25fbb5`

## Fail-closed consequence

MX04 remains held. MX05/C09 remains held. No V3 work or architecture selection is authorized by this return. No success token is issued.
