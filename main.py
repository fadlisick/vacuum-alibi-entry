#!/usr/bin/env python3
"""Vacuum alibi: one deadpan excuse, written out for the judge.

The Vacuum's Alibi (make.fun): the program's only job is to put a single
robot-vacuum excuse, at most 200 characters, into the entry file the
scorer reads. The joke is the payload; everything else is plumbing.
"""

import os
import sys

EXCUSE = "My lidar flagged the dust as load-bearing. I am not the vacuum that brings this house down."

LIMIT = 200


def validate_line(line):
    """Refuse anything the gate would refuse, before writing it."""
    stripped = line.strip()
    if not stripped:
        raise SystemExit("excuse is blank")
    if stripped != line:
        raise SystemExit("excuse has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit("excuse must fit on one line")
    if len(line) > LIMIT:
        raise SystemExit("excuse is over 200 characters")
    return line


def resolve_output():
    """Where the scorer looks, honouring the harness override."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "entry.txt")


def emit():
    line = validate_line(EXCUSE)
    target = resolve_output()
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    os.chmod(target, 0o644)
    with open(target, encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        raise SystemExit("written entry does not match the excuse")
    with open(target, "rb") as handle:
        raw = handle.read()
    if raw != line.encode("utf-8"):
        raise SystemExit("written bytes do not match the excuse")
    print(line)


if __name__ == "__main__":
    emit()
