# OBL059 POSITIVE_APPLICABILITY — R5 GOVERNED BOUNDED COURT EVIDENCE

Status: `PASS__GREEN_GOVERNED_COURT`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r5`

Exact worker start:
`a728990458a4a909186b99520df6bb1cc9a826f1`

Prospective campaign instruction/adjudication:
`1c0f767126cc479c31ddcdc521fa64fa26efbe4f`

Frozen R5 candidate:
`9f7e965fbba64ce94239e36f011f7936681b605a`

Candidate executable blob:
`04cb331af0d7e0d4d14db901ecf79eb0d736bfe3`

Governed court blob:
`78dd9af625783bb906a1e606b6df35450a9d8f16`

Corrected pytest wrapper blob:
`05d451943e33e8eb0143696553dfce1b04545f87`

Court spec blob:
`06261e2d66faa880f768a291e59237dfdd4647dc`

Corrected governed evidence execution:
`2be8ec089c103fad61710387678c7a09e9d72652`

## Repair regressions

The governed R5 court directly verifies:

- `10 ** 5000` at each of the five required bindings returns deterministic `NOT_DIRECTLY_APPLICABLE` with exact `MALFORMED_BINDING:<field>` reason;
- the same for `-(10 ** 5000)`;
- exact integer classification immediately around the runtime decimal conversion ceiling, using integer arithmetic only;
- magnitudes materially larger than the reproduced case;
- nested oversized integers inside exact built-in containers;
- deterministic repeated receipts and proof hashes;
- structural distinction between different oversized integer values through bounded binary-magnitude diagnostics;
- zero, small, and ordinary exact integers preserve exact frozen R4 behavior;
- oversized malformed integers never become valid identifier strings;
- ordinary JSON-safe positive/negative controls remain exactly frozen-R4 behavior;
- inherited custom-object, cycle/depth, bytes/set/frozenset, scope, authority, evidence, no-current-effect, and programmer-error preservation controls.

The R5 projection uses the runtime's current `sys.get_int_max_str_digits()` value only as a read-only ceiling. It does not mutate the process-global setting. Safety classification compares exact integers to `10 ** limit` without decimal conversion. Oversized diagnostic projection records sign, bit length, and SHA-256 of exact binary magnitude instead of decimal text.

## Governed runs

### Initial execution-routing run

Evidence execution:
`48b8b8a3029e37567ee4aa0f277d80aa64e30143`

Run/job:
`34242106442` / `102114628677`

Result:
`failure`

Protocol:
`20 passed`

Court:
`1 failed, 67 passed, 259 subtests passed`

The sole failure was an inherited R3 programmer-error preservation test wired to a different loaded module instance than the one R5 actually delegates through. This was a court-routing defect only. The frozen R5 candidate was not changed.

Artifact:
`10062407899`

Artifact ZIP SHA-256:
`e4dea7cbb8d88b90678bee7148c62891d16e82ce7c0e3b0cd9c0913f0ad272cd`

### Corrected governed run

Corrected evidence execution:
`2be8ec089c103fad61710387678c7a09e9d72652`

Run/job:
`34242233223` / `102115059316`

Result:
`success`

Protocol:
`20 passed in 0.07s`

Bounded court:
`68 passed, 259 subtests passed in 0.18s`

Artifact:
`10062460385`

Artifact ZIP SHA-256:
`1ea926c7e9310b64a503e3b09867c7be18a3b8720257088270b709933888a7c7`

Execution-only PR:
`#291`

PR state:
`CLOSED__UNMERGED`

## Separation and effects

`INDEPENDENT_REVIEW_PERFORMED_BY_R5_REPAIR_WORKER = NO`

`PROJECT_CURRENT_STATE_CREATED = NO`

`ACTOR_CREATED_OR_ACTIVATED = NO`

`ADP008_PHASE_TRANSITION_EXECUTED = NO`

`ADP019_OCCURRENCE_ADMITTED = NO`

`CURRENT_POSITIVE_OBL056_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`OEE_REALIZED = NO`

`OBL058_OR_OBL060_OWNERSHIP_ASSUMED = NO`

`SUB_VOZHD_E_OR_HQ_ADOPTION_CLAIMED = NO`

Court terminal:

`PASS__OBL059_R5_BOUNDED_REPAIR_GOVERNED_COURT_GREEN__NO_SELF_REVIEW`
