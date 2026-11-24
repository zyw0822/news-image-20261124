#!/usr/bin/env python3
"""Entry for make.fun: Sum up 24 November's world news in one image.

The program is deterministic and uses no network: it copies the
pre-built 1024x1024 poster (entry.png, in this repository) to
/output/entry.png. Running it twice writes the same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png")


def main() -> int:
    if not os.path.isfile(SRC):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.path.dirname(DST)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, DST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
