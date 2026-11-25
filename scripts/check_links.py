#!/usr/bin/env python3
"""Check relative Markdown links and image paths in src/<lang>/.

Usage:
    python -I scripts/check_links.py zh
    python -I scripts/check_links.py en
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "zh"
    base = ROOT / "src" / lang
    missing = []
    checked = 0

    for md in sorted(base.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            checked += 1
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                missing.append((md.relative_to(ROOT), raw, resolved.relative_to(ROOT)))

    print(f"checked {checked} relative links in src/{lang}")
    if missing:
        print(f"MISSING {len(missing)}:")
        for src, raw, resolved in missing:
            print(f"  {src}: {raw}  ->  {resolved}")
        return 1
    print("all relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
