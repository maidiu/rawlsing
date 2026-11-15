# M01 -> M1 Interface Receipt

## Boundary

The M1 production runtime does **not** import `pre553_route_b_production`.

That is deliberate.

M01 remains the owner of selected-B execution packaging. M1 accepts exact empirical/discovery objects at its own jurisdictional boundary.

The neutral adapter:

`build_m1_adjudication_input_bundle(...)`

accepts exact object catalogs plus caller-selected DiscoveryResultReceipt objects. It resolves only exact refs from those receipts and builds the closed M1 input bundle.

It does not:

- call M01;
- execute I03;
- execute I05;
- infer a claim family from discovery rule names;
- infer source meaning;
- infer validation criteria;
- infer currentness.

## Source-free M01 interface proof

The hostile suite calls the already-current synthetic M01 compositor fixture, receives its exact:

- DiscoveryResultReceipt;
- DiscoveryAuthority;
- EmpiricalFact;
- EmpiricalQuerySpec;
- EmpiricalPredicate;
- AuthoritySnapshot;
- C11 release identity;

and then supplies those objects to M1 through the neutral bundle builder.

The M1 adapter follows selected receipt refs to recover only the required exact preimages:

1. receipt -> discovery authority;
2. receipt empirical/validation fact refs -> exact facts;
3. receipt winning predicate -> exact predicate;
4. candidate query roles -> exact query/predicate preimages;
5. fact query/predicate refs -> constitutive query/predicate preimages;
6. exact frontier and discovery replay refs are copied into the bundle;
7. exact AuthoritySnapshots are carried for closure verification.

The resulting `M1AdjudicationInputBundle@1.0.0` is then independently verified by M1 before rule dispatch.

## Non-ownership theorem

M01's I05 `rule_id`, I05 validation result, support level, exact replay closure or complete frontier do **not** select an M1 validator.

The acceptance proof explicitly shows:

- valid M01 output;
- supported exact evidence;
- complete replay;
- no M1 family rule binding;

produces:

`BLOCKED__MISSING_FAMILY_VALIDATION_RULE_AUTHORITY`

Therefore:

`M01_EVIDENCE_GRAPH != M1_SUBSTANTIVE_ACCEPTANCE_AUTHORITY`

and:

`I05_DISCOVERY_RULE != M1_FAMILY_VALIDATION_RULE`.
