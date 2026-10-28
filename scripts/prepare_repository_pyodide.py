"""Explicitly download the pinned, hash-checked WASM test runtime into _build."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "_build/pyodide-table-test"
BASE = "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/"
CORE = {
    "pyodide.mjs": "23213d27e9dacbda6f25f955fb38dabfc40ada082c04ee253047ea5dddcaa3b5",
    "pyodide.asm.js": "1263f02b5b26099b96112378156f242dd98b39a8201ba7765e5fe3d455c5ce91",
    "pyodide.asm.wasm": "e2f4ee75b325e35eb31bfb8c613d4dd5098f5502c156a97847686875b5025480",
    "python_stdlib.zip": "4298b6ee445cb724c3973437da47789752b9e6ff4e26619026b283ec801fc46b",
    "pyodide-lock.json": "3256ffc76388de0e37f4b34d42ab484268d1afc675179ff97b2a5bb14f84ccac",
}


def get(name: str, expected: str) -> None:
    path = DEST / name
    if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected:
        return
    with urlopen(BASE + name, timeout=90) as response:
        raw = response.read(60_000_001)
    if len(raw) > 60_000_000 or hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"Pinned runtime hash/size mismatch: {name}")
    path.write_bytes(raw)
    print(f"Downloaded and verified {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    if not parser.parse_args().download:
        parser.error("Pass --download for this explicit development-only network operation")
    DEST.mkdir(parents=True, exist_ok=True)
    for name, digest in CORE.items():
        get(name, digest)
    packages = json.loads((DEST / "pyodide-lock.json").read_text(encoding="utf-8"))["packages"]
    todo = ["numpy", "pandas", "matplotlib", "ipython", "micropip"]
    seen = set()
    while todo:
        key = todo.pop().replace("_", "-")
        if key in seen:
            continue
        seen.add(key)
        entry = packages[key]
        get(entry["file_name"], entry["sha256"])
        todo.extend(entry["depends"])
    print(f"Pinned Pyodide 0.29.3 and {len(seen)} package wheels ready at {DEST}")


if __name__ == "__main__":
    main()
