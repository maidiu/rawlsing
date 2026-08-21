# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 11 REAL-ORACLE CANONICALIZATION CORRECTION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`
Accepted harness before this correction: `ea0d02ffde10a98872e73ea2b1fed8e453246cfb`
Accepted harness SHA-256 before this correction: `12a4eb3bace293ddf355c9661e051f77be3735813d6d776c61c472be0ba81c7d`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Accepted:

- Stage A / A.1 / A.2;
- B1/B2 CLI separation;
- real B1 neutral checkpoint;
- PostgreSQL UTF-8 transport correction and proof;
- shape-agnostic deliberate wrong-oracle negative-test correction and proof.

Three REAL B2 attempts are NON-ADMISSIBLE carrier evidence:

1. PostgreSQL ASCII COPY transport failure;
2. synthetic-era list-only wrong-oracle negative-test failure;
3. shared real-oracle comparison failure after all four replay digests and both negative tests passed.

Binding newest authority:

`30_SR04_REAL_ORACLE_CANONICALIZATION_CORRECTION_GATE.md`

REAL B2 IS BLOCKED.
No raw-source execution is authorized.

## Immediate mission — cheap real-oracle canonicalization proof only

Modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

Implement exactly the bounded correction in authority 30:

1. deterministic non-mutating canonicalization of the frozen B1 mixed-shape oracle into shared row-array comparison shape;
2. Q01 SQL restriction to the exact frozen hostile source-variable sets;
3. shared Q06 finite-value abs/rel tolerance `1e-9` comparator;
4. one explicit checkpoint-only proof mode using the exact shared query map, candidate normalizer and oracle comparator.

Do not modify `QUERY_ORACLE.json` or any accepted checkpoint byte.

## Accepted checkpoint identity

Verify `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT` contains exactly:

| file | bytes | SHA-256 |
|---|---:|---|
| `CHECKPOINT_MANIFEST.json` | 4490 | `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0` |
| `QUERY_ORACLE.json` | 131552 | `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a` |
| `events.arrow` | 104610186 | `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25` |
| `respondents.arrow` | 9920410 | `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73` |
| `sources.arrow` | 5418 | `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d` |
| `variables.arrow` | 33882 | `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b` |

If any identity differs, STOP.

## Cheap proof command shape

After implementing the proof mode, run only:

`python3 data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py --real-oracle-canonicalization-proof --checkpoint-dir /private/tmp/SR04_B1_NEUTRAL_CHECKPOINT --work-root /private/tmp/SR04_REAL_ORACLE_CANON_WORK --output-dir /private/tmp/SR04_REAL_ORACLE_CANON_PROOF`

The exact flag spelling may differ only if the committed implementation uses another explicit unambiguous name documented in the return.

The proof MUST:

`checkpoint_read -> canonicalize frozen oracle -> in-memory DuckDB registration of accepted checkpoint relations -> execute exact shared Q00-Q15 query map once -> exact shared candidate normalization -> exact shared oracle comparator -> proof receipt -> STOP`

No persistent carrier court is allowed.

Required token:

`PRE553_SR04_REAL_ORACLE_CANONICALIZATION_PROOF_PASS`

## Required proof assertions

All must be true:

- checkpoint identity pass;
- checkpoint unchanged before/after;
- no raw source decode;
- no B1/B2 execution;
- no persistent candidate materialization;
- PostgreSQL not started;
- DATABASE_URL unused;
- frozen oracle object unchanged;
- exactly 16 query IDs;
- shared query map used;
- shared candidate normalizer used;
- shared oracle comparator used;
- Q00 through Q15 all pass;
- Q01 excludes the non-hostile filler variables and exactly matches frozen B1 Q01 after canonicalization;
- Q06 finite values and `1e-9` tolerance path pass;
- inside-tolerance synthetic perturbation accepted;
- outside-tolerance synthetic perturbation rejected;
- canonical wrong-oracle negative test detected.

## Forbidden

Do not:

- run B1;
- run B2;
- pass `--source-root`;
- decode WVS7 or LiTS I raw bytes;
- mutate/rewrite/repackage the B1 checkpoint;
- regenerate or replace the frozen B1 oracle;
- change source fixture relations;
- change Q00/Q02-Q15 semantics;
- change candidate implementations/layouts;
- change replay logic;
- change timing loops, index law, budgets or selection law;
- reopen PostgreSQL UTF-8 transport;
- change the accepted shape-agnostic oracle-corruption helper except to route its result through the new canonical comparator if mechanically required;
- use or inspect DATABASE_URL;
- touch live Rawlsing PostgreSQL;
- commit proof outputs.

## Publication

After proof passes:

1. verify only `SR04_CARRIER_BAKEOFF.py` changed;
2. commit only that file with message `Fix SR04 real-oracle canonical comparison`;
3. push the control branch;
4. return to HQ:
   - exact starting HEAD;
   - new harness HEAD;
   - harness SHA-256;
   - exact proof command;
   - complete proof receipt;
   - per-query Q00-Q15 comparison booleans;
   - Q01 observed/canonical row counts and excluded filler-variable evidence;
   - Q06 observed/expected/difference/tolerance evidence;
   - required token;
   - final `git status -sb`;
   - pushed branch HEAD;
5. STOP.

HQ will separately inspect the correction before any further REAL B2 retry.
