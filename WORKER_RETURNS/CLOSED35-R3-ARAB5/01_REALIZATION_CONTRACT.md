# CLOSED35-R3-ARAB5 — Realization Contract

Schema: `CLOSED35_R3_ARAB5_SOURCE_REALIZATION@1.0.0`

Semantic owner: `ARAB5_SEMANTIC_OWNER_V1`

## 1. Court object

This contract defines one candidate-neutral source-specific realization for the exact canonical source:

`Arab Barometer Wave 5.sav`

SHA-256:

`6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc`

It does not execute the source. It freezes semantic and replay law so that later Candidate A/B/C physical strategies cannot manufacture different Arab5 meanings.

## 2. Source and replay identity

Accepted source mode: `SAV_NATIVE_GOVERNED`.

Source-declared text mode: UTF-8 / character code 65001.

Hard replay identity:

`SOURCE_SHA256+ROW_ORDINAL`

Accepted Authority71 evidence records native `ID` collisions, including three remaining duplicate `COUNTRY+ID` pairs. Therefore:

- `ID` is a source attribute, not a hard replay key;
- `COUNTRY+ID` is also not a hard replay key;
- no deduplication, row merge, or replay-key replacement may be inferred from apparent identifier fields.

## 3. Physical versus semantic state

Physical state and semantic meaning are separate jurisdictions.

WT and PSU are physically present carriers and accepted packet evidence records SYSTEM_MISSING cells in each. That fact means only that the physical cell is system-missing.

It does not mean:

- the respondent row is invalid;
- the row must be dropped;
- the case is outside a target population;
- a PSU or stratum may be inferred;
- WT should be imputed;
- WT is the default analytical weight;
- any specific survey-design estimator is authorized.

Rows remain replayable by source SHA + row ordinal regardless of design-carrier missingness.

## 4. Design and weight carriers

Preserve individually:

- `WT`
- `PSU`
- `STRATUM`
- `SAMPLE`
- `MODE`

Current authority does not close the exact analytical/design role, estimand, normalization, or lawful combination of these carriers.

Accordingly, each analytical role is `BOUNDED_UNKNOWN`.

The source field name is physical metadata. It is not sufficient authority for a survey-design operation.

No default weight exists in this realization.

## 5. Q101 dictionary identity

The accepted exact-snapshot packet establishes a Q101 source dictionary containing:

`-9,-8,1,2,3,4,97,98,99`

Accepted observed-code incidence is:

`1,2,3,4,98,99`

Accepted extra unobserved dictionary entries are:

`-9,-8,97`

The questionnaire lists codes `1..4,98,99`; it does not authorize the extra `-9/-8/97` entries as current Q101 response semantics.

Therefore the realization distinguishes four questions:

1. Is a code in the source dictionary?
2. Was the code observed in the accepted snapshot?
3. Is the code documentarily listed for Q101?
4. Is an exact semantic label authorized?

Those questions must not be collapsed.

For `-9/-8/97`:

- source dictionary membership = true;
- accepted observed incidence = false;
- documentary Q101 membership = false at the inspected questionnaire authority;
- semantic status = `BOUNDED_UNKNOWN`.

The codes remain in the dictionary. They may not be pruned merely because unobserved. They also may not be promoted into substantive/current response meanings merely because present in metadata.

## 6. Ranked challenge topology

Q2061A and Q2061B form an ordered documentary structure:

- Q2061A = rank 1 / most important challenge;
- Q2061B = rank 2 / second most important challenge.

The source-native questionnaire also documents Q2061B code 97 as "There is no second problem".

The ordered pair is not an unordered set and not an inferred native SPSS MR set.

Accepted packet evidence records zero native SPSS MR sets for the snapshot. That physical fact does not erase documentary ranked topology.

A candidate must preserve exact slot identity, rank, multiplicity, and row association.

## 7. Split and routing topology

Preserve the split carriers separately:

- SPLITA documentary assignment domain: 1/2;
- SPLITB documentary assignment domain: 1/2/3.

The source-native questionnaire documents random assignment and item-specific programmer gates.

The current realization does not manufacture a universal item-routing table where an exact carrier-level join was not closed.

Therefore:

- split-carrier existence and assignment domains are governed;
- item-level routing requires an exact documentary join;
- unresolved item routing remains `BOUNDED_UNKNOWN`;
- SYSTEM_MISSING or observed/nonobserved incidence cannot itself supply routing authority.

## 8. Unicode and storage continuation

The source is governed as UTF-8.

Accepted Authority71 evidence includes a literal Unicode cell witness in `E2001B` and a storage-continuation witness for that width-21 logical variable.

The realization preserves literal Unicode strings exactly. No normalization step is authorized merely to make text "cleaner", more comparable, ASCII-safe, or cross-wave consistent.

Readable decoded text is still source text. Readability does not turn it into extra documentary semantic authority.

## 9. Cross-wave noninheritance

Arab Barometer waves exhibit documented schema/coding/design drift.

This realization therefore rejects semantic import from Wave 2, Wave 8, or any family-global same-name/same-number rule unless separately governed.

In particular:

- Wave-2 Q101 code law does not fill Wave-5 Q101 extra codes;
- another wave's weight role does not define Wave-5 WT;
- another wave's routing cannot fill Wave-5 item applicability;
- matching labels or question numbers do not establish longitudinal equivalence.

## 10. S35 edge bindings

Exact accepted edge set:

### EC01 — format family

Preserve exact source root, variable incidence/order, raw storage values, physical metadata, and source-row replay identity.

### EC05 — physical missingness multiclass

Preserve SYSTEM_MISSING separately from ordinary stored values and separately from semantic response/routing states.

### EC07 — native-ID collision/noninjectivity

Native ID fields remain attributes. Source SHA + row ordinal remains the hard replay key.

### EC09 — ordered/repeated slot topology

Preserve Q2061A/Q2061B ordered ranks and multiplicity.

### EC10 — form/module/skip/routing carriers

Preserve SPLITA/SPLITB and other physical routing carriers without deriving applicability from missingness.

### EC11 — variable/dictionary identity noncollapse

Preserve Q101's complete dictionary even when some codes are unobserved or semantically unresolved.

### EC12 — weight/design multiplicity and domain

Preserve WT/PSU/STRATUM/SAMPLE/MODE as distinct carriers. No default selection, aliasing, normalization, or design role is inferred.

## 11. R35 physical hooks

I01 schema:

`PRE553_PHYSICAL_METADATA@1.0.0`

I02 schema for non-direct realizations:

`FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`

I03 schemas:

- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

Required physical dimensions include physical metadata, variable inventory/order, raw values, physical missing states/declarations, row replay identity, ranked topology, split/routing carriers, dictionary identity, and weight/design carriers.

R35 hooks have no semantic authority.

## 12. Candidate-neutral law

Future qualification order:

canonical source identity freeze

-> `ARAB5_SEMANTIC_OWNER_V1` freeze

-> independent A/B/C physical realization

-> R35 physical/provenance receipts

-> Arab5 hostile semantic court

-> common A/B/C comparison.

Candidate-specific semantic interpretation is nonconforming.

## 13. Fail-closed rules

Wrong source SHA:

`BLOCKED__CANONICAL_SOURCE_ROOT_UNPROVED`

ID or COUNTRY+ID promoted to hard replay identity:

`BLOCKED__REPLAY_IDENTITY_INVENTED`

WT/PSU/STRATUM/SAMPLE/MODE promoted to undocumented survey-design use:

`BLOCKED__DESIGN_AUTHORITY_INVENTED`

Missing PSU/WT used to drop rows:

`BLOCKED__PHYSICAL_MISSINGNESS_PROMOTED_TO_ROW_EXCLUSION`

Q101 unobserved dictionary entries pruned:

`BLOCKED__SOURCE_DICTIONARY_PRUNED`

Q101 extra dictionary entries given undocumented meanings:

`BLOCKED__UNAUTHORIZED_SEMANTIC_PROMOTION`

Unicode text normalized/lost:

`BLOCKED__SOURCE_TEXT_IDENTITY_CHANGED`

Q2061A/Q2061B flattened or reordered:

`BLOCKED__RANKED_TOPOLOGY_LOSS`

Routing inferred from missingness:

`BLOCKED__ROUTING_AUTHORITY_INVENTED`

Wave-2/Wave-8 semantics imported:

`BLOCKED__CROSS_WAVE_SEMANTIC_LEAKAGE`

A/B/C semantic owners diverge:

`BLOCKED__SEMANTIC_OWNER_DIVERGENCE`

## 14. Lawful bounded UNKNOWNs

The following are accepted governed states rather than blockers:

- exact weight estimand/normalization;
- exact PSU/STRATUM/SAMPLE/MODE analytical design semantics;
- exact treatment of missing WT/PSU in any later estimator;
- Q101 `-9/-8/97` semantic role/jurisdiction;
- item-routing rules not closed by an exact documentary join;
- cross-wave semantic equivalence.

## 15. Proof boundary

This contract is implementation law only.

It does not prove:

- real-source execution;
- whole-source physical equivalence;
- Candidate A/B/C execution;
- I05;
- measured P2X;
- source certification beyond accepted Authority71/72 and S35 evidence.
