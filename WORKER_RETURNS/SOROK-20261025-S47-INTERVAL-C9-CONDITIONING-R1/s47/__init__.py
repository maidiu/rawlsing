"""S47 interval-to-C9 conditioning composer."""
from .bootstrap import install
from .conditioning import SOURCE_CLASS, current_interval_source, qualify_source
from .errors import S47Refusal
from .session import S47Session, S47_SCHEMA

install()

__all__ = [
    "SOURCE_CLASS", "S47Refusal", "S47Session", "S47_SCHEMA",
    "current_interval_source", "qualify_source",
]
