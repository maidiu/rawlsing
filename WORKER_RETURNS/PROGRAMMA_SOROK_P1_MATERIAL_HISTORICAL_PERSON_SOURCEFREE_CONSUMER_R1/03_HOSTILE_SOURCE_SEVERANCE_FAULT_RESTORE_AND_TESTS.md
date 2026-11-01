# P1 hostile source, severance, fault/restore and tests

**Grade:** `TEST_ONLY_SOURCEFREE_NOT_NATIVE`. These are author-executed local receipts; they are not an independent review or native authority.

## Commands and exits

From the P1 worktree, with Python 3.11.3 and pytest 9.1.1:

```sh
OUT=$PWD/WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  M35_JOIN_E_RETURN="$OUT/candidate/deps/join_e" \
  M35_BP2_VENDOR="$OUT/candidate/deps/m35_vendor" \
  PYTHONPATH="$OUT/candidate:$OUT/candidate/deps/m35:$OUT/candidate/deps/join_e" \
  python3 -m pytest -q "$OUT/candidate/tests/test_p1.py" \
  -p no:cacheprovider --junitxml="$OUT/evidence/p1-junit.xml"
# 8 passed, exit 0
```

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  M35_JOIN_E_RETURN="$OUT/candidate/deps/join_e" \
  M35_BP2_VENDOR="$OUT/candidate/deps/m35_vendor" \
  PYTHONPATH="$OUT/candidate/deps/m35:$OUT/candidate/deps/join_e" \
  python3 -m pytest -q "$OUT/candidate/deps/m35/tests" \
  -p no:cacheprovider --junitxml="$OUT/evidence/m35-junit.xml"
# 8 passed, exit 0
```

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  M35_BP2_VENDOR="$OUT/candidate/deps/m35_vendor" \
  PYTHONPATH="$OUT/candidate/deps/m35:$OUT/candidate/deps/join_e" \
  python3 "$OUT/candidate/deps/m35/oracles/m35_source_mutation_oracle.py"
# 9 rejected / 0 accepted, exit 0
```

The bundled 48-file BP2 vendor closure is pinned at `candidate/deps/m35_vendor/` and selected by `M35_BP2_VENDOR`, so the run does not depend on the host-absolute warm path.

The four-life runner and hostile receipt are also committed as scripts:

```sh
"$OUT/candidate/tools/run_p1.sh" --root /tmp/p1-run --output /tmp/p1-results.json
# exit 0; all seven invariants true

"$OUT/candidate/tools/run_hostile.sh" --root /tmp/p1-hostile --output /tmp/p1-hostile.json
# exit 0; simple tamper refused, restore green, selfhash hold typed
```

Receipts: `evidence/p1-tests.out`, `evidence/p1-junit.xml`, `evidence/m35-tests.out`, `evidence/m35-junit.xml`, `evidence/m35-oracle.out`, `evidence/p1-run.out`, `evidence/p1-hostile.out`, and the machine JSON copies.

## Source severance and independent action

- **A vs B, identical B share:** A and B have the same B event hash `16f11d2e…`; A has admitted access, a target and `HELP_ACCEPT`; B has no access, no A response, no target and `UNKNOWN_RECEIVABILITY`. B's B world event and targetless C12 remain. Removing A's access erases the attributed A response, not the B event.
- **Opportunity is not action:** D omit and D perform have the same B share source. Omit leaves one tool and `HELP_ACCEPT`; A's independent inspection leaves zero tools and `HELP_REFUSE`. No inspection is inferred from B's performed event.
- **B refusal is not help accept:** C's B `REFUSE_TOOL` and A's `EXPLICIT_REFUSAL` produce `HELP_REFUSE`, targetless C9 `NO_CHANGE`/`NO_PROPOSAL`, and no help acceptance.
- **Same later speech, different cause:** C and D-performed both expose `HELP_REFUSE`, but C's B event is a refusal and D's is the share-plus-A-inspection route; their B hashes, A actions and target states differ.
- **No acquisition:** every S35 T is `NO_CHANGE`, `target_proposal=null`, `grant=null`, `beforestate_mutation=false`. N4 labels and N5 prior acts do not change the A/T result. No V3MS practice is created.

## C12 tamper and exact restore

The simple tamper test drops the SQLite update trigger, changes an episode body, and closes:

```text
SessionRefusal: ROOT_C12_VERIFY_FAILED:
  ["episode:0:body_hash_mismatch"]
```

The exact original database bytes are restored and a cold reopen verifies GREEN. This is a real persisted C12 body mutation, not a string-only assertion.

A coordinated selfhash edit rewrites both the body and its appended hash. The selfhash verifier then reports `ok=true`; that is exactly why it is not separate custody. The hostile receipt types it:

```json
{"c12_selfhash_ok": true, "verdict": "TRUST_CUSTODY_HOLD",
 "external_anchor": "ABSENT_OWNER_ANCHOR_REQUIRED", "production_accept": false}
```

The exact restore after that edit is GREEN. No claim is made that the selfhash is production custody or that an external owner anchor exists.

## Nine forged B preimages

The M35 reviewer oracle rejects all nine before BP2/C8; no `bp2` directory is created. The mutations are `wrong_owner`, `wrong_event_ref`, `wrong_event_hash`, `wrong_clock`, `wrong_operation`, `wrong_quantity`, `wrong_e1_ref`, `wrong_e1_hash`, and `wrong_e1_clock`. The P1 test suite independently replays the same nine against the copied M35 source; the P1 hostile receipt also records 9/9. Every refusal code is `MATERIAL_SOURCE_PREIMAGE_MISMATCH`.

## Author, reviewer and owner grades

| Evidence | Grade |
|---|---|
| P1 implementation and eight tests | `AUTHOR_EXECUTED_SOURCEFREE`; not independent acceptance |
| M35 eight tests and nine-source oracle | Author evidence from M35 `@4170fbf`; oracle's frozen cut metadata is `55377b…`/`2d11e32…`, not a new reviewer verdict |
| JOIN-E `@7bf2da30` | Inherited JOIN-V `@4387dc81` 30/30 + 5/5 scoped acceptance; not recensused here |
| F1 `@1973d28` / `@8d958529` | Pending independent verdict; not imported, not claimed |
| Native C8/C9/C12, external anchor, C10/C11, Pyat N11/N12, human A5 | HOLD |

## Not run

No native C8/C9/C12 writer, external KMS/owner anchor, production database, original survey bytes, credentials, network/provider call, Pyat world, native person write, human A5, or independent review. No full repository suite or 640-file transplant was run.
