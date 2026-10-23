# R61-R01 R8 author return — target/condition semantic binding

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted. R03 remains
NOT_STARTED.

## Identity

- Branch: `agent/codex-pyat-r61-r01-r7-retained-owner-repair-r1`
- Startup: `9c0f81ecb76ffe35d0190e31492ea1e9b568f01b`
- R8 correction contract: `c18b6ee6060227875e5a7d96b476ba67dc51693b`
- Code commit: `b57e6cf7544c9a66d5dc1c9c7b0ba9d5ba810369`
- R7 independent review: `bfebaeefa452eac90e4b2153c05d17b018347551`
- Executor: same existing OpenCode DeepSeek V4.1-Flash MAX/Global author.

## Function delivered

The shared create/live/restore campaign-context validator now binds semantic
labels to actual native source identities.

- `target_label` must identify exactly one target ref in the pinned query and
  admitted source question inventory. Wrong label and query-target/label
  mismatch refuse before planning/records/native calls.
- Every condition catalog entry is checked against the actual response leaf:
  `SURVEY_RESPONSE_EVENT` leaf, question ref admitted in source inventory,
  occurrence-key/question identity match, and exact typed value equality.
  Form/repeat-qualified occurrence variants remain valid when they resolve to
  the same exact leaf.
- Restore reuses the same validator; a changed condition catalog/value mapping
  refuses.
- `issue(condition_refs)` validates typed keys/values and duplicate refs before
  planning. Malformed keys and duplicate predicate refs now raise
  `RecurrenceRefusal`, not `AttributeError` or bare `ValueError`.
- All R7 owner functions, chronology, multi-batch accounting, stopped head,
  activation preimage, no-rerun retry, fixed-pin restore and native positives
  are preserved.

## Qualification

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r8/junit.xml -o addopts=''
```

- Exit `0`; `32 passed`, `0 failed/errors/skips`; `32.76s`.
- New tests cover H1/H2 target-label/query mismatch both directions, H3
  condition key/value/predicate reversal, question/predicate mismatch,
  form-qualified typed occurrence variant, malformed key typed refusal, duplicate
  condition refs typed refusal, and restore catalog substitution refusal.
- Existing R7 tests retain multi-batch exact counts, pre/post-activation
  restore, native-call conservation, typed receipt states, detached views,
  fixed-pin refusal and native D3/minority/cold positives.

## Changed paths and blobs

| Path | Blob |
|---|---|
| `rawlsing_next/universal_grammar/types.py` | `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` |
| `rawlsing_next/universal_grammar/enumerate.py` | `fd9203a0b272f98771c24070d01a9e5287c9b099` |
| `rawlsing_next/universal_grammar/native_map.py` | `3db04a006802276f131442f299009b1402cb42c9` |
| `rawlsing_next/tests/test_universal_grammar.py` | `098aa99aaeb60c5c9f472e8369bb8a42a5597c85` |

Report artifacts are SHA256-listed in `manifest.json`, excluding itself.

## Limits

Local trusted-host campaign authority only; no protected issuer/signing/global
durable anti-fork/R09. R03/U43/Batch, R04 custody, R05 grades, original
35/1890, F6/F7/F8, N11/N12, Sorok, production/CI and J52/W52 remain NOT_REACHED.
Distinct independent reviewer required.
