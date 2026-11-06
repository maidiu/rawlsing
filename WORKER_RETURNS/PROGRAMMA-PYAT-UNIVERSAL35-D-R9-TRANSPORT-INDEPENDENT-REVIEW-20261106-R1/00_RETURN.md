# Universal35 D r9 — generated-object transport review

**VERDICT: REVISE** at frozen D head `0d48fc73292277a403ca70e0d304450f62b5444b`.

- Code: `fbc6ca3eb1246aa6a946c558a5f6e30dedafeb45`
- Prior transport: `9161ba719f327867db78e084357245e369bc1195` / `7ff5e8b`
- Accepted E codec: `f708b4688f6aebd408510aa33faca453bd213749`
- Review branch: `codex/pyat-universal35-d-r9-transport-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

### Blocking — envelope artifact is published before the final source-read decision check

The actual production wrapper calls `write_field_forge_envelopes` inside the
`non_f1` branch at `rawlsing_next/pre553_original35_execution.py:413`, before the
post-consumer decision equality check at line 435. A sourcefree resolver sequence
`A,A,B` (changed but still current) refuses
`SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`, but the run still leaves
`SRC01.field_forge_envelopes.json` on disk. A refused read therefore emits a
consumable fact/query artifact.

The artifact must be created only after the final decision succeeds, or removed
on the refusal path. No product repair is made here.

### Axes — permission / no-drop / positive support

- **Transport permission: PASS_SCOPED.** `state_root` alone creates no E
  envelope and grants no production right; empty and invalid ceilings fail
  before any envelope artifact; explicit
  `("FIELD_FORGE_RELATION_PRODUCTION",)` propagates unchanged to every envelope.
- **No-drop: PASS_SCOPED.** Actual wrapper positive/restore: 30 governed facts,
  30 envelopes, 30 facts accounted, 15 operations, 18 candidates; caller
  permission is unchanged.
- **Positive support: NOT_RUN/MISSING.** All 30 facts are 1-target; all 30 E
  results are typed `FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED`, 0 support
  profiles, `structural_grant=false`. No fact is relabeled and no positive
  profile is forced. A 2-target joint producer remains missing.
- **Changed controlled input: PASS_SCOPED.** Changing one sourcefree SAV value
  changes the actual fact refs and envelope fact identities while keeping 30
  facts; no fake positive profile is claimed.

### E codec / preservation

The E codec blob is exactly `6acba005…` at both accepted `f708b468…` and this D
head; no semantic rewrite. Cold CLI reload returns the typed arity refusal.
Current 35-source plan/frontier/route floors remain those previously recorded
(18,276/18,413/18,467; 7/694/683/11; 676/4,705/249; historical 20/991 retained).

## Limits

Actual original facts, authentic E handshake, A/C scale, full-estate and 650 s
runs remain **NOT_RUN/HOLD**. No original source read, code repair, A/C/E edit,
native/science/protected promotion, or self-review. Existing visible next-code
interface is `materialize_native_preimages` for the fact bundle and
`execute_governed_frontier` for governed fact/query generation; no new producer
is invented.
