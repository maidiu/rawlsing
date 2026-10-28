# M26 — stored-versus-derived separation

**Court:** HISTORICAL_V3 / EXACT_MECHANISM. **TD-R05 historic audit:** REUSE_UNCHANGED_IF_FULLY_COMPATIBLE. **New Neo transposition:** PROVISIONAL / NOT ACCEPTED. **Historical source provenance:** blob dfcc7e4fc7b6e907218d7a368ceb9d269a49206d. **Current person consumer:** UNTRACED_UNLESS_SEPARATELY_PROVED. **Worker:** UNASSIGNED or mapped first-wave court; see flight board.

## 1. Located original source and functions
`v3/core/state.py; v3/core/derived.py; v3/core/invariants.py; v3/tests/test_architecture_invariants.py` — `DerivedIndices; compute_all_derived; assert_no_derived_fields_in_backbone; test_no_derived_fields_in_backbone_state`

This is the original *historical V3* function inventory. Source identity and behavior attested by TD-R05 original direct-source investigation, not fresh direct reading of this code in the foundation agent.

## 2. What historic source was found to do
The separation is explicit and test-protected.

## 3. Difference from what Neo-V3 requires
Derived quantities must not masquerade as stored causal truths; this is broadly compatible.

## 4. Initial retained/adapt/replace/create disposition (nonissuing)
**REUSE engineering invariant**: pure derived projections with exact dependencies, versioned owners and no hidden memory writes.

## 5. Current bidirectional cross-links
- N11
- N12

## 6. Deepening workload
01_DIRECT_SOURCE_MAP.md: code line/function exact inputs, params, defaults, outputs, read/write, callers/callees and test entry.
02_PHENOMENON_AND_CAUSAL_CLAIMS.md: the actual psychological/social phenomenon and warrant vs mere numeric convenience.
03_DIFFERENTIAL_REQUIREMENTS.md: Nxx→existing/partial/unwired/missing and semantic conflict.
04_FORMAL_OPERATORS_AND_GATES.md: candidate full operators and scoped NO_CHANGE/contradiction/alternative.
05_IMPLEMENTATION_PLAN_AND_SEAM.md: only after theory, owner/rule and source access settled, exact changed/new functions and first consumer.
06_COURT_RETURN.md: immutable branch/commit, court triplet, independent falsifier, next finite action.

**Do not** fill these deepening files with empty green placeholders. Distinguish archived historic tests from current import, native rule or original-grain person proof.
