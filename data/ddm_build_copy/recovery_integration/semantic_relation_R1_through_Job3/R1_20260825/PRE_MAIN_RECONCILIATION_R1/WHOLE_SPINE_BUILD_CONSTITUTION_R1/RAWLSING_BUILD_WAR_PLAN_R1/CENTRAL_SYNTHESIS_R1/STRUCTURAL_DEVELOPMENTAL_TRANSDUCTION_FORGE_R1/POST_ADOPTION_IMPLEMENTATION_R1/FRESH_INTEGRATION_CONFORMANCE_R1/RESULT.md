# SDTF R4 R1–R4 FRESH INDEPENDENT INTEGRATION / CONFORMANCE COURT R1 — GOVERNED RETURN

Status: `BLOCKED`

Terminal:

`SDTF_R4_R1_R4_FRESH_INDEPENDENT_INTEGRATION_CONFORMANCE__EXACT_BLOCKER_PROVED`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-hq-sdtf-r4-r1-r4-fresh-integration-conformance-r1`

Commission tip: `9a4b43da2502c1df77b9d1b73adcdf3498390476`

Exact assembled candidate parent: `64c4c40118c874cfecf9c14ee9a063bdaafa1bd7`

Authorized grain:

`SDTF_R4_R1_R4_FRESH_INDEPENDENT_INTEGRATION_CONFORMANCE_ONLY`

No production repair, semantic redesign, concrete rule minting, actor-fact minting, coefficient/calibration choice, world write, or OBL062 closure was performed.

## 1. Exact blocker

`R1_R2_CURRENT_RULE_ADMISSION_AND_EXACT_RULE_IDENTITY_CHAIN_NOT_CONSERVED`

The assembled candidate does not lawfully connect R1 mechanism-rule authority/currentness to R2 D1 hosting.

R1 correctly supplies a fail-closed current-rule gate. Its exact future-rule identity is:

`ExactRef(kind="SDTF_R4_MECHANISM_RULE", object_id=rule_id@rule_version, content_hash=rule_content_hash)`

and its `MechanismRuleAuthorityBinding` separately binds:

- exact P1–P5 class/composition;
- constitution current-selection evidence;
- source/claim/evidence/mechanism/shape/currentness trace;
- competent rule-owner authority;
- measurement / estimand / identification dispositions;
- mandatory competent causal-use authority;
- calibration authority when numeric;
- rule currentness;
- exact rule-current-selection evidence.

`require_current_rule_admission()` rejects any rule not explicitly `CURRENT_ACCEPTED` with exact current-selection evidence.

R2 does not consume that binding or gate.

Its `D1RuleApplicationRef` accepts only:

```text
rule_application_id
rule_id
rule_version
rule_hash
```

and reconstructs a different exact rule reference:

`ExactRef(kind="MECHANISM_RULE_RECORD", object_id=rule_id@rule_version, content_hash=rule_hash)`.

`ExactRef.key` includes `kind`, so the R1 exact rule identity and R2 reconstructed rule identity are not equal even when id/version/hash text is copied exactly.

More decisively, `D1HostingAdapter.host_direct_derivation()` accepts that R2 application object directly and creates a `D1ApplicationRevision(status="SUPPORTED_CURRENT")`, then exposes its output in `current_output_refs()`, without requiring:

- an R1 `MechanismRuleAuthorityBinding`;
- R1 binding identity;
- `require_current_rule_admission()`;
- rule current-selection evidence;
- the R1 causal-use/calibration/source-authority envelope.

Therefore this forbidden path exists in the exact assembled candidate:

```text
R1 rule body identity exists
BUT no R1 current-rule admission exists
        ↓
copy raw rule_id / version / hash
        ↓
construct R2 D1RuleApplicationRef
        ↓
R2 host_direct_derivation(...)
        ↓
SUPPORTED_CURRENT rule application
        ↓
current derived consequence output
```

That is an integration-level currentness bypass.

## 2. Why this violates adopted R4

The reviewed companion makes the following firewall binding:

```text
CURRENT(D1' CONSTITUTION)
!= CURRENT(MECHANISM RULE)
!= CURRENT(RULE APPLICATION)
!= CURRENT(CONSEQUENCE FACT)
!= CURRENT(WITNESS/STATE SUPPORT)
```

It also requires every current D1' fact to remain auditable through exact direct determinants, the exact governed rule application/version, and the derived consequence, with authority ceilings preserved through composition.

R2's local derivation lineage is content-addressed, but the combined R1→R2 chain is not a governed-rule chain because R2 can create current application/consequence state without proof that the mechanism rule is current under R1.

The defect is not cured by the caller comment that R2 authority/currentness is “decided upstream.” Under the adopted law, the exact proof must survive the seam. An unenforced precondition is not currentness provenance.

## 3. Smallest exact owning grain

Smallest owning family:

`R2 / G2 D1 hosting / dependency / invalidation / replay`

Exact owning commissioned grain:

`SDTF_R4_D1_HOSTING_DIRECT_DERIVATION_REVERSE_DEPENDENCY_INVALIDATION_REPLAY_R1_ONLY`

R1 is not the missing owner. R1 already supplies the exact current-rule authority binding and fail-closed admission gate. The failure occurs when R2 accepts an application/current derivation without consuming that proof.

The smallest lawful repair boundary is therefore only the R1→R2 admission seam inside R2 hosting/redrive: R2 must require and conserve the exact R1 current-rule admission identity/proof before a rule application may become current. The repair owner must not mint rules, select authorities, choose calibration, or redesign R4.

This court does not choose the repair representation. In particular it does not decide whether R2 should consume the full R1 binding object, an exact content-addressed binding reference plus independently verifiable current-selection closure, or another semantically equivalent exact bridge. That is the owning repair grain's implementation decision, constrained by adopted law.

## 4. Court-local hostile proof

Committed hostile proof:

`HOSTILE_R1_R2_CURRENTNESS_BYPASS_PROOF.py`

Creation commit:

`5640f4ea03dd271da0b61be0ce45a23ffc4a2d05`

The proof constructs an R1 `MechanismRuleIdentity` but intentionally supplies no R1 `MechanismRuleAuthorityBinding` and never calls `require_current_rule_admission()`. It then constructs the R2 application from the same raw id/version/hash and follows R2's public hosting path to `SUPPORTED_CURRENT` plus a current output.

It also pins the exact identity mismatch:

```text
R1 rule ref kind = SDTF_R4_MECHANISM_RULE
R2 rule ref kind = MECHANISM_RULE_RECORD
R1 exact ref != R2 exact ref
```

This is a cross-candidate hostile construction, not a producer test and not a repair.

## 5. Exact frozen candidate identities

Production candidate blobs remained unchanged:

- R1: `c94997f5c7f2bbee9cd99c570554fd48c0f47556`
- R2: `66ffd2e1df9ab81970af9264f27de1f449752064`
- R3: `06c8a2259436e7209bad4e4b3f8c314b18446fe6`
- R4: `9964a24e25467fa53cc9f5529b6f40be9f11f53a`

Focused-test blobs remained unchanged:

- R1: `7a63dae14a6d3bf95f70e8b92d7f18e8b27f0538`
- R2: `b18c3c4b3e13e00da97412dba8d647cbd3c2b1cd`
- R3: `e3ccedf6ffd694aa01728b8282582e5229b6bc4f`
- R4: `324ca6095a74e4e3dd2cc27ccb25334318d1bf4a`

Authority basis remained:

- frozen R4: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`;
- final reviewed companion blob: `4e77479afa3cce4cce7e38168f7ee9c6bf021cd0`;
- immutable S5 baseline: `8ad68cd5731db6a4c4c75f5cc1bddbf95018f882` (90 canonical semantic vectors + 30 metamorphic relations), plus the final K4/ACTIVE augmentations.

## 6. Other invariant dispositions

The decisive blocker is cross-candidate R1→R2 composition. It does not imply that every local candidate surface is defective.

Static independent inspection found:

- R1 locally preserves P1–P5 only, rule/constitution currentness separation, independent causal-use authority, and separate calibration authority for numeric rules;
- R2 locally implements exact determinant/application/output references, reverse dependency indexes, scoped redrive, unsupported-output closure, history, replay hashes, and same-context self-ancestry guards;
- R3 locally preserves orthogonal K1/K2/K3/K4 axes, bare `ACTIVE` noncollapse, K4 Path A/B, explicit-negative proof, and `UNKNOWN_NOT_PROVEN` on stale/revoked/unproved witness state;
- R4 locally rejects private V3 state, generic simulation, interpretation/expectation/striving, and OEE/encounter derivation as competent objective-world-response authors; it requires already-admitted external occurrence plus already-admitted competent external objective world response before issuing an R4 redrive request;
- OBL062 remains OPEN and this court creates no non-event laundering path.

Those local holdings do not qualify the assembled runtime while the R1→R2 currentness seam remains open.

Full dispositions are frozen in `INVARIANT_DISPOSITIONS.csv`.

## 7. Execution / test disposition

Producer PASS reports and producer test runs were not used as qualification evidence.

The court terminated at a decisive pre-execution integration conformance blocker visible directly in the exact frozen production interfaces. The four focused suites, the full S5 vector/metamorphic corpus, and a second deterministic replay execution were therefore not freshly credited or represented as executed by this court. A successful local suite cannot make an assembled candidate conformant while a public cross-candidate path still permits current derivation without current governed-rule proof.

This is recorded explicitly in `EXECUTION_TEST_RECEIPT.json`; no execution result is being fabricated.

After the owning R2 seam is repaired and a new exact combined candidate is frozen, the fresh integration court must be rerun from the beginning, including the four focused suites, S5 90+30 plus K4/ACTIVE augmentations, hostile cross-candidate tests, and deterministic replay checks.

## 8. Scope / mutation receipt

- production-code edits: `0`
- focused-test edits: `0`
- R4 semantic redesign: `0`
- concrete mechanism rules minted: `0`
- actor facts minted: `0`
- coefficients/probabilities/thresholds chosen: `0`
- calibration values chosen: `0`
- source authorities minted: `0`
- world facts/writes minted: `0`
- OBL062 closure: `NO`
- rebase: `NO`
- main/coordinator mutation: `NO`

Court-local governed artifacts only were added under the commission directory.

## HQ return

Do **not** adopt the assembled R1–R4 candidate as runtime.

Return the blocker to R2/G2 at the exact admission-consumer seam. The next candidate must prove that a current D1 rule application cannot be hosted or redriven without exact current R1 mechanism-rule admission and identity conservation.

Final terminal:

`SDTF_R4_R1_R4_FRESH_INDEPENDENT_INTEGRATION_CONFORMANCE__EXACT_BLOCKER_PROVED`
