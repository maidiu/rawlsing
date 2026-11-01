# Reproducibility and limits

## 1. Custody and session

- Repository: `maidiu/rawlsing` (private).
- Branch: `agent/pyat-rrif-d3-workload-replay-capability-20261031-r1`.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d3-workload-replay-capability-20261031-r1`.
- Startup/PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29` (rechecked).
- Session: existing verified `ses_e6d29e95cffe854ht2rHaESxcE`; model
  `opencode-go/deepseek-v4.1-flash`, variant `max`, agent `build`. No model,
  editor, host or account switch. This is the current MAX session, not a new
  RRIF-specific session.
- No active worker worktree was modified. D1/D2 and other live worktrees were
  read-only observed. No worker was relaunched.

## 2. Environment and command pattern

macOS Darwin, Python 3.11.3, Git 2.43.0, pytest 9.1.1. All tests ran sourcefree
with:

```sh
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest -q -p no:cacheprovider <suite>
```

Current runs were in the D3 worktree. Candidate runs were in isolated temp
worktrees at the exact candidate commits, with sparse `rawlsing_next` +
`WORKER_RETURNS` checkout. No `data/` directory was present in any candidate
worktree.

## 3. Exact receipts

| Receipt | Command / source | Result |
|---|---|---|
| `test_receipts/current_grammar.log` | current `test_universal_grammar.py` | 32 passed |
| `test_receipts/current_workload.log` | current `test_universal_workload.py` | 16 passed |
| `test_receipts/current_batch_learned_prod_replay.log` | batch + learned world + candidate C + replay audit | 107 passed |
| `test_receipts/current_b5_and_faults.log` | B5 lifecycle + D3 forged-issuer test | 40 passed |
| `test_receipts/candidate_b01d_48.log` | B01D at `ef93f014` | 48 passed |
| `test_receipts/candidate_p01_25.log` | P01 at `3f91dc22` | 25 passed |
| `test_receipts/candidate_s06_26.log` | S06 at `4fec074c` | 26 passed |
| `test_receipts/candidate_a04_85.log` | A04 binder + A04T verifier at `c1df9842` | 82 passed, 2 skipped, 1 stale self-check failure |
| `test_receipts/candidate_r03_15.log` | R03 workload at `61356022` | 15 passed |
| `test_receipts/lineage_probe.json` | current surface/all35/import probe | JSON pass |
| `test_receipts/candidate_blob_compare.json` | current vs candidate blob/line comparison | JSON pass |

The A04T failure is its own stale test:
`test_accepted_owners_a04_a04s_a05_untouched` checks `git diff` against
`b68de0dd` and flags the new verifier files added by its own A04T commit. It is
recorded as a historical test defect, not a capability failure.

## 4. What was consumed

- RRIF-C unresolved rows at `b75addf621c3a6c1a3b196bd92a810fad77ae3ae`.
- RRIF-V hostile corrections at `bec050449f0b38606718e4e9691caa1721fcd94f`.
- A/B/A×B/E8 exact cuts; V's corrected counts used. No whole-estate recount.
- Original returns/reviews at the candidate commits, including R01V R7, R08V R7,
  R03V R4, A04SR, B01D, P01, R136 and S06.
- Current PRE-MAIN code, tests, importers and all35 signatures.

Pending review state at this cut:

- #564 and #565 contain only RRIF phase corrections; no returned independent
  review content.
- #569/#570/#571 contain dispatch/commission text only; no returned review.
- #575–#579 contain only the same HQ correction comment; no returned review.
  #577 remote unchanged is **not** evidence that its worker is idle.
- #580–#584 remain held and were not opened as work.
- No pending review is treated as acceptance or as a substitute for the exact
  source comparison here.

## 5. Limits

- Candidate tests at old cuts prove only those branch-local suites; they do not
  prove current behavioral equivalence or production integration.
- A04T's stale baseline self-check is a test defect; A04S/A04SR reviewer findings
  remain authoritative for the v2 translation/provenance/consumer limits.
- B01D/P01 prove sourcefree durable recovery and a branch-local consumer, not
  exactly-once external effects or a current production receiver.
- S06 is a standalone wrapper; its caller `trusted` flag and nonempty token are
  not independent authentication.
- Current grammar/workload are R8/R5-repaired but test-only; no production
  consumer is proven.
- All35 request construction is not implemented; only a caller-supplied roster
  validator and a single-bundle compiler exist.
- No raw survey/respondent data, native P07, source/native/actor/model/N9/N11/
  N12/Sorok authority, PRE-MAIN write or merge was used or issued.
