# FFP016 — POSITION / DISPOSITION ANCESTRY DISJOINTNESS RECEIPT R1

Receipt state:

`POSITION_DISPOSITION_ANCESTRY_DISJOINTNESS_RECEIPT = ISSUED__EXACT_SOURCE_AND_QIMPL_IDENTITIES_DISJOINT`

Authority: `FFC002 / PRA_BOUNDED_POSITION_ROLE_COURT / EXISTING_VOZHD_HQ_SEMANTIC_ARCHITECTURE_AUTHORITY`.

Claim/scope:

`FFR2_R5_Q03_Q73A_CONDITIONAL_DISPOSITION_REDISTRIBUTION_CANARY@1`

`Afrobarometer / R5 / COUNTRY_ALPHA3 NOT IN {ALG,BDI,BEN,CAM,CDI,EGY,GHA,GUI,LIB,MAD,MLI,MRC,NGR,NIG,SEN,SRL,SUD,SWZ,TAN,TOG,TUN,ZAM,ZIM} / FFP014_R5_CURRENT_RESPONDENT_CARRIER@1 / governed respondent key (COUNTRY, RESPNO)`

## Active-position ancestry set

| source variable | qimpl | exact identity SHA-256 | source block |
|---|---|---|---|
| Q70B | `question_impl.phase0.311d905b2baab867642e` | `311d905b2baab867642e2be9ed3595aa3c556d9d4508db7510f648e96fb9a8fd` | Q70 |
| Q70C | `question_impl.phase0.575fb5e032fab4cd18a4` | `575fb5e032fab4cd18a4a5bc3f55f233530a243cfa5ff7ecc75740b286b812e8` | Q70 |
| Q73A | `question_impl.phase0.cae005624221d7b00dd2` | `cae005624221d7b00dd2e8dcc31a8c73d2d4f1446a06d428ab40f1ee2809ad14` | Q73 |
| Q84 | `question_impl.phase0.5a05ce882452ef85debd` | `5a05ce882452ef85debd9e7031211b1cd884f8b8c063b5080cfd87c40fa8fcb2` | Q84 |

## Active-disposition ancestry set

| source variable | qimpl | exact identity SHA-256 | source block/battery |
|---|---|---|---|
| Q76A | `question_impl.phase0.6a1a2eb3ed5d31e7e0cf` | `6a1a2eb3ed5d31e7e0cfa8a72aac3116431b1877f3822b0a29fbae1e2967906c` | Q76 |
| Q76B | `question_impl.phase0.2d7f53868dd52feea700` | `2d7f53868dd52feea7006e07f493638e525ca7bc5d05d4f9527f102f6299d96b` | Q76 |
| Q86A | `question_impl.phase0.67f036c0efb7fb98ff4a` | `67f036c0efb7fb98ff4a93dc811bf59cfc095608eda374f6534b006a62241bd3` | Q86 |
| Q86B | `question_impl.phase0.2fb3a62609dad4c1306d` | `2fb3a62609dad4c1306d8cfa14f997eab4d6e65ada56083279386a202544a506` | Q86 |
| Q86C | `question_impl.phase0.5e173e45a10de7c832fd` | `5e173e45a10de7c832fd4c78479025f77fb2a4891f705ced3a7833e308c58957` | Q86 |
| Q86D | `question_impl.phase0.b2b6525f8699525e60ea` | `b2b6525f8699525e60ea981cb9a72259af8c0aa9afb8d36c49989e6f7645f440` | Q86 |
| Q86E | `question_impl.phase0.2aef51cfcb3d44e4870a` | `2aef51cfcb3d44e4870afb497cc5a53dbe8d72cc9f2d803d7a8b27813535766c` | Q86 |
| Q86F | `question_impl.phase0.0bdb38e7f76aadd487da` | `0bdb38e7f76aadd487da6606335b8b3add3764c5ef227a0bf1ef3f1ce4f92910` | Q86 |

## Exact disjointness proof

- source-variable intersection: `EMPTY`;
- qimpl intersection: `EMPTY`;
- exact identity SHA-256 intersection: `EMPTY`;
- active-position source blocks: `{Q70,Q73,Q84}`;
- active-disposition source blocks/batteries: `{Q76,Q86}`;
- block intersection: `EMPTY`.

Thus the active-position operands and active-disposition operands are distinct measurement identities at both source-variable and exact qimpl ancestry grains.

FFX002-R2's hard invalidation condition `active position/disposition ancestry overlaps` is not triggered by this exact docket.

Supplementary Q93C is not an active-position operand and is not part of the active-position/disposition overlap test. It is independently identified as `question_impl.phase0.f62bceafa49dd85eb525` / `f62bceafa49dd85eb5254b102b368044c435bae6d9b3efae8061f0a2977ddbb6` and remains `SUPPLEMENTARY` only.

## Ceiling

This receipt proves only ancestry disjointness for the exact admitted source/qimpl identities above. It does not prove realized exposure/coexposure, empirical independence, statistical independence, causal independence, or semantic nonrelation. Any later derived operand that aliases, merges, transports, or combines ancestry across this boundary requires a new explicit ancestry review.
