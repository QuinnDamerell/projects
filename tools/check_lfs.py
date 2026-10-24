#!/usr/bin/env python3
"""Fails the build if any file in docs/ is still a Git LFS pointer instead of the real file.

Binary media is stored with Git LFS. If a checkout skips the LFS download, every image and
PDF is left as a ~130-byte text pointer, and the site would deploy with broken media and no
error. Run this before building:

    python tools/check_lfs.py && zensical build --clean

Pass a directory to check somewhere other than docs/.
"""

import pathlib
import sys

POINTER = b"version https://git-lfs.github.com/spec/v1"


def main():
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "docs"
    pointers = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.stat().st_size < 1024:
            with path.open("rb") as f:
                if f.read(len(POINTER)) == POINTER:
                    pointers.append(path.relative_to(root).as_posix())
    if pointers:
        print(f"{len(pointers)} files in {root.name}/ are Git LFS pointers, not the real files:", file=sys.stderr)
        for pointer in pointers[:20]:
            print(f"  {pointer}", file=sys.stderr)
        if len(pointers) > 20:
            print(f"  ...and {len(pointers) - 20} more", file=sys.stderr)
        print('Install Git LFS and run "git lfs pull" before building.', file=sys.stderr)
        sys.exit(1)
    print(f"Git LFS check passed: no pointer files in {root.name}/.")


if __name__ == "__main__":
    main()
