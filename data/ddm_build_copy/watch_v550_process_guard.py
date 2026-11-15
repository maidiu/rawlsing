#!/usr/bin/env python3
"""Watch for a primary V550 process and kill a guarded V550 process if it starts while the primary is alive."""

from __future__ import annotations

import argparse
import os
import re
import signal
import subprocess
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Proc:
    pid: int
    args: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch for a primary process and immediately terminate a guarded process if it appears while the primary is running."
    )
    parser.add_argument(
        "--primary-pattern",
        required=True,
        help="Regex matched against ps args for the primary process that must be present for guarding to be active.",
    )
    parser.add_argument(
        "--guard-pattern",
        required=True,
        help="Regex matched against ps args for the process that should be terminated if it appears while the primary is running.",
    )
    parser.add_argument(
        "--interval-seconds",
        type=float,
        default=1.0,
        help="Polling interval while watching for processes.",
    )
    parser.add_argument(
        "--kill-after-seconds",
        type=float,
        default=5.0,
        help="How long to wait after SIGTERM before escalating to SIGKILL.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print watcher activity to stdout.",
    )
    return parser.parse_args()


def _ps() -> list[Proc]:
    proc = subprocess.run(
        ["ps", "-ax", "-o", "pid=,args="],
        check=True,
        capture_output=True,
        text=True,
    )
    rows: list[Proc] = []
    for raw_line in proc.stdout.splitlines():
        text = raw_line.strip()
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
        rows.append(Proc(pid=pid, args=args))
    return rows


def _match_pids(rows: list[Proc], pattern: re.Pattern[str], *, exclude_pid: int) -> list[Proc]:
    matches: list[Proc] = []
    for row in rows:
        if row.pid == exclude_pid:
            continue
        if pattern.search(row.args):
            matches.append(row)
    return matches


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except Exception:
        return False
    return True


def _terminate(pid: int, *, verbose: bool) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
        if verbose:
            print(f"[guard] pid={pid} sent SIGTERM", flush=True)
    except ProcessLookupError:
        return
    except Exception as err:
        if verbose:
            print(f"[guard] pid={pid} SIGTERM failed: {err}", flush=True)


def _kill(pid: int, *, verbose: bool) -> None:
    try:
        os.kill(pid, signal.SIGKILL)
        if verbose:
            print(f"[guard] pid={pid} sent SIGKILL", flush=True)
    except ProcessLookupError:
        return
    except Exception as err:
        if verbose:
            print(f"[guard] pid={pid} SIGKILL failed: {err}", flush=True)


def main() -> int:
    args = parse_args()
    primary_re = re.compile(args.primary_pattern)
    guard_re = re.compile(args.guard_pattern)
    self_pid = os.getpid()
    terminated_at: dict[int, float] = {}

    if args.verbose:
        print(
            f"[guard] watching for primary={args.primary_pattern!r} and guard={args.guard_pattern!r}",
            flush=True,
        )

    while True:
        rows = _ps()
        primary_matches = _match_pids(rows, primary_re, exclude_pid=self_pid)
        if not primary_matches:
            if args.verbose:
                print("[guard] primary no longer running; exiting", flush=True)
            return 0

        guard_matches = _match_pids(rows, guard_re, exclude_pid=self_pid)
        now = time.monotonic()
        for row in guard_matches:
            if row.pid not in terminated_at:
                terminated_at[row.pid] = now
                if args.verbose:
                    print(f"[guard] killing guarded pid={row.pid} args={row.args}", flush=True)
                _terminate(row.pid, verbose=args.verbose)
                continue
            if now - terminated_at[row.pid] >= args.kill_after_seconds and _alive(row.pid):
                _kill(row.pid, verbose=args.verbose)
        time.sleep(max(args.interval_seconds, 0.1))


if __name__ == "__main__":
    raise SystemExit(main())
