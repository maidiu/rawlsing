# COLD_BUILDER_OUTPUT_SPEC — exact first-reader ABI and the six projections

**Producer:** `tools/r7_builder.py` (new, 6 functions). **Consumer:** independent C's cold builder card and any downstream implementer.
**Guarantee:** output is a pure function of `(decision, frame, history)`. Same input bytes ⇒ same output bytes; verified twice in `test_builder_is_deterministic`.
**Non-guarantee:** a `PASS` here is a *construction* artifact. It is not science, not independent review, not owner receiving, not native execution.

---

## 1. Invocation

```
python3 tools/r7_builder.py DECISION.json FRAME.json INVENTORY.json --out OUTDIR/
```

Exit 0 on write. It does **not** validate the decision — validation is `r7_integrated.py DECISION`, and C re-validates at its own cut.

## 2. Output set (exactly six + one manifest)

| # | File | Media type | Purpose | First reader |
|---|---|---|---|---|
| 1 | `DESIGN_DECISION.md` | `text/markdown` | human-readable decision, alternative disposition counts, explicit proof boundary | integrator, independent C |
| 2 | `COVERAGE_TO_DECISION.tsv` | `text/tab-separated-values` | 118 rows: `group, id, disposition, candidate_specific_effect, first_consumer_consequence, conservation_or_refusal_witness, origin_row_sha256, evidence_grade, owner` | implementer, auditor |
| 3 | `DOWNSTREAM_BUILD_HANDOFF.jsonl` | `application/jsonl` | one handoff per boundary (or explicit `handoffs`), with owner/negative/restore/status | receiving owner |
| 4 | `EVIDENCE_AND_FALSIFIER_INDEX.jsonl` | `application/jsonl` | one record per boundary × {positive, negative, restore} | independent C |
| 5 | `GLOBAL_ARCHITECTURE.json` | `application/json` | the typed graph verbatim (canonical key order, indent 2) | graph reviewer |
| 6 | `BOUNDARY_TRACE.json` | `application/json` | `boundary_contract_sha256` + the seven-row court | boundary reviewer |
| + | `PROJECTION_MANIFEST.json` | `application/json` | `{schema, files:{name:sha256}, digest, scope}` | `r7_integrated.py C_INTEGRATED` |

### 2.1 `PROJECTION_MANIFEST.json`

```json
{
  "schema": "ANVIL_R7_BUILDER_PROJECTIONS",
  "files": { "<exact filename>": "<sha256 hex>" , … 6 entries … },
  "digest": "<sha256 of json.dumps(files, sort_keys=True, separators=(',',':')) >",
  "scope": "DETERMINISTIC_CONSTRUCTION_ONLY__NO_SCIENCE__NO_RECEIVING"
}
```

C recomputes `digest` and re-hashes every file from `--evidence-root`. Any drift is `C:PROJECTION_BYTES_CHANGED:<name>`; a missing key is `C:PROJECTION_SET_INCOMPLETE`.

## 3. Determinism rules

- JSON: `sort_keys=True`, `ensure_ascii=False`, `separators=(',',':')` for hashing; `indent=2` only for human files.
- No timestamps, hostnames, user paths, locale-dependent formatting, or random ids in any projection.
- Tabular output uses `\n` line endings and one trailing newline.
- `COVERAGE_TO_DECISION.tsv` row order is `(group rank, id)` with a fixed group rank map, so it is independent of input list order.

## 4. Cold-builder procedure (what C actually does)

1. Re-validate `FRAME` and `DECISION` at C's own cut.
2. Run `r7_builder.py` into a **fresh empty directory**.
3. Compare `PROJECTION_MANIFEST.json` to `decision.projection_manifest` byte-hash-wise.
4. Read `COVERAGE_TO_DECISION.tsv` cold: pick one identity, follow `origin_row_sha256` back to the inventory row and the source bytes.
5. Read one `EVIDENCE_AND_FALSIFIER_INDEX.jsonl` negative and its restore; confirm they are distinguishable cases, not the same sentence.
6. Walk `GLOBAL_ARCHITECTURE.json` from an `OBSERVED` node to an `ACTOR_STATE` node and confirm every hop's authority/time/payload.
7. Record `SPECIFICATION_CONSTRUCTION_READY`, `EXECUTED_FIRST_READER_PROOF` or `EXACT_BUILDER_HOLD` **separately** — these are not interchangeable grades (`15_TERMINAL_GRADES_AND_COLD_BUILDER_CHRONOLOGY.md`).

## 5. What a cold builder may NOT infer from these artifacts

- That a row's *semantics* are scientifically correct.
- That any 26 proposal is adopted or any 14 proof closed (both are hard-forbidden by the schema).
- That a `SOURCE_STATIC_CONSERVED` boundary actually ran.
- That the C reviewer is independent, or that H1 received anything.
- That the six projections are "the architecture" — they are a deterministic view of one proposed decision.
