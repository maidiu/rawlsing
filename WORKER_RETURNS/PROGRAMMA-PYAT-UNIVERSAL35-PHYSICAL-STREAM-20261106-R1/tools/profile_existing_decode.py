"""Bounded local profile of the frozen original-source decode/C11 path."""
from __future__ import annotations

import argparse
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rawlsing_next.pre553_original35_physical_stream import bounded_physical_cell_stream
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.source_configuration.factory import (
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.reader import reader_configuration_from_config


def rss_bytes():
    try:
        value = subprocess.check_output(
            ["ps", "-o", "rss=", "-p", str(os.getpid())], text=True,
        ).strip()
        return int(value) * 1024
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def usage():
    u = shutil.disk_usage(REPO_ROOT)
    return {"total": u.total, "used": u.used, "free": u.free}


def run(source_id, mode, batch_size, binding_path, outdir, native_max_items=0):
    binding = json.loads(binding_path.read_text())
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(source_root=root)
    config = library.load_original(source_id)
    resolution = library.resolve_source_path(source_id)
    if resolution["status"] != "RESOLVED_UNDER_EFFECTIVE_ROOT":
        raise RuntimeError("source path not resolved: " + resolution["status"])
    path = resolution["resolved_source_path"]
    reader = reader_configuration_from_config(config)
    before = {
        "wall": time.perf_counter(), "cpu": time.process_time(),
        "rss": rss_bytes(), "maxrss": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "disk": usage(),
    }
    incidence = decode_sav(
        path, encoding=reader.encoding,
        expected_source_sha256=config.original_source_sha256,
    )
    decode_end = {
        "wall": time.perf_counter(), "cpu": time.process_time(),
        "rss": rss_bytes(), "maxrss": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "disk": usage(),
    }
    payload = {
        "schema": "PYAT_UNIVERSAL35_PHYSICAL_STREAM_PROFILE@1",
        "source_id": source_id,
        "mode": mode,
        "batch_size": batch_size,
        "scope": "LOWER_LEVEL_LOCAL_PHYSICAL_PROFILE_NOT_NATIVE_OR_SCIENTIFIC_ISSUANCE",
        "host": platform.node(),
        "platform": platform.platform(),
        "python": sys.version,
        "config": {
            "source_sha256": config.original_source_sha256,
            "row_count": config.active_row_count,
            "physical_slots": len(config.document.get("physical_slots", ())),
            "response_slots": len(config.document.get("response_slots", ())),
            "coordinate_slots": len(config.document.get("coordinate_slots", ())),
            "weight_slots": len(config.document.get("weight_slots", ())),
            "source_format": config.document["identity"]["source_format"],
            "reader_encoding": reader.encoding,
        },
        "resolution": {k: resolution[k] for k in (
            "status", "relative_path", "expected_source_sha256", "source_root_source",
        )},
        "source_bytes": Path(path).stat().st_size,
        "decode": {
            "wall_s": decode_end["wall"] - before["wall"],
            "cpu_s": decode_end["cpu"] - before["cpu"],
            "rss_before": before["rss"], "rss_after": decode_end["rss"],
            "maxrss_before": before["maxrss"], "maxrss_after": decode_end["maxrss"],
            "disk_before": before["disk"], "disk_after": decode_end["disk"],
            "incidence_rows": incidence.row_count,
            "incidence_variables": len(incidence.variables),
            "physical_metadata_digest": incidence.physical_metadata_digest,
            "source_custody": incidence.source_custody,
        },
    }
    if mode == "decode":
        payload["result"] = {"state": "DECODE_ONLY_OK"}
    elif mode == "materialize":
        start = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes()}
        cells = tuple(incidence.iter_cells(batch_size))
        end = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes(),
               "maxrss": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)}
        payload["materialize"] = {
            "cell_count": len(cells),
            "wall_s": end["wall"] - start["wall"],
            "cpu_s": end["cpu"] - start["cpu"],
            "rss_before": start["rss"], "rss_after": end["rss"],
            "maxrss_after": end["maxrss"],
        }
        payload["result"] = {"state": "MATERIALIZE_OK"}
    elif mode == "build":
        start = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes()}
        release = build_validated_c11_release_from_config(
            config, incidence=incidence, batch_size=batch_size,
        )
        end = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes(),
               "maxrss": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)}
        payload["build"] = {
            "wall_s": end["wall"] - start["wall"], "cpu_s": end["cpu"] - start["cpu"],
            "rss_before": start["rss"], "rss_after": end["rss"],
            "maxrss_after": end["maxrss"],
            "release_ref": release.release_ref.as_dict(),
            "replay_ref": release.replay_manifest.ref.as_dict(),
            "public_object_count": len(release.public_objects),
            "internal_record_count": len(release.internal_records),
        }
        payload["result"] = {"state": "BUILD_OK"}
    elif mode in ("stream", "filtered", "d_filtered"):
        selected = None
        if mode in ("filtered", "d_filtered"):
            if native_max_items:
                doc = config.document
                routing = {row["question_id"]: row for row in doc.get("routing", ())}
                qualified = []
                for slot in doc.get("response_slots", ()):
                    name = slot["slot"]["name"]
                    if routing.get(name, {}).get("typed_state") != "ELIGIBLE_APPLICABLE":
                        continue
                    values = [
                        value for value in slot.get("values", ())
                        if value.get("response_state") == "SUBSTANTIVE_RESPONSE"
                        and value.get("canonical_value") is not None
                    ]
                    if values:
                        qualified.append(name)
                qualified = qualified[:native_max_items]
                coordinate = next(
                    (slot["slot"]["name"] for slot in doc.get("coordinate_slots", ())
                     if slot["slot"]["name"] not in set(qualified)),
                    None,
                )
                if coordinate is None:
                    coordinate = next(
                        (slot["name"] for slot in doc.get("physical_slots", ())
                         if slot["name"] not in set(qualified)),
                        None,
                    )
                if not qualified or coordinate is None:
                    raise RuntimeError("native selection is incomplete")
                selected = tuple(qualified) + (coordinate,)
            else:
                selected = tuple(
                    slot["slot"]["name"] for slot in config.document.get("response_slots", ())[:3]
                ) + tuple(
                    slot["slot"]["name"] for slot in config.document.get("coordinate_slots", ())[:1]
                )
            if not selected:
                raise RuntimeError("filtered mode requires configured response/coordinate slots")
        if mode == "d_filtered":
            selected_set = set(selected)
            def cell_iter():
                for cell in incidence.iter_cells():
                    if cell.variable_name in selected_set:
                        yield cell
            transport = "D_CURRENT_FILTERED_GENERATOR"
            digest = incidence.physical_metadata_digest
        else:
            stream = bounded_physical_cell_stream(
                incidence, batch_size=batch_size, include_variables=selected,
            )
            cell_iter = stream.iter_cells
            transport = stream.transport_identity
            digest = stream.decoder_metadata_digest
        passes = []
        for number in (1, 2):
            start = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes()}
            count = 0
            first = last = None
            for cell in cell_iter():
                if first is None:
                    first = [cell.row_ordinal, cell.variable_ordinal, cell.variable_name]
                last = [cell.row_ordinal, cell.variable_ordinal, cell.variable_name]
                count += 1
            end = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes(),
                   "maxrss": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)}
            passes.append({
                "pass": number, "cell_count": count, "first": first, "last": last,
                "wall_s": end["wall"] - start["wall"], "cpu_s": end["cpu"] - start["cpu"],
                "rss_before": start["rss"], "rss_after": end["rss"],
                "maxrss_after": end["maxrss"],
            })
        payload["stream"] = {
            "transport_identity": transport,
            "decoder_metadata_digest": digest,
            "selected_columns": list(selected) if selected is not None else None,
            "passes": passes,
        }
        payload["result"] = {"state": "D_FILTERED_SCAN_OK" if mode == "d_filtered" else ("FILTERED_STREAM_SCAN_OK" if selected else "STREAM_SCAN_OK")}
    elif mode == "repository":
        start = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes()}
        repository, release = build_source_backed_c11_repository_from_config(
            config, incidence, batch_size=batch_size,
        )
        end = {"wall": time.perf_counter(), "cpu": time.process_time(), "rss": rss_bytes(),
               "maxrss": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)}
        payload["repository"] = {
            "wall_s": end["wall"] - start["wall"], "cpu_s": end["cpu"] - start["cpu"],
            "rss_before": start["rss"], "rss_after": end["rss"],
            "maxrss_after": end["maxrss"],
            "release_ref": release.release_ref.as_dict(),
            "repository_count": len(repository),
        }
        payload["result"] = {"state": "REPOSITORY_OK"}
    else:
        raise ValueError("unknown mode")
    incidence.close()
    outdir.mkdir(parents=True, exist_ok=True)
    path_out = outdir / f"{source_id}_{mode}.json"
    path_out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "path": str(path_out), "source_id": source_id, "mode": mode,
        "source_bytes": payload["source_bytes"],
        "decode_wall_s": payload["decode"]["wall_s"],
        "decode_peak_rss": payload["decode"]["maxrss_after"],
        "result": payload["result"],
        "build": payload.get("build"),
        "materialize": payload.get("materialize"),
    }, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--mode", required=True, choices=("decode", "materialize", "stream", "filtered", "d_filtered", "build", "repository"))
    parser.add_argument("--batch-size", type=int, default=10000)
    parser.add_argument("--binding", default=str(REPO_ROOT / ".local-logs/pyat-universal35/source-runtime-binding.local.json"))
    parser.add_argument("--outdir", default=str(REPO_ROOT / ".local-logs/pyat-universal35/physical-stream/results"))
    parser.add_argument("--tmpdir", default=str(REPO_ROOT / ".local-logs/pyat-universal35/physical-stream/tmp"))
    parser.add_argument("--native-max-items", type=int, default=0)
    args = parser.parse_args()
    Path(args.tmpdir).mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = args.tmpdir
    run(args.source_id, args.mode, args.batch_size, Path(args.binding), Path(args.outdir), args.native_max_items)


if __name__ == "__main__":
    main()
