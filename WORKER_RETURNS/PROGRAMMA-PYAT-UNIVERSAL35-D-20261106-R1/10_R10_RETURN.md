# PROGRAMMA PYAT — Universal35 D r10: artifact publication after final decision

**STATUS:** `D_R10_ENVELOPE_PUBLISHED_ONLY_AFTER_EXACT_FINAL_DECISION__STAGED_ATOMIC_REPLACE__G_ORDERING_DEFECT_CLOSED`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `0d48fc73292277a403ca70e0d304450f62b5444b` / code `fbc6ca3eb1246aa6a946c558a5f6e30dedafeb45`
**G R9 REVIEW:** `e693359b44802755453f1052d340f9ead29275ab`

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R10-1. Envelope artifact publish now occurs only after the final exact source-read decision check.** The wrapper previously wrote envelopes inside the governed-result branch before `after_decision` equality/refusal. It now computes facts/ledger first, performs the final decision comparison, and only then calls `write_field_forge_envelopes`. | G's `A,A,B` refused run can no longer leave or overwrite `SRC01.field_forge_envelopes.json`. | G focused closure. | D + G |
| **R10-2. Artifact write is staged and atomically published.** The helper validates explicit permission, matches every query, builds all envelopes in memory, writes a sibling staged temp file, then uses `os.replace`; on failure the temp is removed. | Missing query/permission/replay or interrupted write leaves the prior valid artifact unchanged, not erased and not partially replaced. | Preserve prior durable history. | D |
| **R10-3. Existing explicit-permission/no-drop behavior remains.** Default `producer_permission_ceiling=None` writes no artifact; empty/invalid ceiling refuses; caller ceiling propagates unchanged; missing exact query refuses before publication. | No auto-mint, no partial consumable artifact. | Preserve. | D + E |
| **R10-4. Sourcefree E arity result remains exact.** 30 facts, all 1-target, 30 envelopes, 30 typed `FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED`, 0 profiles, `structural_grant=false`; cold CLI matches. | No forced 2-target positive; 2-target joint producer remains missing. | Preserve typed refusals and facts. | D + E |

## 2. TESTS / EVIDENCE

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes \
  -p no:cacheprovider --tb=short
1 passed in 3.60s
```

Observed: positive 30 facts/30 envelopes/30 typed arity refusals; explicit ceiling round-trips; no-permission/empty-ceiling creates no artifact; missing query leaves pre-existing `PRIOR_VALID_ARTIFACT` unchanged and no staged temp. Wrapper ordering now publishes only after final decision success.

## 3. PRESERVED / LIMITS

- 35 sources; 18,276 items; 18,413 slots; 18,467 operations; route `676/4705/249`; frontier `7/694/683/11`; 28 typed no-route sources.
- Actual original facts/E authentic handshake remain `NOT_RUN`; A coordinate and C scale reviews independent.
- No A/C/E/guide/controller/protected edit, no native/science/protected grant, no 650s or full manifest suite rerun.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r10 publication ordering
- Identity: codex/pyat-universal35-d-20261106-r1@<returned-commit>; input 0d48fc732.
- Function: complete fact/ledger evaluation -> final exact source-read decision pass -> explicit-permission envelope validation -> staged atomic artifact publish.
- Evidence: refused/failing path leaves no new/overwritten consumable artifact; positive 30/30/30 arity refusals, 0 profiles, structural_grant false; cold CLI parity.
- Limits: 2-target joint producer missing; actual original facts/E handshake NOT_RUN; no native/science/protected acceptance.
```

## 5. BOUNDARY

Author evidence only. No fabricated permission/fact/query, no role/arity relabeling, no protected merge or self-review. G focused closure requested on this exact head.
