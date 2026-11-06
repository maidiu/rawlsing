# Sorok developmental recursion engine R1 — final engineering handoff

**HQ disposition: ACCEPT_SCOPED_SOURCEFREE_DEVELOPMENTAL_RECURSION_ENGINE_R1.** The authorized engineering commission is complete at implementation `81b01f654f8ba09550d03df17e8014f43ffcfc9f`. Later changes contain review evidence and documentation only. Protected start: `33c40a315d3c231cb2021bd8e60f3261547efa62`. Delivery branch: `agent/sorok-developmental-recursion-engine-20261105-r1`. [Selective PRE-MAIN PR #704](https://github.com/maidiu/rawlsing/pull/704) is draft and unmerged.

This disposition combines independently demonstrated valid-path behavior with independently accepted repairs at their exact cuts. It does not rewrite the original REVISE verdict, claim that either focused reviewer accepted everything alone, issue native psychological science, or approve protected receiving. The requirement-by-requirement phase audit and all twelve named deliverables are mapped in [FINAL_DISPOSITION.json](FINAL_DISPOSITION.json).

## What now works

Rawlsing can take a supplied model's proposed group of 3–5 events, realize them in order through an actual actor/world owner, and preserve the state and outcome each leaves for the next. The next model call receives the developing actor's own recorded experience of that completed group. Its retrospective half completes the preceding recursion before the next proposed group runs. Bootstrap invents no previous life; terminal retrospection requires no future group. There is no model call between the group's events.

The functioning consumer is:

`run_developmental_recursion.py → RecursionCycle → BatchEngine → P2Owner → unchanged S39–S47/P2 interval/event/C9 owners`.

A real material interval changes the later C9 eligibility result: ACTUAL participation yields `[false,false,false]`; the SCHEDULED_ONLY control yields `[true,true,true]`. This is computed state dependence, not a comparison of prewritten narrative outputs. The generic engine accepts supplied owners/providers and source-grounded proposals; the controlled P2 workshop is an explicit test fixture, not general engine policy.

## State, actor access and failure boundaries

- SQLite batch history binds root, actor, branch, clock, proposal identity, before/after state, actual outcomes, source readsets and receipts. Completed replay does not repeat effects. Interrupted operations reuse the same idempotent owner operation or remain explicitly ambiguous; unknown P2 effects are never blindly reissued.
- New batches reject inverted, equal or nonfuture event times before claims/effects. Every explicit native history ID/hash is checked for existence, actor/branch, duplicate and chronological grounding before the first interval. Historical partial records are preserved.
- Actor experience uses the actual E1/action hash and the developing actor alias's native perception receipts. Missing actor receipts produce HELD even when portal-user receipts exist. The public user view is not substituted. Default CLI output contains event IDs/status, not actor-private experience.
- Explicit non-null language contexts are checked against native S43 schema and its actual registry before effects. Omitted/null keeps the native default. Supported explicit contexts are actually realized and retain their S43 identity through cold reopening.
- A registry-known context can still be incompatible with the eventual native event intent. That is a recorded native semantic refusal with `performed=false`/HELD experience and its actual interval, not an untracked exception or a promise that the actor performed the action. No new preflight policy for every possible semantic outcome is claimed.
- The provider receives detached accessible history and cannot write canonical actor state. Retrospective impressions remain proposals. `MISSING_RULE` remains distinct from evaluated `NO_CHANGE`.

## Exact independent qualification

| Return | Exact subject | Disposition and demonstrated scope |
|---|---|---|
| `ec8724b6db51cb5fd10216660ad6fe3d7c970b58` | `41863919210021eced174ad5abdf49cb2df2042a` | Original integrated REVISE: R1 actor-view substitution, R2 late native grounding, R3 chronology. Independent 66 / P2 baseline 7, state/material dependence, correct recursion boundary, cold/crash/exclusion and sever/restore facts remain valid at that scope. |
| `13f01945c559e704344b40b462c76950e7843c3e` | `7c4907d0b5c42eaf0f6eb92a538516453a922933` | ACCEPT_SCOPED repaired actor access, chronology and native-history grounding; independent 70 tests and actual two-batch/cold CLI. |
| `b4cbf2136821ed89986774e163202c3703fab019` | `81b01f654f8ba09550d03df17e8014f43ffcfc9f` | ACCEPT_SCOPED last R2 native-context delta; independent 5 owner tests, target assertion-level sever/restore, later-proposal negatives, actual default/null/workshop/family realization and cold S43 preservation. |

The only runtime delta from 7c to 81b is the reviewed 11-line native-context preflight. Engine, coordinator, contracts and CLI are otherwise unchanged. Current code/test hashes match 81b and [SOURCE_PINS.json](SOURCE_PINS.json); the review manifests, exclusive write scopes and remote review heads were verified. All three returns are retained unchanged in their respective `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-*REVIEW/RECHECK-R1` roots.

The lead's recorded host/model is GPT-6.1 Sol/High, with the exact verification turn in CHECKPOINT.json. OpenCode implementation/review used the existing Go DeepSeek V4.1 Flash MAX setup; actual assistant-message provider/model/variant metadata was verified for both rechecks. Quota is UNKNOWN. No Codex subworker, UI manipulation, provider/account/region change or protected merge was used.

## Measured execution and reproduction

Current combined author suite: **71 passed in 279.35s**. Three cold processes independently exercise BOOTSTRAP/ORDINARY/TERMINAL: 3+3 events, two retrospectives, same root, clock222→258, zero between-event model calls. The independent repaired-boundary review repeated the70-test prior cut and cold CLI; the final-context review independently qualified the added native boundary. Actual six-event state/readset/receipt evidence is in [evidence/MULTI_BATCH_EXECUTION_RECEIPT.json](evidence/MULTI_BATCH_EXECUTION_RECEIPT.json); cold receipt is [evidence/cold_cli.json](evidence/cold_cli.json).

From this exact repository checkout with its pinned P2 closure and Python/pytest dependencies:

```bash
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests
python3 -B WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/run_cold_cli_witness.py /tmp/sorok-recursion-cold.json
```

The first-consumer CLI also exposes bootstrap/advance/finish with explicit state root, source pack, journal, cycle store and model-response file; see `run_developmental_recursion.py --help`. These reproduction commands use permitted sourcefree fixtures, not original respondent execution or a validated generated person.

Source sensitivity is demonstrated by actual interval→later-C9 severance, retrospective-boundary severance, actor-perception removal/restoration and final native-context preflight removal/restoration. The unchanged PRE-MAIN proof checker also detects the actual material edge and live P2 first reader; exact source restoration is retained. Crash/cross-process receipts prove durable reservations and zero duplicate effects.

## Inheritance, scientific frontier and next code edge

[REUSED_VERSUS_NEW.md](REUSED_VERSUS_NEW.md) and [evidence/source_capital_disposition.json](evidence/source_capital_disposition.json) distinguish accepted S39–S47/P2 reuse, extant S48–S52 candidates and historical V3 capital. Existing event/state/world owners were not rebuilt. S48's single-prospective turn is not the settled 3–5 recursion. S49 current-owned B context and S52 independent paid counterpart remain unavailable/unqualified; their candidate code is retained, not declared absent. Exact historical V3 archive/dependency mismatches remain explicit, including matching individual files whose state closure does not match.

Original CAN008/010/011/012, ADP015/016/017/019 and MUST018 jurisdictions are preserved. Existing semantic authority documents are not new production/native issuance. ADP016 memory is distinct from objective history, actor accessibility and rendered impressions; M6 claim envelopes and SDTF rule binding are not psychological rule execution.

**The first unsupported native causal chain is rule-qualified impression-dependent memory formation and interconnected durable psychological change on a compatible original actor/root.** This engine does not turn observations or prose into acquired beliefs, practices, personality or attractor transitions. P2's participants remain controlled sourcefree fixtures; independently owned B and human validity are not claimed.

The next functional integration edge is a qualified developmental/memory writer supplied through the existing `DevelopmentOwner` ABI with its actual compatible state, issued rules, receipts and consumer rights. This handoff creates no new commission, generic backlog or permission to invent those sources.

## Protected receiving

The actual native/product owners, protected governance, CI checker/workflow and existing Pyat code are unchanged. Canonical-tree and changed-test proof checks pass. The inherited Pyat bounded court remains RED: **3 old hash-pin failures  / 144 passes**, independently traceable to unchanged protected-base code/manifests/tests. See [evidence/receiving_ci.json](evidence/receiving_ci.json); no unrelated repin, test weakening or full governed-green claim is made.

PR #704 prepares the accepted sourcefree engineering tranche for the competent PRE-MAIN receiver. Protected CAS merge, original source/Pyat N11/N12/native C4/C8/C9/C12 rights, original scientific issuance and human receiving remain with their existing owners. They are not exercised by this completed engineering commission.
