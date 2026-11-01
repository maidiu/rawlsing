# Reproducibility and limits — RRIF-D1

## 1. Identity and environment

- **Host:** mainMac (Darwin 22.3.0, x86_64), local Mac.
- **Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d1-accepted-receiver-fates-20261031-r1`.
- **Branch:** `agent/pyat-rrif-d1-accepted-receiver-fates-20261031-r1`.
- **Harness:** OpenCode 1.18.34, agent build, `opencode-go/deepseek-v4.1-flash`, variant `max`.
- **Verification:** process argv contains `--model opencode-go/deepseek-v4.1-flash --variant max --agent build`; session DB row `ses_e6af3a6cbffeVfRfHa85tHy2c6` records the same model/provider/variant. No switch occurred.
- **Python:** 3.11.3. **pytest:** 9.0.2. **pyreadstat:** 1.3.2 (current ambient; historical C3/R9 courts used a different pin and were not transplanted).
- **PREMAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29` at start and end; remote `refs/heads/integration/pre-main-reconciliation-r1` read back unchanged.
- **Working tree:** only `WORKER_RETURNS/PYAT_RRIF_D1_20261031_R1/**` written. No production file, PREMAIN ref, other worktree, Sorok branch, protected source or pending review was mutated.

## 2. Commands and results

All commands were run from the worktree with `PYTHONDONTWRITEBYTECODE=1`; pytest used `-p no:cacheprovider`. `TMPDIR` pointed outside the worktree.

### C1

```
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py
# 48 passed in 11.07s

python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  -k 'r7_closed_16_key or r6_witness_mutation'
# 2 passed, 11 deselected

python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py \
  -k 'pairing or ordering'
# 4 passed, 31 deselected
```

### N10E

```
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py
# 43 passed in 23.52s

python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py \
  -k 'p7_replay or fresh_process or frozen_spine or successor'
# 8 passed, 35 deselected
```

### C3

```
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py
# 16 passed in 69.82s
```

Accepted D01 court materialized from Git and run against current code:

```
2 failed, 6 passed
# failures: missing DECLARED_ENCODING_ALLOWLIST and SOURCE_DECLARED_ENCODING_ONLY
```

Accepted D02 court materialized from Git and run against current code:

```
collection ImportError: cannot import name 'normalize_decoder_physical_value'
```

Sourcefree C3 fault script and PR526 snapshot probe outputs are recorded in `FIRST_CONSUMER_AND_TESTS.md` and in the dispositions JSONL. No raw source file was opened.

### C5 reconstitution

The accepted service module was read from Git at `151d3926` into a temporary path. Because the worktree is sparse and `data/` is not checked out, the four committed GT2 transport resources were extracted from Git object `8e44ca9c` into a temporary root and the repo-native payload loader was pointed at that root for the duration of the process. This is committed-transport, sourcefree use; no raw survey SAV was opened.

The service returned the exact accepted floor (query, fact, denominator 19,210, relation, admission, M1 ELIGIBLE, V557 ALLOW_CONTEXT_ONLY, resolved CONTEXT, producer V554, family F1). A second call with the loaded fact's `raw_denominator_support` changed in memory to `19,211` was refused with `current GT2 denominator is 19211, not 19210`.

### Absence probes

`importlib.util.find_spec` returned absent for:

- `rawlsing_next.pre553_source_access_broker`
- `rawlsing_next.pre553_source_session`
- `rawlsing_next.pre553_execution_binding`
- `rawlsing_next.closed35_g01_sav_numeric_representation_authority`
- `rawlsing_next.current_gt2_structural_context`
- `rawlsing_next.pre553_c1_immutable_release_binding`

No importer of these modules was found.

## 3. Reproduce from the exact cuts

1. Confirm PREMAIN: `git rev-parse 8e44ca9c751049d65e6def47600b5c073ee04b29`.
2. Read the six RRIF-C rows from `b75addf6:WORKER_RETURNS/RRIF-C-POST-GAP-LINEAGE-REDUCTION-20261031-R1/GENUINELY_UNRESOLVED_IMPLEMENTATIONS.jsonl`.
3. Read the RRIF-V corrections from `bec05044:WORKER_RETURNS/PYAT_RRIF_V_HOSTILE_CUSTODY_AB_20261031_R1/`.
4. Read accepted branches and blobs by exact commit and path; do not merge them.
5. Run the sourcefree test commands above. For C5, materialize the accepted service module and committed GT2 transport to a temporary directory, as described.
6. Do not open raw survey, native P07, actor, model-use or protected source material.

## 4. Limits and UNKNOWNs

### NOT_RUN

- No raw survey source access, SAV/DTA source decode, native P07, original U/E_pre, FF, CAN/ADP, N11/N12, Sorok actor or model-use issuance.
- No production patch, merge, cherry-pick, adoption or self-review.
- No R9 historical runtime execution; no R9 transplant.
- No C1-M2 candidate execution in this return; F8E/F8F evidence is consumed as historical evidence.
- No independent execution of the C5 accepted test file; the accepted service function was reconstituted and called directly.
- No whole-estate recount; RRIF-V counts are used as corrections.
- No PR/issue API; GitHub review API access is out of scope.

### UNKNOWN

- Production callgraph for C1, C1-M2, R9, C5 and N10E. Only static imports and test call sites were found; the C3 decoder has an actual production call site.
- Source authenticity for D01/D02, C1-M2, R9 and N10E context. No raw source SHA or competent issuer was available.
- Behavioral equivalence from exact blob identity. Exact bytes are source identity only.
- Whether a future consumer will need the C5 wrapper or an R9 successor. Both are held with precise reversal conditions.
- #565 returned a real S7-FIX boundary/source-ABI review and was consumed: six historical boundary identities and negative custody pass, current ownership mapping is RED, current PR526 decoder tests pass at test scope, source relations has no production consumer, and no merge is recommended. It does not change the six D1 dispositions. #564/#569–571/#575–579 refs present at read time are commission/control tips, not returned review packets. #577 remote unchanged does not mean the worker is idle. #580–#584 remain held.

### RRIF-V corrections applied

- `1,333` branch-only exact implementations are not current PREMAIN integration.
- `291` exact-other-path copies need owner/ABI proof; exact bytes at another path are not runtime equivalence.
- B's `155` are branch rows, not `155` distinct decisions: `122` distinct primary IDs, `135` decision records, `151` fate-classified rows.
- `CKPT-20261009-PYAT-HQ274…` is documentary candidate intake, not code adoption.
- Nine accepted integration branches; none is a PREMAIN ancestor. Acceptance is not merge or retention.
- The C3/R5 exact assets in `24847592…` are historical; D01/D02/G01/R9 current paths are absent. No transplant.

## 5. Scope statement

This return is ENGINEERING evidence at sourcefree/declared grain. It is not a scientific issuance, native source authentication, authority adoption, HQ decision, merge, PREMAIN integration or independent review of itself. The six dispositions are recommendations/records for HQ intake, not self-adoption.
