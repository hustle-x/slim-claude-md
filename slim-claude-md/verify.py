#!/usr/bin/env python3
"""Check that splitting a CLAUDE.md lost nothing.

Usage: python3 verify.py BACKUP.md NEW_CLAUDE.md NOTE.md [NOTE.md ...]

Every non-empty line of BACKUP.md must appear in the new files at least as
many times as it did before. Exits 1 and lists the lines that went missing.
Standard library only, no network.
"""
import sys
from collections import Counter


def lines(path):
    with open(path, encoding="utf-8") as f:
        return [l for l in f.read().split("\n") if l.strip()]


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    before = Counter(lines(argv[1]))
    after = Counter()
    for p in argv[2:]:
        after.update(lines(p))
    missing = [(l, n - after[l]) for l, n in before.items() if after[l] < n]
    size = lambda p: len(open(p, encoding="utf-8").read().encode())
    old, new = size(argv[1]), size(argv[2])
    print(f"CLAUDE.md: {old:,} bytes -> {new:,} bytes "
          f"(about {(old - new) // 4:,} tokens saved per session)")
    if missing:
        print(f"MISSING {len(missing)} line(s):")
        for l, n in missing[:50]:
            print(f"  x{n}  {l[:100]}")
        return 1
    print(f"OK: all {sum(before.values())} non-empty lines are kept.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
