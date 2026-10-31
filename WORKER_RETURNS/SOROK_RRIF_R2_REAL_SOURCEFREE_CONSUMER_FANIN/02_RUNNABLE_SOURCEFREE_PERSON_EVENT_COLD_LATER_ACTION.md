# Runnable sourcefree person/event/cold/later-action proof

## Candidate

`SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2/`

The candidate is a bounded sourcefree closure copied from JOIN-E
`7bf2da302996491ddf34b9a039fea47ac982d135` (444 vendored files + 10 `joined`
modules). It is not native, not a PRE-MAIN import, and not a Programma graph.
No source code in the vendored closure was edited; test-only repository-root
resolution and one focused C12 test were added.

## Positive path: material event -> later help -> cold return

```sh
C="$PWD/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
PYTHONPATH="$C:$PWD" python3 -m joined.cli start --state "$D/encounter" --perform omit
PYTHONPATH="$C:$PWD" python3 -m joined.cli help --state "$D/encounter"
PYTHONPATH="$C:$PWD" python3 -m joined.cli wait --state "$D/encounter" --hours 30
PYTHONPATH="$C:$PWD" python3 -m joined.cli return --state "$D/encounter"
PYTHONPATH="$C:$PWD" python3 -m joined.cli verify --state "$D/encounter"
```

Observed key values:

| Step | Actual result |
|---|---|
| start | `STARTED`; `material_performance=omit`; `b_operation=SHARE_TOOL`; `b_performed=true`; target `229322ed...` |
| start source | A E1 `dac4aeb0...`; B event `16f11d2e...`; `material_feasible_after=true`; `native=false` |
| help | `accepted=true`; `strategy=HELP_ACCEPT`; speech event `TEST_ONLY_BP4_WORLD_EVT_99f411...`; `native=false` |
| help surface | `A material repair is performed in the workshop.` + `"Hold the near edge. I'll check the seam."` |
| wait(30) | `clock=40`; `scene_open=false`; surface: `"The seam held. I need to get it to the market."` |
| return (cold process) | `status=OK`; `strategy=RETURN`; `scene_open=true`; surface: `"The seam held. You came back."` |
| verify | `session_ok=true`; root `C12` verifier `R26E_QUALIFIED_C12_PREIMAGE`; counts episode 2, world_event 1, perception 2, checkpoint 4; import closure `ok=true`; manifest `ok=true` |

The positive actor surface is a real read of persisted C12 state and the E
expression admission, not a hand-written transcript. It is still sourcefree:
`native=false`, `LIVE_ACTOR_MODEL_NOT_RUN`, no model/provider call.

## E2-conditioned later action and matched refusal

```sh
PYTHONPATH="$C:$PWD" python3 -m joined.cli start --state "$D/e2" --perform e2
PYTHONPATH="$C:$PWD" python3 -m joined.cli help --state "$D/e2"
```

Observed:

```json
{
  "start_material_performance": "e2",
  "source_b_operation": "SHARE_TOOL",
  "source_b_performed": true,
  "help_accepted": false,
  "strategy": "HELP_REFUSE",
  "surface": [
    "the repair worker says: \"The tool's gone. I can't do it today.\" A looks at the empty tool space."
  ]
}
```

The `e2` condition consumed the tool before the later help; the `omit` condition
retained it and admitted `HELP_ACCEPT`. This is the performed-change versus
opportunity-only contrast, not a claim of native E2.

## Targetless / NO_CHANGE condition

```python
from pathlib import Path
from joined.refusal import RefusalSession
from joined.session import JoinedSession

s = RefusalSession.start(root / "refusal")
h = s.do_help()
print(s.status()["targetless"], s.meta["target_id"], h["accepted"], h["strategy"])
```

Observed:

```text
targetless=True
target_id=""
help_accepted=False
strategy=HELP_REFUSE
verify=True
```

`JoinedSession.probe_refusal` returned:

```text
status=HOLD
code=JOIN_REFUSAL_NO_TARGET__OWNER_CONTRACT_REQUIRED
source.b_operation=REFUSE_TOOL
target_id=""
c9.target_branch=NO_CHANGE
c9.target_reason=NO_PROPOSAL
c9.response_status=RESPONSE_EFFECTS_VALID_EMPTY
c9.material_reason=NO_ELIGIBLE_MATERIAL_SOURCE
```

No C9 target, no fabricated E2 and no learned practice were created on this
path. This is the lawful targetless/NO_CHANGE boundary.

## Cold and fork reality

The actual tests cover:

- `test_full_encounter_positive_and_cold_reentry`: cold reopen, return session,
  `verify` after cold.
- `test_cold_reopen_is_nonmutating_and_fork_diverges`: product hashes unchanged
  on open; `fork_alt("alt")`; root remains equal; branch episodes diverge.
- `test_nested_forks_receipts_parent_isolation_and_tamper`: nested forks and
  tampered lineage refusal.
- `test_c9_target_consumer_severance_cold_red_restore`: mutate C9 target ->
  cold positive RED -> exact restore -> GREEN.
- `test_coordinated_sidecar_and_meta_source_substitution_rejected`: coordinated
  B source identity substitution -> `J_PROVENANCE_MISMATCH`.
- `test_b_source_edge_help_observable_and_targetless_no_target`: share/refuse
  behavior and targetless no-target.

## Honest limit

The product is an actual sourcefree consumer, not a native person, not an
actual external language-model renderer, and not a human participant. The
`actor_model` field is `LIVE_ACTOR_MODEL_NOT_RUN`. No provider or model call is
made.
