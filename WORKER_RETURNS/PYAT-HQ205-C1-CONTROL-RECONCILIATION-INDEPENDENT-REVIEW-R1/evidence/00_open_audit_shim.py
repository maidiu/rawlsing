"""HQ205 open-audit shim.

Records every path under WORKER_RETURNS that the interpreter actually opens, so
import necessity can be measured instead of asserted.

``pathlib.Path.open``/``read_text`` call ``io.open``, and ``io.open`` is a
separate module attribute from ``builtins.open`` even though both start out
bound to the same function object, so BOTH must be patched or pathlib reads are
invisible.
"""
import builtins
import io
import os

_REAL_OPEN = io.open
_LOG = os.environ.get("HQ205_AUDIT_LOG")


def _audit_open(file, *args, **kwargs):
    if _LOG:
        try:
            name = os.fspath(file)
            if isinstance(name, bytes):
                name = name.decode("utf-8", "replace")
            if isinstance(name, str) and "WORKER_RETURNS" in name:
                with _REAL_OPEN(_LOG, "a", encoding="utf-8") as fh:
                    fh.write(os.path.abspath(name) + "\n")
        except Exception:
            pass
    return _REAL_OPEN(file, *args, **kwargs)


builtins.open = _audit_open
io.open = _audit_open
