# projects.quinn.space

Quinn Damerell's project archive, a static Zensical site. Read `dev-docs/` before making changes:

- `dev-docs/site.md`: how the site is built, local preview, deployment, and template gotchas
- `dev-docs/media-archive.md`: the Media tab and how to archive web pages and videos
- `dev-docs/tools.md`: `tools/snapshot.mjs` and `tools/upload_r2.py`
- `dev-docs/archive-backlog.md`: linked pages not archived yet

Before researching, auditing, or restoring references, check the explicit exclusions in `dev-docs/media-archive.md`. Do not rediscover, recommend, archive, or relink excluded sources from old inventories.

Ground rules:

- `docs/` is published content. Put notes and documentation for contributors in `dev-docs/`, never in `docs/`.
- Binary media is stored with Git LFS (patterns in `.gitattributes`). Add a pattern with `git lfs track` before committing a new binary file type, and never commit a single file over 25 MB, which Cloudflare Pages rejects; put large videos on R2 instead.
- Every external article, interview, podcast, or video linked from quinn.space (`../personal-site`) or from this site should be archived in the Media tab and hosted here. Archive it in the same change that adds the link, and keep `dev-docs/archive-backlog.md` current.
- Summaries on archive pages are written in our own words; the archived copy carries the original text.
- When you change how something works, update the matching note in `dev-docs/`.
