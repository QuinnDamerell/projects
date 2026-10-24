# How the site is built

projects.quinn.space is a static site built with [Zensical](https://zensical.org/) (the successor to Material for MkDocs) using its modern theme. The version is pinned in `requirements.txt`; keep it pinned, since older releases lack features the site uses.

## Layout

| Path | Purpose |
| --- | --- |
| `zensical.toml` | Site settings, theme, palette, plugins, and Markdown extensions |
| `docs/` | Published content. Every file here ends up on the site. |
| `docs/.nav.yml` | Sidebar order and labels for projects, Career, and selected Media (awesome-nav). Pages not listed still build; they just aren't in the sidebar. |
| `docs/index.md` | Home page (`template: home.html`), a hand-written bento grid and the project timeline in raw HTML |
| `docs/<project>.md` | One page per project |
| `docs/media/` | The Media tab: 18 selected stories and two personal-site Time capsules on its index, plus all individual archive pages. See [media-archive.md](media-archive.md). |
| `docs/career/index.md` | The Career tab: patents and awards above an editable timeline with a separate block and year span for each job or work area. See [career.md](career.md). |
| `docs/assets/` | Images and other files. Project images are in `assets/<project>/`, and archive snapshots are in `assets/media/<slug>/`. |
| `docs/stylesheets/extra.css` | All custom styling, split into commented sections |
| `overrides/` | Template overrides: `main.html` (fonts, icons, Matomo), `home.html`, `partials/header.html` |
| `tools/` | Archiving tools. See [tools.md](tools.md). |
| `site/` | Build output (gitignored) |

## Header tabs

The links at the top ("Projects", "Career", "Media", "About Me") are hand-written in `overrides/partials/header.html`, in the `qd-header-links` block, not generated from navigation. To add a tab, add another `<a class="qd-header-link">`. The Career and Media links get `aria-current="page"` on pages under their respective routes, which `extra.css` styles as active. `main.html` also subscribes to the theme's `document$` stream to refresh active links after instant navigation, which preserves the header. Below 50em the links wrap onto a second header row so every section stays available on phones. The Career page is also listed in `.nav.yml` for drawer navigation.

The sidebar's Media group in `docs/.nav.yml` mirrors the approved index selection: its index, 18 stories, and a nested Time capsules group for the 2012 and 2011 personal websites. Keep the group aligned when an editorial selection changes. Other media archives remain reachable from project references and related archive pages, even when absent from the index and sidebar. The main header continues to link to the single Media index.

## Styles

The homepage's main title tile has three compact, text-only actions: **My Projects** scrolls to `#collection`, **My Career** opens `career/`, and **About Me** opens `https://quinn.space`. Their smaller sizing is scoped to `.qd-intro`, leaving other buttons unchanged. They wrap as needed and retain 44px-high targets on phones.

The home page keeps all project stories in one timeline. Recovered projects use their earliest documented year when the start year is unknown, with that distinction retained in the entry; the early experiments collection sits at the end as “Early work.” Keep the projects-per-year chart and its accessible description in sync with these groups. The collection contains 26 project stories. Only add a new project page when Quinn explicitly selects it for the site.


`extra.css` defines the palette as `--qd-*` custom properties for both schemes (`slate` is dark and the default, `default` is light) and maps them onto Zensical's `--md-*` variables. Use the tokens rather than raw colors so both schemes work. The main sections are:

- Site-wide basics, header, and footer
- Project pages (`.md-typeset` tweaks) and `.product-capture` figures
- Archived Media pages: `.qd-archive-meta`, `.qd-archive-actions`, the shared `.qd-archive-frame.qd-archive-frame--site` browser frame with its `.qd-archive-frame__site` iframe, and `.qd-archive-video` for video players
- The home page: `.qd-home`, `.qd-bento`, `.qd-tile`, `.qd-card`, and the year timeline (`.qd-year`, `.qd-entry`)
- The Media page, which reuses the home page's year timeline inside `.qd-home.qd-media`
- The Career page, which reuses the timeline inside `.qd-home.qd-career`, with one `.qd-year` per job or work area. Its `.qd-year__label` shows the full year span at `1.2rem`, a single year for same-year roles, or `Dates to add` when the span is unknown. The Microsoft work-area starters are independent top-level sections, with editable Markdown bodies and Microsoft in their metadata. Patents and awards sit in the Achievements block above the timeline; patent details expand natively. Career entries use `.qd-career-entry` so inline links do not inherit the archive's full-row link styling. See [career.md](career.md) for date and source guidance.

## Local preview

### Writing for browsing and remembering

Keep project introductions brief and personal: what it was, why it existed, and the detail that makes it worth exploring. Use plain language, a relaxed professional tone, and light humor where the story earns it. Preserve facts, dates, figures, collaborators, uncertainty, source links, and original media when tightening prose. Historical source files under `docs/assets/` remain unchanged.

Write project pages in Quinn's own voice: first person, friendly, and direct, like Quinn's founder posts on the [OctoEverywhere blog](https://blog.octoeverywhere.com/) and [Homeway blog](https://blog.homeway.io/). Talk to the reader ("you could pin a story to Start"), tell the project's story rather than how it was researched, and let the fun parts show a little enthusiasm ("Do you have what it takes to crack the whip?"). Keep uncertainty, but say it the way a person would: "I don't know exactly when I made it," not "the exact creation date hasn't been established." In project stories and their reading lists, avoid audit wording such as *establish*, *records*, *preserves*, *surviving*, *recovered source*, *unconfirmed*, or *direct access was not confirmed*. Media archive wrappers and Reddit transcripts may keep precise provenance notes.

Long feature histories, galleries, and source lists can use `<details class="qd-story-details" markdown="1">` with a specific `<summary>` and blank lines around the Markdown body. Keep the main story visible; short pages need no disclosure. Preserve existing heading IDs when renaming headings so old links still work. Retain `markdown="1"` for parsed content, and do not indent the HTML wrapper.

`docs/javascripts/story-details.js` adds **Expand all details** on pages with multiple story disclosures, reveals sections reached by fragment links (including instant navigation), and expands the full record for printing before restoring the previous state. Native disclosures also work without JavaScript. Styling lives beside the project-page rules in `extra.css` and uses both theme palettes.

The table of contents lists only first- and second-level headings (`toc.toc_depth = 2`) to keep long project pages easy to scan. Deeper headings and their direct links remain in the page. Facts tables use the compact label **Code** and tighter cell spacing on phones.

### VS Code dev container (recommended on Windows)

Open the repository with **Dev Containers: Reopen in Container**. The attach command starts Zensical inside `/workspaces/personal-projects`, and VS Code forwards port **8000**. Open <http://localhost:8000/career/> for the Career page. Saving Markdown, styles, or templates rebuilds the page and refreshes the browser automatically.

The container uses `ZENSICAL_POLL_WATCHER=1` with `ZENSICAL_POLL_INTERVAL=500` because file-change events can be missed on Windows bind mounts. This is Zensical's [supported Docker-on-Windows polling mode](https://github.com/zensical/zensical/releases/tag/v0.0.28). `flock` keeps repeated VS Code attachments from starting duplicate preview servers. The forwarded port is labeled **Zensical live preview** and opens in the browser; VS Code reports a collision if local port 8000 is unavailable.

To start the same preview manually inside the container:

```sh
flock -n -E 0 /tmp/personal-projects-preview.lock env ZENSICAL_POLL_WATCHER=1 ZENSICAL_POLL_INTERVAL=500 zensical serve -a 0.0.0.0:8000
```

If a preview is already running, this command exits without starting another. If the server exits after a build error, fix the error and run it again. Container configuration changes take effect on the next reopen/rebuild.

### Native Windows preview

Use this alternative when the container preview is stopped:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\zensical serve -a 127.0.0.1:8001
```

`.claude/launch.json` has a `zensical` configuration on port 8001 for the Claude desktop preview pane. The server rebuilds on changes. If the build fails, the server process exits and prints the template error. Port 8001 is separate from the container's live preview on 8000. Do not use `python -m http.server` for editing: it only serves the last generated `site/` output and cannot rebuild or reload on save. Avoid running two Zensical servers or a separate build against the same workspace's shared cache/output; use an isolated copy for independent build checks.

## llms.txt

Zensical's native `llmstxt` plugin (since 0.0.67; it replaces the MkDocs `mkdocs-llmstxt` plugin) is configured under `[project.plugins.llmstxt]` in `zensical.toml`. Each build writes three things into `site/`:

- `/llms.txt`: the site name, `site_description`, the `markdown_description` paragraph, and a linked list of pages under `## Projects`, `## Career` and `## Media`, following the [llms.txt format](https://llmstxt.org).
- A Markdown copy of every listed page beside its HTML, such as `/crack-the-whip/index.md`.
- `/llms-full.txt` (`full_output`): every listed page's Markdown in one file.

Every page's `<head>` gets `<link rel="describedby">` to `llms.txt`, and listed pages also get `<link rel="alternate" type="text/markdown">` to their copy. The plugin needs `site_url`.

Only pages matched by a `sections` entry are included. Entries are paths relative to `docs/` or `fnmatch` patterns, and `*` also matches `/`, so `"*.md"` would repeat every Career and Media page under Projects. Projects are therefore listed one by one in `docs/.nav.yml` order. **When adding a project page, add it to both `.nav.yml` and the `Projects` list.** Career and Media use `career/*.md` and `media/*.md`, so new Media archives are picked up automatically. The home page is left out because its timeline is hand-written HTML links, which the Markdown copy reduces to empty bullets. Standalone HTML pages, such as the Crack the Whip app, are not Markdown and are never listed.

The theme's **Copy as Markdown** page button uses the same Markdown copies. It is not enabled; adding `content.action.copy` to the theme features would turn it on.

Verified on October 22, 2026 with Zensical 0.0.70 in an isolated build: 26 Projects, 1 Career and 79 Media entries with no duplicates, a 13 KB `llms.txt`, a 286 KB `llms-full.txt` and 106 Markdown copies.

## Deployment

Cloudflare Pages builds and publishes `site/` with this build command:

```sh
python tools/check_lfs.py && pip install -r requirements.txt && zensical build --clean
```

`tools/check_lfs.py` fails the build if any file in `docs/` is still a Git LFS pointer (see [Git LFS](#git-lfs) below), so a checkout without the LFS files can't deploy a site with broken images. The build command lives in the Cloudflare dashboard, not in this repository.

Keep the build-output ignore rule anchored as `/site/`. A bare `site/` also ignores the preserved websites at `docs/assets/media/quinndamerell-homepage-2011/site/` and `docs/assets/media/quinndamerell-homepage-2012/site/`. That caused production 404s for their pages, stylesheets, scripts, and images even though local previews and ZIP downloads worked. Track the complete archive trees, and validate archives from a clean checkout as well as the working directory; files that exist only locally can hide deployment omissions.

The complete website archive trees also use `-text` in `.gitattributes`. Their manifests and ZIPs verify exact bytes, so Git must preserve each file's captured line endings across Windows and Linux. Keep the historical whitespace intact; binary files still use their existing Git LFS filters.

Pages rejects files over 25 MB, so large media goes to the Cloudflare R2 bucket served at `https://projects-storage.quinn.space` instead. Upload through the R2 dashboard for files up to 300 MB, or with `tools/upload_r2.py` for anything larger.

## HTTP caching

`docs/_headers` is copied to `site/_headers` and controls browser caching on the next Cloudflare Pages deployment:

| Files | Browser cache policy |
| --- | --- |
| Generated `/assets/stylesheets/*.min.css` and `/assets/javascripts/*.min.js` | One year, `immutable`; Zensical includes a content hash in each filename. |
| Images, fonts, PDFs, ZIPs, MP3s, WAVs, and SWFs under `/assets/`, plus `/favicon.ico` | One week; do not mark these unversioned files immutable. |
| Pinned `/assets/vendor/ruffle/0.7.1/` runtime | One year, `immutable`; upgrades use a new versioned directory. |
| Custom `/stylesheets/` and `/javascripts/` | `public, no-cache`: browsers can store them but must revalidate before reuse. |
| HTML, search data, and other files | Pages' default `public, max-age=0, must-revalidate`. |

For binary assets, a deployment or CDN purge cannot evict visitors' browser caches. Change the filename and its references when a replacement must appear immediately; otherwise allow up to one week. Keep unversioned code outside the generated bundle directories, and verify that bundle names still contain content hashes when upgrading Zensical. Do not add a blanket `/assets/*` immutable rule: that directory also contains editable archive HTML, metadata, and source files.

Cloudflare Pages already caches deployed assets internally and manages deployment freshness. Keep that behavior instead of adding a broad custom-domain Cache Everything rule. In the Cloudflare dashboard, Browser Cache TTL should respect existing headers, with no Cache Rule overriding this split. `_headers` rules that overlap combine duplicate header values, so keep the cache policies disjoint. If Functions or a Worker start generating responses, set their headers in that code; `_headers` applies to static asset responses. See [Pages caching](https://developers.cloudflare.com/pages/configuration/serving-pages/), [header rules](https://developers.cloudflare.com/pages/configuration/headers/), and [Browser Cache TTL](https://developers.cloudflare.com/cache/how-to/edge-browser-cache-ttl/set-browser-ttl/).

Live audit on October 18, 2026, before this policy was deployed: `projects.quinn.space` returned revalidation headers for HTML/search and a four-hour browser TTL for sampled CSS, JavaScript, logos, and a hero image. Asset responses included ETags. The four-hour TTL suggests a dashboard browser-cache setting; its actual configuration was not inspected. After deployment, verify representative URLs with `curl -I`, including a generated bundle, `stylesheets/extra.css`, an image, and `career/`; the local Zensical server does not implement Cloudflare's `_headers` behavior.

`projects-storage.quinn.space` is a separate R2 host and is not affected by this file. The sampled `youtube-chris-riley-octoeverywhere-klipper-2023.mp4` returned no `Cache-Control` and `CF-Cache-Status: DYNAMIC`. Existing R2 object metadata and that host's cache rules need a separate update for explicit browser/edge caching; `tools/upload_r2.py` currently sets only content type, and dashboard uploads are separate. Do not assume a Pages deployment changes those videos' caching.

## Git LFS

The recovered audio and Flash player are documented in [local-recovery.md](local-recovery.md), including runtime provenance, cache rules, security settings and verification.

The standalone Crack the Whip easter egg is documented in [whip-app.md](whip-app.md). It uses a viewport-filling black Windows Phone layout outside the site's navigation and theme shell. An arrival dialog enables motion on **ok**; turning the phone more than 30° to the left within its screen plane plays the whip, then more than 30° to the right plays the crack, strictly alternating, as in the app's diagrams.

Binary media (images, PDFs, audio, video, and archives) and the Media archive's `snapshot.html` copies are stored with [Git LFS](https://git-lfs.com/). The patterns are in `.gitattributes`. In the repository, these files are ~130-byte pointers, and the real files live on GitHub's LFS server.

- **Setup.** Run `git lfs install` once per machine. Clones and pulls then fetch the real files automatically. If a checkout shows pointer text instead of images, run `git lfs pull`.
- **Adding files.** Nothing special: `git add` stores anything matching `.gitattributes` in LFS. To track a new file type, run `git lfs track "*.ext"` and commit `.gitattributes`, then run `git add --renormalize .` to convert files already committed. `git lfs ls-files` lists everything stored in LFS.
- **Cloudflare Pages** fetches LFS files when it clones the repository. This isn't documented by Cloudflare, but the history shows it: the first commit had 214 MB and 234 MB videos in LFS, and they had to move to R2 because Pages pulled them and rejected them as over 25 MB. The `check_lfs.py` step in the build command is the safety net if that ever changes.
- **Quota.** GitHub's free plan includes 10 GiB of LFS storage and 10 GiB of LFS bandwidth a month, and every Pages build downloads all LFS files (about 85 MB as of October 2026, so roughly 120 builds a month before bandwidth runs out). Keep large videos on R2.
- **History.** Files committed before LFS was enabled on October 17, 2026 are still regular Git objects in older commits. Only `git lfs migrate import --everything` with a force-push would move them.

## Gotchas

- **Quote front matter values that contain `: `** (`title: "Obico vs. OctoEverywhere: Which is best for you?"`). Unquoted, it's invalid YAML, and the whole build stops with "mapping values are not allowed in this context".
- **Templates use MiniJinja, not Jinja2.** Python string methods such as `.startswith()` don't exist. Use slices (`page.url[:6] == 'media/'`) and guard against undefined values (`page and page.url and ...`), because some pages, such as the 404 page, have no `page.url`.
- **Relative paths in raw HTML are rewritten** relative to the Markdown file for `src` and `href`, the same as Markdown links. Write them as you would a Markdown link (for example, `../assets/...` from `docs/media/x.md`). Other attributes, such as `<video poster>`, are not rewritten and must be relative to the page's final URL: from `docs/media/x.md`, which renders at `/media/x/`, use `../../assets/...`.
- **Links to other pages** can point at the `.md` file (`media/foo.md`) in Markdown, or at the rendered directory (`foo/`) in raw HTML. Both resolve.
- **Static HTML files in `docs/`** (such as `snapshot.html` archives) are copied as-is and are not indexed by search.
- **Every Media entry with `snapshot.html`** uses the same `.qd-archive-frame.qd-archive-frame--site` wrapper and `.qd-archive-frame__site` iframe, including articles, CrossTxT, and complete website archives. Give the iframe the unique name `qd-archive-<slug>`. The browser-style toolbar has three decorative window dots marked `aria-hidden="true"`, an address field showing the original URL, and an “Open separately” anchor styled as a button, linking to `snapshot.html` with `target="_blank"`, `rel="noopener"`, and visually hidden “in a new tab” text. Keep the address and button accessible; there is no “Start page” control. The iframe has a descriptive title, `loading="eager"`, `width="1280"`, `height="900"`, and `referrerpolicy="no-referrer"`. Keep PDF, screenshot, Wayback, and available ZIP actions below the frame; omit “Read the archived page.” See [media-archive.md](media-archive.md#archiving-a-web-page) for the page structure.
- **Archive iframe sandboxes have two configurations.** Static articles and CrossTxT use `allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-downloads` without scripts. The full 2011 and 2012 archives use `allow-scripts allow-popups allow-popups-to-escape-sandbox allow-downloads` without same-origin access so their audited local helpers run in an opaque origin. Never combine scripts and same-origin access. See [website-archives.md](website-archives.md#browsing-and-interactions).
- **Images get a lightbox automatically.** Add `class="no-lightbox"` to an `<img>` to opt out.
- **Videos.** `![type:video](url)` (the mkdocs-video plugin) embeds a 16:9 player. Use a raw `<video>` element when you need a poster or a non-16:9 aspect ratio, as the Media video pages do.
