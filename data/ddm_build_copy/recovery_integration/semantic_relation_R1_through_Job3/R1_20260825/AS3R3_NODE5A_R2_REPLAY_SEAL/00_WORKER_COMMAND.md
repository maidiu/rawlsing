# AS3R3 NODE 5A R2 — CORRECTED CARDINALITY REPLAY / SEAL

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-as3r3-node5a-r2-replay-seal`

Mandated starting HEAD: `16098c57883fde512e933eb1a220ea59b6c526a8`

VERIFY EXACT BRANCH AND HEAD FIRST.

Execute Node 5A R2 only. GitHub-ground all claims. Do not consume MX01R2/MX02R2 findings except Authority34's adopted statements; they are unrelated to this execution.

## Governing authority

Read first:

1. Authority 34:
`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/34_PREV3_WAVE1_R2_AND_AS3R3_CARDINALITY_ADOPTION.md`

2. Node 4A accepted return at exact ref `4d66bc34c256f6bf3f9f707dda80d963881f3510`.

3. Original Node 5A fail-closed return at exact ref `34caf24a79a0b49eae4cd0937e7b13f56bb38c2e`.

4. Identity/cardinality court at exact ref `dc597c5293ec62864617ff77a5e928d5edb36171`.

5. Frozen successor producer at exact ref `cfc240aa3a64c59509eab97450a7d3603af813cc`.

## Binding count law

`19 SOURCE/ROLE ROWS -> 19 ROLE-TO-REF MAPPINGS -> 18 DISTINCT CANONICAL EmpiricalPredicate OBJECTS`

The sole lawful alias class is exactly:

`{A000, A1RAPP}`

with:

`successor_ref(A000) == successor_ref(A1RAPP)`.

This is role aliasing, not role erasure.

FORBIDDEN:

- injecting source IDs into canonical predicate identity;
- injecting candidate role into canonical identity;
- injecting derivation wrappers into canonical identity;
- using old AS3R2 hashes to force inequality;
- changing Node4A mapping;
- changing candidate semantics/terrain;
- changing producer/schema merely to produce 19 unique refs.

## Required execution

Consume the exact 19 frozen Node4A predicate input records without semantic alteration.

1. Validate all 19 under the accepted successor producer predicate validator.
2. Invoke the accepted constructor exactly 19 times.
3. Produce exactly 19 source/role-to-successor-ref mapping rows.
4. Require exactly 18 distinct canonical predicate refs.
5. Require exactly one alias class and that it is exactly `{A000,A1RAPP}`.
6. Serialize/store each distinct canonical predicate representation once, while preserving all 19 role/source mapping/provenance rows.
7. Produce explicit role-key lookup material proving downstream callers can resolve `A000` and `A1RAPP` independently to the shared canonical ref.
8. Fresh-process replay the complete package at least twice and require exact reproduction of:
   - all 19 mapping rows;
   - all 18 canonical predicate identities;
   - the sole alias class;
   - producer/replay hashes and package identity.
9. Correct only bounded Node5A/package/count assertions necessary to encode the adopted 19-role/18-object law. If a planned downstream loader/preflight artifact is emitted here, its correction must be additive and must not mutate accepted historical branches.

## Hard stop

Do NOT:

- freeze Node4B query inputs;
- mint successor queries;
- create DiscoveryAuthority/frontier;
- run LiTS-I/I05/C05R2B;
- alter K/J/depth/82-candidate terrain;
- alter A/B/C fairness law;
- enter V3.

## Required outputs

Write under:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS3R3_NODE5A_R2_REPLAY_SEAL/`

At minimum:

- `RESULT.md`
- `RESULT.json`
- `ROLE_TO_CANONICAL_REF_CROSSWALK.csv`
- `CANONICAL_PREDICATE_MANIFEST.json`
- `ALIAS_CLASS_RECEIPT.json`
- `FRESH_REPLAY_RECEIPT.json`
- `COUNT_LAW_VALIDATION_RECEIPT.json`
- `EXACT_REF_LEDGER.csv`
- `CHANGED_FILES.txt`

If production code is changed, it must be the smallest count/loader correction justified by Authority34 and must be separately identified and tested.

## Success condition

Only return success if all of these are simultaneously true:

- 19/19 frozen inputs validated;
- 19 constructor calls;
- 19 role mapping rows;
- 18 distinct canonical predicate refs;
- sole alias exactly `{A000,A1RAPP}`;
- deterministic fresh-process replay;
- zero query minting.

Success token:

`AS3R3_NODE5A_R2_CORRECTED_CARDINALITY_REPLAY_SEAL_COMPLETE__READY_FOR_NODE4B`
