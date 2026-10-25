S49 exact repair2, sameoriginalsession/branchf60a327a16052a8ededcc7c1f341ffdebc8a48a6. Review49 18bd7b21a892ffd4df50e1821293b4cf2bc1ecc5 confirmed originalrawforgery/access absentfix, but three originalrequirements remain: meta observationcachebypassescanonicalstore; canonicalgen validation omitsrole/root/exactrule/sourcechain/attempt; normalS42consumerignores S49chainfields. Fix these reported gaps only. Remove accesscache or validateagainstactualperceptionrow/eventhash/clock/channel/owner everytime, metadataalone cannot licenseB. ExactroleB/currentrootIDhash/acceptedFULL_RULEcontent/sourceandaccesspreimages/canonicalattempt andgenerationmustvalidated independently againstexistingcanonicalstore/currentworld—not just rehashed callerbody or episodeexists. NormalS42 admit_event BEFORE C8 must enforce same gen/attempt/performer/access/world/source chain; minimal mandatory hook override in S49/normalS42 interface permitted byoriginalcommission. Adapterhelper validation followed byignoredchainfields isnotintegration. If S49 sourceclass/fields arepresent, missingvalidator/sourcechainmustfailclosed evencallersdirectlyinvokeadmit_event. No broadnewgovernance or cryptosystem: reuse canonicalstore/rules/currentness machinery.

Use preserved SOROK_REVIEW/S49_CLOSURE/evidence/repro_s49_closure_probes.py for exactcache/mutatedcanonicalgen/rehashednormalconsumer cases, plus focusedsuite. Ensure normalconsumer deletion/cut+restore and cold, no Bworldevent/C8 onfailure. Sourcegrading actualrootBcontexthold/controlledexplicitS39premises remainshonest; no newBcontextlaw/ruleweights/psyche or liveprovidercall. Preserve unchangedS48 sourceownerhold, don'tpretend helper isproductloop. No broadtests/newagents/privateconfig/ /tmp /dev/null output. Commit/push samebranch, report actualnormalconsumerbinding. Fullreview follows.

# S49 closure — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `f60a327a16052a8ededcc7c1f341ffdebc8a48a6`.
- Prior candidate: `67f1c0bfac85d04427adb171910f726af496a47f`.
- Branch: `codex/sorok-s49-independent-actor-producer`; remote matches.
- Base: accepted S48 `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7`.
- Prior reviewer receipt: `0e0854ee0a3609f9efcedbd9937a471450bce671`.
- Reviewed the exact changed code from `67f1c0b..f60a327` in a clean fixture
  with stale bytecode removed. No live provider call, product edit, agent,
  native/science/source grant, or outside-path output was made.

## Executed checks

```text
PYTHONPATH=<S49 return> python3 -B -m pytest -q \
  <S49 return>/tests -p no:cacheprovider
9 passed in 9.11s
```

The original reviewer access/forgery oracle exits 0: B absent gives
`NOT_WITNESSED`; a mutated actor/branch generation is `DENIED`; the world event
count remains unchanged; verify is true. The actual-root turn remains an honest
`SOURCE_OWNER_HOLD` (`S49_MISSING_CURRENT_B_ACTOR_OWNED_CONTEXT`) with no B
event/C8. The controlled path reaches a performed B refusal, source adapter,
normal S42 event, and cold reopen. The controlled B source remains marked
`TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE`; no actual B inner-life claim is made.
The S48 product loop remains unchanged, and this receipt makes no S48
integration claim.

## Passing closures

- Actual B access is now based on an actual C12 perception: `record_b_observation`
  calls `_perceive_if_present`, which records a `co_present` perception in the
  product store. Access uses the current action event identity and location;
  B absent gives `NOT_WITNESSED`, not presence-only access.
- Actor/branch/event/time and access-hash checks exist in
  `validate_b_generation`; raw actor/branch mutation is denied before any world
  event.
- The B performer still checks world constraints and denial creates no event.
- Source cut/restore, role parameterization, controlled-only grade, cold reopen,
  and the refusal-only source adapter pass the focused suite and entrypoint.
- The S42 source-level checks still reject foreign event hashes and stale source
  clocks (`MATERIAL_SOURCE_PREIMAGE_MISMATCH`).

## Remaining blockers

### 1. The B access cache is unverified test-helper authority

`s49/actor.py:48-54` accepts `session.meta["s49_last_b_observation"]` when its
event id and actor match the current action event. It does not require the row
to exist in the product perception store, to have been written by a qualified
owner, or to match the event hash/clock/channel. The store lookup is only a
fallback.

With the store perception lookup forced empty in the review fixture, a raw meta
cache produces:

```json
{
  "store_perceptions": "EMPTY_PATCHED",
  "access_without_cache": "NOT_WITNESSED",
  "access_with_forged_cache": "ACCESSIBLE",
  "forged_access_source_ref": "TEST_ONLY_ADP017_S49_B_...",
  "forged_access_observer": "B"
}
```

This is still helper-asserted access. The cache must be removed, or revalidated
against the canonical perception row/owner/event hash/clock/channel on every
access. Actual access must not be creatable by writing session metadata.

### 2. Canonical generation validation is incomplete

`validate_b_generation` at `s49/actor.py:268` checks `valid()`, canonical episode
identity, actor, branch, event ref, event time/as-of, receipt selection, attempt
request identity, option, and access hash. It does **not** validate the exact
role, root, rule, or source chain. Canonical generation episodes with the
following mutations are all admitted as B refusals after `perform_b_attempt`:

```json
{
  "role_a": {"status": "ADMITTED", "event_kind": "REFUSAL"},
  "root_forged": {"status": "ADMITTED", "event_kind": "REFUSAL"},
  "rule_forged": {"status": "ADMITTED", "event_kind": "REFUSAL"},
  "source_refs_forged": {"status": "ADMITTED", "event_kind": "REFUSAL"}
}
```

The changed-code claim of exact actor/role/root/branch/event/time/rule/source/
access validation is therefore not closed. Bind the generation to the accepted
role, root identity/hash, exact `FULL_RULE` content, and qualified source/access
chain; validate the canonical attempt episode as well as the request body.

### 3. The normal S42 consumer does not validate the S49 chain

`_source_from_b_event` validates the generation before constructing the source
and adds `s49_generation_hash`, `s49_attempt_hash`,
`s49_rule_content_hash`, `s49_access_witness_hash`, and
`s49_source_chain_hash` at `s49/session.py:73-94`. The normal consumer at
`S42Session.admit_event` (`s42/session.py:91-122`) only passes the source through
`firstclass.validate_source`; it does not read or validate those S49 fields.

A source/case with a properly rehashed but forged S49 chain is admitted:

```json
{
  "rehashed_chain": {
    "status": "OK",
    "event_ref": "TEST_ONLY_BP2_E1_OCC-0002",
    "source_chain_hash": "<forged digest>",
    "verify_ok": true
  },
  "foreign_event_hash": {"refused": "MaterialSourceRefusal"},
  "stale_clock": {"refused": "MaterialSourceRefusal"}
}
```

Thus the adapter self-validates, then supplies unverified hash fields to the
actual C8 consumer. The requested rehashed/stale/foreign source refusal at the
actual consumer is not complete: event-hash/stale-clock mutations are refused,
but a rehashed S49 generation/attempt/source chain is accepted. The normal
consumer must validate the S49 generation, performer, access, and source chain
against the canonical store and current world before C8.

## Required repair

- Remove or cryptographically/structurally revalidate the S49 access cache
  against the canonical product perception row, event hash, clock, channel, and
  owner. Session metadata alone must not create access.
- Extend canonical generation validation to exact role, root, accepted rule
  content, source chain, access, event hash/time, and canonical attempt episode;
  reject all mutations before any B world event.
- Make normal S42 admission validate the S49 generation/performer/world/source
  chain, not merely the firstclass source shape. Rehashed, stale, foreign, or
  unlinked S49 fields must refuse at the actual consumer before C8.
- Preserve the passing actual-root hold, controlled TEST_ONLY path, cold reopen,
  source cut/restore, actor parameterization, no-event performer denial, and the
  unchanged S48 source-owner hold.

## Receipt

- Nine focused tests: `evidence/s49-closure-tests-9.out` SHA-256
  `741b68df2dbd150059f55f24f4e6124361bbe832a9f9b4710378294cd099f6b3`;
  9 passed in 9.11s.
- Entrypoint: `evidence/s49-closure-entrypoint.json` SHA-256
  `f48ab1ca3a7f7af8e363bad650bdf617fe3270be55d100a511a59e941e5b8ec0`.
- Original access/forgery oracle: `evidence/s49-closure-original-oracle.json`
  SHA-256 `004f50a8fe747b64125ad08729b4fe1a375fc82bebed39e4102fdcd1ea9c124d`.
- Closure probes: `evidence/s49-closure-probes.json` SHA-256
  `c4853c237d911192507db5a4b1c6b40547cea585800ba5772fee6dd38eb0e0f2`.
- Probe reproducer: `evidence/repro_s49_closure_probes.py` SHA-256
  `6d6d366572fd1d7c838d527ce47792b365bcdd2ce352b0a28102161256d7801b`.
- Candidate source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed by the
  reviewer.
