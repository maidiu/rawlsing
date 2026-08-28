# MX03A LiTS-I Named-Source Destructive C11 Replay R1 — Phase A Return

Status: `BLOCKED_MISSING_EXACT_SOURCE_OR_DURABLE_AUTHORITY`

Blocker component: `EXACT_AUTHORITATIVE_LITS_I_SOURCE_BYTES_UNAVAILABLE_IN_WORKER_ENVIRONMENT`

## Execution boundary

Phase A stopped at P0 exactly as commanded. No P1 baseline realization, P2 deletion, P3 fresh-process reconstruction, or P4 parity adjudication was executed.

An isolated scratch workspace was established at `/mnt/data/mx03a_lits1_destructive_replay_r1_isolated`, containing only an isolation marker. No authoritative source, accepted AS2B artifact, production carrier, sibling artifact, or transformed empirical payload was deleted, overwritten, truncated, moved, or mutated.

## P0 verification

Accepted source identity:

- LiTS-I SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- certified shape: `29,002 rows × 1,198 variables`
- physical cells: `34,744,396`
- AS2A-recorded source size: `139,531,180` bytes
- frozen decoder: `decode_dta(source_path, encoding="latin1")`
- accepted AS2B runtime decoder dependency: `pyreadstat 1.3.2`

Accepted durable semantic/replay anchors were readable from exact repository refs:

- AS2A projection authority: `9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06`
- AS2A slot ledger: `65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60`
- AS2A universe ref hash: `834f9be5c5838226abcc9f0af96f2f582eac8bec2944c514ce52680f45faf99f`
- AS2B governed projection: `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`
- AS2B C11 candidate: `7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c`
- AS2B logical C11 release: `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`
- AS2B repository snapshot: `ff8a49d2560fe3cf229f4d5a0f87a14c52d08086a74649968d8c9c9d0225aa77`
- AS2B ReplayManifest: `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`
- respondent identity law: exact source SHA + 1-based physical row ordinal + selected-respondent semantic role; native ID is attribute/provenance only
- proving response slots: `q301_2`, `q301_7`
- proving coordinate slots: `country`, `city`, `region`, `tablec`, `tabled`
- proving weights: none; RAW/unweighted
- routing state: both proving response slots apply to all 29,002 selected-respondent rows

## Missing exact source

AS2B's accepted receipt records the source path as execution-local-only:

`/Users/matthewsmith/Desktop/Rawlsing/data/Data/LiTS_I.dta`

That path is unavailable in this worker environment. Checks also found no `LiTS_I.dta`, LiTS `.dta`, or LiTS `.sav` source under the mounted `/mnt/data` or `/home/oai/share` worker areas.

A known hash, prior receipt, or source-derived C11 identity is not a substitute for the authoritative source bytes. Reconstructing from AS2B receipts would invert the experiment and counterfeit Proposition A.

## Proposition disposition

- Proposition A: `NOT_TESTED__P0_SOURCE_BYTES_MISSING`
- Proposition B: `NOT_TESTED__P0_SOURCE_BYTES_MISSING`
- architecture selection: `NOT_AUTHORIZED_AND_NOT_PERFORMED`
- Phase B: `PHASE_B_NOT_AUTHORIZED__AWAIT_ACCEPTED_LEARNED_RELEASE_AND_VALIDATION_AUTHORITY`

## Exact unblock

HQ must relaunch MX03A Phase A in an execution host where the exact LiTS-I file is mounted and verifies to SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`, with the accepted AS2A/AS2B authority surface available at its exact refs. Only then may P1-P4 and destructive deletion inside an isolated copy proceed.

Negative ceiling: this blocker says nothing about the truth of permanent-C11 necessity, Route A/B/C superiority, WVS7, lifecycle economics, learned-release persistence, or V3 runtime.

`MX03A_LITS1_NAMED_SOURCE_DESTRUCTIVE_C11_REPLAY_R1_COMPLETE`
