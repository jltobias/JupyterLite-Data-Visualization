"""Portable local evidence validation and presentation for the companion lessons.

Scientific transformations live visibly in the notebooks. Nothing here requests
live data, installs native GIS packages, or changes a source snapshot.
"""
from __future__ import annotations

import csv
from decimal import Decimal
import hashlib
from html import escape
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def json_value_sha256(raw: bytes, *, browser_safe: bool = False) -> str:
    """Hash JSON values, ignoring object order/formatting, not changed data.

    Contents/DriveFS parses and JSON.stringify's JSON files before exposing them
    to Python. Numeric 1 and 1.0 are equivalent; booleans, strings, array order,
    and exact decimal numeric values remain distinct. This is a versioned local
    fingerprint, not a claim of RFC 8785 canonicalization.
    """
    def invalid_constant(value):
        raise ValueError(f"Non-finite JSON constant: {value}")

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def values(value):
        if value is None:
            return ["null"]
        if isinstance(value, bool):
            return ["boolean", value]
        if isinstance(value, str):
            return ["string", value]
        if isinstance(value, Decimal):
            if browser_safe and Decimal(str(float(value))) != value:
                raise ValueError(f"JSON number cannot survive browser binary64 delivery: {value}")
            sign, digits, exponent = value.as_tuple()
            digits = list(digits)
            if not any(digits):
                return ["number", 0, "0", 0]
            while digits[-1] == 0:
                digits.pop()
                exponent += 1
            return ["number", sign, "".join(map(str, digits)), exponent]
        if isinstance(value, list):
            return ["array", [values(item) for item in value]]
        return ["object", [[key, values(value[key])] for key in sorted(value)]]

    document = json.loads(raw, parse_int=Decimal, parse_float=Decimal,
                          parse_constant=invalid_constant, object_pairs_hook=unique_object)
    canonical = json.dumps(values(document), ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def transport_fingerprints(name: str, raw: bytes) -> dict:
    """Extra content checks for registered JSON representation changes in DriveFS."""
    if Path(name).suffix.lower() in {".json", ".geojson"}:
        return {"json_value_sha256": json_value_sha256(raw, browser_safe=True),
                "json_value_algorithm": "typed-json-values-v1"}
    return {}


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
        try:
            actual = transport_fingerprints(name, raw)
            if "json_value_sha256" in actual:
                equivalent = (record.get("json_value_algorithm") == actual["json_value_algorithm"]
                              and record.get("json_value_sha256") == actual["json_value_sha256"])
            else:
                equivalent = False
        except (ValueError, UnicodeError, OverflowError):
            equivalent = False
        if not equivalent:
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
