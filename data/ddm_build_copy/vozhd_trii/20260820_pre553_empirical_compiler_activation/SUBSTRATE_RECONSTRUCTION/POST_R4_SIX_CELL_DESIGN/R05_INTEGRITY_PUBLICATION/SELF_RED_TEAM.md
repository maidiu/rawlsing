# R05 SELF RED TEAM — FAIL-CLOSED INTEGRITY / PUBLICATION

Verdict: `SURVIVES_CONDITIONALLY__LAZY_VERIFICATION_REMAINS_BLOCKED_UNLESS_QUERY_CLOSURE_IS_PROVEN`

## 1. ADVERSARY MODEL

Assume every optimization is hostile until it proves it cannot convert incomplete integrity knowledge into empirical certainty.

Adversarial conditions include:

- one corrupt byte in a cold or rarely read canonical member;
- stale but syntactically valid cache/index material;
- a query whose positive hit lies in a verified chunk while a refuting or denominator-changing event lies in an unverified chunk;
- a crash at every publication boundary;
- concurrent publishers racing to activate different complete releases;
- a mutable path changed after verification but before query interpretation;
- a valid cryptographic root that is not the organizationally authorized release;
- shadow and rollback carriers containing plausible but divergent truth;
- semantic-equivalent rebuilds whose Parquet bytes differ because the physical encoder is not byte-reproducible.

The design passes only if all such conditions either preserve exact results or block empirical output.

## 2. DEEPEST FAILURE MODE: MERKLE PROOF IS NOT QUERY SUFFICIENCY

The central attack against lazy verification is conceptual, not cryptographic.

A Merkle proof can establish:

`these selected bytes belong to this sealed root`.

It cannot by itself establish:

`these selected bytes are sufficient to answer this query`.

That second proposition requires a governed coverage proof. Without it, partial verification is merely authenticated partial observation.

Therefore `CHUNK_VERIFIED` never authorizes empirical output. The authorization state is `QUERY_CLOSED`: every canonical region capable of changing the answer has either been verified or excluded by a root-bound canonical completeness proof.

If a closure planner cannot prove this conservatively, the optimization loses. The system must verify a broader member/release or fail closed.

## 3. LAZY-VERIFICATION ATTACKS

| Attack | Why a naive design fails | Required fail-closed response |
|---|---|---|
| Verify only the chunk containing a positive hit | another unverified chunk can alter provenance/state/duplicate status/denominator | verify all dependencies that can change the emitted claim |
| Verify only chunks named by a stale bitmap | false-negative bitmap entries silently suppress lawful events | cache must over-approximate or canonical fallback must close omitted regions |
| Cache miss used as proof of no match | absence is inferred from non-authoritative material | reject negative answer until exhaustive/root-bound completeness closure |
| Hot tier verified, cold provenance not read | corrupt cold authority can change interpretation of hot values | cold remains canonical and enters closure whenever semantically relevant |
| Footer/metadata verified but data pages not | metadata authenticity is mistaken for member authenticity | verify exact consumed chunks plus closure or full member |
| One row group verified for a weighted aggregate | unverified weights/respondents alter denominator/estimate | close all contributing/excluding/reweighting regions |
| I05 pre-index contains no candidate | unforeseen lawful combination is suppressed by carrier designer | canonical exhaustive fallback or completeness-proven canonical index |
| Routing index says respondent inapplicable | stale cache changes risk set and negatives | routing authority must be verified canonically |
| Corrupt chunk lies outside first query | implementation continues serving unaffected queries | quarantine entire physical release after detected canonical corruption |

## 4. NEGATIVE EVIDENCE IS THE HARDER COURT

A positive atomic claim can sometimes be proven from a narrow verified dependency set.

An exact negative claim normally cannot. To say `no qualifying evidence exists`, every canonical region capable of containing qualifying/refuting material must be closed. Partition pruning is lawful only when the partition/completeness metadata doing the pruning is itself canonical, root-bound, and verified.

A Bloom filter, cache bitmap, materialized discovery table, previous query result, or mutable external index cannot prove absence. At most it may guide the order of canonical reads.

This same rule applies to:

- `0 support`;
- no respondent satisfying a conjunction;
- no admissible discovery candidate;
- no routed/applicable respondent;
- no sparse exception;
- no alternative source relation capable of changing a nonduplication judgment.

## 5. AGGREGATE / DENOMINATOR / UNCERTAINTY ATTACKS

The carrier can appear correct on sampled facts while corrupting aggregates through omission.

Hostile cases include:

- omitted physical missingness rows altering denominator law;
- stale routing/applicability changing risk sets;
- missing or corrupt weights changing estimates;
- lost design/cluster/stratum authority changing uncertainty;
- duplicate respondents or source relations counted twice;
- sparse override member omitted while defaults remain intact;
- one state-code mapping changed in a dimension while facts remain byte-valid.

Query closure must therefore be dependency-directed rather than `verify the file that returned rows`. Every canonical dependency that can add, remove, reweight, reroute, or reclassify a contributor belongs in closure.

## 6. TOCTOU ATTACKS

A verifier can hash a path and a query engine can later reopen that path. If mutation is possible between those operations, integrity is fake.

Rejected substitutes for byte identity:

- path equality;
- inode equality;
- file size;
- mtime;
- open file descriptor without storage guarantees;
- filesystem cache residency;
- object-store ETag without an explicitly governed algorithm/immutability contract;
- previous-process `verified=true` metadata.

Preferred proof: hash an immutable read buffer and interpret that exact buffer. If the execution engine cannot do this for sub-member reads, partial verification must be disabled and a full member must be authenticated before engine access.

## 7. CACHE LAUNDERING ATTACKS

The word `cache` is a common way to smuggle a second canonical database into a design.

A cache is disqualified if any is true:

- deletion changes an exact answer;
- it contains a fact not recoverable from the canonical root;
- a negative answer depends on trusting its completeness but its completeness is not root-bound;
- canonical corruption causes runtime fallback to cache;
- it is used to repair canonical disagreement;
- it is rebuilt from another cache rather than verified canonical material;
- its key omits a relevant root/member/schema/builder/configuration dependency;
- it remains trusted across a new process without re-establishing canonical integrity.

Canonical disagreement invalidates cache. Canonical corruption blocks evidence; cache cannot rescue it.

## 8. PUBLICATION / CRASH ATTACKS

### Before seal

Partial staging bytes must be invisible to readers and disposable after crash.

### After seal but before promote

A sealed candidate remains non-serving. Recovery may verify/reuse or delete it, but never infer authority from its mere completeness.

### After content-addressed promote but before selector swap

The candidate may exist as a complete inactive root. The old active root still serves. No mixed directory is visible.

### Selector update

The selector change must be atomic and compare-and-swap against the expected previous root. Concurrent publishers cannot both silently win.

### Same root already exists

If bytes/manifests are identical, publication is idempotent. If they diverge under the same `physical_root_id`, treat as catastrophic collision/integrity failure, never overwrite.

A storage backend unable to prove these semantics is not an acceptable publication substrate.

## 9. ROOT AUTHORIZATION ATTACK

Cryptographic integrity answers `what bytes are these?`; it does not answer `which valid root is authorized now?`

A malicious or stale release can be internally valid. Therefore selection by lexicographic filename, directory `latest`, newest mtime, highest local counter, or arbitrary discovered root is forbidden.

HQ synthesis must designate an explicit trusted active-root authorization mechanism. Its state is tiny control metadata, not empirical truth, but without it the integrity design authenticates the wrong question.

## 10. CORRUPTION-SCOPE ATTACK

A tempting optimization is to quarantine only the corrupt chunk and continue serving unrelated partitions. R05 rejects that default after detected canonical corruption.

Once a canonical member/chunk fails its promised root, the physical release no longer satisfies its integrity contract. The system is not entitled to assume corruption is locally bounded merely because only one mismatch has been observed. Entire-release serving is quarantined until deterministic rebuild or separately verified replacement is explicitly activated.

## 11. SHADOW / ROLLBACK ATTACKS

### Dual serving

If old and new carriers are both allowed to answer and runtime chooses whichever is faster/available, there are two empirical authorities. Rejected.

### Automatic fallback

If new canonical errors and runtime silently asks old canonical/shadow/cache, the old store is still canonical in practice. Rejected.

### Rollback target staleness

A previous root can rot while inactive. Explicit rollback therefore requires fresh integrity verification before atomic promotion.

### One-copy tension

Authority 44 forbids duplicate steady-state truth. Retaining a whole rollback candidate, even non-serving, may conflict with the intended storage law. R05 flags this for R06/HQ. If strict one-copy law controls, rollback must rebuild/restore deterministically rather than retain a duplicate carrier.

## 12. DETERMINISTIC REBUILD ATTACKS

Naive replay can accidentally bind:

- temporary paths;
- wall-clock timestamps;
- directory enumeration order;
- locale;
- process IDs;
- nondeterministic map/set order;
- unspecified compression/encoder defaults.

These must not affect semantic identity. Same governed inputs must reproduce the same logical member digests and semantic release/results.

Physical byte equality is separately governed. If a profile claims `BYTE_REPRODUCIBLE`, any physical-root drift is a failure. If it does not, byte-different roots still require explicit semantic equivalence proof before substitution.

## 13. CRYPTOGRAPHIC SCHEMA ATTACKS

A Merkle tree is unsafe if leaf preimages do not bind context. Reordering or transplanting equal byte chunks could then preserve leaf hashes while changing interpretation.

Required domain separation binds at least:

- leaf versus internal-node domain;
- member identity;
- chunk ordinal;
- offset;
- length;
- bytes.

Root/member canonical serialization and hash preimage rules must be frozen. The root cannot ambiguously hash a manifest containing its own final digest.

## 14. SELF-REJECTION CONDITIONS

Reject this R05 mechanism rather than weaken integrity if:

1. the query engine cannot ensure consume-after-verify identity;
2. dependency/coverage closure for exact queries cannot be conservatively expressed;
3. a speed index capable of false-negative suppression lacks mandatory canonical fallback;
4. negative answers require trusting a disposable cache;
5. storage publication cannot be made atomic/durable;
6. the active-root authority cannot be made explicit;
7. cache deletion changes correctness;
8. hierarchical verification would remove or weaken the current streaming full audit;
9. shadow/rollback requires simultaneous serving authorities;
10. measured Merkle complexity yields no useful reopen/query benefit.

## 15. RED-TEAM VERDICT

`CONDITIONAL_PASS_FOR_SYNTHESIS`.

The root/member/chunk integrity proposal itself is not the difficult part. The difficult part is proving the **coverage closure** of whatever is not read.

Therefore the final R05 law is deliberately hostile to lazy verification:

> authenticate selected bytes **and** prove that the selected region is sufficient for the exact empirical claim; otherwise verify more or emit no empirical claim.

No performance target overrides that rule.
