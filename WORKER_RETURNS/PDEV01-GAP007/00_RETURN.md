# PDEV01 GAP-007 — P1 plan to current sourcefree receiver

**BRANCH:** `agent/pyat-pdev01-gap007-sourcefree-r1`  
**STARTUP SHA:** `773bb412a820949f13a7178b6671327cd56a3bf1`  
**P1 PIN:** `d1278613e9e1a5d986ccce15782a697f19cbd722`  
**ROLE:** bounded sourcefree integration comparison; TEST_ONLY; not reviewer, issuer or adopter.  
**WRITE ROOT:** `WORKER_RETURNS/PDEV01-GAP007/`

## Result

The exact P1 constructor produces **35 synthetic waves / 70 items / 840 prospective operations**. The current PRE-MAIN `BatchManifest` accepts all **840** units with no holds, no abstentions, no duplicate identities, and a bit-identical manifest ref to the P1 plan's 840 units.

The first execution receiver attempt stops at a typed mismatch:

```text
BatchExecutionRunner(
  manifest=plan.batch_manifest,
  repository=C11Repository(),
)
-> BatchIntegrityError:
   exact C11 release unavailable; no latest/default/fuzzy/nearest fallback
```

The P1 plan carries 35 synthetic `C11LogicalRelease` refs from its fixture, but no matching accepted C11 logical releases are present in the current repository. This is a **binding/input gap**, not a dropped or invented P1 operation.

## Exact no-drop evidence

- `plan_ref`: `e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea`
- `BatchManifest` ref: `d9164f33d81ea2ec30681af98364e06983967a3a1f784f40d30ab2639553dca5`
- 35 waves, 70 items, 840 operations, 840 batch units
- 840 distinct operation refs / 840 distinct batch unit refs
- 0 holds, 0 abstentions
- `processed_item_count = expected_item_count = 70`
- `all_compiled_entries_are_batch_units = true`
- `no_drop_ok = true`; `source_qualification = TEST_ONLY_SOURCEFREE`
- all 35 release refs are synthetic fixture refs; none resolves in current C11 repository

## Run evidence

- Exact P1 constructor tests at d127 loaded on current PRE-MAIN: **18 passed**
- Current PRE-MAIN Batch owner tests: **16 passed**
- Five historical-function jurisprudence tests: **5 passed**
- Standalone replay: `replay/replay_gap.py`; output `evidence/replay_gap.json`

## Five historical-function disposition

1. **Current necessity:** exact P1 prospective units must reach a real execution receiver, not merely a second manifest constructor.
2. **No lawful adequate successor:** current BatchManifest accepts the units, but current BatchExecutionRunner cannot resolve the synthetic release refs; no replacement compiler is demonstrated.
3. **Real receiving need:** current `BatchExecutionRunner` is the execution consumer; it fails before unit scheduling at exact C11 release resolution.
4. **Suitability under constraints:** TEST_ONLY, synthetic, no source rights; P1 remains a candidate constructor; current receiver remains unchanged.
5. **Comparative gain:** reuse P1 constructor + BatchManifest; do not rewrite compiler; defer execution until exact C11 release and I03/I05 semantic job bindings exist. A real source pack remains separate.

**Disposition:** `CURRENT_RECEIVER_BINDING_GAP__NO_PRODUCTION_REPAIR__TEST_ONLY`.

## Smallest necessary repair

No code repair in this return. The P1 wave inputs must carry exact existing `C11LogicalRelease` refs and a real execution owner must bind each P1 operation `job_ref` to exact C11/I03/I05 semantic query/discovery jobs. The current P1 constructor and current receiver are left unchanged. No fabricated releases, source rights, N5/N6, N9/N11/N12 or downstream product is claimed.

**Independent review required before acceptance.**
