# SOROK S45-S47 INDEPENDENT REVIEW — DURABLE DELIVERY

## VERDICT

- `e42faf01b57a9188f0cf75baaccfcd57edb07173` — **ACCEPT** (sourcefree S45-S47 package import closure; preserved).
- `da97d2624486b783bf5c4f465b17fdcdea3af20a` — **ACCEPT** (adjacent package+projection+harness integration; preserved).
- `41bf45813fd0adeffd9b54e1306c2022abe96514` — **ACCEPT** (focused closure of the three review corrections only).

This return is durable delivery of already completed independent review. No tests were rerun and no new review procedure was opened for publication.

## SCOPE

- Shipping unit: the three adjacent returns — product closure, public projection adapter, and causal harness. The package return alone does not contain `s45_projection`.
- Grade: TEST_ONLY sourcefree engineering. No native C8/C9/C12, CAN008/CAN011, ADP person source, Pyat world, human usability/delivery, protected write, PRE-MAIN merge, or native/human acceptance.

## EXACT COMMANDS AND RESULTS

Full command strings and stage labels are in `evidence/COMMANDS_AND_RESULTS.json`; retained source records are indexed in `evidence/RETAINED_EVIDENCE_HASHES.json`.

| Stage | Command (abbreviated) | Result |
|---|---|---|
| e42faf01 | `product/run_s45_s47.py manifest` | exit 0; 417/417 source; import 279/170 local/109 stdlib/0 external |
| e42faf01 | `product/run_s45_s47.py demo --root .local-logs/package-review/demo --keep` | exit 0; all 10 checks true; ACTUAL refused, SCHEDULED accepted; cold `e196c974...` |
| e42faf01 | `product/run_reused_tests.py --junitxml .local-logs/package-review/reused-tests.xml` | `55 passed` |
| e42faf01 | targeted shipped S41/S42/S44 tests | `5 passed` |
| e42faf01 | `.local-logs/package-review/probe_spine.py` | 7/7 independent probes |
| da97d262 | `pytest ... SOROK-S45-S47-PROJECTION-20261105-R1/tests` | `11 passed`; package closure |
| da97d262 | `run_causal_harness.py --package-closure ... --original-tests none` | PASS 22/22; source audit 424/424 |
| da97d262 | projected `product/run_s45_s47.py demo` | exit 0; all 10 checks true; import 284/175/109/0 |
| da97d262 | independent integration probes | 5/5 groups; wrong-root/projection-open refusal pass |
| 41bf458 | `pytest ... product/tests` | `2 passed` |
| 41bf458 | `probe_public_cli.py` | all commands exit 0; no `root_hash`/`root_id`/private markers |
| 41bf458 | harness `--original-tests all` | exit 2; `PACKAGE_CLOSURE_ORIGINAL_TESTS_UNSUPPORTED:all`; no PASS |
| 41bf458 | harness `--original-tests s47` | exit 2; `PACKAGE_CLOSURE_ORIGINAL_TESTS_UNSUPPORTED:s47`; no PASS |
| 41bf458 | harness `--original-tests none` | PASS 22/22; source audit 424; `original_tests=NOT_RUN` explicit none |
| 41bf458 | `tools/readback_census.py` | 462 files / 5,201,019 bytes; excludes `READBACK.json` and `__pycache__`; matches READBACK |

## SOURCE / HEAD / MANIFEST EVIDENCE

- `SOURCE_MANIFEST.json` is byte-identical to parent `da97d262`: 424 files, 4,574,530 bytes, SHA-256 `2535398efa2c376731aec17cd7b2ceda2e0fee477f064ae049870393b838b94b`.
- All 424 installed files match their manifest SHA-256 and git blob; 3 declared S37/S42 integration-cut blobs; 7 added WP19/S11 rows.
- Prior e42faf01 manifest: 417 files, SHA-256 `ab87a09c22733bc6b987e3a9c99a7348a4d50bdab0576a2f3daa5cf01078ec58`.
- Reproducible publication census excludes `READBACK.json` itself and `__pycache__`; a copied return with an added fake pycache reproduced the same count/bytes.
- Exact heads/parents and selected receipts: `evidence/SOURCE_HEAD_AND_MANIFEST.json` and `evidence/SELECTED_MACHINE_RECEIPTS.json`.

## THREE FOCUSED CORRECTIONS

1. **Census:** `tools/readback_census.py` defines and reproduces 462 files / 5,201,019 bytes; self and pycache excluded. `READBACK.publication_census` matches.
2. **Public CLI:** `new` and `view` emit `SOROK_WP19_ENCOUNTER_VIEW@1`; results emit `SOROK_WP19_INTERACTION_RESULT@1`; `status` emits `SOROK_WP19_STATUS@1`. No `root_hash`, `root_id`, or projection private-key/forbidden-marker violations across `new`/`view`/results/status/wait/exit/return/absence and `view --text`.
3. **Harness:** package mode refuses explicit `all` or `s47` with exit 2 before any PASS report; explicit `none` remains the lawful 22/22 path with source audit 424 and `modules_under_package=true`.

## RESIDUAL LIMITS

- ACCEPT is scoped to the adjacent three-return unit; package-return-alone projected CLI is not shipped/supported.
- The 424 manifest pins vendor source/test blobs, not the adjacent `s45_projection` adapter code.
- Prior 55 author tests and 11 projection tests were reused from accepted evidence at unchanged source; they were not rerun for the focused fix commit.
- Package harness mode requires explicit `--original-tests none`; omitted/default `all` also refuses by design.
- `status` retains local root/store path strings, but no `root_hash`/`root_id` or projection private markers.
- No native/human/protected/PRE-MAIN acceptance; all native grants remain false.

## EVIDENCE INDEX

- `READBACK.json` — this return's hash and receipt index.
- `PROGRAMMA_DELTA.json` / `.md` — compact owner-intake delta.
- `evidence/STAGE_VERDICTS.json` — three verdicts and holds.
- `evidence/COMMANDS_AND_RESULTS.json` — exact commands/results.
- `evidence/SOURCE_HEAD_AND_MANIFEST.json` — heads, parents, manifest/census.
- `evidence/SELECTED_MACHINE_RECEIPTS.json` — selected stage receipts.
- `evidence/HARNESS_22_SUMMARY.json`, `evidence/CLI_PRIVACY_SUMMARY.json`, `evidence/CENSUS_REPRODUCTION.json`.
- `evidence/REUSED_55_TESTS.log`, `evidence/PROJECTION_11_TESTS.log`.
- `evidence/RETAINED_EVIDENCE_HASHES.json` — provenance hashes of retained `.local-logs` records.

## REMOTE READBACK

Review branch: `codex/sorok-s45-s47-independent-review-receipt-20261105-r1`. Remote 40-hex head is reported in the final chat after push.
