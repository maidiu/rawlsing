# C2R — adversarial negative evidence and executable limitations

**Inspected source cut:** `45f327a9086b4c95d0807da0774742b9ed8a626a`. The host here supplied authenticated private GitHub read/write, not an independently authorized local Rawlsing Git checkout/runner. **All probes below are S1 in-memory mutations of retrieved Markdown and manifest processed by independent JavaScript checking logic, not executions of `verify_three_frontdoors.py`.** Do not promote them to S2 or native proof.

| Mutation introduced into an in-memory copy | Observed S1 rejection | Intended Python validator criterion |
|---|---|---|
| Remove untagged Pyat first-qualification section heading/body while preserving tagged C1 IDs | EXPECTED_FAIL — deleted required untagged heading | `required_untagged_sections` exact body/heading mismatch |
| Remove Pyat `HQ-C2R-031` local 00D passport tag | EXPECTED_FAIL — Pyat tag no-drop | expected local ID missing; warm/passport mandatory |
| Remove ENGINEERING `OWNER_OF_DECISION` from Sorok shared court | EXPECTED_FAIL — ENGINEERING missing field | three distinct 5-field category blocks; all 15 nonempty |
| Drift Sorok's common 029 clause while leaving Pyat/PRE unchanged | EXPECTED_FAIL — shared text mismatch | exact shared `source SHA + body` parity |
| Substitute a different selected governing source blob identity | EXPECTED_FAIL — `REVALIDATION_REQUIRED` | compare original pinned immutable Git blob with separately selected current protected HEAD |

**Positive S1 readback:** all three entries have expected distinct tags (32 total IDs across the manifest), 20 exact shared bodies, local Pyat/Sorok recovered 00D IDs, 8 frozen untagged sections, explicit M5 locator fields, and no “already existing accepted” G4 description. Git compare from C2 startup to source commit reported exactly five allowed changed files; branch source blobs are listed in 00.

**Not executed:** Python compilation and `python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py --pinned-only`; its `--authoritative-ref` mode; its `--commission` prompt checks; controlled local mutation tests; mainMac/Git source authority HEAD check; GitHub CI/pytest. These remain **S2 NOT_RUN**, not guessed PASS.

**Qualified future test instructions** (on independently authorized isolated full checkout; do not mutate protected source):
```sh
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py --pinned-only
# A STATIC PASS must explicitly say LIVE_AUTHORITATIVE_HEAD NOT_VERIFIED.
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py
# Without chosen current authority, exit 2: REVALIDATION_REQUIRED.
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py --authoritative-ref <owner-verified-protected-ref>
# PASS only if all 15 original-law blobs match; changed selected law → exit 2.
python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py --commission <one-complete-copy-paste-prompt.txt> --pinned-only
# Drop any per-court field → FAIL; keep evidence grades and model/host unknowns.
```
Original source/version comparison requires qualified local Git objects and a separately owner-verified authoritative remote HEAD. The branch's own candidate HEAD must never be misdeclared as that selected protected HEAD.