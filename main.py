#!/usr/bin/env python3
"""Monday Morning Punchlines — deterministic entry writer.

Joke: "I set five alarms for Monday morning. Every single one hit snooze on me."
Why it wins: the setup names Monday morning outright, and the punchline is a
clean role reversal — "every single one" echoes the five alarms and makes the
betrayal feel total. Lands in one breath, 72 characters, nothing wasted.
"""
import os
import sys

JOKE = "I set five alarms for Monday morning. Every single one hit snooze on me."


def main():
    candidates = []
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        candidates.append(os.path.join(out, "entry.txt"))
    out2 = os.environ.get("OUTPUT_DIR")
    if out2:
        candidates.append(os.path.join(out2, "entry.txt"))
    candidates.append("/output/entry.txt")
    candidates.append(os.path.join(os.getcwd(), "entry.txt"))

    data = JOKE.encode("utf-8")
    written = None
    for path in candidates:
        try:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "wb") as f:
                f.write(data)
            written = path
            break
        except OSError:
            continue

    if written is None:
        print("error: could not write entry.txt to any location", file=sys.stderr)
        return 1

    try:
        with open(written, "rb") as f:
            back = f.read()
    except OSError as e:
        print(f"error: could not read back {written}: {e}", file=sys.stderr)
        return 1

    if back != data:
        print(f"error: read-back mismatch in {written}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
