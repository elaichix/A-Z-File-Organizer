#!/usr/bin/env python3
"""
Organise any single folder you paste into an A-Z tree.
NOW pre-creates A-Z folders instantly, whether or not a file needs them.
"""
import os, shutil, argparse, pathlib, string

def ensure_az_folders(root: pathlib.Path) -> None:
    """Create A-Z (and #) in one go – only if missing."""
    for letter in string.ascii_uppercase:          # A-Z
        (root / letter).mkdir(exist_ok=True)
    (root / "#").mkdir(exist_ok=True)              # non-letters bucket
    print("✔  A-Z folders ensured in", root)

def az_dir_for(name: str, root: pathlib.Path) -> pathlib.Path:
    first = name[0].upper()
    if not first.isalpha():
        first = "#"
    return root / first

def main():
    parser = argparse.ArgumentParser(description="A-to-Z organiser (pre-create edition)")
    parser.add_argument("--go", action="store_true", help="Really perform the move")
    parser.add_argument("--copy", action="store_true", help="Copy instead of move")
    args = parser.parse_args()

    src_txt = input("Paste the folder you want to organise: ").strip().strip('"')
    src = pathlib.Path(src_txt).expanduser().resolve()
    if not src.is_dir():
        print("❌  That is not a valid folder – aborting.")
        return

    dst_txt = input("Where should the A-Z tree be created? [same folder = press ENTER] ").strip().strip('"')
    dst = pathlib.Path(dst_txt).expanduser().resolve() if dst_txt else src

    ensure_az_folders(dst)          # <<<<< instant A-Z creation

    action = shutil.copy2 if args.copy else shutil.move
    dry = not args.go

    print("\nDRY RUN – nothing moved yet" if dry else "\nMOVING…")
    print("Source :", src)
    print("A-Z at :", dst)
    print("-" * 60)

    for item in src.iterdir():
        if item.is_file():
            az = az_dir_for(item.name, dst)
            dest = az / item.name

            counter = 1
            stem, suffix = dest.stem, dest.suffix
            while dest.exists():
                dest = az / f"{stem} ({counter}){suffix}"
                counter += 1

            print(f"{'[preview] ' if dry else ''}{item.name}  →  {dest}")
            if not dry:
                action(item, dest)

    print("-" * 60)
    print("Done – A-Z tree ready.")

if __name__ == "__main__":
    main()