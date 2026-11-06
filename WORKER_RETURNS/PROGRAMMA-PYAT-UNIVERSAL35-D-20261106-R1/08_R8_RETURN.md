# PROGRAMMA PYAT — Universal35 D r8: exact fact/query transport to accepted E cold consumer

**STATUS:** `D_R8_EXISTING_FACTS_QUERIES_TRANSPORTED_TO_E_COLD_CODEC__SOURCEFREE_HANDSHAKE_PROVEN__ORIGINAL_FACTS_HOLD`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `f295f90f2dc2202055ddf21b575776621260b118` / code `20c9e383a802462ba46cb71a8221f807950280bf`
**E ACCEPTED CODEC:** `bddef0b5ca40b750fd51770d47df22f2973679b4` / code `f708b4688f6aebd408510aa33faca453bd213749`; F/G accepted cold adapter `c2d4bdcc…`.
**C:** accepted selected stream unchanged. **A:** received accepted mapping commits, no D edit.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R8-1. D now exposes existing fact/query/replay/provenance objects as E envelopes.** `write_field_forge_envelopes` reads `GovernedFrontierResult.native_execution.native_result.empirical_facts`, matches each `fact.empirical_query_spec_ref` against exact existing `native.executed_queries`/catalog queries, and calls the accepted E `envelope_material` with an explicit caller permission ceiling. | No new statistics, compiler, query authority or invented fact. The transport serializes existing canonical objects only. | Use this private artifact for E cold handshake. | D + E |
| **R8-2. The private artifact is optional and cannot auto-mint authority.** It is written only under caller `state_root`; it includes no raw respondent rows/keys and records `native_science_authority=false`. `producer_permission_ceiling` is caller input; no widening of sourcefree grade. | Missing query/replay/permission is fail-closed in E. Facts that E cannot consume remain in the transport and produce typed refusal, not deletion. | Preserve explicit permissions. | D + E + G |
| **R8-3. Sourcefree production facts/query reach the exact E cold command.** The regression builds current governed facts, writes envelopes, reloads the JSON, feeds the accepted E `ingest_envelope` API and cold CLI `python -m rawlsing_next.pre553_field_forge_empirical_ingress --envelope FILE`. | Result is `PRE553_FIELD_FORGE_EMPIRICAL_INGRESS_RESULT@1`; non-two-target facts retain typed arity refusal; 2-target-conforming facts may produce the existing support profile. No role/arity relabeling. | Preserve 1/3+/weighted facts in transport even when E refuses. | D + E |
| **R8-4. Actual original empirical facts remain unavailable.** A coordinate semantics and D/C scale blockers from r7 are unchanged; no 650s rerun. | The handshake proof is sourcefree engineering, not original/native/science handoff. | Keep precise blockers; continue after A/C fixes. | A/C/D |

## 2. EXACT TEST

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes \
  -p no:cacheprovider --tb=short
1 passed in 2.31s
```

Observed: 30 existing facts transported; 30 exact envelopes; JSON reload; E cold CLI returned ingress result schema; missing permission and changed replay fact ref fail closed; no raw rows.

## 3. COVERAGE / LIMITS

- 35 sources; 18,276 items; 18,413 slots; 18,467 operations; route `676/4705/249`; frontier `7/694/683/11`; 28 typed no-route sources.
- Actual original facts/E authentic handshake: `NOT_RUN`; sourcefree transport is not original permission.
- No A/C/E semantic edits beyond received accepted E codec, no raw data/Git grant, no native/science/protected merge.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r8 E cold transport
- Identity: codex/pyat-universal35-d-20261106-r1@<returned-commit>; input f295f90f2.
- Function: existing EmpiricalFact/EmpiricalQuerySpec/replay/provenance -> PRE553_FIELD_FORGE_EMPIRICAL_ENVELOPE@1 private artifact -> accepted E cold API/CLI.
- Evidence: focused sourcefree regression 30 facts/30 envelopes; E ingress result; missing query/replay/permission fail-closed; 1/3+/weighted typed refusals retained.
- Limits: actual original facts still blocked by A coordinate semantics and D/C scale; no native/science/protected acceptance.
```

## 5. BOUNDARY

Author evidence only. No fabricated permission/issuer/fact/query, no role/arity relabeling, no protected merge or self-review. Exact independent G/F closure requested.
