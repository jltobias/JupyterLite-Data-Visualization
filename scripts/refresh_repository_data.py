"""Explicitly refresh the bounded companion snapshots, validating before replacement.

Run with --refresh. Ordinary lessons and builds never access these APIs. Each
response is retained byte-for-byte alongside derived, tidy tables. A failed
download/validation leaves the previous data directory intact.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import re
import shutil
import uuid
from urllib.request import Request, urlopen
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "content/repository_examples"))
from repo_examples import transport_fingerprints
DEST = ROOT / "content/repository_examples/data"
CLIMATE = "https://raw.githubusercontent.com/jltobias/JupyterLite-Climate-and-Health/248f9860d189502013b36b3c4271777edafc4f7f/content/data/"
CHOLERA = "https://raw.githubusercontent.com/jltobias/JupyterLite-GeoLibre-GeoAI/dda3a4667a1267b5ac4858723c46d8c0c82cb7a6/book/notebooks/data/cholera/"
NOAA = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=monthly_mean&application=JupyterLiteDataVisualization&begin_date=20000101&end_date=20241231&datum=MSL&station=8638610&time_zone=gmt&units=metric&format=json"
SENTINEL = "https://earth-search.aws.element84.com/v1/search?collections=sentinel-2-l2a&bbox=25.7%2C-24.9%2C26.2%2C-24.4&datetime=2024-01-01T00%3A00%3A00Z%2F2024-01-31T23%3A59%3A59Z&limit=8"
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-01-01&endtime=2024-02-01&minmagnitude=4.5&minlatitude=30&maxlatitude=46&minlongitude=128&maxlongitude=148&orderby=time-asc"

SOURCES = {
    "notices": {"title": "Companion source and reuse notices", "kind": "original attribution register", "units": "one source-specific statement per dataset", "attribution": "Source-specific authors/providers named in this document and retained metadata", "terms": "Individual dataset/metadata terms apply; project licensing remains undecided", "terms_url": "https://github.com/jltobias/JupyterLite-Data-Visualization/blob/main/references.md", "limitation": "Not a project-wide license grant or clearance of unrelated upstream assets."},
    "atlas": {"title": "Curated inspected sample of 18 related repositories", "kind": "curated source-review metadata", "units": "one inspected repository per row; lesson connections are editorial choices", "attribution": "Pinned source reviews in docs/expansion/related-repositories.md and phi-case-studies.md, inspected 2026-10-28", "terms": "Original factual index and lesson connections; linked repository licenses are scoped evidence, not permission for all assets", "terms_url": "https://github.com/jltobias/JupyterLite-Data-Visualization/tree/main/docs/expansion", "limitation": "A curated inspected sample, not a comprehensive inventory, quality score, popularity ranking or live runtime test."},
    "nasa": {"title": "NASA GISTEMP v4 global annual temperature anomaly", "kind": "observational estimate", "units": "degrees C relative to 1951–1980", "attribution": "GISTEMP Team (2026); Lenssen et al. (2024), doi:10.1029/2023JD040179", "terms": "NASA data reuse guidance; upstream repository software license does not apply to these observations", "terms_url": "https://data.giss.nasa.gov/gistemp/", "limitation": "Global estimated anomalies, not local temperatures or health outcomes. Original source retrieval 2026-10-09."},
    "noaa": {"title": "NOAA CO-OPS Sewells Point monthly mean water levels, 2000–2024", "kind": "observational estimate", "units": "meters, station MSL datum, GMT", "attribution": "NOAA National Ocean Service, CO-OPS, station 8638610", "terms": "NOAA/NOS government information reuse guidance; credit NOAA, inspect any third-party exclusions", "terms_url": "https://oceanservice.noaa.gov/about/faq.html", "limitation": "Local relative sea level; not global sea-level rise, an inundation surface, or a forecast."},
    "cholera": {"title": "Digitized 1854 London cholera deaths and pumps", "kind": "historical records", "units": "recorded deaths per mapped location; WGS84 longitude/latitude degrees", "attribution": "PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic, 476f6dd5a8430e6eb823e79614fda1d7e12a78fb; supplied via GeoLibre-GeoAI dda3a4667a1267b5ac4858723c46d8c0c82cb7a6", "terms": "GPL-3.0 bundle: retain cholera/LICENSE and provenance; separate from undecided project license", "terms_url": "https://github.com/PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic/blob/476f6dd5a8430e6eb823e79614fda1d7e12a78fb/LICENSE", "limitation": "250 locations / 489 recorded deaths. Digitization completeness not independently verified; no dates, denominators, controls or causal labels."},
    "coral": {"title": "CoralWatch single opportunistic survey, 20 colonies", "kind": "citizen-science observations", "units": "colour chart index, 1–6", "attribution": "CoralWatch / BioCollect survey bd39e449-038f-4d45-ab6d-b56922a6f532; source-specific attribution in metadata", "terms": "CC BY 4.0 for this survey extract; retain metadata and attribution", "terms_url": "https://creativecommons.org/licenses/by/4.0/", "limitation": "Two paired readings on each colony; no coordinates/personal fields/photos. Not bleaching percentage, reef coverage, temperature or representative reef sampling."},
    "worldpop": {"title": "WorldPop UGA_DUG_2020 STAC Item and collection", "kind": "catalog metadata", "units": "footprint degrees; Degree of Urbanisation product reference year 2020", "attribution": "Bondarenko et al., WorldPop / University of Southampton (2026), doi:10.5258/SOTON/WP00879", "terms": "CC BY 4.0 identified in collection and item TIFF copyright; inspect asset-specific terms before downloading", "terms_url": "https://creativecommons.org/licenses/by/4.0/", "limitation": "Metadata and footprint only. No population counts, land-cover proportions or raster pixels have been sampled. Publication year differs from reference year."},
    "sentinel": {"title": "Earth Search Sentinel-2 L2A Gaborone bounded January 2024 search", "kind": "catalog metadata", "units": "footprints degrees; eo:cloud_cover percent for whole item", "attribution": "Contains modified Copernicus Sentinel data (2024), processed by Element 84; metadata selection by this course", "terms": "Collection license label is proprietary; Copernicus Sentinel Data Legal Notice applies. This is not a CC/MIT dataset declaration.", "terms_url": "https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice", "limitation": "First 8 returned Items, not all January scenes. Cloud metadata is not local cloud sampling; metadata is not imagery or TB evidence."},
    "usgs": {"title": "USGS January 2024 Japan earthquakes, magnitude ≥4.5", "kind": "event catalog observations", "units": "longitude/latitude degrees; depth km positive downward; UTC milliseconds; reported magnitude type", "attribution": "U.S. Geological Survey Earthquake Hazards Program", "terms": "USGS-authored US government products are generally public domain; third-party content is excluded from that guidance", "terms_url": "https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits", "limitation": "Bounded catalog selection with event revisions and mixed magnitude types. Not an earthquake prediction or a complete seismicity census."},
}


def fetch(url: str) -> bytes:
    with urlopen(Request(url, headers={"User-Agent": "JupyterLite-Data-Visualization/companion-snapshot"}), timeout=90) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError(f"Response exceeds the 2 MB snapshot bound: {url}")
    return data


def csv_bytes(rows: list[dict]) -> bytes:
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return text.getvalue().encode("utf-8")


def validate_staged(directory: Path) -> None:
    """Reject incompatible source semantics before any existing snapshot moves."""
    def require(condition, message):
        if not condition:
            raise ValueError(f"Staged evidence validation failed: {message}")

    def number(value, low, high):
        require(not isinstance(value, bool), "boolean supplied as a scientific number")
        result = float(value)
        require(math.isfinite(result) and low <= result <= high, f"numeric value outside [{low}, {high}]: {value}")
        return result

    def integer(value, low, high):
        result = number(value, low, high)
        require(result.is_integer(), f"expected integer: {value}")
        return int(result)

    def instant(value):
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(result.tzinfo is not None, f"UTC offset missing: {value}")
        return result.astimezone(timezone.utc)

    def rows(name):
        with (directory / name).open(encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))

    def bad_constant(value):
        raise ValueError(f"Non-finite JSON constant: {value}")

    def finite_json(value):
        if isinstance(value, float):
            require(math.isfinite(value), "non-finite JSON number")
        elif isinstance(value, dict):
            for child in value.values():
                finite_json(child)
        elif isinstance(value, list):
            for child in value:
                finite_json(child)

    documents = {}
    for path in directory.rglob("*"):
        if path.suffix in [".json", ".geojson"]:
            body = json.loads(path.read_text(encoding="utf-8"), parse_constant=bad_constant)
            require(isinstance(body, dict), f"expected JSON object: {path.name}")
            finite_json(body)
            documents[path.relative_to(directory).as_posix()] = body
    index = documents["manifest.json"]
    require(index["version"] == 1 and index["sources"] == SOURCES, "manifest/source-card contract changed")
    instant(index["retrieved_utc"])
    for name, record in index["files"].items():
        path = directory / name
        require(path.resolve().is_relative_to(directory.resolve()), f"unsafe path: {name}")
        raw = path.read_bytes()
        require(record["source"] in SOURCES and len(raw) == record["bytes"] and hashlib.sha256(raw).hexdigest() == record["sha256"], f"manifest bytes/source mismatch: {name}")
        for key, expected in transport_fingerprints(name, raw).items():
            require(record.get(key) == expected, f"JSON transport fingerprint mismatch: {name}")
        if record.get("columns") is not None:
            table = rows(name)
            require(len(table) == record["rows"] and list(table[0]) == record["columns"], f"CSV schema/rows: {name}")

    annual = rows("nasa/global-temperature.csv")
    with (directory / "nasa/nasa-gistemp-raw.csv").open(encoding="utf-8", newline="") as stream:
        require(next(stream).strip() == "Land-Ocean: Global Means", "NASA product header")
        raw_nasa = list(csv.DictReader(stream))
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    usable = []
    seen = set()
    for row in raw_nasa:
        year = integer(row["Year"], 1880, 2026)
        require(year not in seen, "duplicate NASA year")
        seen.add(year)
        for field in months + ["J-D"]:
            if row[field] != "***":
                number(row[field], -5, 5)
        if row["J-D"] != "***":
            require(all(row[m] != "***" for m in months), "NASA annual value lacks complete months")
            usable.append((year, float(row["J-D"])))
    require([int(r["year"]) for r in annual] == list(range(1880, 2026)), "NASA annual year coverage")
    require([(int(r["year"]), number(r["anomaly_c"], -5, 5)) for r in annual] == usable, "NASA raw J-D/tidy mismatch")
    require(all(r["data_type"] == "observed" for r in annual), "NASA evidence type changed")
    nasa_meta = documents["nasa/provenance.json"]["observed"]
    require(nasa_meta["sha256"] == index["files"]["nasa/nasa-gistemp-raw.csv"]["sha256"], "NASA provenance hash")
    require(nasa_meta["source_url"] == "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv" and "1951-1980" in nasa_meta["units"] and "NASA" in nasa_meta["license"], "NASA product/baseline/terms")

    coral = rows("coral/coralwatch_random_survey_20.csv")
    coral_meta = documents["coral/coralwatch_random_survey_20.metadata.json"]
    survey = "bd39e449-038f-4d45-ab6d-b56922a6f532"
    require(coral_meta["survey_record_id"] == survey and coral_meta["record_count"] == len(coral) == 20, "CoralWatch survey/count")
    require(coral_meta["license"] == "CC BY 4.0" and coral_meta["license_url"] == coral_meta["license_evidence_value"] == "https://creativecommons.org/licenses/by/4.0/", "CoralWatch current license evidence")
    require(coral_meta["source_record_url"].endswith("/" + survey) and coral_meta["license_evidence_url"] == coral_meta["source_record_url"] and bool(coral_meta["source_attribution_verbatim"]), "CoralWatch attribution/license source")
    require(coral_meta["csv_sha256"] == index["files"]["coral/coralwatch_random_survey_20.csv"]["sha256"], "CoralWatch metadata hash")
    require(len({r["sample_id"] for r in coral}) == 20 and set(coral[0]) == set(coral_meta["schema"]), "CoralWatch sample IDs/schema")
    for row in coral:
        require(row["survey_record_id"] == survey and bool(row["coral_form"]), "CoralWatch row identity/form")
        require(instant(row["event_datetime_source"]) == instant(coral_meta["event_datetime_source"]) and row["country"] == coral_meta["country"] and row["reef_context"] == coral_meta["reef_context"], "CoralWatch survey time/context")
        light = integer(row["lightest_colour_score"], 1, 6)
        dark = integer(row["darkest_colour_score"], 1, 6)
        require(light <= dark and number(row["average_colour_score"], 1, 6) == (light + dark) / 2, "CoralWatch paired arithmetic")

    cholera = documents["cholera/provenance.json"]
    require(cholera["source_revision"] == "476f6dd5a8430e6eb823e79614fda1d7e12a78fb" and "GPL-3.0" in cholera["upstream_repository_license"], "cholera revision/terms")
    for name, evidence in cholera["files"].items():
        require(hashlib.sha256((directory / "cholera" / name).read_bytes()).hexdigest() == evidence["sha256"], f"cholera provenance hash: {name}")
    require(hashlib.sha256((directory / "cholera/LICENSE").read_bytes()).hexdigest() == "3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986", "retained GPL-3.0 notice changed")
    deaths, pumps = rows("cholera/cholera_deaths.csv"), rows("cholera/pumps.csv")
    require(len(deaths) == 250 and len(pumps) == 8 and sum(integer(r["DEATHS"], 1, 489) for r in deaths) == 489, "cholera weighted totals")
    for table in [deaths, pumps]:
        require(len({r["FID"] for r in table}) == len(table), "duplicate cholera IDs")
        for row in table:
            number(row["LON"], -1, 1)
            number(row["LAT"], 51, 52)

    noaa = documents["noaa/raw.json"]
    require(noaa["metadata"]["id"] == "8638610" and noaa["metadata"]["name"] == "Sewells Point", "NOAA station identity")
    require(number(noaa["metadata"]["lat"], -90, 90) == 36.9428 and number(noaa["metadata"]["lon"], -180, 180) == -76.3286, "NOAA station coordinates")
    monthly = rows("noaa/monthly.csv")
    require(len(noaa["data"]) == len(monthly) == 300, "NOAA record count")
    require([(int(r["year"]), int(r["month"])) for r in monthly] == [(y, m) for y in range(2000, 2025) for m in range(1, 13)], "NOAA consecutive selection")
    for raw, tidy in zip(noaa["data"], monthly):
        require(integer(raw["year"], 2000, 2024) == int(tidy["year"]) and integer(raw["month"], 1, 12) == int(tidy["month"]), "NOAA raw/tidy date")
        for source_field, target in [("MSL", "msl_m"), ("highest", "highest_m"), ("lowest", "lowest_m")]:
            require(number(raw[source_field], -10, 10) == number(tidy[target], -10, 10), "NOAA raw/tidy meters")
        require(float(raw["lowest"]) <= float(raw["MSL"]) <= float(raw["highest"]) and str(raw["inferred"]) == tidy["inferred"] and integer(raw["inferred"], 0, 1) in [0, 1], "NOAA extrema/inference fields")

    def bbox(values):
        require(isinstance(values, list) and len(values) == 4, "STAC WGS84 bounding box")
        west, south, east, north = values
        require(number(west, -180, 180) <= number(east, -180, 180) and number(south, -90, 90) <= number(north, -90, 90), "STAC bbox order/bounds")
        return values

    def collection(body, identifier, license_label):
        require(body["type"] == "Collection" and body["id"] == identifier and body["license"] == license_label, f"STAC collection identity/license: {identifier}")
        require(body["stac_version"].startswith("1.") and bool(body["title"]) and bool(body["description"]), "STAC collection required fields")
        require(isinstance(body["links"], list) and any(link["rel"] == "self" for link in body["links"]), "STAC collection links")
        for link in body["links"]:
            require(bool(link["rel"]) and link["href"].startswith("https://"), "STAC collection link URL")
        for extent in body["extent"]["spatial"]["bbox"]:
            bbox(extent)
        for start, end in body["extent"]["temporal"]["interval"]:
            start_time, end_time = instant(start) if start is not None else None, instant(end) if end is not None else None
            require(start_time is None or end_time is None or start_time <= end_time, "STAC collection temporal extent")
        require(bool(body["extent"]["spatial"]["bbox"]) and bool(body["extent"]["temporal"]["interval"]), "STAC collection extents missing")

    def item(body, identifier):
        require(body["type"] == "Feature" and body["collection"] == identifier and isinstance(body["id"], str) and bool(body["id"]) and body["stac_version"].startswith("1."), "STAC Item identity")
        west, south, east, north = bbox(body["bbox"])
        geometry = body["geometry"]
        require(geometry["type"] in ["Polygon", "MultiPolygon"], "STAC footprint type")
        polygons = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
        require(bool(polygons), "STAC empty footprint")
        for polygon in polygons:
            require(bool(polygon), "STAC empty polygon")
            for ring in polygon:
                require(len(ring) >= 4 and ring[0] == ring[-1], "STAC polygon closure")
                for point in ring:
                    require(len(point) >= 2, "STAC position shape")
                    number(point[0], -180, 180)
                    number(point[1], -90, 90)
                    require(west - 1e-6 <= point[0] <= east + 1e-6 and south - 1e-6 <= point[1] <= north + 1e-6, "STAC geometry/bbox mismatch")
        require(isinstance(body["assets"], dict) and bool(body["assets"]), "STAC assets missing")
        for asset in body["assets"].values():
            require(asset["href"].startswith(("https://", "s3://")) and bool(asset["type"]), "STAC asset URL/media type")
        return instant(body["properties"]["datetime"])

    world_collection, sent_collection = documents["stac/worldpop-collection.json"], documents["stac/sentinel-collection.json"]
    collection(world_collection, "UGA", "CC-BY-4.0")
    collection(sent_collection, "sentinel-2-l2a", "proprietary")
    require(any(link["rel"] == "license" and link["href"] in ["https://sentinel.esa.int/documents/247904/690755/Sentinel_Data_Legal_Notice", SOURCES["sentinel"]["terms_url"]] for link in sent_collection["links"]), "Sentinel current legal notice")
    world = documents["stac/worldpop-item.json"]
    require(world["id"] == "UGA_DUG_2020" and item(world, "UGA").year == 2020, "WorldPop reference item/year")
    wp = world["properties"]
    require(wp["year"] == 2020 and wp["project"] == "Degree of Urbanisation" and wp["Digital Object Identifier (DOI)"] == "10.5258/SOTON/WP00879" and "TIFFTAG_COPYRIGHT: CC-BY-4.0" in wp["data:band_1"], "WorldPop product/copyright evidence")
    sentinel = documents["stac/sentinel-search.json"]
    require(sentinel["type"] == "FeatureCollection" and len(sentinel["features"]) == 8 and len({f["id"] for f in sentinel["features"]}) == 8, "Sentinel returned sample")
    start, end = instant("2024-01-01T00:00:00Z"), instant("2024-02-01T00:00:00Z")
    for feature in sentinel["features"]:
        acquired = item(feature, "sentinel-2-l2a")
        require(start <= acquired < end and re.fullmatch(r"S2[AB]_[0-9]{2}[A-Z]{3}_[0-9]{8}_[0-9]+_L2A", feature["id"]) and feature["id"].split("_")[2] == acquired.strftime("%Y%m%d"), "Sentinel date/ID selection")
        number(feature["properties"]["eo:cloud_cover"], 0, 100)
        west, south, east, north = feature["bbox"]
        require(west <= 26.2 and east >= 25.7 and south <= -24.4 and north >= -24.9, "Sentinel bbox does not intersect query")

    earthquakes, tidy_events = documents["usgs/events.geojson"], rows("usgs/events.csv")
    require(earthquakes["type"] == "FeatureCollection" and len(earthquakes["features"]) == len(tidy_events) == 78, "USGS event count/type")
    require(len({f["id"] for f in earthquakes["features"]}) == 78, "USGS duplicate IDs")
    for feature, tidy in zip(earthquakes["features"], tidy_events):
        require(feature["type"] == "Feature" and feature["geometry"]["type"] == "Point", "USGS event geometry")
        lon, lat, depth = feature["geometry"]["coordinates"]
        props = feature["properties"]
        require(feature["id"] == tidy["id"] and props["magType"] in ["mb", "mww", "mwr"] and props["place"] == tidy["place"], "USGS identity/type/place")
        for raw, field, low, high in [(lon, "longitude", 128, 148), (lat, "latitude", 30, 46), (depth, "depth_km", -10, 800), (props["mag"], "magnitude", 4.5, 10)]:
            require(number(raw, low, high) == number(tidy[field], low, high), f"USGS raw/tidy {field}")
        timestamp = datetime.fromtimestamp(number(props["time"], 0, 4_000_000_000_000) / 1000, timezone.utc)
        updated = datetime.fromtimestamp(number(props["updated"], 0, 4_000_000_000_000) / 1000, timezone.utc)
        require(start <= timestamp < end and updated >= timestamp and instant(tidy["time_utc"]) == timestamp and instant(tidy["updated_utc"]) == updated, "USGS date/revision fields")
        require(tidy["magnitude_type"] == props["magType"] and tidy["source_url"] == props["url"] and props["url"].startswith("https://earthquake.usgs.gov/earthquakes/eventpage/"), "USGS type/source URL")


def refresh() -> None:
    expected_parent = (ROOT / "content/repository_examples").resolve()
    if DEST.resolve().parent != expected_parent or not expected_parent.is_relative_to(ROOT.resolve()):
        raise ValueError("Refusing refresh outside the companion workspace")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    # mkdir inherits the workspace ACL on Windows; tempfile's private 0700 ACL
    # can make the eventual published directory unreadable to build accounts.
    stage = DEST.parent / (".data-refresh-" + uuid.uuid4().hex)
    stage.mkdir()
    def contained(path):
        resolved = path.resolve()
        if resolved.parent != expected_parent or resolved.name not in [stage.name, ".data-previous", "data"]:
            raise ValueError(f"Unsafe refresh directory: {resolved}")
        return resolved
    manifest = {"version": 1, "retrieved_utc": datetime.now(timezone.utc).isoformat(), "sources": SOURCES, "files": {}}

    def add(name, data, source, url=None, columns=None, rows=None, transformation=None):
        path = stage / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        manifest["files"][name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "source": source, "url": url, "columns": columns, "rows": rows, "transformation": transformation,
                                  **transport_fingerprints(name, data)}

    def download(name, source, url):
        data = fetch(url)
        add(name, data, source, url)
        return data

    try:
        connections = [
            ("Related", "09", "Browser/native GIS boundaries and small GeoJSON exchange", "No repository-wide license"),
            ("Related", "06,09", "WorldPop metadata and an external native RustGIS handoff", "No repository-wide license"),
            ("Related", "06,09", "Original geographic story sequence; never import invented TB attributes", "No repository-wide license"),
            ("Related", "01,09", "Filtered tidy data and provenance before geographic exchange", "MIT software; separate data terms"),
            ("Related", "02,08", "Global anomaly and paired citizen-science survey evidence", "MIT software; scoped CC BY/CC0; separate data"),
            ("Related", "06", "Bounded STAC metadata discovery and provider-specific terms", "MIT original content; separate data terms"),
            ("Related", "03,07", "Small multiples and scene controls; use NOAA/USGS observations", "MIT software; scoped CC BY/CC0; separate data"),
            ("Related", "09", "Source inventory and approximate locality narrative pattern", "README MIT assertion; no license file"),
            ("Related", "01,09", "Linked views, fixed seeds and honest simulation boundaries", "MIT software; scoped CC BY; separate data"),
            ("PHI", "01,09", "Decision, evidence, activity and limitation as a case structure", "AGPL-3.0 file; individual case terms separate"),
            ("PHI", "04,05", "Historical weighted point maps; retain GPL data bundle", "GPL-3.0 file; provenance retained"),
            ("PHI", "04", "Compare spot symbols and weighted centers with original code", "Apache-2.0 code; data rights not established there"),
            ("PHI", "01", "Polar-area question seed; no workbook/figures imported", "Apache-2.0 code; external assets separate"),
            ("PHI", "01,09", "Progressive investigation narrative; source exercises are simulated", "Apache-2.0 code; external assets separate"),
            ("PHI", "01,09", "Keep person/place/time years and denominators explicit", "Apache-2.0 code; external assets separate"),
            ("PHI", "06", "Footprint and QA discussion; no large NO2 pipeline or causal claim", "Apache-2.0 code; external assets separate"),
            ("PHI", "05", "Independent masking experiment and privacy/utility critique", "README Apache assertion; no license file"),
            ("PHI", "01,09", "Join and missingness questions; no unverified Kaggle data copied", "GPL-3.0 file; data terms unverified"),
        ]
        atlas = []
        for document in ["related-repositories.md", "phi-case-studies.md"]:
            text = (ROOT / "docs/expansion" / document).read_text(encoding="utf-8")
            atlas.extend(re.findall(r"\| \[([^\]]+)\]\((https://github.com/[^\s)]+/blob/([0-9a-f]{40})/README.md)\)", text))
        assert len(atlas) == len(connections) == 18
        rows = [{"repository": name, "readme_url": url, "commit": commit, "collection": connection[0], "lessons": connection[1], "connection": connection[2], "rights_evidence": connection[3]} for (name, url, commit), connection in zip(atlas, connections)]
        add("repository_atlas.csv", csv_bytes(rows), "atlas", columns=list(rows[0]), rows=18, transformation="Pinned README/commit facts extracted from the two reviewed repository tables; original lesson connections and scoped rights summaries")
        for filename in ["nasa-gistemp-raw.csv", "global-temperature.csv", "provenance.json"]:
            download("nasa/" + filename, "nasa", CLIMATE + filename)
        nasa = list(csv.DictReader((stage / "nasa/global-temperature.csv").open(encoding="utf-8")))
        assert len(nasa) == 146 and set(nasa[0]) == {"year", "anomaly_c", "data_type"}
        manifest["files"]["nasa/global-temperature.csv"].update(columns=list(nasa[0]), rows=len(nasa))
        for filename in ["coralwatch_random_survey_20.csv", "coralwatch_random_survey_20.metadata.json"]:
            download("coral/" + filename, "coral", CLIMATE + filename)
        coral = list(csv.DictReader((stage / "coral/coralwatch_random_survey_20.csv").open(encoding="utf-8")))
        assert len(coral) == 20
        manifest["files"]["coral/coralwatch_random_survey_20.csv"].update(columns=list(coral[0]), rows=20)
        for filename in ["cholera_deaths.csv", "pumps.csv", "README.md", "provenance.json", "LICENSE"]:
            download("cholera/" + filename, "cholera", CHOLERA + filename)
        for filename, count, expected in [("cholera_deaths.csv", 250, "1be1926dca480fe8c9a83b663e62758e57c7ebe6c296d6a32c5e93a50d62b40a"), ("pumps.csv", 8, "6ad041659f2dc2abf9048aa4c08c01a9a7d181bd19684f76c74b7df7a4b4b830")]:
            record = manifest["files"]["cholera/" + filename]
            assert record["sha256"] == expected, f"Pinned source changed: {filename}"
            rows = list(csv.DictReader((stage / "cholera" / filename).open(encoding="utf-8-sig")))
            assert len(rows) == count
            record.update(columns=list(rows[0]), rows=count)
        noaa = json.loads(download("noaa/raw.json", "noaa", NOAA))
        rows = [{"year": int(r["year"]), "month": int(r["month"]), "msl_m": float(r["MSL"]), "highest_m": float(r["highest"]), "lowest_m": float(r["lowest"]), "inferred": r["inferred"]} for r in noaa["data"]]
        assert len(rows) == 300 and len({(r["year"], r["month"]) for r in rows}) == 300
        add("noaa/monthly.csv", csv_bytes(rows), "noaa", columns=list(rows[0]), rows=300, transformation="raw.data: year/month to integer; MSL/highest/lowest to meter-valued numbers; inferred retained; no interpolation")
        item = json.loads(download("stac/worldpop-item.json", "worldpop", "https://api.stac.worldpop.org/collections/UGA/items/UGA_DUG_2020"))
        assert item["id"] == "UGA_DUG_2020" and item["type"] == "Feature"
        download("stac/worldpop-collection.json", "worldpop", "https://api.stac.worldpop.org/collections/UGA")
        sentinel = json.loads(download("stac/sentinel-search.json", "sentinel", SENTINEL))
        assert sentinel["type"] == "FeatureCollection" and len(sentinel["features"]) == 8
        download("stac/sentinel-collection.json", "sentinel", "https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a")
        earthquakes = json.loads(download("usgs/events.geojson", "usgs", USGS))
        assert earthquakes["type"] == "FeatureCollection" and len(earthquakes["features"]) == 78
        rows = []
        for f in earthquakes["features"]:
            p, c = f["properties"], f["geometry"]["coordinates"]
            rows.append({"id": f["id"], "longitude": c[0], "latitude": c[1], "depth_km": c[2], "time_utc": datetime.fromtimestamp(p["time"] / 1000, timezone.utc).isoformat(), "magnitude": p["mag"], "magnitude_type": p["magType"], "place": p["place"], "updated_utc": datetime.fromtimestamp(p["updated"] / 1000, timezone.utc).isoformat(), "source_url": p["url"]})
        add("usgs/events.csv", csv_bytes(rows), "usgs", columns=list(rows[0]), rows=len(rows), transformation="GeoJSON point coordinates preserved as lon/lat/depth_km; time/updated UTC milliseconds converted to ISO 8601; reported magnitudes and types retained")
        download("notices/CC-BY-4.0.txt", "coral", "https://raw.githubusercontent.com/jltobias/JupyterLite-Climate-and-Health/248f9860d189502013b36b3c4271777edafc4f7f/licenses/CC-BY-4.0.txt")
        notices = "# Companion snapshot reuse and attribution\n\nProject licensing remains undecided. No upstream repository's general software license is assigned to this collection. Dataset and metadata rights remain separate.\n\n"
        for key, source in SOURCES.items():
            notices += f"## {source['title']}\n\n{source['attribution']}.\n\n{source['terms']}\n\nTerms/citation: {source['terms_url']}\n\n{source['limitation']}\n\n"
        notices += "The NASA, CoralWatch and cholera upstream provenance files are retained byte-for-byte. GPL-3.0 is retained in cholera/LICENSE; CC BY 4.0 is retained in notices/CC-BY-4.0.txt. WorldPop and Sentinel collection/item license metadata are retained. Sentinel attribution above describes the metadata selection; no satellite pixels are bundled. Queries, retrieval UTC, file checksums, schemas and transformations are in manifest.json. Raw inputs must not be overwritten by notebook exports.\n"
        add("NOTICES.md", notices.encode("utf-8"), "notices", transformation="Original source/terms register compiled from inspected input evidence")
        (stage / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        validate_staged(stage)
        # Rename the complete validated directory only. Roll back if replacement fails.
        backup = DEST.with_name(".data-previous")
        for directory in [stage, DEST, backup]:
            contained(directory)
        if backup.exists():
            raise RuntimeError(f"Recover/remove stale backup before refreshing: {backup}")
        if DEST.exists():
            DEST.rename(backup)
        try:
            stage.rename(DEST)
        except Exception:
            if backup.exists():
                backup.rename(DEST)
            raise
        if backup.exists():
            shutil.rmtree(contained(backup))
        print(f"Refreshed {len(manifest['files'])} files atomically in {DEST}")
    finally:
        if stage.exists():
            shutil.rmtree(contained(stage))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Explicitly download and replace the bounded snapshots")
    if not parser.parse_args().refresh:
        parser.error("Pass --refresh; builds and lessons use committed local snapshots")
    refresh()
