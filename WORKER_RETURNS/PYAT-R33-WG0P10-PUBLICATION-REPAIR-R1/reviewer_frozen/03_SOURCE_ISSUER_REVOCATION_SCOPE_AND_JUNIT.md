# WG0Q Phase B — source, issuer, revocation scope and raw JUnit

**WG0P7 finished remote:** `9ecb9747ed12bae4ee8cfbc955210d1e631d5f76`
**WG0P7 content commit:** `67058a94b53c4bf1d449dabc8dd5a59a650916b2`
**WG0P7 sealed startup:** `a72e75a011468a1f0ea7b251f5b07969f59488e0`
**WG0Q Phase A freeze:** `d8e4c86a7a57e0e519063919831e9aad5c902cfb`
**Review base:** WG0O `3ee5d6a4e246fca89740d4d36ab26206230c83bf`
**Unrepaired parent:** WG0P6 `e7e429c3dfb649233e74e0e5106e51ff25024806`

## 1. Actual imported module identity

The repaired module is not the direct `runtime_phase_b/candidate` copy. The
candidate's own `bootstrap_p6` selects:

`candidate/court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py`

- sha256 **`89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`**
- git blob **`62895078908ff748771da9a9fbcec6b36d34a803`**
- `wg0p4_workload.VERSION` remains `WG0P4_NATIVE_FRONTIER_COLD@1`
- six accepted native owners import only from `pinned/rawlsing_next` under that
  P5 runtime; their hashes match WG0P6 and are unchanged.
- The direct `runtime_phase_b/candidate/repro/wg0p4_workload.py` is the pristine
  WG0P6 module (sha256 `3807e46e...`). It must not be used as the repaired
  module.

**Phase A custody correction:** the first WG0P6 replay used the direct candidate
copy `c74b34d1...` without `bootstrap_p6`, not the P5 module `3807e46e...`; the
corrected actual P5 run gives 8 typed refusals and 18 new-matrix REDs, not 19.
The frozen oracle is unchanged; see `02_PHASE_A_CUSTODY_CORRECTION.json`.

All Phase-B reviewer tests were executed with the candidate's explicit
`bootstrap_p6` identity transport on `PYTHONPATH`; raw per-process receipts are
under `02_WG0P7_STAGED/candidate/observations/imports/`.

## 2. Source transport findings (publication custody)

The published WG0P7 tree is **not self-contained** for bootstrap:

1. **11 inherited observation files are missing from the WG0P7 Git tree** even
   though `SOURCE_INPUTS.json` requires them and `bootstrap_p6` refuses their
   absence. Example:
   `court/runtime_phase_b/candidate/pinned/predecessors/j/observations/baseline.json`.
   They were completed in this review from the byte-identical WG0P6 staging and
   verified against WG0P7's `SOURCE_INPUTS.json` SHA-256. With that completion,
   all 11 missing-file hashes are exact and bootstrap passes.
2. **`SOURCE_INPUTS.json` carries a stale repaired-module hash**
   `06fadc7eb8c01fa832fa59beccfc2ea2f6e068216fdc8b04c95365065d492723`,
   while `CANDIDATE_CODE_PIN.json` and the actual P5 module carry
   `89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`.
   The bootstrap updates source inputs from the candidate pin, so the run is
   correct, but a consumer that reads `SOURCE_INPUTS.json` alone would select
   the wrong module. This is a publication/custody HOLD, not a semantic repair
   failure.
3. `05_PUBLICATION_RECEIPT.json` names final containing content SHA
   `67058a94b...`; the exact finished branch tip is the sealing commit
   `9ecb9747e...`. Both are recorded above.

**Consequence:** adapter integrity can PASS on the verified P5 module, but the
WG0P7 return as published cannot be independently bootstrapped from Git alone
without restoring the 11 inherited files and resolving the stale source-input
entry.

## 3. Raw JUnit / court counts

| Court | JUnit | Tests | PASS | FAIL | Classification |
|---|---|---:|---:|---:|---|
| WG0O original frozen 14 | `04_JUNIT/wg0p7_wg0o_original_14.xml` | 17 | **17** | 0 | 14 controls + 3 meta; A2/A3/A4 closed |
| WG0Q new matrix | `04_JUNIT/wg0p7_wg0q_new_matrix.xml` | 36 | **36** | 0 | 34 controls + 2 meta; every negative typed 0 I03 |
| WG0M frozen descriptor 33 | `04_JUNIT/wg0p7_wg0m33.xml` | 33 | **33** | 0 | inherited |
| Original frozen 65 | `04_JUNIT/wg0p7_original65.xml` | 65 | **65** | 0 | includes original25, conditional yes1/no1, cold 1+2 |
| Original-three provenance | `04_JUNIT/wg0p7_original3.xml` | 3 | **3** | 0 | inherited |
| Original J44 / K11 | `04_JUNIT/wg0p7_j44_k11.xml` | 55 | **55** | 0 | inherited |
| Accepted native owners 80 | `04_JUNIT/wg0p7_owners80.xml` | 80 | **80** | 0 | inherited |
| WG0P6 source-view boundary 42 | `04_JUNIT/wg0p7_fresh42.xml` | 42 | **42** | 0 | inherited |
| WG0N hostiles | `04_JUNIT/wg0p7_inherited_wg0n_hostiles.xml` | 20 | 15 | 5 | **12 executed PASS / 5 unconstructible NOT GREEN** |
| Historical characterisation (unmodified) | `04_JUNIT/wg0p7_historical_characterisation_unmodified.xml` | 3 | 1 | 2 | expected stronger-refusal conflict, not regraded |

The mandatory 236 decomposition reproduced physically:
`33 + 3 + 80 + 55 + 65 = 236`, **236 PASS / 0 FAIL**.

Specific original65 nodes observed PASS:

- `conditional/original25_unchanged`
- `conditional/ordinary_full_chain_yes1_no1_over2`
- `cold/actual_abrupt_exit23_after_one`
- `cold/fresh_process_exactly_two_I03_calls`
- `cold/three_original_consumer_values`
- `cold/full_frontier25_retained`
- `cold/source_edition_currentness_refuse`

## 4. Closed REDs and preserved positives

| Control | WG0P6 | WG0P7 |
|---|---|---|
| A2 stale/superseded body | SERVED 42 / 4 I03 | `AuthorityCurrentnessHold` / HELD, 0 / 0 |
| A3 same-hash foreign body | SERVED 42 / 4 I03 | `IdentityError` / REFUSED, 0 / 0 |
| A4 foreign governed operations | SERVED 42 / 4 I03 | `IdentityError` / REFUSED, 0 / 0 |
| 18 WG0Q new body/temporal REDs on actual WG0P6 P5 | served or untyped after I03 | typed refusal, 0 / 0 |
| S1 source-artifact-ref swap | already typed on WG0P6 P5 | typed refusal, 0 / 0 |
| P1/P2/P3 positives | 42 cells, 4 I03 | 42 cells, 4 I03; consumer SHA-256 unchanged |
| Valid cold restore | works | works, 0 I03 |

The pristine consumer values are byte-identical between WG0O and WG0Q:
`4b9d03246167c93df6dde8d590fac33c24c51ef158d60abd8ee33601ca059550`.

## 5. Revocation / issuer scope

- **C1 source-artifact revocation:** `RevocationError`
  `UNKNOWN_RELEASE_NO_REVOCATION` remains the honest typed ceiling. The owner
  can revoke release tags, not independent source artifacts. This is **not
  green**.
- **C2 missing independent issuer:** now typed `IdentityError` /
  `RELEASE_VIEW_SOURCE_BINDING_UNRESOLVABLE`, zero served, zero I03. The caller
  grant hint is still `TEST_ONLY_HINT_CANNOT_ISSUE_PERMISSION`.
- **Independent signed issuer:** absent. No Git hash is treated as a signature
  or source grant.
- **Deeper competent-owner temporal semantics:** WG0P7 conservatively HOLDs any
  non-`ALL_TIME` epoch and any supersession chain. It does not interpret
  `effective_time_or_interval` under an owner-qualified clock. T7 is stopped by
  `NATIVE_SOURCE_DESCRIPTOR_NOT_OWNER_REGISTERED`, not by temporal semantics.
  This is a HOLD, not a reviewer grant.
- **Historical conflict:** the two unmodified characterisation assertions fail
  with `COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED`, exactly because they encode
  “silently ignore the forgery.” They are expected to fail under stronger
  early refusal and are not rewritten.
- **WG0N five unconstructible controls** (C3, D3, E1–E3) remain NOT GREEN; they
  fail at construction on nonexistent fields, not as repair regressions.

## 6. Non-grants

No original SAV/DTA/source35, no real external issuer, no independent
source-artifact revocation, no I05/Route B, no OC05/N11/N12/Sorok V3, no
canonical/accepted native-owner edit, no frozen-oracle edit, no semantic-issuer
adoption, no HQ method acceptance.
