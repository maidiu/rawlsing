# OCT28-P1R2 — independent acceptance of P1F1 repairs

**Verdict: ACCEPT — bounded SOURCEFREE engineering.**

**P2 ABI: `P2_ABI_SAFE_SCOPED`, selector contract v1 at `cd1e7ccf8419a000817b4a8535879da56c06db98`.** Both P1R1 defects are repaired at this exact production source cut. Independent execution reproduced the original supported-provenance forgery, then verified the unchanged regression passes on the repair; the complete native-allocation equivalence test now passes on eager and compact releases. There are no remaining blockers within this review's stated scope.

**Protected integrator: receive repaired production source `cd1e7ccf8419a000817b4a8535879da56c06db98`, subject to your separate receiving/CAS authority. DO NOT merge superseded original P1 source `0a63e7c90cabcfd01dbb169d477f2d0ead5be22c` alone.** The author evidence tip and this review return are evidence, not substitute production targets. No protected merge or scientific acceptance was performed here.

## Custody and independent execution

| Input | Exact pin |
| --- | --- |
| Reviewed production repair | `cd1e7ccf8419a000817b4a8535879da56c06db98` |
| Author return, read first | `4368b8661386c39cab2ed8b87a3521daad53c57d`, `WORKER_RETURNS/PROGRAMMA-OCT28-P1F1-20261104-R1/00_RETURN.md` |
| Original P1 source | `0a63e7c90cabcfd01dbb169d477f2d0ead5be22c` |
| Original independent P1R1 return | `a7024d244f71e55c5a64e62089ba4c710e6f0059` |
| Protected PRE-MAIN baseline | `f58c8400a024d108a8ab9fa814c87967d336ea47` |
| Review branch | `review/programma-oct28-p1r2-independent-acceptance-20261104-r1` |

The repair is a direct child of original P1. Its delta is exactly four paths: `_pre553_c11_execution_view.py`, `_pre553_query_predicate.py`, `test_pre553_c11_execution_view.py`, and `test_pre553_empirical_query.py` under `rawlsing_next`. The complete repaired source versus PRE-MAIN contains the inherited P1 eleven-path delta plus the existing empirical-query test amendment: twelve paths total. Author source and evidence tips have **no difference in `rawlsing_next`**. Global public `ExactRef`/`AuthorityRef` definitions, C11 seal, authority, decoder, logical hashes and physical-cache schema were not changed by F1.

This is the original P1R1 reviewer continuing as the P1R2 nonauthor. This session did not implement P1F1. The author's recorded worktree is `/Users/matthewsmith/.codex/worktrees/60ed/Rawlsing`; this review tested a separate clean detached worktree at the repaired source, restored the prior exact original-P1 worktree for RED, and reused the clean protected-baseline checkout. No production files or tracked implementation tests were edited by the reviewer. After execution, the review return was placed on an isolated branch from protected baseline. Initial/final source identities, code hashes, command results and live branch checks are recorded in `PROVENANCE.json` and `commands.json`.

Actual S2 host: **oldMac.lan**, macOS 13.7.8 x86_64, Python 3.11.3. The existing authorized synthetic runner `/tmp/rawlsing-oct28-p1r1/venv/bin/python` was reused, with Arrow 22.0.0, pyreadstat 1.3.2, pandas 3.0.6 and pytest 9.1.1. Only pinned synthetic fixture owners and the **12-row, 911-byte SAV** were executed. SAV SHA256: `c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b`. P41 runtime remains pinned to `f27d1101048638bba395143a48efb7ef00bfcda4`. No original respondent source or new host/provider/source grant was used. No author log is counted as this review's execution evidence.

## M1 — retained-reference alias fully repaired at the exercised interface

Originally, an outer-frozen selector retained mutable `ExactRef` children. P1R1's unchanged exploit again changed a valid `SUPPORTED` fact to a different `SUPPORTED` fact containing forged event provenance on **original P1**; the unchanged integrity regression was RED. The native-baseline control passed because native event refs are detached. On the repaired source, that same regression is GREEN. The unchanged exploit exits 1 at its intentional assertion `no exercised selector changed a downstream fact`: its prerequisite exploit no longer occurs. This expected assertion is not misreported as a green execution of the original exploit.

Code inspection verifies that event/native/canonical/component identities are now immutable primitive tuples, dimensions are interned as tuples, and authority identities are tuple-of-tuples. Ref properties construct new detached `ExactRef`/`AuthorityRef` exports. Selection compares retained tuples, so corrupting an exported dictionary cannot rewrite the source-certified selector or any sibling occurrence/respondent. Source native reconstruction still uses the existing exact materializer and original member hash.

An additional independently written court obtained selectors through `_select_respondent_events` and poisoned **90 exported event, question and authority refs across 18 events and 3 respondents**, including repeated occurrences. Every I03 fact remained byte-equivalent before, during and after the writes; fresh ref exports and independent sealed native lookup remained exact. Native materialization was patched to raise during this court's hot executions and was never invoked. The focused tracked dimension test separately supplies actual I02-validated canonical/component bindings and checks both optional dimension refs, native/canonical/component matching, state filters, order and occurrence identity against eager events after descendant faults. It passed independently as part of the 42-test focused suite.

Receipts: `original-alias-exploit.log`, `original-integrity-RED.log`, `fixed-integrity-GREEN.log`, `fixed-unchanged-exploit-refused.log`, `native-baseline-control.log`, `detached-reference-court.log`; executable originals and the additional court are included. This is protection against the demonstrated reachable exported-descendant fault, not a claim of arbitrary hostile Python-memory or concurrent same-UID security.

## M2 — exact native value identity, without allocation identity

The production-test diff replaces only `resolved_event is event` with all three required assertions: native `RespondentEvent` type, exact `ref`, and complete `as_dict()` equality. Every original descendant mutation, detached-export, source-authority, respondent, corrupt-body and requery check remains in that test. It passed through the normal eager suite and through the forced-compact suite. No full native event was added to the hot lane to make an allocation-identity check pass. Ordinary native object lookup and public sequence iteration may reconstruct equal immutable objects without preserving their Python allocation.

## Independent S2 results and exact downstream identities

| Court | Reviewer result |
| --- | --- |
| Original P1 unchanged exploit / integrity regression | Forged supported provenance reproduced / expected **1 failure** |
| Repaired source unchanged integrity regression | **1 passed** |
| Additional detached-reference/actual-I03 court | **PASS**, 90 poisoned exports; zero hot native event realizations |
| Pinned related suite | **209 passed, 1 skipped** |
| Focused compact/cache/facade/Route B suite, including both F1 regressions | **42 passed** |
| P1R1 independent query/cache/index courts | **9 passed**; 13 pinned native/compact query executions, 16 slots, 80 collisions |
| Existing I03/frontier/I05 suite forced onto compact releases | **60 passed**, including full M2 immutability test |
| Cache body-hash check sever/restoration, in memory only | **PASS → expected RED → restored PASS** |
| Fresh-process R03→R04 partial checkpoint/resume→actual R05/P41 | **1 passed** |
| Full baseline/repaired native and checkpoint captures | **Byte-identical** |

The sole related-suite skip is the existing installed pyreadstat Stata extended-missing metadata capability limitation. It does not skip the selector or downstream parity courts. The inherited P1R1 harness originally reflected dataclass backing fields; this review changed only that reflection to the same ten documented public selector fields. No semantic expected value or fixture oracle was changed. `force_compact.py` changes repository realization in memory, preserving existing I03/frontier/I05 expected outputs and negative cases; it does not edit production code or tests. Full command argv, exact cut, exit status and expected-RED handling are preserved in `commands.json` and `run_review.py`.

Exact independent results:

- Native capture **53,463,055 bytes**, SHA256 `8048dee503f5d42079bae0b4cd43e944b4de60114b3efdd19b7929e70077254b`.
- Checkpoint **28,017 bytes**, SHA256 `bbc9a626f1045a22e3f4b0f95b44ef62bc434dd593c55cfd818986978d850f9c`.
- Selected P41 view `c6aaef3c9816cdd63601703f4de52adf58d86ef0382adccb7cb6764f53812cf5`.

The capture independently compares complete native bodies, refs, facts, empirical evidence, provenance, replay, checkpoint and P41 consumer material to protected baseline. It changes the actual checkpoint source SHA and recomputes internal hashes; the original external checkpoint pin still refuses with `JOINED_CHECKPOINT_PIN_MISMATCH`. Restoration reaches the same view. The preserved native capture is losslessly compressed as `native.json.xz`; `native-parity.json` records equality and the actual negative determinant.

Cache tests independently exercise same-key altered content with retained metadata, foreign metadata, truncation/deletion/rebuild, interrupted atomic publication, private root/member permissions and final-component symlinks, current workload revocation before cache access, unsupported Arrow fallback, same-release changed index payload and cross-source substitution with E3 recovery. Sixteen direct-mapped committed slots bound member count. Source validation and I02 remain prior to persistent accelerator loading; current source/authority/query gates and replay owners remain in place. No new persistence bypass is introduced by the ref repair. Crash/power-loss durability, ancestor-directory races, arbitrary-memory attacks and a global byte bound are not established by these tests.

## Frozen P2 selector contract v1 and first consumer

The actual runtime module defines `_SELECTOR_CONTRACT_VERSION = 1` and documents the following narrow handoff; its test asserts version 1. Qualification is tied to the reviewed source SHA, not to nominal annotations alone.

```python
_select_respondent_events(
    index: _ReleaseIndex, respondent_key: str, target: ExactRef,
    *, native_only: bool = False, include_component: bool = False,
    states: frozenset[str] | None = None,
) -> Iterator[RespondentEvent | _EventRead]
```

Native fallback yields original native events; compact selection yields selector values. Supported fields are `schema_id`, `ref`, `typed_state`, `native_question_ref`, optional `canonical_question_ref_if_authorized` and `component_or_subitem_ref`, `authority_snapshot_refs`, raw/canonical response values, multiplicity/order/rank material, and occurrence id/index. `schema_id` is `RespondentEvent`. Exported compact refs are **detached, not themselves intrinsically unmodifiable**; modifying them must not modify retained truth. Semantic values retain their recursively frozen canonical representation. Normalize native mapping refs versus compact typed refs through existing exact-ref helpers.

`native_only` excludes canonical/component matching regardless of `include_component`; otherwise native/canonical match and optional component match apply. `states=None` is unfiltered; an empty set selects no rows; a missing respondent key raises `KeyError`. Exact I02 order, duplicate occurrences, respondent/universe grouping, complete respondent membership, risk/denominators, weights, zero-domain and typed-negative semantics are preserved. Ordinary `events_by_respondent` sequence iteration/indexing reconstructs native events; it is not the compact computation operation. Dataclass backing names, Arrow buffers and Python allocation identity are not part of v1.

First real readers are existing predicate leaf evaluation in `_pre553_query_predicate.py` and `_target_component_value` in `_pre553_query_eval.py`, reached through `CarrierNeutralResearchExecutor.execute_i03` → `execute_empirical_query`. I05 continues through the existing discovery engine, then Batch/R04 and the actual R05/P41 consumer. There is no second I03 semantic engine.

P2 must stay behind those entrypoint gates and exact repository/release/universe resolution. `_release_index_for` retains E3's repository-scoped attestation and rebuilds foreign/replaced/missing-attestation indices. A direct `_build_release_index` call alone grants no source/query/authority permission. Grouped/result sharing must include the actual predicate, target plan, risk/weight/design/source-scope and authority determinants as applicable, beyond reusable topology. Do not treat a retained positive as current authorization. Compact selectors provide no arbitrary native `as_dict`, `semantic_projection`, `schema_version`, source/row fields or unapproved extensions; use sealed release/index context and native exact resolution. P2 may not depend on Parquet files, `_EventLane.bodies`, `_CompactPublicObjects.entries`, Arrow, environmental cache paths or unsealed cached identifiers as scientific source.

## Resource evidence and retained limits

| Run | Joined wall | Peak RSS (B) | Hits / misses / publications |
| --- | ---: | ---: | ---: |
| base-a | 23.716 s | 248,868,864 | 0 / 0 / 0 |
| compact-cold | 23.925 s | 255,291,392 | 4 / 2 / 2 |
| compact-warm | 23.963 s | 255,160,320 | 6 / 0 / 0 |
| base-b | 23.789 s | 249,229,312 | 0 / 0 / 0 |
| compact-corrupt | 23.953 s | 250,347,520 | 4 / 2 / 2 |
| compact-deleted | 24.257 s | 257,720,320 | 4 / 2 / 2 |

All compact runs retained 36 compact events, zero full event envelopes in that representation and zero native hot-event reconstructions. Each process opened one 911-byte source snapshot. The release remains 92 public / 15 internal objects; the Arrow body lane is 118,512 B. Two compressed members occupy **41,708 B**; largest staged member **20,854 B**; maximum active-plus-staged footprint under corruption recovery **41,727 B**. Cold and warm RSS exceed both baseline readings in this run; no whole-process memory improvement is demonstrated. Resource native-material digest is `5dd623dbfd4eb6b837644f84ccf4a2579d7403462d0c08fe26c4aff3d98e5287`.

Resource processes used the same pinned harness/source and exact baseline/repaired cuts, sequentially, with cache cold, warm, corrupted and deleted states. Full raw JSON/stderr and a parity-checking summary are included. Baseline A overlapped compression of the already-verified capture receipt; this is a disclosed timing confound. No speedup is inferred from this series. Other host load was not controlled. Cache counters and exact identities establish warm reuse and corruption/deletion recovery; RSS/timing variability cannot establish a broad memory or production gain.

This accepts the respondent-event first slice and its exact repairs. It does **not** complete cold streaming physical projection/I02 validation, compact other eager record families, avoid current source reopening on warm execution, prove 16-GiB or large-production behavior, implement grouped P2, or issue original35 scientific/source/actor rights. W03/W04's larger slices remain as in P1R1; no new blanket architecture or owner is created. The selected hybrid's outstanding work is not erased by these greens.

## Receiving and terminal disposition

**Engineering:** ACCEPT the exact scoped P1+P1F1 implementation at `cd1e7ccf8419a000817b4a8535879da56c06db98`; both original blockers are closed and internal selector v1 is safe within the above gates and limitations. **Scientific/source/actor authority:** unchanged; no original35 S3, U/E_pre, N11, Sorok or broader grant is inferred. **Protected adoption:** remains the separate integrator's action, after refreshing PRE-MAIN and checking the exact receiving delta/cut. No self-merge or author self-acceptance occurred.

The protected integrator should receive **the repaired source SHA**, not superseded original P1 `0a63e7c90cabcfd01dbb169d477f2d0ead5be22c` alone, and not author evidence tip `4368b866…` as a production substitute. This review's source qualification does not automatically transfer to a different code cut. The complete independent return, executable courts, command/negative/resource receipts, native capture and SHA256 manifest are committed and pushed on the named review-only branch. This reviewer stops at that handback.
