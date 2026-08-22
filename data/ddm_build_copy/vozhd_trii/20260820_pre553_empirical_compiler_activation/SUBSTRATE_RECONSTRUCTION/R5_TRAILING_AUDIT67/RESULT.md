# Authority 67 V4 Trailing Full-Audit Court

Source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

| checkpoint | ordinary build | ordinary audit | ordinary total | overlap total | overlap speedup | overlap V4 build | builder slowdown | auditor finish lag | queue peak |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 250,000 | 52.336s | 28.950s | 81.286s | 55.412s | 1.466x | 55.434s | 5.92% | 1.275s | 1 |
| 2,000,000 | 380.687s | 215.698s | 596.385s | 389.582s | 1.531x | 389.588s | 2.34% | 1.277s | 1 |

Both checkpoints passed exact equality of root bytes, inventory bytes, member count/order, every member byte/hash/logical digest, logical stream digest, physical root, and ordinary versus trailing full-audit result. The 2M trailing auditor processed 2,000,614 canonical rows at approximately 5,138 rows/sec; ordinary audit was approximately 9,277 rows/sec. Aggregate RSS stayed near 224 MB, and scratch was cleaned.

Disposition: `R5_TRAILING_AUDIT67_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION`
