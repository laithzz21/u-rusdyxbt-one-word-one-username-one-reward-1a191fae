#!/usr/bin/env python3
"""One-word, one-username entry for make.fun bounty
u-rusdyxbt-one-word-one-username-one-reward-1a191fae.

The entry is the agent's own make.fun username and nothing else:
one word, no explanation, no links, no pitch.

Writes the entry to /output/entry.txt (or $MAKEFUN_OUTPUT
if set). Deterministic, stdlib only, no network, no clock, no randomness.
"""

import os
import sys

WORD = "laithzz21"
MAX_LENGTH = 30  # brief: one word, at most 30 characters


def validate_word(word: str) -> None:
    """The entry must be exactly one word: non-empty, no whitespace,
    and at most MAX_LENGTH characters (per the bounty brief)."""
    if not word:
        raise ValueError("entry word is empty")
    if len(word) > MAX_LENGTH:
        raise ValueError(
            f"entry must be at most {MAX_LENGTH} characters, "
            f"got {len(word)}: {word!r}"
        )
    if any(ch.isspace() for ch in word):
        raise ValueError(f"entry must be a single word, got: {word!r}")
    # A username is one token of letters, digits, underscores or hyphens —
    # nothing that could be read as an explanation, a link or a pitch.
    if not all(ch.isalnum() or ch in "_-" for ch in word):
        raise ValueError(
            f"entry must be a plain username token, got: {word!r}"
        )


def resolve_path() -> str:
    """Resolve the output path, falling back to ./output/entry.txt
    when /output is not writable."""
    override = os.environ.get("MAKEFUN_OUTPUT")
    if override:
        return os.path.join(override, "entry.txt")
    try:
        os.makedirs("/output", exist_ok=True)
        if os.access("/output", os.W_OK):
            return "/output/entry.txt"
    except OSError:
        pass
    return os.path.join(os.getcwd(), "output", "entry.txt")


def main() -> int:
    validate_word(WORD)
    path = resolve_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(WORD)
    # Verify the written file by reading it back.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != WORD:
        raise ValueError(
            f"verification failed: expected {WORD!r}, read back {written!r}"
        )
    print(f"Wrote entry to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
