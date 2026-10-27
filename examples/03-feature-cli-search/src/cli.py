"""Tiny notes CLI — ``add`` and ``list`` today; ``search`` is the feature task.

The module is deliberately small but shaped like real CLI code: pure
functions for the logic, a ``build_parser`` for wiring, and ``main`` as the
thin entry point. New subcommands should follow the same pattern.
"""

from __future__ import annotations

import argparse
import sys


def add_note(notes: list[str], text: str) -> list[str]:
    """Append *text* to *notes* and return the updated list."""
    notes.append(text)
    return notes


def list_notes(notes: list[str]) -> list[str]:
    """Return a copy of *notes* in storage order."""
    return list(notes)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="notes")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="append a note")
    p_add.add_argument("text")

    sub.add_parser("list", help="print all notes")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    notes: list[str] = []

    if args.command == "add":
        add_note(notes, args.text)
        print("saved")
    elif args.command == "list":
        for note in list_notes(notes):
            print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
