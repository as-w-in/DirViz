#/usr/bin/env python3
import os
import argparse
from pathlib import Path
import sys

def get_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path, onerror=lambda e: None):
        for f in filenames:
            try:
                total_size += os.path.getsize(os.path.join(dirpath, f))
            except:
                continue
    return total_size

def human_readable(size):
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}P"

def scan_tree(path, prefix="", depth=1, level=0):
    try:
        size = human_readable(get_size(path))
        if level == 0:
            print(f"{size}  {path}")

        if level >= depth:
            return

        entries = list(Path(path).iterdir())
        entries = sorted(entries, key=lambda e: get_size(e), reverse=True)
        count = len(entries)

        for idx, entry in enumerate(entries):
            is_last = idx == (count - 1)
            connector = "└── " if is_last else "├── "
            size = human_readable(get_size(entry))
            print(f"{prefix}{connector}{size}  {entry.name}")

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                scan_tree(entry, prefix + extension, depth, level + 1)

    except PermissionError:
        print(prefix + "\033[91m[Permission Denied]\033[0m")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(0)
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Disk Usage Visualizer")
    parser.add_argument("path", nargs="?", help="Directory to scan")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Tree depth")

    args = parser.parse_args()

    if not args.path:
        parser.print_help()
        return

    path = Path(args.path)

    if not path.exists():
        print(f"\033[91m❌ Error: Path '{args.path}' does not exist.\033[0m")
        return

    if not path.is_dir():
        print(f"\033[91m❌ Error: '{args.path}' is not a directory.\033[0m")
        return

    scan_tree(path, "", args.depth)

if __name__ == "__main__":
    main()
