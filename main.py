#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog.

Writes one patch-note line -- a software changelog entry for a bug in
real life / human biology, in the terse register of a real release note --
to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

The line is fixed and deterministic: the same bytes on every run, no
network, no clock, no randomness. It is 1-160 characters, a single line
of UTF-8 text, as the bounty gate requires.
"""

import os
from pathlib import Path

# v2.6.0: the brain's storage tiers are badly tuned -- decades-old song
# lyrics are pinned in cache forever, while the reason you walked to the
# fridge is evicted the moment you cross the kitchen threshold.
LINE = (
    "v2.6.0: fixed a bug where the brain retained every song lyric "
    "from 2007 but dropped the reason you opened the fridge."
)

MAX_CHARS = 160


def main() -> None:
    line = LINE.strip()
    if not line:
        raise SystemExit("patch note is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("patch note must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(f"patch note is {len(line)} chars, over {MAX_CHARS}")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(line + "\n", encoding="utf-8")
    # Read it back: the gate reads the file, so the file on disk must be
    # exactly the line we validated, not just what we intended to write.
    if target.read_text(encoding="utf-8") != line + "\n":
        raise SystemExit("entry.txt round-trip mismatch")


if __name__ == "__main__":
    main()
