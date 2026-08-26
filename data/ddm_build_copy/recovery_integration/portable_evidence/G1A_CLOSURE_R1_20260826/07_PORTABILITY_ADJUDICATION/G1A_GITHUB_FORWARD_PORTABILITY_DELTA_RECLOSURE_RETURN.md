# G1A GitHub Forward-Portability Delta Reclosure Return

Status: `BOUNDED_DELTA_ADJUDICATION_COMPLETE__G1A_NOT_CLOSED`

This is a successor delta to the original Agent C portability court return. It does not rewrite that return: at its own evidence state, the original court correctly recorded one forward blocker and a blocked forward theorem.

## Pinned inputs

- Prior Agent C head: `ce8062eebcc02ed013007bccee64e57331962ccd`
- Supplemental Agent B head adjudicated: `aece04ac3fa2e488c6993c6b9c88eda296b2e6b8`
- Supplemental Agent B parent: `ea4d76557343e6eb72394d1c559020c63a551731`
- Coordination ref re-observed: `agent/vozhd-to-vozhdy-inheritance-integration-r1` at `f805c6a0f79f00f66e1ecd7949a8bf05f707249c`

The supplemental B commit has exactly seven added paths: the two distinct register objects and five recovery/provenance/validation artifacts under `03_C3_REGISTER_LINEAGE/`. No unrelated forward input was introduced by the delta.

## Independent Git-object verification

The following checks were performed directly on Git objects at the supplemental B head, not from the narrative report alone.

| Object | Git path | Observed SHA-256 | Observed bytes | Data rows | Columns | Result |
|---|---|---|---:|---:|---:|---|
| Register A | `03_C3_REGISTER_LINEAGE/REGISTER_A/question_structure_register.csv` | `f47c8adb65546b1c0a06dcd31dc0b827b59f8975a3806646f41a0742966c3d84` | 23,612,534 | 18,792 | 62 | `PRESENT_EXACT` |
| Register B | `03_C3_REGISTER_LINEAGE/REGISTER_B/question_structure_register.csv` | `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b` | 26,582,348 | 18,792 | 69 | `PRESENT_EXACT` |

For each object, SHA-256 was recomputed from the actual Git blob bytes; byte count was independently counted; CSV parsing succeeded; and every data row had the stated header width. The 18,792-row count excludes the CSV header, matching the commanded HARVEST-001 convention.

The two installed blobs have separate Git object identities and separate paths. They are not derived projections, rebuilt outputs, or name-only matches.

## Provenance and substitution check

The supplemental recovery TSV records actual observed hashes and source locations, while `99_PROVENANCE/SOURCE_PROVENANCE.tsv` separately identifies each loose historical source, its historical timestamp, byte size, SHA-256, target Git path, and `EXACT_ORIGINAL_LOOSE_FILE` representation. `99_PROVENANCE/SHA256SUMS.txt` independently binds each installed path to its exact SHA-256. The validation JSON records both mechanical results and `no_builder_executed = true`.

Register C, SHA-256 `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219`, is recorded as `NOT_USED_NOT_INSTALLED`. It is not present at either A or B installed path and was not substituted for a required object.

## Delta disposition

`PRIOR_FORWARD_RESIDUAL_BLOCKERS = 1`

The prior blocker was the absence of exact Register A and Register B bytes required to continue the C3 residual court. That condition is now closed. The prior reference to the bounded 92-row / 879-transition material describes work to be performed by the residual court from its recovered inputs; it is not a newly required pre-existing Git carrier. The supplemental commit exposes no new forward-only prerequisite.

`FORWARD_RESIDUAL_BLOCKERS = 0`

The result is limited to evidence portability. It does not adjudicate C3 succession, turn a register into current authority, accept or bank any child return, close G1A, authorize P10/P9, or establish full historical reexecution portability. The independent historical theorem remains unmodified by this delta; in particular, the original C1 historical blockers are not reopened here.

Therefore:

`G1A_GITHUB_FORWARD_CONTINUATION_PORTABILITY_COMPLETE`

G1A_GITHUB_FORWARD_PORTABILITY_DELTA_RECLOSURE_COMPLETE__RETURN_TO_HQ__NO_G1A_CLOSURE_NO_LIVE_MUTATION
