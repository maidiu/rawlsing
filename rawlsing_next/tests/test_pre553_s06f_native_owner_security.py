"""Compatibility helper shim for the frozen S06FR hostile overlay.

The historical S06FR reviewer test imports its fixture helpers from this module
name. Current PRE-MAIN does not carry the S06F test module. This shim exposes
only the source-free fixture helpers from ``s06g_fixtures``; it contains no S06F
acceptance test and creates no issuer, source, actor or production authority.
"""
from rawlsing_next.tests.s06g_fixtures import (  # noqa: F401
    checkpoint_with_publication,
    m2_fixture,
    ref,
    register,
    subject,
)
