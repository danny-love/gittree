#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import List, Optional
import fnmatch


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


def print_matching_files(pattern: str, tracked_files: List[Path]) -> None:
    """Prints the contents of files matching the given pattern."""
    print(f"\nContents of files matching '{pattern}':\n")
    matched_files = [file for file in tracked_files if fnmatch.fnmatch(file.name, pattern)]

    if not matched_files:
        print(f"No files match the pattern '{pattern}'.")
        return

    for file in matched_files:
        print(f"--- {file} ---")
        try:
            with file.open("r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading {file}: {e}")


def main():
    # Parse command-line arguments
    cat_pattern: Optional[str] = None
    if len(sys.argv) > 1 and sys.argv[1].startswith("--cat="):
        cat_pattern = sys.argv[1].split("=", 1)[1]

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

    # Print the tree structure
    print(repo_root)
    print_tree(repo_root, tracked_files=tracked_files)

    # If --cat is provided, print matching file contents
    if cat_pattern:
        print_matching_files(cat_pattern, tracked_files)


if __name__ == "__main__":
    main()
