"""Check advertised destinations, published notebooks, and the removed artwork."""

import ast
import base64
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist"
COMPANIONS = sorted((ROOT / "content/repository_examples").glob("[0-9][0-9]_*.ipynb"))
REMOVED_ARTWORK = "689c3f7c25eadff15c030ba2f32ac952f29285c4ec607206882ff120f688ac89"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.config = None
        self._config_parts = None

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "jupyter-config-data":
            self._config_parts = []
        for key, value in attrs:
            if key in ("href", "src") and value:
                self.targets.append(value)

    def handle_data(self, data):
        if self._config_parts is not None:
            self._config_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._config_parts is not None:
            self.config = json.loads("".join(self._config_parts))
            self._config_parts = None


def main():
    expected = [
        "index.html", "book/index.html", "book/intro.html", "lab/index.html",
        "ai-demo/index.html", "assets/visualization-splash.png", "build-info.json",
        "third-party-licenses/index.json", "files/visualization_methods_v2.ipynb",
        "book/content/repository_examples/index.html", "files/repository_examples/repo_examples.py",
        "files/repository_examples/data/manifest.json", "repository-examples/index.html",
        "repository-examples/story.js", "repository-examples/story.css",
        "repository-examples/scene-data.json", "repository-examples/events.csv",
        "repository-examples/earthquake-handoff.geojson", "repository-examples/provenance.json",
    ]
    assert len(COMPANIONS) == 9, "Expected nine companion notebooks"
    for source in COMPANIONS:
        expected.extend([f"files/repository_examples/{source.name}",
                         f"book/content/repository_examples/{source.stem}.html"])
    for relative in expected:
        assert (SITE / relative).is_file(), f"Missing advertised destination: {relative}"
    # The real loader fetches index.html at both levels and reads this element.
    # A parent landing page without it returns HTTP 200 but prevents lab startup.
    for relative in ["index.html", "lab/index.html"]:
        page = Links()
        page.feed((SITE / relative).read_text(encoding="utf-8"))
        assert isinstance(page.config, dict), f"Missing JupyterLite startup configuration in {relative}"
    linked_pages = [SITE / "index.html", SITE / "ai-demo/index.html", SITE / "repository-examples/index.html",
                    SITE / "book/content/repository_examples/index.html"]
    linked_pages.extend(SITE / f"book/content/repository_examples/{source.stem}.html" for source in COMPANIONS)
    for page in linked_pages:
        links = Links()
        links.feed(page.read_text(encoding="utf-8"))
        for target in links.targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (page.parent / unquote(parsed.path)).resolve()
            if destination.is_dir():
                destination /= "index.html"
            assert destination.is_file(), f"Broken link in {page.name}: {target}"
    for path in (SITE / "files").rglob("*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        code = "\n".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code")
        syntax = ast.parse(code)
        if any(isinstance(node, ast.Attribute) and node.attr == "style" for node in ast.walk(syntax)):
            # Styler's optional dependency is not pulled in by installing pandas.
            browser_packages = set()
            for node in ast.walk(syntax):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and isinstance(node.func.value, ast.Name) and node.func.value.id == "piplite"
                        and node.func.attr == "install" and node.args):
                    requested = ast.literal_eval(node.args[0])
                    browser_packages.update([requested] if isinstance(requested, str) else requested)
            assert "jinja2" in browser_packages, f"Styled table missing browser Jinja2 dependency: {path}"
        for cell in notebook["cells"]:
            for attachment in cell.get("attachments", {}).values():
                for mime, value in attachment.items():
                    if mime.startswith("image/"):
                        encoded = "".join(value) if isinstance(value, list) else value
                        assert hashlib.sha256(base64.b64decode(encoded)).hexdigest() != REMOVED_ARTWORK, path
    for path in SITE.rglob("*.png"):
        assert hashlib.sha256(path.read_bytes()).hexdigest() != REMOVED_ARTWORK, path
    source = ROOT / "content" / "periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.ipynb"
    assert json.loads(source.read_text(encoding="utf-8")) == json.loads(
        (SITE / "files/visualization_methods_v2.ipynb").read_text(encoding="utf-8")
    ), "Release notebook differs from the maintained source"
    assert "visualization-splash.png" in (ROOT / "README.md").read_text(encoding="utf-8")
    catalog = SITE / "book/content/periodic_table_visualization_methods_python_examples_jupyterlite_REVISED.html"
    catalog_links = Links()
    catalog_links.feed(catalog.read_text(encoding="utf-8"))
    figure_sources = [s for s in catalog_links.targets if "_images/" in s or s.startswith("data:image/")]
    assert len(figure_sources) >= 90, "Catalog executed without the expected rendered figures"
    for source in COMPANIONS:
        published = SITE / "files/repository_examples" / source.name
        assert json.loads(source.read_text(encoding="utf-8")) == json.loads(published.read_text(encoding="utf-8")), published
        page = Links()
        page.feed((SITE / f"book/content/repository_examples/{source.stem}.html").read_text(encoding="utf-8"))
        figures = [s for s in page.targets if "_images/" in s or s.startswith("data:image/")]
        assert len(figures) >= 3, f"Companion Book page lacks rendered figures: {source.name}"
        for target in figures:
            if not target.startswith("data:"):
                assert ((SITE / "book/content/repository_examples") / unquote(urlsplit(target).path)).resolve().is_file(), target
    packaged = SITE / "files/repository_examples/data"
    index = json.loads((packaged / "manifest.json").read_text(encoding="utf-8"))
    assert (packaged / "manifest.json").read_bytes() == (ROOT / "content/repository_examples/data/manifest.json").read_bytes()
    for name, record in index["files"].items():
        assert record["source"] in index["sources"], name
        assert hashlib.sha256((packaged / name).read_bytes()).hexdigest() == record["sha256"], f"Published snapshot differs: {name}"
    assert not (SITE / "files/repository_examples/exports").exists(), "Personal/generated exports entered Lite content"
    assert not list((SITE / "files/repository_examples").glob(".data-*")), "Snapshot staging directory entered publication"
    scene = SITE / "repository-examples"
    provenance = json.loads((scene / "provenance.json").read_text(encoding="utf-8"))
    assert hashlib.sha256((scene / "scene-data.json").read_bytes()).hexdigest() == provenance["scene_sha256"]
    scene_html = (scene / "index.html").read_text(encoding="utf-8")
    assert provenance["scene_sha256"] in scene_html and scene_html.count("<tr>") == 79, "Scene lacks its complete static table/checksum"
    handoff = json.loads((scene / "earthquake-handoff.geojson").read_text(encoding="utf-8"))
    assert len(handoff["features"]) == 78
    assert all(len(f["geometry"]["coordinates"]) == 2 and "depth_km" in f["properties"] for f in handoff["features"]), "Depth was confused with GeoJSON altitude"
    notices = json.loads((SITE / "third-party-licenses/index.json").read_text(encoding="utf-8"))
    assert all(record["files"] for record in notices), "A distribution's license files were not exported"
    print("Site checks passed: landing, book, lab, fresh notebook, nine rendered companions, validated data, story/GIS routes, splash, licenses, and no removed artwork.")


if __name__ == "__main__":
    main()
