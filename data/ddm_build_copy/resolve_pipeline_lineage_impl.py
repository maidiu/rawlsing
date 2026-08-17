#!/usr/bin/env python3
"""Compatibility import for the governed W05-B lineage resolver.

The supported resolver is ``resolve_pipeline_lineage``.  This module owns no
filename-derived source/wave discovery, alias parsing, V553 discovery, or
independent CLI behavior.
"""
from __future__ import annotations

from data.ddm_build_copy.resolve_pipeline_lineage import *  # noqa: F401,F403
from data.ddm_build_copy.resolve_pipeline_lineage import main

if __name__ == "__main__":
    raise SystemExit(main())
