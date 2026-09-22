# Required Hostile Tests — Arab Barometer Contract Audit

These tests are specified only. None was executed by this worker.

## A. Source-free adapter/runtime-package tests

### H01 — Typed physical-key nonintersection

For every runtime-admitted numeric response, construct hostile equal-looking native values across R5 lanes (for example integer 0 vs float64 0.0) and require distinct `physical_value_binding_key` identities. A hand-authored documentary integer must not match a decoder float key merely because host-language equality says `0 == 0.0`.

Expected failure: `DECODER_RUNTIME_TYPE__GOVERNED_KEY_NONINTERSECTION`.

### H02 — Missing-state is part of the key

Same raw value, different physical missing states/declarations must produce different governed keys. A user-missing declaration may not collapse into system missing or observed storage.

### H03 — Producer/consumer adapter completeness

Every runtime-admitted source slot must have an explicit `PhysicalSlot(ordinal,name)` and exact governed value/state rule. Missing rules fail closed; labels/frequencies/defaults cannot fill them.

### H04 — Historical dependency no-ambient-fallback

Mutate/remove the exact historical Authority71/72/documentary dependency ref while leaving a same-named current artifact available. Runtime-package construction must fail rather than select the current/adjacent artifact.

### H05 — Frozen runtime catalog identity

Change one adopted authority/catalog content hash, scope release ref, or source SHA while preserving shape. `Pre553RuntimeAuthoritySet` admission must fail.

### H06 — Dynamic query preimage retention

Generate a derived I05 query whose ref is absent from the static template catalog. Terminal packaging must resolve it from the retained exact dynamic preimage. Deleting that preimage must fail closed; no hash inversion/reconstruction/default lookup.

### H07 — Retained I03 fact preimage closure

For every I05 fact ref, require exactly one retained `EmpiricalFact` preimage and exact closure over per-query-role and global fact sets. Missing/conflicting preimages fail.

### H08 — Terminal/post-I05 exact consumer

Feed the post-I05 consumer a shape-compatible query/fact object with one mismatched content hash or replay ref. Reject it even if scalar states/counts match.

### H09 — Routed-target membership preimage

For a runtime-admitted routed Arab target, require exact `risk_set_ref`, `RoutingEligibilityFact`, routing authority, and `member_set_replay_ref`. Delete respondent membership preimage: result must be unavailable/unresolved, never zero/nonmember by absence.

### H10 — No LiTS successor import

Present a LiTS-style successor/risk authority with otherwise compatible shape to an Arab package. Reject unless an independent Arab source-local authority explicitly requires it. Ordinary Arab route membership must be sufficient without fabricating historical-successor machinery.

### H11 — Exact question/value → response-ref binding

For a runtime predicate leaf, mutate either question ref, native value representation, response-value ref, or frozen release scope. Exact dialect validation must reject.

### H12 — Source-specific terminal-state adapter

Attempt to pass source realization states such as `ROUTING_BOUNDED_UNKNOWN`, `SECOND_RANK_NOT_RECORDED_BY_INSTRUMENT`, dictionary-membership states, or documentary route labels directly into a generic PRE553 terminal field. Reject unless a governed adapter maps the exact state to a valid generic domain with authority.

### H13 — Bounded UNKNOWN remains bounded

Ask the runtime package for a value/route/design semantic listed as bounded UNKNOWN. It must omit/unresolve/authority-block the claim according to the governed contract; never synthesize a best guess from name, frequency, neighboring code, or other wave.

## B. Wave-specific source-free hostile cases

### ARAB1

- **A1-H01 literal control text:** `can\u0092t choose` and a typography-repaired display string must remain distinct source/display objects; display normalization cannot rewrite the raw witness.
- **A1-H02 replay identity:** two synthetic rows sharing SER must remain distinct under source-SHA+ordinal.
- **A1-H03 Morocco route:** missingness cannot substitute for COUNTRY-based documentary routing.
- **A1-H04 unresolved alias:** complementary field behavior cannot prove `V715onlymorocco` == printed `q715moroccoonly`.
- **A1-H05 design vacuum:** no named/unnamed design-like carrier may become a default analytical weight without exact authority.

### ARAB2

- **A2-H01 zero/system-missing split:** ordinary Q2062 zero + dictionary label “0. missing” must not become SYSTEM_MISSING.
- **A2-H02 code-0 authority:** Q101/0 or Q2062/0 cannot inherit meaning from neighboring codes or labels.
- **A2-H03 ranked slots:** Q2061/Q2062 cannot flatten, reorder, or deduplicate.
- **A2-H04 Lebanon route:** second-rank applicability follows exact documentary route, never missingness.
- **A2-H05 WT/SAMP:** sample class cannot manufacture WT estimand/default use.
- **A2-H06 exact response binding:** source-authorized 8/9 and 99998/99999 may be bound only at their exact variable/question scope.

### ARAB5

- **A5-H01 ID collision:** ID and COUNTRY+ID cannot replace source-SHA+ordinal.
- **A5-H02 design missingness:** WT/PSU missing state cannot delete respondent or imply out-of-population.
- **A5-H03 dictionary tri-partition:** Q101 dictionary membership, observed incidence, and documentary semantic authority remain separate.
- **A5-H04 unobserved extras:** -9/-8/97 remain retained dictionary entries but cannot acquire response refs without new authority.
- **A5-H05 ranked pair:** Q2061A/Q2061B preserve rank and row association; Q2061B/97 remains exact variable-scoped authority.
- **A5-H06 split routing:** SPLITA/SPLITB domains do not create item applicability without exact join.
- **A5-H07 Unicode/storage:** literal UTF-8/storage continuation is preserved; no ASCII/normalization collapse.

### ARAB8

- **A8-H01 ID=0:** repeated zero IDs remain ordinary stored source values and cannot delete/merge rows.
- **A8-H02 empty BLOCK_ID:** `""` remains an R5 string/observed-storage state, distinct from system missing and null.
- **A8-H03 Q1/STRATUM nonalias:** identical vectors do not merge slot identity, dictionaries, or semantics.
- **A8-H04 Q622C topology:** documentary SELECT-ALL topology survives without invented native SPSS MR metadata.
- **A8-H05 route authority:** Q1A_PAL COUNTRY==15 and Q622C_IRQ COUNTRY==7 + SPLIT A are documentary gates; missingness/frequency cannot replace them.
- **A8-H06 design:** PSU's documented sampling-carrier role cannot inflate into a complete analytic cluster/strata/weight design.

## C. Future qualified-source tests

These must **not** be simulated as source-free proof:

1. freeze decoder-native type distribution and exact R5 physical-key domain for every runtime-admitted Arab slot;
2. prove exact source-SHA/reader configuration;
3. prove whole-source S35/R35 edge preservation, including non-target columns/carriers;
4. prove replay cardinality and exact source-row identity;
5. only then compare runtime rule physical keys with the observed governed key domain.

The failure mode for a missing source-backed proof is `REQUIRES_QUALIFIED_SOURCE_OBSERVATION`, not semantic inference.

## Required terminal for the test court

`PREMAIN_CLOSED35_CONTRACT_AUDIT_ARAB_R1__HOSTILE_TEST_PROTOCOL_AUTHORED__NOT_EXECUTED`
