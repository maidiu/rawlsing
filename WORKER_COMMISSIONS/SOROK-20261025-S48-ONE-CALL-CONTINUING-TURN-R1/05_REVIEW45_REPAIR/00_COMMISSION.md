S48 exact repair1, same original session/branch atae021e470cb6a6e144008e569a286a787120cb9d. Review45 76dc739fc4528153453080b50c3f7fc138d1592d REVISE three actual defects. Fix only these: (1) explicit turn identity/source-event replay vs advance semantics: realized next event must support NEWordinaryturn, same logicalturn replay/cold must not call again. Do not merely flip cache and break cold idempotency; distinguish replay requestedturn from advance newcurrentevent in API canonical IDs. (2) durable pending/dispatch-intent canonicalrecord BEFORE actual provider effect; interruption/ambiguousreturn never reissue blindly. Persist/recover known output where possible; typed UNKNOWN/PENDING if evidence uncertain, don't silently retry/providerreuse. No fakecall receipts or newparallelledger. (3) remove actor-material→otherperson share/refusal inventedlaw. Allowed proposals must derive from actual independently sourcequalified otheractor owner/performer/current admission under EXISTING settled finite sourcefree semantics. LLM candidate is not other's intention. Recover existing otheractor performer/source; no arbitrary new willingness-policy, weights or caller case_for(share) as proof. If no competent otheractor positivecase currentlypossible, preserve exact typed source-owner hold and report indispensable missingfunction rather than fabricated positive. Do not conflate material feasibility with other's will or rewrite captured oldactualproof as proof of repaired independence.

Add focused multi-turn/explicitreplay/cold, crash-after-provider-before-result/ambiguity, independent candidateowner/source mapping regressions. Keep actual onecaptured providercall evidence at oldcut exactgrade; no new liveprovidercall merely to repeat knowntransport, but if newly changed positivebehavior materially needs actual evidence, one bounded sourcefree actual run may be necessary and must be labeledexactcut. SCI05 nonemptyaccount HOLD unchanged; no newpsychology/nativeA/T/secondpsyche or forceabsence. Use in-worktree logs only/no /tmp or /dev/null output. Read unchanged reviewer reproducerfiles under SOROK_REVIEW/S48/evidence, focusedsuite, commit/push samebranch. No unrelatedimprovements/newagents/broadtests. Reviewtext follows.

# S48 one-call continuing turn — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `ae021e470cb6a6e144008e569a286a787120cb9d`.
- Branch: `codex/sorok-s48-one-call-continuing-turn`; remote matches.
- Base: accepted S47 `765a441f87292aa4c17794745b65cb54e6aaa83f`.
- Reviewed in a clean fixture with stale bytecode removed. No live provider
  call was made by the reviewer; the author’s captured raw CLI/evidence was
  inspected. No product edits, agents, provider switches, native/science/source
  grants, transport changes, or `/dev` operations.

## Executed checks

```text
PYTHONPATH=<S48 return> python3 -B -m pytest -q \
  <S48 return>/tests -p no:cacheprovider
10 passed in 11.18s
```

The captured actual provider evidence is one CLI session
`ses_e8aeaf241ffeKxMW1nJHyn7u04`, one `step_start`/`step_finish`, one text
event, empty stderr, and a canonical call receipt with
`provider_call_count: 1`. The captured actual positive turn has narrative,
`self_account: null`, one prospective candidate, an independently admitted
next S42 event, targetless C9, and cold zero-recall. The controlled SCI05 hold
and call-failure branches pass.

## Blocking findings

### 1. A second turn returns the first turn’s cached result

`run_turn` treats the previous result’s newly admitted `event_ref` as the next
source event and returns `_cached_result` before invoking a new turn. A real
second call therefore produces no second product turn, no provider invocation,
and no new event:

```json
{
  "first_status": "REALIZED",
  "first_event_ref": "TEST_ONLY_BP2_E1_OCC-0002",
  "first_provider_call_count": 1,
  "second_status": "REALIZED",
  "second_event_ref": "TEST_ONLY_BP2_E1_OCC-0002",
  "second_cached": true,
  "second_provider_call_count": 0,
  "second_invoked_runner": 0,
  "same_event": true
}
```

This permanently returns the first next event on later turns instead of
progressing the continuing turn.

### 2. Crash after provider return before append causes a duplicate call

The product turn/result is appended only after `run_product_cli` returns. If
the append fails, no pending canonical turn is recorded; a retry invokes the
product again. The fixture produced two provider invocations for one logical
turn:

```json
{
  "first_error": "append failed after product call",
  "first_provider_invocations": 1,
  "second_provider_invocations": 1,
  "second_status": "REALIZED",
  "product_turns": 1
}
```

There is no pre-call pending record or durable call receipt binding the first
effect; cold/retry can duplicate the provider call and create only the second
canonical result.

### 3. Candidate eligibility maps material directly to other-actor will

`eligible_candidate_ids` returns `OTHER_SHARES_TOOL` when material is available
and `OTHER_REFUSES_TOOL` when it is not. These are static descriptions of the
other actor’s action; the product is allowed to select one and
`run_turn` constructs the corresponding `case_for(...share...)` source. No
independently qualified other-actor source, performer receipt or settled finite
owner makes that choice:

```json
{
  "material_before": 1,
  "candidates_before": ["OTHER_SHARES_TOOL"],
  "material_after": 0,
  "candidates_after": ["OTHER_REFUSES_TOOL"],
  "mapping_changed_only_by_material": true
}
```

This invents other-actor willingness/refusal from actor material state rather
than qualifying an existing independent performer/source.

## Required repair

- Cache only while the same occurred source event is still the current source;
  a realized next event must produce a new turn and provider invocation on the
  next call.
- Persist a pending/call receipt before the provider call or bind the actual
  call to a canonical turn ID before any append failure, so retry cannot issue a
  duplicate provider call or lose the first effect.
- Derive allowed prospective candidates from an independently source-qualified
  other-actor owner/performer/admission, not from material availability alone;
  leave unresolved options typed unresolved instead of inventing another
  actor’s action.
- Add focused regressions for multi-turn progression, crash-after-call retry,
  and candidate owner/source mapping.

## Receipt

- 10-test output: `evidence/s48-tests-10.out` SHA-256
  `03bb765352159de3a5d59edbcd8dee88af601f5dd13a0836740670c91f5ef7dd`.
- Captured actual entrypoint: `evidence/s48-actual-entrypoint.json` SHA-256
  `0e4507cdb5c486b5b71e30d3d3d98f3def4a294cbbc14e7dcc64df3744c948b5`.
- Captured raw CLI: `evidence/s48-actual-stdout.jsonl` SHA-256
  `1e44bee6bb7d5752a8486c79859e0656ecb523441342a1afd9ae8afa2c644400`.
- Actual envelope: `evidence/s48-actual-envelope.json` SHA-256
  `fdb0726f325aa0ba33e2001336f1c88e57352398057e9da3097a763bf6e1491c`.
- Multi-turn reproducer: `evidence/repro_multiturn_cache.py` SHA-256
  `c14bc11e91f547e9e9ac766afc418d9e37d8d78988f498f33dc92054a02d210e`;
  output `evidence/s48-multiturn-cache.json` SHA-256
  `e2efaceb0c3835a1bc15ee0db5aa6cd2e3503110fbcfdfc5885d38656f7baed4`.
- Crash/retry reproducer: `evidence/repro_crash_retry.py` SHA-256
  `8df4339bc58ff21549ae223a4c1f68e7ca99afda6563cac6a13b1dd7f9cf25ce`;
  output `evidence/s48-crash-retry.json` SHA-256
  `d6f7ae296b9660c3d4ffc1d76df4e7cc22507a85770055e1a6f3c80039a5d3fc`.
- Candidate-mapping reproducer: `evidence/repro_candidate_mapping.py` SHA-256
  `03c16088518f26da19122932f1453ee08a7c38798a2e12f1deba7f4542279ed1`;
  output `evidence/s48-candidate-mapping.json` SHA-256
  `90e6f3775a04de524a0850708cc54959302a00d29a7648499ed01c25e7b701b6`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed by the
  reviewer.
