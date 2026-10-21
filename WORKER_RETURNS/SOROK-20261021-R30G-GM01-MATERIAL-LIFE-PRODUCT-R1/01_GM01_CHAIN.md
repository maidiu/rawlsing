# R30G GM01 material mechanism to actual C12/A0/A2

## Chain

```text
R29M GM01 TEST_ONLY resource (separate A/T proposal)
  -> B owner performed SHARE_TOOL or REFUSE_TOOL
  -> GM01 evaluate: objective material feasibility + A own E2/omission
  -> R29P StableJoinedProducer: real BP2 C8/E1/CAN008/CAN011/C9/E2 (separate TEST_ONLY target)
  -> GM01Product: material start overlay from GM01 feasibility
  -> A's real product material_inspect or omission
  -> BP4 C12 world event/episode/checkpoint
  -> R26E QualifiedC12Store / M6 / A0/A2
  -> cold subprocess reopen of the same SQLite DB
```

The GM01 material result is not converted into a CAN008 or CAN011 grant. The BP2 rule resources are separate R29M TEST_ONLY proposals with `grant=None`; the R29P C9 target is the existing separate TEST_ONLY target. GM01 only conditions material viability and A's own action.

## Exact source identities

```text
GM01 resource hash        = dc764df790a7e8aa70e80a1714d919c5c5259a44f968e08b4098aa7c139da488
GM01 positive result hash = 5622d5bec951e178414df40cb325470762edc142cabb0df8b655b44332641459
B SHARE_TOOL event        = TEST_ONLY_EVENT_share / 80b83a6ca59b7d20d26d3004e7bda91285f72a88c8ff04f433f71451ed364069
A E1 event                = TEST_ONLY_EVENT_e1 / bba6cbd41cdd6de7bc2c18c82264a136ff39968a408fa8e828bc40051d3ce027
A E2 performed event      = TEST_ONLY_EVENT_e2 / a21c4d6b16f997f5373506ad9fc5b75a135d0d3e3da3928ecc10f80ebb2ceeab
R29P BP2 C8 digest        = cd5a12fc5e1965cbba2a2ef65a6a7af62452226f0c276a061c1616366570ac38
R29P C9 target            = 972d1d439746d9b3c60bce0ee904d6a02d6d6a818a03caa8261ad9eec3b5a7f9
R29P consumed state       = 9ba15e262e7454edcb5ea38a81429f414668f61d1c9b72e59cccaa92443c1f0e
R29P E1 event hash        = 93a461e263cccd18f457ac7c7ba1ae5adafe9d9b4a3427f772fd932dbf4a49e7
R29P E2 receipt hash      = e1b6e03d646244ebb9a4a80b3f77beb32cf7354199cacc874f153079399732bb
```

## Material product result

Positive `share_e2`:

```text
A tools             1 -> 0
A material_remaining 4 -> 3
A completed_units   4 -> 5
A2 other units      4
A2 offscreen        MOVE, OFFSCREEN_NO_CHANGE
C12 counts          episode 4, world_event 4, checkpoint 4, perception 5
C12 verifier        R26E_QUALIFIED_C12_PREIMAGE, ok=true
```

`share_omit` leaves A tools 1, completed 4; B uses the tool offscreen, other units 5 and `OFFSCREEN_REPAIR`. `refuse_e2` leaves tools 0 and A action `DENY`/`GM01_NO_TOOL`; other units 4 and `OFFSCREEN_NO_CHANGE`. `refuse_omit` leaves tools 0, completed 4, other 4. `contrary_omit` retains `UNCERTAIN_CONTRADICTORY_PROJECTS` and the same no-action material result.

## Clock mapping

```text
GM01_TEST_ONLY_ACTIVITY_CLOCK: 1,5,6,9,10
BP2_TEST_ONLY_LOGICAL_CLOCK: event 242 / target commit 242 / E2 257
BP4_TEST_ONLY_WORLD_CLOCK: material start 10 / wait 40
```

Only the GM01 status and viability boolean are consumed; no GM01 time is compared numerically with BP2 or BP4. The declared process order is GM01 evaluate → BP2 C8/C9/E2 → product root → material start checkpoint → A material inspect → BP4 wait 40. `numeric_ordering_used=false`.

## Cold C12

`evidence/r30g_cold.json` reopens the same persisted database in a new Python process. It observes A tools 0, completed 5, material 3, B other 4, a DO episode with the GM01 receipt hash, and `ok=true` from the corrected C12 verifier.
