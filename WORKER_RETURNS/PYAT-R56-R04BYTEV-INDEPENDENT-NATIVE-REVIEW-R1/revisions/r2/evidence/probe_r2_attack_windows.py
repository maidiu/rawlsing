"""R56-R04BYTEV r2 requalification probe: attack windows and reader binding on repaired candidate.

Uses actual generated SAV/DTA through the real decoder and unchanged C11/I03 consumer.
Prints JSON receipt; no mocks returning authored expected values.
"""
import hashlib
import json
import mmap
import os
import subprocess
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
    _ROWS,
    _cell_signature,
    _decode,
    _facts_from_incidence,
    _sha,
    _write_source,
)


def _tmp(prefix):
    return Path(tempfile.mkdtemp(prefix=prefix))


def reader_binding_and_pathname_replacement(source_format):
    tmp = _tmp(f"r04bytev-r2-bind-{source_format}-")
    path = _write_source(tmp / f"source.{source_format}", source_format)
    alternate = _write_source(tmp / f"alt.{source_format}", source_format, _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    seen_sources = []
    orig_read = pyreadstat.read_sav if source_format == "sav" else pyreadstat.read_dta
    orig_chunks = pyreadstat.read_file_in_chunks

    def tracked_read(source, *args, **kwargs):
        seen_sources.append(str(source))
        return orig_read(source, *args, **kwargs)

    def tracked_chunks(reader, source, *args, **kwargs):
        seen_sources.append(str(source))
        return orig_chunks(reader, source, *args, **kwargs)

    setattr(pyreadstat, "read_sav" if source_format == "sav" else "read_dta", tracked_read)
    pyreadstat.read_file_in_chunks = tracked_chunks
    try:
        incidence = _decode(path, source_format, expected_sha)
        snapshot = incidence._source_snapshot
        baseline = _facts_from_incidence(incidence, source_format)
        # Replace a file at the old private snapshot pathname before further reads.
        os.replace(alternate, snapshot.path)
        replacement_exists = snapshot.path.exists()
        observed = _facts_from_incidence(incidence, source_format)
        custody = dict(incidence.source_custody)
        verify_after = incidence.verify_source_identity()
        incidence.close()
        replacement_survives_close = snapshot.path.exists()
        if snapshot.path.exists():
            snapshot.path.unlink()
        try:
            snapshot.directory.rmdir()
        except OSError:
            pass
    finally:
        setattr(pyreadstat, "read_sav" if source_format == "sav" else "read_dta", orig_read)
        pyreadstat.read_file_in_chunks = orig_chunks
    return {
        "format": source_format,
        "reader_sources": seen_sources,
        "reader_path_is_dev_fd": all(s.startswith("/dev/fd/") for s in seen_sources),
        "snapshot_pathname_exists_before_replacement": False,
        "replacement_path_exists_after_attack": replacement_exists,
        "observed_equals_baseline": observed == baseline,
        "observed_i03_y_cells": observed["i03_y_cells"],
        "baseline_i03_y_cells": baseline["i03_y_cells"],
        "observed_source_sha256": observed["source_sha256"],
        "expected_source_sha256": expected_sha,
        "verify_source_identity_after_attack": verify_after,
        "custody": custody,
        "replacement_survives_close": replacement_survives_close,
    }


def in_place_before_lazy(source_format):
    tmp = _tmp(f"r04bytev-r2-inplace-{source_format}-")
    path = _write_source(tmp / f"source.{source_format}", source_format)
    alternate = _write_source(tmp / f"alt.{source_format}", source_format, _ALTERNATE_ROWS)
    incidence = _decode(path, source_format, _sha(path))
    snapshot = incidence._source_snapshot
    alt_bytes = alternate.read_bytes()
    os.pwrite(snapshot.fd, alt_bytes, 0)
    os.ftruncate(snapshot.fd, len(alt_bytes))
    error = None
    try:
        list(incidence.iter_cells())
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"
    incidence.close()
    return {"format": source_format, "error": error, "typed_refusal": isinstance(error, str) and "DecoderError" in error}


def between_batch_external_pwrite():
    tmp = _tmp("r04bytev-r2-between-batch-")
    path = _write_source(tmp / "source.sav", "sav")
    alternate = _write_source(tmp / "alt.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    baseline = _decode(path, "sav", expected_sha)
    baseline_cells = _cell_signature(baseline.iter_cells(4))
    baseline.close()

    incidence = _decode(path, "sav", expected_sha)
    snapshot = incidence._source_snapshot
    alt_bytes = alternate.read_bytes()
    yielded = []
    error = None
    try:
        for index, batch in enumerate(incidence.iter_batches(4)):
            if index == 0:
                os.pwrite(snapshot.fd, alt_bytes, 0)
                os.ftruncate(snapshot.fd, len(alt_bytes))
            yielded.extend(batch)
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"
    incidence.close()
    signature = _cell_signature(yielded)
    return {
        "error": error,
        "typed_refusal": isinstance(error, str) and "DecoderError" in error,
        "yielded_cells": len(yielded),
        "yielded_is_prefix_of_baseline": signature == baseline_cells[: len(signature)],
        "baseline_cells": len(baseline_cells),
    }


def truncate_and_close():
    tmp = _tmp("r04bytev-r2-trunc-")
    path = _write_source(tmp / "source.sav", "sav")
    incidence = _decode(path, "sav", _sha(path))
    os.ftruncate(incidence._source_snapshot.fd, 0)
    trunc_error = None
    try:
        list(incidence.iter_cells())
    except Exception as exc:  # noqa: BLE001
        trunc_error = f"{type(exc).__name__}: {exc}"
    incidence.close()
    close_error = None
    try:
        list(incidence.iter_cells())
    except Exception as exc:  # noqa: BLE001
        close_error = f"{type(exc).__name__}: {exc}"
    return {
        "truncate_error": trunc_error,
        "truncate_typed": isinstance(trunc_error, str) and "DecoderError" in trunc_error,
        "closed_read_error": close_error,
        "closed_typed": isinstance(close_error, str) and "DecoderError" in close_error,
    }


def dta_chunk_limitation_and_shape():
    tmp = _tmp("r04bytev-r2-dta-shape-")
    path = _write_source(tmp / "source.dta", "dta")
    incidence = _decode(path, "dta", _sha(path))
    snapshot = incidence._source_snapshot
    fd_path = snapshot.reader_path
    direct_chunk_error = None
    try:
        list(pyreadstat.read_file_in_chunks(pyreadstat.read_dta, fd_path, chunksize=1,
                                            apply_value_formats=False, user_missing=True))
    except Exception as exc:  # noqa: BLE001
        direct_chunk_error = f"{type(exc).__name__}: {exc}"
    calls = {"read_dta": 0, "chunks": 0}
    orig_read = pyreadstat.read_dta
    orig_chunks = pyreadstat.read_file_in_chunks

    def tracked_read(source, *args, **kwargs):
        calls["read_dta"] += 1
        return orig_read(source, *args, **kwargs)

    def tracked_chunks(reader, source, *args, **kwargs):
        calls["chunks"] += 1
        return orig_chunks(reader, source, *args, **kwargs)

    pyreadstat.read_dta = tracked_read
    pyreadstat.read_file_in_chunks = tracked_chunks
    try:
        list(incidence.iter_cells(4))
    finally:
        pyreadstat.read_dta = orig_read
        pyreadstat.read_file_in_chunks = orig_chunks
    incidence.close()
    return {
        "dev_fd_direct_chunk_error": direct_chunk_error,
        "value_pass_reader_calls": calls,
        "dta_full_frame_per_pass": calls["read_dta"] >= 1 and calls["chunks"] == 0,
    }


def sav_chunk_shape():
    tmp = _tmp("r04bytev-r2-sav-shape-")
    path = _write_source(tmp / "source.sav", "sav")
    incidence = _decode(path, "sav", _sha(path))
    calls = {"read_sav": 0, "chunks": 0}
    orig_read = pyreadstat.read_sav
    orig_chunks = pyreadstat.read_file_in_chunks

    def tracked_read(source, *args, **kwargs):
        calls["read_sav"] += 1
        return orig_read(source, *args, **kwargs)

    def tracked_chunks(reader, source, *args, **kwargs):
        calls["chunks"] += 1
        return orig_chunks(reader, source, *args, **kwargs)

    pyreadstat.read_sav = tracked_read
    pyreadstat.read_file_in_chunks = tracked_chunks
    try:
        list(incidence.iter_cells(4))
    finally:
        pyreadstat.read_sav = orig_read
        pyreadstat.read_file_in_chunks = orig_chunks
    incidence.close()
    return {"value_pass_reader_calls": calls, "sav_uses_chunks": calls["chunks"] >= 1}


def posix_refusal():
    tmp = _tmp("r04bytev-r2-posix-")
    path = _write_source(tmp / "source.sav", "sav")
    expected_sha = _sha(path)
    original_is_dir = Path.is_dir

    def fake_is_dir(self):
        if str(self) == "/dev/fd":
            return False
        return original_is_dir(self)

    Path.is_dir = fake_is_dir
    error = None
    try:
        _decode(path, "sav", expected_sha)
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"
    finally:
        Path.is_dir = original_is_dir
    return {"error": error, "typed_refusal": isinstance(error, str) and "DecoderError" in error}


def _capture_mapping(source_path):
    captured = {}
    original_unlink = os.unlink

    def unlink_capture(target):
        if str(target).endswith("source.bin") and "mapping" not in captured:
            os.chmod(target, 0o600)
            fd = os.open(target, os.O_RDWR)
            captured["mapping"] = mmap.mmap(fd, 0, access=mmap.ACCESS_WRITE)
            captured["fd"] = fd
        return original_unlink(target)

    os.unlink = unlink_capture
    try:
        incidence = _decode(source_path, "sav", _sha(source_path))
    finally:
        os.unlink = original_unlink
    return incidence, captured


def mmap_between_batch():
    tmp = _tmp("r04bytev-r2-mmap-batch-")
    path = _write_source(tmp / "source.sav", "sav")
    alternate = _write_source(tmp / "alt.sav", "sav", _ALTERNATE_ROWS)
    baseline_inc = _decode(path, "sav", _sha(path))
    baseline_cells = _cell_signature(baseline_inc.iter_cells(4))
    baseline_inc.close()
    incidence, captured = _capture_mapping(path)
    snapshot = incidence._source_snapshot
    alt_bytes = alternate.read_bytes()
    mapped = captured.get("mapping")
    yielded = []
    error = None
    result = {"mmap_captured": mapped is not None, "signature_changed": None,
              "error": None, "observed_y_cells": None, "cells_after_first_batch_differ": None}
    if mapped is not None:
        for index, batch in enumerate(incidence.iter_batches(4)):
            if index == 1:
                before = snapshot._current_signature()
                mapped[: len(alt_bytes)] = alt_bytes
                if len(alt_bytes) < len(mapped):
                    mapped[len(alt_bytes):] = b"\x00" * (len(mapped) - len(alt_bytes))
                after = snapshot._current_signature()
                result["signature_changed"] = before != after
                result["signature_before"] = before
                result["signature_after"] = after
            yielded.extend(batch)
        signature = _cell_signature(yielded)
        result["cells_after_first_batch_differ"] = signature != baseline_cells[: len(signature)]
        result["yielded_cells"] = len(yielded)
        try:
            observed = _facts_from_incidence(incidence, "sav")
            result["observed_y_cells"] = observed["i03_y_cells"]
        except Exception as exc:  # noqa: BLE001
            result["error"] = f"{type(exc).__name__}: {exc}"
        mapped.close()
        os.close(captured["fd"])
    incidence.close()
    return result


def mmap_before_metadata_verify():
    tmp = _tmp("r04bytev-r2-mmap-meta-")
    path = _write_source(tmp / "source.sav", "sav")
    alternate = _write_source(tmp / "alt.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    captured = {}
    original_unlink = os.unlink

    def unlink_capture(target):
        if str(target).endswith("source.bin") and "mapping" not in captured:
            os.chmod(target, 0o600)
            fd = os.open(target, os.O_RDWR)
            captured["mapping"] = mmap.mmap(fd, 0, access=mmap.ACCESS_WRITE)
            captured["fd"] = fd
        return original_unlink(target)

    original_read = pyreadstat.read_sav
    alt_bytes = alternate.read_bytes()

    def hostile_metadata(source, *args, **kwargs):
        if kwargs.get("metadataonly") and captured.get("mapping") is not None:
            mapped = captured["mapping"]
            mapped[: len(alt_bytes)] = alt_bytes
            if len(alt_bytes) < len(mapped):
                mapped[len(alt_bytes):] = b"\x00" * (len(mapped) - len(alt_bytes))
        return original_read(source, *args, **kwargs)

    os.unlink = unlink_capture
    pyreadstat.read_sav = hostile_metadata
    error = None
    try:
        _decode(path, "sav", expected_sha)
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"
    finally:
        os.unlink = original_unlink
        pyreadstat.read_sav = original_read
        if captured.get("mapping") is not None:
            captured["mapping"].close()
        if captured.get("fd") is not None:
            os.close(captured["fd"])
    return {"error": error, "typed_refusal": isinstance(error, str) and "DecoderError" in error}



def mmap_residual():
    tmp = _tmp("r04bytev-r2-mmap-")
    path = _write_source(tmp / "source.sav", "sav")
    alternate = _write_source(tmp / "alt.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    captured = {}
    original_unlink = os.unlink

    def unlink_capture(target):
        if str(target).endswith("source.bin") and "mapping" not in captured:
            os.chmod(target, 0o600)
            fd = os.open(target, os.O_RDWR)
            mapped = mmap.mmap(fd, 0, access=mmap.ACCESS_WRITE)
            captured["mapping"] = mapped
            captured["fd"] = fd
        return original_unlink(target)

    os.unlink = unlink_capture
    try:
        incidence = _decode(path, "sav", expected_sha)
    finally:
        os.unlink = original_unlink
    snapshot = incidence._source_snapshot
    baseline = _facts_from_incidence(incidence, "sav")
    alt_bytes = alternate.read_bytes()
    mapped = captured.get("mapping")
    result = {
        "mmap_captured": mapped is not None,
        "baseline_y_cells": baseline["i03_y_cells"],
        "observed_y_cells": None,
        "error": None,
        "signature_before": None,
        "signature_after_mmap_write": None,
    }
    if mapped is not None:
        before = snapshot._current_signature()
        mapped[: len(alt_bytes)] = alt_bytes
        if len(alt_bytes) < len(mapped):
            mapped[len(alt_bytes):] = b"\x00" * (len(mapped) - len(alt_bytes))
        after = snapshot._current_signature()
        result["signature_before"] = before
        result["signature_after_mmap_write"] = after
        result["signature_changed"] = before != after
        try:
            observed = _facts_from_incidence(incidence, "sav")
            result["observed_y_cells"] = observed["i03_y_cells"]
            result["observed_equals_baseline"] = observed == baseline
        except Exception as exc:  # noqa: BLE001
            result["error"] = f"{type(exc).__name__}: {exc}"
        mapped.close()
        os.close(captured["fd"])
    incidence.close()
    return result


def cold_replay(source_format):
    tmp = _tmp(f"r04bytev-r2-cold-{source_format}-")
    path = _write_source(tmp / f"cold.{source_format}", source_format)
    original_bytes = path.read_bytes()
    original_sha = hashlib.sha256(original_bytes).hexdigest()
    script = (
        "import json, sys\n"
        "from rawlsing_next.tests.test_universal_source_byte_custody import _cold_observation\n"
        "print(json.dumps(_cold_observation(sys.argv[1], sys.argv[2], sys.argv[3]), sort_keys=True))\n"
    )

    def run():
        return subprocess.run([sys.executable, "-c", script, str(path), source_format, original_sha],
                              cwd=REPO, capture_output=True, text=True, timeout=180)

    baseline = run()
    _write_source(path, source_format, _ALTERNATE_ROWS)
    fault = run()
    path.write_bytes(original_bytes)
    restored = run()
    return {
        "format": source_format,
        "baseline_rc": baseline.returncode,
        "fault_rc": fault.returncode,
        "fault_stdout_empty": fault.stdout == "",
        "fault_error_tail": fault.stderr.strip().splitlines()[-1] if fault.stderr.strip() else None,
        "restored_rc": restored.returncode,
        "restored_equals_baseline": baseline.stdout == restored.stdout and baseline.returncode == 0,
    }


def repeated_reads():
    tmp = _tmp("r04bytev-r2-repeat-")
    path = _write_source(tmp / "source.sav", "sav")
    incidence = _decode(path, "sav", _sha(path))
    first = _cell_signature(incidence.iter_cells(4))
    second = _cell_signature(incidence.iter_cells(4))
    third = _cell_signature(incidence.iter_cells(3))
    incidence.close()
    return {"first_equals_second": first == second, "first_equals_third": first == third, "cells": len(first)}


if __name__ == "__main__":
    print(json.dumps({
        "binding_sav": reader_binding_and_pathname_replacement("sav"),
        "binding_dta": reader_binding_and_pathname_replacement("dta"),
        "in_place_before_lazy_sav": in_place_before_lazy("sav"),
        "in_place_before_lazy_dta": in_place_before_lazy("dta"),
        "between_batch_external_pwrite": between_batch_external_pwrite(),
        "truncate_and_close": truncate_and_close(),
        "dta_chunk_limitation_and_shape": dta_chunk_limitation_and_shape(),
        "sav_chunk_shape": sav_chunk_shape(),
        "posix_refusal": posix_refusal(),
        "mmap_residual": mmap_residual(),
        "mmap_between_batch": mmap_between_batch(),
        "mmap_before_metadata_verify": mmap_before_metadata_verify(),
        "cold_replay_sav": cold_replay("sav"),
        "cold_replay_dta": cold_replay("dta"),
        "repeated_reads": repeated_reads(),
    }, indent=2, sort_keys=True, default=str))
