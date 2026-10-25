S49 exact repair1 same originalsession/branch67f1c0bfac85d04427adb171910f726af496a47f. Review48 0e0854ee0a3609f9efcedbd9937a471450bce671 REVISE two explicit failures: unconditionalACCESSIBLE Baccess with no observedADP017source, and forged generationactor/branch/event accepted by performer thennormalS42. Fix these only, preserve knownactualrootcontextHOLD and honestcontrolledgrade. Reuse actualworld perception/actoraccess owner registry/witness APIs. Presencealone isnot access. No ownerlabel/selfseal as evidence: actual observation/ADP017 receipt bound event/actor/time isrequired; no suchsource means holdbeforegeneration/performance. Controlledmodelpremise alone cannot licenseaccess. Controlledpositive can use genuinely issued simulation observation source through realowner/perceptionpath, not testhelper markingACCESSIBLE. No newpsychology/grants.

Separateperformer validates exactsealedgeneration+attempt linkage/source/access/currentactorrole/root/branch/event/time/asof/rule/options/constraints BEFORE anyworldevent, rawforgedbodymusthavenoeffect. Canonical actorproducer issuance must be validated not recomputedcallerhash-only. Normal sourceadapter/S42admission must bind BOTH generationandperformer+world/sourcechain before C8; reconstructingcase from justBworldevent insufficient. Cut/remove/forgegenerationoraccess at actualnormalconsumer must refuse and restore recover, cold. Minimal existingS42 hook if required originallyauthorized, no broadrewrite. Do not merely hide helper from tests or remove controlledpositive and call completedproducer. Actualroot Bpremise absence remains separate genuinecontenthold; independent engineering of actualaccess+performerchain isbuildable.

Run unchanged reviewer SOROK_REVIEW/S49/evidence/repro_s49_access_and_forgery.py plus focused meaningful regressions, no broadsuite/providercalls. Preserve originalS39FULL_RULE no arbitrarynew comparisons/weights. Keep refusal-only source mapping/ATTEND REQUEST typedholds and S48hold honest (S49helper not yetproductloop). Commit/push samebranch with exactresults. No newagents/privateconfigread or /tmp /dev/null outputs. Reviewtext follows.

# S49 independent actor producer — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `67f1c0bfac85d04427adb171910f726af496a47f`.
- Branch: `codex/sorok-s49-independent-actor-producer`; remote matches.
- Base: accepted S48 `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7`.
- Prior reviewer receipt: `7de8451dd5652d369b89fa23acdb75aac4a8cc6d`.
- Final tree contains 18 new S49 files; intermediate pytest artifacts were not
  part of this review.
- Reviewed in a clean fixture with stale bytecode removed. No live provider call
  was made by the reviewer. No product edits, agents, provider switches,
  native/science/source grants, private-config reads, or outside-path outputs.

## Executed checks

```text
PYTHONPATH=<S49 return> python3 -B -m pytest -q \
  <S49 return>/tests -p no:cacheprovider
6 passed in 6.58s
```

The actual-root hold is honest: no B world event is created, no C12 event is
created, the clock is unchanged, and `verify()` succeeds. The controlled run
produces an explicit test-only B refusal, a B performer event, a current source,
and a normal S42/C9 result. Cold reopen returns the same B-turn store. The
role test is parameterized to actor B, and the source adapter refuses to map a
non-refusal operation to `REFUSE_TOOL`.

Scope note: `S49Session.produce_b_turn` is a separate helper. S48
`run_turn`/its source-owner hold was not changed and S49 does not claim that
this helper is S48 product integration.

## Remaining blockers

### 1. B access is fabricated, not observed

`s49/actor.py:32` (`_b_access`) always emits `access_status="ACCESSIBLE"`,
`scene="workshop"`, and a `TEST_ONLY_S49_B_ACCESS_*` source, regardless of
B's actual access, observation, or ADP017 qualification. `generate_b` at
`s49/actor.py:79` passes that witness into `generate_choice` with
`access_outcome="RECEIVABLE_NO_OBSERVED_UPTAKE"`.

Reproducer `evidence/repro_s49_access_and_forgery.py` shows:

```json
{
  "access_with_b_absent": {
    "b_position": "market",
    "access_status": "ACCESSIBLE",
    "access_scene": "workshop",
    "observer": "B",
    "access_source_ref": "TEST_ONLY_S49_B_ACCESS_TEST_ONLY_BP2_E1_OCC-0001"
  }
}
```

With B back at the workshop but without any B observation/ADP017 source, the
controlled generation selects `EXPLICIT_REFUSAL` and the performer admits the
B refusal. The world presence check in `_world_for_b` is not an access,
observation, or source-qualification check. Actual B access must be established
before generation and performance, or the turn must hold. A TEST_ONLY
controlled premise may supply the model premise, not a synthetic ACCESSIBLE
access witness.

### 2. The B performer accepts forged generation/attempt linkage

`perform_b_attempt` at `s49/actor.py:119` checks that the body has an
`actor_id` and a request, then checks B's position and option constraints. It
does not verify the sealed generation hash, the attempt request's event ref/hash,
the current event, branch, root, time, actor identity, source/access receipt, or
the exact generation-to-attempt linkage. A mutated sealed body with
`actor_id="FORGED_ACTOR"`, `branch_id="FORGED_BRANCH"`, and forged event refs is
accepted and creates a B `REFUSAL` world event.

The normal source path does not repair this: `_source_from_b_event` at
`s49/session.py:39` reads only the B event's actor and kind, then constructs the
source/case itself. The generated/attempt body is not bound into the source or
checked by `admit_event`.

Reproducer result:

```json
{
  "forged_generation": {
    "status": "ADMITTED",
    "performed": true,
    "event_kind": "REFUSAL",
    "result_actor": "FORGED_ACTOR",
    "generation_hash_unchanged": true,
    "normal_s42": {
      "status": "OK",
      "event_ref": "TEST_ONLY_BP2_E1_OCC-0002",
      "source_has_generation": false
    }
  },
  "forged_verify_ok": true,
  "forged_world_event_count": 14
}
```

This violates the requirement that a raw forged request cannot create a B
world fact and that normal S42 source admission validate the generation and
world chain before C8. A self-sealed source case built from the B event is not
sufficient provenance.

## Required repair

- Derive B access from actual current B presence/observation and a qualified
  access/ADP017 source. If that evidence is absent, hold before generation and
  performance; do not synthesize an ACCESSIBLE witness. Keep controlled
  premises explicitly TEST_ONLY and do not represent them as actual inner life.
- Make the separate B performer validate the exact sealed generation and attempt
  request: generation hash, actor/role, current event ref/hash, branch/root,
  time/as-of, options, constraints, and source/access receipts. Reject a mutated,
  unlinked, foreign, stale, or forged generation without creating a B event.
- Require the normal S42 consumer/source adapter to bind and validate the
  generation/performer/source/world chain before C8. Do not reconstruct a
  self-sealed B source solely from an existing B event.
- Preserve the passing actual-root hold, controlled test-only grading,
  refusal-only source mapping, ATTEND/REQUEST holds, cold reopen, source
  cut/restore, and the unchanged S48 source-owner hold.

## Receipt

- Six focused tests: `evidence/s49-tests-6.out` SHA-256
  `2719b16b7f131f422ed94dd4fe854305137b8d1717d2ebac648c46f0c4fe938e`; 6
  passed in 6.58s.
- Entrypoint: `evidence/s49-entrypoint.json` SHA-256
  `4f6eec7bf08c4c4c33fef4336a39dec49dc4077bd71326874cc51760da400ed9`.
- Access/forgery output: `evidence/s49-access-and-forgery.json` SHA-256
  `7fa6e42c2f4e93ba92e5493ad3e32459ff29bdc665be0f3715c297353cbd7c22`.
- Reproducer: `evidence/repro_s49_access_and_forgery.py` SHA-256
  `2842fec1cf8d1242eff2509d27b9b606d26d9c50f34574b9348163091baee796`.
- Candidate source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed by the
  reviewer.
