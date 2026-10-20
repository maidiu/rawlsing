"""BP1 sourcefree historical actor production package.

This package is an executable historical actor composer at explicitly
SOURCEFREE / TEST_ONLY grade. It is NOT native ADP007 actor genesis, not a
competent developmental-rule issuer, and not a person or genealogy authority.
"""
from .source import (
    BP1_ACTOR_SOURCE_GRADE,
    BP1_ACTOR_SOURCE_SCHEMA,
    BP1_NATIVE_GRANT,
    ActorSource,
    SourceRefusal,
    issue_actor_source,
    reseal_with_changed_source_ref,
    verify_actor_source,
)
from .ledger import (
    ActorLedger,
    LedgerEvent,
    LedgerRefusal,
    make_objective_event,
    verify_snapshot,
)
from .composer import (
    TwoActorLife,
    build_no_change_life,
    build_denied_life,
    build_two_actor_life,
    future_child_findings,
)
from .c9_bridge import (
    BP1C9Result,
    build_c9_actor_record,
    build_c9_conditioning,
    build_c9_event,
    run_bp1_c9,
)

__all__ = [
    "BP1_ACTOR_SOURCE_GRADE",
    "BP1_ACTOR_SOURCE_SCHEMA",
    "BP1_NATIVE_GRANT",
    "ActorLedger",
    "ActorSource",
    "BP1C9Result",
    "LedgerEvent",
    "LedgerRefusal",
    "SourceRefusal",
    "TwoActorLife",
    "build_c9_actor_record",
    "build_c9_conditioning",
    "build_c9_event",
    "build_denied_life",
    "build_no_change_life",
    "build_two_actor_life",
    "future_child_findings",
    "issue_actor_source",
    "reseal_with_changed_source_ref",
    "make_objective_event",
    "run_bp1_c9",
    "verify_actor_source",
    "verify_snapshot",
]
