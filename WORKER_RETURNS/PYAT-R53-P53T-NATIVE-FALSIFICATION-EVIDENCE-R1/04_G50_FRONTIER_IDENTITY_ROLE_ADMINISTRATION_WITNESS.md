# G50 — FRONTIER IDENTITY, ROLE, ADMINISTRATION WITNESS

**Source:** commit `d379bafe36b8d89da27ea5bf33614d33aca7f2d2`
**Modules:** `g50/enumerate.py` blob `f610ef2dea39519a51a5b57fd35bbe245fb9dc9b`; `g50/types.py` blob `a376edad00a3b40f69fc3a87c83658b4406bc67b`; `g50/fixture.py` blob `41b6191cdd62a387800fd76f36ceb6b6f5a2fdcf`.
**Execution:** actual unchanged G50 module in-process with sourcefree synthetic `SourceDecisionBundle` and `ScientificGrammarPolicy`. No B49, C11, I03, I05, U43, or Batch execution. This is a G50-module-boundary reproduction, not proof that a full native engine run behaves identically.

Command:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -m pytest WORKER_RETURNS/PYAT-R53-P53T-NATIVE-FALSIFICATION-EVIDENCE-R1/tests/test_g50_frontier.py -q
```

Result: 7 passed. Tests pass when they observe the vulnerable current behavior and its positive controls.

## Positive control — stock fixture

`enumerate_frontier(stock_bundle(), stock_policy())` succeeds:

- `e_pre_count = 432`
- dispositions: `ELIGIBLE 432`, `PROHIBITED 248`, `DEFERRED 4`, `INAPPLICABLE_PROVED 1`, `UNRESOLVED_SCIENCE 3`, `UNSUPPORTED_RUNTIME 3`
- eligible classes: `JOINT 132`, `CO_TRAVEL 132`, `INTERACTION 96`, `CONDITIONAL 42`, `FORK 24`, `DIST 4`, `STATE_ROBUSTNESS 2`

This is the normal baseline, not a source or original35 claim.

## Arbitrary item IDs

Input: complete bundle with only `Qa`, `Qb`, `Qy`, `Qm`, each target and conditioner eligible, same domains/units/forms; policy target and conditioner roles rewritten to those IDs; `denied_roles=()`.

Observed unchanged exception:

```
KeyError: 'ID'
  enumerate.py:151 in add
      unit=items[targets[0]].unit if targets else "adult"
  enumerate.py:193 in enumerate_frontier
      add("DIST", ("ID",))
```

The `role_disposition()` call already returned `PROHIBITED` for missing `ID`, but `add()` dereferences `items[targets[0]].unit` before/without respecting that disposition. The entire finite frontier is lost.

With `ID` present but `Y` absent, the next literal raises `KeyError('Y')` at line 151 from line 194. This shows the failure is a ledger of hardcoded literals, not a single accidental `ID` lookup.

Padded control: stock reserved items `ID/H/RT/X1/X2/SET/RANK/REP` plus renamed `Qa/Qb/Qy` enumerates successfully and produces eligible Q operations. The main grammar is name-generic; padding only masks the literal ledger. It is not a repair.

## D8 — unadministered item remains eligible

Input: stock bundle with `Y.administered=False`; everything else unchanged.

Observed:

- `DIST(Y)` sample remains `ELIGIBLE`, unit `adult`.
- `e_pre_count = 432`, identical to the administered stock control.
- `role_disposition()` and the target/conditioner pools never inspect `administered`.

All-missing-but-administered control: `Y.administered=True` with `state_map={"Y":"MISSING"}` and `held=("Y_ALL_RESPONSES_MISSING",)` remains eligible and also yields `e_pre_count=432`. G50 has no outcome/missingness input and does not distinguish missingness from unadministration at this boundary. This does not say a real source may treat an administered all-missing item as measured; it says G50 cannot express the distinction.

Positive role control: setting `Y.target_role=False` removes sample `DIST(Y)` and leaves the Y population declaration prohibited under `TARGET_ROLE_DENIED`. The role gate exists; the administration gate does not.

## D10 — duplicate item identity silently collapses

Input: stock bundle plus a second `ItemOccurrence` with the same `item_id="Y"`, unit `household`, forms `G`, otherwise valid.

Observed:

- No duplicate refusal.
- `DIST(Y)` sample selects the last occurrence and reports unit `household`.
- Eligible count collapses from `432` to `114` (318 eligible operations disappear because the last Y no longer links to the adult unit).
- `u_item_root` is recomputed from both bundle items and differs from the control root, while the frontier operations use only the last one.

The `items = {item.item_id: item for item in bundle.items}` construction (`enumerate.py:106`) silently overwrites. `u_item_root` hashes `bundle.items` (`enumerate.py:228-246`), so the identity root includes an occurrence the frontier does not represent. This is a stronger actual effect than the static "last record only" description.

## D9 — Y versus Z lexical direction asymmetry

Input: stock bundle plus an identical `Z` occurrence; policy target and conditioner roles include both Y and Z; same domains and semantics.

Observed:

- `CONDITIONAL(A | Y=1)` is `PROHIBITED` with reason `REVERSE_ROLE_RISK_NOT_AUTHORIZED`.
- `CONDITIONAL(A | Z=1)` is `ELIGIBLE` with no reasons.
- `role_disposition()` returns the same asymmetry directly.
- `ScientificGrammarPolicy.__dataclass_fields__` has no `reverse_authorized`; the policy instance has no such attribute. The code's `getattr(policy, "reverse_authorized", False)` can only ever be false for a standard policy.

Consequence: scientific direction is keyed to the literal item name `Y`, not to a source-defined direction decision. This is not a claim that reverse causation should be permitted; it is a claim that the policy cannot explicitly permit or deny it by source identity.

## Downstream state and limits

- All cases stop at the prospective G50 frontier or its typed operations. No I05 fact, E04 receipt, original U/E_pre, or source permission is produced.
- The G50 `native_map.py` literal dependence was not separately executed; the explicit `enumerate.py` literals are sufficient to explain the observed arbitrary-ID failure.
- The full B49→G50→U43 native joined producer was not run; that limitation is recorded in 00 and 07.
- No repair patch, no production edit, no new schema, no scientific issuance.
