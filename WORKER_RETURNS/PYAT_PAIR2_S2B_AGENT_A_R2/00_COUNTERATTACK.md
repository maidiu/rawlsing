# PYAT S2-B / P2-02 — Agent A reciprocal adversarial engineering return

**CURRENT RESULT:** \`REVISE_EXACT_DEFECT__A_B_A_LINEAGE_PRESERVED__COUNTERATTACK_CODE_COMMITTED__NEW_CI_EXECUTION_UNVERIFIED__G5_NOT_RUN\`

**This is unambiguously the user's S2-B/P2-02/issue #919 commission**, under #909 R3/R3C/R3S. An S1-C label in B's inherited narrative is not the controlling assignment. Do not restart this S2-B lineage, or promote its incomplete physical/source-direct proof.

## 1. Exact artifact and actual evidence grade

- Initial A: [PR #952](https://github.com/maidiu/rawlsing/pull/952) @ \`d5d6577b557fa8ced2dbb42d190ab254ab983b19\`.
- Opposing B: [PR #954](https://github.com/maidiu/rawlsing/pull/954) @ **frozen** \`f5ee89b8e700ac14cf266c2e3eae4c25f021c349\`; [**88/88 PASS at B's exact HEAD**](https://github.com/maidiu/rawlsing/actions/runs/43278005794).
- Reciprocal A: [PR #957](https://github.com/maidiu/rawlsing/pull/957), branch \`agent/pyat-pair2-s2b-a-counterattack-20261112-r2\`, based **directly on B**. **Final source/test cut:** \`b2931f9ccce0a5e2cd4b680a80a52c87f88f068f\`. Only this return and JSON receipt follow that code/test cut.
- Original G5-pending S2-A input: [#944](https://github.com/maidiu/rawlsing/pull/944) @ \`d3814d08dbe03b8464ac6fff4164765179869213\`, still draft/unmerged at last verification.
- Protected PRE-MAIN: \`6a5c12f04323d74001f9632063ec907f4fc4468e\`, unchanged. W03/W04 remain paused. No source/scientific grants, no protected merge, no S2-C physical reader and no G5 by either duel agent.

**Changed code paths since B frozen HEAD:**
\`rawlsing_next/_pre553_external_i02_certificate.py\`,
\`rawlsing_next/tests/test_pre553_external_i02_certificate.py\`,
\`rawlsing_next/tests/repro_s2b_sqlite_session_attack_stdlib.py\`,
\`.github/workflows/pyat-pair2-s2b-external-i02.yml\`.
Handoff artifacts: this markdown and \`01_G1_G5_RECEIPT.json\`.

**Run exactly:**
\`\`\`bash
git checkout b2931f9ccce0a5e2cd4b680a80a52c87f88f068f
python rawlsing_next/tests/repro_s2b_sqlite_session_attack_stdlib.py
python -m pip install pytest pyarrow pandas pyreadstat
PYTHONPATH=. /usr/bin/time -v python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py
PYTHONPATH=. /usr/bin/time -v python -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py::test_s2b_material_sourcefree_resource_probe
\`\`\`
Any failed real native test is a **defect to fix**, not an acceptable formalism exception.

## 2. B's genuine victories preserved

The successor must preserve B's reproduced four failures and causal repairs:
1. A fake certificate-shaped object carrying the legitimate external roots and respondent census could install empty selector postings into native I03.
2. An overrideable verified subclass could impersonate the certified selector.
3. A closed verifier could leak \`sqlite3.ProgrammingError\` to the native consumer instead of typed integrity refusal.
4. Reassigning the genuine verifier's \`db\` connection **after** cold root verification actually changed real native I03 facts. B self-attacked its first repair and fixed this.

I independently inspected B's frozen code/diff, both RED records and final GREEN record. These are genuine improvements. A's derived corpus/keyspace certificate, externally supplied logical+physical roots, paired alias/occurrence/typed states, positive I03 fact/replay and B's four corrected boundaries are retained. No unrelated scientific evaluator rewrite.

## 3. New attack: an immutable verifier can still have a mutable SQL *session*

### G3-NEW-01 — TEMP-table counterfeit of semantic selectors

**Exact inherited surface:** \`VerifiedExternalI02.db\` was a public \`sqlite3.Connection\`, even after \`_sealed=True\`. The caller could call \`PRAGMA query_only=OFF\`, then create a TEMP \`selectors\` table with zero or forged postings. In SQLite an unqualified \`FROM selectors\` resolves the attacker-created TEMP table before the root-verified \`main.selectors\`. The actual saved file, held SHA256 roots, verifier class and Python attributes remain unchanged, while the ordinary native I03 range consumer can silently see EMPTY.

**Reproduced SQLite primitive locally** with \`python rawlsing_next/tests/repro_s2b_sqlite_session_attack_stdlib.py\`: same connection yields \`count=2\` originally, \`count=0\` unqualified under TEMP shadow, and \`count=2\` for \`main.selectors\`; saved original file untouched. **This standalone result is not a measured real-native-I03 changed-fact run.**

**Repair:** qualify all certified corpus/closure/binding/selector queries with \`main\` and replace the post-verified raw connection with a read-only SELECT facade, so ordinary callers cannot change \`query_only\` or create TEMP objects. Hostile native test \`test_s2b_a_counterattack_sqlite_temp_selector_shadow_changes_real_i03\` added; new-HEAD CI still execution-blocked (below).

### G3-NEW-02 — BINARY collation poisons even \`main\`-qualified queries

SQLite permits \`sqlite3.Connection.create_collation('BINARY', fn)\` after validation. A comparator returning 0 can change \`WHERE respondent=?\` equality and admit unrelated event rows while roots and main tables are unchanged. **Independently reproduced locally**: the same main-qualified query returns one event before the override, two afterward. This shows why simply qualifying \`main\` is inadequate.

**Repair:** no raw SQLite connection or raw cursor leaks from the certified public object after the cold verification. \`_VerifiedSelectOnlyDatabase\` exposes SELECT-only results; \`_VerifiedSqlRows\` wraps cursor fetch/iteration and does not expose \`Cursor.connection\`. Both have slots and immutable backing handles, after a deliberate self-attack showed my first facade would have reproduced B's ordinary assignment vulnerability one level down. Native attack tests include collation override and nested facade/cursor reassignment.

**Boundary:** private Python introspection, \`object.__setattr__\`, malicious extension/C code, filesystem adversaries and OS/process compromise are not turned into a cryptographic sandbox claim. This is a concrete *public API* integrity repair.

### G3-NEW-03 — cursor closes *between* selected occurrences

The inherited verifier checked open state only at call boundaries, so a streaming cursor could be invalidated after yielding an earlier event and surface a raw SQLite failure. \`_rows\` now checks lifecycle around each row and converts invalidated SQLite errors to typed \`ExternalI02IntegrityError\`. Test \`test_s2b_a_counterattack_midstream_close_typed_refusal\` closes after the first of two real-I02 duplicate occurrences.

### G4-NEW-04 — final-name publication was not no-clobber

The builder checked \`target.exists()\` and later used \`os.replace(staged,target)\`. This silently overwrites a second writer's newly claimed output between the two operations, violating the explicit exclusive-writer discipline and transactional custody. The local stdlib reproducer verifies atomic \`os.link\` refusal against an already claimed final path. Builder now uses a same-directory fsynced staged file and \`os.link(...,follow_symlinks=False)\` as the atomic no-clobber publication; on name collision it fails closed and cleans only its own stage. A crash between link and unlink can leave a duplicate stage orphan, not an incompletely initialized published artifact. Test \`test_s2b_a_counterattack_publication_cannot_clobber_rival\` exercises the exact race with a real sourcefree I02 fixture.

## 4. Execution — mandatory honesty

**Verified executable evidence:**
- B original [Actions #43278005794](https://github.com/maidiu/rawlsing/actions/runs/43278005794) at \`f5ee89b8e700ac14cf266c2e3eae4c25f021c349\`: 88/88 **PASS**. This is a **parent** result, not A R2 proof.
- Standalone zero-dependency SQL/OS reproducer executed locally on Linux/Python 3.11+; output:
\`\`\`text
SQL_TEMP_SHADOW: RED unqualified=0; GREEN main=2; held disk unchanged
BINARY_COLLATION: RED main-qualified WHERE gained unrelated event
ATOMIC_LINK: GREEN existing destination retained without clobber
STANDALONE_G3_G4_PRIMITIVE_REPRODUCTION_PASS
\`\`\`
- The new G3/G4 native I03 + certificate + B 88-case regression tests have **NOT executed successfully** on this branch. [R2 Actions #43281068800](https://github.com/maidiu/rawlsing/actions/runs/43281068800) and subsequent runs failed before reporting any runner steps; run details show \`steps=null\`, approximately four seconds. A rerun failed the same way; other repository PYAT workflows also displayed no steps. Therefore: **RUNNER/BILLING/PLATFORM EXECUTION BLOCKER—NOT EVIDENCE OF SOURCE GREEN OR RED**. Do not infer test correctness from this. Run the exact commands above on a working executor before promotion.
- The 2,048 respondent sourcefree resource measurements remain B's inherited numbers only; **R2 resource overhead NOT MEASURED**. Integrated 100k/6 GiB, peak scratch and process-tree RSS still NOT_RUN.

## 5. Original G1–G5 contract: conserve the mission

| Gate | R2 evidence | What remains |
| --- | --- | --- |
| G1 | PARTIAL: true legacy M01–M18 verified input conserved, derived whole-corpus+selector hash/aliases unaffected in intended logic | Full independent bounded **source-direct** I02 validator missing; P01–P20/T01–T18 and CURRENT separate |
| G2 | PARTIAL: B actual native I03/changed/restore positives and four repairs at tested parent; R2 stronger binding code | R2 new-native suite not executed; legacy materialized repository still required |
| G3 | PARTIAL: local SQL TEMP/collation falsifiers reproduced; new native tests committed and repairs implemented | Actual R2 new-native tests remain unexecuted; filesystem/hostile-process boundary not established |
| G4 | PARTIAL: derived disk sorter, inherited 2048 resource case; local no-clobber primitive passed | R2 resources unmeasured, legacy \`ReplayManifest.closure_refs\` O(all refs), 100k/6 GiB integrated proof absent |
| G5 | NOT_RUN | Requires one separate nonauthor reviewer (neither A nor B) after actual G1–G4 evidence |

The **largest unresolved S2-B engineering obligation** remains replacing legacy fully materialized \`C11LogicalRelease\` and \`ReplayManifest.closure_refs\` with genuinely bounded source-direct M01–M18 certification and full native I03 comparison. Do not relabel this as merely a rights HOLD. S2-C compact physical saved bodies remain a separate packet; original35 source/scientific/current/root-issuer rights must not be fabricated.

## 6. Best remaining adversarial attacks / failure surfaces

1. **First priority:** obtain a working executor; independently run new native I03 counterexamples and the entire inherited court at exact R2 code cut. Repair any actual regression before G5. Green B tests at another commit do not substitute.
2. Inspect whether even the restricted SELECT facade leaks an alterable SQL session through ordinary API; the nested backing slots are immutable under normal assignment but Python co-resident arbitrary private manipulation remains out-of-scope.
3. Attempt hostile file replacement **between whole-file physical SHA256 and SQLite open**, including same-semantics/different-physical saved bytes. The current physical-root TOCTOU proof is incomplete under an actively hostile filesystem. If a real allowed adversary can falsify correct cold acceptance, repair with same-descriptor or copied verified snapshot rather than more admission ceremonies.
4. Reconstruct exact M01–M18 source-direct streaming validator from S1-B actual sourcefree input, preserving original absent-state and authorized alias/occurrence semantics. Do not fake old \`C11LogicalRelease\` seal, and do not require a whole object-shaped canonical rehydration.
5. Physical 100k sample economics, peak scratch and process-tree RSS, cold I03 latency, atomic stage/orphan restart, independently held external roots/issuer remain unproved. A/B cannot self-grant G5.

## 7. Alternatives considered

- **Only qualify \`main\`: REJECTED** because locally reproducible \`BINARY\` collation changes equality on main tables.
- **Just set \`PRAGMA query_only=ON\`: REJECTED** because a public caller can turn it OFF and install TEMP tables.
- **Subclass B's verifier or counterfeit a second seal:** REJECTED; B's exact-type guard and independent roots are preserved.
- **Return raw SELECT SQLite cursors:** REJECTED because \`cursor.connection\` exposes mutable SQL session; wrapper used.
- **Keep first mutable cursor/connection wrapper:** REJECTED after own assessment; ordinary assignment could duplicate B's DB swap via nested state, so wrappers now immutable.
- **Replace all scientific query logic with SQL:** REJECTED; actual I03 evaluator and its meanings must be conserved.
- **A new owner committee or a new source/issuer permission:** REJECTED; execute sourcefree and keep competent authority boundaries separate.

**Return to independent receiving:** \`REVISE_EXACT_DEFECT\`, **not** G5-ready. User instruction is to move once executable G1–G4 hard exit is satisfied, not proliferate review loops.
