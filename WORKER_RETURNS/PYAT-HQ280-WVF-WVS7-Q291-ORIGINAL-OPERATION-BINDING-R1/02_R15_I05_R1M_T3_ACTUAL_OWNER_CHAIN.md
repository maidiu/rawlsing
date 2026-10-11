# HQ280 WVF — R15 → I05 → R1M → T3 actual owner chain

All identities below are read from committed receipts on the sealed branch. No raw WVS source was opened.

## 1. Chain (actual, ordered)

```
WVS7 exact source            2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d   (97,220 rows x 613 vars)
  -> R15 C11LogicalRelease   WVS7_FROZEN_P2_EXACT_SOURCE / e6881e9a08a48f8871790e781c28bddbc44ee35db894d6ad7b1105a6a8fd262f
     R15 ReplayManifest      996ba218fc5da5e0ad1ddf0cdc7f91ce8fb8a7363ce62076dc3f4073b85c383f
  -> candidate grammar       a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6
  -> R16 re-entry, generic I05 blob c7380774e8a1959da5ed8c6f23c2fc3cf99ad18d (UNMODIFIED), 2 neutral executions
     evaluated frontier      b2c3c50b68bcadb94ff2bf898d11c2b72694ced9fee4154e535db2694e26a4f3
     I05 frontier replay     a9d999d96533ceaf4535448a6a488227c05d205866a93feb391080c68d6f3024
  -> R1M fresh oracle        3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800
     R1M truth payload       eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405
  -> T3 standard oracle      RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0 / e546c15533ba138be9995095059ea3b70b64a6d7b5765e3789935cff7342ef00
```

## 2. Owners and receipts inspected

| owner / receipt | path | what it establishes |
|---|---|---|
| R1M return | `WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/00_RETURN.md` | scope + terminal |
| 46-candidate conservation | `…/03_46_CANDIDATE_REPLAY_CONSERVATION.json` | 46 ordered hashes, `additions: 0`, `exact_hash_stream_equal: true` |
| R16 execution receipt | `…/06_R16_EXECUTION_RECEIPT.json` | `admitted_r15_release_ref`, `generic_i05_blob`, `covered_candidate_count: 46`, `generic_i05_modified: false` |
| fresh WVS oracle | `…/07_FRESH_WVS_ORACLE.json` | `truth_payload.expected_fact_manifest` (46), `freeze_receipt`, `source_identity` |
| independence proof | `…/08_ORACLE_INDEPENDENCE_PROOF.json` | independence from Candidate A/B/C |
| command telemetry | `…/10_COMMAND_TELEMETRY.json` | **gate order and durations — the chronology evidence** |
| T3 parity oracle | `WORKER_RETURNS/PREMAIN-FIABC-LITS-INDEPENDENT-ACCEPTANCE-T3-FREEZE-R1/court/oracles/WVS7.standard.json` | same frontier/authority digests, 46 `COVERAGE_LIMITED` |
| generic I05 owner code | Git blob `c7380774e8a1959da5ed8c6f23c2fc3cf99ad18d` (present; introduced in `3bef6f693`) | I05 owner is committed code, not a local script |
| R1M worker branch | `refs/heads/agent/rabochii-premain-fiabc-lm2-r1m-lock2-successor-r16-oracle-r1` @ `04443d0f8f85234363da29f77f5544a353986246` | GitHub-Actions execution provenance (`github_execution_sha 4302685a…`) |

## 3. Producer / consumer signatures

- **Producer:** `FIABC_LM2_R1M_SUCCESSOR_LOCK2_COMMON_C11_GENERIC_I05_RECEIPT_TRUTH_ORACLE` (`oracle_build_provenance.builder`), dependencies classified `EXACT_SOURCE` and `ACCEPTED_AUTHORITY` — no candidate-owned root.
- **Consumer boundary:** the T3 candidate-neutral parity oracle consumes the same frontier/authority digests; it does not re-derive them.
- **Modification guard:** `generic_i05_modified: false`, `generic_validation_guard_passed_naturally: true`, `r15_mechanical_rehydration: true`, `r15_semantic_rebuild: false`.

## 4. Chronology — the one claim that does not survive

`10_COMMAND_TELEMETRY.json` gate order and durations:

| gate | ms | meaning |
|---|---:|---|
| GATE_3_SOURCE_FREE_FRONTIER_REPLAY | 78 | the 46 expected identities are replayed here |
| GATE_4_SUCCESSOR_LOCK2 | 12 | discovery authority sealed |
| **GATE_5_R16_REENTRY** | **790,750** | **the two generic I05 executions** |
| **GATE_6_FRESH_ORACLE_AND_SECOND_REPLAY** | **504,100** | **the oracle truth payload is assembled here** |
| GATE_7_R01_R18_FINAL | 0 | ledger |

The oracle self-reports `PASS__FROZEN_BEFORE_CANDIDATE_EXECUTION` — correctly, since it is frozen before the A/B/C candidates — and the retained failure labels are `POST_I05_ORACLE_…`. **The expected set is pre-I05; the truth payload is post-I05.** Any statement that the 46-member *oracle* predates the I05 outcome would be false; any statement that the 46-member *frontier* predates it is true.

## 5. Typed negative law preserved

`08` records the negative-state law: physical vs semantic missing distinct; `VALID_EMPTY` distinct from unavailable/unresolved/integrity failure; governance-blocked is not empirical data; `DISTINCT_BY_DEFAULT` source-relation state requiring exact authority; routing states `ROUTING_UNKNOWN / RULE_UNAVAILABLE / INAPPLICABLE / NOT_ASKED / NOT_ELIGIBLE / ELIGIBLE_APPLICABLE`. These distinctions are what makes `COVERAGE_LIMITED` an honest typed state rather than a euphemism for failure.
