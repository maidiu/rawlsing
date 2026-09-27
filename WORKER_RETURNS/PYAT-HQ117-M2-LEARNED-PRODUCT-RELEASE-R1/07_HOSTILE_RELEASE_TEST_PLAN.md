# PYAT HQ117 — M2 Hostile Release Test Plan

## Purpose

This is the minimum adversarial qualification plan for a future explicitly authorized M2 implementation.

The tests are source-free unless a later implementation commission separately authorizes source-backed specimens.

| ID | Hostile case | Required result |
|---|---|---|
| H01 | Same semantic subject + identical closures constituted twice | identical release_id; idempotent |
| H02 | Same semantic subject + different authority closure | different release_id; semantic subject may remain same |
| H03 | Same release moved to a new filesystem path | same release_id; new publication_binding_id |
| H04 | Same release serialized/compressed differently | same release_id if semantic subject unchanged; representation/binding integrity changes only |
| H05 | Materialized representation replaced by exact virtual rebuilder | same release_id; new publication binding; replay grade verified |
| H06 | Virtual rebuilder silently uses current/latest authority instead of historical ref | hard fail FORBIDDEN_SELECTOR / authority mismatch |
| H07 | Requested exact release unavailable but newer release exists | hard fail; no fallback |
| H08 | Caller requests "latest" | hard fail; M2 does not select current |
| H09 | Caller requests semver range or nearest compatible release | hard fail |
| H10 | Direct producer ref published without copying payload | pass if exact producer identity/closure preserved |
| H11 | Publication wrapper copies product fields and drops producer ref | fail SEMANTIC_REOWNERSHIP_ATTEMPT |
| H12 | Higher-order/n-ary product published through pairwise flattened copy | fail subject parity / reownership |
| H13 | VALID_EMPTY published as positive relation with empty payload | fail NEGATIVE_STATE_LAUNDERING_ATTEMPT |
| H14 | VALID_EMPTY published as exact typed disposition | pass |
| H15 | EXACT_CANDIDATE_REJECT encoded as negative semantic claim | fail |
| H16 | BLOCKED encoded as REJECT | fail |
| H17 | MISSING_AUTHORITY encoded as NOT_APPLICABLE | fail |
| H18 | NONCOMPARABLE encoded as NO_TRANSPORT without producer authority equating them | fail |
| H19 | COVERAGE_LIMITED partial search published as exhaustive absence | fail |
| H20 | OBSERVED_ZERO published with exact measure/risk-set/time/uncertainty | pass if producer subject owns zero fact |
| H21 | ZERO_SUPPORT collapsed into OBSERVED_ZERO | fail |
| H22 | Cache loss causes release to disappear semantically though exact rebuild remains | fail implementation invariants; cache is nonsemantic |
| H23 | Cache loss yields typed operational miss then exact governed rebuild | pass |
| H24 | Changed cache/index layout changes release_id | fail |
| H25 | Changed validation rule in determinant closure leaves release_id unchanged | fail |
| H26 | Changed unrelated determinant invalidates release globally | fail selective-invalidation law |
| H27 | Changed exact determinant returns affected release refs only | pass; no lifecycle classification by M2 |
| H28 | Dependency engine auto-labels affected release CORRECTS or WITHDRAWS | fail CURRENTNESS_INFERENCE_ATTEMPT / jurisdiction violation |
| H29 | Publication order used to choose current | fail |
| H30 | Only release in registry automatically treated as current | fail |
| H31 | Successful resolution grants PRE-V3 target-use permission | fail PERMISSION_WIDENING_ATTEMPT |
| H32 | Successful resolution grants Field Forge structural admission | fail |
| H33 | Successful resolution grants actor/V3 knowledge | fail |
| H34 | Current M3 selector returns exact release_id, then M2 resolves it exactly | pass |
| H35 | M3 selector returns mutable alias, M2 accepts it | fail |
| H36 | Two bindings for same release use two mirrors | pass if both resolve exact same release/subject |
| H37 | Failover chooses a binding for a different release_id | fail |
| H38 | Endpoint relocates for a released learned service | same release_id; new binding id |
| H39 | Service endpoint serves a different model/config release under old binding | fail release/binding integrity |
| H40 | Historical service invocation lacks exact random/search/subsampling determinants while claiming exact replay | fail REPLAY_CLOSURE_INCOMPLETE |
| H41 | Adaptive partial search preserves unvisited/unknown state and exact budget/stop law | pass |
| H42 | Adaptive partial search drops unvisited state and claims global negative | fail |
| H43 | Release closure stores only package/library name/version where executable semantics cannot be reproduced | cannot claim exact deterministic rebuild; fail or downgrade replay grade |
| H44 | Historical release replay resolves newer authority with same authority id but different hash | fail |
| H45 | Authority id/version/hash mismatch | fail |
| H46 | Source content hash mismatch during rebuild | fail SOURCE_CONTENT_MISMATCH |
| H47 | Rebuild returns physically different bytes but exact producer semantic identity is equal and physical bytes are nonconstitutive | pass |
| H48 | Rebuild returns same-looking fields but loses typed absence/order/cardinality that producer makes constitutive | fail SEMANTIC_REBUILD_MISMATCH |
| H49 | Explanation lineage omits a blocker/missing-authority node | fail EXPLANATION_LINEAGE_INCOMPLETE |
| H50 | Human-readable explanation exists but exact refs do not | fail |
| H51 | Release of a typed integrity-failure audit disposition is attempted | pass if producer owns exact failure disposition; no underlying positive truth implied |
| H52 | Publication binding unavailable | typed operational failure; release history remains |
| H53 | All materialized bindings unavailable but exact rebuilder binding works | pass; same release_id |
| H54 | Direct consumer dereferences exact producer object without M2 release where its contract permits | pass; do not invent M2 release/currentness |
| H55 | Direct consumer calls exact producer object and labels it a generic published/current learned product | fail unless an actual M2 release + M3 selection exists |
| H56 | Same release receives second valid publication binding | pass; no currentness effect |
| H57 | Deleting one mirror binding withdraws semantic release | fail jurisdictional inference |
| H58 | Search catalog metadata differs from producer semantic scope | fail projection integrity; catalog cannot become authority |
| H59 | Content hash computed over timestamp/insertion order so same preimage gets different ids | fail canonicalization |
| H60 | Concurrent constitution of same release creates competing semantic ids | fail; must converge on identical release_id |

## Mandatory grouped gates

### Identity gate
H01-H06, H24-H25, H47-H48, H59-H60.

### Ownership gate
H10-H12, H31-H33, H54-H55.

### Negative-state gate
H13-H21, H41-H42, H51.

### Replay gate
H06-H07, H40, H43-H46, H49-H50, H53.

### Lifecycle firewall
H08-H09, H27-H30, H34-H35, H57.

### Publication-resolution gate
H03-H05, H22-H23, H36-H39, H52-H53, H56, H58.

A future implementation does not qualify by passing only happy-path publication.

## Terminal criterion

PASS only if:
- all required positive canaries pass;
- all forbidden inference/laundering canaries fail closed with typed state;
- release identity is stable under nonsemantic physical change;
- release identity changes under constitutive closure change;
- M2 never selects currentness or grants consumer permission.
