"""Preserve public Reddit archive data as an inert, attributed transcript.

Usage: python tools/reddit_archive.py --audit <audit-data.json> --results <output.json>
Uses the documented public Arctic Shift API through native curl. Raw responses,
request provenance, exact comment IDs, and incomplete recovery are retained.
No Reddit credentials, challenge solving, source-page edits, or index edits.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import time
from urllib.parse import urlencode, urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://arctic-shift.photon-reddit.com"
SLUGS = {
    "p9opj": "reddit-baconit-free-donation-2012",
    "40z2kj": "reddit-baconit-editing-2016",
    "ulxfp": "reddit-crack-the-whip-2012",
    "gs4nd": "reddit-crosstxt-beta-2011",
    "1b0x4x8": "reddit-homeway-companion-2024",
    "18xyenl": "reddit-homeway-introduction-2024",
    "g2rxw": "reddit-liquid-physics-testing-2011",
    "f0j1h": "reddit-liquid-physics-launch-2011",
    "qg05i": "reddit-next-bus-introduction-2012",
    "1cjh8qv": "reddit-octoeverywhere-bambu-launch-2024",
    "k3b892": "reddit-octoeverywhere-beta-2020",
    "jm1bs": "reddit-purdue-menu-launch-2011",
    "cb7lr": "reddit-reddit-time-machine-launch-2010",
    "uuy3d": "reddit-thinking-of-you-launch-2012",
    "atmxj": "reddit-txtback-relaunch-2010",
    "bxcwu": "reddit-zune-shuffler-launch-2010",
    "1bpf0w": "reddit-baconit-april-fools-comments-2013",
}
PROJECT_FILES = {
    "Baconit": "baconit.md",
    "Crack the Whip": "crack-the-whip.md",
    "CrossTxT": "crosstxt.md",
    "Homeway": "homeway.md",
    "Liquid Physics": "liquid-physics-wallpaper.md",
    "Next Bus": "next-bus.md",
    "OctoEverywhere": "octoeverywhere.md",
    "Purdue Menu": "purdue-menu.md",
    "Reddit Time Machine": "reddit-time-machine.md",
    "Thinking of You": "thinking-of-you.md",
    "TxTBack": "txtback.md",
    "Zune Playlist Shuffler": "zune-playlist-shuffler.md",
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stamp(value):
    try:
        return dt.datetime.fromtimestamp(float(value), dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except (TypeError, ValueError, OverflowError):
        return "Date not recorded"


def esc(value):
    return html.escape(str(value), quote=True)


class SafeMarkdown(HTMLParser):
    """Allow only static formatting and explicit HTTP(S) hyperlinks."""
    allowed = {"p", "br", "hr", "strong", "em", "del", "blockquote", "pre", "code", "ul", "ol", "li", "a", "h1", "h2", "h3", "h4", "h5", "h6", "table", "thead", "tbody", "tr", "th", "td"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            self.output.append("[Image reference: " + esc(a.get("alt", "image")) + "]")
        elif tag in self.allowed:
            attr = ""
            if tag == "a":
                u = a.get("href", "")
                if urlsplit(u).scheme in {"http", "https"}:
                    attr = ' href="' + esc(u) + '" target="_blank" rel="noopener noreferrer"'
            self.output.append("<" + tag + attr + ">")

    def handle_endtag(self, tag):
        if tag in self.allowed:
            self.output.append("</" + tag + ">")

    def handle_data(self, data):
        self.output.append(esc(data))


def body_html(body):
    if body is None or body == "":
        return '<p class="gap">No text body was recorded. This may be a link post.</p>'
    p = SafeMarkdown()
    # Escape raw HTML before Markdown parsing, then independently allowlist output.
    p.feed(markdown.markdown(html.escape(body), extensions=["fenced_code", "tables"]))
    p.close()
    return "".join(p.output)


def fetch(directory, name, url, attempts):
    path = directory / "raw" / (name + ".json")
    meta_path = path.with_suffix(".request.json")
    if path.exists() and meta_path.exists():
        try:
            data = json.loads(path.read_bytes())
            if isinstance(data, dict) and isinstance(data.get("data"), list):
                record = json.loads(meta_path.read_text(encoding="utf-8"))
                if "final_url" not in record:
                    headers = path.with_suffix(".headers.txt").read_text(errors="replace")
                    if len(re.findall(r"(?im)^HTTP/", headers)) == 1 and not re.search(r"(?im)^location:", headers):
                        record["final_url"] = record["url"]
                        record["final_url_evidence"] = "Single retained HTTP response with no redirect Location header."
                        meta_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
                attempts.append(record)
                return data
        except (ValueError, OSError):
            pass
    path.parent.mkdir(parents=True, exist_ok=True)
    for number in range(1, 3):
        headers = path.with_suffix(".headers.txt")
        result = subprocess.run(["curl.exe", "-sS", "-L", "--max-time", "40", "-D", str(headers), "-w", "\n%{http_code}\n%{url_effective}", url], capture_output=True)
        chunks = result.stdout.rsplit(b"\n", 2)
        raw = chunks[0] if len(chunks) == 3 else result.stdout
        status = chunks[1].decode("ascii", "replace") if len(chunks) == 3 else "000"
        final_url = chunks[2].decode("utf-8", "replace") if len(chunks) == 3 else None
        record = {"url": url, "final_url": final_url, "final_url_evidence": "curl url_effective", "fetched_utc": now(), "http_status": status, "curl_exit": result.returncode, "attempt": number, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "raw_file": "raw/" + path.name}
        try:
            data = json.loads(raw)
            valid = isinstance(data, dict) and isinstance(data.get("data"), list)
        except ValueError:
            valid = False
        record["valid_archive_json"] = valid
        if status == "200" and valid:
            path.write_bytes(raw)
            meta_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
            attempts.append(record)
            time.sleep(0.6)
            return data
        record["error"] = result.stderr.decode("utf-8", "replace")[:1000]
        attempts.append(record)
        if status == "429":
            text = headers.read_text(errors="replace")
            match = re.search(r"(?im)^x-ratelimit-reset:\s*(\d+)", text)
            delay = min(55, int(match[1]) + 1) if match else 30
            time.sleep(delay)
        elif number < 2:
            time.sleep(2)
    return {"data": []}


def flatten(nodes, out, collapsed):
    for node in nodes:
        if not isinstance(node, dict):
            continue
        data = node.get("data", {})
        if node.get("kind") == "more":
            collapsed.update(data.get("children", []))
        elif node.get("kind") == "t1" and data.get("id"):
            copy = {k: v for k, v in data.items() if k != "replies"}
            out[data["id"]] = copy
            replies = data.get("replies")
            if isinstance(replies, dict):
                flatten(replies.get("data", {}).get("children", []), out, collapsed)


CSS = """*{box-sizing:border-box}body{margin:0;background:#f4f2eb;color:#242b28;font:17px/1.65 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:36px 24px}h1{font-size:2rem;line-height:1.2}h2{margin-top:2rem}a{color:#23684c;text-underline-offset:3px;overflow-wrap:anywhere}.notice{background:#e6ece1;border-left:4px solid #598060;padding:18px 24px}.meta{font-size:.85rem;color:#505d55;overflow-wrap:anywhere}.comment{border-left:2px solid #c9d1c4;margin:20px 0;padding:8px 0 8px 18px}.replies{margin-left:18px}.replies>.comment:last-child{margin-bottom:0;padding-bottom:0}.comment[data-depth="4"] .replies{margin-left:0}.comment[data-depth="4"] .comment{border-left:0;padding-left:0}.comment:target{background:#fff0c5;outline:3px solid #bb9140;scroll-margin-top:20px}.post{background:white;border:1px solid #d5d9cd;padding:24px}.body{overflow-wrap:anywhere}.body pre{overflow:auto;white-space:pre-wrap}.body table{max-width:100%;border-collapse:collapse}.body td,.body th{border:1px solid #ccd1c6;padding:6px}.gap{color:#794a32}blockquote{border-left:3px solid #c1cabb;margin-left:0;padding-left:18px}details{margin:16px 0}code{font-size:.9em}footer{margin-top:40px;font-size:.85rem}@media(max-width:600px){main{padding:22px 14px}.replies{margin-left:8px}.comment{padding-left:10px}.post{padding:16px}h1{font-size:1.6rem}}@media print{body{background:white}main{max-width:none;padding:0}.comment,.post{break-inside:avoid}details{display:block}.notice{border:1px solid #bbb}}"""


def build(row):
    original_urls = list(dict.fromkeys([row["url"]] + row.get("related_urls", [])))
    match = re.search(r"/r/([^/]+)/comments/([^/]+)", row["url"])
    sub, pid = match.groups()
    slug = SLUGS[pid]
    directory = ROOT / "docs/assets/media" / slug
    directory.mkdir(parents=True, exist_ok=True)
    required = {m[1] for u in original_urls if (m := re.search(r"/comment/([a-z0-9]+)/?", u))}
    attempts = []
    posts = fetch(directory, "post", BASE + "/api/posts/ids?" + urlencode({"ids": pid}), attempts)["data"]
    post = next((p for p in posts if p.get("id") == pid), None)
    data = fetch(directory, "comments-tree", BASE + "/api/comments/tree?" + urlencode({"link_id": pid, "limit": 25000, "start_breadth": 1000, "start_depth": 1000}), attempts)["data"]
    comments, collapsed = {}, set()
    flatten(data, comments, collapsed)
    tree_comment_count = len(comments)
    # Individually recover required or API-collapsed comments, and missing ancestors.
    needed = required | collapsed
    for generation in range(5):
        missing = sorted(needed - comments.keys())
        if not missing:
            break
        for offset in range(0, len(missing), 500):
            batch = missing[offset:offset + 500]
            fetched = fetch(directory, "comments-ids-" + str(generation) + "-" + str(offset), BASE + "/api/comments/ids?" + urlencode({"ids": ",".join(batch)}), attempts)["data"]
            for c in fetched:
                if c.get("id") and c.get("link_id", "").removeprefix("t3_") == pid:
                    comments[c["id"]] = c
        needed = {c["parent_id"][3:] for c in comments.values() if c.get("parent_id", "").startswith("t1_")} | required | collapsed
    # A second documented public index query helps establish an empty or incomplete tree.
    expected = post.get("num_comments") if post else None
    if not comments or (expected is not None and len(comments) < expected):
        extra = fetch(directory, "comments-search", BASE + "/api/comments/search?" + urlencode({"link_id": pid, "limit": "auto", "sort": "asc"}), attempts)["data"]
        for c in extra:
            if c.get("id") and c.get("link_id", "").removeprefix("t3_") == pid:
                comments[c["id"]] = c
    # Search may contribute descendants whose ancestors were absent from the tree.
    for generation in range(5):
        missing = sorted({c["parent_id"][3:] for c in comments.values() if c.get("parent_id", "").startswith("t1_")} - comments.keys())
        if not missing:
            break
        recovered = 0
        for offset in range(0, len(missing), 500):
            fetched = fetch(directory, "parent-ids-" + str(generation) + "-" + str(offset), BASE + "/api/comments/ids?" + urlencode({"ids": ",".join(missing[offset:offset + 500])}), attempts)["data"]
            for c in fetched:
                if c.get("id") and c.get("link_id", "").removeprefix("t3_") == pid:
                    comments[c["id"]] = c
                    recovered += 1
        if not recovered:
            break
    missing_required = sorted(required - comments.keys())
    missing_collapsed = sorted(collapsed - comments.keys())
    missing_parents = sorted({c["parent_id"][3:] for c in comments.values() if c.get("parent_id", "").startswith("t1_")} - comments.keys())
    placeholder_comments = [c["id"] for c in comments.values() if c.get("body") in {"[deleted]", "[removed]", None, ""}]
    gaps = []
    if not post:
        gaps.append("The original post was not returned by the public archive; the curated title below is a label, not reconstructed post text.")
    elif post.get("selftext") in {"[deleted]", "[removed]"}:
        gaps.append("The archived post body is marked " + post["selftext"] + "; no missing wording has been reconstructed.")
    if pid == "18xyenl" and post:
        gaps.append("The project source records that moderators later removed the Homeway introduction. This archive retains the earlier post body observed on " + stamp(post.get("retrieved_on")) + "; it does not imply the original post remains visible today.")
    if pid == "1bpf0w":
        gaps.append("The older preserved page referenced 15 comments; this public archive's post record reports 16 and its comment tree returns 17. These are separate archive observations, not a claim to have recovered an exact historical count.")
    if missing_required:
        gaps.append("Required comment IDs not recovered: " + ", ".join(missing_required) + ".")
    if missing_collapsed:
        gaps.append("Comment IDs advertised by the archive tree but not recovered individually: " + ", ".join(missing_collapsed) + ".")
    if tree_comment_count >= 25000:
        gaps.append("The public tree query reached its 25,000-record limit. This transcript must be treated as incomplete.")
    if not comments:
        gaps.append("No comments were returned by the public archive tree or comment search. This is not proof that the original discussion had no comments.")
    if expected is not None and len(comments) != expected:
        gaps.append(f"Recovered {len(comments)} comment records; the archived post reports {expected}. Counts come from different archive observations and cannot establish complete recovery.")
    if placeholder_comments:
        gaps.append(f"{len(placeholder_comments)} recovered comment records contain deleted/removed/empty text; those placeholders are retained.")
    if missing_parents:
        gaps.append("Missing parent comments: " + ", ".join(missing_parents) + ". Their recovered descendants appear in a separate section.")
    permalink = "https://www.reddit.com/r/" + sub + "/comments/" + pid + "/"
    if post and post.get("permalink"):
        permalink = "https://www.reddit.com" + post["permalink"]
    title = post.get("title") if post else row["title"]
    by_parent = {}
    for c in comments.values():
        by_parent.setdefault(c.get("parent_id", ""), []).append(c)
    visited = set()

    def render_comment(c, depth=0):
        cid = c["id"]
        if cid in visited:
            return ""
        visited.add(cid)
        url = f"https://www.reddit.com/r/{sub}/comments/{pid}/comment/{cid}/"
        source_time = " · Archive observation: " + stamp(c["retrieved_on"]) if c.get("retrieved_on") else " · Archive observation date not recorded"
        parent_id = c.get("parent_id", "").removeprefix("t1_")
        parent_link = f' <span> | <a href="#comment-{esc(parent_id)}">Parent comment</a></span>' if parent_id in comments else ''
        flag = " · Cited comment" if cid in required else ""
        chunk = f'<article class="comment" data-depth="{depth}" id="comment-{esc(cid)}"><header class="meta"><b>u/{esc(c.get("author", "[author not recorded]"))}</b> · {stamp(c.get("created_utc"))}{esc(flag)}<br><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">Original comment</a> · <a href="#comment-{esc(cid)}">Local permalink</a>{esc(source_time)}{parent_link}</header><div class="body">{body_html(c.get("body"))}</div>'
        children = sorted(by_parent.get("t1_" + cid, []), key=lambda x: (x.get("created_utc", 0), x["id"]))
        if children:
            chunk += '<div class="replies">' + "".join(render_comment(x, depth + 1) for x in children) + "</div>"
        return chunk + "</article>"

    thread = "".join(render_comment(c) for c in sorted(by_parent.get("t3_" + pid, []), key=lambda x: (x.get("created_utc", 0), x["id"])))
    orphans = [c for cid, c in comments.items() if cid not in visited]
    if orphans:
        thread += '<h3>Comments with an unavailable parent</h3>' + "".join(render_comment(c) for c in sorted(orphans, key=lambda x: (x.get("created_utc", 0), x["id"])))
    required_links = " · ".join(f'<a href="#comment-{esc(c)}">{esc(c)}</a>' for c in sorted(required) if c in comments)
    gap_html = "<ul>" + "".join("<li>" + esc(x) + "</li>" for x in gaps) + "</ul>" if gaps else "<p>All specifically cited comment IDs were recovered. Archive completeness beyond the returned records is not guaranteed.</p>"
    raw_links = " · ".join(f'<a href="{esc(a["raw_file"])}">{esc(Path(a["raw_file"]).stem)}</a>' for a in attempts if a.get("valid_archive_json") and a["http_status"] == "200")
    post_html = body_html(post.get("selftext")) if post else '<p class="gap">Post text unavailable.</p>'
    if post and not post.get("is_self") and post.get("url"):
        post_html += '<p>Original linked destination: <a href="' + esc(post["url"]) + '" target="_blank" rel="noopener noreferrer">' + esc(post["url"]) + "</a></p>"
    retrieved = now()
    content = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>{esc(title)} — archived discussion</title><style>{CSS}</style></head><body><main><div class="notice"><strong>Archived Reddit transcript</strong><p>This readable transcript was assembled from public Arctic Shift archive records on {esc(retrieved[:10])}. It preserves recovered wording and parent/reply relationships; it is not a screenshot of Reddit and does not reproduce Reddit's voting order or interface. Images and linked websites are not automatically copied. Record observation dates can differ.</p><p>{len(comments)} recovered comments · {len(required) - len(missing_required)}/{len(required)} cited comment IDs recovered.</p>{gap_html}<p><a href="{esc(permalink)}" target="_blank" rel="noopener noreferrer">Original Reddit thread</a> · <a href="snapshot.json">Provenance and coverage</a> · <a href="transcript.json">Normalized transcript</a></p><p>Raw archive responses: {raw_links}</p></div><h1>{esc(title)}</h1><p class="meta">r/{esc(sub)} · u/{esc(post.get('author', '[not recovered]') if post else '[not recovered]')} · {stamp(post.get('created_utc') if post else None)}<br>Archive observation: {stamp(post.get('retrieved_on') if post else None)}</p><section class="post body" id="post">{post_html}</section><h2>Discussion</h2><p>{required_links}</p>{thread or '<p class="gap">No comment text recovered.</p>'}<footer>Source: <a href="{BASE}/">Arctic Shift public archive</a>. Raw source bytes and their SHA-256 checksums are retained in this archive. Deleted or removed placeholders have not been replaced with invented text.</footer></main></body></html>'''
    (directory / "snapshot.html").write_text(content, encoding="utf-8", newline="\n")
    normalized = {"post": post, "comments": sorted(comments.values(), key=lambda x: (x.get("created_utc", 0), x["id"]))}
    (directory / "transcript.json").write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = {"url": permalink, "original_urls": original_urls, "title": title, "site": "Reddit via Arctic Shift", "captured": retrieved, "format": "reconstructed static transcript", "post_recovered": bool(post), "post_created_utc": post.get("created_utc") if post else None, "post_archive_observed_utc": post.get("retrieved_on") if post else None, "api_coverage": {"tree_record_limit": 25000, "tree_start_breadth": 1000, "tree_start_depth": 1000, "tree_comment_count": tree_comment_count, "tree_limit_reached": tree_comment_count >= 25000, "advertised_collapsed_comment_ids": sorted(collapsed), "unrecovered_collapsed_comment_ids": missing_collapsed, "pagination_note": "The tree API returns nested records and collapsed IDs rather than page cursors. Every advertised collapsed ID and missing ancestor is queried individually. A separate comments search supplements empty or numerically short trees. All specifically cited IDs are checked independently; differing record observations prevent an assertion of completeness."}, "comment_count": len(comments), "recorded_comment_count": expected, "required_comment_ids": sorted(required), "missing_required_comment_ids": missing_required, "placeholder_comment_ids": placeholder_comments, "missing_parent_ids": missing_parents, "gaps": gaps, "requests": attempts, "source_api_documentation": "https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md", "snapshot_sha256": hashlib.sha256(content.encode()).hexdigest()}
    (directory / "snapshot.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    wrapper = ROOT / "docs/media" / (slug + ".md")
    focuses = []
    for cid in sorted(required):
        c = comments.get(cid)
        block = f'<h2 id="comment-{cid}">Cited comment {cid}</h2>\n'
        if c:
            block += f'<p>By u/{esc(c.get("author", "[not recorded]"))} · {stamp(c.get("created_utc"))}</p>\n<div class="qd-archive-comment">{body_html(c.get("body"))}</div>\n'
            block += f'<p><a href="../assets/media/{slug}/snapshot.html#comment-{cid}" target="_blank" rel="noopener">Open this comment in the archived discussion</a></p>\n'
        else:
            block += '<p>This specifically cited comment could not be recovered. The available thread is preserved below.</p>\n'
        focuses.append(block)
    previous = '\nThe earlier [April Fools page and photograph](reddit-baconit-april-fools-2013.md) remain preserved separately; this page supplements them with recovered discussion records.\n' if pid == "1bpf0w" else ""
    project_link = f"Related project: [{row['project']}](../{PROJECT_FILES[row['project']]})."
    address = permalink.removeprefix("https://").removeprefix("www.")
    wrapper_text = f'''---
title: {json.dumps(row['title'], ensure_ascii=False)}
description: {json.dumps('A preserved Reddit discussion with recovered comments and disclosed gaps.', ensure_ascii=False)}
hide:
  - navigation
  - toc
search:
  exclude: true
---

# {row['title']}

This archive preserves the original Reddit post and **{len(comments)} recovered comment records** as a readable transcript. The source is the public Arctic Shift archive, fetched on {retrieved[:10]}. It preserves recovered text and reply relationships, rather than Reddit's visual interface. The underlying archive does not guarantee every original comment or edit is available.
{previous}
{project_link}

<dl class="qd-archive-meta">
  <div><dt>Source</dt><dd>Reddit via Arctic Shift</dd></div>
  <div><dt>Published</dt><dd>{stamp(post.get('created_utc') if post else None)}</dd></div>
  <div><dt>Recovered</dt><dd>{retrieved[:10]} UTC</dd></div>
  <div><dt>Original</dt><dd><a href="{esc(permalink)}">Original Reddit thread</a></dd></div>
</dl>

<aside aria-label="Recovery notes">{gap_html}</aside>

<div class="qd-archive-actions"><a class="md-button" href="{esc(permalink)}">Original Reddit thread</a><a class="md-button" href="../assets/media/{slug}/snapshot.json">Provenance and coverage</a><a class="md-button" href="../assets/media/{slug}/transcript.json">Download transcript JSON</a></div>

{''.join(focuses)}
## Full recovered discussion

<figure class="qd-archive-frame qd-archive-frame--site">
  <div class="qd-archive-frame__bar">
    <span class="qd-archive-frame__dots" aria-hidden="true"><span></span><span></span><span></span></span>
    <span class="qd-archive-frame__url" title="{esc(address)}">{esc(address)}</span>
    <a class="md-button md-button--primary qd-archive-frame__control" href="../assets/media/{slug}/snapshot.html" target="_blank" rel="noopener">Open separately<span class="qd-visually-hidden"> in a new tab</span></a>
  </div>
  <iframe class="qd-archive-frame__site" name="qd-archive-{slug}" src="../assets/media/{slug}/snapshot.html" title="Archived Reddit discussion: {esc(row['title'])}" width="1280" height="900" loading="eager" sandbox="allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-downloads" referrerpolicy="no-referrer"></iframe>
  <figcaption>Static transcript from public archive records. No original text has been supplied for missing or removed records.</figcaption>
</figure>
'''
    wrapper.write_text(wrapper_text, encoding="utf-8")
    wrapper_url = "https://projects.quinn.space/media/" + slug + "/"
    mappings = {}
    for u in original_urls:
        m = re.search(r"/comment/([a-z0-9]+)/?", u)
        mappings[u] = wrapper_url + ("#comment-" + m[1] if m else "")
    return {"slug": slug, "project": row.get("project"), "title": row["title"], "primary_url": row["url"], "original_urls": original_urls, "url_mappings": mappings, "wrapper_url": wrapper_url, "wrapper_file": str(wrapper), "asset_directory": str(directory), "post_recovered": bool(post), "comment_count": len(comments), "recorded_comment_count": expected, "required_comment_ids": sorted(required), "missing_required_comment_ids": missing_required, "placeholder_comment_ids": placeholder_comments, "missing_parent_ids": missing_parents, "unrecovered_collapsed_comment_ids": missing_collapsed, "tree_limit_reached": tree_comment_count >= 25000, "gaps": gaps, "status": "recovered" if post and not missing_required else "partial", "anchor_strategy": "Wrapper #comment-ID shows the recovered cited comment and links to snapshot.html#comment-ID for its complete threaded context.", "files": [str(p.relative_to(ROOT)) for p in directory.rglob('*') if p.is_file()] + [str(wrapper.relative_to(ROOT))]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audit", type=Path, required=True)
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--only", help="Comma-separated post IDs")
    args = p.parse_args()
    rows = [r for r in json.loads(args.audit.read_text(encoding="utf-8"))["rows"] if "reddit.com" in urlsplit(r["url"]).netloc]
    rows.append({"url": "https://www.reddit.com/r/baconit/comments/1bpf0w/got_a_pic_of_the_april_fools_joke_nice_one_quinn/", "title": "Baconit's April Fools prank: recovered comments", "project": "Baconit", "related_urls": []})
    if args.only:
        wanted = args.only.split(",")
        rows = [r for r in rows if re.search(r"/comments/([^/]+)", r["url"])[1] in wanted]
    results = []
    for row in rows:
        result = build(row)
        results.append(result)
        args.results.write_text(json.dumps({"source": "Public Arctic Shift archive", "recovered_utc": now(), "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({k: result[k] for k in ["slug", "comment_count", "recorded_comment_count", "missing_required_comment_ids", "status"]}), flush=True)


if __name__ == "__main__":
    main()
