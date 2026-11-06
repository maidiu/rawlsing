"""Thin CLI over the bounded S45-to-WP19 projection contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapter import S45Projection
from .runtime import install_package_closure


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def _render_text(view: dict) -> str:
    try:
        from wp19.interface import render_text as wp19_render_text

        return wp19_render_text(view)
    except Exception:
        lines = [
            "Mode: " + str(view.get("mode", "")),
            "Clock: " + str(view.get("clock", "")),
            "Location: " + str(view.get("location", "") or "UNKNOWN"),
        ]
        for event in view.get("visible_events") or []:
            lines.append(
                "- " + str(event.get("kind", "")) + " at "
                + str(event.get("clock", "")) + ": "
                + str(event.get("summary", ""))
            )
        for speech in view.get("visible_speech") or []:
            if speech.get("text"):
                lines.append(
                    "- SAY: " + str(speech["text"])
                    + (" [" + str(speech.get("gesture")) + "]"
                       if speech.get("gesture") else "")
                )
        for item in view.get("accessibility_announcement") or []:
            lines.append("Announcement: " + str(item))
        lines.append("Exit: " + str(view.get("exit_control", {}).get("label")))
        lines.append("Return: " + str(view.get("return_control", {}).get("reason")))
        return "\n".join(lines)


def _open(args):
    root = Path(args.root)
    if args.start:
        return S45Projection.start(root, seed=args.seed)
    if not (root / "session.json").is_file():
        raise FileNotFoundError("S45_SESSION_NOT_FOUND:" + str(root))
    return S45Projection.open(root)


def main(argv: list[str] | None = None) -> int:
    install_package_closure()
    parser = argparse.ArgumentParser(
        description="Bounded S45 encounter projection over the WP19 surface"
    )
    parser.add_argument("--root", required=True)
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--seed", default="01" * 32)
    sub = parser.add_subparsers(dest="command", required=True)
    view = sub.add_parser("view")
    view.add_argument("--text", action="store_true")
    sub.add_parser("status")
    sub.add_parser("demo")
    sub.add_parser("wait")
    sub.add_parser("exit")
    sub.add_parser("return")
    sub.add_parser("absence")
    sub.add_parser("attend")
    say = sub.add_parser("say")
    say.add_argument("text")
    do = sub.add_parser("do-help", aliases=["do"])
    do.add_argument("intent", nargs="?", default="help")
    args = parser.parse_args(argv)
    adapter = _open(args)
    try:
        if args.command == "view":
            value = adapter.view()
            if args.text:
                print(_render_text(value))
            else:
                _print(value)
        elif args.command == "status":
            _print(adapter.status())
        elif args.command == "say":
            _print(adapter.say(args.text))
        elif args.command in {"do-help", "do"}:
            _print(adapter.do_help())
        elif args.command == "attend":
            _print(adapter.attend())
        elif args.command == "wait":
            _print(adapter.wait())
        elif args.command == "exit":
            _print(adapter.exit())
        elif args.command == "return":
            _print(adapter.return_())
        elif args.command == "absence":
            _print(adapter.absence())
        elif args.command == "demo":
            _print({
                "view": adapter.view(),
                "say": adapter.say("Can I help?"),
                "do_help": adapter.do_help(),
                "attend": adapter.attend(),
                "exit": adapter.exit(),
                "wait": adapter.wait(),
                "return": adapter.return_(),
                "absence": adapter.absence(),
                "status": adapter.status(),
            })
    finally:
        adapter.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
