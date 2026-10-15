# R4 D2R — independent actual Python/JUnit

**Verified runtime:** Python 3.13.5, pytest 9.0.2, git 2.47.3. Source rooted isolated `/mnt/data/r4_d2r_clean` (not user Mac). Original pinned `D2P:external_fields.py`, `D2P:n9c_reader.py` and `N9C:n9c_fields.json` materialized from authenticated GitHub file returns and checked with `sha1(b'blob '+len+b'\\0'+bytes)` against exact GitHub blob IDs: `583f60559bb04232a1165e85b708079247ceb5f6`, `03eb46efccadd6880cb34b2e2ac609ffc9b16c59`, `1a1bec6e2fc5a89e2ea1b589832801a43933a632`. No filesystem Python module replacement by local mocks; imports `d2p.external_fields` and `d2p.n9c_reader` were actual pinned files.

**Positive independent freeze:**
```bash
cd /mnt/data/r4_d2r_clean
PYTHONPATH=$PWD python -m pytest -q repro/test_d2r_sourcefree_hostiles.py --junitxml=repro/positive_junit.xml
# exit 0, 35 passed in 0.15s
```
Test source Git blob SHA `65ffd5f37e10b1f7563568027d6411873898e4ca`, size 8491 bytes. Includes 35 actual parameterized cases: both official arithmetic identities, native scope and units, exactly disjoint fields/determinants, field-ref dereference refusal, 5 historical cutoffs, nonpositive partial, GSS-only and NCA-only mutation plus old/new independent refs and unaffected opposite role, source-revocation dependency-readset retention, issuer/signature/SHA/permission forgery x6, NCA invalid unit/mode/population label x5, GSS personal-unit and mains-only rejection, excluded vacant/secondary required, false-person/pool/model inference x3, unissued EE13, malformed asof, CURRENT clock refusal and exact replay. This is **not** an issued world.

**Mandatory acceptance REDs (genuine pytest failures):**
```bash
cd /mnt/data/r4_d2r_clean
PYTHONPATH=$PWD python -m pytest -q repro/test_d2r_required_integrity_red.py --junitxml=repro/negative_junit.xml
# exit 1; seven failed in 0.11s
```
Test source SHA `323beb9216dc81ad4f8efc0cdca772c995d497a8`, size 3448 bytes. All seven as explicit must-raise / exact-ref assertions. Not skipped/xfail. Negative original stdout exactly:
- RED01: `REFUSED_REQUIRED_FIELD_TEST_ONLY` vs required `TWO_VALUES_READ_TEST_ONLY` when directly supplying D2P refs.
- RED02: `dependency_readset` N9C refs, not exact D2P produced refs.
- RED03: mutable field payload changed after emission; `field_content_ref` returns old ref rather than rejecting.
- RED04: N9C registry accepts forged `issuer_signature` (D2P authority check correctly would refuse).
- RED05: N9C five-electric-subtypes validation permits renaming `wind` to `hydro_turbine` if sum/length conserved.
- RED06: D2P producer directly emits field labeled `PERSON_WITH_MOBILE_DATA` (N9C reader refuses when separately offered rows).
- RED07: N9C source registry accepts `publisher='Invented Census Foundation'` under same role/family.

**Bounds on RED04–07:** the registry and producer never claim they authenticate original binary sources; these tests specify *required* boundary closure if used together. They reveal schema/identity/issuer trust holes before any adopted owner, not a real-world source impersonation proven to occur. Native labels and issuer proof must be pinned by competent independent source issuer rather than self-authenticated caller strings.

**Receipt file identities:** locally generated `positive_junit.xml` 5561 bytes Git blob `171c1a51c4d28e0d618c818b35f82e1075a917f1`; `negative_junit.xml` 7154 bytes Git blob `318845630dfe848a3e658ce77c20b64204c4b876`; positive stdout `3b92486ebd80e5c1a907287c7e5b9cfe210ccc1a`; negative stdout `d0b5cbef02ec8f72a72b097ffaa0b1468acfaede`. Available in the actual retained host execution; GitHub return includes this run manifest and exact code IDs.

**Historical author tests are NOT new independent results.** Read D2P's committed JUnit, SHA `baa20d37f5cf46af4ba745018fb69ee5ab277d1a`, `tests=29`, `failures=0`, `errors=0`, `skipped=0`; author's log `29 passed in 0.38s`. D2P's additional 47 N9C and 40 D2I were **reported by D2P**, not independently rerun in this R4 host. Complete `rawlsing_next.pre553_learned_world_composition` imports demand more historically pinned modules than this browser sandbox physically staged. Therefore the original 29+47+40 rerun is `NOT_EXECUTED_IN_R4`; no claim of 116 independent green or actual accepted-owner call. Prior reported `compose_direct_producer` receipt remains evidence of an explicitly TEST_ONLY transport route, not a field owner/N9 reader.

**No original PDF binary SHA/sizes** despite web parsed original official tables; container direct HTTP transport unresolved. `curl`/publisher archive not made into an invented custody result. No original respondent or licensee records, physical source-issued N5/N6, authorized N7/EE13 or current OC05 test.
