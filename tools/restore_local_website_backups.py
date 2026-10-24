"""Publish inspected local-backup supplements without executing historical code.

D: is an input-only archive. Outputs are confined to this repository on C:.
Requires beautifulsoup4. Run from the repository with its Python environment.
Wayback source bytes and original recovery statuses remain unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit

from bs4 import BeautifulSoup, Comment

REPO = Path(__file__).resolve().parents[1]
STAGING = REPO / ".cache/local-website-backups"
OLD = STAGING / "old" if (STAGING / "old").is_dir() else Path(r"D:\Website Archive\Websites\Backups\Personal\Personal")
NEW = STAGING / "later" if (STAGING / "later").is_dir() else Path(r"D:\Website Archive\Websites\Personal\2023")
SOURCE_ROOTS = {"old": OLD, "later": NEW}
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".ico"}
DOWNLOADS = {".jar", ".class"}
CSS_URL = re.compile(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", re.I)
DATE = "October 21, 2026"
CSP = "default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'none'; connect-src 'none'; object-src 'none'; frame-src 'none'; form-action 'none'; base-uri 'none'"
STYLE = "body{font:16px/1.6 system-ui,sans-serif;margin:0;background:#f4f3ef;color:#222}main{max-width:1000px;margin:auto;padding:28px 22px}a{color:#175b85}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:13px}td,th{padding:8px;text-align:left;border-bottom:1px solid #bbb;overflow-wrap:anywhere}.backup-notice{background:#162e3b;color:#fff;padding:12px 20px;font:14px/1.5 system-ui,sans-serif;text-align:center;position:relative;z-index:1000}.backup-notice a{color:#bce7ff}.backup-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}.backup-grid figure{margin:0}.backup-grid img{max-height:220px;object-fit:contain}code{overflow-wrap:anywhere}"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def key(url: str) -> str:
    u = urlsplit(url)
    return unquote(u.path).lower().rstrip("/") or "/"


def slug(relative: Path) -> str:
    return "/".join(re.sub(r"[^a-z0-9._-]", "_", p.lower()) for p in relative.parts)


def relative(target: Path, current: Path) -> str:
    return os.path.relpath(target, current.parent).replace("\\", "/")


def shell(title: str, body: str) -> str:
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta http-equiv="Content-Security-Policy" content="{CSP}"><title>{html.escape(title)}</title><style>{STYLE}</style></head><body><main>{body}</main></body></html>'


def flatten_frameset(soup: BeautifulSoup) -> bool:
    """Expose legacy frame destinations without weakening the static-page CSP."""
    frameset = soup.find("frameset")
    if frameset is None:
        return False
    body = soup.new_tag("body")
    main = soup.new_tag("main")
    main["style"] = "max-width:900px;margin:auto;padding:28px 22px;font:16px/1.6 system-ui,sans-serif"
    heading = soup.new_tag("h1")
    heading.string = soup.title.get_text() if soup.title else "Recovered website"
    main.append(heading)
    note = soup.new_tag("p")
    note.string = "This website originally used a Flash title and separate frames. Open its surviving pages below; the original frame layout is preserved in the source text."
    main.append(note)
    links = soup.new_tag("ul")
    for frame in frameset.find_all("frame"):
        value = frame.get("src", "")
        if not value or urlsplit(value).path.lower().endswith(".swf"):
            continue
        row = soup.new_tag("li")
        anchor = soup.new_tag("a", href=value)
        anchor.string = {"list": "Browse the fireworks catalog", "product": "Open the original home page"}.get(frame.get("name"), frame.get("name") or value)
        row.append(anchor)
        links.append(row)
    main.append(links)
    body.append(main)
    frameset.replace_with(body)
    return True


class Supplement:
    def __init__(self, year: int):
        self.root = REPO / f"docs/assets/media/quinndamerell-homepage-{year}"
        if self.root.drive.lower() != "c:" or not self.root.is_relative_to(REPO):
            raise ValueError("Outputs must remain in this repository on C:")
        self.year = year
        self.manifest = json.loads((self.root / "manifest.json").read_text(encoding="utf-8"))
        self.records = {key(r["original_url"]): r for r in self.manifest["files"]}
        self.base = self.root / "site/local-backup"
        self.sources = self.root / "local-backup-sources"
        self.copied = {}
        self.pages = {}
        self.entries = []
        self.generated = set()
        self.gaps = {}
        self.gap_bridges = 0
        self.gallery_repairs = 0

    def write(self, target: Path, data: str | bytes):
        if not target.resolve().is_relative_to(self.root.resolve()):
            raise ValueError("Output escaped archive")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)
        self.generated.add(target)

    def identify(self, source: Path):
        for label, root in SOURCE_ROOTS.items():
            if source.is_relative_to(root):
                return label, source.relative_to(root)
        raise ValueError(f"Unexpected input: {source}")

    def source_url(self, source: Path):
        return "http://www.quinndamerell.com/" + self.identify(source)[1].as_posix()

    def add_source(self, source: Path, output: Path, data: bytes, note=""):
        label, source_relative = self.identify(source)
        self.entries.append({"source_collection": label, "source_relative_path": source_relative.as_posix(),
            "source_sha256": sha(source.read_bytes()), "source_bytes": source.stat().st_size,
            "published_path": output.relative_to(self.root).as_posix(), "published_sha256": sha(data),
            "published_bytes": len(data), "transformation": note or "Exact local-backup bytes"})

    def copy_asset(self, source: Path) -> Path | None:
        if source.suffix.lower() not in IMAGES | DOWNLOADS | {".css"}:
            return None
        if source in self.copied:
            return self.copied[source]
        label, source_relative = self.identify(source)
        output = self.base / label / slug(source_relative)
        self.copied[source] = output
        data = source.read_bytes()
        note = ""
        if source.suffix.lower() == ".css":
            text = data.decode("utf-8", errors="replace")
            text = re.sub(r"@import\s+[^;]+;", "", text, flags=re.I)
            text = re.sub(r"expression\s*\([^;]+", "", text, flags=re.I)
            text = CSS_URL.sub(lambda m: 'url("' + self.resource(m[1].strip(), source, output) + '")', text)
            data = text.encode("utf-8")
            note = "CSS resource URLs rewritten locally; imports and expressions removed"
        self.write(output, data)
        self.add_source(source, output, data, note)
        return output

    def resolve(self, value: str, source: Path) -> Path | None:
        url = urlsplit(urljoin(self.source_url(source), value.replace("\\", "/")))
        if url.hostname and url.hostname.lower().removeprefix("www.") != "quinndamerell.com":
            return None
        path = unquote(url.path).lstrip("/")
        preferred = self.identify(source)[0]
        for label in [preferred] + [x for x in SOURCE_ROOTS if x != preferred]:
            root = SOURCE_ROOTS[label]
            candidate = (root / path).resolve()
            if not candidate.is_relative_to(root.resolve()):
                continue
            if candidate.is_file():
                return candidate
            if candidate.is_dir():
                for index in ("index.html", "index.php", "index.htm"):
                    if (candidate / index).is_file():
                        return candidate / index
        return None

    def resource(self, value: str, source: Path, output: Path) -> str:
        if value.startswith("data:"):
            return value
        candidate = self.resolve(value, source)
        saved = self.copy_asset(candidate) if candidate else None
        return relative(saved, output) if saved else "data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22/%3E"

    def destination(self, value: str, source: Path, output: Path) -> str:
        if value.startswith("#"):
            return value
        absolute = urljoin(self.source_url(source), value.replace("\\", "/"))
        u = urlsplit(absolute)
        if u.scheme not in ("http", "https", "") or (u.hostname or "").lower().removeprefix("www.") != "quinndamerell.com":
            return absolute if u.scheme in ("https", "http", "mailto") else relative(self.base / "index.html", output)
        candidate = self.resolve(value, source)
        target = self.pages.get(candidate)
        if not target and candidate:
            target = self.copy_asset(candidate)
        if not target:
            record = self.records.get(key(absolute))
            if record and record.get("served_path"):
                target = self.root / record["served_path"]
        if target:
            return relative(target, output)  # Old cross-page anchors are inconsistent.
        gap_key = sha(absolute.encode())[:12]
        target = self.base / "gaps" / (gap_key + ".html")
        if gap_key not in self.gaps:
            self.gaps[gap_key] = absolute
            self.write(target, shell("Original destination unavailable", f'<p><a href="../index.html">Local backup collection</a></p><h1>Original destination unavailable</h1><p>The old page linked to <code>{html.escape(absolute)}</code>. A usable local copy was not recovered. Original server actions are not reproduced.</p>'))
        return relative(target, output)

    def select(self):
        selections = [OLD / "websites.php", OLD / "projects.php", OLD / "PicGen/index.php", OLD / "ZuneShuffler/index.php", OLD / "RedditTimeMachine/index.php",
                      NEW / "NextBus/index.html", NEW / "TxTBack/index.html", NEW / "ThinkingOfYou/index.html"]
        for folder in (OLD / "websites/Final", OLD / "websites/Friework Web", OLD / "websites/animations", OLD / "java_applets"):
            selections += [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in {".html", ".htm"}]
        for source in selections:
            label, rel = self.identify(source)
            self.pages[source] = (self.base / label / slug(rel)).with_suffix(".html")
        for folder in (OLD / "PicGen", OLD / "ZuneShuffler", OLD / "java_applets"):
            for path in folder.rglob("*"):
                if path.is_file() and path.suffix.lower() in DOWNLOADS:
                    self.copy_asset(path)

    def publish_page(self, source: Path, output: Path):
        original = source.read_bytes()
        public_text = original.decode("utf-8", errors="replace")
        php = source.suffix.lower() == ".php"
        if php:
            public_text = re.sub(r"<\?.*?\?>", "", public_text, flags=re.S)
        label, rel = self.identify(source)
        inert = self.sources / label / (slug(rel) + (".public-html.txt" if php else ".txt"))
        self.write(inert, public_text if php else original)
        self.add_source(source, inert, inert.read_bytes(), "Public HTML extracted; all PHP blocks omitted. Original source hash records the private input, which is not distributed." if php else "Exact original HTML stored inertly as text")
        soup = BeautifulSoup(public_text, "html.parser")
        had_frameset = flatten_frameset(soup)
        for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
            comment.extract()
        for item in soup.find_all(["script", "noscript", "base", "iframe"]):
            item.decompose()
        for item in soup.find_all(["object", "embed", "applet"]):
            if not item.parent:
                continue
            replacement = soup.new_tag("p")
            replacement.string = "Original browser plug-in content is preserved separately. "
            a = soup.new_tag("a", href=relative(REPO / "docs/early-experiments/", output) + "/#flash-animations")
            a.string = "Explore the recovered animations and experiments"
            replacement.append(a)
            item.replace_with(replacement)
        for item in soup.find_all("meta"):
            if item.get("http-equiv", "").lower() in ("refresh", "content-security-policy"):
                item.decompose()
        for form in soup.find_all("form"):
            for control in form.find_all(["input", "button", "select", "textarea"]):
                control["disabled"] = "disabled"
            form.name = "div"
            form.attrs = {"class": "archived-form"}
            note = soup.new_tag("p")
            note.string = "Original form unavailable in this static copy."
            form.insert(0, note)
        for el in soup.find_all(True):
            nav = re.search(r"location(?:\.href)?\s*=\s*['\"]([^'\"]+)", el.get("onclick", ""))
            if nav:
                el.name = "a"
                el["href"] = nav[1]
            for attr in list(el.attrs):
                if attr.lower().startswith("on") or attr in ("srcdoc", "ping", "integrity", "crossorigin"):
                    del el[attr]
            if el.name in ("a", "area"):
                if el.get("href"):
                    el["href"] = self.destination(el["href"], source, output)
                    if urlsplit(el["href"]).scheme:
                        el["target"] = "_blank"
                        el["rel"] = "noopener noreferrer"
                    else:
                        el.attrs.pop("target", None)
                else:
                    el.name = "span"
            for attr in ("src", "background", "poster"):
                if el.get(attr):
                    el[attr] = self.resource(el[attr], source, output)
            if el.name == "link" and el.get("href"):
                el["href"] = self.resource(el["href"], source, output)
            if el.get("style"):
                el["style"] = CSS_URL.sub(lambda m: 'url("' + self.resource(m[1].strip(), source, output) + '")', el["style"])
        for style in soup.find_all("style"):
            style.string = CSS_URL.sub(lambda m: 'url("' + self.resource(m[1].strip(), source, output) + '")', style.get_text())
        if not soup.html:
            soup = BeautifulSoup("<html><head></head><body>" + str(soup) + "</body></html>", "html.parser")
        if not soup.head:
            soup.html.insert(0, soup.new_tag("head"))
        if not soup.body:
            soup.html.append(soup.new_tag("body"))
        if "websites/friework web/" in rel.as_posix().lower() and any(
            re.search(r"position\s*:\s*absolute", tag.get("style", ""), re.I)
            for tag in soup.body.find_all(True)
        ):
            # Web Page Maker placed the catalog and product content absolutely.
            # Give it a containing block below the added provenance notice.
            content = soup.new_tag("div", attrs={"class": "backup-original", "style": "position:relative"})
            for child in list(soup.body.contents):
                content.append(child.extract())
            soup.body.append(content)
        for attrs in ({"charset": "utf-8"}, {"name": "robots", "content": "noindex"}, {"http-equiv": "Content-Security-Policy", "content": CSP}):
            soup.head.insert(0, soup.new_tag("meta", attrs=attrs))
        style = soup.new_tag("style")
        style.string = STYLE.split(".backup-notice", 1)[1].split(".backup-grid", 1)[0]
        style.string = ".backup-notice" + style.string
        soup.head.append(style)
        notice = soup.new_tag("aside", attrs={"class": "backup-notice"})
        notice.append("Recovered from Quinn's local backup on " + DATE + ". Backup date is not the page's creation date. ")
        for title, target in (("Local backup collection", self.base / "index.html"), ("Wayback homepage", self.root / "snapshot.html"), ("Source text", inert)):
            a = soup.new_tag("a", href=relative(target, output))
            a.string = title
            notice.append(a)
            notice.append(" · ")
        soup.body.insert(0, notice)
        data = str(soup).encode("utf-8")
        self.write(output, data)
        self.add_source(source, output, data, "Static browsing derivative: PHP, scripts, trackers and plug-ins removed; local links/resources rewritten; original forms disabled" + ("; legacy frames replaced with links to surviving pages" if had_frameset else ""))

    def recover_gaps(self):
        for r in self.manifest["files"]:
            if r.get("status") != "unavailable":
                continue
            source = self.resolve(r["original_url"], OLD / "index.php")
            target = self.pages.get(source)
            if not target and source and source.suffix.lower() in IMAGES | DOWNLOADS:
                target = self.copy_asset(source)
            if not target:
                continue
            bridge = self.root / (r.get("served_path") or r.get("placeholder_path", ""))
            if not bridge.is_file() or bridge.suffix != ".html":
                continue
            content = f'<p><a href="{relative(self.root / "snapshot.html", bridge)}">Wayback homepage</a> · <a href="{relative(self.base / "index.html", bridge)}">Local backup collection</a></p><h1>A local backup was found</h1><p>The Internet Archive retrieval did not recover <code>{html.escape(r["original_url"])}</code>. Quinn later found a local backup. Its exact historical revision is not established.</p><p><a href="{relative(target, bridge)}">Open the recovered file</a></p>'
            if target.suffix.lower() in IMAGES:
                content += f'<p><a href="{relative(target, bridge)}"><img src="{relative(target, bridge)}" alt="Recovered original image"></a></p>'
            self.write(bridge, shell("Recovered local backup", content))
            r["local_backup"] = {"path": target.relative_to(self.root).as_posix(), "provenance": "Owner-supplied local backup; historical revision unknown"}
            self.gap_bridges += 1
        # Keep the historical gaps as valid navigation targets while restoring
        # larger images to the existing inspected gallery helpers.
        for page in list((self.root / "site").rglob("*.html")):
            if page.is_relative_to(self.base):
                continue
            soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
            changed = False
            for gallery in soup.select("a[href]"):
                if not gallery.find("img"):
                    continue
                gap = (page.parent / unquote(urlsplit(gallery["href"]).path)).resolve()
                record = next((r for r in self.manifest["files"] if r.get("local_backup") and (self.root / r.get("served_path", "")).resolve() == gap), None)
                if not record or Path(record["local_backup"]["path"]).suffix.lower() not in IMAGES:
                    continue
                old_href = gallery["href"]
                gallery["href"] = relative(self.root / record["local_backup"]["path"], page)
                gallery["title"] = "Full image recovered from Quinn's local backup. " + gallery.get("title", "").replace("Only the archived thumbnail was recovered. ", "").replace("Full image recovered from Quinn's local backup. ", "")
                rel = " ".join(gallery.get("rel", []))
                if "lightbox" in rel.lower():
                    gallery["data-archive-gallery" if self.year == 2012 else "data-gallery"] = rel
                note = soup.new_tag("a", href=old_href, attrs={"class": "archive-missing-inline"})
                note.string = "Local backup provenance"
                gallery.insert_after(note)
                changed = True
            for note in soup.select("a.archive-missing-inline[href]"):
                gap = (page.parent / unquote(urlsplit(note["href"]).path)).resolve()
                record = next((r for r in self.manifest["files"] if r.get("local_backup") and (self.root / r.get("served_path", "")).resolve() == gap), None)
                if not record:
                    continue
                gallery = note.find_previous_sibling("a")
                if gallery and gallery.find("img"):
                    gallery["href"] = relative(self.root / record["local_backup"]["path"], page)
                    gallery["title"] = "Full image recovered from Quinn's local backup. " + gallery.get("title", "").replace("Only the archived thumbnail was recovered. ", "").replace("Full image recovered from Quinn's local backup. ", "")
                    note.string = "Local backup provenance"
                    self.gallery_repairs += 1
                    changed = True
            if changed:
                self.write(page, str(soup))

    def index(self):
        groups = {}
        for source, page in self.pages.items():
            label, rel = self.identify(source)
            group = "Later product pages" if label == "later" else "Early websites and programs"
            groups.setdefault(group, []).append(f'<li><a href="{relative(page, self.base / "index.html")}">{html.escape(rel.as_posix())}</a></li>')
        body = f'<p><a href="../../snapshot.html">Wayback homepage</a> · <a href="../../archive-index.html">Full archive inventory</a></p><h1>Recovered from the local backups</h1><p>Quinn found these original website files in an old backup. They were added on {DATE}. They supplement the {self.year} Wayback collection: the folder dates do not establish when every page was created or which revision a file represents.</p><p>The original layouts are retained where their assets survive. Original scripts, trackers, forms, Java applets and server actions are disabled. Flash animations are available on the <a href="../../../../../early-experiments/">early experiments page</a>.</p><p><a href="photos.html">Recovered photo galleries</a> · <a href="downloads.html">Java programs and applet files</a> · <a href="../../local-backup-manifest.json">Source inventory and checksums</a></p><p>The local website index gives 2002 / 2004 / 2005 for the animation, fireworks and Crazy Horse sites; the January 2011 Wayback copy gives 2004 / 2006 / 2007. These conflicting dates are preserved without choosing a new creation year.</p>'
        for group, links in groups.items():
            body += f'<h2>{group}</h2><ul>' + "".join(links) + "</ul>"
        self.write(self.base / "index.html", shell("Local website backups", body))
        download_body = '<p><a href="index.html">Local backup collection</a></p><h1>Original Java downloads</h1><p>Preserved binaries, not tested applications. They are available as downloads; this archive does not execute them.</p><ul>'
        for source, output in sorted(self.copied.items()):
            if source.suffix.lower() in DOWNLOADS:
                download_body += f'<li><a download href="{relative(output, self.base / "downloads.html")}">{html.escape(self.identify(source)[1].as_posix())}</a> ({source.stat().st_size:,} bytes)</li>'
        self.write(self.base / "downloads.html", shell("Original Java downloads", download_body + "</ul>"))
        photo_body = '<p><a href="index.html">Local backup collection</a></p><h1>Recovered photo galleries</h1><p>These larger images are original local-backup files. Open an image to see its full saved size. Their original photo dates have not been independently established.</p>'
        for folder, title in (("miss_indiana", "Miss Indiana 2007"), ("miss_indiana_2008", "Miss Indiana 2008"), ("miss_indiana2009", "Miss Indiana 2009"), ("miss_indiana2010", "Miss Indiana 2010"), ("senior", "Senior photos")):
            photo_body += f'<h2>{title}</h2><div class="backup-grid">'
            for source in sorted((OLD / "images/picture_page" / folder).iterdir()):
                if source.suffix.lower() not in IMAGES:
                    continue
                stem = source.stem.lower()
                if (folder == "miss_indiana" and "_full" not in stem) or (folder == "miss_indiana_2008" and stem.endswith("s")) or "thumb" in stem or (folder == "senior" and not stem.endswith("l")):
                    continue
                saved = self.copy_asset(source)
                href = relative(saved, self.base / "photos.html")
                photo_body += f'<figure><a href="{href}"><img loading="lazy" src="{href}" alt="{html.escape(title + ": " + source.stem)}"></a><figcaption>{html.escape(source.stem)}</figcaption></figure>'
            photo_body += "</div>"
        self.write(self.base / "photos.html", shell("Recovered photo galleries", photo_body))

    def finish(self):
        self.select()
        for source, target in self.pages.items():
            self.publish_page(source, target)
        self.recover_gaps()
        self.index()
        inventory = {"added": "2026-10-21", "collections": {"old": "Website Archive/Websites/Backups/Personal/Personal", "later": "Website Archive/Websites/Personal/2023"}, "date_note": "Local backup folders are provenance, not publication dates. Wayback raw files remain unchanged.", "gap_bridges": self.gap_bridges, "gallery_links_restored": self.gallery_repairs, "files": self.entries}
        self.write(self.root / "local-backup-manifest.json", json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")
        index = self.root / "archive-index.html"
        soup = BeautifulSoup(index.read_text(encoding="utf-8"), "html.parser")
        old_notice = soup.find(id="local-backup-notice")
        if old_notice:
            old_notice.decompose()
        notice = soup.new_tag("p", id="local-backup-notice")
        a = soup.new_tag("a", href="site/local-backup/index.html")
        a.string = "Explore the local-backup supplements"
        notice.append(a)
        notice.append(f" — added {DATE}; {self.gap_bridges} previously unavailable references now lead to local-backup copies. Original Wayback recovery statuses and dates remain below.")
        (soup.find("main") or soup.body).insert(0, notice)
        self.write(index, str(soup))
        self.manifest["local_backup_supplement"] = {"index": "site/local-backup/index.html", "manifest": "local-backup-manifest.json", "added": "2026-10-21", "gap_bridges": self.gap_bridges, "gallery_links_restored": self.gallery_repairs, "original_recovery_statuses_preserved": True}
        for row in self.manifest["files"] + self.manifest.get("historical_pages", []) + self.manifest.get("capture_gaps", []):
            if row.get("served_path"):
                path = self.root / row["served_path"]
                if path in self.generated:
                    row.update(served_sha256=sha(path.read_bytes()), served_bytes=path.stat().st_size)
        previous = [r for r in self.manifest.get("reconstructed_files", []) if not r.get("local_backup_supplement")]
        for path in sorted(self.generated):
            previous.append({"path": path.relative_to(self.root).as_posix(), "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size, "local_backup_supplement": True})
        self.manifest["reconstructed_files"] = previous
        (self.root / "manifest.json").write_text(json.dumps(self.manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
        print(json.dumps({"year": self.year, "pages": len(self.pages), "published_sources": len(self.entries), "gap_bridges": self.gap_bridges, "gallery_links_restored": self.gallery_repairs, "generated_files": len(self.generated)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-root", type=Path, default=OLD, help="Read-only root of the oldest personal-site backup")
    parser.add_argument("--later-root", type=Path, default=NEW, help="Read-only root of the later personal-site backup")
    args = parser.parse_args()
    OLD, NEW = args.old_root.resolve(), args.later_root.resolve()
    SOURCE_ROOTS = {"old": OLD, "later": NEW}
    for label, source_root in SOURCE_ROOTS.items():
        if not source_root.is_dir():
            parser.error(f"Missing {label} input directory: {source_root}. Reconnect the archive or pass --old-root and --later-root. No archive output was changed.")
    for year in (2011, 2012):
        Supplement(year).finish()
