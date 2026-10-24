# R91 R05V independent review — return

Verdict: **REVISE / HOLD full R05 acceptance.** The narrow M01 → M1 → M2 → C1
→ unchanged N10E positive and the recovered E41 direct extension are genuine
and useful, but the new consumer is a single-composition canary, not the full
commissioned R05 productive integration. No new authority is needed; the gap is
the in-scope consumer/function.

## Custody

- Exact stable root `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r91-r05v-consumer-independent-review-r1`;
  startup/HEAD `31d77fd37c501954c088c786db20d8056b6748f5`; clean at gate.
- R05 author contract `4524cc431747aa84d0eb22c4fa67a82a6492d8a4`; code
  `766652c47bf3b34c19b10116a3f84f62e0ffd257`.
- Frozen R05V EXPECTATIONS:
  `0ad34409c1f456677e6c84ce17cfc1086dfa456e`, committed before candidate code
  inspection.
- Code delta from `8a6ea2f6c` is exactly three allowlisted paths plus the author
  return root: learned-world composition, universal empirical extension,
  learned-consumer test. No analytical-composition or provider edit.
- Code blobs independently equal author pins:
  learned-world `cdd5a1b5...`, extension `37279fa8...`, test `61c84067...`.
- Accepted R08 bodies are present unchanged (`pre553_universal_evidence_binding.py`
  blob `3ca860e4...`, test blob `5832ce05...`); accepted C1/provider/evaluator/
  empirical-object blobs remain `604c8d59...`, `23167aa2...`, `62e5eced...`,
  `a61365b9...`. No native owner was rewritten.
- Author R05 manifest independently recomputed: all six artifacts match; explicit
  self-exclusion.
- No candidate repair, adoption, author wake, new worker/session/provider/account.

## Already-qualified narrow capability

- Author 34/34 R05 tests pass; independent replay confirms 34/34.
- Actual native M01 fixture execution → discovery/facts → M1 `RULE_SATISFIED` →
  M2 release/protocol → actual C1 conditional evidence → unchanged N10E
  consumer `EXACT_SUPPORTED`; consumer hash
  `8e54f8b0f664051a089590379ba53a1716bbd8f9fa8d8813c29ea46cba1d52cc`.
- The single-case sever/restore probes work: blocked learned product, wrong
  producer predicate/query and absent required current selection refuse; exact
  restoration returns the original positive.
- Recovered E41 extension delegates the direct route to the accepted provider and
  produces the same consumer hash; the extension source references the accepted
  provider/composition owners and is not a duplicate evaluator.
- Broader provider regression: with ONLY the exact read-only
  `WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1` fixture path
  materialized, 43/43 provider tests pass. The author's "69 pass / 8 fixture
  missing" is therefore 77/77 applicable passes after exact fixture
  materialization, not 8 semantic failures. (Author 34 + provider 43 = 77.)
- The 13-test analytical-composition replay also passes as a relevant C1
  regression.

## Missing productive function (priority)

### P1 — Consumer accepts only one composition and does not bind the full R03/M1/M2/B5/I4/E41 product graph

`evaluate_learned_world_consumer` has exactly one `composition:
AnalyticalCompositionResult` parameter and one consumer query/model. It has no
product/evidence collection, no E41 extension result/route, no recursive handoff,
discovery frontier/lineage or joint component input. It validates producer
query/predicate and source-universe membership, then calls the unchanged N10E
evaluator on the one evidence slice. It does not validate or bind:

- joint component count/order/morphology;
- discovery receipt/frontier/coverage;
- recursive handoff/lineage;
- E41 direct/multi/discovery/recursive route result;
- minority/counterpattern disposition fields.

Independent probe
`probes/test_r05v_consumer_gap.py::test_joint_recursive_discovery_bindings_affect_consumer`:
a composition carrying joint count 2, discovery receipts/frontier and recursive
handoff/lineage is accepted as `LEARNED_CONSUMER_EXACT_SUPPORTED`, but the
consumer values have no `joint_component_count`, `discovery_receipt_refs`,
`recursive_handoff_refs` or `producer_route` keys. The E41 extension's direct
result is likewise not an input to this consumer. The author's four new tests
exercise one M01 case, one C1 composition and one direct E41 call; they are not
the required joint/conditional/recursive/minority/counterpattern matrix.

### P2 — Typed status/axes are collapsed, not preserved

The consumer checks only `producer_fact_state == "SUPPORTED"` and evidence
presence; it ignores `composition.analytical_state` and does not expose
denominator/axes/Z. Independent probe
`::test_typed_status_axes_are_preserved_by_consumer` replaced the same
composition with `ZERO_SUPPORT`, `VALID_EMPTY` and `UNRESOLVED` (denominator 16):

```text
ZERO_SUPPORT  -> REFUSED / EMPIRICAL_EVIDENCE_NOT_SUPPORTED
VALID_EMPTY   -> REFUSED / EMPIRICAL_EVIDENCE_NOT_SUPPORTED
UNRESOLVED16  -> REFUSED / EMPIRICAL_EVIDENCE_NOT_SUPPORTED
```

No typed result state, denominator or Z `UNRESOLVED` survives on the
`LearnedWorldConsumerResult`; `consumer_values_read` is `None`. The existing
status/reducer court is not called or projected. Observed zero cells are present
only inside the single exact-supported composition; the wrapper does not
distinguish observed zero from absent/valid-empty/held at the commissioned
consumer grain. This violates the explicit R05/R05V status requirement,
including all-missing Z UNRESOLVED denominator 16.

## Exact missing function

Extend the R05 consumer to accept and validate the complete actual native product
graph — M1 disposition (including minority/counterpattern and typed axes), M2/B5
currentness, I4/joint/conditional/recursive/discovery components, and the
E41 extension route/receipt — and feed that full graph to the unchanged N10E
consumer. It must validate joint/discovery/recursive/currentness evidence
identities, bind them into the same consumer assertion, preserve
eligibility/execution/result axes, denominator/cells and all-missing Z
UNRESOLVED16, and sever/restore each component with exact actual values. Single
M01/single-C1/direct-E41 is only a partial demonstration, not full R05.

## Limits

Full live J42/P41/E04 maintained service remains NOT_REACHED; this finding does
not demand it. No original data/source/science, F6/F7/FieldForge, actor,
CI/production, N11/N12, Sorok, J52/W52, R04.joined dependency or new method
issuance is claimed. R04 remains independent. The extension's recovered
direct/delegation provenance is accepted as a partial capability; it is not
full learned-consumer integration. No adoption or candidate edit.

Artifacts: `EXPECTATIONS.md`, `defects.md`, `limits.md`, `RESUME.md`,
`proof_witness.json`, `SHA256manifest.json`, `outcomes/r05v_observations.json`,
`probes/test_r05v_consumer_gap.py`, `junit/*.xml`, `logs/stdout.jsonl`.
