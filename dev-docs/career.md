# Career

The Career tab is a single page at `docs/career/index.md`, using `home.html` and the timeline styling shared with Projects and Media. Career gives each job or work area its own timeline block and shows its full year span. Career-specific styling is under `.qd-home.qd-career` in `docs/stylesheets/extra.css`. Header navigation is hand-written in `overrides/partials/header.html`; the mobile drawer uses `docs/.nav.yml`.

## Editing Achievements

The `View LinkedIn` button sits immediately below Achievements and above Work history. Its `.qd-career__links` navigation uses the shared `.qd-btn--ghost` style; Career's underlined text-link rules exclude `.qd-btn` links.

The compact Achievements block sits above Work history in `docs/career/index.md`. It has two columns on desktop and stacks on phones, with reduced `.5rem` side padding to give long patent titles more room. Edit the `.qd-career-highlights` section to add patents or awards.

Each patent is a `<details class="qd-career-patent" markdown="1">` inside `.qd-achievement-list`. The summary shows its title, grant number, and grant year. A nested `<span class="qd-career-patent__use">· Mixer.com</span>` inside `.qd-achievement-meta` places a short product name beside the year in accent-colored text, visible even while collapsed. Longer names wrap naturally. Expanding the patent reveals its description, full grant date, and record link; do not duplicate the product note there. Keep all four patents here as the single source of content.

Patent summaries and expanded paragraphs have no left margin, keeping the disclosure marker, metadata, and description aligned with the Patents heading.

For an award, copy a list item in `.qd-achievement-list--awards`: an `h4` with a source link, a `.qd-achievement-meta` paragraph for the competition and known year, and a short paragraph identifying the project or team. Use existing local archive links. Do not infer the year of Gathr's ACM Google win: the surviving record only establishes it was documented by February 2012.

## Editing the timeline

Give each job or work area its own `.qd-year` block, even when another entry has the same dates or employer. The `.qd-year__label` shows its full start–end year span, such as `2023–2025` or `2026–present`, at `1.2rem`; use one year for a role that began and ended in the same year. Keep the detailed month dates in `.qd-career-job__meta`. Purdue, East Noble Cole Auditorium, and Miss Indiana each have their own block and span. Education remains explicitly labeled rather than presented as employment. All jobs remain visible. Native `<details>` elements let readers expand longer lists of achievements without leaving the page.

The former Microsoft employment block is now eight editable work-area starters approved by Quinn: Windows Mixed Reality / HoloLens / Holoportation, Xbox xCloud, Mixer, Xbox Game Bar, Xbox in-home streaming, Xbox Streaming App for Oculus, Xbox Arcadia, and Internet Explorer on Windows Phone. Each has its own `h3`, with Microsoft identified in its metadata. The starters do not establish exact team boundaries or chronology. Their rail labels say `Dates to add` until Quinn supplies the individual spans. An HTML comment in the page preserves the overall August 2012–January 2023 employment period and asks editors to confirm team dates and boundaries; it does not appear on the published page.

The Mixer block now links to the [archived August 4, 2017 Outerhaven article](../docs/media/outerhaven-mixer-obs-2017.md), which names Quinn as the developer announcing FTL support in official OBS. The archive also links to the [primary release record](https://github.com/mixer/obs-studio-ftl/releases/tag/v1.0.0), published by `QuinnDamerell-MS`. This supports the announcement and named involvement, not sole authorship of OBS or FTL. The article describes an early alpha; the release description was subsequently updated. Neither source establishes the full Mixer team date range, so its `Dates to add` label remains.

Once dates are known, update both the rail label and the detailed metadata, then arrange entries in descending order of their start dates. Do not reuse the three LinkedIn promotion windows as team spans: those describe job titles held during the overall Microsoft employment period, not the duration of each team assignment. The initial research table below is retained as a source record.

Each job has a stable, unique heading ID for direct links. Write paragraphs, lists, and links inside `.qd-career-job__body` using Markdown. The `md_in_html` extension is enabled in `zensical.toml`; keep `markdown="1"` on the surrounding containers, articles, and body, and use `markdown="block"` on list items, or nested Markdown will remain unparsed. Keep HTML tags flush left: indenting them by four spaces creates a code block. Leave a blank line before and after Markdown content. Do not use `.qd-entry` for career entries: its link styles assume an entire row is a single link.

To add a job or work area, copy this entire block, change the span and content, and use a unique ID. Keep one job per `.qd-year` so its label always belongs to that job.

```html
<div class="qd-year" markdown="1">
<div class="qd-year__label"><span>2027–present</span></div>
<ul class="qd-year__list" markdown="1">
<li class="qd-career-entry" markdown="block">
<article class="qd-career-job" aria-labelledby="employer-name" markdown="1">
<header class="qd-career-job__header">
<h3 id="employer-name">Employer or team name</h3>
<p class="qd-career-job__role">Job title</p>
<p class="qd-career-job__meta">Month 2027–present · Company, if needed · Location</p>
</header>
<div class="qd-career-job__body" markdown="1">

A short description of the work, in first person.

- A project or achievement, with useful context.
- Another highlight, with a link when there is a public source.

</div>
</article>
</li>
</ul>
</div>
```

Work history uses `h2`; each job or work area uses `h3`. Optional subroles use `h4`. Add longer achievements inside a job body using this pattern. Use `h4` beneath a job, or `h5` if nesting achievements beneath a subrole. Patents are collected in the top Achievements block instead.

```html
<details class="qd-career-achievements" id="employer-achievements" markdown="1">
<summary>Selected achievements</summary>

#### Achievement title

Describe the contribution and its result. Include only metrics that can be supported.

- Supporting detail or related milestone.
- [Public source](https://example.com/).

</details>
```

If a job needs separate promotion details, optionally add a `<section class="qd-career-role" aria-labelledby="unique-role-id" markdown="1">` inside its body, with an `h4`, a `.qd-career-job__meta` paragraph, and Markdown content. Keep patents attributed as **co-inventor** work and distinguish filing dates from grant dates. The four current patents are attributed to Quinn's time at Microsoft. Product-use notes were supplied by Quinn after the initial research; they are not inferred from the grant records.

When adding an external article, interview, podcast, or video, follow `media-archive.md` and link its local archive. LinkedIn profile and patent-record links are reference records rather than media articles and do not need archive entries.

## Sources and initial facts

Awards added to Achievements are supported by existing local records:

- **People's Choice, Big App on Campus (2012):** Baconit; `docs/media/windows-phone-blog-big-app-on-campus-2012.md` and the archived March 22, 2012 Windows Phone Blog announcement.
- **App of the Year, Community App Awards (2012):** Baconit; `docs/media/windows-blog-baconit-2012.md` and the November 2012 product page linked from `docs/baconit.md`.
- **First place, ACM Google coding competition:** Gathr, built with Tyler Reid and Bryan Ehrlich; `docs/gathr.md` and the February 2012 portfolio. Competition year unknown.
- **Top-five team, State Farm coding competition (2010):** with Bryan Ehrlich; `docs/assets/media/quinndamerell-homepage-2012/site/_captures/20120213160132-X47AU36R.html`, linked through the full 2012 website archive.

The initial page was populated on **October 18, 2026** from Quinn's authenticated [LinkedIn profile](https://www.linkedin.com/in/quinndamerell/) and [experience page](https://www.linkedin.com/in/quinndamerell/details/experience/), plus the patent records below. Dates and responsibilities were transcribed from those pages; public descriptions are concise paraphrases. Do not infer additional duties or achievements from a title alone. LinkedIn's current-role status is a snapshot; update it when a role changes.

| Entry | Verified dates | Source details used |
| --- | --- | --- |
| Mojang Studios — Senior Software Engineer | March 2026–present | LinkedIn: Redmond; networking and game engine for Minecraft Bedrock. |
| Turn 10 Studios — Senior Software Engineer | January 2023–July 2025 | LinkedIn: Redmond; lead network engineer for ForzaTech, used by Forza Motorsport, Forza Horizon, and Fable. No claim about release status. |
| Microsoft — employment group | August 2012–January 2023 | LinkedIn groups the following three roles. |
| Microsoft — Senior Software Engineer | September 2018–January 2023 | LinkedIn: Greater Seattle; Windows Mixed Reality, HoloLens, and Holoportation streaming; Xbox xCloud low-latency streaming; Xbox Mixer FTL video. |
| Microsoft — Software Engineer 2 | September 2014–September 2018 | LinkedIn: Redmond; Xbox Mixer FTL video; Xbox Game Bar on Windows 10; Xbox Windows 10 in-home streaming. |
| Microsoft — Software Developer | August 2012–September 2014 | LinkedIn: Redmond; streaming for the former Xbox Arcadia team; Internet Explorer input/rendering on Windows Phone 8/8.1 (Apollo/Blue). |
| Microsoft Corporation — Software Developer Internship | May–August 2011 | LinkedIn: developer on Windows Phone 7.5 (Mango). Public employer name is shortened to Microsoft. |
| Raytheon — Software Engineer Internship | May–August 2010 | LinkedIn: developed for Android, Windows, and Linux. |
| Purdue University — Undergraduate Computer Science | August 2008–May 2012 | LinkedIn: education, not employment; no degree credential inferred. |
| J.O. Mory — Assistant Network Administrator Internship | February–June 2008 | LinkedIn: title and dates only; no responsibilities invented. |
| East Noble Cole Auditorium — Lead Technical Director | April 2006–January 2010 | LinkedIn: led a five-person team handling lighting and sound for productions. |
| Miss Indiana Scholarship Pageant — Head Lighting Tech | April 2006–January 2010 | LinkedIn: designed, managed, and operated production lighting. |

Quinn is listed as a co-inventor on all four grants. The utility patents' original assignee is Microsoft Technology Licensing LLC; the design patent's original assignee is Microsoft Corporation.

| Patent record | Filed | Granted | Description used |
| --- | --- | --- | --- |
| [US10034036B2 — Media synchronization for real-time streaming](https://patents.google.com/patent/US10034036B2/en) | October 9, 2015 | July 24, 2018 | Adjusting audio playback for changing video delay. |
| [USD826965S1 — Display screen with graphical user interface](https://patents.google.com/patent/USD826965S1/en) | November 21, 2016 | August 28, 2018 | Design patent for a display-screen graphical user interface. |
| [US10200768B2 — Low-latency mobile device audiovisual streaming](https://patents.google.com/patent/US10200768B2/en) | June 28, 2017 | February 5, 2019 | Combining app, microphone, and camera media for live mobile streaming. |
| [US11388464B2 — Increasing video bit rates while maintaining video quality](https://patents.google.com/patent/US11388464B2/en) | September 25, 2018 | July 12, 2022 | Testing available bandwidth to raise video quality with low latency. |
