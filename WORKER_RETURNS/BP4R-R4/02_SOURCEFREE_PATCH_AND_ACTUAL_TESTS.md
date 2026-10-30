# BP4R sourcefree patch and actual tests

## Environment

| Item | Value |
|---|---|
| Device | `mainMac` (`scutil --get ComputerName`) |
| Harness | OpenCode CLI `1.18.34`, agent `build` |
| Model / effort | `opencode-go/deepseek-v4.1-flash`; session variant `max` |
| Python / pytest / SQLite | 3.11.3 / 9.0.2 / 3.40.1 |
| Determinism | `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 BP2P4J_ORIGIN_RUNTIME=off` |
| Base | BP2P4J `5b3e6577400ea1d88971ae6b48e41a118b8059ae` |
| C9 actual consumer | `1e99681f58086f2784834df1186cfba71a2c50b9` |
| C12 repaired source | `68b058656254234f0af02df2a592aa6f8c6a8bd2` |
| S36 dependency | `8da78d803` (exact `SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1`) |
| Source access | sourcefree returns only; no SAV, native source or production DB |
| Temporary staging | exact C12/S36 sources were staged only for hard-coded C9 test paths; staging was removed after execution, with commit/blob identities retained in `01_...json` |

## Exact source/overlay order

1. BP2P4J base at `5b3e657…`.
2. F2 verifier overlay from `0636d257…` (`bp2p4/c12_verify.py` blob `c1699c8d…`, focused test blob `ebe1e828…`).
3. Author guard overlay from `790f793…` (`bp2p4/c12_guard.py` blob `a6a8de75…`, test blob `8ca11491…`).
4. `candidate/patches/01_c12_guard_episode_origin_and_version.patch`.
5. `candidate/patches/02_c9_actual_consumer_writer_version.patch`.
6. `candidate/tests/test_bp4r_candidate.py`.

Both patches were applied with `patch -p1` in a clean replay tree and reproduce the
full candidate files byte-exactly.

## Original negative reproduction

### BP4I3-01 — legitimate episode-bearing fork rejected

`JoinedProduct.say("legitimate episode before fork")` followed by a guarded fork
on the original guard returned:

```json
{
  "content_ok": false,
  "fork_ok": true,
  "errors": ["episode:0:branch_id_column_body_mismatch"],
  "child_episode_body_branch_id": "root",
  "child_sql_location": "alt"
}
```

The sealed episode body keeps `branch_id=root`; the fork changes only the SQL
location to `alt`; the original guard required those distinct fields to be equal.

### BP4I3-02 — unsupported C9 writer version admitted

A C12 database declaring `BP4_C12_STORE@2` was read by the actual C9
`c12_fork_guard` with its exact perception digest:

```json
{
  "state": "FORK_READY",
  "code": "FORK_READY",
  "writer_schema": "BP4_C12_STORE@2"
}
```

`two_store_readiness` also returned `READY` for matching `@2` caller strings,
and `check_c9_mirror_handshake` returned `ok=true`.

### Original F2 RED

The focused valid-SAY test on the unmodified BP2P4J verifier failed with
`episode:0:body_hash_mismatch` (exit 1). The exact F2 overlay made the same
assertion green.

## Repairs

### 1. Immutable episode origin vs current branch location

`bp2p4/c12_guard.py` now:

- resolves each episode row's expected origin from fork prefix counts;
- requires the sealed body `branch_id` to equal that origin;
- treats the SQL `branch_id` column as the current storage location;
- preserves the hashed parent body unchanged;
- refuses a transplanted child-local episode with `branch_id_origin_mismatch`.

The root branch origin is the root; a copied child row keeps the parent body's
origin; a child-local row's origin is the child. Nested forks recurse through the
exact prefix counts.

### 2. C9 actual consumer writer-version gate

`c9_actor_r3.c12_fork_guard` now reads `meta.schema` before any fork decision and
returns `FORK_HELD` with:

- `C12_WRITER_SCHEMA_UNSUPPORTED` for `@2`;
- `C12_SCHEMA_META_UNREADABLE` if the schema metadata cannot be read;
- `C12_SQLITE_USER_VERSION_UNSUPPORTED` for nonzero `PRAGMA user_version`;
- `C12_SQLITE_APPLICATION_ID_UNSUPPORTED` for nonzero `PRAGMA application_id`.

`check_c9_mirror_handshake`/`two_store_readiness` now require the declared C12
writer schema and mirror source domain to be in the supported set, not merely to
match each other.

## Actual commands and results

### Original BP2P4J

```sh
cd <bp2p4j-base>
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 BP2P4J_ORIGIN_RUNTIME=off \
python3 -m pytest tests -p no:cacheprovider --junitxml=01_ORIGINAL_BP2_33_1.xml
```

Actual: **33 passed, 1 skipped**, exit 0. The skipped test is the typed
`BP2_ORIGIN_RUNTIME_ABSENT` literal-origin case.

### Focused F2 RED and F2 overlay

```sh
python3 -m pytest \
  tests/test_episode_verifier_regression.py::test_valid_say_episode_is_green_and_preserves_the_post_hash_id \
  -q -p no:cacheprovider
```

Actual: **1 failed** `episode:0:body_hash_mismatch`, exit 1.

After copying the exact F2 `c12_verify.py` and focused test:

```sh
python3 -m pytest tests -p no:cacheprovider --junitxml=02_F2_OVERLAY_37_1.xml
```

Actual: **37 passed, 1 skipped**, exit 0.

### Guard court

```sh
python3 -m pytest tests/test_c12_guard.py -p no:cacheprovider \
  --junitxml=03_GUARD_ORIGINAL_11_0.xml
```

Actual: **11 passed, 0 skipped**, exit 0. The exact C9 mirror-schema path was
present in this host and hash-matched `1e99681f…`; when absent the test is a
typed skip, which explains the reviewer’s 10/1 result.

### Combined original F2 + guard

```sh
python3 -m pytest tests -p no:cacheprovider --junitxml=04_COMBINED_ORIGINAL_48_1.xml
```

Actual: **48 passed, 1 skipped**, exit 0.

### Repaired candidate combined

```sh
BP4R_C9_DIR=<patched-c9-dir> \
python3 -m pytest tests -p no:cacheprovider --junitxml=05_CANDIDATE_COMBINED.xml
```

Actual: **57 passed, 1 skipped**, exit 0 (F2 + guard + 9 BP4R tests).

### New BP4R fork/version court

```sh
BP4R_C9_DIR=<patched-c9-dir> \
python3 -m pytest tests/test_bp4r_candidate.py -p no:cacheprovider \
  --junitxml=07_C9_GATE_AND_FORK_COURT.xml
```

Actual: **9 passed**, exit 0. The court covers:

- legitimate episode-bearing fork, including cold reopen;
- forged child-local branch transplant;
- actual C9 `@2` refusal and `@1` readiness;
- forced/cold schema mismatch;
- mixed writer domain;
- C9 schema-gate source severance (RED before restore, HOLD after);
- preserved global-clock and anchor actor/created-clock residuals.

### Actual C9-R3 suite (staged exact C12/S36 sources)

```sh
cd C9_SQL
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest tests -q -rs -p no:cacheprovider --junitxml=06_C9_PATCHED_14_1.xml
```

Actual: **14 passed, 1 failed**, exit 1.

The failure is the known C9/C12 old-count conflict at
`tests/test_c9_r3.py:476`:

```
assert len(store.perceptions("root")) == len(store.perceptions("child"))
assert 2 == 3
```

The repaired C12 writer preserves the formerly dropped perception suffix; the
old test assumes it is dropped. This is a true version incompatibility and is
preserved RED, not weakened.

## Source severance

`tests/test_bp4r_candidate.py::test_c9_writer_schema_gate_source_severance_red_then_restored`
temporarily widens `SUPPORTED_C12_WRITER_SCHEMAS` to include `@2`, observes
`FORK_READY`, restores the gate, and observes `FORK_HELD`
`C12_WRITER_SCHEMA_UNSUPPORTED` on the same input. This proves the new consumer
check is load-bearing.

## Preserved HOLDs

- External anchor: no owner-issued key/trust root/monotonic ledger; deletion,
  injection, rehash and perception substitution remain content-green and
  anchor-required.
- Anchor payload still excludes branch actor/created_clock metadata; changing
  them leaves the payload unchanged.
- Global writer chronology still accepts perception clock 11 followed by episode
  clock 10; not repaired by this candidate.
- C9/C12 suffix old-count conflict remains RED.

## Exact evidence hashes

See `01_EPISODE_FORK_WRITER_VERSION_FALSIFIERS.json` for all JUnit and probe
SHA-256 values.

## NOT RUN

- real external signature/trust root/custodian/anchor service;
- native C12/C11/CAN/ADP/Pyat/source execution;
- C9/C12 cross-database ACID;
- standalone historical BP2/BP4 suites beyond the exact sourcefree cuts;
- QF2;
- PRE-MAIN CAS, merge or canonical registry update.
