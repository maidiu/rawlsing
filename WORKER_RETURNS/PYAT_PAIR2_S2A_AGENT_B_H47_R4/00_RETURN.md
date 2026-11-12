# PROGRAMMA PYAT / Pair 2 / S2-A — Agent B R4 receiving handoff

**Return disposition:** `READY_FOR_INDEPENDENT_G5_AT_SOURCEFREE_NATIVE_GRADE`; **NOT TERMINAL_CLOSED**, not a protected merge, and no S2-B–G work. Source/host/original35 science and external source-backed component issuance remain distinct holds.

**Original binding commission:** [#919 R3 S2-A G1–G5](https://github.com/maidiu/rawlsing/issues/919) and its controlling R3S STOP/ADVANCE rule. This return is a *single bounded defect-specific* repair exchange following Agent A's counterattack, not an indefinite hardening campaign.

## 1. Exact provenance / what was independently reconstructed

- Protected PRE-MAIN was inspected read-only at `6a5c12f04323d74001f9632063ec907f4fc4468e`; no protected or W03/W04 file changed.
- Agent B previous [PR #934](https://github.com/maidiu/rawlsing/pull/934): `c651c3519e83d2399717718ccff71a908e28a899`.
- Agent A corrective [PR #941](https://github.com/maidiu/rawlsing/pull/941), frozen incoming HEAD **`8e58e05882683df65e9813e4e2c8e19b524c5731`**.
- This [draft PR #944](https://github.com/maidiu/rawlsing/pull/944), branch `review/pyat-s2a-range-toctou-20261112-r4`, is based on that exact HEAD; distinct review branch, no write to Agent A or prior Agent B branches. A GitHub branch is not a verified exclusive Mac worker lease or HQ appointment.
- Exact tested source/CI HEAD **`00668714fc4595f2ca950ec727f168e27fe842df`**. This handoff is committed afterward with no source or workflow changes. Read back final report-bearing HEAD for citation.

## 2. Independently verified strengths of Agent A R3 — retained

Agent A's fix is substantive. `_pre553_verified_semantic_range._bindings` builds I02-sealed `(universe, native question, instrument version) -> original (canonical, component) paired grants`. It requires asserted event aliases to coexist within a single exact grant row for each possible version, not in separate allowlists. This preserves valid same-version sibling components and prevents cross-row invented canonical/component combinations. H38/H39/H40 and H42 are negative, H41/H43/H44 preserve allowed variants, H45 exercises the actual sourcefree changed input → native I03 changed fact → restore, and H46 establishes the distinct occurrence-rule provenance limit without inventing a new I02 grant.

My own earlier canonical-only check was inadequate; Agent A's paired-grant construction supersedes it. Preserve the independently held selector witness, full typed-state/occurrence digest before filtering, alias dedup, and the real owner-installed I03 first reader from [PR #934](https://github.com/maidiu/rawlsing/pull/934). All 105 inherited tests remain passing after this repair.

## 3. Exact material defect established — check/use substitution at the real first consumer

S2-A existing G2/G3 H26 requires that a poisoned derived selector cannot silently produce an incorrect supported I03 result; it must **refuse or rebuild**, then restore genuine facts. This is not an invented requirement.

In Agent A R3, `CertifiedRespondentEvents._verified_alias` captured the untrusted `rows = _postings.get(key, ())`, ran `_digest(rows)`, then returned **that same non-frozen Sequence object**. `select()` iterated it a second time via `heapq.merge`. This was a check/use gap. A mutable list, custom Sequence or tuple subclass can change the members observed in the second traversal. The I02 witness authenticates the first traversal only.

H47 used a **genuinely I02-accepted sourcefree release**, with two respondents R1 (Y=1) and R2 (Y=0), and kept the canonical source corpus and held root unchanged. Only the derived secondary posting for R1 was a `FlipAfterDigest(list)`: first iterator produced R1's real event (valid digest), next iterator produced R2's real event. The original source event refs were valid; the mapping from respondent→verified posting was fraudulent.

- Initial hostile RED: test-only commit `4c99e11ef4263d2df655ded2854c4e8ec2ecf0a7`, [CI #43183926672](https://github.com/maidiu/rawlsing/actions/runs/43183926672): **105 passed, H47 failed**, because `SemanticRangeIntegrityError` was not raised after the digest.
- Narrowed native-first-consumer RED: commit `6965dca52e5bca6fe972f64d566c41b18fab8189`, [CI #43184091827](https://github.com/maidiu/rawlsing/actions/runs/43184091827): **105 passed, H47 failed** with assertion `'SUPPORTED' == 'INTEGRITY_FAILURE'`. Direct selector had consumed the wrong respondent's real event after authenticating R1; native `execute_empirical_query` also failed to refuse. That is a reproduced breach of the original frozen G3/H26, not speculative hardening.

## 4. Exact repair, with no semantic-engine rewrite

Changed `rawlsing_next/_pre553_verified_semantic_range.py::_verified_alias`:

```python
rows = self._postings.get(key, ())
if type(rows) is not tuple:
    raise SemanticRangeIntegrityError(
        "uncertified mutable or custom semantic-range posting sequence"
    )
observed = _digest(rows)
```

The original trusted `_bindings` producer emits **exact built-in tuples**. This check is O(1) and guarantees the same immutable sequence is used for verification and subsequent native I03 iteration; it does not allocate a new O(K) snapshot or change the original empirical/routing/replay/math engine. It also refuses deceptive tuple subclasses with overridden `__iter__`.

- H47 now requires actual direct selector `SemanticRangeIntegrityError` and real I03 `INTEGRITY_FAILURE`; reinstall the intact sourcefree I02-derived index restores exact equality of the original full native `QueryExecutionResult`.
- H48 new negative: a `DeceptiveTuple(tuple)` returns different data via custom iteration. It is refused, while a genuine `tuple` from the source-derived builder remains admitted and returns the original exact event.
- All 105 predecessor tests are preserved. This is an in-scope H26 integrity correction, not a requirement to make saved external readers use Python tuples forever. Any future S2-C physical reader would need its own authenticated immutable snapshot/verified cursor equivalent.

## 5. Exact measured GREEN execution and resources

- Native sourcefree court: [GitHub Actions #43184396936](https://github.com/maidiu/rawlsing/actions/runs/43184396936), code/test HEAD `9fb17bd79c8b2ff1a7775db0a06bc4202d621f2a`: **107 passed, 0 failed**.
- To make G4 resource evidence explicit without building S2-B, workflow now prefixes the unchanged full court command with `/usr/bin/time -v` and retains JUnit.
- **Final code/test/CI HEAD `00668714fc4595f2ca950ec727f168e27fe842df`**, [GitHub Actions #43184559352](https://github.com/maidiu/rawlsing/actions/runs/43184559352): job `real-native-selector` success, **107 passed in 6.96s**, `/usr/bin/time` **peak RSS 221,532 KB** (~216.3 MiB), elapsed wall time **7.50 s**, exit 0. This is the Python test process for the full **small-fixture sourcefree court**, NOT a 100k respondent source or an integrated saved-reader 6 GiB/process-tree benchmark.

Exact court:
```bash
PYTHONPATH=. /usr/bin/time -v python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  --junitxml=s2a-pair2.xml
```

## 6. Challenge to my correction / negatives not claimed

- The built-in `tuple` check is **specific to this in-memory I02-derived S2-A adapter**; an arbitrary externally sourced disk stream is not certified by being or becoming a tuple. External saved reads must demonstrate source-independent root membership and immutable checked-consumed bytes under their own S2-C contract. Do **not** extend this as a general science ontology or physical-reader type requirement.
- `_digest` validates each event's full semantic projection against its exact content hash, then the complete selected count+order against the I02 witness; tuple immutability stabilizes the range but cannot grant current source/host permissions.
- `CertifiedRespondentEvents._postings` can still be a mutable dict under synthetic hostile tests; a subsequent replacement with a new built-in tuple must pass the full held digest. Cached index authority is not a cryptographic cross-process issuer.
- No claimed genuine source-backed occurrence→component grant where QVB is typed absent. H46 correctly preserves incumbent native I03 and refuses the extra QVB-only certificate; an upstream qualified occurrence sidecar is an **external evidence/authority HOLD**, not a new S2-A sourcefree requirement to fabricate source rights.
- No full 100k/6GiB test, durable cold saved release, external physical artifact proof, native original35 P05 equivalence or current issuer. Those are not silently inferred from 107 sourcefree tests or from 221,532 KB RSS.
- Existing sourcefree tests were run through GitHub CI and are reproducible; **independent nonauthor G5 terminal receipt was not done**. Do not claim TERMINAL_CLOSED or an HQ merge.

## 7. Disposition against the five frozen gates

| Gate | Grounded state |
|---|---|
| G1 | Original native/canonical/component/repeated state/order contract and source-qualified paired grant checks conserved in inherited tests, with H46 external source-sidecar HOLD disclosed |
| G2 | Native I03 original baseline, poison→refuse→restore, changed sourcefree result→new fact→restore all executed; ordinary I03 owner installer preserved |
| G3 | H26–H46 inherited 105 tests plus reproduced real I03 H47/H48 negative and full restoration: 107/107 PASS, no current reproduced in-scope defect remaining from this bounded court |
| G4 | Bounded selected-page interface, no all-ref inventory tuple, 64-respondent pilot, exact CI peak process RSS 221,532 KB; full 100k benchmark explicitly NOT_RUN per commission |
| G5 | **PENDING mandatory independent nonauthor receiving** |

**R3S STOP/ADVANCE:** With the reproduced H47 fixed and the available frozen G1–G4 sourcefree court green, the only honest next step is independent G5 receiving or exact HQ defect adjudication. No more discretionary coding, competing review fleet, or S2-B–G implementation in this packet.

## 8. Strongest challenge back to Agent A / independent receiving

Reproduce H47 against this exact SHA with an input Sequence that changes between digest and use; show a native I03 SUPPORTED fact from any event not authenticated for its chosen respondent. If that attack fails, test whether a native I02-certified **genuine built-in tuple** can similarly switch membership without changing source release or authoritatively held keyspace. Re-run H38–H46 and original H26/H27 with real I02 ingress and native I03. If no reproduced in-scope SEV-0/1/2 defect survives, stop: receive at sourcefree native S2-A grade, record H46 as external HOLD, and advance through HQ according to the binding STOP rule.

**Final source/test cut: `00668714fc4595f2ca950ec727f168e27fe842df`; report-bearing HEAD follows by one docs-only commit.**