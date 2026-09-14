# L03 — LiTS-I learned exact query-envelope / expected-record freeze R1

Status: `BLOCK__EXACT_EXPECTED_RECORD_ID_EXTENSION_NOT_MATERIALIZED`

Executed grain:

`LITS_I_LEARNED_EXACT_QUERY_ENVELOPE_EXPECTED_RECORD_AND_PREQUERY_RISK_SET_COMPOSITION_FREEZE_R1_ONLY`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w10-l03-lits-learned-query-envelope-r1`

Commission tip: `eee532f0927db99ad2040d987772a506680192dc`

HQ authority: `dbcedcc6bd2ceeda2de9c23543a392f70fb7bac2`

Parent K03 authority: `9c765641a0c1c32c1becbc308feec488c136c30d`

Bound generic law: J02 `4c86fb44d06e27763b004dbd3181271cfb83efc1`

Bound source semantics: J03 `9a61151246ebf6ad5866aecc4b7e593282ac0f6f`

## 1. Holding

L03 resolves and freezes the lawful **query-envelope and pre-query composition law** for the exact D02/F02 LiTS-I `50-candidate / 77-query-role` learned workload, but does **not** claim PASS for the commissioned exact expected-record-ID freeze.

The smallest exact remaining blocker is:

`L03_BLOCK__K03_Q301_2_Q301_7_MEMBER_RECORD_ID_EXTENSIONS_AND_THEIR_COMMON_INTERSECTION_HAVE_NOT_BEEN_MATERIALIZED_FROM_THE_EXACT_CARRIER`

This is an extensional materialization blocker, not a semantic ambiguity and not permission to alter a denominator.

K03 intentionally froze target-local rules and count oracles while leaving `member_ids_materialization = MECHANICAL_FROM_EXACT_CARRIER_BEFORE_OUTCOME`. No accepted repository artifact persists the exact q301_2 or q301_7 member-ID extension. The exact LiTS-I Library carrier was materialized for L03, but this worker execution surface failed every attempted local binary/code execution call before the DTA could be decoded. L03 therefore refuses to fabricate record IDs, member-set hashes, common-intersection counts, or common-intersection hashes.

Everything that can be frozen without inventing those extensional identities is frozen below and in the governed companion artifacts.

## 2. Exact source / release scope

Exact carrier authority inherited from F02/B16/K03:

- Library file id: `file_0000000036dc81f8b8b546e356590a03`
- Library version: `1`
- filename: `LITS-2006-data.dta`
- bytes: `139531180`
- accepted SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows: `29002`
- variables: `1198`

Exact C11 logical release:

- kind: `C11LogicalRelease`
- object id: `LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79`
- content hash: `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`

Exact empirical universe hash:

`83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080`

The complete 29,002-record universe remains the accounting root. No row may disappear by omission.

## 3. Frozen target-local denominator authorities

### q301_2

Target-domain hash:

`6f80fc3c628e58f67777f9e60c1d1e433941b74297fb3387873d56f5aa162873`

Target-use authority hash:

`6002c1b572e3fff7a60554fda4e6b6749a80c88e5ee87da06d610a900568606d`

Risk-set-rule hash:

`1ec233e682e06e4befe434b166411a98ed97e2ca8927c02f3ff6f6aec1807a82`

Routing-risk authority hash:

`88a34f2a6bc46426c77bde88f87b0b704db06ea6cf358306ec5f7f88c0331c03`

Frozen count oracle:

- denominator members, native `1..5`: `24897`
- pre-query excluded: `4105`
  - `6 = Not applicable`: `1774`
  - `7 = Don't know`: `2327`
  - physical/system missing: `4`

Define exact expected member set `R2` extensionally as:

`R2 := { exact C11 respondent record r in U29002 | K03(q301_2,r) = DENOMINATOR_MEMBER }`

The definition and expected cardinality are frozen. Its exact enumerated member IDs / canonical member-set root are **not** claimed by L03.

### q301_7

Target-domain hash:

`5aca6389fb3fcf6584cde2a2d8c84a1b99fa5d27ef3b8e115714f2c31b3256df`

Target-use authority hash:

`d4d0af7aeb4313c5fa826b8a20a5c2a80cc107bb53c2bd9bdc1e51c7f8c62a5b`

Risk-set-rule hash:

`fd1bc16d5eae5f2763f03274a5b07de6289791c3042a6988b37d648186d9a95a`

Routing-risk authority hash:

`4626363db7ebaef6e719ddc0805fc3b00ba3c6de835c702ea7a77f97e098e7db`

Frozen count oracle:

- denominator members, native `1..5`: `28325`
- pre-query excluded: `677`
  - `6 = Not applicable`: `224`
  - `7 = Don't know`: `442`
  - physical/system missing: `11`

Define exact expected member set `R7` extensionally as:

`R7 := { exact C11 respondent record r in U29002 | K03(q301_7,r) = DENOMINATOR_MEMBER }`

The definition and expected cardinality are frozen. Its exact enumerated member IDs / canonical member-set root are **not** claimed by L03.

## 4. Bounded common-target composition

For the two D02 workload families that actually require both q301 variables as target variables — P1's joint role and P4's 5x5 joint-cell roles — L03 freezes the only lawful common-target pre-query composition:

`R27 := R2 INTERSECTION R7`

This does **not** assign any new meaning to a source code and does not create a predictor eligibility rule. It is the mechanical `COMMON_ELIGIBLE_RECORDS_ACROSS_VARIABLES` composition of two already-authorized target-local denominator memberships under J02/I03 accounting law.

No union, left-priority, right-priority, imputation, fallback, post-outcome deletion, or missing-value collapse is authorized.

Because the exact R2/R7 extensions are not persisted upstream and the exact carrier could not be decoded on this worker execution surface, L03 does **not** invent an `R27` cardinality or content hash.

## 5. Predictor-conditioned query law

The frozen D02/F02 workload already has exact q301 endpoint predicates plus the six F02 q310/q311 selectors. These are **query predicates**, not denominator-removal authorities.

Therefore:

- P0 target-cell queries use `R2` as their pre-query denominator envelope.
- P1 marginal q301_2 role uses `R2`.
- P1 marginal q301_7 role uses `R7`.
- P1 joint role uses `R27`.
- P2 baseline and conditioned roles target q301_7 and use `R7`; q301_2 endpoint + q310 + q311 conditions select a query subpopulation inside the lawful target envelope.
- P3's eight conditional-reversal roles target q301_7 and use `R7`; q301_2 endpoint and q310 stratum conditions are predicates inside the envelope.
- P4's 25 q301_2 x q301_7 joint-cell roles use `R27`.

A predictor nonmatch is not a new denominator exclusion. L03 creates no rule saying that predictor missingness, code 6, code 7, or system missing makes an otherwise target-eligible q301_7 record disappear from `R7`. Such records simply do not satisfy an exact equality predicate when that predicate is part of the query population definition.

This preserves K03's explicit `no_predictor_exclusion_authority` ceiling.

## 6. Exact frozen workload

Authority root: D02/F02 learned frontier `PREV3_LEARNED_WORLD_POSITIVE_WORKLOAD_R1`.

Exact workload size:

- P0 q301_2 target cells 1..5: `5 candidates / 5 roles`
- P1 q301_2 x q301_7 joint non-factorization: `1 / 3`
- P2 q301_7 conditioned by q301_2 endpoint x q310 x q311: `18 / 36`
- P3 q301_2 endpoint contrast across q310 strata for q301_7 cell 5: `1 / 8`
- P4 complete q301_2 x q301_7 5x5 cells: `25 / 25`

Total: `50 candidates / 77 query roles`.

Candidate order remains `CANONICAL_CANDIDATE_HASH_ORDER`. No learned empirical result was executed, scored, ranked, pruned, added, or deleted.

Raw query identities inherited from D02 remain frozen:

- q301_2 query hash: `8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44`
- q301_7 query hash: `deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7`
- q301_2 x q301_7 joint query hash: `ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053`

## 7. F02 selector closure preserved

F02 final authority:

`482bb884a99e31ba77e904d0df39fffc872cbed3`

F02 already closed the old q310/q311 selector-materialization blocker without learned outcome execution. L03 consumes those exact predicates as condition predicates only.

Exact selector membership roots:

- Q310V1: count `12941`, root `8652031a8c7753051f521bcf30aefb8dbfeeed623f0387e9a2c34e42ee45526d`
- Q310V2: count `5916`, root `7d5ab913560088d8602165cdc6752b27a2d262129b2d3fe0ad08e2b4d5e7d25`
- Q310V3: count `9375`, root `04a0f054095510057eb75b23bdd6de82bb5b9372cdf9a234d79f9852889511a6`
- Q311V1: count `20527`, root `4f0a903ee2fe803d156575105dfa51702dda824aa59e76c487a5df532c17f2a2`
- Q311V2: count `1312`, root `f6b11e45fc6250ea32e10d36077a18bc282ace1652464241174a1b6d0b3fe7e`
- Q311V3: count `6359`, root `77910ca898aec053a03690c77798755c51f7d0495a0341442133087142953788`

No selector is re-labeled, inferred, widened, or turned into a risk-set rule.

## 8. K02 boundary

K02 `639aec0e6b8310f07283922faf0afdc7e3dc7c48` is a producer candidate only. L03 does **not** consume it as independently qualified or centrally integrated production authority.

The J02 semantic/accounting law is sufficient to adjudicate the frozen envelope semantics here; later learned execution still requires the separately commissioned L02 independent qualification and HQ convergence before K02 production machinery may be relied on.

## 9. Exact blocker / minimal successor work

There is no remaining semantic decision about which risk-set law applies to which of the 77 query roles.

The single unresolved commissioned product is extensional:

1. decode the exact accepted Library carrier;
2. reconstruct the exact C11 respondent record IDs under the accepted C11 identity law;
3. materialize and canonically order all `R2` member IDs and verify cardinality `24897`;
4. materialize and canonically order all `R7` member IDs and verify cardinality `28325`;
5. compute exact `R27 = R2 ∩ R7` and its cardinality;
6. freeze canonical exact-set hashes/roots for R2, R7 and R27;
7. bind those roots into the already-frozen P0-P4 / 77-role envelope matrix;
8. do all of this before observing or scoring any learned outcome.

The Library carrier itself was successfully materialized to the worker environment with the exact accepted Library file identity and byte length. The worker-local execution substrate then returned transport/runtime failures for every attempted container/Python call, including a simple existence/hash read, so no truthful DTA decode or set-root computation completed in this turn.

This worker-local execution failure is **not** a new Rawlsing semantic authority defect. It is recorded only because the commission requires exact record-ID extensions and L03 will not claim them without actually deriving them.

## 10. Boundary preservation

- no learned workload executed or scored;
- no empirical outcome observed;
- no K02 producer candidate promoted to qualified authority;
- no code 6 / code 7 / system-missing collapse;
- no predictor eligibility invented;
- no post-outcome denominator deletion;
- no target widening or binary recode;
- no V3/person/psychic semantics;
- no OBL063 revival;
- no MAIN mutation;
- no PRE-MAIN mutation.

## 11. Successor gate

`GATE-LITS-I-LEARNED-POSITIVE-REEXECUTION = BLOCKED__EXACT_R2_R7_R27_EXPECTED_RECORD_ID_EXTENSIONS_MUST_BE_FROZEN__AND_K02_PRODUCTION_MUST_STILL_PASS_INDEPENDENT_QUALIFICATION_AND_HQ_CONVERGENCE`

Terminal:

`L03_BLOCK__QUERY_ENVELOPE_AND_PREQUERY_COMPOSITION_LAW_FROZEN_FOR_ALL_50_CANDIDATES_77_ROLES__EXACT_EXPECTED_RECORD_ID_EXTENSIONS_NOT_FABRICATED__REQUIRES_CARRIER_DERIVATION_BEFORE_LEARNED_EXECUTION`
