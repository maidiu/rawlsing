# T9S — Phase A test-authoring corrections (transparency note)

Two authoring bugs in the Phase A preregistered test file were discovered and
corrected in Phase B, without changing any frozen oracle expectation:

1. `test_F1_unused_future_wave_cannot_upgrade_held_product_authority` read
   `.value` off the `OpportunitySet` returned by `read_selected_world` (that
   object has no `.value`; the numeric value lives on the `TemporalValue` from
   `evaluate`). Corrected to read the numeric value via `evaluate(...).value`
   while asserting the SAME frozen expectations (value 0.20, basis `("W0",)`,
   key not AUTHORIZED, no open route, `W1` only in archive context). In Phase A
   this case's recorded failure was that AttributeError, not the underlying RED;
   the underlying RED was nonetheless physically reproduced in
   `observations/phase_a_reproduced_reds.json` via direct adapter calls.
2. `case()` passed `target_year=1995` positionally and also accepted `target_year`
   via `**kw`, so `test_F5_archive_known_at_2020...` raised a duplicate-keyword
   TypeError. Corrected `case()` to forward `**kw` only.

The frozen oracle `01_T9S_PRECOMMITTED_PERMISSION_ORACLE.json` is unchanged. The
corrections only make the tests actually exercise the assertions they always
stated. This note is committed for full transparency to the independent reviewer.
