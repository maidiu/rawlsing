# Native input preflight contract

## Purpose

`source/native_input_preflight.py` is a fail-closed receiving gate for one bounded original A/B practice pathway. It answers one question: does the presented bundle contain every structurally required, currently effective and internally bound artifact for a competent owner to consider a native `c9p:coordinated_material_inspection` practice test?

It does not answer whether the science is true, whether the source owner should grant access, whether a concrete rule should be issued or whether the actor acquired a practice. It never writes an actor, event, rule, grant, target or occurrence.

## Bundle schema

The bundle is `R27S_NATIVE_INPUT_BUNDLE@1`. It contains:

- `mode`: `TEST_ONLY_TECHNICAL` or `NATIVE_CANDIDATE`;
- `grade`: `TEST_ONLY_SOURCEFREE_TECHNICAL` or `NATIVE_ORIGINAL_SOURCE`;
- `as_of`: the review clock;
- `production`: must declare `native_issued=false`, `grant_written=false`, `production_registry_entries=0`;
- `source_grant_ref`: current source edition, content hash, host, purpose and permission;
- `actor_a` and `actor_b`: distinct actors, A history/contrary/nonperformance refs, B performed refs, `self_knowledge=UNKNOWN_WITHOUT_ADP017`;
- `encounter`: ADP010 opportunity, contact and encounter refs;
- `e1_ref`, `c8_ref`, `rule_a_ref`, `rule_t_ref`, `grant_ref`, `target_ref`, `e2_ref`;
- `source_artifacts`: content-addressed records with exact owner and grade;
- `readset`: the exact declared refs and content hashes.

The positive technical fixture is `fixtures/positive_technical_bundle.json`. It uses only `TEST_ONLY_` identities and is explicitly not native.

## Checks

| Group | What is enforced |
|---|---|
| Schema/mode | exact schema, mode and grade consistency; test-only mode cannot claim native grade |
| Production | zero production registry entries, no grant write, no native issue |
| Source grant | edition, content identity, host, purpose, permission, currentness at review and E2 |
| Artifacts | every declared content hash matches its canonical content; no missing artifact |
| Actors | A and B distinct; A and B source histories are not self-owned; no demographic/role psychogenesis; A self-knowledge remains unknown |
| A history | at least two enacted target operations, distinct times, distinct source owners, before E1 |
| Rivals | at least one dated contrary commitment and one matched nonperformance |
| B | at least one independent performed offer/refusal |
| ADP010 | opportunity→encounter, independent contact witness, no co-location substitution, monotonic time |
| ADP019 | ADMIT status, receipt/event identity, encounter parent, independent source owner, before target |
| C8 | verified proof, monotonic external anchor, protected writer and native key custody in native mode |
| CAN008 | concrete RULE_A, CAN008 R2 authority, exact object and subject, required readset, current/not revoked |
| CAN011 | separate target owner and issuer, exact rule T, response dependency, current/not revoked |
| Grant | CREATE decision, actor/rule/response/prestate binding, separate owner, current/not revoked |
| Target | committed, exact E1/rule/grant binding, state hash, after E1 and grant effective |
| E2 | performed, exact act, independent actuator/occurrence/owner, exact consumed state hash, after commit |
| Readset | declared refs equal the exact pathway refs; every readset hash matches the artifact |
| Native | a separately supplied `SignatureVerifier` must verify every required signature; absent verifier refuses |

## Result statuses

| Status | Meaning |
|---|---|
| `TECHNICAL_PREFLIGHT_PASS__NATIVE_FALSE__PRODUCTION_EMPTY` | structural and currentness checks pass for a TEST_ONLY bundle; no native authority |
| `NATIVE_INPUT_ELIGIBLE_FOR_COMPETENT_RECEIPT__NO_GRANT_ISSUED` | native-shaped bundle with verified signatures; still no grant or write |
| `REFUSED` | typed reasons list; no event, target, grant or production mutation |

Every result carries `native=false`, `native_issued=false`, `production_registries=EMPTY`, `grant_written=false`, `input_digest` and `receipt_hash`.

## Mapping to the existing receiving product

A future competent owner can map a passing native bundle onto the existing BP2P4J/C9R receivers, without changing their semantics:

| Preflight field | Existing receiver |
|---|---|
| `source_grant_ref` | qualified source runtime / `ActorSourceResolver` |
| `actor_a`, `actor_b` | `ActorSourceResolver.resolve_actor_source` and BP1 histories |
| `encounter` | `bp2_joined.ports.ADP010EncounterPort` |
| `e1_ref` | `bp2_joined.ports.ADP019EventPort.admit_native` |
| `c8_ref` | `c8_exclusive_writer` committed occurrence and anchor |
| `rule_a_ref` | `bp2_joined.ports.CAN008RulePort.bind` |
| `rule_t_ref`, `grant_ref` | `bp2_joined.ports.CAN011TargetPort.bind_rule/bind_grant` |
| `target_ref` | C9R `CandidateStore` / `run_candidate_path` durable target |
| `e2_ref` | `bp2_joined.ports.E2OwnerPort.bind` and the later E2 consumer |
| passing result | existing BP2P4J C8→C9→C10→C12/A0/A2 product |

The current BP2P4J production registries are empty. This preflight does not populate them, and no code path in this return calls a native port writer.

## Commands

```sh
cd WORKER_RETURNS/SOROK-20261020-R27S-FIRST-ORIGINAL-SCIENCE-POSITIVE-R1
PYTHONPATH=source:tests python3 -m pytest -q tests/test_native_input_preflight.py
python3 tools/run_preflight.py fixtures/positive_technical_bundle.json
```

Executed result in this return: 22/22 preflight tests pass; the positive fixture returns `TECHNICAL_PREFLIGHT_PASS__NATIVE_FALSE__PRODUCTION_EMPTY`; 10 named negative cases are refused with their expected reason codes (`evidence/negative_preflight_receipts.json`).

## Limits

- The preflight cannot authenticate a real signature without an independently supplied native verifier.
- It cannot prove that a real source owner granted the host/purpose permission.
- It cannot prove that a real encounter, E1, rule, grant or E2 occurred.
- It cannot itself clear the C8 D1/D2/D3 hold or the Pyat N11/N12/R53 hold.
- It is not a scientific ADOPT and not a native person.
