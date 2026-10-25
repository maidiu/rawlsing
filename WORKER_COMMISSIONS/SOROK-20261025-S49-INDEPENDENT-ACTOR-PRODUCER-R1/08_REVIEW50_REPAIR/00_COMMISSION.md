Exact S49 repair3 sameoriginalsession/branchb1b9e8b0720d1e29d410a18646eaa0b728057f3b. Review50 3bbdaef831189ad7d97078f8d91bd17e6f84b0e8 closedcache/genvalidation/intactchain, three narrow originalrequirementsremain. (1) strippingextensionfields mustnot downgrade S49-generatedBworldevent to legacyshape; baseS42normalconsumer BEFOREC8 detects actualcanonical generatedevent/actorperformer provenance independently of rawextensionpresence. (2) baseS42admit_event must enforce invariant eveninstanceoverride validator monkeypatched/no-op. Move mandatorybaseguard outof optionaloverride path; independently validatecanonicalS49chain or failclosed for generatedBsource, legacyactualnonS49source stillunchanged. No broadgenericsecuritysystem/dynamicmodulepatch. (3) exactcanonicalattempt-intent must matchfull expectedactor/role/rootIDhash/branch/eventIDhash/time/ruleversion+FULL_RULEhash/accessrefhash/sourcechain/requesthash/option/seal to actualgeneration/currentowner; forgedintent denied beforeworldevent. Digest-equality on subset not exactrecord. Reuse already constructed canonicalattemptpreimage and validatedgeneration; no newframework.

Run unchanged SOROK_REVIEW/S49_FINAL_CLOSURE/evidence/repro_s49_legacy_bypass.py plus originalprobes/focusednewregression stripping/noopbase/forgedintent and cleancontrolledpath/cold, no broadacceptedtests/providercalls. Use canonicalstore/worldevidence no marker-onlyauthority. If cannot failclosed while preserving positive, preserve typedhold ratherthan bypass. ActualrootBcontenthold/controlledTEST_ONLYsourcegrade/S48loopunchanged remain; no native/source/sciencegrants/newpsyche. Commit/push samebranch, fix only these demonstrateddefects. No newagents/privateconfig/tmp/devnulloutput. Reviewtext follows.

# S49 final closure — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `b1b9e8b0720d1e29d410a18646eaa0b728057f3b`.
- Prior candidate: `f60a327a16052a8ededcc7c1f341ffdebc8a48a6`.
- Branch: `codex/sorok-s49-independent-actor-producer`; remote matches.
- Base: accepted S48 `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7`.
- Prior reviewer receipt: `18bd7b21a892ffd4df50e1821293b4cf2bc1ecc5`.
- Reviewed the exact changed code from `f60a327..b1b9e8b` in a clean fixture
  with stale bytecode removed. The candidate adds a minimal seam in accepted
  `s42/session.py`; the S48 loop is unchanged. No reviewer product edit, agent,
  native/science/source grant, private-config read, or outside-path output was
  made. No live provider call was made.

## Executed checks

```text
PYTHONPATH=<S49 return> python3 -B -m pytest -q \
  <S49 return>/tests -p no:cacheprovider
9 passed in 12.81s
```

The preserved access/forgery oracle exits 0: absent access is `NOT_WITNESSED`,
the mutated actor/branch generation is `DENIED`, and no world event is created.
The preserved closure probe exits 0: the metadata access cache no longer creates
access; role/root/rule/source-ref mutations are denied; clean normal consumer is
`OK`; a rehashed chain with intact S49 fields is refused; foreign/stale source
mutations are refused by firstclass. The actual-root path remains an honest
`SOURCE_OWNER_HOLD` with no B event/C8; the controlled path remains an explicit
`TEST_ONLY` B refusal with a normal S42 event and cold reopen. The controlled
grade, native=false, and targetless outcome remain intact.

## Passing closures

- The `session.meta` access cache was removed. With the store perception lookup
  empty, both cached and uncached access are `NOT_WITNESSED`; access now requires
  an actual store perception row and current action event identity.
- Canonical generation validation now checks role B, root ID/hash, exact
  `FULL_RULE` ID/version/content hash, source refs, source-chain digest, event
  hash/time, and canonical attempt-intent linkage. Role/root/rule/source-ref
  mutations are denied before any world event.
- A complete S49 source chain with intact fields is validated at the normal S42
  pre-C8 hook; a rehashed chain and foreign/stale source are refused.
- Actual-root content hold, controlled S39 model-premise grade, no native/psyche
  claim, source cut/restore, no-event performer denial, and S48-loop unchanged
  status pass.

## Remaining blockers

### 1. Stripping all S49 fields admits the generated B source as legacy shape

`S49Session._validate_admit_source_chain` at `s49/session.py` begins:

```python
s49_keys = [key for key in source if str(key).startswith("s49_")]
if not s49_keys:
    return None
```

The base `S42Session` hook returns `None` by default. A generated B source with
every `s49_` field removed is therefore admitted by the actual normal consumer:

```json
{
  "stripped_s49_fields": {
    "status": "OK",
    "event_ref": "TEST_ONLY_BP2_E1_OCC-0002",
    "s49_fields_remaining": [],
    "verify_ok": true
  }
}
```

This is exactly the warned legacy-shape bypass: an S49-generated B refusal
becomes an ordinary accepted source because the chain-required marker was
removed. The normal consumer must fail closed for a generated B event/source
even when the extension fields are absent; extension presence cannot be the
only trigger for validation.

### 2. Bypassing the overridden validator admits the same generated B source

The base S42 default hook returns `None`, so security depends on the S49
override. Replacing that override with a no-op and admitting the intact
generated source succeeds:

```json
{
  "bypassed_s49_validator": {
    "status": "OK",
    "event_ref": "TEST_ONLY_BP2_E1_OCC-0002",
    "has_s49_fields": true,
    "verify_ok": true
  }
}
```

The base consumer must not be able to accept a generated B source as legacy
shape when the override is bypassed. The canonical B event/performer/source
must be discoverable and rejected at the base pre-C8 hook, or the source must
carry non-strippable provenance that the base validator enforces.

### 3. Canonical attempt-intent exactness is incomplete

`validate_b_generation` checks the canonical attempt-intent episode's request
hash, option, and source-chain hash, but not its exact actor, role, root,
branch, event, rule, or access fields. A forged sealed attempt-intent episode
with the same generation hash and source chain but `actor_id="FORGED_ACTOR"`,
`role="A"`, `root_hash="FORGED_ROOT"`, and `access_source_ref="FORGED_ACCESS"`
is accepted:

```json
{
  "forged_attempt_intent": {
    "status": "ADMITTED",
    "performed": true,
    "event_kind": "REFUSAL",
    "reason": "OK",
    "world_events": 14
  }
}
```

The canonical attempt must be validated for exact actor/role/root/branch/event/
rule/FULL_RULE/access/source-chain equality, not only request-hash/option
linkage. The forged intent must be denied before any world event.

## Required repair

- Make the base S42 pre-C8 hook fail closed for generated B sources even when
  `s49_` fields are stripped. Identify the canonical B event/performer/source
  from the C12 store or add non-strippable provenance; do not treat an absent
  extension as legacy authority.
- Make a bypassed S49 override unable to turn a generated B source into a
  legacy S42 source. The base default must reject or independently validate the
  canonical generated B chain before C8.
- Validate exact canonical attempt-intent actor/role/root/branch/event/rule/
  FULL_RULE/access/source-chain fields and sealing; deny forged intent before
  any B world event.
- Preserve the passing actual-root content hold, controlled TEST_ONLY path,
  cold reopen, source cut/restore, generation role/root/rule/source checks,
  no-event world denial, and unchanged S48 loop.

## Receipt

- Nine focused tests: `evidence/s49-final-tests-9.out` SHA-256
  `ab2ae58381c366dd6a9f356fc46bc9d6ed7399c43bdf66805c23f2b1c2c242a3`;
  9 passed in 12.81s.
- Entrypoint: `evidence/s49-final-entrypoint.json` SHA-256
  `dcf93e24037ef702c08adfb5292925ad405370b1d6487683ba5816d0f84acc59`.
- Original access/forgery oracle: `evidence/s49-final-original-access-forgery.json`
  SHA-256 `3546d1447aab1d0cc3e1a11f5f969a8dbb5676178cb5046ed4fde34f423f6261`.
- Preserved closure probes: `evidence/s49-final-preserved-probes.json` SHA-256
  `b097339a8fdb5bab864c9b8d0335d64e67efc44590b7aaa25d411aa3222fb507`.
- Legacy/bypass probes: `evidence/s49-final-legacy-bypass.json` SHA-256
  `f24797ba73a8576688eb2fae116cc484f34ff754a945f2a29c4099cb3093de96`.
- Reproducer: `evidence/repro_s49_legacy_bypass.py` SHA-256
  `a0d0d8f4163b0c761f7eff10f3554483791ad0d6802a57bde725c76d82fe34c3`.
- Candidate/S42 source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed by the
  reviewer.
