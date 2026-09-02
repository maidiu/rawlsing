# FFIF013 — CHALLENGER GENERATION + OBJECT-GRAIN SPLIT RULES R1

Status: `DESIGN_ONLY__FINITE_CLOSURE_PREPARATION__NO_COCR_ISSUED`

## 1. Deterministic challenger generator

For frozen assertion bundle `A = {AS01..AS08}`:

### G1 — slot decomposition

For every assertion slot, list the minimum required capabilities:

- exact identity;
- support/state information;
- same-unit linkage if needed;
- external operand access;
- relation/query logic;
- exact status law;
- replay path.

Do not begin from historical representation families.

### G2 — commitment lowering

Starting from a claim-complete lossless same-unit capability, remove one commitment at a time where lawful:

- remove full-state retention while keeping predicate membership;
- remove local membership while preserving exact producer re-query;
- replace generic re-query with a query-specific exact sufficient statistic;
- remove follow-up-specific information and retain discovery support only;
- reduce replayable summary to final-answer cache to test `SAVED_RESULT != REPLAY`.

A projection survives as a challenger only if its semantics are explicit and it can be fairly adjudicated under the frozen claim.

### G3 — known Rawlsing challengers

Import claim-relevant known object specifications/capabilities from FFIF007 and the second-canary W1–W5 evidence where their exact commitment pattern maps lawfully onto this claim. Do not import geometry, motif, graph, or other families merely because they exist historically.

### G4 — fresh adversarial pass

Before output, a fresh reviewer must ask:

- can the final frozen assertion be banked without the statistic that generated it?
- can a query-specific exact contingency/sufficient-statistic summary answer the claim without membership?
- can producer-owned direct re-query reconstruct both predicate and follow-up operand without any local carrier?
- can exact predicate membership alone replace the full state carrier?
- is any proposed fusion merely a set/composition rather than a new AOS?

Any obvious lawful challenger discovered here must be included or explicitly disposed before target output.

### G5 — blocked challenger rule

If a known challenger would be claim-relevant and fairly executable on the same frozen empirical substrate but is blocked only by an **owed current** authority/substrate/execution dependency, closure must abstain:

`CLOSURE_ABSTAIN__KNOWN_BLOCKED_CHALLENGER`.

Do not prove a stronger object necessary by starving a weaker owed challenger.

### G6 — freeze

Freeze the ordered finite challenger universe, AOS identities, method-variant policies, blocked/excluded dispositions, dominance/weaker relation, query quantifier, and fresh-review receipt before any target follow-up output.

## 2. Object-grain hierarchy

Use:

`OBJECT_FAMILY -> ADMISSIBLE_OBJECT_SPECIFICATION -> METHOD_VARIANT -> EXECUTION_INSTANCE`.

The court member is the claim-scoped admissible object specification/capability, not a filename, SQL engine, dataframe, compression format, or one run.

## 3. Mandatory split rules

Create distinct AOS members before output when candidates differ in any of the following:

1. which AS01–AS08 slots are primitive, derived, or undefined;
2. exact semantic/relation commitment;
3. local respondent-membership retention versus no local membership;
4. direct producer dereference at query time versus self-contained local materialization;
5. exact recoverability/loss profile;
6. follow-up quantifier ceiling (`Q1`, declared `QF`, or broader separately authorized capability);
7. authority dependencies or permission requirements;
8. source-native ancestry ceiling;
9. whether final assertions, sufficient statistics, membership, or full states are retained;
10. inferential/status ceiling;
11. whether another stronger object is consulted at query time;
12. whether a fusion creates a new primitive relation rather than a union of interfaces.

Thus W1, W3, W4, and W5 remain distinct even if they happen to emit identical final tables.

## 4. Non-split rules

Keep candidates as one AOS with method variants when they differ only in:

- serialization/file format;
- row ordering under canonical key recovery;
- exact lossless compression;
- SQL versus dataframe versus in-memory implementation;
- index/cache layout that changes latency only;
- optimizer/solver/parallelization;
- equivalent deterministic query implementation;
- regenerated versus persisted bytes when exact identity, interface, authority, and replay law remain the same.

`INFORMATION_EQUIVALENT_ENCODING != DISTINCT_SEMANTIC_OBJECT`.

## 5. Weaker relation is partial, not total

Byte size and persistence duration do not define semantic weakness.

Examples:

- W3 may retain less respondent information than W1 yet be more target-specific and less extensible;
- W1 may persist nothing locally but depend on a stronger producer dereference permission surface;
- W4 may retain only predicate membership and therefore be strictly narrower than W5 in information breadth;
- W0 may serve an exact result while failing replay.

The court should use a partial dominance relation over constitutive commitments and assertion coverage rather than a single scalar “complexity” rank.

## 6. Fusion rule

A combination of W-members is a `SUFFICIENT_SET` when it merely unions independently authorized interfaces.

It becomes a separate AOS only if the fusion introduces a new primitive relation, learned bridge, semantic equivalence, query contract, or cross-object interaction. Such a fusion must be frozen before output. Post-output W6 resurrection is forbidden.
