"""BP2 joined actor/event/rule/performed-action source-free producer.

Public surface:

* ``bootstrap``      exact staged source closure + import path + verification
* ``binding``        BP1 occurrence -> BP3 C8 commit -> OUT9 read binding
* ``ports``          native-ready ADP010/ADP019/CAN008/CAN011/E2 receiving ports
* ``producer``       the whole joined chain, stage by stage
* ``severance``      six same-assertion source-edge cuts and restoration
* ``scientific``     the finite PS0-D01-based rule/ADP decision request

This package does not issue native authority. Every TEST_ONLY resource it binds
is explicitly declared as such and production registries remain empty.
"""
from __future__ import annotations

from . import binding, bootstrap, ports, producer, scientific, severance  # noqa: F401
from .bootstrap import SourceClosureDrift, install, verify_sources  # noqa: F401
from .binding import (  # noqa: F401
    BindingRefusal,
    C8Commit,
    Out9Binding,
    WorldOccurrence,
    build_world_occurrence,
    commit_world_occurrence,
    read_out9,
    validate_occurrence_payload,
    verify_out9_against_source,
)
from .ports import (  # noqa: F401
    ADP010EncounterPort,
    ADP019EventPort,
    CAN008RulePort,
    CAN011TargetPort,
    Currentness,
    E1Binding,
    E2OwnerPort,
    PortRefusal,
    Resource,
    production_registries,
)
from .producer import (  # noqa: F401
    JoinedOutcome,
    JoinedProducer,
    JoinedRefusal,
    SEVER_CODES,
    joined_consumer_assertion,
    prepare_journal_env,
)
from .severance import (  # noqa: F401
    SEVERANCE_EDGES,
    SeveranceTrial,
    run_all_severances,
    run_severance,
)
from .scientific import (  # noqa: F401
    build_scientific_decision_request,
    write_scientific_decision_request,
)

__all__ = [
    "ADP010EncounterPort",
    "ADP019EventPort",
    "BindingRefusal",
    "C8Commit",
    "CAN008RulePort",
    "CAN011TargetPort",
    "Currentness",
    "E1Binding",
    "E2OwnerPort",
    "JoinedOutcome",
    "JoinedProducer",
    "JoinedRefusal",
    "Out9Binding",
    "PortRefusal",
    "Resource",
    "SEVERANCE_EDGES",
    "SEVER_CODES",
    "SeveranceTrial",
    "SourceClosureDrift",
    "WorldOccurrence",
    "binding",
    "bootstrap",
    "build_scientific_decision_request",
    "build_world_occurrence",
    "commit_world_occurrence",
    "install",
    "joined_consumer_assertion",
    "ports",
    "prepare_journal_env",
    "producer",
    "production_registries",
    "read_out9",
    "run_all_severances",
    "run_severance",
    "scientific",
    "severance",
    "validate_occurrence_payload",
    "verify_out9_against_source",
    "verify_sources",
    "write_scientific_decision_request",
]
