# GT3/GT4 OBL053 HASH-GRAPH INTEGRITY REPAIR WAVE R1

Repository: `maidiu/rawlsing`

Commissioning authority: VOZHD / grounded corrective project decision.

Canonical commissioning basis before this instruction commit:

`fdf770734a3a190d8441d67680eb1759c4398663`

Controlling corrective disposition:

`../GT3_GT4_OBL053_HASH_INTEGRITY_EMERGENCY_DISPOSITION_R1/00_VOZHD_DISPOSITION.md`

Historical S1 candidate blob:

`59c88df41b90f3ca932f52326fe4b275e84c4551`

Historical T1 audit evidence blob:

`4cff92f4f6b8625a94eee7c8aa69dc3566026490`

Historical HQ adoption blob:

`286ff7b851e920ff2760082d8b2fb194560ab127`

## Current project state

- OBL053 = `RETURN_REQUIRED` at content-addressed identity-integrity grain.
- The S1 constitutive semantic reading is preserved; this wave does not reopen its semantic jurisdiction.
- The exact frozen seed projection/hash survives independent recomputation.
- T1's authority/object/receipt exact-hash PASS is superseded by contradictory mechanical evidence.
- Historical HQ adoption is preserved but is not a competent current downstream authentication root.
- OBL054/U1 is suspended on corrected OBL053 adoption.
- OBL052 is blocked on OBL053 + OBL054.
- OBL055 remains downstream of OBL054.
- positive V3 remains forbidden.

## Independent diagnostic recomputation

From the exact historical candidate projection:

- seed declared/recomputed: `b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53` = MATCH
- authority declared `e024220d...`; recomputed exact projection: `867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29`
- stale semantic-object projection as persisted hashes to `d937f666...`, not declared `d9647033...`
- stale receipt projection as persisted hashes to `06f81a64...`, not declared `1561942f...`

The stale downstream diagnostic values are NOT repaired identities because the downstream projections themselves embed the invalid upstream identities.

An independent recursive correction predicts, subject to worker verification:

- corrected authority hash: `867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29`
- corrected semantic-object hash after replacing all embedded old authority-hash occurrences: `9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- corrected semantic-object ID: `urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- corrected objective-evidence-receipt hash after binding corrected authority + object identities: `153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c`

These are verification targets, not authority. If executable recomputation disagrees, fail closed and report the exact divergence.

---

# WORKER V1 — OBL053 CONTENT-ADDRESSED HASH-GRAPH INTEGRITY REPAIR R1

Profile:

`BOUNDED_IDENTITY_REPAIR_AND_MECHANICAL_HASH_COURT`

## Mission

Repair only the false content-addressed identity graph in the S1 one-object authority package.

Do not redesign the semantic authority.

Do not change the five objective entity facts.

Do not add a seed, object, classifier, encounter, actor, comparator, PSEPF, metabolism, CAN-008, V2, or positive-V3 authority.

Do not edit or erase the historical S1/T1/HQ artifacts.

## Required repair architecture

### A. Preserve the exact seed

Mechanically recompute the exact persisted generation-seed semantic projection under the declared canonical-JSON law.

The expected hash is:

`b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53`

If it does not recompute exactly in executable code, STOP and return FAIL.

### B. Correct the authority identity from the exact authority semantic projection

The historical authority semantic projection itself must remain byte-for-semantics equivalent at the JSON data-model level.

Do not mutate it merely to recover the old `e024...` hash.

Compute its content hash mechanically.

The expected corrected hash is:

`867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29`

The authority ID and semantic version remain the historical bounded semantic identity unless a mechanical reason proves that impossible. This is a correction of a false declared hash, not permission for semantic widening.

### C. Rebuild the semantic-object projection recursively

The semantic-object projection embeds authority identity in more than one location.

Replace every exact embedded historical authority hash that represents the semantic owner with the corrected authority hash.

Do not alter objective facts, seed identity, semantic ceiling, object slot, schema, or other semantics.

Then compute the semantic-object hash from that corrected projection.

Expected corrected object hash:

`9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`

Expected corrected object ID:

`urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`

### D. Rebuild the objective-evidence receipt recursively

Replace the historical embedded authority hash with the corrected authority hash.

Replace the historical semantic-object hash and object ID with the corrected semantic-object identity.

Do not change the receipt's epistemic ceiling: it remains provenance/integrity evidence of generated facts, not independent empirical corroboration.

Then compute the receipt hash.

Expected corrected receipt hash:

`153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c`

### E. Persist a repaired candidate, not a rewritten history

Create a new repaired candidate artifact under this wave.

It must record:

- source historical candidate blob;
- exact preserved seed projection/hash;
- exact corrected authority projection/hash;
- exact corrected semantic-object projection/hash/ID;
- exact corrected receipt projection/hash;
- explicit old -> corrected identity mapping;
- exact semantic no-change proof;
- historical T1/HQ records as superseded-at-hash-integrity-grain only.

Do not edit historical S1, T1, or HQ adoption artifacts.

### F. Executable mechanical proof

Create an executable test surface that:

1. loads the repaired candidate artifact;
2. independently canonicalizes each semantic projection;
3. recomputes seed, authority, object, and receipt hashes;
4. proves all declared repaired hashes exactly;
5. proves downstream object projection binds the corrected authority hash everywhere required;
6. proves receipt binds corrected authority + object identity;
7. proves the five objective facts are exactly unchanged from the historical candidate;
8. proves seed semantic projection is exactly unchanged;
9. proves no second seed/object exists;
10. proves no classifier/actor/encounter/comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 semantics were added.

The court must fail if any repaired declared hash is merely copied without matching its exact semantic projection.

## Historical audit disposition

Do not edit T1's evidence to make it look like it passed.

The repaired return must say plainly:

`T1_HASH_RECOMPUTATION_FINDING_SUPERSEDED_BY_MECHANICAL_REPAIR_EVIDENCE`

This does not convert T1's semantic analysis into a FAIL. It invalidates only its exact hash-recomputation assertion and the downstream currentness that depended on that assertion.

## Adoption boundary

V1 may produce a repaired OBL053 candidate and mechanical evidence only.

V1 does NOT re-adopt OBL053.

After V1 PASS:

1. independent hostile review of the repaired graph;
2. only on hostile PASS may VOZHD issue a fresh OBL053 HQ adoption;
3. only after that adoption may OBL054/U1 resume.

## Required return

Path:

`.../GT3_GT4_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_WAVE_R1/V1_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_R1/00_RETURN.md`

Preferred terminal:

`PASS__GT34_V1_OBL053_CONTENT_ADDRESSED_HASH_GRAPH_REPAIRED__NO_ADOPTION`

A PASS means only that a corrected candidate graph exists and is ready for independent hostile review.

## Forbidden

Do not:

- move `main`;
- move PRE-MAIN;
- touch the suspended U1 branch;
- preserve invalid old hashes for compatibility;
- reinterpret the five objective facts;
- emit a V3 subject_ref;
- close OBL052;
- repair OBL054 or OBL055;
- define OBL048;
- create encounter/comparator/PSEPF/metabolism/CAN-008/V2/positive-V3 authority.
