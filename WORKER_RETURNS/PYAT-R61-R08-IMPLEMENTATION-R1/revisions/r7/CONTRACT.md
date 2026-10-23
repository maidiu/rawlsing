# R08 R7 pre-code contract

Authority: commission 37050d3f11b5dea155f418ce1cdb643753f20f1d;
binding R61AF e349da0d886d8e365648afccf40a2e6b8e105ff7; R61Q D1-D6;
R6 independent review c42b4abee4e54340659ec6b1f8f6760dfbef9411.
Startup d8a7b4005d23a1e39b35360ca96bf2aef5b9e591, clean assigned checkout and branch verified before reads/writes.
Requested route GPT-6.1 Sol HIGH; actual model/effort UNKNOWN to this worker (no independent runtime introspection). Author evidence only; distinct DeepSeek review required.

## Frozen normal form
Cache schema R61_AUTHENTICATED_EVIDENCE_CACHE@5. Cache owner descriptor schema
R61_CACHE_OWNER_DESCRIPTOR@1; top-level entry name cache_owner_descriptor.
Exactly six fields: schema, request_key, owner_identity_material,
owner_identity_hash, validated_conditions, descriptor_hash. descriptor_hash is
SHA256 canonical preceding five fields, never a signature or live binding_hash.
Exact owner classes (13): context_ref, context, actual_conditions,
producer_query_ref, predicate_ref, predicate_hash, release_refs,
consumer_query_ref, consumer_binding_fingerprint, model_rule_hash,
source_universe_ref, risk_set_ref, target_ref. No duplicated top-level owner
fields; no admission field/token. All mappings returned/stored detached.
Unknown fields refuse at cache/entry/descriptor/envelope owner boundary.

Legacy @4 and prior caches explicitly typed refuse; no automatic migration.
Nonempty legacy trusted_binding_hashes configuration explicitly typed refuses
cache operations as LEGACY_BINDING_PINS_REQUIRE_MIGRATION; it is never silently
ignored/reinterpreted. Add separately named trusted_descriptor_hashes for @1
read-only descriptor restrictions; enforce on export/import/replay. Existing
live binding_hash meaning remains unchanged.

## Shared checked projection and API coverage
One checked owner projection verifies the configured signature, full request K,
all owner/envelope duplicate associations, context/content refs, ordered typed
conditions, evidence/query/model identities, evaluator and signed result
projection. Export, import, verified replay and direct qualified reader use it.
Import stores detached authenticated descriptor plus detached objects and signed
execution; export never uses raw live binding material as transport truth.
Reader/evaluator object validation and result projection remain shared.
Replay/re-export requires verifier only, preserves original signature/mode,
never selects/invokes producer nor requires a new signing capability.
Qualified result-only reader omits unsigned local delivery label.

| API | Positive | Hostile obligation |
| --- | --- | --- |
| live bind/resolve | native 54/6/60; changed54/16/70 | wrong admission/root/callable pin; counter0 |
| export | signed canonical descriptor | corrupted retained result/object/owner state refuses |
| import | verifier-only exact replay | per-owner-class mutate/remove/duplicate/type alias; ordered reorder; recompute public hashes; admission/unknown/legacy refuse |
| read/replay | same consumer + unchanged evaluator | signed owner/envelope/K/source/query/rule disagreements; deep mutation refuses |
| re-export/second import | unchanged signature, original provenance | no ownership/capability propagation; descriptor pins enforced |
| cold process | first and second verifier-only chain | no verifier/wrong root/old version refuse |

## Qualification inventory and limits
Table-driven inventory from all 13 declared classes, not a single producer ref.
For each: independent mutate, removal, duplicate compatibility field, type alias;
reorder for ordered actual_conditions/release_refs where multi-entry exists.
Each attack gets independent pristine cache and recomputed public descriptor and
entry hashes, then import/read/re-export/second-import pathway. Restore original
positive after every attack. Signed internally inconsistent owner duplicates
also tested via trusted synthetic fixture issuance. Unknown owner/schema fields
and forbidden admission tested separately. Optional pins, wrong/missing roots,
legacy schema, deep mutation, swapped signed envelope, current/asof, bool/int/
null/order, ZERO_SUPPORT and allmissingZ UNRESOLVED16 retained.
Same-consumer evidence fault/restore must restore original cell6 (not60), and
query/rule attacks independently restore positive. Fresh-process verifier-only
re-export preserves signature, canonical provenance and values54/6/60.
Sourcefree synthetic only; no original data, new architecture, science,
production, HQ/other-node writes/adoption. Full J42/P41/E04 integration NOT_REACHED.

Write terrain: only rawlsing_next/pre553_universal_evidence_binding.py,
rawlsing_next/tests/test_universal_evidence_binding.py and this r7 return root.
