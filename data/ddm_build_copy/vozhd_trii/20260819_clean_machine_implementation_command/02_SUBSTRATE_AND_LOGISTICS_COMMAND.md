# 02 — SUBSTRATE & LOGISTICS COMMAND

## 1. Mission

The Data & Logistics command ensures every subsystem operates against one exact, frozen understanding of the incoming empirical substrate and one canonical physical representation of the distinctions Rawlsing must preserve.

The database is not an implementation afterthought. It is a governed physical representation of semantic distinctions.

## 2. Pre-implementation substrate gate

Before semantic-service implementation fanout, G2 must issue an `INCOMING_DATA_REALITY_AND_PHYSICAL_SUBSTRATE_CONTRACT` that answers mechanically, not narratively:

### Source identity

- What is a source family?
- What is a source instance/release/wave?
- What is an `EmpiricalUniverse`?
- Which identities are source-local versus globally canonical?
- What is required to assert semantic equivalence between source universes?
- What is required for respondent linkage?
- What is required for pooling/composition?

These are separate authorities by default.

### Respondent/event grain

- respondent identity and scope;
- event/response identity;
- repeated response events;
- multiselect incidence;
- ranking/order where supplied;
- component/subquestion identity;
- duplicate-row and correction/revision semantics.

### Question topology

- canonical question identity;
- source question identity;
- component identity;
- answer-option identity;
- multi-component topology;
- routing prerequisites;
- eligible/not-eligible/not-asked distinctions.

### Risk sets and routing

- exact risk-set identity;
- respondent membership representation or deterministic membership rule;
- routing/applicability authority;
- denominator semantics;
- distinction among not asked, ineligible, unknown, refusal, missing, structural zero, observed zero, and zero support.

### Weights / measures / estimands

- raw design weight identity;
- transformed weight identity;
- measure/estimand authority;
- weighted versus unweighted basis;
- design/version/source provenance;
- normalization/calibration authority;
- when equal numeric totals do not imply equal measure basis.

### Time

- source release time;
- wave/field period;
- respondent/event time where present;
- observation/effective interval;
- revision/system-validity time;
- unknown time;
- prohibition on hidden latest/nearest-time fallback.

### Provenance / replay

- source artifact identity/hash;
- ingestion authority identity/version/hash;
- exact transform version;
- content-addressable source retention or immutable resolver;
- historical authority binding;
- replay receipt relation to actual replay material.

## 3. Physical-schema requirements

The physical schema must be designed from canonical object/grain law, not inherited from convenient legacy table shape.

At minimum it must make first-class or exactly reconstructible:

- source universe;
- respondent;
- response event;
- question/component;
- coordinate/answer incidence;
- routing/risk-set membership;
- weight/measure basis;
- temporal coordinate;
- typed raw and normalized negative/absence state;
- authority snapshot;
- exact provenance edge;
- immutable content identity.

No column may silently carry several incompatible semantic roles because legacy input happened to overload it.

## 4. Database invariants

G2 must publish enforceable rules for:

- primary keys / uniqueness;
- foreign/reference integrity;
- content hashing;
- source-scoped versus global identifiers;
- immutable versus append-only material;
- revision lineage;
- duplicate handling;
- nullability and typed absence;
- schema versioning;
- transaction/atomic ingestion boundaries;
- deterministic canonicalization;
- index strategy needed for exact governed queries;
- migration/backfill receipts.

## 5. No silent normalization

Every source-to-canonical transformation must declare:

- original field/value;
- canonical field/value;
- authority/rule;
- information discarded, if any;
- whether the transform is reversible;
- whether discarded information is retained in source-native material;
- whether canonical hash includes the transformed or native representation and why.

Defaulting before validation is forbidden unless an authority explicitly defines that default as semantic meaning.

## 6. C11 physical carrier relationship

The final C11 carrier remains governed by accepted D13/D15 law. The implementation court may choose physical storage/codec/indexing only after proving that the physical representation preserves C11 M01-M18 and all later accepted requirements.

The physical store must not confuse:

- canonical semantic material;
- index;
- cache;
- denormalized acceleration copy;
- migration adapter;
- source-native retained evidence.

Cache or index loss may cost performance. It may never cost meaning.

## 7. Schema-change request

If a worker needs a substrate change it must file a `SUBSTRATE_CHANGE_REQUEST` containing:

- requesting worker;
- current contract version;
- exact missing capability;
- proposed semantic distinction;
- proposed physical representation;
- affected tables/objects;
- affected hashes/identities;
- affected producers/consumers;
- migration requirement;
- replay implication;
- golden-fixture update requirement;
- whether current work can continue safely without the change.

G2 + G3 + G6 adjudicate; Campaign Vozhd resolves cross-domain disputes.

## 8. Logistics acceptance gate

No semantic service may be declared implementation-ready until it can name:

- exact substrate contract version;
- exact input grain(s);
- exact query/read pattern;
- exact output object contract;
- required transaction/replay assumptions;
- every typed absence it may observe;
- every source-universe relation it relies on.

Any `unknown but probably obvious` answer is a block, not an invitation to guess.
