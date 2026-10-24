# R91 R05 R8 admitted-original closure contract

Startup `65f7acf226b7b21a1a8f3be23f14a93b3f3cfbcc`; same OpenCode author.

## Sole defect correction

`TrustedNativeGraphCoordinator.execute` now treats the independently admitted slot
as the sole authority for the retained original/slot records. Request slots may
select an admitted slot id/base metadata but request-supplied actual associations
(M1 disposition, M2 release, B5/currentness, target arity/order, discovery,
recursive, E41, witnesses, actual owner objects) are ignored; original records are
built only from admitted slots. A request-forged learned association cannot
rewrite the fixed original.

## Preserved

Source/release/query/predicate/consumer/model base mismatch still refuses.
Actual admitted discovery/recursive/joint/E41 execution, learned association
checks, changed-evidence trusted refusal/restore, typed axes/Z16 and prior
positives are unchanged.

## Limits

Full live J42/P41/E04 NOT_REACHED; no new authority/registry/service. Other holds
unchanged. Author candidate only; distinct review follows.
