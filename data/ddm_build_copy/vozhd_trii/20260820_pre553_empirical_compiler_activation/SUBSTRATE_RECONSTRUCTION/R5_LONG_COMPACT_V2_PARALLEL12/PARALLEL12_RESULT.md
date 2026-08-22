# R5 Compact V2 Parallel-12 Court

Authority: 65
Starting HEAD: 11877f5a043418100773b8a476ee425ec63305cd
Source SHA-256: 2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d

## Result

Both exact WVS courts passed canonical equivalence and full audit. The parallel path is correct but has no practical gain and is not selected under Authority 65.

Disposition: `R5_PARALLEL12_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT`

| checkpoint | serial build s | parallel build s | speedup | peak RSS | scratch peak | members | logical digest | physical root |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 250,000 | 43.705169410 | 51.167557966 | 0.854157813 | 244,379,648 | 209,736,201 | 16 | a76aae65d6e0d767e53c5a9e651a38372d5569888daed38aa2d5f442426a2ed9 | 8770a469068c7ba8f0b50d66f99a2a64a46528611d276a54e6d0e51a957fe1a5 |
| 2,000,000 | 418.360303339 | 473.099067598 | 0.884297459 | 245,084,160 | 1,647,333,731 | 123 | fa6249de1b0ae8ce34c5612e7d06eb10947ae967cdcd94e4e0016bf69ab8b189 | 6e8b6c942ca563b74a8313a93a995db2666ec220f4b114d1d8a375012969ebb0 |

The 2M audit reported 2,000,614 canonical rows, 2,000,000 source physical cells, 613 source variables, and one source metadata relation for both paths. Root bytes, inventory bytes, member order/count, every member byte length/hash/logical digest/coverage descriptor, and full-audit results were equal.

The implementation used exactly 12 worker processes, one decoder/coordinator, queue capacity 12, zero persistent cache, and zero worker failures. Scratch was cleaned after each court.

