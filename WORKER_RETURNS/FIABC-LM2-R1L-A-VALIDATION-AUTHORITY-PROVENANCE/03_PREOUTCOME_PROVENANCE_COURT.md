# FIABC-LM2-R1L-A — Validation-Authority Provenance Court

## Holding

**PASS.** The three validation kinds used by the frozen WVS 46-candidate grammar already have independent pre-outcome authority. The R16 defect is:

`INCOMPLETE_SERIALIZATION_OF_ALREADY_FROZEN_AUTHORITY`

not:

`NEW_AUTHORITY_PREMISE_REQUIRED`

This court does **not** repair the authority.

## Why grammar use is not being mistaken for authority

The grammar's use of a token is evidence of intended serialization, but is not treated as self-authorizing. The independent chain is:

1. The accepted generic PRE553 I05 contract defined the validation semantics and admission guard before the P2 court.
2. HQ Lock1 froze the four WVS program families and required construction using the current accepted PRE553 I05 exact-bounded constructors.
3. EE-P2F1 separately audited **R12 support/validation rules and HQ competence** and classified it `B__SEMANTIC_AUTHORITY_EXISTS__PRE553_ISSUANCE_OR_BINDING_ONLY`, supported by Lock1 (I01) plus the accepted I05 contract (I08).
4. HQ adopted that decomposition as **14 B rows / 0 new authority**, expressly calling the deficit authority-form/exact-binding rather than missing semantics.
5. EE-P2F2 was then commissioned to issue R12 exact support/validation bindings with **zero new semantic proposition** and to use current accepted constructors without inventing validation semantics.
6. P2F2 issued the positive `EE-P2F2-WVS7-LOCK1-DISCOVERY-FRONTIER` AuthoritySnapshot for `pre553_discovery_exact_execute` over `DiscoveryAuthority@1.0.0` / `DiscoveryResultReceipt@1.0.0`.
7. The P2F2 issuer hard-coded the exact three validator names into the frozen grammar and compiled candidate identities before any WVS outcome access. It simultaneously omitted those names from the separate local `DiscoveryAuthority.validation_rules.kinds` envelope.

Thus the grammar is not the authority parent. It is the exact frozen child whose intended validation set can be checked against an already-existing authority chain.

## Generic I05 lineage

The path history for `rawlsing_next/pre553_discovery_exact.py` has two relevant pre-P2 commits:

- `8a3382d9de7ce38591f92e3a09481b38198a106c` — 2026-08-20 16:06:13Z, “Implement PRE553 I05 exact-bounded autonomous discovery”, blob `bfc8c560f7e2584c158d908b5fabfd0f889499fd`. It introduced `DISTRIBUTION_DIFFERS_FROM_BASELINE`, `JOINT_NOT_PRODUCT_OF_MARGINALS`, their evaluator semantics, the candidate grammar validation contract, and the fail-closed `validation_rules.kinds` admission guard.
- `6a75433b9a12b66e75f1def97f69163587970fd1` — 2026-08-20 16:14:10Z, “Complete I05 higher-order configuration frontier coverage”, blob `b2b99460cc5991bc26aa2ffe5bda129b408fc197`. It added `TARGET_CELL_SUPPORTED`, made `BASE_QUERY` require it, and added its exact evaluator.

P2F2 used that exact completed blob `b2b99460cc5991bc26aa2ffe5bda129b408fc197`; the generic admission guard was already present. No validator was invented by P2F2 or by R1K.

## Per-kind court

### TARGET_CELL_SUPPORTED

**Definition.** `_target_cell_supported` returns true only when the exact target cell has positive count under a positive denominator in at least one returned fact.

**Constructor binding.** `BASE_QUERY` hard-requires this kind. In the frozen WVS grammar it governs both `UNARY_SOCIAL_FORK` (10 candidates) and `BOUNDED_K_WAY_RESPONSE_CONFIGURATION` (25 candidates).

**First introduction.** `6a75433...`, 2026-08-20, before Lock1/P2F1/P2F2 and before any final-court WVS outcome access.

**Authority parent.** Accepted I05 contract I08 + Lock1 I01, expressly joined by P2F1 R12 and adopted by HQ; exact P2F2 DISCOVERY_FRONTIER later scopes the operation.

**P2F2 intent.** Frozen explicitly in issuer rules `R08_UNARY_Q0`, `R08_UNARY_Q1`, `R08_JOINT_5X5` and in compiled candidate identities.

**New premise if enumerated in `validation_rules.kinds`?** No.

### JOINT_NOT_PRODUCT_OF_MARGINALS

**Definition.** `_joint_dependence` uses exact counts and denominator cross-products to test whether any observed joint cell rate differs from the product of its marginal rates, with exact scope and zero-support guards.

**Constructor binding.** `JOINT_DEPENDENCE` hard-requires this kind. In the WVS freeze it governs the one `PAIR_RESPONSE_COTRAVEL` candidate.

**First introduction.** `8a3382d...`, 2026-08-20.

**Authority parent / P2F2 intent / new-premise holding.** Same independent chain above; explicitly frozen in `R08_PAIR_COTRAVEL`; adding it to the local allowed-kind envelope adds no new proposition.

### DISTRIBUTION_DIFFERS_FROM_BASELINE

**Definition.** `_distribution_differs` compares conditioned and baseline exact cell distributions using cross-multiplied counts after requiring identical source scopes and compatible measures.

**Constructor binding.** Normal branch candidates hard-require this kind. In the WVS freeze it governs the 10 `BRANCH_CONDITIONED_DISTRIBUTION` candidates.

**First introduction.** `8a3382d...`, 2026-08-20.

**Authority parent / P2F2 intent / new-premise holding.** Same independent chain above; explicitly frozen in `R08_BRANCH_Q0_TO_Q1` and `R08_BRANCH_Q1_TO_Q0`; adding it to the local allowed-kind envelope adds no new proposition.

## P2F1/P2F2 provenance

P2F1's authority inventory identifies:

- `I01_LOCK1_WVS_SOURCE_AND_PROGRAM_FREEZE` as possessing the four families, 46 shape, complete-frontier/no-pruning/raw law; and
- `I08_PRE553_I05_EXACT_BOUNDED_CONTRACT` as possessing exact-bounded support/validation invariants and deterministic candidate identity law.

Its R12 crosswalk joins **I01 + I08** and says `MECHANICAL_ISSUANCE_BINDING_ONLY`. HQ then adopted P2F1 as `ADOPTED_PASS__MECHANICAL_PRE553_ISSUANCE_ONLY`.

P2F2's commission says R12 is “exact support/validation-rule bindings required by the frozen exact-bounded program,” forbids inventing validation semantics, and permits PASS only with zero new semantic proposition. Its issuer then reported R12 PASS.

This is stronger than post hoc inference from the candidate grammar.

## Exact defect

P2F2's `DiscoveryAuthority` hash:

`24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`

embeds grammar:

`a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6`

whose exact rules use all three kinds. But its `validation_rules` contains only:

- `exact_authority_closure_required`
- `exact_universe_scope_required`
- `unresolved_predicate_or_query = REJECT`

and omits `kinds`.

The generic I05 executor compiles the frontier, computes `used_validation`, reads `validation_rules.kinds` (default empty), and fail-closes unless `used_validation <= allowed_validation`. R1K therefore blocked lawfully.

## Identity consequence

`DiscoveryAuthority.validation_rules` is a required semantic field. Canonical PRE553 identity hashes all semantic fields through `semantic_projection()`. Therefore any future exact repair must reissue the DiscoveryAuthority identity and transitively dependent identities. That is a succession/invalidation issue, **not** evidence that a new authority premise is needed.

## Negative limits

This holding authorizes no fourth validation kind, wildcard, `ALL`, future validator, new family, candidate pruning, source-semantic change, empirical inference, or candidate execution. No dedicated standalone per-kind AuthoritySnapshot was found; the lawful parentage is the composite pre-outcome chain proved above.

Terminal:

`FIABC_LM2_R1L_A_PASS__THREE_VALIDATION_KINDS_HAVE_PREOUTCOME_AUTHORITY__DISCOVERY_ENVELOPE_OMISSION_IS_REPAIRABLE`
