# R61-R03V R4 independent review — RESUME / stop

## Disposition

**REVISE.** One bounded successor review is complete. Fixed-original-pin cold
restore works for genuine results and refuses all three prior coordinated
fact/job faults; the remaining gap is live checkpoint capture, which does not
run the shared structural/closure/multiplicity validation before returning a
pin. No candidate repair, self-adoption, production merge, new worker or
downstream wake occurred.

## Established

- First-tool preflight passed at the exact R4 branch/HEAD.
- R4 EXPECTATIONS were frozen and committed before candidate code inspection.
- Author R4 suite: 15 passed; retained R01 suite: 32 passed.
- Reviewer fixed-pin probes: 3 passed, 2 capture-boundary failures.
- Genuine original-pin restore, missing/wrong pin refusal, the three prior
  fact/job substitutions with recomputed hashes, and content mutation retaining
  advertised refs all behave correctly against the genuine pin.
- U43 exact, four-path scope, owners unchanged, governed/D3/minority/pending/
  source-value/HELD/UNKNOWN positives retained.

## Remaining failure

`freeze_restore_checkpoint()` checks only anti-join flags and nonempty refs. An
incomplete result with empty operation ledger, or duplicated fact refs, still
acquires a checkpoint. Required: run the shared structural/closure/
expected-mapping/multiplicity validator (or equivalent pin-free helper) before
returning the checkpoint.

## Not reached

Sourcefree TEST_ONLY trusted-host only; no source respondent access. Both pin
and candidate replaced by a different trusted host is R61AF excluded. R04 joined
custody/durability, R05 lifecycle/grades, F5-F8 global, original35/1890 N11,
N12/Sorok, protected CI/production and J52/W52 remain NOT_REACHED.

## Preservation

R1/R2/R3 and historical evidence remain unchanged. The reviewer wrote only the
R4 own root. No new session, subagent, provider/model/account switch, force push
or candidate edit was used.
