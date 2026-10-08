# ASTRA HQ247 — evidence ledger (append only during audit)

Initial issuance observations (not conclusions of Astra's independent audit):

| ID | Observation | Exact evidence | Grade | HQ action |
|---|---|---|---|---|
| SETUP-001 | Control latest checkpoint is HQ247 at pinned handoff commit | control HEAD `4246cea7657b6bfb1e405a27f3dff952c4d157df`, pointer blob `f30c5e803191affb294f0bdcea3b8b843d2eb4a8` | control read | none |
| SETUP-002 | F7 R2 worker pushed partial repair, claims B1–B4/P1 fixed; leak and T1 remain | `c2c0ab7335a3bcfeabb4297139378e3e657cd432`, `WORKER_RETURNS/PYAT-HQ247-F7-NATIVE-B1-B4-PARITY-TRUST-REPAIR-R2/06_FINAL_DISPOSITION.json` | author return, NOT independent R2 review | HQ intake pending |
| SETUP-003 | Frozen f09 independent reviewer still blocks f09, not later R2 | `fa3c69b832d4649e046d84e4dde89897585aa4e3`, `WORKER_RETURNS/PYAT-HQ247-F7-F09-REPAIR-INDEPENDENT-RUNTIME-REVIEW-R1/05_FINAL_DISPOSITION.json` | independent Mac reviewer claim scoped only to f09 | HQ intake pending |
| SETUP-004 | N10E C1 issuer/root-placement competence not yet provisioned | `80023846b13b9d2cea93f6a3d4f7cd36601b7ccd`, `WORKER_RETURNS/PYAT-HQ247-N10E-AT07-OWNER-ROOT-PLACEMENT-PREFLIGHT-R1/FINAL_DISPOSITION.json` | documentary return, NOT root | HQ intake pending |
| SETUP-005 | Full F1–F8 PRE-V3 functional realization not established by prior Astra Atlas or HQD125/216 | `PYAT_CONTROL_ROOM/25_HQD125_DDM_FUNCTIONAL_CONSERVATION_CROSSWALK.md`, `26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md` | binding law and prior summary, not new proof | audit mandate |

## New evidence entry format

`[ID] [date/phase] claim | exact commit/blob/path(+line/test) | [DIRECT_BLOB / EXECUTED / INHERITED_PROOF / RETURN_UNADOPTED / PROPOSAL / INFERENCE / UNKNOWN] | challenger/counterevidence | effect on F1–F8 / critical path | falsifier | disposition`

No vague "passed" without named test, execution environment and exact candidate. No inheritance of reviewer independence between different candidate SHA values.
