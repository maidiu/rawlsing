#!/usr/bin/env python3
"""Launch V550 shard runs from a shard plan with bounded parallelism."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import selectors
import shlex
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_READINESS_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "readiness_checks"


@dataclass
class RunningShard:
    shard_id: str
    source: str
    wave: str
    log_path: Path
    process: subprocess.Popen[str]
    log_handle: TextIO | None = None
    stream: TextIO | None = None
    paused: bool = False
    pause_reason: str | None = None
    started_work: bool = False
    last_activity_at: float = 0.0
    last_heartbeat_at: float = 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run V550 shard commands from a shard plan with bounded parallelism.")
    parser.add_argument("--plan-dir", required=True, help="Path to the shard plan directory containing shard_plan.csv.")
    parser.add_argument(
        "--max-workers",
        default="auto",
        help="Maximum number of shard processes to run concurrently, or 'auto' to use the machine's CPU count capped by plan size.",
    )
    parser.add_argument("--adaptive", action=argparse.BooleanOptionalAction, default=True, help="Adapt concurrency to CPU and DB pressure.")
    parser.add_argument(
        "--cpu-high-water",
        type=float,
        default=0.95,
        help="Pause threshold as a fraction of shard CPU capacity (0.95 means 95%% of cpu_count * 100).",
    )
    parser.add_argument(
        "--cpu-low-water",
        type=float,
        default=0.80,
        help="Resume threshold as a fraction of shard CPU capacity (0.80 means 80%% of cpu_count * 100).",
    )
    parser.add_argument(
        "--memory-high-water",
        type=float,
        default=0.86,
        help="Pause threshold as a fraction of used system memory, sampled from macOS vm_stat.",
    )
    parser.add_argument(
        "--memory-low-water",
        type=float,
        default=0.76,
        help="Resume threshold as a fraction of used system memory, sampled from macOS vm_stat.",
    )
    parser.add_argument("--db-active-high-water", type=int, default=6, help="Pause/resume threshold for active Postgres sessions.")
    parser.add_argument("--db-active-low-water", type=int, default=3, help="Relax threshold for active Postgres sessions.")
    parser.add_argument("--db-waiting-high-water", type=int, default=1, help="Pause/resume threshold for waiting Postgres sessions.")
    parser.add_argument("--db-waiting-low-water", type=int, default=0, help="Relax threshold for waiting Postgres sessions.")
    parser.add_argument("--db-url", default=None, help="Optional Postgres URL for DB pressure sampling.")
    parser.add_argument("--env-file", default=str(ROOT / ".env"), help="Optional env file for DB URL lookup if --db-url is not provided.")
    parser.add_argument("--response-option-map", default=None, help="Optional response option map to append to each shard command.")
    parser.add_argument(
        "--shard-id",
        action="append",
        default=[],
        help="Only launch shards whose shard_id matches one of these values. May be repeated.",
    )
    parser.add_argument("--max-depth", type=int, default=None, help="Optional branching depth cap to forward to each shard worker.")
    parser.add_argument("--min-cell-n", type=int, default=None, help="Optional minimum cell size to forward to each shard worker.")
    parser.add_argument("--min-branch-n", type=int, default=None, help="Optional minimum branch size to forward to each shard worker.")
    parser.add_argument("--min-answer-n", type=int, default=None, help="Optional minimum answer size to forward to each shard worker.")
    parser.add_argument(
        "--full-readiness",
        action="store_true",
        default=False,
        help="Forward full readiness to each shard worker instead of the launch-ready shortcut.",
    )
    parser.add_argument(
        "--readiness-only",
        action="store_true",
        default=False,
        help="Forward readiness-only mode to each shard worker.",
    )
    parser.add_argument(
        "--readiness-artifact",
        default=None,
        help="Optional readiness artifact path to forward to each shard worker.",
    )
    parser.add_argument(
        "--readiness-output-root",
        default=None,
        help="Optional readiness output root to forward to each shard worker when running readiness-only.",
    )
    parser.add_argument(
        "--stop-after-stage",
        type=int,
        default=0,
        help="Forward a stop-after-stage request to each shard worker. Currently only stage 4 is supported.",
    )
    parser.add_argument(
        "--shared-respondent-substrate-mode",
        default="off",
        choices=("off", "write"),
        help="Forward shared respondent substrate mode to each shard worker.",
    )
    parser.add_argument(
        "--joint-configuration-registry-path",
        default=None,
        help="Forward a bounded V550J registry path to each shard worker.",
    )
    parser.add_argument(
        "--joint-configuration-id",
        action="append",
        default=[],
        help="Forward a selected joint configuration id to each shard worker. May be repeated.",
    )
    parser.add_argument(
        "--restart-incomplete",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Restart incomplete shards from scratch instead of skipping them. Completed shards are still skipped.",
    )
    parser.add_argument(
        "--write-csv",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Write CSV mirrors for each shard. Disable this to reduce disk usage substantially.",
    )
    parser.add_argument(
        "--write-parquet",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Write Parquet outputs for each shard.",
    )
    parser.add_argument("--resume", action="store_true", help="Append --resume to each shard command.")
    parser.add_argument(
        "--launch-stagger-seconds",
        type=float,
        default=20.0,
        help="Minimum time to wait between starting new shards.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the commands that would run without launching them.")
    parser.add_argument("--mirror-output", action="store_true", help="Mirror shard stdout/stderr to the terminal while logging to files.")
    parser.add_argument("--verbose", action="store_true", help="Print progress while launching and waiting for shards.")
    return parser.parse_args()


def _load_plan_rows(plan_csv: Path) -> list[dict[str, str]]:
    with plan_csv.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _parse_countries(raw: str | None) -> list[str]:
    if not raw:
        return []
    text = raw.strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        try:
            payload = json.loads(text)
            if isinstance(payload, list):
                return [str(item) for item in payload if str(item).strip()]
        except Exception:
            pass
    return [part.strip() for part in text.split("|") if part.strip()]


def _build_command(
    row: dict[str, str],
    *,
    response_option_map: str | None,
    max_depth: int | None,
    min_cell_n: int | None,
    min_branch_n: int | None,
    min_answer_n: int | None,
    full_readiness: bool,
    readiness_only: bool,
    readiness_artifact: str | None,
    readiness_output_root: str | None,
    stop_after_stage: int,
    shared_respondent_substrate_mode: str,
    joint_configuration_registry_path: str | None,
    joint_configuration_ids: list[str],
    resume: bool,
    overwrite_shard: bool,
    write_csv: bool,
    write_parquet: bool,
) -> list[str]:
    cmd = [
        sys.executable,
        str(ROOT / "data" / "ddm_build_copy" / "build_determinicity_wave_shard_v550.py"),
        "--run-id",
        str(row["run_id"]),
        "--shard-id",
        str(row["shard_id"]),
        "--source",
        str(row["source"]),
        "--wave",
        str(row["wave"]),
        "--verbose",
    ]
    canonical_wave = str(row.get("canonical_wave", "") or "").strip()
    if canonical_wave and canonical_wave != str(row["wave"]):
        cmd.extend(["--canonical-wave", canonical_wave])
    for country in _parse_countries(row.get("countries")):
        cmd.extend(["--country", country])
    if response_option_map and "--response-option-map" not in cmd:
        cmd.extend(["--response-option-map", response_option_map])
    if max_depth is not None:
        cmd.extend(["--max-depth", str(max_depth)])
    if min_cell_n is not None:
        cmd.extend(["--min-cell-n", str(min_cell_n)])
    if min_branch_n is not None:
        cmd.extend(["--min-branch-n", str(min_branch_n)])
    if min_answer_n is not None:
        cmd.extend(["--min-answer-n", str(min_answer_n)])
    if full_readiness:
        cmd.append("--full-readiness")
    if readiness_only:
        cmd.append("--readiness-only")
    if readiness_artifact:
        cmd.extend(["--readiness-artifact", readiness_artifact])
    if readiness_output_root:
        cmd.extend(["--readiness-output-root", readiness_output_root])
    if stop_after_stage > 0:
        cmd.extend(["--stop-after-stage", str(stop_after_stage)])
    if shared_respondent_substrate_mode != "off":
        cmd.extend(["--shared-respondent-substrate-mode", shared_respondent_substrate_mode])
        if "--v550-prepared-substrate-mode" not in cmd:
            cmd.extend(["--v550-prepared-substrate-mode", "country"])
    if joint_configuration_registry_path:
        cmd.extend(["--joint-configuration-registry-path", joint_configuration_registry_path])
    for joint_configuration_id in joint_configuration_ids:
        cmd.extend(["--joint-configuration-id", joint_configuration_id])
    if write_csv:
        cmd.append("--write-csv")
    else:
        cmd.append("--no-write-csv")
    if write_parquet:
        cmd.append("--write-parquet")
    else:
        cmd.append("--no-write-parquet")
    if resume and "--resume" not in cmd:
        cmd.append("--resume")
    if overwrite_shard and "--overwrite-shard" not in cmd:
        cmd.append("--overwrite-shard")
    return cmd


def _shard_is_complete(status: dict[str, object] | None) -> bool:
    if not status:
        return False
    # Treat only an explicit success as complete.
    # Older shard states may still have promotable=True even when the shard
    # was only partial; that should not cause the launcher to skip it.
    success_flag = status.get("success")
    if isinstance(success_flag, bool):
        return success_flag
    return str(status.get("status", "")).lower() == "success"


def _shard_status(status: dict[str, object] | None) -> str:
    if not status:
        return ""
    return str(status.get("status", "")).strip().lower()


def _load_existing_state(row: dict[str, str]) -> dict[str, object] | None:
    output_dir = row.get("output_dir")
    if not output_dir:
        return None
    shard_dir = Path(output_dir)
    status = _read_json(shard_dir / "shard_status.json")
    if status:
        return status
    manifest = _read_json(shard_dir / "shard_manifest.json")
    if manifest:
        return manifest
    return None


def _active_readiness_lock_for_shard(readiness_root: Path, shard_id: str) -> Path | None:
    if not readiness_root.exists():
        return None
    for run_dir in readiness_root.iterdir():
        if not run_dir.is_dir():
            continue
        candidate = run_dir / shard_id / "readiness.lock"
        if candidate.exists():
            return candidate
    return None


def _find_stale_shard_pids(row: dict[str, str]) -> list[int]:
    run_id = str(row.get("run_id", "")).strip()
    shard_id = str(row.get("shard_id", "")).strip()
    if not run_id or not shard_id:
        return []
    try:
        proc = subprocess.run(
            ["ps", "-ax", "-o", "pid=,args="],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return []
    matches: list[int] = []
    run_needle = f"--run-id {run_id}"
    shard_needle = f"--shard-id {shard_id}"
    script_needle = "build_determinicity_wave_shard_v550.py"
    for line in proc.stdout.splitlines():
        text = line.strip()
        if not text:
            continue
        parts = text.split(None, 1)
        if len(parts) != 2:
            continue
        pid_text, args = parts
        try:
            pid = int(pid_text)
        except ValueError:
            continue
        if script_needle in args and run_needle in args and shard_needle in args:
            matches.append(pid)
    return matches


def _kill_stale_shard_processes(row: dict[str, str], *, verbose: bool) -> None:
    pids = _find_stale_shard_pids(row)
    if not pids:
        return
    shard_id = str(row.get("shard_id", "unknown"))
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            if verbose:
                print(f"[kill] {shard_id} pid={pid} sent SIGTERM")
        except ProcessLookupError:
            continue
        except Exception as err:
            if verbose:
                print(f"[kill-failed] {shard_id} pid={pid}: {err}")
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline and any(_pid_alive(pid) for pid in pids):
        time.sleep(0.2)
    for pid in pids:
        if _pid_alive(pid):
            try:
                os.kill(pid, signal.SIGKILL)
                if verbose:
                    print(f"[kill] {shard_id} pid={pid} sent SIGKILL")
            except ProcessLookupError:
                continue
            except Exception as err:
                if verbose:
                    print(f"[kill-failed] {shard_id} pid={pid}: {err}")


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except Exception:
        return False
    return True


def _resolve_max_workers(value: str, shard_count: int) -> int:
    text = str(value).strip().lower()
    if text == "auto":
        cpu_count = os.cpu_count() or 1
        return max(1, min(cpu_count, shard_count))
    try:
        resolved = int(text)
    except ValueError as err:
        raise SystemExit(f"Invalid --max-workers value: {value!r}. Use an integer or 'auto'.") from err
    if resolved < 1:
        raise SystemExit("--max-workers must be at least 1")
    return resolved


def _launch(cmd: list[str], log_path: Path, *, mirror_output: bool) -> tuple[subprocess.Popen[str], TextIO | None, TextIO | None]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_handle = log_path.open("w", encoding="utf-8")
    if mirror_output:
        proc = subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        return proc, log_handle, proc.stdout
    return subprocess.Popen(cmd, cwd=ROOT, stdout=log_handle, stderr=subprocess.STDOUT, text=True), log_handle, None


def _tail_log(path: Path, max_lines: int = 1) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    return lines[-max_lines:]


def _sample_cpu_pressure(pids: list[int]) -> float:
    if not pids:
        return 0.0
    pid_args = [str(pid) for pid in pids if pid and pid > 0]
    if not pid_args:
        return 0.0
    try:
        proc = subprocess.run(
            ["ps", "-p", ",".join(pid_args), "-o", "%cpu="],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return 0.0
    total = 0.0
    for line in proc.stdout.splitlines():
        try:
            total += float(line.strip() or "0")
        except ValueError:
            continue
    return total


def _cpu_capacity() -> float:
    return float((os.cpu_count() or 1) * 100)


def _sample_memory_pressure() -> dict[str, float] | None:
    try:
        memsize_proc = subprocess.run(
            ["sysctl", "-n", "hw.memsize"],
            check=True,
            capture_output=True,
            text=True,
        )
        memsize = int(memsize_proc.stdout.strip())
        vm_stat_proc = subprocess.run(
            ["vm_stat"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None

    page_size = 4096
    header_match = re.search(r"page size of (\d+) bytes", vm_stat_proc.stdout)
    if header_match:
        try:
            page_size = int(header_match.group(1))
        except ValueError:
            page_size = 4096

    pages: dict[str, int] = {}
    for raw_line in vm_stat_proc.stdout.splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip().strip('"')
        digits = "".join(ch for ch in value if ch.isdigit())
        if not digits:
            continue
        try:
            pages[key] = int(digits)
        except ValueError:
            continue

    total_pages = max(1, memsize // max(1, page_size))
    free_pages = pages.get("Pages free", 0)
    inactive_pages = pages.get("Pages inactive", 0)
    speculative_pages = pages.get("Pages speculative", 0)
    purgeable_pages = pages.get("Pages purgeable", 0)
    wired_pages = pages.get("Pages wired down", 0)
    active_pages = pages.get("Pages active", 0)
    compressor_pages = (
        pages.get("Pages occupied by compressor", 0)
        or pages.get("Pages compressed", 0)
        or pages.get("Compressor page count", 0)
    )

    reclaimable_pages = free_pages + inactive_pages + speculative_pages + purgeable_pages
    reclaimable_pages = max(0, min(total_pages, reclaimable_pages))
    used_pages = max(0, total_pages - reclaimable_pages)

    return {
        "total_pages": float(total_pages),
        "page_size": float(page_size),
        "free_pages": float(free_pages),
        "inactive_pages": float(inactive_pages),
        "speculative_pages": float(speculative_pages),
        "purgeable_pages": float(purgeable_pages),
        "wired_pages": float(wired_pages),
        "active_pages": float(active_pages),
        "compressor_pages": float(compressor_pages),
        "reclaimable_pages": float(reclaimable_pages),
        "used_pages": float(used_pages),
        "used_ratio": used_pages / total_pages,
        "reclaimable_ratio": reclaimable_pages / total_pages,
        "used_gib": used_pages * page_size / (1024**3),
        "reclaimable_gib": reclaimable_pages * page_size / (1024**3),
    }


def _sample_db_pressure(db_url: str | None, env_file: str | None) -> dict[str, int] | None:
    if not db_url and env_file:
        try:
            from data.ddm_build_copy.ddm_v550_storage import load_env_database_url

            db_url = load_env_database_url(Path(env_file), None)
        except Exception:
            db_url = None
    if not db_url:
        return None
    try:
        from data.ddm_build_copy.ddm_v550_storage import try_connect_database

        conn, _ = try_connect_database(db_url)
        if conn is None:
            return None
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        COUNT(*) FILTER (WHERE state = 'active') AS active_count,
                        COUNT(*) FILTER (WHERE wait_event IS NOT NULL) AS waiting_count
                    FROM pg_stat_activity
                    WHERE datname = current_database()
                    """
                )
                row = cur.fetchone()
                if not row:
                    return None
                return {"active": int(row[0] or 0), "waiting": int(row[1] or 0)}
        finally:
            conn.close()
    except Exception:
        return None


def _pause_shard(shard: RunningShard, reason: str, *, verbose: bool) -> None:
    if shard.paused:
        shard.pause_reason = reason
        return
    try:
        shard.process.send_signal(signal.SIGSTOP)
        shard.paused = True
        shard.pause_reason = reason
        if verbose:
            print(f"[pause] {shard.shard_id} ({reason})")
    except Exception as err:
        if verbose:
            print(f"[pause-failed] {shard.shard_id}: {err}")


def _resume_shard(shard: RunningShard, *, verbose: bool) -> None:
    if not shard.paused:
        return
    try:
        shard.process.send_signal(signal.SIGCONT)
        shard.paused = False
        if verbose:
            print(f"[resume] {shard.shard_id}")
        shard.pause_reason = None
    except Exception as err:
        if verbose:
            print(f"[resume-failed] {shard.shard_id}: {err}")


def _stoppable_running(running: list[RunningShard]) -> list[RunningShard]:
    return [shard for shard in running if shard.process.poll() is None]


def _drain_output(selector: selectors.BaseSelector, *, verbose: bool) -> None:
    while True:
        events = selector.select(timeout=0)
        if not events:
            return
        for key, _ in events:
            shard: RunningShard = key.data
            stream = shard.stream
            if stream is None:
                continue
            line = stream.readline()
            if line == "":
                try:
                    selector.unregister(stream)
                except Exception:
                    pass
                try:
                    stream.close()
                except Exception:
                    pass
                shard.stream = None
                continue
            if shard.log_handle is not None:
                shard.log_handle.write(line)
                shard.log_handle.flush()
            if verbose:
                sys.stdout.write(line)
                sys.stdout.flush()
            shard.last_activity_at = time.monotonic()
            if (
                "processing questions" in line
                or "question " in line and "completed=" in line
                or "question 1/" in line
            ):
                shard.started_work = True


def _manage_pressure(
    running: list[RunningShard],
    pending: list[tuple[dict[str, str], list[str]]],
    paused: list[RunningShard],
    *,
    args: argparse.Namespace,
) -> tuple[list[RunningShard], list[RunningShard]]:
    if not args.adaptive:
        return running, paused

    cpu = _sample_cpu_pressure([shard.process.pid for shard in running])
    cpu_capacity = _cpu_capacity()
    memory = _sample_memory_pressure()
    memory_used_ratio = memory["used_ratio"] if memory else 0.0
    memory_used_gib = memory["used_gib"] if memory else 0.0
    memory_total_gib = ((memory["total_pages"] * memory["page_size"]) / (1024**3)) if memory else 0.0
    db = _sample_db_pressure(args.db_url, args.env_file)
    active_db = db["active"] if db else 0
    waiting_db = db["waiting"] if db else 0

    high_pressure = (
        (cpu_capacity > 0 and cpu / cpu_capacity >= args.cpu_high_water)
        or (memory is not None and memory_used_ratio >= args.memory_high_water)
        or active_db >= args.db_active_high_water
        or waiting_db >= args.db_waiting_high_water
    )
    low_pressure = (
        (cpu_capacity <= 0 or cpu / cpu_capacity <= args.cpu_low_water)
        and (memory is None or memory_used_ratio <= args.memory_low_water)
        and active_db <= args.db_active_low_water
        and waiting_db <= args.db_waiting_low_water
    )

    if args.verbose and db is not None:
        print(
            f"[pressure] shard_cpu={cpu:.1f}/{cpu_capacity:.0f} "
            f"mem_used={memory_used_gib:.1f}/{memory_total_gib:.1f}GiB "
            f"db_active={active_db} db_waiting={waiting_db} running={len(running)} paused={len(paused)} pending={len(pending)}"
        )
    elif args.verbose and memory is not None:
        print(
            f"[pressure] shard_cpu={cpu:.1f}/{cpu_capacity:.0f} "
            f"mem_used={memory_used_gib:.1f}/{memory_total_gib:.1f}GiB "
            f"running={len(running)} paused={len(paused)} pending={len(pending)}"
        )
    elif args.verbose:
        print(f"[pressure] shard_cpu={cpu:.1f}/{cpu_capacity:.0f} running={len(running)} paused={len(paused)} pending={len(pending)}")

    running = _stoppable_running(running)
    paused = _stoppable_running(paused)

    if high_pressure and len(running) > 1:
        # Pause the newest runnable shard first so we keep at least one worker moving.
        candidate = next((shard for shard in reversed(running) if not shard.paused), None)
        if candidate is not None:
            reason_parts = [f"shard_cpu={cpu:.1f}/{cpu_capacity:.0f}"]
            if memory is not None:
                reason_parts.append(f"mem_used={memory_used_gib:.1f}/{memory_total_gib:.1f}GiB")
            reason_parts.append(f"db_active={active_db}")
            reason_parts.append(f"db_waiting={waiting_db}")
            reason = ",".join(reason_parts)
            _pause_shard(candidate, reason, verbose=args.verbose)
            if candidate not in paused:
                paused.append(candidate)
        return running, paused

    if low_pressure and paused:
        # Resume one paused shard at a time to avoid bursty pressure.
        candidate = paused.pop(0)
        _resume_shard(candidate, verbose=args.verbose)
        return running, paused

    return running, paused


def _emit_heartbeat(
    running: list[RunningShard],
    pending_count: int,
    paused_count: int,
    *,
    verbose: bool,
) -> None:
    if not verbose:
        return
    now = time.monotonic()
    for shard in running:
        if now - shard.last_heartbeat_at < 30.0:
            continue
        shard.last_heartbeat_at = now
        latest = _tail_log(shard.log_path, max_lines=1)
        latest_text = latest[-1] if latest else "(no log output yet)"
        status_bits = [
            f"pid={shard.process.pid}",
            f"paused={'yes' if shard.paused else 'no'}",
        ]
        if shard.started_work:
            status_bits.append("started_work=yes")
        if shard.last_activity_at:
            status_bits.append(f"last_activity={now - shard.last_activity_at:0.0f}s")
        print(
            f"[heartbeat] {shard.shard_id} {' '.join(status_bits)} pending={pending_count} paused={paused_count} log={latest_text}",
            flush=True,
        )


def main() -> int:
    args = parse_args()
    plan_dir = Path(args.plan_dir)
    plan_csv = plan_dir / "shard_plan.csv"
    if not plan_csv.exists():
        raise SystemExit(f"Missing shard plan CSV: {plan_csv}")

    rows = [row for row in _load_plan_rows(plan_csv) if str(row.get("skip_by_default", "")).lower() != "true"]
    if args.shard_id:
        requested = {str(value).strip() for value in args.shard_id if str(value).strip()}
        rows = [row for row in rows if str(row.get("shard_id", "")).strip() in requested]
    if not rows:
        print("No runnable shards found in plan.")
        return 0

    commands: list[tuple[dict[str, str], list[str]]] = []
    skipped_completed = 0
    skipped_running = 0
    restarted_incomplete = 0
    for row in rows:
        existing_state = _load_existing_state(row)
        if _shard_is_complete(existing_state):
            skipped_completed += 1
            if args.verbose:
                print(f"[skip] {row.get('shard_id', '')} already completed")
            continue
        existing_status = _shard_status(existing_state)
        should_resume = args.resume and existing_state is not None and not _shard_is_complete(existing_state)
        should_overwrite = bool(existing_state is not None and not _shard_is_complete(existing_state) and args.restart_incomplete and not should_resume)
        if existing_status == "running" and args.restart_incomplete:
            _kill_stale_shard_processes(row, verbose=args.verbose)
        elif existing_status == "running" and not args.restart_incomplete and not should_resume:
            skipped_running += 1
            if args.verbose:
                print(f"[skip] {row.get('shard_id', '')} already running")
            continue
        active_lock = _active_readiness_lock_for_shard(DEFAULT_READINESS_ROOT, str(row.get("shard_id", "")).strip())
        if active_lock is not None:
            skipped_running += 1
            if args.verbose:
                print(f"[skip] {row.get('shard_id', '')} blocked by active readiness lock: {active_lock}")
            continue
        if should_overwrite:
            restarted_incomplete += 1
            if args.verbose:
                print(f"[restart] {row.get('shard_id', '')} clearing incomplete state ({existing_status or 'unknown'})")
        cmd = _build_command(
            row,
            response_option_map=args.response_option_map,
            max_depth=args.max_depth,
            min_cell_n=args.min_cell_n,
            min_branch_n=args.min_branch_n,
            min_answer_n=args.min_answer_n,
            full_readiness=args.full_readiness,
            readiness_only=args.readiness_only,
            readiness_artifact=args.readiness_artifact,
            readiness_output_root=args.readiness_output_root,
            stop_after_stage=args.stop_after_stage,
            shared_respondent_substrate_mode=args.shared_respondent_substrate_mode,
            joint_configuration_registry_path=args.joint_configuration_registry_path,
            joint_configuration_ids=args.joint_configuration_id,
            resume=should_resume,
            overwrite_shard=should_overwrite,
            write_csv=args.write_csv,
            write_parquet=args.write_parquet,
        )
        commands.append((row, cmd))

    resolved_max_workers = _resolve_max_workers(args.max_workers, len(commands))

    if args.dry_run:
        print(f"# resolved_max_workers={resolved_max_workers}")
        print(f"# skipped_completed={skipped_completed}")
        print(f"# skipped_running={skipped_running}")
        print(f"# restarted_incomplete={restarted_incomplete}")
        for row, cmd in commands:
            print(f"{row.get('shard_id', '')}: {' '.join(shlex.quote(part) for part in cmd)}")
        return 0

    logs_root = plan_dir / "logs"
    logs_root.mkdir(parents=True, exist_ok=True)
    selector = selectors.DefaultSelector()
    running: list[RunningShard] = []
    paused: list[RunningShard] = []
    pending = commands[:]
    completed_ok = 0
    completed_failed = 0
    last_launch_at = 0.0
    seeded_launch = False

    while pending or running:
        _drain_output(selector, verbose=args.verbose)
        running, paused = _manage_pressure(running, pending, paused, args=args)
        _emit_heartbeat(running, len(pending), len(paused), verbose=args.verbose)
        while pending and len(running) < resolved_max_workers:
            if running and time.monotonic() - last_launch_at < args.launch_stagger_seconds:
                break
            if args.adaptive:
                if not seeded_launch and running:
                    break
                if running and not any(shard.started_work for shard in running):
                    break
                cpu = _sample_cpu_pressure([shard.process.pid for shard in running])
                cpu_capacity = _cpu_capacity()
                memory = _sample_memory_pressure()
                memory_used_ratio = memory["used_ratio"] if memory else 0.0
                db = _sample_db_pressure(args.db_url, args.env_file)
                active_db = db["active"] if db else 0
                waiting_db = db["waiting"] if db else 0
                if (
                    (cpu_capacity > 0 and cpu / cpu_capacity >= args.cpu_high_water)
                    or (memory is not None and memory_used_ratio >= args.memory_high_water)
                    or active_db >= args.db_active_high_water
                    or waiting_db >= args.db_waiting_high_water
                ):
                    break
            row, cmd = pending.pop(0)
            shard_id = str(row.get("shard_id", "unknown"))
            source = str(row.get("source", "unknown"))
            wave = str(row.get("wave", "unknown"))
            log_path = logs_root / f"{shard_id}.log"
            if args.verbose:
                print(f"[launch] {shard_id} -> {log_path}")
            proc, log_handle, stream = _launch(cmd, log_path, mirror_output=args.mirror_output)
            shard = RunningShard(
                shard_id=shard_id,
                source=source,
                wave=wave,
                log_path=log_path,
                process=proc,
                log_handle=log_handle,
                stream=stream,
            )
            if stream is not None:
                selector.register(stream, selectors.EVENT_READ, shard)
            running.append(shard)
            last_launch_at = time.monotonic()
            seeded_launch = True
            if args.adaptive and not any(shard.started_work for shard in running):
                break

        if not running:
            time.sleep(0.5)
            continue

        still_running: list[RunningShard] = []
        for shard in running:
            rc = shard.process.poll()
            if rc is None:
                still_running.append(shard)
                continue
            if rc == 0:
                completed_ok += 1
                if args.verbose:
                    print(f"[done] {shard.shard_id}")
            else:
                completed_failed += 1
                print(f"[fail] {shard.shard_id} exited {rc}; see {shard.log_path}", file=sys.stderr)
                if shard in paused:
                    paused = [p for p in paused if p.process.pid != shard.process.pid]
            if shard.stream is not None:
                try:
                    selector.unregister(shard.stream)
                except Exception:
                    pass
                try:
                    shard.stream.close()
                except Exception:
                    pass
                shard.stream = None
            if shard.log_handle is not None:
                try:
                    shard.log_handle.close()
                except Exception:
                    pass
        running = still_running
        paused = _stoppable_running(paused)
        if running or pending:
            time.sleep(1.0)

    _drain_output(selector, verbose=args.verbose)
    print(
        f"Shard launcher finished: ok={completed_ok} failed={completed_failed} skipped_completed={skipped_completed} skipped_running={skipped_running} restarted_incomplete={restarted_incomplete} total={completed_ok + completed_failed + skipped_completed + skipped_running}"
    )
    return 0 if completed_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
