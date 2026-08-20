# PRE553 P04 — Migration Rules

These rules govern the P04 current-producer compatibility prerequisite consumed by I04. They are admission rules, not adapter implementation.

## 1. No carrier is admitted by ancestry

A V550, V550J, V551, V551J, V552, V552J or R1 artifact is not PRE553-compatible merely because its family is historically upstream, its schema parses, its path exists, or its fields resemble a current object. The migration unit is semantic meaning under exact authority, not artifact class.

## 2. Required proof chain

For each candidate migration object, I04 must establish all applicable links below before admission:

1. **Carrier identity** — the concrete producer family/version/source is unambiguous.
2. **Authority identity** — exact bound contract, source, manifest or equivalent authority is present where required.
3. **Scope identity** — query scope, finite universe, partition/risk set and eligibility meaning are preserved.
4. **Measure identity** — variable, measure, weighting/estimand or other interpretation-critical meaning is preserved.
5. **Observation-state identity** — observed, not observed, missing, query failed, invalid, unauthorized and analogous states remain distinct where the producer contract distinguishes them.
6. **Value/state separation** — valid numeric `0` and valid Boolean `false` remain generated values and are never used as encodings for negative states.
7. **Source/provenance identity** — semantically relevant source identity and provenance are retained; provenance alone does not authorize composition.
8. **Artifact-class neutrality proof** — any change of carrier/artifact family is demonstrated to be nonsemantic for this object.

If any required link is absent, ambiguous, contradictory or unverifiable, the migration candidate is rejected.

## 3. V550/V551 bound semantics

The exact V550/V551 response-semantics binding at the accepted base is authoritative for the seam it covers:

`data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.manifest.json`

Contract `V550_V551_RESPONSE_SEMANTICS_INFRASTRUCTURE_SEAM_R1@v1`, SHA-256 `3a04a9e689b5d027e501a1cc165093773407338313feb25e86c2356ea752b704`, requires among other things:

- retrieval scope semantics limited to the bound `all`/`filtered` meanings;
- producer generation success before generated empirical meaning is claimed (`searches2_n >= 1` where applicable);
- generated statistical content rather than substituted constants;
- preservation of `ok`, `query_failed`, `missing`, `variable_present`, `not_observed` distinctions at the metric-source seam;
- no downgrade of a failure state to value `0`.

P04 does not extend this contract beyond the seam it actually governs.

## 4. J/non-J rule

No generic equivalence between a J family and its non-J namesake is asserted by P04. An adapter may collapse the artifact distinction only if it proves that the J-specific distinction contributes no semantic information to the concrete migrated object and that all source, scope, partition, variable/measure, observation and negative-state meanings remain identical.

Unknown equivalence is rejection, not permission.

## 5. V552 rule

P04 grants no blanket V552 or V552J carrier equivalence. A V552-family object is admissible only when its exact upstream empirical meaning can be proved through the PRE553 ingress without invoking V552 as a hidden live fallback and without reconstructing missing meaning from carrier shape, filenames, defaults or historical convention.

## 6. R1 finite-universe rule

R1 authority is exact rather than generic. For the released R1 authority examined by P04, admission requires the exact `ATP_W135` universe and its bound evidence:

- source file `ATP W135.sav`;
- source SHA-256 `6cec90ec72df360341236f7634d5d76c9a0604168d4174a03e8b8efd388bbbae`;
- authority manifest `22_shared_respondent_relation_manifest.R1.json`;
- manifest SHA-256 `84009652424d200ced06933173eb8b2f8fb89d51f7909d3da40f6f59ad5da9d9`;
- exact respondent-key set and relation/authority tuple;
- source-backed respondent linkage;
- fail-closed source-level exclusions.

A different study, widened source universe, row-order-derived respondent identity or merely similar manifest is not this R1 authority.

## 7. Retired-runtime prohibition

Compatibility permits **migration of meaning**, never revival of a retired runtime carrier. Therefore I04 must reject any implementation that:

- calls V550/V551/V552 as a hidden fallback when PRE553 current ingress cannot resolve a candidate;
- reads active V558 metadata/repository state as current empirical runtime context;
- chooses a retired path because it happens to produce an answer;
- repairs missing semantic bindings by `latest`, filesystem ordering, filename resemblance, fuzzy matching or model judgment.

## 8. Negative-semantics rule

The following classes are never interchangeable merely because a downstream consumer could map each to a falsey value:

- generated zero;
- generated false;
- unknown;
- invalid;
- missing;
- not observed;
- query failed;
- not authorized;
- absent;
- source/universe mismatch;
- parity not proved.

The producer's exact state vocabulary controls where a finer distinction exists. PRE553 may normalize representation only after proving preservation of meaning.

## 9. Deterministic decision procedure

For each candidate, evaluate in order:

1. Is carrier identity exact and unambiguous? If no: `REJECT_AMBIGUOUS_CARRIER_IDENTITY`.
2. Is required source/contract/provenance authority exact? If no: `REJECT_PROVENANCE_MISMATCH` or `REJECT_SOURCE_UNIVERSE_MISMATCH`.
3. Are scope/universe/partition semantics preserved? If no: `REJECT_SCOPE_DOWNCAST` or `REJECT_SOURCE_UNIVERSE_MISMATCH`.
4. Are negative states preserved distinctly from valid zero/false? If no: `REJECT_NEGATIVE_SEMANTICS_COLLAPSE`.
5. If carrier/artifact class changes, is semantic parity proved? If no or unknown: `REJECT_UNPROVEN_PARITY`.
6. Does resolution require a retired runtime fallback? If yes: `REJECT_RETIRED_RUNTIME_FALLBACK`.
7. Does resolution require active V558 as current runtime context? If yes: `REJECT_V558_CURRENT_RUNTIME_FALLBACK`.
8. Otherwise admit under `ADMIT_EXACT_PARITY`, or `ADMIT_R1_EXACT_AUTHORITY` for the exact R1 finite-universe authority.

No later step may override an earlier rejection.

## 10. Scope of this return

P04 changes no runtime, launcher, IO policy, producer or downstream interface. The adapter remains I04 work. I04 must make its implementation mechanically conform to `CURRENT_PRODUCER_COMPATIBILITY_MATRIX.json`; it may narrow admission further, but it may not widen it by inference.
