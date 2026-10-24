
# Quinn Damerell's Project Archive

A collection of projects, experiments, and stories, published at [projects.quinn.space](https://projects.quinn.space).

Built with [Zensical](https://zensical.org/) and its modern theme. Site settings live in `zensical.toml`, project pages in `docs/`, and navigation order in `docs/.nav.yml`.

## Local development

Use Python 3.11 or newer. Create a virtual environment and install the pinned dependencies:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\zensical serve
```

On macOS or Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/zensical serve
```

Open [localhost:8000](http://localhost:8000). The preview reloads when Markdown, styles, or configuration changes.

Alternatively, open the repository in VS Code with Docker running and choose **Reopen in Container**. The dev container installs dependencies and starts the live preview on port **8000**, which VS Code forwards and opens in your browser. It polls for file changes so saves reliably rebuild and refresh the page on Windows bind mounts. Reconnecting reuses the running preview. See [the preview guide](dev-docs/site.md#vs-code-dev-container-recommended-on-windows) for the manual start command and troubleshooting. A separate static server on port 8001 will not update on save.

## Media archive

The Media tab (`docs/media/`) keeps archived copies of press coverage and videos, so they survive the original pages going offline. `tools/snapshot.mjs` captures web pages (live, or from the Wayback Machine), and `tools/upload_r2.py` uploads large videos to R2. See [`dev-docs/`](dev-docs/README.md) for the archiving policy, step-by-step recipes, and tool documentation.

## Production build

Run `zensical build --clean` from an activated virtual environment, or `.venv\Scripts\zensical build --clean` on Windows. The generated static website is written to `site/`, which can be published by the existing hosting provider.

For the existing Cloudflare Pages project, set the build command to `python tools/check_lfs.py && pip install -r requirements.txt && zensical build --clean`, keep the output directory as `site`, and use Python 3.11 or newer. These hosting dashboard settings are separate from the repository and must be updated when deploying this migration.

Images, PDFs, and other binary media are stored with Git LFS. Run `git lfs install` once before cloning, or `git lfs pull` if a checkout shows pointer text instead of images. `tools/check_lfs.py` stops the build if the real files are missing. See [`dev-docs/site.md`](dev-docs/site.md#git-lfs).

Zensical natively handles `.nav.yml` navigation, image lightboxes, video embeds, search, and HTML minification. These features require only the Zensical package in `requirements.txt`. Keep the pinned version when building locally and in deployment, since older releases do not support all of these features.

Custom styles are in `docs/stylesheets/extra.css`; template overrides and the existing Matomo analytics integration are in `overrides/`. Google Analytics and social links remain configured in `zensical.toml`.
