#!/usr/bin/env python3
"""Validate a browsable static archive without executing its historical code.

Usage:
    python tools/check_site_archive.py docs/assets/media/<archive> --check-zip
    python tools/check_site_archive.py <2011-root> <2012-root> --web-root docs \
        --opaque-origin --json <report.json>

Only Python's standard library is required. Local scripts are permitted and
inventoried, not treated as failures. This is a static integrity/navigation
check, not a JavaScript security audit or a substitute for a browser walkthrough.
The manifest uses files[] entries with original_url, raw_path, sha256, bytes,
served_path, served_sha256, and served_bytes; local_path is a fallback below site/.
Raw-source navigation, including common old onclick handlers, is compared with
the local navigation graph. --require-coverage makes uncovered source links
errors; otherwise they remain review warnings. Query strings remain significant
unless --ignore-query-param explicitly names a disposable session parameter.
Explicit url_aliases are honored; recovered destinations and honest local gap
pages are counted separately. Editable GET forms are inventoried for review,
because the GET method alone does not distinguish searches from signup actions.
Optional historical_pages[] uses the same source/served hash fields. Each
historical variant is checked with its own self URL, without replacing the main
site's URL mapping or adding it to main-menu reachability requirements.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlencode, urljoin, urlsplit, urlunsplit
import zipfile


CSS_URL = re.compile(r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s)]*))\s*\)", re.I)
CSS_IMPORT = re.compile(r"@import\s+(?:\"([^\"]+)\"|'([^']+)')", re.I)
NAV_HANDLER = re.compile(r"(?:window\.)?location(?:\.href)?\s*=\s*(['\"])(.*?)\1|(?:window\.)?location\.(?:assign|replace)\(\s*(['\"])(.*?)\3\s*\)", re.I)
SCROLL_HANDLER = re.compile(r"goToByScroll\(\s*(['\"])(.*?)\1\s*\)", re.I)
FONT_SUFFIXES = {'.woff', '.woff2', '.ttf', '.otf', '.eot'}
RESOURCE_LINKS = {'stylesheet', 'icon', 'shortcut', 'preload', 'modulepreload', 'manifest'}


@dataclass(frozen=True)
class Reference:
    url: str
    kind: str
    tag: str
    attribute: str
    line: int
    form_index: int | None = None


def css_urls(text: str):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    for pattern in (CSS_URL, CSS_IMPORT):
        for match in pattern.finditer(text):
            yield next(value for value in match.groups() if value is not None)


def srcset_urls(value: str):
    """Tokenize ordinary srcsets, retaining embedded commas in data URLs."""
    position = 0
    while position < len(value):
        while position < len(value) and (value[position].isspace() or value[position] == ','):
            position += 1
        start = position
        while position < len(value) and not value[position].isspace():
            position += 1
        url = value[start:position]
        if not url:
            break
        if url.endswith(','):
            yield url.rstrip(',')
            continue
        yield url
        # Descriptors can contain parenthesized expressions; their commas do
        # not separate candidates. Data-URL commas were consumed above.
        depth = 0
        while position < len(value):
            char = value[position]
            depth += (char == '(') - (char == ')')
            position += 1
            if char == ',' and depth <= 0:
                break


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.refs: list[Reference] = []
        self.ids: set[str] = set()
        self.scripts: list[dict] = []
        self.handlers: list[dict] = []
        self.forms: list[dict] = []
        self.frames: list[dict] = []
        self.dead_anchors: list[dict] = []
        self.targets: list[dict] = []
        self.csps: list[str] = []
        self.base: str | None = None
        self._script: dict | None = None
        self._style: list[str] | None = None
        self._anchor: dict | None = None
        self._form: dict | None = None
        self.feed(text)

    def add(self, value, kind, tag, attribute):
        if value is not None:
            self.refs.append(Reference(value.strip(), kind, tag, attribute, self.getpos()[0]))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and a.get('name'):
            self.ids.add(a['name'])
        if tag == 'base' and a.get('href'):
            self.base = a['href']
        if tag == 'meta' and a.get('http-equiv', '').lower() == 'content-security-policy':
            self.csps.append(a.get('content', ''))
        if tag in {'a', 'area'}:
            self.add(a.get('href'), 'navigation', tag, 'href')
            if a.get('target') or 'download' in a:
                self.targets.append({'line': line, 'href': a.get('href'), 'target': a.get('target'),
                                     'download': 'download' in a})
        if tag == 'a':
            self._anchor = {'line': line, 'href': a.get('href'), 'name': a.get('name'),
                            'id': a.get('id'), 'label': '', 'interactive': bool(a.get('onclick'))}
        if tag == 'img' and self._anchor is not None:
            self._anchor['label'] += a.get('alt') or '[image]'
        if tag == 'link' and set(a.get('rel', '').lower().split()) & RESOURCE_LINKS:
            self.add(a.get('href'), 'resource', tag, 'href')
        for attr in ('src', 'poster', 'background'):
            if tag != 'base':
                self.add(a.get(attr), 'resource', tag, attr)
        if tag in {'image', 'use'}:
            self.add(a.get('href') or a.get('xlink:href'), 'resource', tag, 'href')
        if tag == 'object':
            self.add(a.get('data'), 'resource', tag, 'data')
        for value in srcset_urls(a.get('srcset', '')):
            self.add(value, 'resource', tag, 'srcset')
        # Contracts used by the small audited archive helper scripts. The
        # browser loads these only on interaction, so normal src checks miss them.
        self.add(a.get('data-rollover'), 'resource', tag, 'data-rollover')
        self.add(a.get('data-archive-hover'), 'resource', tag, 'data-archive-hover')
        if a.get('data-video-box'):
            self.add('#' + a['data-video-box'], 'navigation', tag, 'data-video-box')
        if a.get('data-archive-video'):
            self.add('#' + a['data-archive-video'], 'navigation', tag, 'data-archive-video')
        for attr in ('data-gallery', 'data-archive-gallery'):
            if attr in a:
                self.add(a.get('href'), 'resource', tag, attr)
        for value in css_urls(a.get('style', '')):
            self.add(value, 'resource', 'css', 'url')
        if tag == 'style':
            self._style = []
        if tag == 'script':
            self._script = {'line': line, 'src': a.get('src'), 'type': a.get('type', ''), 'code': ''}
            self.scripts.append(self._script)
        if tag in {'iframe', 'object', 'embed'}:
            self.frames.append({'line': line, 'tag': tag, 'src': a.get('src') or a.get('data'),
                                'sandbox': a.get('sandbox'), 'srcdoc': 'srcdoc' in a})
        for attr, value in attrs:
            if attr.startswith('on') and value:
                self.handlers.append({'line': line, 'attribute': attr, 'code': value})
                for match in NAV_HANDLER.finditer(value):
                    self.add(match.group(2) or match.group(4), 'navigation', tag, attr)
                for match in SCROLL_HANDLER.finditer(value):
                    self.add('#' + match.group(2), 'navigation', tag, attr)
        if tag == 'form':
            self._form = {'line': line, 'action': a.get('action', ''),
                          'method': a.get('method', 'get').lower(), 'fields': [], 'controls': [],
                          'onsubmit': a.get('onsubmit'), 'target': a.get('target')}
            self.forms.append(self._form)
        if tag == 'input' and self._form is not None and a.get('name') and 'disabled' not in a:
            kind = a.get('type', 'text').lower()
            if kind == 'hidden' or (kind in {'checkbox', 'radio'} and 'checked' in a):
                self._form['fields'].append((a['name'], a.get('value', 'on' if kind != 'hidden' else '')))
        if tag in {'input', 'select', 'textarea', 'button'} and self._form is not None:
            self._form['controls'].append({k: a[k] for k in ('name', 'type', 'value', 'disabled') if k in a})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 'script':
            self._script = None
        if tag == 'style' and self._style is not None:
            for value in css_urls(''.join(self._style)):
                self.add(value, 'resource', 'css', 'url')
            self._style = None
        if tag == 'a' and self._anchor is not None:
            a = self._anchor
            if not a['name'] and a['label'].strip() and a['href'] in (None, '', '#'):
                self.dead_anchors.append(a)
            self._anchor = None
        if tag == 'form' and self._form is not None:
            form = self._form
            if form['method'] == 'get':
                u = urlsplit(form['action'])
                query = urlencode(form['fields'])
                # A GET form replaces its action's query with successful fields.
                value = urlunsplit((u.scheme, u.netloc, u.path, query, u.fragment))
                self.refs.append(Reference(value, 'navigation', 'form', 'action',
                                           self.getpos()[0], len(self.forms) - 1))
            self._form = None

    def handle_data(self, text):
        if self._script is not None:
            self._script['code'] += text
        if self._style is not None:
            self._style.append(text)
        if self._anchor is not None:
            self._anchor['label'] += text


def original_key(value: str, base: str = '', ignored_params=()) -> str:
    value = urljoin(base, value)
    replay = re.match(r'^(?:https?:)?//web\.archive\.org/web/\d+[a-z_]*/(https?://.*)$', value, re.I)
    if replay:
        value = replay.group(1)
    u = urlsplit(value)
    host = (u.hostname or '').lower().removeprefix('www.')
    # Scheme/www variations refer to the same historic origin. Query values
    # remain significant unless a caller explicitly names a disposable key.
    port = f':{u.port}' if u.port and u.port not in (80, 443) else ''
    ignored = {name.casefold() for name in ignored_params}
    query = '&'.join(part for part in u.query.split('&')
                     if unquote(part.split('=', 1)[0]).casefold() not in ignored)
    return urlunsplit(('http', host + port, u.path or '/', query, ''))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Audit:
    def __init__(self, root: Path, args):
        self.root = root.resolve()
        self.args = args
        self.web_root = Path(args.web_root).resolve() if args.web_root else self.root
        self.errors = []
        self.warnings = []
        self.inventory = defaultdict(list)
        self.counts = Counter()
        self.pages = {}
        self.dirnames = {}
        self.generated_links = []

    def name(self, path):
        return os.path.relpath(path, self.root).replace('\\', '/')

    def issue(self, code, path=None, detail=None, *, warning=False):
        record = {'code': code}
        if path is not None:
            record['file'] = self.name(path)
        if detail is not None:
            record['detail'] = detail
        (self.warnings if warning else self.errors).append(record)

    def local(self, source: Path, value: str):
        """Resolve paths lexically first so Windows cannot hide casing errors."""
        u = urlsplit(value)
        if u.scheme or u.netloc:
            return None
        path = unquote(u.path)
        if '\\' in path:
            self.issue('backslash_url', source, value, warning=True)
            path = path.replace('\\', '/')
        target = self.web_root / path.lstrip('/') if path.startswith('/') else source.parent / path
        if not path:
            target = source
        target = Path(os.path.abspath(os.path.normpath(target)))
        if target.is_dir():
            target /= 'index.html'
        return target

    def exact_case(self, target: Path, source: Path, value: str):
        if not target.is_relative_to(self.web_root):
            self.issue('outside_web_root', source, value, warning=True)
            return
        current = self.web_root
        for part in target.relative_to(self.web_root).parts:
            if current not in self.dirnames:
                self.dirnames[current] = {p.name for p in current.iterdir()} if current.is_dir() else set()
            names = self.dirnames[current]
            if part not in names:
                matches = [n for n in names if n.casefold() == part.casefold()]
                if matches:
                    self.issue('path_case_mismatch', source, {'url': value, 'requested': part, 'actual': matches})
                return
            current /= part

    def generated_markdown(self, target):
        candidates = [target.with_suffix('.md')]
        if target.name == 'index.html':
            candidates.extend([target.parent.with_suffix('.md'), target.parent/'index.md'])
        return next((p for p in candidates if p.is_file()), None)

    def reference(self, source: Path, ref: Reference):
        value = ref.url
        u = urlsplit(value)
        if u.scheme or u.netloc:
            if u.scheme in {'data', 'mailto', 'tel', 'market'}:
                return
            if u.scheme == 'javascript':
                self.issue('javascript_url', source, value, warning=True)
                return
            bucket = 'external_resources' if ref.kind == 'resource' else 'external_links'
            self.inventory[bucket].append({'file': self.name(source), 'url': value, 'line': ref.line})
            if ref.kind == 'resource':
                self.issue('external_resource', source, value)
            return
        target = self.local(source, value)
        if target is None:
            return
        if not target.is_file():
            generated = self.generated_markdown(target) if self.args.allow_generated else None
            if generated:
                self.generated_links.append({'file': self.name(source), 'url': value, 'markdown': str(generated)})
            else:
                self.issue('missing_local_target', source, {'url': value, 'kind': ref.kind, 'line': ref.line})
            return
        self.exact_case(target, source, value)
        self.counts['local_references_checked'] += 1
        if target in self.pages and (ref.tag == 'img' or ref.attribute in {'data-gallery', 'data-archive-gallery'}):
            self.issue('image_target_is_html', source, value)
        if u.fragment and target in self.pages:
            fragment = unquote(u.fragment).split(':~:text=', 1)[0]
            if fragment and fragment not in self.pages[target].ids:
                self.issue('missing_fragment', source, value)
        if self.args.opaque_origin and ref.kind == 'resource' and target.suffix.lower() in FONT_SUFFIXES:
            self.issue('opaque_origin_font_cors', source, value, warning=True)
        if target.name == 'missing-asset.svg':
            self.inventory['placeholder_resources'].append({'file': self.name(source), 'url': value})

    def active_content(self, path: Path, page: Page):
        active = [s for s in page.scripts if s['type'].lower() not in
                  {'application/json', 'application/ld+json', 'importmap', 'speculationrules'}]
        for script in active:
            self.inventory['scripts'].append({'file': self.name(path), 'line': script['line'],
                'src': script['src'], 'type': script['type'],
                'inline_sha256': hashlib.sha256(script['code'].encode()).hexdigest() if not script['src'] else None})
            if self.args.opaque_origin and script['type'].lower() == 'module':
                self.issue('opaque_origin_module_cors', path, script['src'], warning=True)
        for group, entries in [('handlers', page.handlers), ('forms', page.forms), ('frames', page.frames), ('dead_anchors', page.dead_anchors), ('navigation_targets', page.targets)]:
            for entry in entries:
                self.inventory[group].append({'file': self.name(path), **entry})
        if page.dead_anchors:
            self.issue('anchors_without_destinations', path, len(page.dead_anchors), warning=True)
        if self.args.opaque_origin:
            permissions = set(getattr(self.args, 'iframe_sandbox', 'allow-scripts').split())
            for link in page.targets:
                needed = []
                if link['target'] in {'_top', '_parent'} and not permissions & {'allow-top-navigation', 'allow-top-navigation-by-user-activation'}:
                    needed.append('allow-top-navigation-by-user-activation')
                if link['target'] == '_blank' and 'allow-popups' not in permissions:
                    needed.append('allow-popups')
                if link['download'] and 'allow-downloads' not in permissions:
                    needed.append('allow-downloads')
                if needed:
                    self.issue('sandbox_navigation_permission_needed', path, {**link, 'required_flags': needed}, warning=True)
        self.inventory['csp'].append({'file': self.name(path), 'policies': page.csps})
        if active and not page.csps:
            self.issue('scripts_without_csp', path, warning=True)
        for policy in page.csps:
            directives = {d.split()[0].lower(): d.split()[1:] for d in policy.split(';') if d.split()}
            allowed = directives.get('script-src-elem', directives.get('script-src', directives.get('default-src', [])))
            if active and "'none'" in allowed:
                self.issue('csp_blocks_scripts', path, allowed)
            for script in active:
                if script['src'] or not allowed or "'unsafe-inline'" in allowed:
                    continue
                sha = base64.b64encode(hashlib.sha256(script['code'].encode()).digest()).decode()
                if f"'sha256-{sha}'" not in allowed and not any(x.startswith("'nonce-") for x in allowed):
                    self.issue('csp_blocks_inline_script', path, script['line'])
        if page.base:
            self.issue('base_url_needs_browser_review', path, page.base, warning=True)

    def verify_hash(self, row, path_key, hash_key, size_key, *, fallback=None):
        value = row.get(path_key) or fallback
        if not value:
            return
        path = self.root / value
        if not path.resolve().is_relative_to(self.root):
            self.issue('manifest_path_outside_archive', detail=value)
            return
        if not path.is_file():
            self.issue('manifest_missing_file', detail=value)
            return
        self.exact_case(path, self.root/'manifest.json', value)
        expected = row.get(hash_key)
        if not expected:
            self.issue('manifest_missing_hash', path, hash_key, warning=True)
        elif digest(path) != expected:
            self.issue('manifest_hash_mismatch', path, hash_key)
        else:
            self.counts[hash_key + '_verified'] += 1
        if row.get(size_key) is not None and path.stat().st_size != row[size_key]:
            self.issue('manifest_size_mismatch', path, size_key)

    def source_graph(self, rows, manifest, *, source_rows=None,
                     report_prefix='source_navigation', self_override=False):
        def key_for(value, base=''):
            return original_key(value, base, getattr(self.args, 'ignore_query_param', []))
        lookup = {key_for(r['original_url']): r for r in rows if r.get('original_url')}
        for alias in manifest.get('url_aliases', []):
            source, target = alias.get('original_url'), alias.get('target_url')
            if source and target and key_for(target) in lookup:
                lookup[key_for(source)] = lookup[key_for(target)]
            else:
                self.issue('manifest_alias_target_missing', detail=alias)
        requested = manifest.get('requested_url') or manifest.get('url')
        # Captured external embeds/gap pages do not make their entire host part
        # of this website. Use the requested website origin when available.
        hosts = {urlsplit(key_for(requested)).hostname} if requested else {
            urlsplit(k).hostname for k, r in lookup.items()
            if r.get('kind') == 'page' and r.get('status') == 'saved'}
        edges = []
        for row in rows if source_rows is None else source_rows:
            if row.get('kind') != 'page' or not row.get('raw_path') or not row.get('original_url'):
                continue
            raw = self.root / row['raw_path']
            served = self.root / (row.get('served_path') or 'site/' + row.get('local_path', ''))
            if not raw.resolve().is_relative_to(self.root) or not raw.is_file() or served not in self.pages:
                continue
            original = row['original_url']
            capture_lookup = {key_for(g['original_url']): g for g in row.get('capture_gaps', [])
                              if g.get('original_url')} if self_override else {}
            source = Page(raw.read_text(encoding='utf-8', errors='replace'))
            for form in source.forms:
                self.inventory['source_forms'].append({'source': original, **form})
            actual = {(self.local(served, r.url), unquote(urlsplit(r.url).fragment)) for r in self.pages[served].refs
                      if r.kind == 'navigation' and not urlsplit(r.url).scheme and not urlsplit(r.url).netloc}
            for ref in source.refs:
                if ref.kind != 'navigation' or urlsplit(ref.url).scheme in {'mailto', 'tel', 'javascript', 'market', 'data'}:
                    continue
                if ref.tag == 'form':
                    # Fixed hidden/checked controls can represent pagination.
                    # Editable inputs may be searches OR account/signup actions;
                    # never classify them as safe navigation just from GET.
                    editable = [f for i, f in enumerate(source.forms) if i == ref.form_index and any(
                        c.get('type', 'text').lower() not in {'hidden', 'submit', 'button', 'reset', 'checkbox', 'radio'}
                        and 'disabled' not in c for c in f['controls'])]
                    if editable:
                        self.inventory['source_get_forms_needing_review'].append({'source': original, 'forms': editable})
                        continue
                key = key_for(ref.url, original)
                if urlsplit(key).hostname not in hosts:
                    continue
                destination = row if self_override and key == key_for(original) else capture_lookup.get(key, lookup.get(key))
                fragment = unquote(urlsplit(urljoin(original, ref.url)).fragment)
                edge = {'source': original, 'target': key, 'fragment': fragment, 'via': ref.attribute}
                if self_override:
                    edge.update(capture=row.get('actual_timestamp'), served_source=self.name(served))
                if not destination:
                    edge['status'] = 'not_in_manifest'
                else:
                    local = destination.get('served_path') or destination.get('placeholder_path')
                    if not local and destination.get('local_path') and destination.get('status') == 'saved':
                        local = 'site/' + destination['local_path']
                    if not local:
                        edge['status'] = 'not_recovered'
                    else:
                        expected = (self.root / local, fragment)
                        if expected in actual:
                            edge['status'] = 'linked' if destination.get('status') == 'saved' else 'gap_linked'
                        else:
                            edge['status'] = 'served_link_missing'
                edges.append(edge)
        unique = {json.dumps(e, sort_keys=True): e for e in edges}
        self.inventory[report_prefix] = list(unique.values())
        uncovered = [e for e in unique.values() if e['status'] not in {'linked', 'gap_linked'}]
        for edge in uncovered:
            self.issue(report_prefix + '_' + edge['status'], detail=edge, warning=not self.args.require_coverage)
        self.counts[report_prefix + '_edges'] = len(unique)
        self.counts[report_prefix + '_linked'] = sum(e['status'] == 'linked' for e in unique.values())
        self.counts[report_prefix + '_gap_linked'] = sum(e['status'] == 'gap_linked' for e in unique.values())
        self.counts[report_prefix + '_accounted'] = len(unique) - len(uncovered)

    def manifests(self):
        path = self.root / 'manifest.json'
        if not path.is_file():
            self.issue('manifest_not_found', warning=True)
            return
        manifest = json.loads(path.read_text(encoding='utf-8'))
        rows = manifest.get('files', [])
        historical = manifest.get('historical_pages', [])
        capture_gaps = manifest.get('capture_gaps', [])
        historical_gaps = [gap for row in historical for gap in row.get('capture_gaps', [])]
        paths = defaultdict(list)
        for row in rows + historical + capture_gaps + historical_gaps:
            if row.get('raw_path'):
                self.verify_hash(row, 'raw_path', 'sha256', 'bytes')
            if row.get('served_path'):
                self.verify_hash(row, 'served_path', 'served_sha256', 'served_bytes')
            if row.get('local_path'):
                paths[row['local_path']].append(row)
            if row.get('status') == 'saved' and 'css' in row.get('content_type', '') and not row.get('local_path', '').endswith('.css'):
                self.issue('stylesheet_missing_css_extension', detail=row.get('local_path'))
        for row in manifest.get('reconstructed_files', []):
            self.verify_hash(row, 'path', 'sha256', 'bytes')
        if manifest.get('helper_script'):
            self.verify_hash(manifest['helper_script'], 'path', 'sha256', 'bytes')
        for local, group in paths.items():
            if len(group) > 1 and len({r.get('sha256') for r in group}) > 1:
                self.issue('distinct_captures_collide', detail={'path': local, 'urls': [r.get('original_url') for r in group]})
        summary_path = self.root/'snapshot.json'
        if summary_path.is_file():
            summary = json.loads(summary_path.read_text(encoding='utf-8'))
            if summary.get('snapshot_sha256'):
                self.verify_hash(summary, 'snapshot_path', 'snapshot_sha256', 'snapshot_bytes', fallback='snapshot.html')
        self.source_graph(rows, manifest)
        if historical:
            self.source_graph(rows + capture_gaps, manifest, source_rows=historical,
                              report_prefix='historical_navigation', self_override=True)
            self.counts['historical_pages_checked'] = len(historical)
        self.reachability(rows)

    def reachability(self, rows):
        """Ignore inventory/history links: they should not hide a broken menu."""
        entry = self.root/'snapshot.html'
        if entry not in self.pages:
            entry = self.root/'site'/'index.html'
        if entry not in self.pages:
            self.issue('site_entry_not_found', warning=True)
            return
        visited = set()
        frontier = [entry]
        while frontier:
            page = frontier.pop()
            if page in visited:
                continue
            visited.add(page)
            for ref in self.pages[page].refs:
                if ref.kind != 'navigation':
                    continue
                target = self.local(page, ref.url)
                if target in self.pages and (target == entry or target.is_relative_to(self.root/'site')):
                    frontier.append(target)
        expected = set()
        for row in rows:
            if row.get('kind') == 'page' and row.get('status') == 'saved':
                value = row.get('served_path') or ('site/' + row['local_path'] if row.get('local_path') else None)
                if value:
                    expected.add(self.root/value)
        unreachable = sorted(expected - visited)
        self.counts['site_pages_reachable'] = len(expected & visited)
        self.counts['site_pages_unreachable'] = len(unreachable)
        self.inventory['site_pages_unreachable'] = [self.name(p) for p in unreachable]
        for path in unreachable:
            self.issue('page_unreachable_from_site_menu', path, warning=True)

    def archive_zip(self):
        path = self.root/'website.zip'
        if not path.is_file():
            self.issue('zip_missing', detail='website.zip')
            return
        expected = {p.relative_to(self.root).as_posix(): p for p in self.root.rglob('*')
                    if p.is_file() and p != path
                    and (not self.args.json or p.resolve() != Path(self.args.json).resolve())}
        with zipfile.ZipFile(path) as archive:
            infos = [i for i in archive.infolist() if not i.is_dir()]
            names = [i.filename for i in infos]
            for name, count in Counter(names).items():
                if count > 1:
                    self.issue('zip_duplicate_entry', detail=name)
            for name in names:
                if name.startswith(('/', '\\')) or '..' in name.replace('\\', '/').split('/'):
                    self.issue('zip_unsafe_path', detail=name)
            for name in sorted(set(expected) - set(names)):
                self.issue('zip_missing_entry', detail=name)
            for name in sorted(set(names) - set(expected)):
                self.issue('zip_extra_entry', detail=name)
            for name in set(names) & set(expected):
                if hashlib.sha256(archive.read(name)).hexdigest() != digest(expected[name]):
                    self.issue('zip_content_mismatch', detail=name)
                else:
                    self.counts['zip_entries_verified'] += 1

    def run(self):
        for path in self.root.rglob('*.html'):
            if 'raw' in path.relative_to(self.root).parts:
                continue
            self.pages[path] = Page(path.read_text(encoding='utf-8', errors='replace'))
        for path, page in self.pages.items():
            self.active_content(path, page)
            for ref in page.refs:
                self.reference(path, ref)
        for path in self.root.rglob('*.css'):
            if 'raw' in path.relative_to(self.root).parts:
                continue
            for value in css_urls(path.read_text(encoding='utf-8', errors='replace')):
                self.reference(path, Reference(value, 'resource', 'css', 'url', 0))
        self.counts['html_pages_checked'] = len(self.pages)
        self.manifests()
        if self.args.check_zip:
            self.archive_zip()
        return {'root': str(self.root), 'passed': not self.errors, 'counts': dict(self.counts),
                'errors': self.errors, 'warnings': self.warnings, 'inventory': dict(self.inventory),
                'generated_markdown_links': self.generated_links}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('roots', nargs='+', type=Path)
    parser.add_argument('--web-root', help='Static document root for /absolute URLs and casing checks (default: archive root).')
    parser.add_argument('--allow-generated', action='store_true', help='Accept links whose target is generated from an existing .md file.')
    parser.add_argument('--opaque-origin', action='store_true', help='Report fonts/modules requiring CORS in an iframe without allow-same-origin.')
    parser.add_argument('--iframe-sandbox', default='allow-scripts', help='Sandbox flags granted by the wrapper, used with --opaque-origin to assess link/download behavior.')
    parser.add_argument('--require-coverage', action='store_true', help='Fail when raw-source navigation has no corresponding local served link.')
    parser.add_argument('--ignore-query-param', action='append', default=[], help='Explicitly ignore one query key only in source-navigation comparison; repeat as needed (for example PHPSESSID).')
    parser.add_argument('--check-zip', action='store_true', help='Compare website.zip entries and bytes with the complete archive directory.')
    parser.add_argument('--json', help='Write a detailed JSON report (prefer a path outside the archive).')
    args = parser.parse_args(argv)
    results = []
    for root in args.roots:
        if not root.is_dir():
            parser.error(f'Archive directory does not exist: {root}')
        try:
            result = Audit(root, args).run()
        except (OSError, ValueError, zipfile.BadZipFile) as error:
            result = {'root': str(root), 'passed': False, 'errors': [{'code': 'audit_failed', 'detail': str(error)}]}
        results.append(result)
        print(f"{'PASS' if result['passed'] else 'FAIL'} {root}: {len(result.get('errors', []))} errors, {len(result.get('warnings', []))} warnings")
        print(json.dumps(result.get('counts', {}), sort_keys=True))
        for error in result.get('errors', [])[:15]:
            print('  ' + json.dumps(error, ensure_ascii=False))
    report = {'passed': all(r['passed'] for r in results), 'archives': results,
              'limitations': ['Static URL extraction cannot prove runtime JavaScript navigation or server-side form behavior.',
                              'Source navigation coverage only covers recovered raw pages listed in each manifest.',
                              'Scripts, handlers, forms, and CSP need human review and a browser walkthrough.']}
    if args.json:
        target = Path(args.json)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
