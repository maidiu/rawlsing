# S2-C Agent B — hostile construction return (scoped, unreceived)

## Frozen provenance and grade

- Original authority: PYAT R3 #909 and S2-C/P2-03+P2-04 G1–G5 #919; selected Oct28 physical architecture at `315251451a6d112fb312a6a2e80b096d345c5de6`, target invariant blob `f4c342ea74a444f19cb492d04684e6007979e65d`; canonical MCR-lite in protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e`.
- A source: PR #984 unchanged `85446cfe31e96275e582676381ed382184cfd993`; its initial program/test/CI and mapping repair are retained unchanged as the ancestor. A executable MappingProxy fix cut `3be87c57393ccab66d40f66b2e7140adc8398282`.
- B independent source cut: `85446cfe31e96275e582676381ed382184cfd993`.
- B executable code and tests **exact cut**: `4c998d40a3d6925657df2fabd649a98123e8dffd` on `agent/pyat960-s2c-agent-b-hostile-repair-20261113-r1`. This report is a subsequent documentation-only descendant.
- B proposed receiving: draft PR #987 targeted ONLY to A's author branch. No PR is merged and protected PRE-MAIN is unchanged.
- Changed executable paths ONLY: `rawlsing_next/pre553_source_direct_parquet_estate.py` (blob `da8037b2643915b45fba3d92ec9fd2d1a66098fa`) and `rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py` (blob `0c32a1b15ddeb74a1bde54b1c5cc4844ed77e388`).
- Proof grade: **SOURCE-INSPECTED AND PATCHED / CODE TESTS NOT_EXECUTED**. Independently received G5: NO. Cold native `CarrierNeutralResearchExecutor.execute_i03`: NOT_RUN. Original35/S2-D/native science/rights/actor/protected merge: NOT_GRANTED. Do not infer a real CLI/S2 pass from GitHub checks, which failed without job steps.

## Independently conceded strengths

A retained the 13 typed `SourcefreeDirectI02Sections` source families, produced one-shot typed Parquet/Zstd body members with a metadata-only locator and source-direct temporary I02 SQLite, deleted that proof after publication, and required externally held manifest hash/direct I02 roots for cold read. A used the existing exact canonical object serializer/decoder, reconstructed selected row groups without a full `pq.read_table(...).to_pylist()` call, and truthfully disclosed absent native I03. A's use of `exact_ref` for immutable `MappingProxyType` selectors repairs a genuine contract mismatch; B preserved it. Those are source-level observations, not a newly executed passing court.

## Exact defects and B repairs

1. **Premature unauthorized physical bytes**: A's `VerifiedDirectEstate.__init__` invoked `_hash(manifest)` and `_hash` of all 14 physical members BEFORE `self._live()`. This directly violated G3 CURRENT-before-unauthorized-byte-access. B checks exact root type/held digest/callback and calls `_live` before `_root`, manifest and Parquet byte access. New `test_denied_current_does_not_open_estate_bytes` instruments `Path.open`.
2. **Exact-ref-only misdirected selected events**: A read selector postings based on respondent/question/state and verified only target event ref, allowing a physically wrong posting to return an authentic body to the wrong query. B now crosschecks all five posting selector fields (respondent/native/canonical/component/state) against the decoded exact event; a forged posting does not become a positive native event. Five parametrized hostile cases rehash and repin a newly malformed physical manifest while keeping the direct I02 roots. This does **not** show a bypass of an unchanged independently held manifest hash.
3. **Count-only release false-positive**: A compared only physical event index count against body count before deleting the semantic SQLite proof. Wrong event postings, omitted/duplicated bodies and mismatched typed-family bodies could be published while count remained unchanged. B adds `_verify_emitted_physical_payloads`: a bounded Parquet row-group reconstruction of ALL thirteen typed families, compared by exact ref/family to the existing S2-B direct-I02 object table; event canonical selector, posting, row-group and offset must equal the source-I02-certified event. This happens before scratch deletion and publication, so a wrong new release is refused instead of pinned as valid. Test `test_corrupt_locator_before_publication_refused` injects the wrong respondent without changing actual source or I02.
4. **Self-discovered duplicate-for-missing attack against B's first fix**: Count + individual presence in S2-B still allows two physically emitted copies of one authentic ref to replace another required ref. B added a temporary, stage-local SQLite `seen(ref PRIMARY KEY)` anti-join covering all 13 families, with uniqueness plus per-family counts and direct-I02 ref membership establishing exact no-drop. It is deleted after verification and is not a persistent authoritative corpus. New `test_duplicate_physical_event_cannot_replace_missing_exact_event` injects that precise swap during the physical flush.
5. **Reconstruction regression**: `test_every_emitted_family_cold_reconstructs_at_its_exact_census` traverses all thirteen exact bodies (including truly empty families) at batch size one; no placeholder family is accepted as complete merely because a manifest declares it.

## Why the repairs are causal and proportional

The source is still visited ONCE by the existing one-shot S2-B/Parquet tee. New audit reads Parquet + temporary certified SQLite at build time, not a second original SAV/DTA read or permanent C11 corpus. No native science, query/predicate authority, source decision, historical W03/W04 branch, Q2 owner, protected integration or native math owner was altered. B's branch is an exact descendant with only two changed executable files.

## Execution and preservation evidence

- Verified via GitHub immutable readback: B code blob `da8037b...`; test blob `0c32a1b...`, exact remote executable HEAD `4c998d40a3d6925657df2fabd649a98123e8dffd`.
- Git compare against A `85446cfe...`: 6 descendant commits, only the above code/test paths changed (122 additions/4 deletions code, 126 test additions).
- GitHub CI for earlier B SHA `c948537...` failed in approximately 2 seconds with **zero job steps** and no retrievable job logs; this is not an executed assertion failure or green result. Local container has no GitHub checkout or `pyarrow`, and private repository network access is unavailable. Therefore **all B runtime assertions remain NOT_RUN**.
- Exact local runner preflight required on B executable cut:
  ```bash
  git checkout 4c998d40a3d6925657df2fabd649a98123e8dffd
  python3 -m py_compile rawlsing_next/pre553_source_direct_parquet_estate.py
  PYTHONPATH=. python3 -m pytest -vv -o addopts='' -p no:cacheprovider \
    rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py
  PYTHONPATH=. python3 -m pytest -q -o addopts='' -p no:cacheprovider \
    rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
    rawlsing_next/tests/test_pre553_external_i02_certificate.py \
    rawlsing_next/tests/test_pre553_empirical_query.py
  ```
- No independent resource measurements for B have been made. The bounded full-family build audit plus temporary exact-ref SQLite increases build I/O and peak scratch use; compare before/after CPU, wall, RSS, temp disk, retained bytes and cold selected query speed on the same fixtures. Do not claim faster or 6GiB compliance.

## Attacks refuted / limits preserved

- **Refuted**: S2-B's temporary SQLite certificate is a body store. It contains selector metadata, not event bodies; A correctly feeds physical Parquet from the source stream.
- **Refuted**: A's selected reader obligatorily calls full `pq.read_table`. It reads selected event row groups; it still scans the full locator and verifies file hashes at reopen.
- **Conceded**: A's repaired `MappingProxyType` canonicalization is appropriate and was not reversed.
- **Not proven**: an attacker can replace a fixed externally pinned physical manifest undetected. B's repinning tests model an incorrect newly published/accepted artifact, not breaking SHA256.

## Remaining G1–G5 and stronger adversarial challenge to A

- **Highest-priority G2 gap**: `VerifiedDirectEstate.select_events` is still NOT attached to `CarrierNeutralResearchExecutor.execute_i03`. The existing I03 requires a real `C11Repository`, sealed `C11LogicalRelease` and attested release index; the S2-B direct certificate by itself lacks bodies and is NOT a legacy I02 seal. Build a legitimate owner-reviewed lazy read session/real native first reader, without a complete object-shaped C11 fallback, then test changed legitimate body → changed exact native fact → original root restores. Do not call an in-memory legacy comparator a saved first consumer.
- **Q2 body ABI**: its distinct G5 recheck remained active at last GitHub record, not accepted. Consume ONLY a qualified final body-preserving Q2 ABI; do not bypass the user-paused separate Codex Q3 work or collide with Q2.
- **G3 remaining**: externally held physical-root/selector completeness, wrong CURRENT after opening, symlink TOCTOU/descriptor-anchored root, partial crash/orphans, malformed codec, revoked authority; test only frozen material cases before adding mandatory gates.
- **G4 remaining**: cold reader currently hashes every physical member on open and scans all postings; bound the actual 100k respondents/6GiB and read/cold/repeat performance, including B's new build-time audits and peak scratch. No fixture is a production economy claim.
- **Replay**: exact ReplayManifest `ref` is preserved through S2-B roots, but actual full bounded reconstruction and native replay consumer have NOT been independently proved.
- **Receipt**: external nonauthor G5 still required for S2-C exact frozen code once upstream body/certificate and consumer prerequisites qualify. A new material code failure can justify one exact repair; no recursive ceremony.

**Challenge to Agent A**: On B frozen code, find an admissible native positive/refusal or a real no-drop counterexample that survives B's source-I02/Parquet parity, or construct the real source→cold saved body→native I03 causal first-consumer bridge without full in-memory C11. If B's new full-family audit fails on a valid internal typed object, demonstrate the exact ref/roundtrip violation and provide a smaller correct verifier. If it fails only because of resource overhead, measure it and replace the proof with a bounded equivalent without loosening false EMPTY/UNKNOWN denial.

B does **not** certify its own completion. Return to Agent A and then independent receiving at correct sourcefree scope only after real execution evidence.
