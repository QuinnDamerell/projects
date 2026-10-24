# Tools

## snapshot.mjs

Captures a web page for the Media archive: a full-page screenshot, a PDF, and a self-contained HTML copy. It drives the locally installed Chrome or Edge over the DevTools protocol and needs no npm packages (Node 22 or newer).

```sh
node tools/snapshot.mjs <url> <slug> [--image <match>=<replacement>] [--remove <selector>] ...
```

- `<url>` is a live page or a Wayback Machine link (`https://web.archive.org/web/<timestamp>/<url>`). For Wayback links, the copy records both the original URL and the capture.
- `<slug>` names the output folder, `docs/assets/media/<slug>/`, which is recreated on each run.
- `--image <match>=<replacement>` swaps a broken image for a copy found elsewhere. `<match>` is any part of the original image URL, and `<replacement>` is a URL (Wayback links are converted to raw `id_` downloads) or a local file. When images are swapped, the page as it originally loaded is also kept as `as-captured.png`.
- `--remove <selector>` deletes every element matching a CSS selector before and after the scroll pass. Use it, repeated, to leave out ads and endless "more stories" feeds; [media-archive.md](media-archive.md#archiving-a-web-page) has the selectors used for Windows Central and OnMSFT. The notice bar in the HTML copy then says ads and unrelated sections were left out, and `snapshot.json` lists the selectors.
- Set `CHROME_PATH` if Chrome or Edge isn't in a standard location.

### Output

| File | Contents |
| --- | --- |
| `snapshot.png` | Full-page screenshot at 1280 px wide: the faithful visual record |
| `snapshot.pdf` | Print version with selectable text |
| `snapshot.html` | Static copy: scripts, iframes, trackers, and event handlers removed; stylesheets inlined; images saved to `images/`; YouTube embeds replaced with a thumbnail link; a notice bar at the top; `noindex` and a canonical link to the original |
| `images/` | The page's images, including restored ones and YouTube thumbnails |
| `snapshot.json` | URL, title, site, publication date when the page states one, capture time, Wayback source, restored images, and YouTube links |

Fonts and background images referenced from CSS still load from their original (or Wayback) addresses. If those disappear, the HTML copy falls back to system fonts; the screenshot and PDF are unaffected.

### How it works, and why

- **Rendering.** It loads the page at 1280×900, scrolls through it once (for up to 20 seconds) so lazy images load, waits up to 20 seconds for pending images (archived images often go through several slow redirects), then waits for fonts.
- **Screenshots.** It grows the viewport to the full page height before capturing. `captureBeyondViewport` leaves cross-origin iframes, such as YouTube embeds, blank.
- **Isolated world.** All in-page code runs in a DevTools isolated world, which shares the DOM but not the page's JavaScript. Wayback pages run `wombat.js`, which patches built-ins so that `href`, `src`, `sheet.href`, `getAttribute`, and even `outerHTML` report original addresses instead of archived ones. Reading through those patches sends downloads to dead servers and strips every archive link from the copy. Blocking wombat isn't a fix either, because old pages that rewrite image URLs in JavaScript then point at the wrong place. Isolation gets the true values while the page still renders correctly.
- **Stylesheets** are read from the browser's CSS engine (`CSS.getStyleSheetText`) rather than downloaded again, then inlined in place of their `<link>`. `url()` references are made absolute. `:defined` selectors are neutralized, because custom elements never get defined without scripts, and Microsoft's header and footer, for example, would stay hidden.
- **Links** in archived copies are pointed at their Wayback versions.
- **Image downloads** send the page as the `Referer`, since some sites refuse images requested without one.
- **Robustness.** Downloads time out after 30 seconds, and each in-page step after 90. JavaScript dialogs are dismissed automatically. Progress is printed at each stage, so a stall shows where it happened.

### Troubleshooting

- **A run hangs or is slow.** The Wayback Machine is often slow and occasionally offline. Retry later. Captures of old pages typically take one to three minutes.
- **The article's photos show as broken on a Wayback copy.** Try a capture from a different date, or find the image elsewhere and pass `--image`.
- **The live site returns 403 to `curl`.** That's fine, because the script uses a real browser with a normal user agent.
- **The screenshot is a bot check or CAPTCHA page.** Use a Wayback copy instead. Don't try to solve or bypass the check.
- **The page is enormous.** Endless feeds, sponsored "next article" loaders, and sticky ad columns. Find their selectors and pass `--remove`.

## Complete website archives

The complete personal-site mirrors use a separate workflow from `snapshot.mjs`; see [website-archives.md](website-archives.md). These tools preserve the archived HTML tree rather than flattening it into one page.

### check_site_archive.py

Checks local HTML and CSS references, case-sensitive paths, fragments, source navigation coverage, raw/served checksums, content security policies, and optional ZIP integrity. Local interaction scripts are reported for inspection rather than banned. Use `--opaque-origin` for the sandboxed Media iframe and `--allow-generated` for documented restoration files.

```sh
python tools/check_site_archive.py docs/assets/media/quinndamerell-homepage-2011 docs/assets/media/quinndamerell-homepage-2012 --web-root docs --allow-generated --opaque-origin --iframe-sandbox "allow-scripts allow-popups allow-popups-to-escape-sandbox allow-downloads" --require-coverage --ignore-query-param PHPSESSID --check-zip
```

`--require-coverage` makes uncovered source-navigation destinations errors; a recorded local gap notice counts as covered navigation. Dated `historical_pages` are checked separately from the main mirror so multiple captures of one original URL cannot replace its normal navigation target. `--json <file>` saves the machine-readable audit. Browser-test navigation, images, and galleries as well; structural validation cannot prove that an interaction works.

### render_site_archive.mjs

Renders an already recovered local homepage to `snapshot.png` and a one-page `snapshot.pdf`, updating the dimensions in `snapshot.json`. Requires Node 22+ and Chrome or Edge, with `CHROME_PATH` available for other installation locations. It starts its own loopback server and temporary headless browser, checks for broken images and automatic remote requests, and never rewrites the archived HTML.

```sh
node tools/render_site_archive.mjs docs/assets/media/quinndamerell-homepage-2011
```

Inspect the PNG and render the PDF for visual verification. This tool is for local archive directories only; use `snapshot.mjs` for a single external web page.

For an already recovered, self-contained article or discussion transcript, add `--paginated` to produce a normal A4 PDF while keeping the full-height screenshot. This avoids the single-page homepage PDF's height restriction. The default homepage behavior is unchanged. Both modes require `manifest.json` and reject broken images or automatic remote resource requests.

## reddit_archive.py

Recovers the selected Reddit discussions from Arctic Shift's documented public archive API. It creates static transcripts and unlisted archive wrappers, preserving post/comment text, authors, UTC dates, parent relationships, exact comment IDs, raw responses, retrieval metadata, and checksums. It does not operate the live Reddit site or solve its access challenges.

```powershell
.venv\Scripts\python tools/reddit_archive.py --audit <audit-data.json> --results <capture-reddit-results.json>
```

Requires Python's `markdown` package and native `curl.exe`. The current thread-to-slug mapping is explicit in the script. Successful raw responses are cached in each archive's `raw/` folder; rerunning rebuilds the transcript from those saved responses. Review the requested thread mapping before extending the tool to another collection.

The coverage record distinguishes recovered comments from the post's observed count; differing counts cannot establish completeness. Missing parents, unresolved collapsed records, deleted/removed placeholders, and missing cited IDs are disclosed. A later removed post can have an earlier surviving archive body; its observation date must remain visible. Cited comments get anchors on the wrapper and in the complete transcript. Original linked media and unrelated outbound pages are not implicitly copied.

The October 18, 2026 WordPress recovery uses the same provenance principle: `3dp-and-me-octoeverywhere-klipper-2023/source.json` retains the official public post API response, and `snapshot.json` records the API address, publication/edit dates, image downloads, and checksums. Its HTML is a labeled reading copy with simplified formatting, not a claimed screenshot of the blocked site. The screenshot and PDF render that recovered HTML.

### package_site_archive.py

Creates `website.zip` from all files in a finished archive, excluding the existing ZIP itself. Every member is verified against the source bytes before the ZIP is replaced. The command rejects symlinks, files over 25 MB, a ZIP over 25 MB, and sources that change during packaging. It leaves any previous ZIP intact on verification failure.

```sh
python tools/package_site_archive.py docs/assets/media/quinndamerell-homepage-2011
```

Always package after rendering and final manifest/README edits; repackage whenever any archive file changes.

## check_lfs.py

Fails with a list of offending files if anything in `docs/` is a Git LFS pointer rather than the real file, which happens when a checkout skips the LFS download. It runs first in the Cloudflare Pages build command (see [site.md](site.md#deployment)), so a bad checkout fails the build instead of deploying broken images.

```sh
python tools/check_lfs.py            # checks docs/
python tools/check_lfs.py <folder>   # checks another folder
```

## upload_r2.py

Uploads a file to the R2 bucket behind `https://projects-storage.quinn.space`, keeping its file name. Use it for files over the dashboard's 300 MB limit. It uploads in parallel 64 MB parts and shows progress.

```sh
pip install boto3
python tools/upload_r2.py <file> <api-token>
```

- Set `ACCOUNT_ID` and `BUCKET` at the top of the script once, or pass `--account-id` and `--bucket` (or set `R2_ACCOUNT_ID` and `R2_BUCKET`).
- `<api-token>` is an R2 API token value with Object Read & Write access. The script derives the S3 credentials from it: the access key ID is the token's ID (looked up through Cloudflare's token verify endpoint), and the secret is the SHA-256 hash of the token value. To use the S3 credentials the dashboard shows instead, pass the secret as `<api-token>` and add `--access-key-id <id>`.
- It refuses to replace an existing object with the same name unless you pass `--overwrite`.
- It prints the public URL when done. Use that URL, percent-encoded, in the page.
- Boto3 is not in `requirements.txt` on purpose, because that file is the Cloudflare Pages build environment. It's installed in the local `.venv`.
