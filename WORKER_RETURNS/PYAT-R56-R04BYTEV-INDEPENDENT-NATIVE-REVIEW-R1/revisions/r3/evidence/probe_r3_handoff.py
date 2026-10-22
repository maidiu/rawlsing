"""R56-R04BYTEV r3 probe: read-only handoff capability, denial, failure paths, windows.

Actual generated SAV/DTA through the real decoder and unchanged C11/I03 consumer.
Prints JSON receipts; no mocks returning authored expected values.
"""
import fcntl
import hashlib
import json
import mmap
import os
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO))

import pyreadstat  # noqa: E402

import rawlsing_next.pre553_physical_decoder as decoder  # noqa: E402
from rawlsing_next.pre553_physical_decoder import DecoderError  # noqa: E402
from rawlsing_next.tests.test_universal_source_byte_custody import (  # noqa: E402
    _ALTERNATE_ROWS,
    _decode,
    _facts_from_incidence,
    _sha,
    _write_source,
)


def _tmp(prefix):
    return Path(tempfile.mkdtemp(prefix=prefix))


def _digest_fd(fd, size):
    return hashlib.sha256(os.pread(fd, size, 0)).hexdigest()


def _attempt(fn):
    try:
        value = fn()
        if isinstance(value, mmap.mmap):
            value.close()
        return {"denied": False, "result": repr(value)[:120]}
    except Exception as exc:  # noqa: BLE001
        return {"denied": True, "type": type(exc).__name__, "errno": getattr(exc, "errno", None),
                "message": str(exc)[:160]}


def _open_records(source_format, path, expected_sha):
    records = []
    original_open = os.open

    def tracked_open(target, flags, *args, **kwargs):
        fd = original_open(target, flags, *args, **kwargs)
        records.append((str(target), flags, fd))
        return fd

    os.open = tracked_open
    try:
        incidence = _decode(path, source_format, expected_sha)
    finally:
        os.open = original_open
    return incidence, records


def handoff_capability(source_format):
    tmp = _tmp(f"r04bytev-r3-handoff-{source_format}-")
    path = _write_source(tmp / f"source.{source_format}", source_format)
    alternate = _write_source(tmp / f"alt.{source_format}", source_format, _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    incidence, records = _open_records(source_format, path, expected_sha)
    snapshot = incidence._source_snapshot
    construction = [r for r in records if r[0].endswith("source.bin") and (r[1] & os.O_ACCMODE) == os.O_RDWR]
    reader = [r for r in records if r[0].endswith("source.bin") and (r[1] & os.O_ACCMODE) == os.O_RDONLY]
    construction_fd = construction[-1][2] if construction else None
    reader_fd = reader[-1][2] if reader else None
    open_fds = sorted(os.listdir("/dev/fd"))
    construction_closed = False
    if construction_fd is not None:
        try:
            os.fstat(construction_fd)
            construction_closed = False
        except OSError:
            construction_closed = True
    baseline = _facts_from_incidence(incidence, source_format)
    alt_bytes = alternate.read_bytes()
    n = snapshot.size
    attempts = {
        "write": _attempt(lambda: os.write(snapshot.fd, b"x")),
        "pwrite": _attempt(lambda: os.pwrite(snapshot.fd, alt_bytes, 0)),
        "ftruncate": _attempt(lambda: os.ftruncate(snapshot.fd, len(alt_bytes))),
        "mmap_write": _attempt(lambda: mmap.mmap(snapshot.fd, 0, access=mmap.ACCESS_WRITE)),
        "mmap_write_dup": _attempt(lambda: _mmap_dup(snapshot.fd)),
        "reopen_devfd_O_RDWR": _attempt_open(snapshot.fd, os.O_RDWR),
        "reopen_devfd_O_WRONLY": _attempt_open(snapshot.fd, os.O_WRONLY),
        "reopen_devfd_O_RDONLY": _attempt_open(snapshot.fd, os.O_RDONLY),
        "fcntl_F_SETFL_O_RDWR": _attempt(lambda: fcntl.fcntl(snapshot.fd, fcntl.F_SETFL, os.O_RDWR)),
    }
    digest_after = _digest_fd(snapshot.fd, n)
    facts_after = _facts_from_incidence(incidence, source_format)
    access_after_fcntl = snapshot.access_mode
    custody = dict(incidence.source_custody)
    result = {
        "format": source_format,
        "expected_source_sha256": expected_sha,
        "retained_fd_matches_reader_open": reader_fd == snapshot.fd,
        "construction_fd": construction_fd,
        "construction_fd_closed": construction_closed,
        "construction_fd_not_in_dev_fd": str(construction_fd) not in open_fds if construction_fd is not None else None,
        "reader_fd_in_dev_fd": str(snapshot.fd) in open_fds,
        "access_mode": snapshot.access_mode,
        "custody": custody,
        "snapshot_nlink": os.fstat(snapshot.fd).st_nlink,
        "snapshot_path_exists": snapshot.path.exists(),
        "digest_equal_after_denials": digest_after == expected_sha,
        "facts_equal_baseline": facts_after == baseline,
        "access_mode_after_fcntl": access_after_fcntl,
        "attempts": attempts,
    }
    incidence.close()
    return result


def _attempt_open(fd, flags):
    try:
        new_fd = os.open(f"/dev/fd/{fd}", flags)
    except Exception as exc:  # noqa: BLE001
        return {"denied": True, "type": type(exc).__name__, "errno": getattr(exc, "errno", None),
                "message": str(exc)[:160]}
    os.close(new_fd)
    return {"denied": False, "opened": True}


def _mmap_dup(fd):
    dup = os.dup(fd)
    try:
        return mmap.mmap(dup, 0, access=mmap.ACCESS_WRITE)
    finally:
        os.close(dup)


def wrong_and_closed_fd():
    tmp = _tmp("r04bytev-r3-wrongfd-")
    path = _write_source(tmp / "source.sav", "sav")
    expected_sha = _sha(path)
    result = {}
    incidence = _decode(path, "sav", expected_sha)
    snapshot = incidence._source_snapshot
    real_fd = snapshot.fd
    wrong = os.open(path, os.O_RDWR)
    snapshot.fd = wrong
    result["substituted_O_RDWR_reader_path"] = _attempt(lambda: snapshot.reader_path())
    result["substituted_O_RDWR_prefix"] = _attempt(lambda: snapshot.read_prefix(8))
    snapshot.fd = real_fd
    os.close(wrong)
    devnull = os.open("/dev/null", os.O_RDONLY)
    snapshot.fd = devnull
    result["substituted_O_RDONLY_nonregular"] = _attempt(lambda: snapshot.read_prefix(8))
    snapshot.fd = real_fd
    os.close(devnull)
    snapshot.fd = 10**6
    result["substituted_invalid_fd"] = _attempt(lambda: snapshot.verify())
    snapshot.fd = real_fd
    incidence.close()
    result["after_close_access_mode"] = snapshot.access_mode
    result["after_close_iter"] = _attempt(lambda: list(incidence.iter_cells()))

    incidence2 = _decode(path, "sav", expected_sha)
    snapshot2 = incidence2._source_snapshot
    os.close(snapshot2.fd)
    result["os_closed_verify"] = _attempt(lambda: incidence2.verify_source_identity())
    result["os_closed_access_mode"] = _attempt(lambda: snapshot2.access_mode)
    # real close path on an externally closed descriptor (do not preset _closed)
    incidence3 = _decode(path, "sav", expected_sha)
    snapshot3 = incidence3._source_snapshot
    os.close(snapshot3.fd)
    try:
        incidence3.close()
        result["os_closed_close"] = {"raised": None}
    except Exception as exc:  # noqa: BLE001
        result["os_closed_close"] = {"raised": type(exc).__name__, "message": str(exc)[:120]}
    try:
        snapshot2._closed = True
        incidence2.close()
    except Exception:  # noqa: BLE001
        pass
    return result


def handoff_failure_paths():
    tmp = _tmp("r04bytev-r3-failure-")
    path = _write_source(tmp / "source.sav", "sav")
    result = {}
    temp_root = Path(tempfile.gettempdir())

    def custody_dirs():
        return {p.name for p in temp_root.glob("rawlsing-source-custody-*")}

    before = custody_dirs()

    # (a) reader open failure
    original_open = os.open
    construction_fds = []

    def failing_reader_open(target, flags, *args, **kwargs):
        if str(target).endswith("source.bin") and (flags & os.O_ACCMODE) == os.O_RDONLY:
            raise PermissionError(13, "reader open denied")
        fd = original_open(target, flags, *args, **kwargs)
        if str(target).endswith("source.bin"):
            construction_fds.append(fd)
        return fd

    os.open = failing_reader_open
    try:
        _decode(path, "sav", _sha(path))
        result["reader_open_failure"] = {"raised": None}
    except Exception as exc:  # noqa: BLE001
        result["reader_open_failure"] = {"raised": type(exc).__name__, "message": str(exc)[:120]}
    finally:
        os.open = original_open
    result["reader_open_failure"]["construction_fds"] = construction_fds
    result["reader_open_failure"]["construction_fds_closed"] = all(
        _attempt(lambda fd=fd: os.fstat(fd))["denied"] for fd in construction_fds
    )
    result["reader_open_failure"]["leftover_dirs"] = sorted(custody_dirs() - before)

    # (b) pathname replacement between reader open and pre-unlink stat
    foreign = tmp / "foreign.bin"
    foreign.write_bytes(b"foreign-replacement")
    original_open = os.open
    original_fstat = os.fstat
    state = {"reader_fd": None, "path": None, "done": False}

    def tracking_open(target, flags, *args, **kwargs):
        fd = original_open(target, flags, *args, **kwargs)
        if str(target).endswith("source.bin") and (flags & os.O_ACCMODE) == os.O_RDONLY:
            state["reader_fd"] = fd
            state["path"] = str(target)
        return fd

    def swapping_fstat(fd):
        real = original_fstat(fd)
        if not state["done"] and fd == state["reader_fd"] and state["path"]:
            state["done"] = True
            os.replace(foreign, state["path"])
        return real

    os.open = tracking_open
    os.fstat = swapping_fstat
    try:
        _decode(path, "sav", _sha(path))
        result["path_replacement_failure"] = {"raised": None}
    except Exception as exc:  # noqa: BLE001
        result["path_replacement_failure"] = {"raised": type(exc).__name__, "message": str(exc)[:120]}
    finally:
        os.open = original_open
        os.fstat = original_fstat
    leftovers = sorted(custody_dirs() - before)
    leftover_contents = {}
    for leftover in leftovers:
        target_dir = temp_root / leftover
        for item in target_dir.iterdir():
            if item.is_file():
                leftover_contents[item.name] = item.read_bytes().decode("latin1")
    result["path_replacement_failure"]["leftover_dirs"] = leftovers
    result["path_replacement_failure"]["leftover_contents"] = leftover_contents
    result["path_replacement_failure"]["foreign_preserved_at_leftover_path"] = any(
        value == "foreign-replacement" for value in leftover_contents.values()
    )
    result["path_replacement_failure"]["foreign_original_name_absent_after_move"] = not foreign.exists()
    for leftover in leftovers:
        target_dir = temp_root / leftover
        for item in target_dir.iterdir():
            item.unlink()
        target_dir.rmdir()

    # (c) reader/construction inode mismatch
    original_open = os.open
    original_fstat = os.fstat
    state2 = {"reader_fd": None, "done": False}

    def tracking_open2(target, flags, *args, **kwargs):
        fd = original_open(target, flags, *args, **kwargs)
        if str(target).endswith("source.bin") and (flags & os.O_ACCMODE) == os.O_RDONLY:
            state2["reader_fd"] = fd
        return fd

    def mismatched_fstat(fd):
        real = original_fstat(fd)
        if not state2["done"] and fd == state2["reader_fd"]:
            state2["done"] = True
            values = list(real)
            values[1] = real.st_ino + 1
            return os.stat_result(values)
        return real

    os.open = tracking_open2
    os.fstat = mismatched_fstat
    try:
        _decode(path, "sav", _sha(path))
        result["inode_mismatch_failure"] = {"raised": None}
    except Exception as exc:  # noqa: BLE001
        result["inode_mismatch_failure"] = {"raised": type(exc).__name__, "message": str(exc)[:120]}
    finally:
        os.open = original_open
        os.fstat = original_fstat
    result["inode_mismatch_failure"]["leftover_dirs"] = sorted(custody_dirs() - before)
    return result


def path_and_lifetime_windows(source_format):
    tmp = _tmp(f"r04bytev-r3-window-{source_format}-")
    path = _write_source(tmp / f"source.{source_format}", source_format)
    alternate = _write_source(tmp / f"alt.{source_format}", source_format, _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    incidence = _decode(path, source_format, expected_sha)
    snapshot = incidence._source_snapshot
    baseline = _facts_from_incidence(incidence, source_format)
    result = {"format": source_format, "baseline_y": baseline["i03_y_cells"]}

    # original-path replacement after acquisition
    _write_source(path, source_format, _ALTERNATE_ROWS)
    result["original_path_replacement_facts_equal"] = _facts_from_incidence(incidence, source_format) == baseline

    # private-path recreation at the old snapshot pathname before more reads
    os.replace(_write_source(tmp / f"foreign.{source_format}", source_format, _ALTERNATE_ROWS), snapshot.path)
    result["private_path_replacement_facts_equal"] = _facts_from_incidence(incidence, source_format) == baseline
    result["foreign_path_exists"] = snapshot.path.exists()
    incidence.close()
    result["foreign_survives_close"] = snapshot.path.exists()
    if snapshot.path.exists():
        snapshot.path.unlink()
    try:
        snapshot.directory.rmdir()
    except OSError:
        pass
    return result


def repeated_new_identity_and_cold(source_format):
    tmp = _tmp(f"r04bytev-r3-identity-{source_format}-")
    path = _write_source(tmp / f"source.{source_format}", source_format)
    original_bytes = path.read_bytes()
    original_sha = hashlib.sha256(original_bytes).hexdigest()
    script = (
        "import json, sys\n"
        "from rawlsing_next.tests.test_universal_source_byte_custody import _cold_observation\n"
        "print(json.dumps(_cold_observation(sys.argv[1], sys.argv[2], sys.argv[3]), sort_keys=True))\n"
    )
    import subprocess

    def cold():
        return subprocess.run([sys.executable, "-c", script, str(path), source_format, original_sha],
                              cwd=REPO, capture_output=True, text=True, timeout=180)

    true_cold_baseline = cold()
    incidence = _decode(path, source_format, original_sha)
    first = _facts_from_incidence(incidence, source_format)
    second = _facts_from_incidence(incidence, source_format)
    old_ref = first["i03_fact_ref"]
    _write_source(path, source_format, _ALTERNATE_ROWS)
    new_sha = _sha(path)
    new_inc = _decode(path, source_format, new_sha)
    new_facts = _facts_from_incidence(new_inc, source_format)
    new_inc.close()
    old_after = _facts_from_incidence(incidence, source_format)
    refused = _attempt(lambda: _decode(path, source_format, original_sha))
    fault_cold = cold()
    incidence.close()
    path.write_bytes(original_bytes)
    restored_cold = cold()
    return {
        "format": source_format,
        "repeated_facts_equal": first == second,
        "old_incidence_keeps_old_facts": old_after == first,
        "new_digest_differs": new_sha != original_sha,
        "new_facts_differ": new_facts["i03_fact_ref"] != old_ref and new_facts["i03_y_cells"] != first["i03_y_cells"],
        "old_digest_on_changed_path_refused": refused["denied"],
        "old_digest_refusal": refused.get("type"),
        "cold_true_baseline_rc": true_cold_baseline.returncode,
        "cold_fault_rc": fault_cold.returncode,
        "cold_fault_stdout_empty": fault_cold.stdout == "",
        "cold_restored_rc": restored_cold.returncode,
        "cold_restored_equals_baseline": true_cold_baseline.stdout == restored_cold.stdout and true_cold_baseline.returncode == 0,
    }


def sav_hashing_and_streaming_shape():
    tmp = _tmp("r04bytev-r3-sav-shape-")
    path = _write_source(tmp / "source.sav", "sav")
    incidence = _decode(path, "sav", _sha(path))
    original_sha_fd = decoder._sha_fd
    hash_calls = {"n": 0}

    def counted_sha_fd(fd):
        hash_calls["n"] += 1
        return original_sha_fd(fd)

    chunk_calls = {"n": 0}
    original_chunks = pyreadstat.read_file_in_chunks

    def counted_chunks(reader, source, *args, **kwargs):
        chunk_calls["n"] += 1
        return original_chunks(reader, source, *args, **kwargs)

    decoder._sha_fd = counted_sha_fd
    pyreadstat.read_file_in_chunks = counted_chunks
    try:
        cells = sum(len(batch) for batch in incidence.iter_batches(4))
    finally:
        decoder._sha_fd = original_sha_fd
        pyreadstat.read_file_in_chunks = original_chunks
    incidence.close()
    return {"cells": cells, "sha_fd_calls_in_one_pass": hash_calls["n"],
            "chunk_generator_calls": chunk_calls["n"],
            "streaming_not_per_chunk_hash": hash_calls["n"] <= 1}


if __name__ == "__main__":
    print(json.dumps({
        "handoff_sav": handoff_capability("sav"),
        "handoff_dta": handoff_capability("dta"),
        "wrong_and_closed_fd": wrong_and_closed_fd(),
        "handoff_failure_paths": handoff_failure_paths(),
        "windows_sav": path_and_lifetime_windows("sav"),
        "windows_dta": path_and_lifetime_windows("dta"),
        "identity_sav": repeated_new_identity_and_cold("sav"),
        "identity_dta": repeated_new_identity_and_cold("dta"),
        "sav_shape": sav_hashing_and_streaming_shape(),
    }, indent=2, sort_keys=True, default=str))
