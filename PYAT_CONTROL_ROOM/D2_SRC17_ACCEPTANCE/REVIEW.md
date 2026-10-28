# D2 independent review — SRC17 GSS 1973 original C11 positive

**Disposition: PASS** at the source-native C11 qualification grade, with one recorded non-material historical process deviation.

- Candidate: `5b1b9bd5f04f0456eac319264a6f2b64d4e87038`
- Branch: `agent/pyat-d2-src17-original-c11-review`
- Reviewer: independent D2 reviewer `ses_e84b9f75cffeOYB4AakaEDZNJg`; not the SRC17 author or D1 tally author.
- Grant: `TRUE_HQ_GRANT.txt` SHA-256 `f51de878…`; program `PROGRAM.txt` SHA-256 `9e292a10…`; both match the pinned control commit `3b703e878946a442b5c880f318b929365865ed00`.
- Scope: D2 only. This is not an I03/I05 workload, population estimate, M2/M3, F1–F4, N11/N12, Sorok, actor, CI/prod or J52/W52 action.

## Actual independent checks

I did not directly stat, hash or read the SRC17 source before the existing admission. Independent source access used the exact D2 grant through `decode_config_with_source_read_permission`; the private runtime bundle is outside Git and no respondent cells were printed or committed.

| Check | Actual result |
|---|---|
| Admission-gated source read | `1504` rows × `339` columns, `1,984,639` bytes, SHA-256 `59e65801…` |
| Custody | `PRE553_CONTENT_BOUND_SOURCE_SNAPSHOT@1.0.0`, `O_RDONLY`, `OPEN_FD_VIA_POSIX_DEV_FD`, snapshot unlinked, content-bound SHA |
| Reader | pyreadstat `1.3.2`, `user_missing=true`, encoding `null`, `apply_value_formats=false` |
| Physical/native-code agreement | `339_OF_339`, all audit checks passed, `0` issues; metadata digest `c9876c34…` |
| Selection | `279` configured response slots; `258` selected; `21` held; `2` selected coordinates; `339/339` physical slots and items accounted |
| Maximality | Every selected slot has exactly `1504` cells and `0` unbound cells; every held slot has positive unbound observed cells |
| Runtime config diff | `339` missing declarations + `3312` missing-state + `3312` source-missing-declaration bindings; **no other differences**; authority, identity, binding, universe, questions, routing, weights, canonical values and transform refs unchanged |

The selection matches the author receipt exactly, including held ordinals `11,12,29,32,73,74,110,113,114,123,127,183,188,222,264,282,283,284,290,317,323` and coordinates `2,237`.

## Native release

Release identity **`2f81b527ba1a62ecb79c7cc858063d60a10826a91af7d689606ed83e6bbd039e`**.

| Public/internal family | Count |
|---|---:|
| `RespondentEvent` | 388,032 |
| `RoutingEligibilityFact` | 388,032 |
| `EmpiricalCoordinateFact` | 3,008 |
| `EmpiricalUniverse` | 1 |
| `AuthoritySnapshot` | 5 |
| `WeightMeasureFact` | 0 |
| `RespondentIdentity` | 1,504 |
| `QuestionVariableBinding` | 258 |
| Public objects | 779,078 |
| Internal records | 1,762 |

The independent private primary reproduced the author’s complete local bundle content exactly:

- `public_objects.jsonl.gz` SHA-256 `03558bc8041f7e3e18587761753d53025a80ce672c29f79a5aafa9638e32232c`, 779,078 lines, 259,939,660 bytes.
- `internal_records.jsonl.gz` SHA-256 `b13302503b3a5e72287485b92f1035de91773a9585298b59491d0b1b25308278`, 1,762 lines, 172,623 bytes.

That private primary process was interrupted during local manifest persistence; I did not use its zero-byte private manifest. I instead verified the complete author local bundle and manifest:

- Replay manifest record content hash `239f041d…` recomputes exactly.
- Authority snapshot set hash `ea357f7d…` recomputes exactly from the 5 release authority snapshots.
- Manifest closure contains all 780,840 public/internal objects plus `SOURCE_ARTIFACT` and `SOURCE_SNAPSHOT`.
- Release semantic hash recomputes to `2f81b527…` from the manifest projection hash, manifest ref, and complete M01–M18 coverage.

State and authority preservation:

- Response states: `SUBSTANTIVE_RESPONSE 335,183`; `INAPPLICABLE 44,449`; `MISSING 2,164`; `DK 5,281`; `INVALID_UNRESOLVED 920`; `REFUSAL 35`.
- Routing: all `388,032` facts are `ROUTING_UNKNOWN`; no eligibility was invented.
- Coordinates: all `3,008` are `OBSERVED_COORDINATE`; canonical coordinate values `0`.
- Canonical response values `0`; transform refs `0`; weight facts `0`.
- Authority snapshots: `DEFER` ×4, `ALLOW` ×1; the one ALLOW is the replay protocol only, not semantic/canonical authority.
- Question semantic and topology authority refs resolve to `DEFER` for all 258 bindings; canonical question refs are `NOT_AUTHORIZED` for all 258.
- Source-native key witnesses: `1,504` distinct `SOURCE_NATIVE_RESPONDENT_KEY` exact refs; no typed-absence fallback.

## Negatives and restore

| Negative | Actual result |
|---|---|
| Wrong source SHA | `REFUSED` before source I/O: `SOURCE_READ_SOURCE_SHA256_MISMATCH`, resolver calls 1, `source_read_performed=false` |
| Held slice (`fileversion`, disposition `admin`) | `REFUSED`: `SourceBackedC11FacadeError: unbound response value/state`; no release |
| Canonical authority injection | `REFUSED`: `C11IntegrityError: canonical response/question material lacks exact mapping authority`; no release |
| Restore | Positive release built after the negatives with the same content hashes and release identity |

## Local durability / replay

The local bundle is outside Git at the documented receipt path. Public objects, internal records and replay manifest hashes match `LOCAL_RELEASE_RECEIPT.json`; the bundle is 259.9 MB public + 172.6 KB internal + 224.9 MB manifest. The author cold-replay receipt reports a cold process, selection match, release match, source read-through and local bundle hash match. I independently verified the bundle files, manifest closure, authority set hash and release identity.

I did **not** repeat a third full source-redecode replay after the interrupted private primary. The independent primary already reproduced the exact public/internal content; the cold-replay receipt and complete local bundle/manifest are consistent. This is a verification-depth limit, not a release defect.

## Committed artifact and privacy checks

- All 18 `RETURN.json` changed-artifact hashes/bytes match.
- Both pinned control-commit grant/program hashes match.
- `campaign_d2_src17/tests` passes `6 passed in 1.36s`.
- No `"raw_response_value"` or `"raw_coordinate_value"` token occurs in committed evidence; no respondent cells are in Git.
- The local bundle remains outside Git; source respondent data was not printed or uploaded.

## Historical deviation — exact record and material effect

The candidate final commit `5b1b9bd5` discloses:

- id: `PRE_ADMISSION_METADATA_LISTING`
- recorded command text: exploratory `ls -la` of the authorized SRC17 path **before** the admission-first runner existed
- effect disclosed: file size/mtime displayed; no source bytes opened, read, hashed or decoded outside admission
- exact shell transcript in Git: **not preserved**; the record is the disclosure in `RETURN.json` and `run_d2_src17.py`

I did not claim a zero-I/O uninterrupted history. The implemented current path is admission-first: `run_primary` authenticates the grant and runs the wrong-source refusal before `decode_original`; `decode_with_source_read_permission` resolves current permission before opening, stat’ing, hashing or decoding the source. The independent primary reproduced the exact release content, so the bounded material effect is no observed effect on the C11 result.

The grant says “No unapproved direct-file preflight outside the permission boundary.” Whether a metadata-only `ls -la` is inside or outside that exact wording is a **governance interpretation**, not an indispensable technical prerequisite for the independently reproduced native release. This review does not issue a new ALLOW or retroactively make the historical access admission-first. If strict governance requires the exact command transcript or a decision on metadata-only preflight, that is the smallest process decision; it does not require changing the release, config, validator or source evidence.

## Authority and privacy limits

Original snapshot semantics remain `DEFER`; no semantic or canonical ALLOW is issued. `ROUTING_UNKNOWN` remains unchanged. Weight design/estimand authority is not established; no weight fact is emitted. No population estimate, eligibility claim, I03/I05 workload, M2/M3, F1–F4, N11/N12, Sorok, actor action, CI/prod change or J52/W52 action is claimed or enabled. The local bundle is the only row-wise product and stays outside Git.

## Next consumer

D2 acceptance of the source-native C11 positive; then separately authorized Campaign A2/C11 product consumers. The smallest process follow-up, if strict preflight governance requires it, is to record the exact historical `ls -la` transcript or decide the metadata-only interpretation. No native release repair is required.
