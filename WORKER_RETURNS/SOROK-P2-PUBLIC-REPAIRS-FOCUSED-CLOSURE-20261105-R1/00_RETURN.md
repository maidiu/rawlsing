# SOROK P2 PUBLIC REPAIRS — FOCUSED CLOSURE

## VERDICTS (separate per exact repair)

- `76d5a3d13e0219c1a085ebadd55071de2dd90e7d` interval public-key/receipt repair — **ACCEPT_SCOPED_TEST_ONLY** for the concrete original findings.
- `b71624f21d0bc638e8817f3929cc6c01ab8b0f61` later-event public-boundary repair (code `4bdba46c4d3a667a9cd7845eb57caa980df76373`) — **ACCEPT_SCOPED_TEST_ONLY** for the concrete original findings.

Historical old findings remain preserved: interval `7a256ed` review `89b334` REVISE; later `76fdb624` review `f1a287` REVISE; historical `bdad` REVISE. Integrated `25d40806` remains ACCEPT_SCOPED_TEST_ONLY under review `332e00c`; it is not reopened because the unused old standalone defects were held. No final newer integrated head was provided, so none is assumed or reviewed.

## EXACT COMMANDS AND RESULTS

Snapshots were extracted only under `.local-logs/p2-public-repairs-review/` from Git (accepted product/projection at `41bf` plus the exact repair commits); no author runtime cache, `/tmp`, or shared config.

```text
python3 -B .local-logs/p2-public-repairs-review/probe_interval_public.py
# all focused interval checks true
# admission_status/c9_public present; admission/c9 absent; privacy empty
# evidence/result.json: 29/29 files exist; no pycache/nonexistent entries

python3 -B .local-logs/p2-public-repairs-review/probe_later_public.py
# all focused later checks true
# public CLI/API privacy hits: 0; no engineering keys in public default
# observation: no auto DO_HELP, encounter 0 -> 0
# explicit do-help: exactly one attempt, encounter 0 -> 1; ACTUAL REFUSED, SCHEDULED OK/HELP_ACCEPT
# causal primitives, S43 history, exact source, cut/restore and cold: preserved
```

No full inherited 6/8/7/55 suites were rerun; the original failure oracles were minimally adapted and discriminate the concrete findings.

## INTERVAL 76d — PASSED CONCRETE FINDINGS

- Public result fields now use `admission_status` and `c9_public`; reserved keys `admission` and `c9` are absent from observation, explicit-do-help and interval-only results.
- Projection privacy scan is empty for all three public result paths.
- `evidence/result.json` deterministic authored-file receipt contains exactly 29 actual files, all present; no `__pycache__`, `.pyc`, or nonexistent entries.
- Primary no-auto-help repair was already independently established in review `89b334`; this closure reuses that finding and confirms the renamed public keys/receipt.
- Non-gating limit: `PUBLICATION_RECEIPT.json` still contains final-readback placeholders (`repair_commit`, `pushed_at_utc`); the exact repair head and 29-file receipt are supplied by this review.

## LATER b716 — PASSED CONCRETE FINDINGS

- Public CLI and public API (`run_positive_public`/`run_scheduled_public`/`public_report`) have zero privacy hits; public outputs contain no `c9`, `s43`, `history_refs`, `plan_hash`, `source_event_id` engineering keys.
- Engineering evidence is explicitly opt-in: `run_positive`/`run_scheduled` engineering returns and CLI `--engineering-out` only; default public CLI did not create or emit engineering.
- Positive/scheduled observation performs no user action: SAY/DO_HELP/ATTEND all null, encounter count `0 -> 0`; no auto DO_HELP.
- Explicit `do-help` performs exactly one canonical user attempt (`0 -> 1`): ACTUAL REFUSED/HELP_REFUSE; SCHEDULED_ONLY OK/HELP_ACCEPT with actor REPAIR.
- Causal primitives/source/cold preserved: later events real, event 3 history contains event 2, exact C9 source preserved, S43 ACCEPTED, cold verify true; interval cut refuses `S46_INTERVAL_CONDITION_REVOKED`, restore/continues, cold source/root preserved.
- Non-gating limit: raw engineering functions (`run_positive`/`run_scheduled`/`P2Continuation` returns) remain internal/opt-in, not public default.

## PRESERVED SCOPE AND LIMITS

- Do not reopen accepted integrated `25d40806`; its unused old standalones were held.
- No blanket acceptance of old standalone interval/later surfaces, PRE-MAIN merge, native C8/C9/C12, CAN008/CAN011, ADP, Pyat, B-owned context, human usability, external delivery, security/tamperproof or concurrency.
- No product/guide/global config/protected branch write; all work under `.local-logs` and this review return.
- No new integrated head was provided; no assumption about newer fanin is made.

## EVIDENCE

- `READBACK.json` — exact heads/bases/verdicts and hashes.
- `PROGRAMMA_DELTA.json` / `.md` — compact owner-intake delta.
- `evidence/INTERVAL_PUBLIC_ORACLE.json` — interval public-key/receipt oracle.
- `evidence/LATER_PUBLIC_ORACLE.json` — later public-boundary/causal oracle.
- `evidence/COMMANDS_AND_RESULTS.json` — executed commands and NOT_RUN list.
- `evidence/RETAINED_LIMITS.json` — preserved old findings and non-gating limits.
- `evidence/SOURCE_HEAD.json` — exact repair/component/base heads.
