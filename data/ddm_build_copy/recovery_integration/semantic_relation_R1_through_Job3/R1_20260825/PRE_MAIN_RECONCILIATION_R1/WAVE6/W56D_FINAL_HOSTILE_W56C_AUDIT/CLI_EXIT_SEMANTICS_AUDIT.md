# CLI EXIT SEMANTICS AUDIT

Static code proof:

`adoptive_requested = effect in ADOPTIVE_EFFECTS`.

The process returns success only as:

- adoptive request: `ADOPTION_ELIGIBLE == true`;
- nonadoptive request: `PACKET_VALID == true`.

Thus a structurally valid adoptive packet with `ADOPTION_ELIGIBLE=false` exits nonzero. `PROJECT_CLOSURE_AT_GRAIN` is an adoptive effect, so failed closure eligibility cannot be laundered into successful process status through structural packet validity. Lawful `FORENSIC_RETURN`, `EXPLORATORY_RETURN`, and `BOUNDED_EXECUTION_RETURN` may succeed as nonadoptive structural returns while adoption remains false.

Classification: `CLI_FAIL_CLOSED`.