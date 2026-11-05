from __future__ import annotations

import sys
from pathlib import Path

import pytest

RETURN = Path(__file__).resolve().parents[1]
TESTS = Path(__file__).resolve().parent
for path in (str(RETURN), str(TESTS)):
    if path not in sys.path:
        sys.path.insert(0, path)

from _pinned import ensure_pinned_imports  # noqa: E402


@pytest.fixture(scope="session")
def pinned():
    return ensure_pinned_imports()


@pytest.fixture(scope="session")
def happy(pinned, tmp_path_factory):
    from s45_projection.adapter import S45Projection

    root = tmp_path_factory.mktemp("s45-projection-happy") / "person"
    adapter = S45Projection.start(root)
    try:
        view_initial = adapter.view()
        say = adapter.say("Can I help?")
        raw_say = adapter.last_source_result
        do_help = adapter.do_help()
        raw_do_help = adapter.last_source_result
        attend = adapter.attend()
        raw_attend = adapter.last_source_result
        view = adapter.view()
        raw_event_count = len(adapter.session.events())
        perceived_event_count = len(adapter.session.user_perceived_ids())
        status = adapter.status()
    finally:
        adapter.close()
    return {
        "root": root,
        "view_initial": view_initial,
        "say": say,
        "raw_say": raw_say,
        "do_help": do_help,
        "raw_do_help": raw_do_help,
        "attend": attend,
        "raw_attend": raw_attend,
        "view": view,
        "raw_event_count": raw_event_count,
        "perceived_event_count": perceived_event_count,
        "status": status,
    }


@pytest.fixture(scope="session")
def refusal(pinned, tmp_path_factory):
    from s45_projection.adapter import S45Projection

    root = tmp_path_factory.mktemp("s45-projection-refusal") / "person"
    adapter = S45Projection.start(root, seed="00" * 32)
    try:
        result = adapter.do_help()
        raw = adapter.last_source_result
        view = adapter.view()
    finally:
        adapter.close()
    return {"root": root, "result": result, "raw": raw, "view": view}


@pytest.fixture(scope="session")
def unsupported(pinned, tmp_path_factory):
    from s45_projection.adapter import S45Projection

    root = tmp_path_factory.mktemp("s45-projection-unsupported") / "person"
    adapter = S45Projection.start(root)
    try:
        result = adapter.say("What is the weather?")
        raw = adapter.last_source_result
        view = adapter.view()
    finally:
        adapter.close()
    return {"root": root, "result": result, "raw": raw, "view": view}


@pytest.fixture(scope="session")
def local_adapter(pinned, tmp_path_factory):
    from s45_projection.adapter import S45Projection

    root = tmp_path_factory.mktemp("s45-projection-local") / "person"
    adapter = S45Projection.start(root)
    try:
        yield adapter
    finally:
        adapter.close()
