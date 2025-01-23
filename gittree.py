#!/usr/bin/env python3
import os
from pathlib import Path
from typing import List


def get_git_tracked_files() -> List[Path]:
    """Returns a list of files tracked by Git, ignoring files in .gitignore."""
    try:
        tracked_files = os.popen("git ls-files").read().splitlines()
        return [Path(file).resolve() for file in tracked_files]
    except Exception as e:
        print(f"Error retrieving tracked files: {e}")
        exit(1)


def print_tree(path: Path, indent: str = "", tracked_files: List[Path] | None = None) -> None:
    """Recursively prints the tree structure of a directory."""
    if tracked_files is None:
        tracked_files = []

    # Get all children sorted
    children = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
    for i, child in enumerate(children):
        # Check if the current child or its contents are tracked
        if not any(tracked_file == child or tracked_file.is_relative_to(child) for tracked_file in tracked_files):
            continue

        # Determine the branch character
        branch = "└── " if i == len(children) - 1 else "├── "
        print(f"{indent}{branch}{child.name}")

        # If it's a directory, recursively print its contents
        if child.is_dir():
            new_indent = indent + ("    " if i == len(children) - 1 else "│   ")
            print_tree(child, new_indent, tracked_files)


def main():
    # Get the tracked files
    tracked_files = get_git_tracked_files()
    if not tracked_files:
        print("No tracked files found.")
        return

    # Find the root directory of the Git repository
    repo_root = Path(os.popen("git rev-parse --show-toplevel").read().strip()).resolve()
    if not repo_root.exists():
        print("Error: Unable to determine the Git repository root.")
        return

    print(repo_root)
    print_tree(repo_root, tracked_files=tracked_files)


if __name__ == "__main__":
    main()
