"""Copy the poster beside this file into the harness output directory."""

import os
import shutil
import sys
from pathlib import Path

DEFAULT_OUTPUT_DIR = "/output"
POSTER_NAME = "entry.png"


def main():
    """Copy entry.png next to this file into $MAKEFUN_OUTPUT_DIR, or /output."""
    source = Path(__file__).resolve().parent / POSTER_NAME
    if not source.is_file():
        print(f"error: poster not found: {source}", file=sys.stderr)
        return 1

    raw_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    output_dir = Path(raw_dir or DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / POSTER_NAME)
    return 0


if __name__ == "__main__":
    sys.exit(main())
