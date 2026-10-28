"""Portable local evidence validation and presentation for the companion lessons.

Scientific transformations live visibly in the notebooks. Nothing here requests
live data, installs native GIS packages, or changes a source snapshot.
"""
from __future__ import annotations

import csv
import hashlib
from html import escape
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def manifest() -> dict:
    path = DATA / "manifest.json"
    if not path.is_file():
        raise FileNotFoundError("Companion data/manifest.json is missing. Open the notebook in content/repository_examples (desktop/Book) or repository_examples (Lite), with its sibling helper and data folder.")
    return json.loads(path.read_text(encoding="utf-8"))


def checked_path(name: str) -> Path:
    record = manifest()["files"].get(name)
    if record is None:
        raise ValueError(f"Unregistered snapshot: {name}")
    path = DATA / name
    if not path.resolve().is_relative_to(DATA.resolve()):
        raise ValueError(f"Snapshot path escapes the data directory: {name}")
    if not path.is_file():
        raise FileNotFoundError(f"Missing packaged snapshot: {name}. Restore the published data directory; no substitute observations will be generated.")
    raw = path.read_bytes()
    if len(raw) != record["bytes"] or hashlib.sha256(raw).hexdigest() != record["sha256"]:
        raise ValueError(f"Snapshot checksum mismatch: {name}. Restore the published snapshot or explicitly refresh and review its manifest.")
    return path


def read_csv(name: str):
    import pandas as pd
    path = checked_path(name)
    record = manifest()["files"][name]
    # Validate source field order and row count before pandas performs inference.
    records = list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig"))))
    columns = list(records[0]) if records else []
    if record.get("columns") != columns or record.get("rows") != len(records):
        raise ValueError(f"Snapshot CSV schema/row count mismatch: {name}")
    return pd.read_csv(path)


def read_json(name: str):
    return json.loads(checked_path(name).read_text(encoding="utf-8"))


def validate_all() -> dict:
    index = manifest()
    for name, record in index["files"].items():
        if record["source"] not in index["sources"]:
            raise ValueError(f"Unknown manifest source: {record['source']}")
        checked_path(name)
        if record.get("columns") is not None:
            read_csv(name)
    return {"files_verified": len(index["files"]), "snapshot_retrieved_utc": index["retrieved_utc"]}


def source_card(key: str):
    from IPython.display import HTML
    index = manifest()
    source = index["sources"][key]
    rows = [(label, source[field]) for label, field in [("Evidence", "kind"), ("Units", "units"), ("Credit", "attribution"), ("Terms", "terms"), ("Limits", "limitation")]]
    body = "".join(f"<tr><th style='text-align:left;vertical-align:top'>{escape(k)}</th><td>{escape(v)}</td></tr>" for k, v in rows)
    return HTML(f"<section><h3>{escape(source['title'])}</h3><table>{body}</table><p>Snapshot retrieval: {escape(index['retrieved_utc'])}. <a href='{escape(source['terms_url'], quote=True)}'>Source terms / citation</a>. Full queries and hashes: data/manifest.json.</p></section>")


def finish(ax, title: str, xlabel: str, ylabel: str):
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=0.18)
    return ax
