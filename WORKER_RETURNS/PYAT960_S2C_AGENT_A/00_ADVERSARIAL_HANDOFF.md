# S2-C Agent A — adversarial handoff, local runner defect repair

Status: **SOURCEFREE IMPLEMENTATION CANDIDATE / NOT ACCEPTED / B ATTACK REQUIRED**.

## 1. Artifact and lineage

- PR: https://github.com/maidiu/rawlsing/pull/984 (draft, isolated).
- Branch: \`agent/pyat960-s2c-parquet-agent-a-20261113-r1\`
- Frozen composed base: \`591056a948fb0fdd68adbd581301dd903485adc8\`.
- Initial A implementation/test/workflow HEAD: \`c735f42da2b59c869865b9f77ec6872df79d5f02\`.
- Source-level MappingProxyType correction: \`7b387485babddf01bcfe6cd92a84d51b2b70f968\`.
- Added strict mapping/negative test: \`3be87c57393ccab66d40f66b2e7140adc8398282\`.
- Implementation: \`rawlsing_next/pre553_source_direct_parquet_estate.py\`.
- Tests: \`rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py\`.
- CI workflow: \`.github/workflows/pyat-s2c-source-direct-candidate.yml\`.
- This handoff is documentary only; the executable code/test evidence cut remains the SHA ending \`8282\`. Pin the actual descendant branch HEAD for review.

## 2. Governing source

- Oct28 architecture \`315251451a6d112fb312a6a2e80b096d345c5de6\`; Nov11–12 current source-direct vision in issues #960 and #978.
- Original #919 S2-C P2-03/P2-04; #909 R3/R3C/R3S; adopted MCR-lite.
- Preserve 13 typed C11 family inputs, full M01–M18 I02 validation and exact semantic meaning; direct respondent-aligned Parquet/Zstd, source/operation/authority/occurrence completeness, external roots, safe private publication, bounded cold native read.
- Do not reinstate full object-first \`C11LogicalRelease.public_objects/internal_records\`, giant replay closure, copied \`C11Repository\` or duplicate persistent event-body SQLite. Retain historical legacy reader independently.
- One selected genuine native I03 first consumer and change/restore are required for S2-C acceptance at that grade. S2-D other consumers, source rights, original35 science, N11/N12 and 100k/6GiB are separate.

## 3. What actually works at the **previous** SHA (external local runner return)

The user-provided independent local runner reports exact \`c735f42da2b59c869865b9f77ec6872df79d5f02\`:

- Focused S2-C: **6 passed, 1 failed**, reproduced on macOS and Linux.
- Inherited: **Linux 87/87 passed**; macOS **55 passed, 32 environment-blocked** by S2-B's Linux \`/proc/self/fd\` verifier.
- Hostile targets 1–7 reportedly PASS at test fixture grade; native I03 target 8 NOT_RUN/SOURCE_INTERFACE_BLOCKED.
- Fixture: retained 184,074 B; peak staging/total 276,187 B; write 0.513 s; cold open 0.0027 s; process-tree peak RSS 96,928 KiB.
- Runner outputs reside at local path \`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-s2c-agent-a-local-run-20261112-r1-output/\`, which this GitHub author could not independently access.
- **These are user-reported observations of the old SHA; no test result for the repaired SHA is claimed.** GitHub workflows have reported failure but exposed no usable job-step/log evidence; CI green is not claimed.

## 4. Root-cause repair already committed

The old \`select_events\` guard required \`type(respondent_ref) is ExactRef\` and same for \`target\`. Actual \`CanonicalSemanticObject\` carries immutable mapping-proxy references. It therefore refused its own valid semantic references before the reader could select its first event. The existing \`pre553_empirical_objects.exact_ref\` enforces exactly \`kind/object_id/content_hash\` and valid SHA; A now canonicalizes both selectors and maintains exact-type and malformed-ref refusal. A added a regression against valid \`MappingProxyType\` and plain mappings, extra-field forgery and invalid hash.

**Mandatory immediate follow-up:** rerun full focused S2-C at SHA \`3be87c57393ccab66d40f66b2e7140adc8398282\` (or documentary descendant) and inherited direct-I02/sourcefree native tests. Do not claim 8/8 until actually observed.

\`\`\`bash
PYTHONPATH=. python3 -m pytest -vv -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py
PYTHONPATH=. python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_empirical_query.py
\`\`\`

## 5. Serious open attack surfaces — NOT disguised as completion

1. **Native first reader missing:** \`VerifiedDirectEstate.select_events\` is a standalone reader; actual \`CarrierNeutralResearchExecutor.execute_i03\` / certified read-session integration and real changed/restore are NOT_RUN. No accepting a mock.
2. **Physical/global completeness:** writer's direct-S2-B certificate is temporary SQLite and removed; cold estate validation trusts externally held manifest+I02 roots but has not independently established an on-disk source-canonical selector-complement/nonmembership equivalence proof. Dropped or misassigned postings with recomputed local roots remain a high-priority hostile target.
3. **Path TOCTOU:** path-symlink and nlink static checks are not a descriptor-anchored \`openat\` no-follow security guarantee against a concurrent hostile parent swap. Atomic publish uses a preexisting root and no-clobber directory claim, but full race/crash/orphan tests are not run.
4. **Resource economy:** event locator scans all postings and per-family Parquet carries canonical JSON body plus typed/selector columns; physically redundant columns, peak scratch, cold index locality, and 100k real respondents/6GiB remain unproved. Do not confuse fixture metrics with large-scale design sufficiency.
5. **Authority:** a caller-supplied boolean \`current_authorizer\` is not an independently competent production issuer; no original35/source rights/CURRENT granted.
6. **Exact body replay:** original ReplayManifest is recovered as S2-B hash, not an actual persisted replay object; full bounded physical replay reconstruction and all original scientific/negative/provenance effects need adversarial proof.
7. **Cross-owner interface:** real Q2/S1-E source decoder one-pass body feed and independent S2-B G5 remain pending; sourcefree fixture is not a permission for original respondents.
8. **Recovery:** crash mid-publish leaves an orphan that the cold reader refuses, but automatic bounded orphan cleanup and independent recovery across restarts are not demonstrated.
9. **Portability:** original S2-B \`VerifiedExternalI02\` needs Linux \`/proc/self/fd\`; the estate's own reader is portable but no source-native universal S2-B portable verification is proved.

## 6. Alternatives explicitly rejected

- Old \`ParquetC11Carrier.persist/reopen\` as mandatory writer/reader: O(all objects) arrays, full relation Arrow materialization, eager whole \`pq.read_table(...).to_pylist()\`.
- Copying the temporary direct-I02 SQLite \`objects\` table as a second permanent authoritative event-body store: it does not contain bodies anyway.
- Accepting local member hashes without independently supplied roots/currentness.
- Launching W03/W04 or wholesale cherry-picking their paused branches.
- Inventing a new statistical/SQL semantic issuer in place of existing native I03.

## 7. Evidence grade and clear boundaries

- Agent A candidate: implementation exists at sourcefree fixture grade. Latest repair code/tests committed but **not yet locally rerun**. G5 NOT_RUN, protected merge NONE.
- No source-native SAV/DTA/Original35 demonstration; no entrusted production root/issuer.
- No native first-consumer changed/restore claim; no S2-D success.
- No integrated 100k-respondent/6GiB, crash-restart, race-proof filesystem or full scientific acceptance.
- **B should attack, causally repair or replace, freeze its own descendant and return code/tests/evidence.** Do not spend time on bureaucracy or optional hardening.

## 8. Immediate ranking for B

1. Reproduce A's patched mapping-ref test and independently challenge invalid accepted mappings.
2. Forge physical selector omission/misdirection, recompute manifest locally, try to fool independently pinned cold root.
3. Make the real I03 first reader run without constructing the forbidden giant release.
4. Compare simple row-group index vs global locator scan and demonstrate bounded cold resource economics.
5. Threat model no-follow publication with hostile symlink swap and hard crash.

This is an adversarial engineering handoff, **not a request to accept A**.
