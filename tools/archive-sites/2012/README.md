# April 2012 mirror recovery

These scripts resume and rebuild the QuinnDamerell.com mirror from its checked-in manifest and preserved raw sources. They do not execute historical JavaScript or fetch live-site replacements. The directory is specific to this archived website and its original navigation conventions; it is not a general-purpose crawler for arbitrary domains.

Requires Python 3.10+, `beautifulsoup4`, and curl (`curl.exe` on Windows). Run from the repository root. A cache directory outside the repository avoids interference from documentation builds.

```powershell
python tools/archive-sites/2012/recover_mirror.py `
  --output docs/assets/media/quinndamerell-homepage-2012 `
  --cache "$env:TEMP/wayback-2012-retrieval" `
  --inventory docs/assets/media/quinndamerell-homepage-2012/history/cdx-inventory.json `
  --reuse docs/assets/media/quinndamerell-homepage-2011 `
  --retry-missing

python tools/archive-sites/2012/build_mirror.py `
  --output docs/assets/media/quinndamerell-homepage-2012
```

`recover_mirror.py` reads the requested timestamp from `manifest.json`, follows internal links and referenced assets, and records bounded replay attempts. It verifies Memento headers and rejects HTML responses masquerading as images or scripts. Capture timestamps remain distinct from the requested timestamp. Existing successful raw files are retained unless explicitly retried with `--retry-url URL`; each retry updates the source provenance. An optional saved CDX inventory supplies the nearest known page capture before replay fallback. This tool does not claim that a failed request proves the archive has no copy.

Use `--reuse-only --retry-missing --reuse <other-archive>` to import matching recovered sources without network access. `--reuse-state` accepts an explicitly supplied recovery state file containing source-file paths, but no temporary state is required for normal operation. Content-bearing query parameters are retained; only PHPSESSID is removed. Distinct directory and explicit-index captures receive distinct local paths. A resource limit stops unexpected expansion for review.

`build_mirror.py` verifies original hashes, writes the local pages and gap notices, embeds recovered font bytes in CSS, and refreshes raw/served hashes and inventory counts. Original scripts remain inert `.txt` sources. The small generated helper restores image dialogs, the header flip, available hover artwork, and video selection without fetch, storage, parent access, or server submission. Native expandable photo groups and ordinary navigation anchors work without that helper. Missing original sections get explicit notices; no missing project text is invented.

The scripts preserve `history/`. They do not render screenshot/PDF artifacts or package the ZIP. After recovery, use the shared archive validator, renderer, and packager documented in `dev-docs/media-archive.md`. Review changed capture dates, unavailable resources, helper code, and browser behavior before publishing an updated archive.

## Additional exact historical captures

The manifest's `historical_pages` list explicitly selects other already preserved HTML captures for original-layout browsing. These variants live under `site/_captures/` and retain separate source/served hashes and exact timestamps. Their ordinary navigation uses the wider mirror; self-links stay on the selected capture. PageSpeed derivative URLs may reuse a recovered original asset, with the substitution and its source hash/date listed in each capture's `references` and `resource_aliases`. Missing new destinations receive per-capture local gap pages. No network requests occur.

Register a known reader filename from `history/manifest.json`, or omit `--add-historical` to rebuild the registered list:

```powershell
python tools/archive-sites/2012/build_mirror.py `
  --output docs/assets/media/quinndamerell-homepage-2012 `
  --historical-only `
  --add-historical 20120501190612-D5LFX4OT.html
```

`--historical-only` writes the selected variants, their local gap notices, the provenance manifest, and the additional-capture inventory section. It leaves the April homepage, ordinary mirror pages/assets, screenshot/PDF, and historical source files unchanged. A normal full build also reproduces the registered additional captures.
