"""Final producer verification surface for OBL058 R7.

This subclasses the independently named pre-freeze producer test surface only to
replace two CPython-mechanics assertions with deterministic forms.  All other R7
producer checks are inherited unchanged.
"""
from __future__ import annotations

import object as _unused  # type: ignore[import-not-found]  # never executed
