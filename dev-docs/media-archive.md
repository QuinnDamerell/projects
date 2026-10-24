# The Media archive

The Media archive (`docs/media/`) keeps copies of press coverage, interviews, podcasts, talks, and videos about Quinn's work, so they stay available after the original sites change or disappear. Several already have: All About Bambu deleted its 2025 interview within a year, and every 2012 article was gone by the time the archive started. Its public index is a curated selection, not the complete inventory.

## Policy

### Explicit content exclusions

On October 18, 2026, Quinn requested removing all references to the OctoPrint usage-statistics incidents, explaining that OctoEverywhere was not responsible. Treat this as a standing editorial exclusion for both project sites: do not rediscover, recommend, archive, or re-add these stories, related commentary, or their local archive pages unless Quinn explicitly reverses this instruction. Old audits and capture logs are historical evidence, not a backlog for restoring excluded links.

The excluded URLs are listed as plain text for matching, not as recommendations:

- `https://octoprint.org/blog/2024/06/28/stats-manipulation/`
- `https://octoprint.org/blog/2024/07/04/more-stats-manipulation/`
- `https://all3dp.com/4/octoprint-usage-stats-manipulated-by-sponsor/`

Match redirects, Wayback versions, fragments, and trailing-slash variants too. Removed archive slugs are `octoprint-statistics-incident-2024`, `octoprint-statistics-follow-up-2024`, and `all3dp-octoprint-statistics-2024`. Their wrappers and assets are outside the published source tree. This exclusion overrides the general requirement below to archive external articles and reduces the current web shortlist from 48 to 46 source groups.

### Preservation scope

**October 21, 2026 approved curation:** Quinn approved the [18-piece selection review](media-index-review-2026-10-21.md): keep nine previously listed stories, promote seven existing archives, and add the Notts IoT talk and The Outerhaven's Mixer/OBS article. The 18 main stories run newest first. The two complete personal-site archives appear separately under **Time capsules**, with 2012 before 2011. The CrossTxT homepage remains a project reference. Preserve every other archive page, asset, and project citation; removing an index row is not deleting an archive. Optional additions from the review were not selected.

Keep `docs/.nav.yml` aligned with that selection: the Media group contains its index, the same 18 stories, and a nested Time capsules group with the two personal sites. Related article/video pairs stay linked through the selected article, and the PhoneArena prank article links to its supporting Reddit photo and discussion. The new Notts wrapper includes both the full recording and its event announcement, with `#talk` and `#event-announcement` anchors. Check the latest capture/upload state in [archive-backlog.md](archive-backlog.md) before publishing new media.

**October 18, 2026 preservation pass (historical scope):** Quinn initially selected 48 important web source groups, now 46 after the explicit exclusions above, including historical Reddit discussions, after excluding assets, social profiles, own sites, GitHub, routine references, and YouTube. New copies from this pass were initially unlisted reference archives, linked from project citations without being added to the index or sidebar. The October 21 selection promotes only the approved subset. Related translations, follow-ups, comments, and research PDFs stay with their source group. YouTube was reviewed separately.

**October 18 video follow-up (historical scope):** Quinn selected ranks 1–17 from the video priority report. These were downloaded to a Desktop handoff folder with stable filenames matching their R2 object names, then uploaded by Quinn. Their individual archive pages and project citations, including timestamp references, were initially unlisted. The October 21 selection promotes the Domótica Fácil Homeway video; the remaining videos stay project references. The pages target the existing `projects-storage.quinn.space` bucket domain. Local download verification does not establish that R2 has the objects: see [the upload handoff](video-r2-upload-2026-10-18.md) for the dated verification record.

- **Archive every external article, interview, podcast, or video linked from quinn.space (`../personal-site/site/index.html`) or from this site's pages.** When you add a press link anywhere, archive it in the same change.
- **Host the copy here.** The Wayback Machine is the backup and the proof of provenance, not the primary copy: items can be removed on a rights holder's request, and the Internet Archive has outages (several weeks in October 2024; it also returned "Temporarily Offline" pages during this archive's own captures).
- **Link to the archive, not the original.** Press links on project pages and on quinn.space point straight at the Media page, with no "(archived copy)" note: Markdown links like `[Title](media/<slug>.md)` on this site, and `https://projects.quinn.space/media/<slug>/` on quinn.space. The Media page links on to the original. The exception is the "YouTube Source" credit under videos that are already embedded from R2, which stays on YouTube.
- **Not covered by the policy:** Quinn's own live services (octoeverywhere.com, homeway.io, plot.game), GitHub repositories, social profiles, and media already hosted on R2.
- **To find what's missing,** extract every external link from both sites (`href`, `src`, Markdown links, bare URLs), drop the categories above, and compare the rest with `docs/media/`. Record the result in [archive-backlog.md](archive-backlog.md).

## Structure

| Path | Contents |
| --- | --- |
| `docs/media/index.md` | The selected 18 stories in a year timeline reusing `qd-year`/`qd-entry` markup, followed by two personal-site Time capsules. Newest year first, and newest story first within a year. |
| `docs/media/<slug>.md` | One page per archived item |
| `docs/assets/media/<slug>/` | That item's files: `snapshot.png`, `snapshot.pdf`, `snapshot.html`, `images/`, `snapshot.json`, and `poster.jpg` for videos |

Slugs are `<outlet>-<topic>-<year>` for web pages (`winsource-baconit-2012`) and `youtube-<channel>-<topic>-<year>` for videos (`youtube-next-layer-octoeverywhere-2023`).

### Index category filters

The Media index has four toggle buttons, all enabled on a fresh page load. Every listed `.qd-entry` must have exactly one `data-media-category` value:

| Value | Button | Includes |
| --- | --- | --- |
| `interviews` | Interviews & talks | Written interviews, developer Q&As, interview podcasts or videos, and Quinn's technical talks. Personal interview content takes precedence over format, so Next Layer, Hanselminutes, and Notts IoT belong here. |
| `videos` | Videos | Product demonstrations, walkthroughs, and video reviews that are not interviews. |
| `articles` | Articles & posts | Selected press coverage, award announcements, and creator-authored stories such as Glow. |
| `websites` | Time capsules | The two complete personal-site archives, grouped below the main timeline. The data key remains `websites`. |

Keep the existing kind badges (Video, Podcast, Article, etc.) as format metadata. The category is a separate, broader grouping; do not infer it from the badge in JavaScript. Categorize only listed entries, without adding unlisted reference archives to the index.

`docs/javascripts/media-filters.js`, loaded through `extra_javascript` in `zensical.toml`, hides entries in disabled categories, any years left empty, and the Time capsules group when its category is disabled. It reports stories and time capsules separately, offers **Show all media** when nothing is selected, and reinitializes through Zensical's `document$` stream after instant navigation. Selections survive instant navigation within the page session; a full reload enables everything again. Without JavaScript, the controls stay hidden and all 18 stories and two time capsules remain readable.

## Archiving a web page

1. **Find a source.** If the page is live, use its URL. If it's gone, or broken (for example, missing images), find a capture in the Wayback Machine. The CDX API is the reliable way to list captures:

    ```sh
    curl "https://web.archive.org/cdx/search/cdx?url=<url-without-scheme>&output=txt&fl=timestamp,original,statuscode&filter=statuscode:200&limit=10"
    ```

    The `archive.org/wayback/available` API often returns empty results even for archived pages, so don't trust a negative answer from it. Old blogs often moved, so also try the earlier address (for example, `windowsteamblog.com/...aspx` before `blogs.windows.com/...`). Prefer the capture closest to the publication date.

2. **Capture it** with [`tools/snapshot.mjs`](tools.md#snapshotmjs), passing a live URL or a Wayback link:

    ```sh
    node tools/snapshot.mjs https://web.archive.org/web/20120413180410/http://winsource.com/2012/04/12/winsource-interview-quinn-damerell-of-baconit/ winsource-baconit-2012
    ```

    Check the screenshot. "Broken image" lines in the output list images that didn't load. Small icons that were never archived are fine; missing article photos are worth chasing with `--image`. For example, the Reddit thread's photo was restored from its original Imgur upload with `--image "external-preview.redd.it/<id>=https://i.imgur.com/<id>.jpg"`.

    - **News sites with endless feeds and ads.** Strip the clutter with `--remove <selector>`, repeated as needed, and say so in the caption ("with ads and the site's news feed left out"). For Windows Central, these selectors keep just the article:

        ```sh
        --remove ".wcp-item-content > section:not(.content-wrapper)" --remove ".ad-unit" --remove ".dfp-leaderboard-container" --remove "[id^=slice-container-newsletterForm]" --remove "#upnext-ribbon" --remove ".bordeaux-generated-container" --remove "[class*=bordeaux-skin]" --remove ".infinite-container" --remove "#pressboard-ad-sponsorship-msg"
        ```

        OnMSFT needs `--remove "[id^=AdThrive_]" --remove ".adthrive-sticky-outstream"`. To find selectors for a new site, look at the screenshot, then inspect the page at 1280 px wide: ad containers often hold the page height open (Windows Central's sticky sidebar ads made a 3,700 px article 17,000 px tall).
    - **Sites that show a bot check** ("Prove your humanity", "Confirm you are human"). Reddit and the OctoEverywhere blog both do this. Don't try to get past it; capture the latest good Wayback copy instead, and say so in the summary.

3. **Write the page** at `docs/media/<slug>.md`, copying an existing one such as `winsource-baconit-2012.md`. Each page has:
    - front matter with `title`, `description`, and `hide: [navigation, toc]`
    - an `# H1` with the article's title
    - one paragraph summarizing the piece **in your own words**. Don't copy the article's text; the archived copy carries it. Link the project page. For copies from the Wayback Machine, end with "The original ... is offline, so this copy comes from the Internet Archive."
    - a `<dl class="qd-archive-meta">` with Outlet, Published, Archived ("<date>, by the Internet Archive" for Wayback copies, or the capture date), and Original (a "View the live page" link, or "Offline")
    - the shared `<figure class="qd-archive-frame qd-archive-frame--site">` browser frame displaying the local `snapshot.html`, with a caption saying when and where the copy came from
    - `<div class="qd-archive-actions">` **below the frame**, with PDF, screenshot, Wayback Machine (the exact capture link, or `https://web.archive.org/web/*/<url>` for live pages), and ZIP download when available. Omit the redundant "Read the archived page" action; the copy is already visible in the frame.

    All Media entries with `snapshot.html` use this same display, including articles, the CrossTxT homepage, and complete website archives. The browser-style toolbar has three decorative window dots marked `aria-hidden="true"`, an address field showing the original URL, and an "Open separately" anchor styled as a button. That anchor links to `snapshot.html` with `target="_blank"`, `rel="noopener"`, and `<span class="qd-visually-hidden"> in a new tab</span>` after its visible label. Hide only the decorative dots from assistive technology, not the toolbar or its button. There is no "Start page" control.

    The iframe uses `class="qd-archive-frame__site"`, `name="qd-archive-<slug>"`, a descriptive `title`, `loading="eager"`, `width="1280"`, `height="900"`, and `referrerpolicy="no-referrer"`. Original fixed-width layouts scroll inside the frame on narrow screens. Static article and CrossTxT snapshots use `sandbox="allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-downloads"` **without scripts**; CrossTxT's CSS-only feature tabs still work. The full 2011 and 2012 sites instead use `sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-downloads"` **without same-origin access** for their audited local helpers. See [website-archives.md](website-archives.md#browsing-and-interactions).

4. **List it** in `docs/media/index.md` under its year unless the requested collection is unlisted (as in the October 18 preservation pass). Include name, kind (Article, Interview, Q&A, Podcast, Award, Video, Blog post, Community, Website, or Store listing), outlet, and a one-line description. Assign exactly one `data-media-category` from the [index category filters](#index-category-filters). If a podcast has a video version, the video goes on the podcast's page rather than a page of its own (see `hanselminutes-octoeverywhere-2022.md`).

5. **Link it** from the related project page's press section, and from quinn.space if it's listed there, as a direct link (see the policy above).
6. **Update [archive-backlog.md](archive-backlog.md).**

## Complete personal website archives

The user expanded the original one-off request: old personal websites should be preserved as complete browsable local sites and embedded in their Media pages. The January 16, 2011 and April 16, 2012 QuinnDamerell.com captures each have their own asset subtree and named iframe. See [website-archives.md](website-archives.md) for the workflow, provenance rules, interaction support, and validation. Keep each requested snapshot separate; don't silently send navigation to a different era's mirror.

Ordinary articles and other individual pages still use `tools/snapshot.mjs`. Do not run that tool against a full-site archive directory: it recreates the directory and produces a single-page snapshot. The 2012 archive also retains a separate `history/` source collection used for [the project-history review](wayback-homepage-review.md).

## Archiving a YouTube video

1. **Get the video file.** Quinn downloads these locally (WebM is fine). Probe it for the dimensions and length: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height:format=duration -of compact <file>`.
2. **Upload it to R2.** Files up to 300 MB can go through the dashboard; larger ones need `python tools/upload_r2.py <file> <api-token>`. The object keeps the file name, and the public URL is `https://projects-storage.quinn.space/<url-encoded name>`. Spaces and other special characters must be percent-encoded in the page.
3. **Get the details** from the YouTube watch page (`ownerChannelName`, `uploadDate`, `lengthSeconds`, `shortDescription` in its embedded JSON). Note that the channel name doesn't always match the show's name.
4. **Make a poster** at `docs/assets/media/<slug>/poster.jpg`. Use `https://i.ytimg.com/vi/<id>/maxresdefault.jpg` for 16:9 videos, or a frame from the file when the aspect ratio differs: `ffmpeg -ss 90 -i <file> -frames:v 1 -q:v 3 poster.jpg`.
5. **Write the page,** copying `youtube-next-layer-octoeverywhere-2023.md` (or `youtube-wmpoweruser-baconit-review-2012.md` for an MP4 already on R2). It uses the same header as web pages (H1, summary, meta with Channel, Published, Length, and Original), action buttons (Watch on YouTube, Download video, and links to related archive pages), and then a `<figure class="qd-archive-video">` with a `<video controls preload="metadata" playsinline>` element. Give it the file's real `width` and `height` so the player reserves the right shape, a `poster` written as `../../assets/...` (posters aren't rewritten; see [site.md](site.md#gotchas)), a `<source>` with the right `type` (`video/webm` or `video/mp4`), and a fallback link to YouTube.
6. **List and link it** as for web pages, with the kind set to Video.

## Verifying

Run the preview (see [site.md](site.md#local-preview)) and check:

- the Media page and the new page render, in both color schemes and at phone width
- `snapshot.html`, `snapshot.pdf`, and `snapshot.png` return 200, and `snapshot.html` renders like the original
- the embedded copy scrolls without widening the Media page, the browser-style toolbar shows the original address, and "Open separately" opens the copy in a new tab
- for videos, the player loads (`readyState` 4) and plays
