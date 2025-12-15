#!/usr/bin/env python3
"""
move_to_az.py  –  drop a folder on this script → every **file** sorted into A-Z buckets.
ASCII-only bucket names guarantee compatibility with FAT/exFAT/NTFS drives.
MIT licence – do anything you want.
"""
from __future__ import annotations
import argparse
import string
import unicodedata
from pathlib import Path
from shutil import move, copy2

SRC_HINT = r"Example: C:\Users\%USERNAME%\Desktop\New folder"


# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------
def ensure_az(root: Path) -> None:
    """Create A-Z + '#' buckets (ASCII-only names)."""
    for letter in string.ascii_uppercase:
        (root / letter).mkdir(exist_ok=True)
    (root / "#").mkdir(exist_ok=True)


def az_bucket(name: str, root: Path) -> Path:
    """
    Return ASCII bucket for *name*.
    Non-ASCII first char  →  '#' bucket (safe for every filesystem).
    """
    first = unicodedata.normalize("NFKD", name[0])[0].upper()
    return root / (first if first.isascii() and first.isalpha() else "#")


def unique_name(dest: Path) -> Path:
    """If *dest* exists return file (1), file (2), …  else *dest* itself."""
    if not dest.exists():
        return dest
    stem, suffix, n = dest.stem, dest.suffix, 1
    while True:
        candidate = dest.with_name(f"{stem} ({n}){suffix}")
        if not candidate.exists():
            return candidate
        n += 1


# ------------------------------------------------------------------
# core
# ------------------------------------------------------------------
def organise(src: Path, dst: Path, *, copy: bool = False, dry: bool = True) -> None:
    """Move/copy every top-level file into A-Z tree."""
    action = copy2 if copy else move
    ensure_az(dst)

    for item in src.iterdir():
        if item.is_file():
            target_dir = az_bucket(item.name, dst)
            final = unique_name(target_dir / item.name)

            tag = "[preview] " if dry else ""
            print(f"{tag}{item.name}  →  {final}")
            if not dry:
                action(item, final)


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Sort files into A-Z folders.")
    parser.add_argument("src", nargs="?", help=f"folder to organise  ({SRC_HINT})")
    parser.add_argument("-d", "--dst", help="where A-Z tree lives  [same as src]")
    parser.add_argument("--copy", action="store_true", help="copy instead of move")
    parser.add_argument("--go", action="store_true", help="actually perform the action")
    args = parser.parse_args()

    src = Path(args.src or input("Folder to organise: ").strip('"'))
    dst = Path(args.dst or input("A-Z tree location [ENTER = same]: ").strip('"') or src)

    if not src.is_dir():
        parser.error("Source must be an existing directory")

    organise(src, dst, copy=args.copy, dry=not args.go)


# ------------------------------------------------------------------
if __name__ == "__main__":
    main()