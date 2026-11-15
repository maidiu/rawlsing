#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PRODUCT = Path(__file__).resolve().parent
sys.path.insert(0, str(PRODUCT))

from sorok_s45_s47.bootstrap import WORKER_RETURNS, install

install()

import pytest

SUITES = (
    WORKER_RETURNS / "SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1" / "tests",
    WORKER_RETURNS / "SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1" / "tests",
    WORKER_RETURNS / "SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1" / "tests",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--junitxml", default=None)
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()
    argv = [str(path) for path in SUITES]
    if args.junitxml:
        argv.append("--junitxml=" + args.junitxml)
    if args.quiet:
        argv.append("-q")
    return int(pytest.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
