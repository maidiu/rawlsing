# C02F — Real Concrete Fixture and Callers

## Fix vs C02E
C02E fixture attempted `B5.LearnedProductLifecycleSubject.from_protocol(TestLearnedProductReleaseProtocol(...))` — instantiating a `runtime_checkable` Protocol. Python 3.11 refuses: "Protocols cannot be instantiated".

C02F constructs `B5.LearnedProductLifecycleSubject(...)` DIRECTLY (concrete frozen dataclass, 15 required + 3 optional keyword fields). No abstract type is ever instantiated.

## Caller graph (from c02f_bypass_court.py)
- `build_m2(repo, tag, producer_credential=None)` — genuine M2 release via accepted `register_producer_subject` + `constitute_release`
- `b5_subject_from_m2(repo, release, subject)` — builds B5 subject directly from M2 output (K4 bypass construction)
- `direct_executor_publish(subject)` — raw B5 executor, no perimeter (K4 bypass)
- `custody_for(repo, release, subject, slot, ceiling, ...)` — owner custody with complete expected_identity
- `expected_identity(repo, release, subject, ceiling_key, replay_grade)` — closed 21-key expected identity from real M2 output

## Factories used
- `M2.register_producer_subject` — accepted M2 owner
- `M2.constitute_closure` / `M2.constitute_release` — accepted M2 owner
- `B5.LearnedProductLifecycleExecutor` — accepted B5 owner (direct construction, no Protocol)
- `B5.LearnedProductLifecycleSubject` — concrete frozen dataclass (direct construction)
- `C02.AuthenticatedB5Ingress` — C02 candidate perimeter
