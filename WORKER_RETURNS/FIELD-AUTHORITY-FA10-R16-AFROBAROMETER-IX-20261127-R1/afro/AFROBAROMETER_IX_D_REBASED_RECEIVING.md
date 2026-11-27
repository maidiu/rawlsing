# Afrobarometer IX — D-arm repaired lineage receipt

**Scope:** Afrobarometer Round 9 only. No WVS7 work was performed in this continuation.

## D/C exact-source repair

- Sealed packet SHA-256: `42a7b865af1069f116ab2c1bc6a4ef669941b85fc687b0587d13c49d5d3ab8a4`.
- The first literal-evidence repair received `CORRECTION_REQUIRED` for CQ97; its other dispositions were eight `PASS` and four `HOLD`.
- A focused CQ97 repair was run in OpenCode DeepSeek session `ses_de12d810fffeyIGdkpGcfFSiKf`; its independent source-bound re-review returned `PASS` in session `ses_de12d0867ffezu5yHlJk0VZ8Az`.
- The integrated candidate replaces CQ106C, CQ106E, CQ109F, CQ28, CQ48A, CQ50B, CQ51A, CQ63B, and Q97; it holds CQ29B, CQ48B, CQ51B, and CQ98A. The prior D/C response is preserved byte-for-byte in `core/D/C/repair-literal-evidence-integrated-20261127/original_response.json`.
- Incumbent `frozen/fa10.py validate()` passed. The stage remains `STRUCTURE_ONLY`; this is not scientific acceptance or source/native authority.

## Downstream lineage

Changing D/C changed the prior-response hash bound into D/R, D/I, and D/S. The prior sequence was preserved under `core/`; a separate Afro-only lineage was created under `afro-D-repaired/core/D/`. D/R, D/I, and D/S were regenerated sequentially against the repaired ancestry. Each passed incumbent structural validation. The D-arm projection at `afro-D-repaired/core/D/projection.json` is `STRUCTURALLY_VALID_NOT_SEMANTICALLY_ADJUDICATED`, with 14 item holds.

This does not close the full factorial: author products and structural projections do not provide independent semantic/scientific acceptance, and no full factorial winner or quality-adjusted economy verdict is asserted. Existing frozen source assets and prior trial records remain preserved.


## Second scoped receiving correction — addressee and threat/candor wording

An independent exact-branch review identified overstatement in the interviewer addressee and felt-versus-physical-threat language. A targeted Afro-only worker repair was independently received `PASS_SCOPED` for D/C, D/R, D/I, and D/S. The update keeps the literal addressee ambiguous, distinguishes the separately worded/coded threat items without asserting a relationship, and states that Q109F's supplied metadata lists three labels but no special response codes, leaving missing handling undetermined. The D/I `INTHREAT` and D/S `STHREAT` inquiries remain explicit holds pending interviewer/administration attribution and interview-level linkage.

The exact received patch is integrated in a fresh ancestry-bound branch at `afro-D-repaired-v2/core/`. Each stage passed incumbent structural validation and the D projection remains `STRUCTURALLY_VALID_NOT_SEMANTICALLY_ADJUDICATED` with 14 item holds and 6 projected candidate inquiries. The earlier v1 and original frozen records remain preserved. This is not scientific, native, or full-factorial acceptance.
