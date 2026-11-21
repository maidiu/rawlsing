"""Print measured peak process-tree RSS for an exact S1-C sourcefree pytest run.

This wrapper measures the hosted fixture run, not original35 production.
It does not alter the source reader, permission, cache or test environment.
"""
from __future__ import annotations

import subprocess
import sys
from time import monotonic, sleep

import psutil


def main(argv: list[str]) -> int:
    cmd = [
        sys.executable, "-B", "-m", "pytest",
        "-q", "-s", "-o", "addopts=", "-p", "no:cacheprovider", *argv,
    ]
    started = monotonic()
    child = subprocess.Popen(cmd)
    peak_rss = 0
    observed = 0
    try:
        while child.poll() is None:
            try:
                root = psutil.Process(child.pid)
                processes = [root, *root.children(recursive=True)]
                rss = sum(
                    p.memory_info().rss for p in processes if p.is_running()
                )
                observed += 1
                peak_rss = max(peak_rss, rss)
            except (psutil.Error, OSError):
                pass
            sleep(0.02)
        return child.wait()
    finally:
        print(
            "S1C_MEASURED_PROCESS_TREE",
            {
                "peak_rss_bytes": peak_rss,
                "samples": observed,
                "elapsed_wall_seconds": round(monotonic() - started, 4),
                "scope": "GITHUB_HOSTED_SOURCEFREE_FIXTURE_NOT_ORIGINAL35",
            },
            flush=True,
        )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
