"""Check advertised destinations, published notebooks, and the removed artwork."""

import base64
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist"
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
    ]
    for relative in expected:
        assert (SITE / relative).is_file(), f"Missing advertised destination: {relative}"
    # The real loader fetches index.html at both levels and reads this element.
    # A parent landing page without it returns HTTP 200 but prevents lab startup.
    for relative in ["index.html", "lab/index.html"]:
        page = Links()
        page.feed((SITE / relative).read_text(encoding="utf-8"))
        assert isinstance(page.config, dict), f"Missing JupyterLite startup configuration in {relative}"
    for page in [SITE / "index.html", SITE / "ai-demo/index.html"]:
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
    notices = json.loads((SITE / "third-party-licenses/index.json").read_text(encoding="utf-8"))
    assert all(record["files"] for record in notices), "A distribution's license files were not exported"
    print("Site checks passed: landing, book, lab, fresh notebook, splash, licenses, and no removed artwork.")


if __name__ == "__main__":
    main()
