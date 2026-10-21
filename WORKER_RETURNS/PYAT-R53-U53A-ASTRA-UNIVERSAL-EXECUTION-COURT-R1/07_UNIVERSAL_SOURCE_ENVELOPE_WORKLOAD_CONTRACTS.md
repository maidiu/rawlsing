# Proposed contracts — NOT ADOPTED / NOT EXECUTED

These are extension contracts for existing B49/G50/U43/native owners. They are not a new empirical engine. Exact implementation compatibility remains subject to the unresolved court frontier.

## 1. Input separation

SourceEnvelope@proposal1:
- identity: original SRC id, dataset identity, family, canonical wave plus authority-bound aliases, edition, byte digest, country/shard, release/instrument version and decoder configuration.
- access: authenticated decision ref, issuer identity, host, purpose, export scope, effective interval, revocation/current selection; TEST_ONLY has a disjoint namespace and never resolves as original.
- instrument: complete source-native occurrences with item/option/repeat/form keys; separately typed target, conditioner, design, identity and administrative roles. Include inventory completeness evidence and gaps.
- units: source respondent namespace, sampling unit, person/household/reporting role, authorized links, form/routing/risk applicability, and explicit nonresponse versus not-administered.
- measures: RAW versus governed population target, estimand, weight/design/strata/cluster/covariance rules and uncertainty; zero weights and missing weight states are explicit.
- clocks: observation/reference time, release time, as-of selection time and permitted comparisons.
- semantics: exact source-specific authority refs, response domains/state mapping, MR/rank/repeat topology, source relations and consumer-use limitations.

No defaults may assert LiTS, adult identity, scalar topology, population weighting or source time. Shape normalization preserves semantics; it never manufactures them. Null original U/E_pre means incomplete knowledge/issuance, not an empty instrument.

## 2. Prospective compiler

Normalize SelectedSourceRulePackage + governed instrument into a SourceDecisionBundle using occurrence identity, not only column name. Inherited rule candidates and observed data values cannot certify the universe. Context/age/position exclusion from attitude targets must not erase governed conditioner roles.

Compile the full finite universe authorized by GrammarPolicy:
1. Validate exact inventory/policy identity and grade; freeze without reading response values.
2. Enumerate authorized target tuples, ordered when semantics require; conditioner tuples over frozen domains, permissible forms, units and common risk sets. Apply issued class, arity J, conditioning K and recursion D bounds; no hardcoded universal bounds.
3. Emit a stable operation identity for every considered candidate with disposition and reason. Missing native support retains the scientific operation as UNSUPPORTED_RUNTIME.
4. Retain obligations outside the finite release in a deferred-boundary record. Resource truncation is PENDING/UNKNOWN, never INAPPLICABLE.
5. Partition lazy/sharded execution by stable identities with an independently checkable total expected set/root and count. Resume cannot change the frontier.
6. Retain aliases without conflating different target direction, respondent grain, topology or baseline.

Operation identity binds source/instrument/policy/grade, unit/risk/measure, ordered targets, ordered conditions and values, operation class, topology, state policy, recursion/baseline and clock/comparability references. Response observations do not determine membership. Physical artifact identity changes may change provenance roots; comparing mutations must distinguish stable logical grammar from legitimately changed byte identity.

## 3. Native lowering

Proposed owner extension:
lower_operation(bundle, policy, operation, native_capabilities) -> LoweringRecord

LoweringRecord = operation_ref + exact predicate/query/DiscoveryAuthority refs + expected candidate/query-role keys + Batch unit refs + lowering version + typed refusal + evidence-grade ceiling.

Reuse B49 catalog constructors, U43 NativeWorkload/IssuedWorkloadRecord, existing C11/Route B/I03/I05 and Batch APIs. Extend unary OperationFixture compatibly or add a typed n-ary companion. Every eligible supported operation needs semantic mapping to actual native evaluation roles; a many-to-one template requires an explicit surjective coverage witness from every operation to its adequate executed roles. Counting rules is insufficient. Never infer native inability solely from G50 native_map returning None; inspect the existing executor's expressive contract.

I05 exact-bounded discovery remains responsible for its declared frontier. U43's independent expected_jobs protects supplied jobs, but cannot certify that a dishonest producer supplied all eligible scientific operations. Bind the upstream expected frontier independently.

## 4. Execution, custody and consumer

Admission resolves current permission before source_factory and again around native work. Full output maps operation -> native candidate/query -> fact/typed negative -> validated/released product -> current/historical selection -> actual consumer values-read receipt. Preserve EMPTY, OBSERVED_ZERO, EMPIRICAL_NULL, DIFFUSE, UNKNOWN, HOLD, INAPPLICABLE_PROVED, ERROR and positive independently.

Cold resume must use authenticated existing fact/receipt custody. Current U43 refuses prior_receipts; do not advertise that ingress as cold-resumable until repaired/wired and tested. Investigate duplicate discovery in U43's unbounded Route B plus Batch path without changing empirical results.

C1/learned M1/M2/B5/I4 and E41 provide the next integration boundary. F5, F6 and F7 have separate typed source-indexed products and use decisions; world composition never constructs cross-survey respondents. N9 selects exact versions/as-of; N10E and N10W expose computed evidence to the existing permitted consumer. N11 joins source/operation and global F6/F7/F8 proofs. N12/Sorok remains external.

## Invariants

Independent expected operations = executed adequately + pending + held + unsupported + prohibited/inapplicable entries at the appropriate policy universe, with disjoint states, no duplicates and no unaccounted difference. A scoped execution subset may be complete as a subset while the universal product remains incomplete. All 35 SRC obligations remain present irrespective of permission. No 35-name synthetic run satisfies original acceptance.

## Revision 2 — binding contracts and falsification rules

This amendment supersedes any ambiguous state/identity wording above. Proposal only. Core evidence: E:empirical:531-625; E:j42:87-132,182-221,234-250; E:p41:124-185; E:e04:6-24; E:G50enum:44-84,106-246.

### Public boundary and ownership

`compile_universal_workload(envelope, instrument, grammar, capability_catalog) -> WorkloadCompilation` is the proposed single source-independent entrypoint in rawlsing_next/pre553_universal_workload.py. It delegates existing corpus selection, C11 projection, G50 enumeration and native binding. No source-specific operation-list argument. Adapters may supply source-semantic inventories and authorized policies, not choose the easiest emitted operations.

`WorkloadCompilation` contains schema/version, exact input refs, immutable logical frontier root, physical provenance root, complete operation disposition index, lowering coverage multimap, issued-workload preimage, pending schedule and typed unresolved edges. Its construction issues neither source rights nor original E_pre. Issuer remains external; U43 admission consumes an independently authorized issue record.

`resolve_empirical(request: EvidenceRequest, registry) -> EvidenceResult` and `reduce_required_support(results) -> SupportSummary` are separate provider duties. J42/P41 must call or validate these boundaries. A cache lookup by target/depth is forbidden. A stored slice is usable only if the full request key and permission/clock checks pass. Candidate-provided hashes without resolved objects are insufficient.

### Exact identity that must be conserved

EvidenceRequest key K = schema + claim grade + source/dataset/wave/edition/digest + instrument version + occurrence identity (item, option, form, repeat) + sampled/reporting unit and lawful link refs + applicability/risk/predicate identity + ordered target tuple + ordered condition tuples (occurrence, typed value, domain/state version) + operation class/arity + sample/population estimand + weight/design/uncertainty method refs + direction/role/consumer-use authority + grammar/model version + release/custody + observation/reference/as-of/publication clocks.

K is computed with a versioned canonical encoding: tagged scalar types, explicit null versus absent, deterministic object keys, preserved semantic order, no float/string coercion. Sort only sets declared unordered by the owner. Preserve both logical identity and byte provenance; a legitimate bijective label rename changes physical refs but must produce equivalent logical operations and values under the supplied bijection.

For progressive prefix i, actual evidence must bind K(request prefix i), not just i. Verify requested and returned target, conditions AND values, source edition, risk, role, model, design and clock. Any mismatch => IDENTITY_MISMATCH with evidence=null and no exact-support label. Missing object/unresolved refs => UNKNOWN/HELD, not a best-match fallback. Mixed sources require an explicitly governed F6 relation; they never become a same-person joint by hash concatenation.

### Total states and consumer reduction

Separate three axes: eligibility {ELIGIBLE, PROHIBITED, INAPPLICABLE_PROVED, HELD, UNKNOWN}; execution {NOT_STARTED, PENDING, COMPLETED, UNSUPPORTED_RUNTIME, ERROR}; result {SUPPORTED, OBSERVED_ZERO, VALID_NULL, DIFFUSE, VALID_EMPTY, ZERO_SUPPORT, UNSUPPORTED, UNKNOWN}. Preserve exact upstream native states in addition to normalized categories. A single enum that conflates these axes is forbidden.

| Required input | Provider and aggregate consequence |
|---|---|
| All exact supported steps; validated structural state | Productive at its declared TEST_ONLY/original grade |
| Supported distribution with observed zero cell | Keep supported denominator and zero cell; no missingness fabrication |
| Scientifically valid null/diffuse result | Preserve computed product and uncertainty; not runtime refusal |
| Zero denominator / ZERO_SUPPORT | Typed no empirical support; no productive all-support aggregate |
| ROUTING_UNKNOWN, unsupported, missing state | Explicit partial/unknown/refusal; never EXACT_SUPPORT_ON_CONDITIONED_RISK_SET |
| Identity/permission/clock conflict | Fail closed before value serving; no positive cache replay |
| No operations with independently valid complete empty frontier | VALID_EMPTY, not invented positive/filler |
| Budget exhausted or interrupted | PENDING with remaining exact IDs; cannot be INAPPLICABLE or complete |

Aggregate completeness is an AND over required identity and support predicates. Optional channels may remain partial only if the response explicitly scopes its positive claim and lists missing obligations. Repair J42 aggregate and P41 summary at their owners; retain unchanged E04 as the baseline endpoint. Passing a different default E04 call alongside a requested C progressive result is not an end-to-end proof for C. Future integration must supply a consumer-visible request-to-values-read association; where the consumer API has fixed semantics, declare and test those fixed semantics rather than inventing arbitrary-condition coverage.

### Occurrence and prospective inventory

Reject ambiguous duplicate occurrence keys before dictionary construction. Legitimate repeat/form occurrences need distinct qualified keys and distinct accounting. Explicit administered=False cannot yield eligible executed work for that occurrence. Unknown administration must remain unknown. Administered but all-missing response data must not shrink the prospectively frozen eligible frontier; its native result can be typed no-support/missing. Held semantics need a structured owner reason bound to the affected occurrence/operation; free-text held labels do not authorize exclusion.

Direction is an explicit decision over exact target/condition roles and use; literal Y has no scientific meaning. Source-wide permission never substitutes for direction, temporal comparability or structural-use decisions.

### Conservation and capacity

Maintain two independently auditable partitions: considered scientific universe = eligible + prohibited + proven-inapplicable + held/unknown; eligible workload = adequately completed + pending + runtime-unsupported + errored. Preserve operation multiplicity, exact IDs and lineage. Runtime failure cannot rewrite eligibility. Each many-to-one native template must prove adequate target/condition/query-role coverage for every mapped operation.

Enumerate lazily with deterministic partitions from an immutable policy. Report estimates from measured branching/cardinality and pilot runtime; cap concurrency/memory/checkpoint interval explicitly. Resource constraints cannot silently lower J/K/D or skip complex shapes. Admission permission is revalidated on cold replay and before consumer release. Receipt dedup keys bind operation, native owner, version and authorized attempt lineage; repeated computation and duplicate scientific counting are separate quantities.
