"""Package the original earthquake story from checksum-validated local evidence."""
from __future__ import annotations

import csv
import hashlib
from html import escape
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "content/repository_examples"
sys.path.insert(0, str(LESSONS))
import repo_examples as rx


def package() -> None:
    rx.validate_all()
    destination = ROOT / "static/repository-examples"
    destination.mkdir(parents=True, exist_ok=True)
    events = list(csv.DictReader(rx.checked_path("usgs/events.csv").open(encoding="utf-8")))
    for event in events:
        for key in ["longitude", "latitude", "depth_km", "magnitude"]:
            event[key] = float(event[key])
    index = rx.manifest()
    metadata = {"title": "USGS January 2024 Japan earthquake teaching selection", "source": index["files"]["usgs/events.geojson"]["url"],
                "retrieved_utc": index["retrieved_utc"], "credit": "U.S. Geological Survey Earthquake Hazards Program",
                "terms": index["sources"]["usgs"]["terms"], "terms_url": index["sources"]["usgs"]["terms_url"],
                "units": "longitude/latitude degrees; depth_km positive downward; UTC ISO 8601; reported magnitude/type",
                "projection": "Local equirectangular approximation; origin 138 E, 38 N; sphere radius 6371 km; scene z=-depth_km × visible exaggeration",
                "geometry": "GIS handoff uses 2D WGS84 lon/lat; depth remains a named property, not GeoJSON altitude",
                "selection": "2024-01-01 inclusive to 2024-02-01 exclusive UTC, magnitude >=4.5, latitude 30–46, longitude 128–148",
                "limitations": "Catalog selection, revised events and mixed magnitude types; distortion in the local approximation; no location/depth uncertainty, fault surface or prediction"}
    payload = {"metadata": metadata, "events": events}
    raw = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    (destination / "scene-data.json").write_bytes(raw)
    (destination / "events.csv").write_bytes(rx.checked_path("usgs/events.csv").read_bytes())
    handoff = {"type": "FeatureCollection", "metadata": metadata, "features": [
        {"type": "Feature", "id": event["id"], "geometry": {"type": "Point", "coordinates": [event["longitude"], event["latitude"]]},
         "properties": {k: v for k, v in event.items() if k not in ["longitude", "latitude", "id"]}}
        for event in events]}
    (destination / "earthquake-handoff.geojson").write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (destination / "provenance.json").write_text(json.dumps({**metadata, "input_sha256": index["files"]["usgs/events.geojson"]["sha256"], "scene_sha256": hashlib.sha256(raw).hexdigest(), "transformation": "Select tidy source fields; numeric conversion only; all 78 events preserved. Optional scene filtering happens locally. GeoJSON geometry is two-dimensional and unexaggerated."}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rows = "\n".join("<tr>" +
        f'<td><a href="{escape(event["source_url"], quote=True)}" aria-label="Open USGS event {escape(event["id"], quote=True)} source">{escape(event["id"])}</a></td>' +
        "".join(f"<td>{escape(str(event[key]))}</td>" for key in ["time_utc", "longitude", "latitude", "depth_km", "magnitude", "magnitude_type", "place"]) + "</tr>" for event in events)
    template = (destination / "story.template.html").read_text(encoding="utf-8")
    html = template.replace("<!-- EVENT_ROWS -->", rows).replace("SCENE_SHA256", hashlib.sha256(raw).hexdigest()).replace("SNAPSHOT_RETRIEVED_UTC", escape(index["retrieved_utc"]))
    (destination / "index.html").write_text(html, encoding="utf-8")
    print(f"Packaged original story: {len(events)} USGS events, table, CSV, GeoJSON and provenance")


if __name__ == "__main__":
    package()
