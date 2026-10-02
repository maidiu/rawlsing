# PYAT HQ166 — AT07 SUCCESSOR SPINE HQ ADOPTION

Decision:
`HQD-2026-10-01-166`

Governing Astra decision:
`a2e7767ecec9ecb6d241861628759f2e933920d5`

Independent oracle freeze:
`92ddee2241a78b46394665d325e5ebf0e75adf40`

Independent review:
`agent/reviewer-pyat-hq165-at07-successor-spine-independent-review-r1 @ 2a454f4cd6359d149269dbbbe5497ea1c263f9c8`

Reviewer disposition:
`APPROVE_AT_DECLARED_GRAIN`

Accepted branch:
`integration/pyat-hq166-at07-successor-spine-accepted-r1`

## Adopted exact successor identities

Forward:
`01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd`

Reverse:
`a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca`

Schema:
`PYAT_AT07_C1_02_SUCCESSOR_IDENTITY_SPINE@1.0.0`

## Currentness law

The R8 spine remains immutable historical accepted C1-01 evidence:

- historical forward:
  `03610f9d91b23cfb6f862dc91b5de92c7f4e4b8e44a53b9efdacb1cf73af6b9e`
- historical reverse:
  `1202822cf98d802c04440328496dc64ee02e6d6030a3da6c9bf10ef1a6490a3c`

Those historical identities are not aliases of the successor and are not current composed-result identity oracles under the adopted C1-02 owner.

For the exact source-free AT07 direct paths under adopted analytical-composition owner blob:

`604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`

the two successor identities above are now the HQ-adopted expected composed-result identities.

## Adopted derivation law

Historical direct field set:
`38`

Current direct field set:
`44`

Removed fields:
`0`

Exactly six direct additions:

1. `discovery_receipt_refs=[]`
2. `discovery_frontier_ref=null`
3. `recursive_handoff_refs=[]`
4. `recursive_lineage_refs=[]`
5. `joint_component_count=1`
6. `joint_order_semantics="SEMANTIC_ORDERED"`

All 38 historical fields remain canonically equal in both directions.

## Independence basis

The oracle producer did not execute production composition/identity projection and did not use the observed join forward hash as expected truth.

The independent reviewer:
- verified all 24 pinned inputs independently;
- reconstructed the 38→44 field law;
- reproduced both historical digests;
- independently derived both successor digests;
- reproduced the undisclosed reverse successor blind;
- reran the oracle procedure under Python 3.12.14 versus producer Python 3.11.3 with byte-identical artifacts;
- confirmed 44/44 hostiles reject with zero false accepts.

Informational reviewer residuals R-1 and R-2 are nonblocking and retained.

## Downstream status

AT17/N10E remains semantically accepted historically, but its current C1-02 identity binding must now be requalified against this adopted successor spine.

The previous C1-03 join run remains historical failed evidence:
`434 passed / 1 failed`.

It is not converted into a PASS by this adoption.

The next authorized action is one substantial AT17/N10E successor requalification plus C1-03 join rerun.

No raw sources.
No owner redesign.
No C1-R.
No Omega-1 until the rerun is independently accepted and HQ-adopted.

Terminal:
`AT07_SUCCESSOR_SPINE_HQ_ADOPTED`
