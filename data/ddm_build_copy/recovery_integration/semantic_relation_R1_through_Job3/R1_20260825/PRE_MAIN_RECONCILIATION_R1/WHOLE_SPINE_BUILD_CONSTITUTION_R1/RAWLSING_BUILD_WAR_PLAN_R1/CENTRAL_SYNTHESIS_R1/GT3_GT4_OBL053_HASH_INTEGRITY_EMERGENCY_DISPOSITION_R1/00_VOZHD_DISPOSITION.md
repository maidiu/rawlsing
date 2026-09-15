# GT3/GT4 OBL053 HASH-INTEGRITY EMERGENCY DISPOSITION R1

## Terminal

`RETURN_REQUIRED__GT34_OBL053_T1_HASH_RECOMPUTATION_FALSE__HQ_ADOPTION_ROOT_NOT_COMPETENT_FOR_DOWNSTREAM_AUTHENTICATION`

## Exact boundary

- repository: `maidiu/rawlsing`
- canonical state inspected: `a721677d57efc702ed0479a5dd814ce75e2fb3e5`
- S1 candidate artifact blob: `59c88df41b90f3ca932f52326fe4b275e84c4551`
- T1 hostile-audit evidence blob: `4cff92f4f6b8625a94eee7c8aa69dc3566026490`
- OBL053 HQ adoption artifact blob: `286ff7b851e920ff2760082d8b2fb194560ab127`
- independent recomputation evidence: `01_INDEPENDENT_RECOMPUTATION.json`

No historical artifact is rewritten or deleted.

## Finding

T1's exact hash-audit claim is mechanically false under the content-addressing law stated by S1 and repeated by T1:

`SHA256(UTF8(CANONICAL_JSON(EXACT_SEMANTIC_PROJECTION)))`

with lexicographically sorted mapping keys, compact comma/colon separators, Unicode preserved, and ordered sequences preserved.

Independent recomputation from the exact persisted S1 artifact gives:

| node | declared | recomputed from persisted projection | result |
| --- | --- | --- | --- |
| generation seed | `b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53` | same | MATCH |
| authority | `e024220dfd21bd2544f86dd9ceec332b42115ff55afdc94183811d2ed52924ed` | `867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29` | MISMATCH |
| semantic object | `d9647033de698e38e16001984580e1e0af3ba30c362acf3258aef3b78070cb53` | `d937f666dca0ba000939982a1fcc5ea1f55d1e0683b6a02cd21545c79e3c66c6` | MISMATCH |
| objective evidence receipt | `1561942f1fe4fc43b248c61be866c0bc459773b7c6dbb8e393e13b064cdacce0` | `06f81a64ea4e25e1aebe16cc04d1d07d8562889a1bd135077fae7c4b9ef6e80e` | MISMATCH |

The latter two recomputations are **diagnostic values of the stale persisted projections**, not final repaired identities. A lawful repair must first correct the upstream authority identity embedded downstream and then recursively recompute object and receipt identity.

## Disposition

The semantic reading T1 defended is not rejected here. The defect is narrower and prior to downstream materialization: the adopted content-addressed identity graph does not authenticate the exact persisted semantic projections it claims to authenticate.

Therefore:

- T1's `PASS` is preserved as historical audit evidence but is **superseded at the exact hash-recomputation finding**.
- The HQ adoption blob `286ff7...` remains immutable historical evidence but is **not a competent current trust anchor for OBL054 authentication**.
- OBL053 returns to `RETURN_REQUIRED` at the content-addressed identity-integrity grain.
- OBL054/U1 is suspended. It must not bind S2 to the invalid OBL053 root.
- OBL052 is blocked on repaired/re-hostile-reviewed/re-adopted OBL053 plus OBL054.
- OBL055 remains downstream of OBL054.
- positive V3 remains forbidden.

This does not authorize a different semantic object, a second seed/object, a classifier, encounter, comparator, PSEPF, metabolism, CAN-008, V2, or positive V3.

## Smallest repair

Repair only the OBL053 content-addressed identity graph.

The repair must:

1. preserve the exact admitted generation-seed semantic projection if its hash continues to recompute exactly;
2. recompute the authority from its exact persisted semantic projection rather than copying the old declared hash;
3. rewrite every downstream embedded upstream identity to the corrected authority identity;
4. only then recompute the semantic-object identity;
5. rewrite every receipt embedding of corrected authority/object identities;
6. only then recompute the objective-evidence receipt identity;
7. mechanically prove all four hashes in executable tests;
8. hostile-review the repaired graph independently;
9. require a fresh explicit HQ adoption before OBL053 again becomes current.

No cosmetic compatibility with `e024...`, `d964...`, or `1561...` is required or permitted if those identities do not authenticate the repaired graph.

## Branch consequence

The already-created U1 branch remains untouched at its pre-repair base. It is not deleted or repurposed. A new OBL053 hash-integrity repair wave must precede any U1 restart.

`main` remains untouched.
