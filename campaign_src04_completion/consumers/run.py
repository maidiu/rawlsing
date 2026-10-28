"""CLI for the bounded SRC04 lane-D consumer bridge."""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

from .consumer import (
    ConsumerRefusal,
    ProducerBundle,
    consume_native_producer,
    consume_retained_b0_fixture,
    refuse_d1_tally,
)

ROOT = Path(__file__).resolve().parents[2]


def _write(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def _load_producer(spec: str) -> ProducerBundle:
    if ":" not in spec:
        raise ConsumerRefusal("PRODUCER_MODULE_SPEC_INVALID", "expected module:function")
    module_name, function_name = spec.split(":", 1)
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        raise ConsumerRefusal("PRODUCER_MODULE_UNAVAILABLE", f"{module_name}: {exc}") from exc
    function = getattr(module, function_name, None)
    if not callable(function):
        raise ConsumerRefusal("PRODUCER_FUNCTION_MISSING", spec)
    bundle = function()
    if not isinstance(bundle, ProducerBundle):
        raise ConsumerRefusal("PRODUCER_BUNDLE_REQUIRED", f"{spec} returned {type(bundle).__name__}")
    return bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_b0 = sub.add_parser("b0-fixture", help="consume the retained B0 nonrespondent fixture fact")
    p_b0.add_argument("--receipt", default=str(Path(__file__).resolve().parent / "evidence/B0_FIXTURE_POSITIVE.json"))
    p_b0.add_argument("--claim-ceiling", default="SUPPORTED_COMPONENT_ONLY")
    p_b0.add_argument("--use-scope", default="SUPPORTED_COMPONENT_ONLY")
    p_b0.add_argument("--out", required=True)

    p_native = sub.add_parser("native", help="consume a full source-local producer bundle")
    p_native.add_argument("--producer-module", default=None, help="module:function returning ProducerBundle")
    p_native.add_argument("--expected-source-id", default="SRC04")
    p_native.add_argument("--claim-ceiling", default="SOURCE_LOCAL_STATISTIC")
    p_native.add_argument("--use-scope", default="SOURCE_LOCAL_STATISTIC")
    p_native.add_argument("--out", required=True)

    p_d1 = sub.add_parser("refuse-d1-tally", help="prove the D1 tally is not accepted as EmpiricalFact")
    p_d1.add_argument("--tally", default=str(Path(__file__).resolve().parent / "evidence/D1_TALLY_REF.json"))
    p_d1.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    out = Path(args.out)
    try:
        if args.command == "b0-fixture":
            document = consume_retained_b0_fixture(
                args.receipt,
                requested_claim_ceiling=args.claim_ceiling,
                use_scope=args.use_scope,
            )
            _write(out, document)
            print(json.dumps({"status": document["status"], "out": str(out)}, indent=2))
            return 0
        if args.command == "native":
            try:
                if not args.producer_module:
                    raise ConsumerRefusal(
                        "FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED",
                        "no full SRC04 source-local producer module supplied",
                    )
                bundle = _load_producer(args.producer_module)
            except ConsumerRefusal as exc:
                blocker = {
                    "schema": "PYAT_SRC04_LANE_D_BLOCKER@1.0.0",
                    "status": "BLOCKED",
                    "blocker": exc.code,
                    "detail": exc.detail,
                    "required_producer": "full source-local SRC04 C11 release + EmpiricalQuerySpec + EmpiricalPredicate + EmpiricalFact + exact authority refs",
                    "producer_contract": "campaign_src04_completion/consumers/PRODUCER_CONTRACT.json",
                    "source_read_performed": False,
                    "original_workload_issued": False,
                }
                _write(out, blocker)
                print(json.dumps(blocker, indent=2))
                return 2
            document = consume_native_producer(
                bundle,
                expected_source_id=args.expected_source_id,
                requested_claim_ceiling=args.claim_ceiling,
                use_scope=args.use_scope,
            )
            _write(out, document)
            print(json.dumps({"status": document["status"], "out": str(out)}, indent=2))
            return 0
        if args.command == "refuse-d1-tally":
            document = refuse_d1_tally(args.tally)
            _write(out, document)
            print(json.dumps({"status": document["status"], "code": document["error_code"], "out": str(out)}, indent=2))
            return 0
    except ConsumerRefusal as exc:
        refusal = {
            "schema": "PYAT_SRC04_LANE_D_NEGATIVE@1.0.0",
            "status": "REFUSED",
            "error_type": type(exc).__name__,
            "error_code": exc.code,
            "detail": exc.detail,
            "out": str(out),
            "source_read_performed": False,
            "original_workload_issued": False,
        }
        _write(out, refusal)
        print(json.dumps(refusal, indent=2))
        return 1
    parser.error("unhandled command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
