"""S49 independent actor-parameterized producer."""
from .bootstrap import install
from .errors import S49Refusal
from .actor import (
    B_ACTOR_KEY, CONTROLLED_GRADE, MISSING_B_CONTEXT, S49_GRADE,
    SOURCE_OWNER_HOLD, controlled_b_sources, generate_b, perform_b_attempt,
    root_b_sources,
)
from .session import (
    ACTUAL_SOURCE_GRADE, B_RESULT_KIND, B_TURN_KIND,
    CONTROLLED_SOURCE_GRADE, S49_SCHEMA, S49Session,
)

install()

__all__ = [
    "ACTUAL_SOURCE_GRADE", "B_ACTOR_KEY", "B_RESULT_KIND", "B_TURN_KIND",
    "CONTROLLED_GRADE", "CONTROLLED_SOURCE_GRADE", "MISSING_B_CONTEXT",
    "S49_GRADE", "S49Refusal", "S49Session", "S49_SCHEMA", "SOURCE_OWNER_HOLD",
    "controlled_b_sources", "generate_b", "perform_b_attempt", "root_b_sources",
]
