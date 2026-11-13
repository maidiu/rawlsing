# PYAT960 Q2 S1-E — A counter handoff

**Role:** A_COUNTER · **session:** `ses_e3122f686ffeByL78cGOKAacTS`
**Fixed rival:** B `ses_e3120baacffegE3ZnR5uZcHb0N`
**Branch:** `agent/pyat960-s1e-a-r1`
**Base:** `591056a948fb0fdd68adbd581301dd903485adc8`
**B delivery:** `ed9bda50ec1c1cbbc0ced56262a696b65fb14dad`
**B code cut:** `9987a00e10dbb4e2dca7032b7d66a90e2303c780`
**A previous code cut:** `75d09e87dbaf8273fab3a5ece2bb7981328113ce`
**A-counter implementation SHA:** `047298f9d6bff987f319c686aae336baba07cf9e`
**Contract v1 SHA-256:** `0ed0384411441b2f647dc5ea3369931c88d408c71802ec8cd7eaff00c3052a40`
**Provisional ABI SHA-256:** `cbc8988b6f38fc354311d7db7afe02a5bd66c8e53ab2c6f9cca2b5134d383f54`

**Stop state:** `READY_FOR_RECEIVING` (same fixed B next, then distinct nonauthor G5)
**G5:** `NOT_RUN` · **Integration:** `UNMERGED` · original task not complete.

## 0. S01–S05 / reuse acknowledgements

- **S01:** R157 source meaning/entitlement reused; original35 CURRENT/source rights remain HOLD.
- **S02:** S1-C frozen operation/fate census reused; B's source-body realization anti-join retained.
- **S03:** One compact direct I02 certificate plus B's body-preserving 13-family tee; no Q3 writer claim.
- **S04:** Actual Q2-driven native I03/Batch fact now **SUPPORTED** on the existing Linux `s2b` runner (details below); full S2-D all-consumer work remains separate.
- **S05:** learned products untouched.
- **Selected destination:** Oct28 respondent-coherent typed C11 + Nov11 compact direct I02; no compulsory full-object `C11LogicalRelease`, no permanent second body corpus, no new statistical engine.
- **Reuse:** R157 adapter/decoder/facade, S1-C census, S2-B direct builder/certificate/native selector/query math. **Rejected physical order:** old full-object-first producer/W03/W04 retention as Q2 foundation. W03/W04 remain USER_PAUSED.
- **Old W03/W04 pilot:** matched candidate peaked at `6,468,513,792` B, above the `6,442,450,944` B cap and was killed. No 100k/6 GiB claim.
- **Named first consumers:** `build_sourcefree_direct_i02`; existing `VerifiedExternalI02` + `install_direct_sourcefree_i02_i03`; existing native `execute_empirical_query`.
- **Owner/lease:** only this new worktree/branch and A_COUNTER return were written. B/A returns, Q3, upstream owners, protected facade, W03/W04 and controller are read-only. Linux `s2b` was reused only as the existing private runner/codecopy and cleaned afterward.

## 1. B strengths accepted

B's return is substantive. I independently accept and preserve:

- `SourceI02BodyTee` / `SourceI02BodySink`: 13-family body transport on the same one-shot builder consumption; no second source read; finish/abort ordering and certificate invalidation.
- Source/operation realization anti-join for eligible operations, unprojected/held operations, occurrence dimensions and emitted-body counts.
- Honest `source_reads`, prehash/snapshot/decode/cell-pass counters and cleanup/invalidation.
- Linux native selector proof: certificate 5 events, native-selected 5/5 exact refs, reader closed.
- Existing S2-B native suite: 81 passed on Linux.
- 30 B Q2 tests, 33 inherited S1-B tests, 18 S1-C tests, 56 decoder/custody pass + 1 skip.

## 2. B's native-fact HOLD resolved

B correctly kept the full Q2 native fact as HOLD rather than faking it, but did not adjudicate its exact cause. I reproduced the Linux `native_query_probe` and printed the otherwise-hidden `execution_detail`:

1. First failure: `routing/risk-set fact lacks exact ROUTING_RISK_SET authority`. The sourcefree fixture's routing snapshot used the generic `SOURCE_SEMANTICS_TOPOLOGY` kind. This is an engineering fixture omission: the existing native owner requires the existing `ROUTING_RISK_SET` authority kind.
2. Second failure after correcting the kind: `realized exact target cell is absent from the query-declared full target domain`. The test query declares domain `0/1`, while the sourcefree config emitted canonical values `0.0/1.0`. Correcting the fixture's canonical spelling to `0/1` (same raw values and response states) resolves it.
3. With those two sourcefree fixture corrections, the existing native query returns **SUPPORTED**: raw numerator/denominator `5/5`; changed valid branch operation returns `3/3`; exact restore returns the original fact ref and raw `5/5`. No new engine, science, production CURRENT or original35 right was added.

Exact actual native fact evidence (`evidence/native_fact_GREEN.json`):

- Base fact: `urn:rawlsing:pre553:EmpiricalFact:sha256:e25ec9ff75b5840fc62511de0fcc22bf7d3bf588419e304bd1c982581dbef685`, SUPPORTED, raw `5/5`.
- Changed valid branch operation: `...03ff3852a9770eb3fa8b4422ff25de5d41822261cc62f3bb86b2d62e860405f9...`, SUPPORTED, raw `3/3`.
- Restored fact: exact base ref, raw `5/5`; direct logical root restored.
- Detail: `exact governed target distribution resolved`.
- Fixture corrections: existing routing authority kind `ROUTING_RISK_SET`; canonical values `0/1` matching the query's declared domain. These are sourcefree engineering preimages, **not** original35 science or a new production issuer.

The Q2 native selector remains 5/5 exact on Linux (`evidence/native_selector_GREEN.json`).

## 3. New counter defect found and repaired

B's source/operation anti-join still had a real multi-owner hole:

- Config with a valid multi-owner slot (q101 response **and** coordinate) plus all routing `ROUTING_UNKNOWN`.
- B's guard used `response_only = all(family == RespondentEvent ...)`, so the presence of the coordinate owner disabled the routing-denominator check.
- The handoff **accepted** an eligible response operation with no eligible routing body realization.
- My fix changes both the pre-source and post-source checks to `response_owned = any(...)` and only examines RespondentEvent sections when applying routing-state checks. Valid multi-owner eligible routing remains accepted; unknown routing now refuses before source.
- Actual RED/GREEN: `evidence/multiowner_RED.txt` (B code accepted) and `evidence/multiowner_GREEN.txt` (A code refuses with `OPERATION_ROUTING_FATE_MISMATCH`).

This is a Q2 G3 source/operation/routing realization defect, not speculative hardening.

## 4. Tests and resources

- Q2 Darwin: **32 passed, 1 skipped** (`VerifiedExternalI02` host skip).
- Q2 Linux s2b: **33 passed** (including native fact).
- Existing S2-B native suites Linux: **81 passed**.
- S1-B inherited: **33 passed**; S1-C: **18 passed**; decoder/custody: **56 passed, 1 skipped**.
- Resource (`evidence/resource.json`): 1,200 rows, 1,200 events, 1,200 coordinates; source byte pass 1, decode 1, cell pass 1, direct builder 1, full C11 0; spool 7,464,000 B cleaned; certificate 19,369,984 B; peak disk 46,223,669 B; peak RSS 128,163,840 B; cold 6.341 s/repeat 6.261 s; denied source opens 0. 100k/6 GiB NOT_RUN.

## 5. Remaining attack surfaces

- Body sink is caller-owned; Q3 must stage/commit only in `finish`. The adapter enforces ordering/invalidation but not a third-party sink's internal publish policy.
- Partial routing: Q2 handoff preserves routing states; native query correctly returns `RISK_SET_UNAVAILABLE` for partial unknown rather than a false supported fact.
- Full S2-D all I03/I05/Batch/resume is not claimed; one Q2 native fact is the canary.
- Keyed source handoff still requires an external key-witness read; one Q2 pass plus that external read.
- Original-source path retains S1-B prehash + snapshot (2 byte passes); sourcefree fixture path is one pass.
- Original35 native science/rights, S1-D production CURRENT, protected merge and 100k/6 GiB remain HOLD.

## 6. Disposition

`READY_FOR_RECEIVING` at `047298f9d6bff987f319c686aae336baba07cf9e` for fixed B attack and then one distinct nonauthor G5. The direct I02 certificate, body transport, operation/fate conservation, Linux native selector and actual Q2 native fact are demonstrably working at the sourcefree TEST_ONLY grade. No `ACCEPT_SCOPED` is self-issued; integration remains `UNMERGED`.
