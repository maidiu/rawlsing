# PYAT S2-B / P2-02 — independent G5-R1 recheck

**Verdict: `ACCEPT_SCOPED@S2_SOURCEFREE_DIRECT_I02`.**

Scope: sourcefree direct I02 logical/selector certificate and compatible native
I03 selector admission at the frozen repaired SHA below. This is not S2-C cold
physical body realization, original35 source equivalence, CURRENT permission,
P01–P20/T01–T18, native production authority, or protected merge. G5-R2 remains
the previously adjudicated nonblocking external-root-issuer vulnerability.

## 1. Independence and artifacts

- Reviewer role: same independent nonauthor receiver from
  `review/pyat-s2b-independent-g5-20261113-r1`.
- Prior independent finding: `acfd5b516a5ae8177730aeb672b846fe4e22fdfe`
  (`REVISE_EXACT_DEFECT`, G5-R1).
- Rejected implementation: `155cd1b7244ab22ede804386e6d5253a39fe3587`.
- **Repaired code/test under test:**
  `092db6bc50a6f256756edf8ab1e95981e2d95abe`.
- Author evidence delivery: `b829e7f857a4219a38b0d98aa524bb95184bed3e`.
- PR under test: https://github.com/maidiu/rawlsing/pull/994
- Review branch: `review/pyat-s2b-independent-g5-recheck-20261113-r1`.
- Protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e` remains an
  ancestor; no protected merge or protected modification.

Artifact checks (`logs/01_ARTIFACT_VERIFICATION.txt`):

- `rawlsing_next` diff between repaired code/test `092db6b` and evidence
  `b829e7f` is empty (evidence commit is documentation only).
- Changed files from rejected `155cd1b` to repaired `092db6b` are exactly
  `_pre553_external_i02_certificate.py` and the external certificate test.
- `_pre553_direct_i02_sourcefree.py` is unchanged by this repair.
- The protected PRE-MAIN commit is an ancestor of the reviewed evidence HEAD.

## 2. Sound execution filesystem

The author's degraded VM was not used. This recheck ran in a fresh Linux VM:

- Lima 2.3.0, `lima-s2b-g5r2`, Ubuntu 26.10, kernel `7.3.0-9-generic`,
  x86_64, 2 vCPU, 4 GiB RAM.
- Fresh root ext4 `/dev/vda1`: filesystem state **clean**, writable; `/tmp` on
  the same ext4, 7+ GiB free.
- Python `3.11.18`, pytest `9.2.0`, pyarrow `26.0.1`, pandas `3.1.1`,
  pyreadstat `1.3.7`.
- `/proc/self/fd` present; descriptor-pinned cold verification exercised.

`logs/00_ENVIRONMENT.txt`. No timing below is used as a performance benchmark.

## 3. G5-R1 recheck — malformed cold header

### Four original attacks

The original independent attack was rerun against repaired `092db6b`:

```text
invalid-json TYPED_REFUSAL ExternalI02IntegrityError certified M01-M18 coverage header is not valid JSON
missing-key  TYPED_REFUSAL ExternalI02IntegrityError certified M01-M18 coverage header missing or non-text
json-null    TYPED_REFUSAL ExternalI02IntegrityError M01-M18 missing or malformed in certified header
json-number  TYPED_REFUSAL ExternalI02IntegrityError M01-M18 missing or malformed in certified header
```

`logs/02_ORIGINAL_FOUR_ATTACKS_REPAIRED.log`.

### Extended independent attack and closure

An independent review script exercised direct and derived legacy-schema
certificates with invalid JSON, absent coverage, null, number, array, string,
empty object, missing/extra atom, empty/non-array/non-text/wrong atom bodies,
and a forged-both-roots malformed variant. Every refusal was
`ExternalI02IntegrityError`; no certificate object was returned. The untouched
original certificate still cold-opened and served real native selector refs.

Open file descriptors were counted before and after every refusal, three times
per case and schema: stable at 4, no DB or descriptor leak.
`logs/04_INDEPENDENT_ATTACK_AND_FD_CLOSURE.log`.

The repaired regression test also passes (`logs/03_G5R1_REGRESSION_TEST.log`).

### Logical-root trust

Physical-root-only rehash attacks still refuse; a malformed header with both
roots forged still refuses typed because the header type boundary precedes
native selection. Independently exercised trust checks:
`logs/10_LOGICAL_ROOT_TRUST.log`.

## 4. Regression, repairs, parity and native consumer

- Full court: **130 passed, 0 failed, 0 skipped** in 22.24 s on the fresh VM;
  process max RSS 149,296 KiB.
  `logs/05_FULL_COURT_130.log`, `logs/06_FULL_COURT_130.xml`.
- Original six repairs and G5-R1: **9 targeted tests passed**
  (`logs/07_TARGETED_9.log`). Prior frozen RED for D1–D6 is preserved at
  `logs/14_PRIOR_FROZEN_SIX_REPAIR_RED.log`.
- Historical parity probes are green for base, weights, reversed order,
  aliases, multi-universe relation, all optional internal families and the
  legacy-valid no-ReplayManifest-count case (`logs/08_PARITY_PROBES.log`).
- Actual native I03 full query independently reproduced:
  **2 → 3 → 2** with changed logical root and exact restoration
  (`logs/09_NATIVE_2_3_2.log`).
- Direct 2,048-event material probe: 13,135,872 B retained, 42,716 KiB process
  RSS (`logs/11_MATERIAL_2048.log`).
- 100,000 one-shot events / **1 respondent**: 638,414,848 B retained SQLite,
  40,424 KiB process RSS, 2,231,458 B Python builder peak
  (`logs/12_SCALE_100000.log`). Not 100k respondents or 6 GiB; timing not used
  as a benchmark.

## 5. G5-R2 — preserved nonblocking

The previously adjudicated forged-external-root selector-omission attack is
unchanged: with both roots fraudulently replaced, the direct installer accepts
and native selection returns 1 where the sealed release requires 2
(`logs/13_G5R2_NONBLOCKING.log`). This remains defense-in-depth for a future
competent root issuer/integration; it is not a new acceptance condition and is
not marked native/production accepted.

## 6. Gate disposition

- **G1:** PASS at scoped sourcefree typed-section evidence.
- **G2:** PASS at direct-selector plus sealed-body scope.
- **G3:** PASS at tested hostile scope; G5-R1 typed-refusal defect is closed.
- **G4:** PASS at measured sourcefree scope; 100k respondents, integrated 6 GiB,
  process-tree RSS and live S1-B/E adapter remain named external/unmeasured.
- **G5:** `ACCEPT_SCOPED@S2_SOURCEFREE_DIRECT_I02`.

Authority holds remain: original35 source equivalence HELD; CURRENT NOT ISSUED;
P01–P20/T01–T18 HELD; S2-A receiving PENDING; S2-C cold physical NOT BUILT;
W03/W04 PAUSED; protected merge NONE; native production permissions NONE;
competent external root issuer NOT ESTABLISHED.

## 7. Evidence index

All under `WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_RECHECK_R2/`:

- `01_G5_RECHECK_RECEIPT.json`
- `02_EXACT_REPAIR_DIFF.patch`
- `logs/00…15`
- `scripts/attack_and_closure.py`, `scripts/native_2_3_2.py`
- `attacks/attack_malformed_header.py`,
  `attacks/attack_selector_omission_forged_root.py`
- `SHA256SUMS`

R3S STOP. No further author duel, no additional reviewer chain, no protected
merge, no original35 or production authority.
