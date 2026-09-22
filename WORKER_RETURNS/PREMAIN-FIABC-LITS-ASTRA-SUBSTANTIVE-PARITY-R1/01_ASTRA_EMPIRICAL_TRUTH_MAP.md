# ASTRA-D04-R2 Empirical Truth Map

Authority commit: `e631de162c582423639b7067a4f36b29f8aa4d89`.

This map records only the historical empirical substance conserved by the new parity gate. Historical serialization identities remain provenance, not cross-schema equality targets.

## Frontier

- candidates: 50
- logical query roles: 77
- accepted frontier seal: `ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`
- lane accounting: P0 5/5, P1 1/3, P2 18/36, P3 1/8, P4 25/25
- all 77 historical logical roles: `SUPPORTED`
- role result reuse count: 0

## D03

| Root | Count | Accepted root |
|---|---:|---|
| R2 | 24897 | `f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3` |
| R7 | 28325 | `0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844` |
| R27 | 24630 | `f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29` |

Role ownership conserved by normalization:

- P0 / q301_2: R2
- P1 JOINT: R27
- P1 MARGINAL_0 / q301_2: R2
- P1 MARGINAL_1 / q301_7: R7
- P2 CONDITION and BASELINE: R7
- all P3 pooled/stratum roles: R7
- all P4 BASE roles: R27

## P0

| Target | Candidate hash | Denominator | Support |
|---:|---|---:|---:|
| 1 | `2fc1d8b918298b9f1050b76bf16b71e42b8cdd679caa6df1d3bf3a446c2cf594` | 24897 | 4377 |
| 2 | `97f479ddb5a8094e73e8c5bf558f5548f73c8882cb9aea9d011d320a0f67811c` | 24897 | 6440 |
| 3 | `2757ddc2ea169b4dc5dfbd1b18dd92c7af089d2a70b28f5270e9f395d24aa515` | 24897 | 5226 |
| 4 | `98d2cd5db30a03b5760e21527d93404502c6eb642f28223b2df956964dd97381` | 24897 | 6972 |
| 5 | `bb28edd743df0f47c0e5dd0c38b9958de427c493f92d16061c31d54c4d992670` | 24897 | 1882 |

## P1

Candidate:

`38f4e2fcdb85b9e69010671a938c1ecf2269fa7c4f7131046b59ed91cff66d34`

First exact dependence witness, cell [1,1]:

- joint: 1485 / 24630
- marginal q301_2: 4377 / 24897
- marginal q301_7: 2889 / 28325

The normalizer verifies the exact cross-product inequality; it does not merely copy the `SUPPORTED` label.

## P2

Every candidate is keyed by its ASTRA-recorded candidate hash and exact first-difference witness. Baseline witness is always 2889 / 28325 at cell 1.

| Candidate hash | Condition support / denominator |
|---|---:|
| `7439307e410c8219fcfa4f801fd15238ab495c38c3554f649d8ff1f5701a85d6` | 352 / 1191 |
| `865c8ade8df5a9fa1e1e7038fa445a67283d75dedc9cc293380f84489de0aa5d` | 59 / 195 |
| `1dea28e3da527a192340818ac2089d274fcacca5757eb76662b927ae8d59437e` | 39 / 137 |
| `4673e06ede36a292024d0cc9b9988d27e6f54f09d64f92f199763959d961bb5c` | 188 / 584 |
| `7159c60b9e84363a5d977c018eccf1b6b95d30b15e1e5c17f77d01e16b91b490` | 212 / 541 |
| `eb18023a7d65d72c3d8ea27189f81cefdeb626f9da23a3ad1317f8a433e8bde4` | 67 / 210 |
| `5fd907201a19a05ff1a1a58e6b0c58569e0f165217761c6650e3e50ce50e0f83` | 123 / 381 |
| `e6c1017f35e8b497a1ce60f111bbbd7a93628bb64c4c63cf34a347f918c734f8` | 53 / 143 |
| `208b11c86bdac0d7625b6c47b1d4012a62b16916dc7939b7df2f69af58af50c0` | 387 / 931 |
| `4604bdf49761748868ffdc84883dce2498c59428e49a9a091a8ef8892f4b9f53` | 16 / 906 |
| `1d73562e6cbf48eb1e3f0a1b6093acac0b81b72ae9a3e1c306f5ad02dd4f157c` | 1 / 66 |
| `d516fed1dbbdb758ebb4cb88892a092ac9e2e184cde96a032198cdcb4ae870c5` | 5 / 41 |
| `c19906d0949529ce14339910b2190e34eb1e97344eab4b856e5886c89ee81e0e` | 10 / 222 |
| `e31fa2bef3f1b339504f750aea8f807ddc9de6dbdb0021323c9b6812f105e788` | 10 / 115 |
| `3de3ce793e5f95e3c8e1d42c08156e9cdbcd3d3e61b24a9957f448425ba77042` | 4 / 47 |
| `2528ee7ae06643d28a05c16a233cbcab1ac4e8470c18fd81fdf571c3021c76bd` | 6 / 170 |
| `867fe555397d9014032abfbf47e7a5c92e0bebcdef31b071767d4d5b0b38aaec` | 0 / 38 |
| `a0b28932f8a6246d6ac88f099e9657d10cb35a2528fb72781469f9055098993d` | 13 / 247 |

The current side independently recomputes the first differing cell from complete current fact projections. Candidate-hash/witness association is exact; permutations fail.

## P3

Candidate:

`82a1ff4b9f5d6521d2d9fe1310680e20d9457c083e0eb16d6b016a7f08931771`

Target cell: 5.

Exact rates:

- POOLED_NEG = 206/4327
- POOLED_POS = 595/1854
- Q310V1_NEG = 81/1523
- Q310V1_POS = 366/1013
- Q310V2_NEG = 50/1337
- Q310V2_POS = 29/96
- Q310V3_NEG = 5/97
- Q310V3_POS = 16/65

Pooled sign = +1. Stratum signs = [+1,+1,+1].

Therefore the frozen conditional-reversal predicate is false: the strata do not reverse the pooled sign. Historical terminal is `EVALUATED_VALID_EMPTY`.

The current normalizer additionally requires every one of the eight role facts to be `SUPPORTED` with a positive denominator before it is allowed to call this the accepted valid-empty mechanism.

## P4

Exact 5×5 located support matrix:

| q301_2 \ q301_7 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|
| 1 | 1485 | 976 | 873 | 787 | 206 |
| 2 | 555 | 2139 | 1543 | 1910 | 229 |
| 3 | 305 | 1029 | 1647 | 1841 | 347 |
| 4 | 232 | 1103 | 1439 | 3458 | 672 |
| 5 | 65 | 201 | 274 | 719 | 595 |

The cell coordinate is part of parity truth. The normalizer sorts by coordinate, never by count, so a count permutation fails.

## Final envelope

- `EVALUATED_SUPPORTED = 49`
- `EVALUATED_VALID_EMPTY = 1`
