# WG0P7 — immutable authority-body repair

Author continuation of WG0P4→P5→P6. **Not** an independent review, HQ
acceptance, or source/issuer decision. Answers the WG0O three REDs by binding
the constructed `AuthoritySnapshot.content_hash` body into the owner-registered
release material, binding the permitted operation to the owner-qualified release
tag, and HELD-ing unqualified epoch/supersession.

Repaired module `wg0p4_workload.py`: sha256
`89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`, blob
`62895078908ff748771da9a9fbcec6b36d34a803` (pristine WG0P6
`3807e46eec947694a1bd76afe23fd96183dd989b511584ec2ad3991ae943925e`).

## Deliverables

| path | meaning |
| --- | --- |
| `00_REAL_AUTHORITY_BODY_REPAIR.md` | defect, repair, courts, limits |
| `01_FULL_AUTHORITY_SNAPSHOT_PREIMAGE_AND_THREE_NEGATIVES.json` | full bound body preimage + A2/A3/A4 outcomes |
| `02_FROZEN_14_AND_ORIGINAL_NATIVE_POSITIVES.json` | 14-case raw outcomes, inherited counts, positive byte identity |
| `03_JUNIT_COLD_SOURCE_CUSTODY.md` | commands, JUnit, imports, cold, source custody |
| `04_WG0Q_INDEPENDENT_REVIEW_WAKE.md` | reviewer handoff, falsifiers, residual owner decisions |
| `candidate_change.patch` | exact 68-line productive diff |
| `tests/test_wg0p7_frozen14.py` | JUnit-grade 14-control regression |
| `repro/` | frozen WG0O oracle + unchanged adapter + reviewer transport + runners |
| `candidate/` | exact WG0P6 court runtime with the repaired module staged |
| `observations/junit/` | JUnit XML + stdout for every executed court |

## Reproduce

```sh
cd WORKER_RETURNS/PYAT-R29-WG0P7-AUTHORITY-BODY-ADAPTER-REPAIR-R1
WG0O_RUN=my_run python3 repro/run_frozen14.py
python3 -m pytest -q tests/test_wg0p7_frozen14.py --import-mode=importlib -p no:cacheprovider
python3 repro/capture_preimage.py
(cd candidate && python3 -B repro/run_court.py wg0m33 && python3 -B repro/run_court.py original65)
```

## Headline result on the frozen 14

A2 HELD, A3 REFUSED, A4 REFUSED — each 0 supported cells and 0 new I03 calls
(before repair: 42 cells / 4 I03 each). Eight other negatives stay typed; P1/P2/P3
serve 42 cells with consumer bytes identical. Mandatory 236 (33+3+80+55+65) green.

No original35, external issuer, artifact revocation, I05/Route B, OC05/N11/N12/V3,
method adoption or HQ acceptance is granted. WG0Q and HQ decide.
