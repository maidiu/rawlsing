from __future__ import annotations

import json
import sys
from pathlib import Path

PRODUCT = Path(__file__).resolve().parents[1]
if str(PRODUCT) not in sys.path:
    sys.path.insert(0, str(PRODUCT))

from sorok_s45_s47 import cli  # noqa: E402

PROJECTION = Path(cli.PROJECTION_RETURN)
if str(PROJECTION) not in sys.path:
    sys.path.insert(0, str(PROJECTION))

from s45_projection import projection  # noqa: E402


def _assert_public(value, path="<root>") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            assert key not in projection.PRIVATE_KEYS, path + "." + str(key)
            assert key not in {"root_hash", "root_id"}, path + "." + str(key)
            _assert_public(item, path + "." + str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _assert_public(item, path + "[" + str(index) + "]")
    elif isinstance(value, str):
        for marker in projection.FORBIDDEN_VALUE_MARKERS:
            assert marker not in value, path + " contains " + marker


def _run(capsys, *args):
    capsys.readouterr()
    code = cli.main(list(args))
    captured = capsys.readouterr()
    assert code == 0, captured.err
    return json.loads(captured.out)


def test_new_and_view_are_public_wp19_views(tmp_path, capsys):
    state = tmp_path / "person"
    new = _run(capsys, "new", "--state", str(state))
    view = _run(capsys, "view", "--state", str(state))
    assert new["schema"] == projection.VIEW_SCHEMA
    assert view["schema"] == projection.VIEW_SCHEMA
    assert "root_hash" not in json.dumps(new)
    assert "root_hash" not in json.dumps(view)
    _assert_public(new)
    _assert_public(view)


def test_result_and_status_receipts_do_not_leak_root_identity(tmp_path, capsys):
    state = tmp_path / "person"
    _run(capsys, "new", "--state", str(state))
    said = _run(capsys, "say", "--state", str(state), "Can I help?")
    helped = _run(capsys, "do-help", "--state", str(state))
    attended = _run(capsys, "attend", "--state", str(state))
    status = _run(capsys, "status", "--state", str(state))
    assert said["schema"] == projection.RESULT_SCHEMA
    assert helped["schema"] == projection.RESULT_SCHEMA
    assert attended["schema"] == projection.RESULT_SCHEMA
    assert status["schema"] == projection.STATUS_SCHEMA
    for value in (said, helped, attended, status):
        assert "root_hash" not in json.dumps(value)
        _assert_public(value)
