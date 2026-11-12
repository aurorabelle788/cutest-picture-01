# cutest-picture-01 entry (Python 3.13, standard library only).
#
# The picture is entry.png beside this file: an impossibly round baby
# axolotl with huge sparkling eyes and a tiny pink bow, floating in soft
# pastel-blue water among bubbles. The program copies it to
# /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader).
#
# Deterministic: the same bytes in, the same bytes out, every run.

import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

MAX_BYTES = 1_048_576
MAX_SIDE = 1_024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_gate(path: Path) -> None:
    """Fail loudly if the output would not pass the competition gate:
    a whole PNG (or JPEG) of at most 1 MiB and 1024x1024 px."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB gate")
    if data[:8] == PNG_MAGIC:
        width, height = struct.unpack(">II", data[16:24])
    elif data[:2] == b"\xff\xd8":
        raise SystemExit("unexpected JPEG output: entry.png must be the PNG")
    else:
        raise SystemExit("entry.png is neither PNG nor JPEG")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024x1024 gate")
    print(f"wrote {path} ({width}x{height}, {len(data)} bytes)", file=sys.stderr)


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    check_gate(dest)


if __name__ == "__main__":
    main()
