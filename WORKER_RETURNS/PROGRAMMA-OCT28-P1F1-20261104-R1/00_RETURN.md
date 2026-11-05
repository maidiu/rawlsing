# OCT28-P1-F1 repaired implementation return

**LOCAL S2 PASS; READY FOR SAME NONAUTHOR P1R2. No independent acceptance claimed.**

Source commit: `cd1e7ccf8419a000817b4a8535879da56c06db98`. Exact original P1 start: `0a63e7c90cabcfd01dbb169d477f2d0ead5be22c`. Branch: `agent/programma-oct28-p1f1-selector-ref-integrity-20261104-r1`. Protected PRE-MAIN refreshed on launch and remains `f58c8400a024d108a8ab9fa814c87967d336ea47` (`integration/pre-main-reconciliation-r1`). Exact independent P1R1: `a7024d244f71e55c5a64e62089ba4c710e6f0059`. The attached user commission is preserved verbatim as `COMMISSION.md`; its standing synthetic/test-only authorization was used. No OpenCode worker was launched, following the user's instruction to finish the work myself.

## Exact repairs and selector v1

M1: `_EventRead` now retains only immutable primitive tuples for event, native, canonical, component and authority identities. Public reference properties construct detached ExactRef/AuthorityRef exports. Dictionary writes on an exported descendant cannot change a retained identity, another occurrence/respondent, an independent sealed native lookup, or supported fact provenance. Shared dimensions are interned as immutable tuples. Selection compares these primitives without materializing native events. ExactRef/AuthorityRef public definitions, physical cache schema, native body/hash/replay contracts and scientific owners are unchanged.

M2: the exact allocation-identity assertion is replaced by RespondentEvent native type, exact reference and complete `as_dict()` equality. All original descendant mutation, detached export, sealed-body and requery assertions remain. The full eager suite and all forced compact semantic tests pass.

`_SELECTOR_CONTRACT_VERSION = 1` and the existing `_select_respondent_events` docstring freeze the internal handoff at this source SHA:

```python
_select_respondent_events(
    index: _ReleaseIndex, respondent_key: str, target: ExactRef,
    *, native_only: bool = False, include_component: bool = False,
    states: frozenset[str] | None = None,
) -> Iterator[RespondentEvent | _EventRead]
```

Native fallback returns native RespondentEvent; compact `.select()` returns `_EventRead`. Ordinary Sequence iteration reconstructs native events. Fields: schema_id, exact ref, typed_state, native_question_ref, optional canonical/component refs, authority_snapshot_refs, raw/canonical values, multiplicity/order/rank and response occurrence identity. Refs are normalized through existing exact-ref helpers. Compact selectors do not supply arbitrary native `as_dict`, schema_version or source/row fields: sealed release/index authority and the exact resolver remain the source. Native-only overrides canonical/component matching, empty states yields no rows, None states includes all, missing respondent raises KeyError. Order, duplicates and respondent/universe grouping remain exact. New tests cover all reference families, multiple respondents, repeated ordered occurrences and mutation/restoration.

The first consumers remain the existing `_eval_predicate` and `_eval_target_for_respondent` through `CarrierNeutralResearchExecutor.execute_i03` -> `execute_empirical_query`. P2 remains behind that entrypoint; it gains no Arrow/Parquet/private-cache scientific-source authority, new semantic engine or external API. Existing per-call authority/source gates, E3 sealed-index invalidation, typed refusals, risk/denominator/weights and zero domains retain their original owners.

## Executed S2 evidence

- Original unchanged reviewer exploit: reproducible changed SUPPORTED provenance at original P1 (`selector-alias-original.log`). Unchanged owner regression RED: 1 failure (`selector-integrity-RED.log`). Fixed unchanged owner regression GREEN: 1 pass (`selector-integrity-GREEN.log`).
- Re-running the original exploit on fixed code exits 1 at its intentional assertion `no exercised selector changed a downstream fact`; it requires an exploit and none occurred (`selector-alias-fixed-original-probe.log`). The preserved fixed counterpart keeps both original fault loops, exact native lookup and restoration, and asserts no changed fact for every event/question descendant: PASS (`selector-alias-fixed-GREEN.log`). It is explicitly adapted, not mislabeled as the untouched original exploit.
- Full pinned related suite: **209 PASS, 1 SKIP**. The skip is the existing installed pyreadstat DTA writer/readback limitation: missing_user_values metadata does not expose the extended-missing declaration.
- Focused P1/cache/facade/Route B: **42 PASS**, including both new reference/selector regressions.
- P1R1 harness rerun: **9 PASS**, including 13 pinned native/compact query cases and 16-slot/80-collision cache integrity. Its public-field comparison was adapted from dataclass storage reflection to the same ten documented public selector fields because backing fields are now private. No expected semantic values were changed. These are author-executed reviewer tests, not a new independent review.
- Forced compact existing I03/frontier/I05 semantic suite, including the complete amended immutability test: **60 PASS**.
- Deliberately severed cache-body hash check: expected RED, restored check PASS (`cache-red-restore.log`). Existing tests cover altered body/hash, invalid source, revoked authority, foreign/mutated cache/index and restored exact rebuild.
- Fresh-process R03 -> R04 partial resume -> R05/P41 first consumer: **1 PASS** (`p41-first-consumer.log`).
- Original native detached-ref control PASS. Full native capture: **53,463,055 bytes exact**, SHA256 `8048dee503f5d42079bae0b4cd43e944b4de60114b3efdd19b7929e70077254b`. Full checkpoint: **28,017 bytes exact**, SHA256 `bbc9a626f1045a22e3f4b0f95b44ef62bc434dd593c55cfd818986978d850f9c`. Equality covers native body/ref, facts/evidence/provenance/replay, checkpoint and P41 consumer values. The capture also requires refusal of a rehashed changed source determinant against its original checkpoint pin. `native.json.xz` preserves the exact full capture losslessly; `native-parity.json` and `checkpoint-0.json` record the comparison.

## Serial resource comparison

Same inherited reviewer harness, same host and synthetic 12-row source. Resource processes ran sequentially after all test and capture processes completed. The only resource-script change is replacing the P1 candidate pin by the repaired source SHA. Raw process JSON/stderr are in `resource-raw`; all commands/statuses are preserved. `MEASUREMENTS.json` verifies exact native/P41 material before summarizing timings and cache counts.

| Run | Wall seconds | Peak RSS MiB |
| --- | ---: | ---: |
| base-a | 25.974 | 237.9 |
| base-b | 27.408 | 237.8 |
| compact-cold | 23.824 | 241.9 |
| compact-corrupt | 26.090 | 244.0 |
| compact-deleted | 24.443 | 243.3 |
| compact-warm | 29.362 | 228.1 |

All four compact runs report zero hot native event reconstructions. Cold/corrupt/deleted runs miss and rebuild; warm runs hit every view. Cache retention remains bounded to sixteen direct-mapped members with per-body sealed identity checks. Cold and rebuilt compact runs use more RSS than eager baseline; the warm run uses less RSS but takes longer than either baseline process. Both timings and RSS vary between processes. These bounded synthetic results do not establish production speedup, cold streaming I02, or other eager-family gains. Original35 S3 science, Sorok, grouped P2, protected CAS and wider semantic/source grants remain outside this commission.

## Reproduction and independent handback

`validation.json`, `resources-status.json`, the two runner scripts, original/adapted harness files, pinned synthetic inputs and PROVENANCE retain exact commands, paths, input bytes, source pin, dependencies, exit codes and host. Reuse the existing `/tmp/rawlsing-oct28-p1r1/venv/bin/python` runner and the recorded baseline/candidate worktrees. The original P1 RED commands are recorded against the original source pin; fixed commands run against `cd1e7ccf8419a000817b4a8535879da56c06db98`. The archived `check_qualified_identity.py` is the original P1-only in-memory amendment proposal; its search for the old allocation assertion is intentionally obsolete on fixed code. The complete tracked test now directly passes under both release paths.

P1R2 handback target is **`cd1e7ccf8419a000817b4a8535879da56c06db98`**, against original P1 `0a63e7c90cabcfd01dbb169d477f2d0ead5be22c` and protected baseline `f58c8400a024d108a8ab9fa814c87967d336ea47`. Receiving reviewer: the same nonauthor P1R1 reviewer at `a7024d244f71e55c5a64e62089ba4c710e6f0059`, or another genuinely independent qualified S2 reviewer. Requested cut: inspect the two exact repairs and v1 contract, rerun RED/GREEN reference courts and the pinned suite/capture/cache/resource courts, and issue its own verdict. This worker does not adopt its own implementation or call its test reruns independent acceptance. No protected merge and no original P1 SHA merge were performed. `CHANGED_FILES.json` lists the repair delta, all inherited production changes versus protected baseline and return-evidence paths. Final branch readback is supplied in chat; the evidence-only return tip preserves the tested source byte-for-byte.

**PASS / CLOSURE_ONLY. No required implementation or background work remains in this commissioned author turn. Independent P1R2 acceptance is the receiving role's next action.**

`PROGRAMMA_OCT28_P1F1_LOCAL_S2_PASS_READY_FOR_P1R2__RETURN_TO_HQ`
