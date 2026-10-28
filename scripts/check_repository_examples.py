"""Validate companion evidence; optionally execute all nine in fresh kernels."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
from unittest.mock import patch
import uuid

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "content/repository_examples"
sys.path.insert(0, str(LESSONS))
import repo_examples as rx
import numpy as np
import pandas as pd


def validate() -> None:
    result = rx.validate_all()
    atlas = rx.read_csv("repository_atlas.csv")
    assert len(atlas) == 18 and atlas.commit.str.fullmatch("[0-9a-f]{40}").all()
    assert atlas.readme_url.str.contains("/blob/").all()
    assert atlas.collection.value_counts().to_dict() == {"Related": 9, "PHI": 9}
    annual = rx.read_csv("nasa/global-temperature.csv")
    raw = pd.read_csv(rx.checked_path("nasa/nasa-gistemp-raw.csv"), skiprows=1, na_values="***")
    usable = raw.loc[raw["J-D"].notna()]
    assert np.array_equal(annual.year, usable.Year)
    assert np.allclose(annual.anomaly_c, usable["J-D"])
    rebased = annual.anomaly_c - annual.loc[annual.year.between(1991, 2020), "anomaly_c"].mean()
    assert np.allclose(np.diff(rebased), np.diff(annual.anomaly_c))
    water = rx.read_csv("noaa/monthly.csv")
    raw_water = rx.read_json("noaa/raw.json")
    assert len(water) == 300 and water.groupby("year").size().eq(12).all()
    assert not water[["year", "month"]].duplicated().any()
    assert np.allclose(water.msl_m, [float(row["MSL"]) for row in raw_water["data"]])
    deaths = rx.read_csv("cholera/cholera_deaths.csv")
    assert len(deaths) == 250 and deaths.DEATHS.sum() == 489
    assert len(rx.read_csv("cholera/pumps.csv")) == 8
    coral = rx.read_csv("coral/coralwatch_random_survey_20.csv")
    assert len(coral) == 20 and coral.sample_id.is_unique
    assert np.allclose(coral.average_colour_score, (coral.lightest_colour_score + coral.darkest_colour_score)/2)
    assert coral[["lightest_colour_score", "darkest_colour_score"]].ge(1).all(axis=None)
    assert coral[["lightest_colour_score", "darkest_colour_score"]].le(6).all(axis=None)
    earthquakes = rx.read_csv("usgs/events.csv")
    features = rx.read_json("usgs/events.geojson")["features"]
    assert len(earthquakes) == 78 and earthquakes.id.is_unique
    assert np.allclose(earthquakes[["longitude", "latitude", "depth_km"]], [f["geometry"]["coordinates"] for f in features])
    assert np.allclose(-earthquakes.depth_km, [-f["geometry"]["coordinates"][2] for f in features])
    assert len(rx.read_json("stac/sentinel-search.json")["features"]) == 8
    assert rx.read_json("stac/worldpop-item.json")["id"] == "UGA_DUG_2020"
    assert rx.read_json("stac/sentinel-collection.json")["license"] == "proprietary"
    assert rx.read_json("stac/worldpop-collection.json")["license"] == "CC-BY-4.0"
    # Exercise actual failure paths without touching the committed source bytes.
    scratch = ROOT / "_build" / ("companion-validation-" + uuid.uuid4().hex)
    scratch.mkdir(parents=True)
    try:
        record = rx.manifest()
        (scratch / "manifest.json").write_text(json.dumps(record), encoding="utf-8")
        with patch.object(rx, "DATA", scratch):
            try:
                rx.checked_path("repository_atlas.csv")
            except FileNotFoundError:
                pass
            else:
                raise AssertionError("Missing-data path did not fail")
            (scratch / "repository_atlas.csv").write_text("changed", encoding="utf-8")
            try:
                rx.checked_path("repository_atlas.csv")
            except ValueError as error:
                assert "checksum" in str(error)
            else:
                raise AssertionError("Modified bytes did not fail validation")
            raw_bad = b"wrong,fields\n1,2\n"
            (scratch / "repository_atlas.csv").write_bytes(raw_bad)
            record["files"]["repository_atlas.csv"].update(bytes=len(raw_bad), sha256=hashlib.sha256(raw_bad).hexdigest())
            (scratch / "manifest.json").write_text(json.dumps(record), encoding="utf-8")
            try:
                rx.read_csv("repository_atlas.csv")
            except ValueError as error:
                assert "schema/row" in str(error)
            else:
                raise AssertionError("CSV schema change did not fail")
    finally:
        resolved = scratch.resolve()
        assert resolved.parent == (ROOT / "_build").resolve() and resolved.name.startswith("companion-validation-")
        shutil.rmtree(resolved)
    check_refresh_failures()
    print(f"Companion checks passed: {result['files_verified']} hashes/schemas, 18 pinned repositories, scientific invariants, missing/modified/schema failures, malformed/semantic refresh rejection and replacement rollback.")


def check_refresh_failures() -> None:
    """All refresh mutations and rename failures operate on disposable copies."""
    spec = importlib.util.spec_from_file_location("snapshot_refresh", ROOT / "scripts/refresh_repository_data.py")
    refresh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(refresh)
    refresh.validate_staged(rx.DATA)
    fixture = ROOT / "_build" / ("companion-refresh-test-" + uuid.uuid4().hex)
    destination = fixture / "content/repository_examples/data"
    source_index = rx.manifest()
    response_bytes = {record["url"]: (rx.DATA / name).read_bytes() for name, record in source_index["files"].items() if record["url"]}
    url_for = {name: record["url"] for name, record in source_index["files"].items()}
    def fingerprint():
        return {p.relative_to(destination).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in destination.rglob("*") if p.is_file()}
    def json_change(name, change):
        body = json.loads(response_bytes[url_for[name]])
        change(body)
        return {url_for[name]: json.dumps(body).encode("utf-8")}
    try:
        shutil.copytree(rx.DATA, destination)
        (fixture / "docs/expansion").mkdir(parents=True)
        for name in ["related-repositories.md", "phi-case-studies.md"]:
            shutil.copy2(ROOT / "docs/expansion" / name, fixture / "docs/expansion" / name)
        before = fingerprint()
        bad_coral = list(csv.DictReader(io.StringIO(response_bytes[url_for["coral/coralwatch_random_survey_20.csv"]].decode("utf-8"))))
        bad_coral[0]["average_colour_score"] = "5"
        bad_coral_bytes = refresh.csv_bytes(bad_coral)
        coral_case = json_change("coral/coralwatch_random_survey_20.metadata.json", lambda body: body.update(csv_sha256=hashlib.sha256(bad_coral_bytes).hexdigest()))
        coral_case[url_for["coral/coralwatch_random_survey_20.csv"]] = bad_coral_bytes
        bad_annual = list(csv.DictReader(io.StringIO(response_bytes[url_for["nasa/global-temperature.csv"]].decode("utf-8"))))
        bad_annual[0]["anomaly_c"] = "0.5"
        cases = [
            ("provider failure", None),
            ("malformed WorldPop collection", {url_for["stac/worldpop-collection.json"]: b"{"}),
            ("non-object Sentinel collection", {url_for["stac/sentinel-collection.json"]: b"[]"}),
            ("wrong collection identity", json_change("stac/worldpop-collection.json", lambda body: body.update(id="OTHER"))),
            ("changed collection license", json_change("stac/worldpop-collection.json", lambda body: body.update(license="proprietary"))),
            ("missing Sentinel notice", json_change("stac/sentinel-collection.json", lambda body: body.update(links=[link for link in body["links"] if link["rel"] != "license"]))),
            ("invalid cloud bounds", json_change("stac/sentinel-search.json", lambda body: body["features"][0]["properties"].update({"eo:cloud_cover": 101}))),
            ("NASA raw/tidy semantic mismatch", {url_for["nasa/global-temperature.csv"]: refresh.csv_bytes(bad_annual)}),
            ("CoralWatch paired arithmetic", coral_case),
            ("NOAA wrong station", json_change("noaa/raw.json", lambda body: body["metadata"].update(id="OTHER"))),
            ("USGS out-of-query magnitude", json_change("usgs/events.geojson", lambda body: body["features"][0]["properties"].update(mag=3))),
        ]
        with patch.object(refresh, "ROOT", fixture), patch.object(refresh, "DEST", destination):
            for label, replacements in cases:
                def fetch(url):
                    if replacements is None:
                        raise OSError("Simulated unavailable provider")
                    return replacements.get(url, response_bytes[url])
                with patch.object(refresh, "fetch", side_effect=fetch):
                    try:
                        refresh.refresh()
                    except (ValueError, OSError, KeyError, AssertionError):
                        pass
                    else:
                        raise AssertionError(f"Refresh accepted {label}")
                assert fingerprint() == before, f"Refresh changed the prior directory: {label}"
                assert not list(destination.parent.glob(".data-refresh-*")) and not (destination.parent / ".data-previous").exists()
            original_rename = Path.rename
            def fail_replacement(path, target):
                assert path.resolve().is_relative_to(fixture.resolve())
                assert Path(target).resolve().is_relative_to(fixture.resolve())
                if path.name.startswith(".data-refresh-") and Path(target) == destination:
                    raise OSError("Simulated replacement rename failure")
                return original_rename(path, target)
            with patch.object(refresh, "fetch", side_effect=lambda url: response_bytes[url]), patch.object(Path, "rename", fail_replacement):
                try:
                    refresh.refresh()
                except OSError as error:
                    assert "replacement rename failure" in str(error)
                else:
                    raise AssertionError("Replacement rename failure was not exercised")
            assert fingerprint() == before and not (destination.parent / ".data-previous").exists()
            assert not list(destination.parent.glob(".data-refresh-*"))
    finally:
        resolved = fixture.resolve()
        assert resolved.parent == (ROOT / "_build").resolve() and resolved.name.startswith("companion-refresh-test-")
        shutil.rmtree(resolved)


def execute() -> None:
    import nbformat
    from nbclient import NotebookClient
    output = ROOT / "_build/executed-companions"
    figures = ROOT / "_build/companion-figures"
    output.mkdir(exist_ok=True)
    figures.mkdir(exist_ok=True)
    notebooks = sorted(LESSONS.glob("[0-9][0-9]_*.ipynb"))
    assert len(notebooks) == 9
    for number, path in enumerate(notebooks):
        nb = nbformat.read(path, as_version=4)
        # Exercise all three documented launch locations with independent kernels.
        cwd = [ROOT, ROOT / "content", LESSONS][number % 3]
        NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(cwd)}}).execute()
        count = 0
        for cell in nb.cells:
            for result in cell.get("outputs", []):
                assert result.output_type != "error"
                if "image/png" in result.get("data", {}):
                    import base64
                    count += 1
                    (figures / f"{path.stem}-{count}.png").write_bytes(base64.b64decode(result.data["image/png"]))
        assert count >= 3, f"{path.name}: executed without at least three rendered figures"
        nbformat.write(nb, output / path.name)
        print(f"Fresh desktop kernel: {path.name}, {count} rendered figures; cwd={cwd.relative_to(ROOT) or '.'}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    validate()
    if args.execute:
        execute()
