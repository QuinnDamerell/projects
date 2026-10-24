# Original website recovery and historical review

Requested October 17, 2026: preserve the full linked site rooted at `https://web.archive.org/web/20120416170518/http://www.quinndamerell.com/index.html`, then compare archived homepage versions for missing project details. This began as a one-off exception. The user subsequently requested complete embedded archives for both the January 2011 and April 2012 sites; [website-archives.md](website-archives.md) describes the current workflow. Counts and validation below record the initial recovery pass.

## Published files

- Media page: `docs/media/quinndamerell-homepage-2012.md`.
- Site archive: `docs/assets/media/quinndamerell-homepage-2012/`.
- The root `snapshot.html` opens the preserved homepage; `site/` holds local pages/assets. `archive-index.html` and `manifest.json` identify exact replay provenance, supplemental captures, and gaps. Raw source files are inert text.
- `history/` is a separate source collection for other years. It preserves readable extracted text and original HTML as `.source.html.txt`, not a whole-site mirror for every year. Its index, CDX inventory, and manifest document coverage and failed downloads. Project citations now open the matching full-layout page in the 2011 or 2012 archive. Separately dated revisions needed by those citations live under `site/_captures/`, using the original HTML and the archive's recovered assets; the history readers remain available as research records.

The homepage HTML is the exact requested 2012 capture. Linked resources are independently captured by Wayback; pages only recovered in later years are labeled as supplements. Some homepage tile artwork is only available from later captures, so the screenshot and PDF are reconstructions using those assets. Do not describe the entire set as a simultaneous April 2012 snapshot. External sites, databases, working contact forms, Java applet execution, and server code are outside a static Wayback copy.

## Review coverage

The main-domain CDX query includes www/non-www and HTTP/HTTPS variants. It returned 116 rows after adjacent-digest collapse, representing 98 distinct HTML digests across the site. All 20 homepage digests were retrieved; some are substantively identical. The history collection preserves 46 source pages and lists 52 linked-page versions that could not be retrieved during this review; many repeat pages recovered at another date. The distinct-HTML inventory spans 2008–2024, with uncollapsed root capture records extending into 2025; the latest distinct homepage revision is from 2022. Subdomains and revisions never captured by Wayback are outside this inventory.

## Content recovered

- New pages for Gathr, Ninja Cam, Zune Playlist Shuffler, and PicGen; grouped early websites, Java applets, and school projects in Early Experiments.
- Gathr: Android social-event coordinator, collaborators Tyler Reid and Bryan Ehrlich, three-month development, first place in an ACM Google competition. Supplemental text added during the shared-workspace review cites Bryan's portfolio for map-based meetup invitations and location sharing; that source was checked. No exact competition or creation year asserted.
- Ninja Cam: the original site supplies the title and Windows Phone Marketplace identifier, although its product page is a placeholder. Its misleading HTML title says Next Bus, but its visible heading and app link identify Ninja Cam. Supplemental research recovered the March 16, 2012 Marketplace listing: taking still photos by tapping a simulated webpage, version 1.5.0.0, Windows Phone 7.5 compatibility, and a February 29 release field. Those details were checked against the listing; the release field is not asserted to be the original launch date.
- Zune Playlist Shuffler: Java utility, playlist selection and directory search, version 1.3, and advice to close Zune before editing. Supplemental research added Quinn's April 28, 2010 Reddit announcement, checked against the live thread, which establishes public availability before the June website capture. April is a documented-by date, not an inferred creation date.
- PicGen: May 2009 homepage introduction, Java and exhaustive black/white pixel-combination concept in the 2011 project index. No claim that enumeration completed.
- CrossTxT: sale corrected from 2012 to the end of 2011, named buyer Spider Web Design, and continued development after sale. The existing $5,000 and Chicago recollections were retained.
- Liquid Physics: Grant Kot simulation credit, initial Android port by XDADevelopers member jgittins, multi-touch, and more than 35,000 downloads reported by February 2012.
- Purdue Food Court Menu: first Android app and learning project. PurdueBus: route maps, live arrivals, and timetable fallback.
- TxTBack: first major public project, Java server in the dorm. Reddit Time Machine: twice-daily capture cadence.
- BaconSync: send-to-phone, synchronization across devices, and separate Chrome (Quinn), Firefox (Pradeek J.), and Opera (Ivan Kiselovs) credits.
- Baconit: People's Choice in the free-app division, three voting rounds, roughly three months of development before entry, and a 2012 Community App Awards App of the Year claim attributed to the original product page.
- Baconit versions: the May 2012 product page shows 2.0 while describing Mango support. Corrected the former 2.0/Windows Phone 8 association and added the 2.5/Windows Phone 8 milestone from the already-archived November 2012 walkthrough. Removed the unsupported shared-Windows-8-codebase assertion.

## Dates and uncertainty

Do not turn a capture date into a creation date. The new pages say "Documented by"; they appear together beneath the existing chronology on the homepage. Thinking of You's existing 2011 creation date can coexist with its 2012 launch. Reddit Time Machine's existing creation date was not inferred anew from its 2010 announcement.

Crack the Whip's former 2014 creation date conflicts with the already-linked June 5, 2012 discussion in which Quinn describes the published app. It is now qualified as "By June 2012," with an availability note on the timeline, rather than assigned an exact release date. That source remains in the previously authorized external-reference backlog.

The two early Atom records differ: `projects.php` labels an Atom Project 2006, while `websites.php` gives an Atom Model in Flash date of October 16, 2005. Both descriptions are retained, without assuming they are the same version.

The former Baconit paragraph described a second-place finish and included an anecdote about an XNA-demo entry. The contemporary portfolio identifies a People's Choice award instead. The award paragraph now uses that directly supported description; this review did not independently establish the anecdote about the other entry.

## Initial archive and validation

The requested-site recovery contains 16 page variants, including five later supplements, and 116 saved resources. The inventory records 29 resources that could not be recovered or were excluded because their archived endpoint returned the wrong content. No resources remain unattempted. Next Bus and TxTBack have explicit local gap notices; their retrieval attempts failed and neither appears in the saved main-domain capture inventory. This does not establish that no capture exists anywhere in Wayback.

`website.zip` is the downloadable copy: 334 files, 14,692,932 bytes. It includes the raw sources, local site, history collection, screenshot, PDF, inventories, and a README. Extract it and open `snapshot.html`. The ZIP excludes itself. If any archive content changes, recreate the ZIP before delivery.

Final checks passed: a clean Zensical build in a separate temporary copy, the Git LFS pointer check, ZIP integrity and byte-for-byte contents, all 116 raw hashes, served hashes, and case-sensitive local links. The static HTML audit checked 67 pages with no missing targets, unresolved fragments, active scripts/forms, or remote resource loads. The Media index and entry were visually checked in dark/light themes and at phone width; the homepage screenshot and one-page PDF were inspected. HTML, PDF, PNG, ZIP, and history index returned HTTP 200 in the local preview. All new files are below the 25 MB hosting limit; ZIP and font binaries match Git LFS patterns.
