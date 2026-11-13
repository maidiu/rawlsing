# PYAT960 Q2 S1-E — B independent attack/repair handoff

**Role:** B_INDEPENDENT_ATTACK_AND_REPAIR · **session:** `ses_e3120baacffegE3ZnR5uZcHb0N`
**Fixed opponent:** A `ses_e3122f686ffeByL78cGOKAacTS`
**Branch:** `agent/pyat960-s1e-b-r1`
**Base:** `591056a948fb0fdd68adbd581301dd903485adc8`
**Received A HEAD:** `f4aaf2b17c7519642bb0bcfc5987cf21f86a46af`
**A code cut:** `75d09e87dbaf8273fab3a5ece2bb7981328113ce`
**B code cut:** `9987a00e10dbb4e2dca7032b7d66a90e2303c780`
**Contract v1 SHA-256:** `0ed0384411441b2f647dc5ea3369931c88d408c71802ec8cd7eaff00c3052a40`
**Provisional ABI SHA-256:** `cbc8988b6f38fc354311d7db7afe02a5bd66c8e53ab2c6f9cca2b5134d383f54`
**Disposition:** `HOLD_EXTERNAL` for the full Q2 native I03/Batch fact · **G5:** `NOT_RUN` · **Integration:** `UNMERGED`

## 0. Required S01–S05 / reuse acknowledgements

- **S01:** governed source meaning/current entitlement. R157 source config, projection, decoder and admission are reused; original35 CURRENT/source rights remain HOLD.
- **S02:** exhaustive qualified operations/fates. S1-C `verify_frozen_inputs` is reused; B adds exact source-body realization and operation preimages.
- **S03:** one compact direct I02 certificate; B adds the missing 13-family body-preserving seam for a future source-direct estate. No Q3 writer is claimed.
- **S04:** native I03/Batch. On the existing Linux `s2b` runner, the Q2 certificate drives native selector **event bodies** (5/5 exact refs). A Q2-driven full native empirical fact returns `UNAVAILABLE / MISSING_REQUIRED_AUTHORITY`; it is a typed HOLD, not a pass. The upstream S2-B 81 native tests pass with their properly constructed fixture.
- **S05:** learned products untouched; not a Q2 claim.
- **Selected destination:** Oct 28 respondent-coherent typed C11 + Nov 11 source-direct compact I02, no compulsory full-object `C11LogicalRelease`, no second authoritative body corpus, no universal SQL semantic owner.
- **Reuse vs replaced physical order:** reuse source/decoder/projection/census/direct builder/external certificate/native selector/query math. Reject the old full-object-first producer and W03/W04 full-object order for Q2. The legacy full-object release remains a test-only comparator/sealed body fixture.
- **Known failed W03/W04 pilot:** the matched saved-artifact candidate peaked at **6,468,513,792 B**, above the **6,442,450,944 B** cap and was killed. W03/W04 remain USER_PAUSED; no resume or acceptance.
- **Named first consumers:** existing `build_sourcefree_direct_i02`; `VerifiedExternalI02` + `install_direct_sourcefree_i02_i03` + native selector event bodies; full native empirical query owner. G5 is not self-issued.
- **Owner/lease:** only this new worktree/branch and `WORKER_RETURNS/PYAT960_S1E_B/` written. Upstream owners, A/Q3 returns, protected facade, W03/W04 and controller untouched. The existing Linux `s2b` Lima VM and its existing venv were used read/write only under a private temp copy, then removed.
- **Highest-risk false-green:** treating the direct certificate's metadata/selector SQLite as a body estate; treating the Q2 native selector event read as a full native I03/Batch fact; or treating a self-rehashed root as external trust.

## 1. Exact artifact

Code/test cut `9987a00e10dbb4e2dca7032b7d66a90e2303c780`:

- `rawlsing_next/pre553_source_i02_handoff.py` — A handoff extended with body sink, source/operation anti-join, honest open counters, fail-closed cleanup/invalidation.
- `rawlsing_next/pre553_source_i02_streams.py` — new bounded synchronous 13-family body transport.
- `rawlsing_next/tests/test_pyat960_s1e_support.py`
- `rawlsing_next/tests/test_pyat960_s1e_body_transport.py`
- `rawlsing_next/tests/test_pyat960_s1e_operation_antijoin.py`
- `rawlsing_next/tests/test_pyat960_s1e_native_bridge.py`

Return artifacts:

- `WORKER_RETURNS/PYAT960_S1E_B/receipt.json`
- `00_HANDOFF.md`
- `all35_ledger.json` — 35 IDs, 18,276 inherited identities, 18,413 slots, exact 26 unjoined IDs.
- `reuse_matrix.json` — 15 function-level entries with path/blob/disposition/first consumer/no-loss/reason.
- `reproduce_a_defects.py`, `resource_probe.py`, `native_probe.py`, `native_query_probe.py`, `evidence/`.

## 2. Independently verified A strengths

A’s direct I02 builder is real. It runs generated nonrespondent SAV/DTA bytes through R157 projection and the existing direct builder, returns exact `ExternalI02Roots`, and survives changed-source-meaning/restore. A’s S1-C census/anti-join is substantive (18 inherited tests pass). A’s host disclosure was honest: Darwin cannot open `VerifiedExternalI02`; the existing Linux runner resolves that host limit. A correctly kept native I03/Batch HOLD rather than substituting a mock. A’s direct certificate also reconstructs release/source/replay identities sufficient for the existing native selector bridge on Linux.

## 3. Defects established

All red evidence is in `evidence/red_at_75d09e87.txt`.

1. **Body-dropping handoff (SEV-1 for the Q3-required producer ABI).** A’s certificate stores refs/selectors/state but no canonical body. `build_source_i02_handoff` consumes the 13 family iterables, deletes the JSONL spool, and returns roots/manifest/audit only. Q3 cannot consume a completed certificate as a body estate. The A implementation has no `body_sink` parameter.
2. **Operation/fate integration was label-only (SEV-1).** A accepted:
   - eligible operations targeting an unprojected `HELD_NOT_SUPPORTED` physical slot (45 operation fates, no body),
   - an ELIGIBLE response operation when every routing fact was `ROUTING_UNKNOWN`,
   - eligible operations targeting q101 with `option_id="9"` absent from the source mapping.
   Each produced a certificate and copied operation labels without an actual body realization check.
3. **Hardcoded source opens (SEV-2 honesty).** On the original-source path, instrumentation shows one prehash + one snapshot acquisition = **2 actual source byte passes**, but A reports `source_reads=1`. The fixture path is genuinely one.
4. **Cleanup / retained-disk accounting (SEV-2).** A’s spool cleanup swallows rmdir errors and has no sink failure path. A’s `evidence/resource.json` says `retained_disk_bytes=0` while the certificate is 19,345,408B; A’s receipt reports 19,345,408. The historical record was not rewritten; B measures the current artifact directly.
5. **Native host HOLD (not a defect, but a blocked evidence grade).** On Darwin the existing native reader refuses `/proc/self/fd`. On the existing Linux `s2b` runner, the Q2 direct certificate drives native selector event bodies 5/5. A full Q2-driven native I03/Batch fact returns `UNAVAILABLE / MISSING_REQUIRED_AUTHORITY`; the observed Q2 synthetic config has `replay.predicate=NOT_APPLICABLE` and no query-authority preimage was supplied. B did not adjudicate the exact root cause beyond that observed state.

## 4. Corrections implemented

### 4.1 Body-preserving 13-family transport

`pre553_source_i02_streams.py` adds a caller-owned `SourceI02BodySink` and `SourceI02BodyTee`. While the existing direct builder consumes the one-shot sections, the same exact canonical/internal objects are synchronously `emit`ted to the sink. Typed absences are delivered exactly once. `finish` receives the already-published `ExternalI02Roots`, manifest and 13-family counts; `abort` discards staged sink output. The adapter also invalidates its own certificate if the sink or builder fails after publication; spool cleanup is verified.

This is **not** a second source read, a permanent body store, a second semantic engine or a Q3 writer. It is the Q2 producer ABI the Q3 preflight said was missing.

### 4.2 Source/operation/fate anti-join

The handoff now carries exact operation preimages (source authority, source decision, meaning, operation hash, occurrence IDs, science fate refs, U/S/Epre refs) and verifies:

- every ELIGIBLE target/condition item has a projected semantic owner;
- every ELIGIBLE operation has an emitted body for each key;
- response targets have an eligible source-routing denominator;
- occurrence dimension `option_id`/`form_id`/`repeat_id` is represented in the source mapping, or is a typed HOLD;
- held/unknown operations may target preparation material but are returned with `source_realized=false`, `unrealized_keys`, typed held state and native HOLD; they are never silently positive.

The anti-join runs pre-source for config/projection-impossible cases (projected owner, routing, occurrence) and post-source for emitted counts. Orphan, all-routing-unknown and option-9 defects now refuse before source.

### 4.3 Honest counters and cleanup

`SourceI02Stats` now reports `source_prehash_passes`, `snapshot_acquisitions`, `decode_calls`, `key_witness_passes`, `cell_passes`, `full_c11_builds`, `source_open_model`, `spool_bytes`, `spool_files`, `cleanup_complete`. Fixture path reports one byte pass; original path reports two (prehash + snapshot); keyed path reports one handoff read plus one in-handoff key-witness pass, with the external key-witness source read disclosed separately. Spool cleanup is checked; failure invalidates the certificate.

### 4.4 Linux native evidence

On the existing `s2b` Linux VM with its existing Python 3.11 venv:

- Q2 30 tests: **30 passed**.
- Native selector: certificate 5 events, native selected 5 events, refs equal, reader closed, body transport complete.
- S2-B external/direct/verified native suites: **81 passed**.
- Full Q2-driven native empirical query: one `UNAVAILABLE` fact with `p02_failure_state=MISSING_REQUIRED_AUTHORITY`; not claimed PASS.

## 5. Proof of improvement

### Darwin

```text
python3 -m pytest -q rawlsing_next/tests/test_pyat960_s1e_*.py -o addopts=''
30 passed in 4.12s

python3 -m pytest -q rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py -o addopts=''
18 passed in 86.83s

python3 -m pytest -q [B01-B09 four files] -o addopts=''
33 passed in 77.35s

python3 -m pytest -q [decoder/custody four files] -o addopts=''
56 passed, 1 skipped in 9.47s
```

Darwin S2-B native files are host-blocked: `32 failed, 49 passed`, all cold failures `descriptor-pinned SQLite cold verification requires Linux /proc/self/fd` (evidence `s2b-host-hold.txt`, `s2b-host-dependency.txt`). This is the preserved host boundary, not a Q2 regression.

### Linux `s2b` (existing runner)

```text
Q2 tests: 30 passed in 7.41s
S2-B native suites: 81 passed in 32.86s
native selector: certificate_event_count=5, native_selected_event_count=5,
                 native_selected_refs_equal_certificate=true
native query:    UNAVAILABLE, MISSING_REQUIRED_AUTHORITY
```

### Resource receipt

`evidence/resource.json`:

- 1,200 rows; 1,200 events; 1,200 coordinates; 0 weights.
- Cold: source byte passes **1**, snapshot 1, decode 1, direct builder 1, cell pass 1, full C11 **0**.
- Repeat: the same one-pass counts.
- Spool 7,464,000B, 3 files, cleaned.
- Retained certificate 19,337,216B; peak disk 46,158,133B; scratch 7,464,000B.
- Peak process RSS 127,545,344B; baseline 119,353,344B.
- Cold 5.978842s; repeat 5.571991s.
- Denied-read source opens 0.
- 100k respondent / 6GiB integrated gate **NOT_RUN**; no S2-C/S2-D economics claimed.

## 6. Challenges refuted

- **A’s direct I02 is fake / only metadata:** refuted. Native selector event bodies 5/5 exact refs on Linux.
- **Native HOLD is purely host:** partially refuted. Native selector event bodies work on Linux. The attempted full Q2 native fact returned `UNAVAILABLE / MISSING_REQUIRED_AUTHORITY`; the Q2 synthetic config has `replay.predicate=NOT_APPLICABLE` and no query-authority preimage was supplied. B did not adjudicate the exact root cause. The S2-B 81 native tests show the owner works with a properly constructed fixture.
- **A’s operation/fate census is wholly label-only:** the S1-C census layer is substantive; the defect was the missing source-body realization join, now added.
- **Body sink requires a second source read:** refuted. The tee sits on the same one-shot sections; instrumentation shows one source byte pass.
- **The 26 unjoined IDs can be treated as Q2 operations:** refused; they remain preparation-held, never slots/operations/science.

## 7. New attack surfaces

- The sink is caller-owned; the adapter enforces finish/abort ordering and its own certificate invalidation, but a third-party sink that publishes before `finish` is outside the adapter’s control. Q3 must stage and commit only in `finish`.
- The operation anti-join depends on source config sections/occurrence tokens; an external scientific option/crosswalk absent from the config produces a typed HOLD, not a positive.
- Q2 full native fact requires a predicate replay/query authority preimage; the current Q2 synthetic config has `replay.predicate=NOT_APPLICABLE` and no query-authority preimage was supplied. Exact root cause remains a next-turn question.
- Keyed sources still need an external key-witness read; the handoff discloses 1 inward + 1 external = 2 scenario reads.
- Original-source path remains two byte passes (prehash+snapshot); not weakened, not run as a positive.
- Resource evidence is small-fixture only; 100k/6GiB remains a separate integrated gate.

## 8. Surviving disagreements

- Whether Q2 owns a full native I03/Batch fact from its synthetic config or whether that is the distinct S2-D/issued consumer dependency. B kept the exact native fact HOLD.
- Whether a Q2 source config can lawfully carry a predicate replay/query authority preimage without new science.
- Whether the body seam should be a standalone stream factory instead of the co-production tee.
- Whether keyed sources should derive row-native keys in-pass or accept an external key witness.

## 9. Challenge to Agent A

1. Construct or identify a lawfully sourcefree Q2 config with the exact predicate replay/query authority preimage; run a supported Q2-driven native I03/Batch fact on the Linux `s2b` runner with changed/restore.
2. Attack the body sink lifecycle: publish-before-finish, outside-root writes, abort survival, sink failure after certificate publication.
3. Attack the anti-join with multi-owner slots, coordinate/weight targets, partial routing denominators and held unprojected operations.
4. Decide whether keyed key-witness derivation belongs in the single Q2 pass; if so, prove no raw-cell second corpus.
5. Reconcile A’s retained_disk_bytes=0 historical evidence with the certificate without rewriting history.

## 10. Disposition

The direct I02 body transport, 13-family completeness, operation/fate realization anti-join, honest source-open model, cleanup/invalidation and Linux native selector body proof are verified improvements. The full Q2-driven native I03/Batch empirical fact remains `HOLD_EXTERNAL`: the attempted query returned `UNAVAILABLE / MISSING_REQUIRED_AUTHORITY`, the Q2 synthetic config has `replay.predicate=NOT_APPLICABLE`, and no query-authority preimage was supplied; B did not adjudicate the exact root cause. The upstream S2-B native owner passes 81 tests with its own fixture. G5 remains `NOT_RUN`; integration is `UNMERGED`; this is not `ACCEPT_SCOPED`.
