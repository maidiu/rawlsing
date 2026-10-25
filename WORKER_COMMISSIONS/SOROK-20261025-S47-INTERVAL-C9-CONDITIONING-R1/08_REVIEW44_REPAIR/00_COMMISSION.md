Exact remaining S47 repair2, same original session and branch at56f0a2ad276e253f9589bdc072050160567eef8a. Review44 7358ac217035ebffd10bd1e4666f764ac26b6525 confirms event-key/cut/cold fixes, C9edge/actorfirewall/guard/Bprovenance. One blocker: historical source reconstructed from interval-end material differs from actual source consumed at C9admission after material changes in same interval. Fix exact source persistence/binding at canonical event/C9 admission or eventlocal immutable evidence, no parallel ledger/shadow history. Historical reader must return exact admitted sourcehash/content/access and validate against event binding. Present currentavailability/revocation separate. Add warm/cold interval→actualdo_helpmaterialchange→nextrealC9 regression, plus forged event-bound source refusal proportionately. Reuse existing canonicaltransaction/record readset machinery; don't infer past from latest/endstate. No bundledimprovements/newscience/agents/nativegrants. Preserve currenteventkey/defaultlatest and cutretention. Run unchanged preserved oracle SOROK_REVIEW/S47_CLOSURE/evidence/repro_historical_source_hash.py + focused meaningful suite; commit/push same branch. Use in-worktree output paths only, avoid /tmp or /dev/null redirection. Full review follows.

# S47 event-keyed conditioning closure — REVISE

Decision: **REVISE**.

## Exact cut

- Corrected candidate: `56f0a2ad276e253f9589bdc072050160567eef8a`.
- Prior reviewed candidate: `d58c4e9e6a8fefe8fabed4269a77db0ab6237cd8`.
- Prior review receipt: `d1c54ace4fc2f25c56312021c034679e64bc7d46`.
- Branch: `codex/sorok-s47-interval-c9-conditioning`; remote matches.
- Base: accepted S46 `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e`.
- Reviewed in a clean fixture with stale bytecode removed. No product edits,
  provider/model calls, extra agents, source/native/science grants, or
  outside-path outputs.

## Executed checks

```text
PYTHONPATH=<S47 return> python3 -B -m pytest -q \
  <S47 return>/tests -p no:cacheprovider
15 passed in 54.26s
```

The actual C9 edge remains correct: interval source is in the readset, ACTUAL
material is false, scheduled-only material is true, the response remains
targetless `NO_CHANGE`/`NO_PROPOSAL`, source cut/restore works, and the reader
now selects by event ID. The preserved event-key reproducer passes warm and
cold; the previous cut reproducer now retains the historical source in the
readset warm and cold.

The existing `ResolvedStructuralContext` source class remains the material
class; its `access` is objective material availability while
`actor_access_granted` is false, so no actor-knowledge inference was found.
The C9 readset retains B event/access provenance and the new S47 source.

## Remaining blocker

The historical source is reconstructed with **end-of-interval material**, while
the actual source used at C9 admission used **current material availability**.
These differ when material changes later within the same interval. In a real
consumer run, a scheduled interval ended with material available and source
hash `d73a…`; a real `do_help` then consumed material, and the source actually
used at C9 admission was denied with hash `f4af…`. The historical reader
reconstructs and returns `d73a…` (granted), not the actual C9 source
`f4af…` (denied); `objective_material_eligible` remains false and verify stays
true:

```json
{
  "source_at_interval_end": {"access": "granted", "hash": "d73a00…"},
  "source_at_admission": {"access": "denied", "hash": "f4af94…"},
  "read_historical_hash": "d73a00…",
  "read_historical_access": "granted",
  "read_current_hash": "f4af94…",
  "read_current_access": "denied",
  "read_historical_matches_admission": false,
  "read_historical_matches_interval_end": true,
  "cold_historical_matches_admission": false,
  "objective_material_eligible": false,
  "verify_ok": true
}
```

The current C9 readset exposes the source ref but not the source hash/content,
so the reader cannot reconstruct the exact event-bound source from the ordinary
current/end-of-interval path. It silently presents a different source identity
than the one consumed, including a different access state. This violates the
exact historical identity/content requirement even though the event-keyed
binding and cut retention are fixed.

## Required repair

- Bind/persist the exact source identity and content used at each C9 admission,
  or reconstruct it from event-local canonical evidence rather than current
  material or interval-end material.
- Validate the historical source hash/access against that event; keep current
  availability/revocation as separate present-state information.
- Add a warm/cold regression where material changes after the interval and
  before C9 admission, requiring the reader to return the actual admitted
  source.

## Receipt

- 15-test output: `evidence/s47-closure-tests-15.out` SHA-256
  `be9702f5d6808fdc32976d1f394ae7e7636e8ffa7ed3cfb7cd090787ea48b191`.
- Entrypoint: `evidence/s47-closure-entrypoint.json` SHA-256
  `e788a672e2312f580d2bbab41849249a31d3a213964edc72dc978f05466c3104`.
- Corrected event-key reproducer: `evidence/s47-event-ref-correction.json`
  SHA-256 `08509421c19703ad197c6c93a06de223420de8cb12956e4ce2e82345df94762e`.
- Corrected cut reproducer: `evidence/s47-cut-correction.json` SHA-256
  `9e5f4d23081749ffe4a376053c3bb5c99ae656a406205153f3a9512c1c931683`.
- Historical-source reproducer: `evidence/repro_historical_source_hash.py`
  SHA-256 `7f0be52cde3197cce5cd1268aef65e1a087026cd1235705db277b60b23f7a8f8`;
  output `evidence/s47-historical-source-hash.json` SHA-256
  `c110c17b6d04ccffd4f4350b872f4fd280038c0af6c6402dab15677f2a8fef20`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
