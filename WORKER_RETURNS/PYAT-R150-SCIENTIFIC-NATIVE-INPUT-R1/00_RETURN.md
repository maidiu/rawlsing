# R150 — wire B49 item authority into current native scientific inputs

**Status:** `B49_ITEM_AUTHORITY_WIRED_TO_PENDING_NATIVE_INPUTS__NO_SOURCE_OR_SCIENCE_ISSUANCE`
**Base:** `29982440dd3148552b23173af0c52288393023f5` (R148 complete metadata retained)
**Scope:** sourcefree documentary/native preparation only. No survey file was opened, stat'ed, hashed or decoded; no source/science/current grant.

## Working adapter

`runtime/scientific_native_input.py` loads the staged B49 compiler/corpus read-only,
joins its **4,460** item-level authority records to the R148 all35 current
codebooks by exact source ID/wave/variable identity, and emits:

- 35 per-source scientific native-input records, 35 selected-rule packages, and
  4,460 pending typed native-occurrence records under
  `records/ITEMS/` and `records/PACKAGES/`;
- exact `NativeSourceIdentity` objects for all 35 sources (inherited documentary
  identity, not current edition/grant);
- `SourceAuthorityCorpus`/`SelectedSourceRulePackage` consumable by the current
  native planner for grounded documentary fields;
- exact item-level disposition, direction, routing, response binding, relation
  scope, evidence IDs and codebook row evidence.

All 4,460 items join exactly to current codebook rows; zero collisions and zero
codebook-missing items. No variable casefold substitution is used. Latinobarómetro's
accented corpus family label is resolved by exact source/wave identity and the
resolution is recorded; unmatched relation IDs remain exactly **26**.

## Item accounting

| Group | Count |
|---|---:|
| B49 item records | 4,460 |
| Selected administered-U candidates | 371 |
| Held/unresolved | 285 |
| Excluded non-U but retained as context | 3,804 |
| Unmatched relation IDs held | 26 |
| Pending native occurrences | 4,460 |
| Native identities / selected packages | 35 / 35 |
| NativeSourceRule / SourceInventory constructed | 0 / 0 |

LiTS is processed first and accounts for 4,434 items:
- LiTS I: 1,198 = 50 selected + 7 held + 1,141 context;
- LiTS II: 627 = 116 selected + 9 held + 502 context;
- LiTS III: 1,290 = 98 selected + 51 held + 1,141 context;
- LiTS IV: 1,319 = 107 selected + 192 held + 1,020 context.

Other covered dictionaries: Latinobarómetro 1995 (18 held), 2024 (5 held),
Afrobarometer R1 (3 held). The remaining 28 sources have no staged B49 item
records; their exact successor target/binding refs are carried from R148, not
called globally absent.

Material/demographic/position exclusions stay in a distinct conditioner/context
lane (3,804 retained). They are not deleted and are not promoted to target U.
`NOT_CERTIFIED` direction is preserved; it is not rewritten as missing raw
nominal evidence and no scalar/polarity/complete-case/same-household inference is
made.

## Native-input premises

Grounded actual native objects: `SourceAuthorityCorpus`, 35 actual
`SelectedSourceRulePackage`s, and 35 actual `NativeSourceIdentity`s; exact
codebook join and item evidence are preserved.

Not fabricated: `Occurrence`/`NativeSourceRule`/`SourceInventory` are
**not** constructed because per-item unit, topology, exact typed domain and risk
set are not settled. Each item is an exact canonical pending occurrence naming
those missing premises. The scientific frontier remains unsigned pending
grounded roles/risk/Epre; no all-pairs, old worklist or fabricated U/Epre.

## Current source separation

R148 current metadata/row accounting is carried separately from B49 historical
evidence and from current access. For all 35 sources:
`current_source_access_permission=null`, `current_source_edition_sha256=null`,
`u_root=null`, `e_pre_root=null`, no response-read grant. No historical
B49 adoption/candidate grade is promoted to current acceptance.

## Next calls

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/runtime/render_scientific_native_input.py --source-id SRC27
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/runtime/render_scientific_native_input.py --source-id SRC24
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/runtime/render_scientific_native_input.py --source-id SRC35
```

Each record contains exact already-grounded fields and the next original
`decode_with_source_read_permission`/`prepare_production_discovery` calls with
their unbound arguments. Those calls must not run until current source identity,
edition hash, source-read grant/current resolver, complete U/Epre and semantic
roles are supplied.

## Verification

- Focused checks: **7 passed** (`evidence/focused.log`).
- Verified: 35/35 sources, 4,460 item denominator, LiTS-first counts, all exact
  codebook joins/collisions, 26 unmatched relation holds, context retention,
  native identity/package types, pending occurrence premises, successor targets
  for uncovered sources, no current grant/bundle, no decoder/survey call.
- CLI probes: SRC24, SRC35 and SRC27 under `evidence/`.
- Receipt: `evidence/PROOF_RECEIPT.json`.

## Limits

No actual source/respondent access, administered U, Epre, empirical/learned/FF
execution or current scientific adoption. No all35 qualification, 1890/F1–F8/
global claim. Representative empirical AND learned-to-actualFF remains parallel.
Full35/1890/F1–F8/global/LongMemory/C5 and all R09/CI/prod/N11/N12/Sorok/J52/W52/
actor holds remain. Native core read-only at `44e7ace44d9e1b023a15d14ee1ead9b176d0e522`.
