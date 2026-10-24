# Developer notes

Notes for people and agents working on this repository: how the site is built, how the Media archive works, and how to use the tools in `tools/`. Keep these notes current when you change how something works.

These notes live in `dev-docs/` rather than `docs/` because everything in `docs/` is published to [projects.quinn.space](https://projects.quinn.space).

| File | What it covers |
| --- | --- |
| [site.md](site.md) | The Zensical site: layout, templates, styles, local preview, deployment, and gotchas |
| [career.md](career.md) | Editing the Career timeline, adding job details and nested achievements, and the sources for the initial work history and patents |
| [media-archive.md](media-archive.md) | The Media tab: the archiving policy, page structure, and step-by-step recipes for archiving web pages and videos |
| [tools.md](tools.md) | Page snapshots, website archive validation and packaging, and large file uploads to R2 |
| [archive-backlog.md](archive-backlog.md) | Linked pages that aren't archived yet |
| [website-archives.md](website-archives.md) | Complete personal website archives, embedded browsing, provenance, and validation |
| [wayback-homepage-review.md](wayback-homepage-review.md) | The initial original-website recovery, historical sources, and project details recovered |

## Related repositories

- **projects.quinn.space** is this repository.
- **quinn.space**, the personal site, is `QuinnDamerell/personal-site` (locally `../personal-site`). It's a single `site/index.html`, and its press links count toward the archiving policy.
