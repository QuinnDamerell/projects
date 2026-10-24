# Complete personal website archives

Quinn requested local copies of his old personal websites that can be explored inside their Media pages. This supersedes the earlier one-off restriction. Each supplied Wayback timestamp is a separate archive; ordinary articles remain single-page snapshots. All Media entries containing `snapshot.html` share the same embedded browser frame, regardless of how many pages were recovered.

## Requested captures

| Media slug | Exact starting capture |
| --- | --- |
| `quinndamerell-homepage-2011` | `https://web.archive.org/web/20110116181801/http://www.quinndamerell.com/index.php` |
| `quinndamerell-homepage-2012` | `https://web.archive.org/web/20120416170518/http://www.quinndamerell.com/index.html` |

Each lives under `docs/assets/media/<slug>/`, with a corresponding `docs/media/<slug>.md` entry. Keep these paths stable because project pages also cite historical sources in the 2012 subtree.

## Recovery and provenance

Start with the exact homepage response and preserve its bytes in `raw/`. Crawl same-site navigation recursively, including links supplied by known JavaScript navigation handlers, image maps, nested CSS imports, background images, fonts, and gallery images. Rewrite PHP and query-based destinations to stable local HTML filenames. Preserve case and distinguish URLs that have different captures; a directory URL and its explicit `index.html` are not automatically interchangeable.

Wayback captures assets independently. Prefer the closest usable capture and record the actual capture timestamp and source URL for every recovered response. A later fallback must be labeled on the local page and in the inventory, never represented as contemporaneous with the requested homepage. A failed connection is a retrieval failure, not proof that no capture exists. Check returned MIME/content as well as status: an HTTP 200 homepage fallback is not a recovered image or JavaScript file.

Keep every reachable same-site destination local, including a local gap notice when a usable capture cannot be obtained. External navigational links may point to the archived or original external destination and open separately. External destinations are not implicitly additional full-site mirrors.

Do not invent original pages, images, project facts, server responses, or successful account actions. Missing images get a visible explanation where needed; missing decoration can be omitted with a manifest entry. Save raw executable text inertly as `.txt`, and retain real binaries in Git LFS. Every hosted file must remain below 25 MB.

## Browsing and interactions

`snapshot.html` starts the local site; `site/` holds pages and assets. Preserve original visual styling and fixed desktop dimensions. On narrow screens the iframe scrolls horizontally, without widening the surrounding Media page.

Retain ordinary links. Convert simple legacy navigation handlers such as `location.href` and `goToByScroll` to normal anchors before removing handlers. Restore image rollovers and screenshot galleries with small inspected local helpers where appropriate. Galleries must retain direct-image links as a fallback and support closing with Escape. Avoid executing arbitrary old libraries, trackers, or Java applets just to recover one interaction. Contact forms, authentication, databases, and other server-dependent behavior remain unavailable and are labeled accordingly.

Every Media page with a local `snapshot.html` uses `<figure class="qd-archive-frame qd-archive-frame--site">`. Its browser-style toolbar has three decorative window dots marked `aria-hidden="true"`, an address field showing the original URL, and an “Open separately” anchor styled as a button. That anchor links to `snapshot.html`, with `target="_blank"`, `rel="noopener"`, and `<span class="qd-visually-hidden"> in a new tab</span>` after the visible label. Hide only the dots from assistive technology; keep the address and button accessible. There is no “Start page” control.

The iframe uses `class="qd-archive-frame__site"`, `name="qd-archive-<slug>"`, a descriptive `title`, `loading="eager"`, `width="1280"`, `height="900"`, and `referrerpolicy="no-referrer"`. Place PDF, screenshot, Wayback, and available ZIP actions below the frame. Do not add a separate “Read the archived page” action. Articles and the CrossTxT homepage use the same frame and controls as the full personal sites.

Choose the sandbox according to the archived content:

- Static article and CrossTxT snapshots use `sandbox="allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-downloads"`, with scripts disabled. CrossTxT's CSS-only tabs remain usable.
- The full 2011 and 2012 archives use `sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-downloads"`, without same-origin access. Only their inspected local helpers execute.

Do not combine `allow-same-origin` with scripts: a script-enabled archive should not be able to reach its parent page or storage. Its local helper must work without fetch, storage, or parent DOM access. Embed font bytes in served CSS when necessary to avoid opaque-origin font CORS failures; retain the original font responses separately.

Each archived document has a restrictive Content Security Policy. Allow only local/data resources and explicitly inspected local helpers; block remote automatic loads, forms, objects, and base URL changes. Internal links remain inside the iframe; external links use a new tab. Preserve the original source separately from this browsable derivative.

## Files and verification

| File | Purpose |
| --- | --- |
| `snapshot.html` | Local starting page |
| `site/` | Local pages, images, styles, and interaction helpers |
| `raw/` | Exact recovered source bytes, with executable text stored inertly |
| `archive-index.html` | Human-readable file list, capture dates, and gaps |
| `manifest.json` | Source URLs, requested/actual dates, statuses, paths, and checksums |
| `snapshot.json` | Starting capture and summary metadata |
| `snapshot.png`, `snapshot.pdf` | Rendered homepage reference copies |
| `README.txt`, `website.zip` | Offline opening instructions and downloadable bundle |

The 2012 `history/` folder is a separate source collection for the earlier project-history review. It is not a full mirror of every historical revision. Project-page citations should link to the corresponding browsable HTML under `site/`, matching the original capture timestamp and raw source bytes. Use the 2011 archive for its matching early pages and the 2012 archive for later pages. When a cited revision differs from the main mirror, retain its exact source as a dated page under the 2012 `site/_captures/` directory, with local assets and navigation into the surrounding archive. These supplemental pages preserve individual revisions, not an entire additional site snapshot. Keep the history readers and their raw sources as research records; do not redirect a date-specific citation to a different revision merely because its URL matches.

Validate the finished archive with `tools/check_site_archive.py`, inspect the reported script/resource inventory, and test actual navigation and galleries in the sandboxed Media iframe. Check desktop and phone width, both site color schemes, recovery notices, browser-style chrome, and the “Open separately” button. Run the normal LFS check and a clean build in a separate temporary copy when a live Zensical watcher is using the shared cache.

After all archive files are stable, run `python tools/package_site_archive.py docs/assets/media/<slug>`. The packager verifies every byte, refuses files/packages above 25 MB, and excludes the output ZIP itself. Repackage whenever archive content changes. Do not use the single-page `snapshot.mjs` on either full archive directory.

## Current recovery and checks

The October 17, 2026 recovery preserves the exact requested homepage bytes for both snapshots. Counts below exclude the separately labeled historical source collection and generated helper resources.

| Capture | Recovered pages | Recovered resources | Recorded unavailable references | ZIP files | ZIP bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| January 2011 | 11 | 76 | 116 | 270 | 5,557,813 |
| April 2012 | 23 | 169 | 122 | 516 | 15,884,740 |

The source-navigation audit accounts for all 158 internal links in the 2011 sources and all 276 in the 2012 sources, either as recovered destinations or explicit local gap pages. Every recovered page is reachable through the site's own navigation. The audit checks local paths, case-sensitive deployment paths, fragment targets, raw and served hashes, gallery image targets, CSP compatibility, and iframe restrictions. No errors or warnings remained. The ZIP packager verified every bundled byte against the saved tree.

The October 18 citation update replaced 23 history-reader links across 12 project pages. Nine distinct captures match pages already in the complete mirrors. Five additional dated pages under `site/_captures/` retain the exact cited raw sources, reuse recovered assets, and link into the full archive. Their 83 internal navigation links resolve to 73 recovered/self destinations and 10 explicit gaps. These supplemental captures do not change the main mirror counts above; the 2012 ZIP includes them and five new gap notices. The 167 existing site files remained byte-identical. Final source, served-file, navigation, and ZIP checks passed with no errors or warnings.

Browser checks followed a project citation into the 2011 archive, inspected all five supplemental captures, opened the November Baconit gallery, and navigated back into the main 2012 portfolio. The 2009 page uses a documented solid sidebar background and small text bullets where decorative images are unavailable. A clean isolated build and LFS checks passed; the local preview includes the updated pages and archive bundle.

The initial browser checks covered actual in-frame navigation, the then-present start-page control, 2012 Baconit screenshot navigation and Escape/focus return, 2011 photo categories and gallery navigation, and 2011 video-tab switching. The start-page control was subsequently removed from the Media toolbar. The video panels show the original YouTube destinations and explain the missing Flash player. Both Media pages were checked at desktop size and at 390-pixel phone width, with dark and light site themes; the legacy fixed-width content scrolls inside the frame without widening the outer page. Both homepage renders loaded no remote resources and had no broken image loads. PNGs and one-page PDFs were generated and visually inspected. Git LFS pointer checks and a clean build in an isolated temporary copy passed.

The original Wayback retrieval record includes gaps for full-size legacy photos, the separate Next Bus/TxTBack/Thinking of You pages, and obsolete Java/Flash/download resources. The October 21 local-backup supplement below now supplies many of those files with separate provenance; it does not rewrite the Wayback retrieval results. Thumbnail substitutions remain limited to established image pairs and are labeled. The old school-video players still have no recovered video binaries. Server-side account actions and forms cannot work from captured HTML.

## October 21 local-backup restoration

Quinn found the original files in `D:\Website Archive\Websites\Backups\Personal\Personal` and `D:\Website Archive\Websites\Personal\2023`, and authorized adding the recovered media. D: was read-only throughout. Selected public pages, assets and Java files were copied to the ignored `.cache/local-website-backups/{old,later}/` on C: because the encrypted archive drive can close automatically. Backend endpoints, authentication sources, private notes and unrelated executables were excluded from staging.

Both archives now contain a separately labeled `site/local-backup/` collection with 51 static pages. It includes the Fireworks and Crazy Horse websites, the animation-site pages, Java applet wrappers, the original project/website indexes, PicGen, Zune Playlist Shuffler, Reddit Time Machine, Next Bus, TxTBack and Thinking of You. Next Bus and TxTBack are authentic “coming soon” pages, not reconstructed product descriptions. Thinking of You has its original landing page and local artwork. Original applet binaries and the two Java program downloads are preserved but never executed. The playable Flash collection lives on the main Early Experiments page, linked from these supplements.

The larger Miss Indiana photos, senior photos and original gallery images now open from existing gallery links. A provenance link retains the original Wayback gap destination. The supplement also has a dedicated photo collection, including nine larger photos each from the 2009 and 2010 productions. Original Wayback `raw/` bytes, requested capture dates, retrieval histories, and original saved/unavailable statuses remain unchanged. Former gap pages now explain that a separate local copy was found and link to it; these are not claims that Wayback successfully recovered those files.

| Archive | Gap pages linked to local copies | Existing gallery links restored | ZIP files | ZIP bytes |
| --- | ---: | ---: | ---: | ---: |
| January 2011 | 85 | 39 | 610 | 11,256,076 |
| April 2012 | 51 | 39 | 853 | 21,574,134 |

The path-match counts from the discovery scan were provisional; the table above counts completed, published recovery links. `local-backup-manifest.json` records each input's relative original path, SHA-256, byte count, published path and transformation. Original HTML is retained inertly in `local-backup-sources/`. For PHP public pages, only the HTML with every PHP block removed is distributed; the input checksum is recorded without publishing server code. The top-level manifest retains its original records and adds `local_backup_supplement`, per-gap `local_backup` metadata, and checksum-verified reconstructed files. Both file indexes and Media wrappers link to the collection.

The local website index says 2002 / 2004 / 2005 for the animation, Fireworks and Crazy Horse sites, while the January 2011 Wayback index says 2004 / 2006 / 2007. The original versions and this disagreement remain visible. Backup folder dates and copied timestamps do not establish publication dates.

`tools/restore_local_website_backups.py` rebuilds the supplements from staged inputs, falling back to the original D: paths only when staging is absent. Its output guard confines writes to this repository on C:. It requires BeautifulSoup, never executes historical PHP/Java/Flash, removes old executable scripts and trackers, disables forms and plugin objects, rewrites resources locally, and applies a restrictive CSP. No remote resources load automatically. Existing sandbox and archive-helper contracts are preserved. Run it with the repository Python, then repackage both archives:

Staging under `.cache/` is temporary and may be removed by a clean Zensical build. Published media and provenance do not depend on it. If the archive folders move or staging is gone, reconnect the drive and pass `--old-root "<current oldest-backup path>" --later-root "<current later-backup path>"`. Both input directories are checked before any output is written. The original discovery paths remain in the provenance record even when a source directory has subsequently been renamed.

```powershell
.venv\Scripts\python tools/restore_local_website_backups.py
.venv\Scripts\python tools/package_site_archive.py docs/assets/media/quinndamerell-homepage-2011
.venv\Scripts\python tools/package_site_archive.py docs/assets/media/quinndamerell-homepage-2012
```

Static archive checks pass with zero errors and warnings, accounting for all 158 and 276 original main-site navigation links plus 83 historical-page links. Both ZIPs are byte-verified and below the 25 MB limit. The homepage HTML and original screenshot/PDF were not changed; their reference captures remain valid. Browser checks verified both wrapper sandboxes, 390-pixel layouts, light/dark themes, and recovered full-size photos in both gallery helpers. The 2011 helper's Next, Escape, and focus return were also checked. Crazy Horse and Thinking of You render their recovered images. The Fireworks entry originally used a Flash title and HTML frames; its static derivative now links to the surviving catalog and home pages instead of attempting blocked frames. The original frameset source remains inert and unchanged.

Portable, site-specific recovery and publication scripts live in [`tools/archive-sites/2011/`](../tools/archive-sites/2011/README.txt) and [`tools/archive-sites/2012/`](../tools/archive-sites/2012/README.md). They require Python, BeautifulSoup, and curl, accept explicit output/cache locations, and retain original sources and provenance. The 2011 publisher was also verified from a fresh cache using only retained manifest/raw files. Re-run rendering, packaging, and validation after rebuilding either archive; old screenshot/PDF/ZIP output can otherwise be stale.
