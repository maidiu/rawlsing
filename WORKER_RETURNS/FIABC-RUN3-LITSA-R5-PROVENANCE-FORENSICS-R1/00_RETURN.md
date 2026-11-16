# FIABC RUN3 — LiTS/A R5 Provenance Contract Forensics — R1

## Terminal classification

`RUN3_LITSA_VOID_AS_CANDIDATE_EVIDENCE__COURT_PROVENANCE_GLUE_DEFECT_PROVED`

RUN3 LiTS-I/A is **not valid evidence of a Candidate-A architectural or semantic failure**. The frozen Candidate-A owner correctly rejected an R5 release identity constructed by the measured court/backend without the exact source-artifact identity required by the accepted Route-A/C11 contract.

The direct RUN3 exception text — `R5 release source ref object_id missing` — is exactly the frozen owner's fail-closed check for a malformed `source_artifact_ref`. Repository authority fixes the missing object identity and also shows that the measured backend used the wrong `kind`.

No Candidate A/B/C execution, measured P2X, source decoding, raw survey inspection, or production mutation was performed in this forensic lane.

## Governed identities

- Repository: `maidiu/rawlsing`
- Measured execution head: `bc832181b4284ac110d2be44fc83504e04de081e`
- Protected execution branch: `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`
- Frozen Candidate-A owner commit: `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
- Frozen Candidate-A owner path: `rawlsing_next/pre553_r5_source_backed_adapter.py`
- Frozen Candidate-A owner blob: `d4915e7e6755ba1850756aebff72f982f73a332b`
- Measured backend path: `rawlsing_next/ee_p2x_darwin_stage_backend.py`
- Measured backend blob: `1bb84723b2f9c33eedae87736564d36cc9504ff0`
- Measured driver path: `rawlsing_next/ee_p2x_darwin_court_driver.py`
- Frozen T3: `7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`
- PRE_CANDIDATE_STOP: `203fae32dc31ad6afe6dd2e85aed0ddf1a262d9a93efa6597a0c09173c64b384`

## 1. Exact Candidate-A source-artifact-ref contract

### 1.1 Frozen owner runtime check

At frozen owner commit `0b96b8...`, `rawlsing_next/pre553_r5_source_backed_adapter.py` lines 203–210 reads `reader.release_identity["source_artifact_ref"]` and requires:

1. a mapping;
2. `content_hash` that is a valid SHA-256;
3. a nonempty string `kind`;
4. a nonempty string `object_id`.

The exact immediate RUN3 error is emitted at line 210 when `object_id` is absent.

The same adapter later projects the verified R5 physical-cell stream through the accepted source-backed C11 facade and checks that the resulting C11 release source hash equals the R5 descriptor source hash (around lines 345–349). The owner therefore does not infer a missing provenance identity from physical values; it requires the identity to arrive lawfully.

### 1.2 Canonical ExactRef law fixes the full shape

`rawlsing_next/pre553_empirical_objects.py` at the frozen owner line defines `ExactRef` at lines 279–288 as exactly:

- `kind: str`;
- `object_id: str`;
- `content_hash: str`;

with nonempty text validation for `kind` and `object_id` and SHA-256 validation for `content_hash`.

`rawlsing_next/pre553_c11_ingest.py` defines `SourceReleaseManifest.source_artifact_ref` at lines 134–136 as:

```python
ExactRef("SOURCE_ARTIFACT", self.source_artifact_id, self.source_artifact_content_hash)
```

That exact ref is included in the source-release semantic projection, replay substrate refs, replay closure, and the sealed `C11LogicalRelease` (`pre553_c11_ingest.py` around lines 138–153, 392–399, 703–707, 779–787; `pre553_c11_repository.py` line 28).

Therefore the accepted Candidate-A provenance contract is not merely “three arbitrary nonempty fields.” Its lawful source reference is:

```json
{
  "kind": "SOURCE_ARTIFACT",
  "object_id": "<governed source_artifact_id>",
  "content_hash": "<exact canonical source SHA-256>"
}
```

### 1.3 Candidate-A qualification constructed that canonical shape

The repaired/frozen Route-A qualification test blob `25e905868a21bb36035269065b7bc3640201b7d8` at repair commit `8103a70b43dc657a41d2f42401eef9dfadcd3c1f` constructs `R5ReleaseIdentity` by first building the validated C11 release and then doing:

```python
source_ref = native.source_artifact_ref.as_dict()
...
R5ReleaseIdentity(..., source_artifact_ref=source_ref, ...)
```

It does **not** synthesize a hash-only R5-specific source identifier. Thus accepted Route-A qualification inherited the canonical C11 `SOURCE_ARTIFACT` ExactRef intact.

B19Q2 subsequently qualified the exact frozen owner blob `d4915...` with that repaired test blob twice in independent Python processes: 8/8 PASS on both runs. Authority:
`.../WORKERS/B19Q2_AS4I_ROUTE_A_ADAPTER_QUALIFICATION_R1/00_RETURN.md`,
`01_INPUT_IDENTITY_RECEIPT.json`,
`02_RUN1_PYTEST_RECEIPT.json`,
`03_RUN2_PYTEST_RECEIPT.json`,
`05_COMMON_HARNESS_INTAKE_HANDOFF.json`.

## 2. Exact LiTS-I object_id

The accepted LiTS projection is materially instantiated by:

- banked commit `3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`;
- builder path `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2b/run_as2b_lits1_mechanical_certification.py`;
- builder blob `c51b56779ab9d79126619b7733d41f5253c8150f`.

Its `build_projection(...)` constructs the governed projection at lines 349–357 with:

- `source_artifact_id = f"urn:rawlsing:source:lits1:sha256:{SOURCE_SHA}"`;
- `expected_source_sha256 = SOURCE_SHA`;
- `SOURCE_SHA = 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- a separate `release_id = LITS1-AS2B-C11-...`;
- a separate `SOURCE_SNAPSHOT` retention ref using the same source URN and SHA.

Hence the exact lawful LiTS-I source ref is:

```json
{
  "kind": "SOURCE_ARTIFACT",
  "object_id": "urn:rawlsing:source:lits1:sha256:7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
  "content_hash": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
}
```

The `object_id` is the governed **source artifact identifier**. It is not the C11 source-release `release_id`, not a release manifest hash, and not a newly invented hash URN.

This identity is already available to the measured backend through `projection.source_artifact_id`. No raw-source inference is needed.

## 3. Measured backend emitted a malformed and noncanonical ref

At exact measured head `bc832181...`, `rawlsing_next/ee_p2x_darwin_stage_backend.py` lines 1315–1331 defines `_r5_release_identity(...)`. Lines 1322–1326 emit:

```python
R5ReleaseIdentity(
    ...
    source_artifact_ref={"kind":"SOURCE_SHA256","content_hash":source_sha},
    ...
)
```

Compared with the accepted contract:

| Field | Accepted law | Measured backend |
|---|---|---|
| `kind` | `SOURCE_ARTIFACT` | `SOURCE_SHA256` |
| `object_id` | governed `projection.source_artifact_id` | **absent** |
| `content_hash` | canonical source SHA-256 | correct LiTS SHA-256 |

Thus two defects coexist. The immediate RUN3 exception was caused by the absent `object_id`; adding an arbitrary identifier would not be a lawful repair because the backend also uses a noncanonical `kind`.

The same backend also contains a stale two-field expectation in `_assert_r5_canonical_source_root(...)`, expecting `{"kind":"SOURCE_SHA256","content_hash":...}`. That is corroborating evidence that the backend carried its own divergent provenance mini-schema rather than the accepted C11/Route-A ExactRef contract.

## 4. Exact malformed-input path into Candidate A

The measured path is deterministic:

1. `_compose_lits(...)` lines 1280–1313 obtains the accepted governed LiTS projection.
2. For LiTS/A S01, it calls `_lits_a_build_current_s01(...)`.
3. That function requires the canonical LiTS incidence and absent target, then calls `_build_r5_from_incidence(...)` (around lines 1204–1217).
4. `_build_r5_from_incidence(...)` calls the R5 builder with `release_identity=_r5_release_identity(ctx.stage.source, projection)` (around lines 1418–1423).
5. The resulting reader is passed as `builder_kwargs={"reader": reader}` to `services.compose_p2r1_binding(...)`.
6. In `rawlsing_next/ee_p2x_darwin_court_driver.py`, `OWNER_SPECS` lines 73–76 pins Candidate A to the exact frozen owner path/blob. `DriverServices.accepted_repository_builder` and `load_exact_owner_module` (around lines 816–842) verify and load that frozen owner. `compose_p2r1_binding` lines 820–826 also reconstructs the complete governed projection and injects it into the accepted owner builder.

Therefore the bad ref is constructed by the court/backend **before** the frozen Candidate-A owner receives the R5 reader. Candidate A then performs the fail-closed validation it was qualified to perform.

## 5. Why the receipt says CANDIDATE_LOCAL_FAILURE anyway

This label does not prove causation.

In the measured backend:

- `BackendStop` defaults to terminal `CANDIDATE_LOCAL_FAILURE`, kind `CANDIDATE_LOCAL_CORRECTNESS_FAILURE`, scope `CANDIDATE_ONLY`.
- `R5SourceBackedAdapterError` is not a `BackendStop`.
- `run_stage(...)` lines 2550–2555 catches any other exception on a non-COURT source and wraps it in a generic `BackendStop("untyped production backend implementation failure", ...)`.
- `_failure(...)` then serializes the resulting default candidate-local terminal.

So the court's classification machinery can label an owner rejection as `CANDIDATE_LOCAL_FAILURE` even when the rejected object was malformed by court glue. The provenance chain above proves that is what happened here.

## 6. Historical evidence and contract chronology

### Route-A implementation and qualification

- Initial Route-A implementation commit: `c935c7003c6081f699968ee4385d6a91bba5f13e` (“Implement B19 Route A R5 to C05R2A adapter”).
- B19 implementation return states that Route A binds reopened R5 release identity to exact source SHA and validates source metadata/identity fail-closed.
- B19R repair commit `8103a70b43dc657a41d2f42401eef9dfadcd3c1f` changed **only the qualification test**, not the Route-A implementation. Its repair ensured replay-equivalent builds shared one governed release identity.
- B19Q2 then passed all eight Route-A tests twice with frozen owner blob `d4915...`.

### P2R1 accepted final-court qualification

At commit `9511f44728a8469d685463ec0fc880864c9187de`:

- `WORKER_RETURNS/EE-P2R1/10_ABC_ADAPTER_QUALIFICATION_MATRIX.json` marks LiTS-I/A `READY__PRESERVED_R5_PLUS_ACCEPTED_PROJECTION_TO_COMMON_RUNNER`.
- `WORKER_RETURNS/EE-P2R1/00_RETURN.md` states that the accepted Candidate-A repository surface composes with the exact governed projection and common runner.
- `07_GOVERNED_PROJECTION_BINDING_RECEIPT.json` says every `GovernedC11Projection` field is required explicitly and validation delegates to the accepted projection contract.
- `rawlsing_next/pre553_carrier_execution.py` `bind_governed_c11_projection(...)` lines 164–188 implements that exact no-default/no-inference binding.

### Preserved real LiTS A first-build evidence

`WORKER_RETURNS/EE-P2X/01_LITS_I_A_FIRST_BUILD_STAGE.json` at commit `29e434a385719f9835e0bcd252fb24bc37675a99` records a prior fresh absent-target LiTS-I/A R5 build as PASS and identifies preserved commit `02a7ff71ae65b1aa8c52add0b315244a9eaea9df`. P2R1 explicitly adopted that preserved evidence rather than requiring a rebuild.

### Backend provenance divergence appears at backend introduction

The history of `rawlsing_next/ee_p2x_darwin_stage_backend.py` shows the malformed constructor already at initial production-backend fan-in commit:

`548d7ae9be4a8a624601b5d468fb2e19693ca597` — “EE-P2X: selectively fan in qualified R6S production backend”.

At that commit, `_r5_release_identity` emitted the same two-field `{"kind":"SOURCE_SHA256","content_hash":source_sha}` mapping.

The same expression remains unchanged through later backend lineage including `617c9c...`, `0520db...`, `e15b3f...`, and exact measured head `bc832181...`.

The mismatch is therefore a **stale/later court-backend contract divergence**, not evidence that Candidate A changed its accepted contract.

## 7. Adjudication

Primary cause:

**Malformed backend/court glue.**

More precisely:

- Candidate-A architecture/semantics: **not reached as a lawful-input failure**.
- Candidate-A owner behavior: **correct fail-closed rejection of malformed court input**.
- Backend/court provenance construction: **defective**.
- Stale owner/backend contract mismatch: **proved**, with the stale side being the later backend constructor.
- Missing upstream authority: **disproved** for this field; exact source artifact identity is already present in the accepted governed projection and C11 contract.
- Authority conflict: **none found**. The backend's two-field mini-schema is implementation glue contradicting the accepted owner/C11 authority, not an independent governing source-identity authority.

Therefore RUN3 LiTS-I/A's terminal failure must not be used as Candidate-A comparative evidence.

## 8. Minimal lawful repair surface — do not implement here

### Necessary repair

The repair belongs in the **court/backend R5 provenance construction**, principally:

`rawlsing_next/ee_p2x_darwin_stage_backend.py::_r5_release_identity(...)`

It should construct the source ref from the already-bound governed projection, i.e. the equivalent of:

```python
{
  "kind": "SOURCE_ARTIFACT",
  "object_id": projection.source_artifact_id,
  "content_hash": projection.expected_source_sha256
}
```

with the existing source-SHA equality gate retained.

The backend's stale `_assert_r5_canonical_source_root(...)` expectation should be brought to the same canonical shape so WVS-A/generic Route-A court glue does not preserve the divergent mini-schema.

### Not a lawful repair target

Do **not** repair:

- the frozen Candidate-A owner;
- the accepted `ExactRef` / C11 source-artifact contract;
- the accepted LiTS source authority or source artifact ID;
- the frozen oracle/answer key;
- metric definitions;
- source values or physical-value semantics.

### Optional hardening, not required to repair this cause

`rawlsing_next/fiabc_derivative_parentage.py::assert_r5_root_parent(...)` currently validates only the embedded `content_hash`; it does not reject a missing/wrong `kind` or `object_id`. That explains why current parentage verification can pass the malformed root before Candidate A rejects it.

A future source-free hardening could validate the full canonical source ExactRef. This is a defense-in-depth improvement, not the minimal causal repair.

A shared provenance-construction helper could also prevent future schema drift, but introducing a new abstraction is not required for the minimal repair and should not be smuggled into this adjudicative lane.

## 9. Effect of the lawful repair

| Dimension | Effect |
|---|---|
| Candidate-A semantics | **No change.** The owner and C11 projection semantics remain frozen. |
| Source identity | **No source substitution/change.** Same governed LiTS artifact and same SHA; the malformed mapping is replaced by its already-governed exact identity. |
| Source-native R5 rows / typed physical cells | **No change.** Same `iter_source_native_rows(...)` input and carrier encoding law. |
| Serialized R5 root metadata | **Changes.** The lawful ref adds `object_id` and corrects `kind`. |
| R5 `physical_root_id` | **Changes.** `pre553_r5_compact_carrier.py` lines 531–568 embeds `release_identity` in `unsigned_root` and hashes that whole object for `physical_root_id`. |
| Metric law | **No change.** |
| Exact measured byte metrics | **Must be remeasured in any lawful successor run.** `root.json` bytes are included in steady-state bytes, so a provenance correction has a small but real serialized-size consequence. |
| Frozen answer key / oracle | **No change.** |
| T3 / PRE_CANDIDATE_STOP | **Remain frozen.** |
| RUN3 evidence | The existing RUN3 failure remains historical evidence of a court-glue defect; it cannot be retroactively “patched” into candidate evidence. |

This is why the repair is semantically provenance-only but cannot be applied in place to an already measured R5 root.

## 10. Required source-free qualification before any successor measured run

Recommended tests, all source-free:

1. **Canonical R5 provenance constructor test** — feed a bounded governed projection and assert exact equality to its canonical C11 source ref: `kind == SOURCE_ARTIFACT`, `object_id == projection.source_artifact_id`, `content_hash == projection.expected_source_sha256`.
2. **Route-A frozen-owner intake test** — build a tiny bounded R5 with the backend constructor and prove frozen owner blob `d4915...` accepts it through `build_r5_source_backed_c11_repository(reader, projection)`.
3. **Negative missing-object-id test** — preserve the current fail-closed behavior and exact `R5 release source ref object_id missing` rejection.
4. **Negative wrong-kind test at court boundary** — ensure `SOURCE_SHA256` cannot be emitted/accepted as canonical court provenance even though the owner runtime check only requires nonempty text.
5. **LiTS governed-ID binding test** — source-free accepted projection fixture/authority must produce the exact LiTS object ID URN above, without hardcoding it in the R5 constructor.
6. **Backend canonical-root assertion test** — make `_assert_r5_canonical_source_root` agree with the same full ExactRef contract.
7. **Root determinism test** — two bounded builds with identical canonical release identity reproduce one `physical_root_id`; changing only malformed-vs-lawful provenance changes the root ID while leaving logical stream digest/member payloads invariant.
8. **Parentage hardening test (if that optional guard is changed)** — malformed kind/object_id must fail before owner invocation.
9. **Exception-scope regression test** — malformed court-produced provenance should be classified as court/glue qualification failure in source-free qualification, not counted as candidate-local architectural evidence.
10. **No-drift assertions** — frozen Candidate-A owner commit/blob, T3, PRE_CANDIDATE_STOP, answer-key identities, semantic projection identity, source SHA, and metric-law definitions must be byte-identical.

No real-source execution is needed for these qualifications.

## 11. What must remain frozen

- Candidate-A owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6` and blob `d4915...`.
- Accepted LiTS source SHA and source artifact ID.
- Accepted LiTS governed projection semantics/authority.
- R5 source-native row construction and typed codec/physical-cell semantics.
- Candidate-neutral frozen answer key/oracle, including frozen T3.
- PRE_CANDIDATE_STOP.
- Metric definitions and equal-work law.
- Existing RUN3 work/evidence as immutable historical evidence; no retroactive rewriting.
- Protected measured execution branch/head unless a separately governed successor explicitly qualifies and advances it.

## 12. Residual uncertainty

No authority conflict remains on the adjudicated source-artifact-ref question.

This return does **not** certify every other synthetic field currently populated by `_r5_release_identity(...)` (for example its locally constructed `semantic_release_hash` or `source_release_manifest_hash`) as globally canonical. Those fields were not necessary to prove the RUN3 failure cause and should be audited separately if HQ needs full R5 release-identity provenance closure.

The source-ref defect alone is sufficient and directly demonstrated.

## Final holding

The frozen Candidate-A owner was given an R5 root whose court-constructed `source_artifact_ref` lacked the governed `object_id` and used the wrong provenance `kind`. The owner rejected that malformed input exactly as its accepted fail-closed contract requires. The court then generically wrapped that exception as `CANDIDATE_LOCAL_FAILURE`.

**Primary terminal classification:**

`RUN3_LITSA_VOID_AS_CANDIDATE_EVIDENCE__COURT_PROVENANCE_GLUE_DEFECT_PROVED`
