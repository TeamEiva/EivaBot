#!/usr/bin/env python3
"""Install only the requirements that changed between an old and a new
requirements file. Used by the Eivabot launcher during updates.

Usage: python setup/updater.py <old_requirements> <new_requirements>
"""
import asyncio
import difflib
import shlex
import sys
from typing import List, Tuple


def read_lines(path: str) -> List[str]:
    with open(path, encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


def lines_difference(file1: str, file2: str) -> Tuple[List[str], List[str]]:
    lines1 = read_lines(file1)
    lines2 = read_lines(file2)
    diff = difflib.unified_diff(
        lines1, lines2, fromfile=file1, tofile=file2, lineterm="", n=0
    )
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line.startswith("+")]
    removed = [line[1:] for line in lines if line.startswith("-")]
    additions = [i for i in added if i not in removed]
    removals = [i for i in removed if i not in added]
    return additions, removals


async def runcmd(cmd: str) -> Tuple[str, str, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
    )


async def update_requirements(old: str, new: str) -> None:
    additions, _removals = await lines_difference(old, new)
    if not additions:
        print("No new requirements to install.")
        return
    for req in additions:
        if not req or req.startswith("#"):
            continue
        stdout, stderr, code = await runcmd(
            f"{sys.executable} -m pip install --upgrade {shlex.quote(req)}"
        )
        if code == 0:
            print(f"Successfully installed {req}")
        else:
            print(f"Failed to install {req}: {stderr or stdout}")


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: python updater.py <old_requirements> <new_requirements>")
        raise SystemExit(1)
    asyncio.run(update_requirements(sys.argv[1], sys.argv[2]))


if __name__ == "__main__":
    main()
