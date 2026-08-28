# I07 — REAL-DATA CO-SIGNATURE / J=3 ACCEPTANCE CONTRACT R1

Status: `SOURCE_BACKED_ACCEPTANCE_CONTRACT_FROZEN__PRODUCTION_TARGET_NOT_YET_AVAILABLE`

This contract is an independent harness specification for the Authority-37 branch co-signature implementation. It is not production code and does not repair or extend I03/I05/controller semantics.

## 1. Governing law

Authority 37, blob `48c0860ff2d7548ff2fa98d20021149aa2049953`, binds:

`PAIRWISE_ASSOCIATION != BRANCH_CONDITIONED_HIGHER_ORDER_COSIGNATURE_TOPOLOGY`

and authorizes `maximum_target_arity_J = 3` for this acceptance workload. J=3 must be direct same-respondent joint execution. Exact J=2 projections may be retained, but they may not manufacture or substitute for the J=3 joint.

Accepted real-data witness authority is L03 commit `74834f5028cae0cdd3c525483494437f81c721e0`.

## 2. Exact source gate

The harness must first resolve the exact Library source bytes and fail closed on any mismatch:

| source | Library file ID | size | SHA-256 |
|---|---|---:|---|
| `ArabBarometer_WaveVIII_English_v3.sav` | `file_00000000e4a8722f9131ea801a527554` | 12,275,728 | `a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998` |
| `Arab Barometer Wave 8 codebook.csv` | `file_00000000102c71fbbd6a569011ead989` | 677,029 | `328bbbbfa6cb8a78eacad52847b1432a56a81ec9ecfcd4f18754e05532afd4fc` |
| Wave-VIII English questionnaire | `file_00000000682c722f9ea8eb2e8830e790` | 1,395,546 | `d72c3afc4529703376dc1133a3d984541c2ceebd1af6cb03a1562f6ce104c2fb` |

The current Library materialization reproduced all three accepted hashes.

The SAV source must replay the accepted geometry: layout `2`; case size `692`; compression `1`; `15,627` declared and decoded cases; bias `100.0`; data offset `176,848`; `688` retained numeric variables; final decoder byte `12,275,728`.

## 3. Anti-leakage seed contract

The implementation under test MAY receive only ordinary governed capability:

1. the complete governed Q873 multi-select response surface and its ordinary component semantics;
2. exact Lebanon Wave-VIII source/release/universe/risk/routing/measure authority;
3. the bounded individual substantive-target catalog specified below;
4. ordinary coordinate authority, with demographic variables explicitly typed as conditioners/predictors rather than response nodes;
5. Authority-37 controller/J<=3 policy identity.

The seed MUST NOT contain:

- a flag that Q873 option 1 is the branch the oracle cares about;
- the Q873_1 branch respondent list or respondent-ID digest;
- any of the five known L03 pair combinations as a precomposed winning/priority candidate list;
- any of the three known L03 triples as a precomposed winning/priority candidate list;
- expected Cramér's V, G², joint-TV, cell residuals, raw/weighted tensor hashes, or oracle rankings;
- any result-dependent pruning hint derived from this harness.

Known witness variables may occur **individually** in the ordinary authorized target catalog. That is not answer leakage. Leakage occurs when the oracle-known combinations or expected outcomes are precomposed, ranked, privileged, or otherwise handed to the implementation.

The harness/oracle may know the expected answer. The implementation may not receive it.

## 4. Bounded substantive target catalog

For this parity harness, the authority-bounded individual response-target catalog is:

`Q201A_1, Q201A_3, Q511, Q512, Q533_4, Q601_3, Q601_4, Q605, Q606_2, Q606_4, Q606_8, Q631, Q867B, Q885`.

`Q1001`, `Q1002`, and `Q1003` are demographic/positional conditioners and must not enter the co-signature attitude/response graph as targets.

Q873 is the root response surface that generates/contains the branch structure. It is not silently reintroduced as an “other question” target merely to satisfy the oracle.

Within this bounded catalog the production controller must enumerate candidates under Authority-37 law, not under an oracle-supplied shortlist. For J=3, canonical triple enumeration over 14 individual targets yields `C(14,3)=364` unordered target triples before any source/routing/authority typed exclusions. No L03 winner may receive special reachability.

## 5. Branch identity oracle

The integrated controller must naturally recover and retain the Lebanon response branch:

`COUNTRY == 10 AND Q873_1 == 1`

where Q873 option 1 means **socioeconomic class selected as one perceived basis of discrimination**.

It must not reinterpret this as objective socioeconomic class, a demographic identity, a causal type, or an actor belief essence.

Exact expected identities:

- Lebanon raw respondents: `2403`; sorted-ID SHA-256 `a6eddf236aa11073caa813a79a92a02fa74068c85176afc03f495e3be6735e7a`;
- Q873_1 branch raw respondents: `1334`; sorted-ID SHA-256 `ee6d4b46cdfc6dbcab7acc3673231517283fed65aabdbf9bfa2e43b6c65f3d50`;
- Q873_1 complement raw respondents: `1069`; sorted-ID SHA-256 `cc0ca1d852d94445130843bb3d18bc3f03ff211795b35d76fc3b800b29c92184`.

Exact WT sums from the source-decoded IEEE-754 values, represented as rational numbers:

- Lebanon: `43288601587674396853/18014398509481984` (`2403.000109323061` display);
- branch: `6041736647516061767/4503599627370496` (`1341.535026958787` display);
- complement: `19121654997610149785/18014398509481984` (`1061.465082364274` display).

Branch membership and replay identity are acceptance facts. They are not seed inputs.

## 6. Pair co-signature witnesses

The implementation must retain multiple naturally enumerated supported co-signatures; it may not collapse the branch to one “best” pair. At minimum, the following oracle-known pairs must be reproduced when reached by ordinary bounded enumeration:

| case | pair | branch n / V | overall n / V | complement n / V |
|---|---|---|---|---|
| P001 | `Q201A_1 × Q601_4` | 1276 / 0.09410435250419058 | 2295 / 0.14877303864980299 | 1019 / 0.24001995990139308 |
| P002 | `Q511 × Q601_4` | 1307 / 0.26823494415235805 | 2364 / 0.19762740917237048 | 1057 / 0.14158535567063227 |
| P003 | `Q606_4 × Q867B` | 1208 / 0.17683543166138382 | 2181 / 0.11664040376167224 | 973 / 0.054349840672116234 |
| P004 | `Q512 × Q631` | 1327 / 0.28609885263899415 | 2385 / 0.21206844860987328 | 1058 / 0.16841262491944498 |
| P005 | `Q606_4 × Q606_8` | 1315 / 0.39622754736530613 | 2349 / 0.3482247108118129 | 1034 / 0.2908000878590915 |

Cramér's V is a descriptive derivation from same-respondent joint evidence, not the primary empirical carrier and not a significance gate.

Acceptance requires the direct joint cell projection (or information-equivalent exact incidence) and exact complete-case denominator, not merely a scalar V.

## 7. J=3 direct-joint witnesses

Three source-backed triples are frozen. The first is the primary information-loss witness; the other two prevent overfitting to one accidental configuration.

### H01 — primary

`Q201A_3 × Q606_2 × Q606_8`

Branch:
- raw joint denominator `1265`;
- exact WT joint denominator `22689411435814542979/18014398509481984`;
- direct raw 4×4×4 tensor SHA-256 `734077830a27ac3a2a3961e520f4ac6c4907070259357f718770b506784a89bb`;
- normalized exact-WT tensor SHA-256 `02dee6ed7352a4fe0db8cb557801da3aa1a389e0022bb4409e4c2b2ba1b5021d`;
- all-pairwise-margin maximum-entropy reconstruction matches each pairwise margin within `4.547473508864641e-13` but differs from the observed direct joint by TV `0.08395055830683337`;
- `G²=87.32678818699358`, `df=27`; p-value is diagnostic only;
- largest residual cell `4|4|1`: observed `204`, pairwise-only expected `224.13897891630518`.

Complement:
- raw denominator `1004`;
- WT denominator `1119426255918164647/1125899906842624`;
- raw tensor SHA `70e3597f8def78553c6c588b9dac700544832cd0814163de7b779c5797cd143a`;
- WT tensor SHA `f3d1b8f59ac8d4eb8525c2a4463b882abb6b18da075830da57a2fea642ee2a54`;
- pairwise-margin error `1.7053025658242404e-13`; direct-joint TV from pairwise model `0.04403338817639841`.

Lebanon overall:
- raw denominator `2269`;
- WT denominator `40600231530505177331/18014398509481984`;
- raw tensor SHA `8dc41e2e634fbbb4992dea12dd85f8075aa720c3645a66e0307a8bea8f11aa16`;
- WT tensor SHA `42123517b42b98a9cdefd1949be5ca74e310d292a07ffc09915ef9835d4dd455`;
- pairwise-margin error `2.2737367544323206e-13`; direct-joint TV from pairwise model `0.061364685599260185`.

### H02 — corroborating

`Q606_2 × Q606_4 × Q601_4`

- branch: raw `1299`, WT `11636702508324549299/9007199254740992`, raw tensor `6ce8e3afc3f528d8dd24c52eeab9076878fb9b6004a355b6dd400eaa63a6840a`, WT tensor `4cff2fe7ab36cacdbc4611cfc564a836a742cdf711a69495029bf7aec55c6890`, joint-TV `0.06396104408108777`;
- complement: raw `1038`, WT `9265931201049728953/9007199254740992`, raw tensor `74f342a36a1ae9a0932b696a986dd5a89d361b24a5dc8daa53f28391f5109cdd`, WT tensor `c53d263b7975df4b1b7c08188b7aa7c5d10a8e206c49e5fe4f3756bdf9565c50`, joint-TV `0.03789035857893133`;
- overall: raw `2337`, WT `5225658427343569563/2251799813685248`, raw tensor `f2bd9f2b20e2b46a9bdd5eeb84b1fc513a9670e2ad2d9502a62a0e1a60e4872b`, WT tensor `f0b5217c85ad4828cc88ad32deba5ce2d2fc801f0fcf72a09cedfc65473de2f0`, joint-TV `0.043765613196712225`.

### H03 — corroborating

`Q533_4 × Q606_8 × Q631`

- branch: raw `1296`, WT `726841595072089263/562949953421312`, raw tensor `057c08b4d9a20caf84b202cfbee19e5bf9ff14a6d7db73e350fd715223238136`, WT tensor `278c6c3211f430a5db2e4cb2238f648d913f9ebdf0f8a1e5f5e46a5b6008ebb8`, joint-TV `0.08561175190061374`;
- complement: raw `1024`, WT `18190634781082692459/18014398509481984`, raw tensor `f208733eafd75690362ea2a786633e7a7b36bf3f3344d3a693d34ed7e690b9a0`, WT tensor `f1fe14f2afd1adb1da83b06fd57d5f5b5cfeb9cb14c8ec3278f0520501cbe8ba`, joint-TV `0.06017593953527609`;
- overall: raw `2320`, WT `41449565823389548875/18014398509481984`, raw tensor `7d254304ea26e88db4eea910606b1ed969ae9065d762694f46ed3b4ff70c714e`, WT tensor `34f7dd1f80df20f7c71ec7dd90f583d25d42b6914145e9eb1b131d367b837514`, joint-TV `0.06262704463071202`.

## 8. Tensor canonicalization

For oracle hashing, response values use the source-governed ordered target list in the query, while the complete Cartesian substantive domain includes zero cells.

Raw payload:

```text
{
  variables: [ordered target identities],
  raw_denominator: exact integer,
  cells: {"v1|v2[|v3]": exact integer for every domain cell}
}
```

Weighted payload is identical except every WT value is first normalized to its exact numeric rational value and summed exactly per cell and denominator. Oracle files represent those values as `numerator/denominator` strings.

Hash rule: canonical JSON with sorted mapping keys and compact separators, then SHA-256.

A production exact-number representation does not have to copy this textual fraction syntax. The harness must normalize numerically exact production values to the same rational value before comparing the oracle hash. Approximate float equality is not sufficient for an “exact” pass.

## 9. Denominator law

The following may not be collapsed:

`BRANCH_TOTAL != TARGET_DENOMINATOR != PAIR_JOINT_DENOMINATOR != J3_JOINT_DENOMINATOR`

For example, branch membership is `1334`, but H01 branch complete-case n is `1265` and P003 branch complete-case n is `1208`. Each target/joint object must retain its own risk/response-state-resolved denominator.

Raw and governed-weighted support are separate parallel observations. Weighting does not alter respondent identity.

## 10. Typed response-state law

For the frozen L03 domains, `98/99` DK/refusal are not substantive target categories and are excluded according to their governed response-state semantics. A substantive source value such as `Q885=97` remains substantive where the source semantics say it is substantive.

The harness must reject:

- DK/refusal/missing being treated as empirical zero;
- missing rows being silently turned into a smaller denominator without a typed state/risk explanation;
- a substantive special-looking code being removed merely because its numeric value resembles a conventional missing code.

## 11. Pairwise-only negative control

A candidate implementation FAILS J=3 parity if it can reproduce all three pairwise margins of H01/H02/H03 but cannot emit/replay the direct three-way joint.

Specifically, H01 proves that all pairwise margins can be reproduced essentially exactly while the direct branch joint still differs by TV `0.08395055830683337`. Therefore:

`PAIRWISE_MARGINS_MATCH =/= J3_PARITY`

A synthetic/IPF table is a diagnostic negative control, not an acceptable substitute for source-backed same-respondent J=3 evidence.

## 12. Deterministic replay

Acceptance must bind at minimum:

- exact source hash and source/release/universe refs;
- root Q873 query/surface identity;
- exact discovered branch predicate and branch-membership replay identity;
- bounded target catalog authority;
- exact ordered target refs and arity;
- branch/overall/complement risk identities;
- raw versus weighted measure identity;
- exact response-state semantics;
- direct joint fact/receipt refs;
- controller/frontier authority/version;
- deterministic replay refs.

Re-running unchanged source + authority + controller law must reproduce the same branch membership and same normalized direct tensor receipts.

Combined source-derived oracle digest for this prep lane:

`150b6ea7e7ccb08e906cf43eea207aea716a29dec0e0a33eba3d18eea1dac851`

## 13. Current launch-tree target probe

At launch HEAD `4c3453b81179464670600992ef2b2bdafd871127`, Authority 37 has been adopted but the authorized production fracture-map controller/J=3 integration has not yet been merged onto this worker lineage. Tree/code searches resolve no production `EmpiricalFractureMapReceipt` or fracture-map controller surface. The exact lineage from Authority-36A HQ to this worker adds only Authority 37 and this I07 command.

Therefore the executable production parity test is intentionally:

`NOT_EXECUTED_FAIL_CLOSED__AUTHORITY37_CONTROLLER_INTERFACE_NOT_PRESENT_AT_LAUNCH_HEAD`

This lane MUST NOT repair that absence.

## 14. Acceptance outcome vocabulary

A later implementation test should return exactly one of:

- `PASS__REALDATA_BRANCH_COSIGNATURE_AND_DIRECT_J3_PARITY`;
- `FAIL__SOURCE_OR_AUTHORITY_IDENTITY_MISMATCH`;
- `FAIL__BRANCH_IDENTITY_OR_MEMBERSHIP_MISMATCH`;
- `FAIL__TARGET_ENUMERATION_LEAKED_OR_INCOMPLETE`;
- `FAIL__PAIR_OR_MULTIPLE_COSIGNATURE_LOSS`;
- `FAIL__J3_DIRECT_JOINT_MISMATCH`;
- `FAIL__J3_RECONSTRUCTED_FROM_J2`;
- `FAIL__RAW_WEIGHTED_DENOMINATOR_COLLAPSE`;
- `FAIL__TYPED_RESPONSE_STATE_COLLAPSE`;
- `FAIL__REPLAY_NONDETERMINISM`;
- `BLOCKED__TARGET_CONTROLLER_INTERFACE_UNAVAILABLE`.

## Negative ceiling

This contract establishes no causation, actor belief/personality/ideology, significance threshold, physical architecture choice, A/B/C preference, or permission to commit raw survey bytes.

`I07_REALDATA_COSIGNATURE_PREP_R1_COMPLETE`
