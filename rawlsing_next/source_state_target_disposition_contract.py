"""K02 J02-vocabulary compatibility repair for the PRE-V3 source-state contract.

This module preserves the frozen K02 production implementation byte-for-byte in
``_source_state_target_disposition_k02_candidate.py`` and changes only the
accepted vocabulary surface proven incompatible by the L02 independent court.
No source-family/native-code semantics are introduced here.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

_IMPL_PATH = Path(__file__).with_name("_source_state_target_disposition_k02_candidate.py")
_SPEC = importlib.util.spec_from_file_location(
    "rawlsing_next._source_state_target_disposition_k02_candidate",
    _IMPL_PATH,
)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"cannot load frozen K02 implementation from {_IMPL_PATH}")
_IMPL = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _IMPL
_SPEC.loader.exec_module(_IMPL)

# Exact accepted J02 vocabulary repaired under M02 authority.
TYPED_MISSING_NONRESPONSE = "TYPED_MISSING_NONRESPONSE"
NOT_APPLICABLE_OR_INELIGIBLE = "NOT_APPLICABLE_OR_INELIGIBLE"
SOURCE_NOT_APPLICABLE_OR_INELIGIBLE = "SOURCE_NOT_APPLICABLE_OR_INELIGIBLE"

# Replace, rather than alias, K02's unauthorized source-class substitution.
_IMPL.STATE_CLASSES = frozenset({
    "SOURCE_SUBSTANTIVE",
    TYPED_MISSING_NONRESPONSE,
    SOURCE_NOT_APPLICABLE_OR_INELIGIBLE,
    "SOURCE_SPECIFIC_SPECIAL",
    "SOURCE_UNKNOWN",
})

# J02 typed-missing and not-applicable dispositions are lawful product states,
# but remain unresolved for denominator members because the frozen K02
# build_record_audit law resolves only TARGET_MEMBER / RESOLVED_NON_TARGET.
# AUTHORIZED_PREQUERY_EXCLUSION remains outside state_bindings: denominator
# removal is still exclusively the frozen pre-query risk-set path.
_IMPL.DISPOSITIONS = frozenset({
    _IMPL.TARGET_MEMBER,
    _IMPL.RESOLVED_NON_TARGET,
    TYPED_MISSING_NONRESPONSE,
    NOT_APPLICABLE_OR_INELIGIBLE,
    _IMPL.UNRESOLVED,
})

for _name in _IMPL.__all__:
    globals()[_name] = getattr(_IMPL, _name)

STATE_CLASSES = _IMPL.STATE_CLASSES
DISPOSITIONS = _IMPL.DISPOSITIONS

__all__ = tuple(dict.fromkeys([
    *_IMPL.__all__,
    "TYPED_MISSING_NONRESPONSE",
    "NOT_APPLICABLE_OR_INELIGIBLE",
    "SOURCE_NOT_APPLICABLE_OR_INELIGIBLE",
]))
