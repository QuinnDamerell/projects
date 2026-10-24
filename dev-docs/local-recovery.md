# Local archive additions — October 21, 2026

The user approved adding the findings in [the discovery review](local-archive-review-2026-10-21.md), including a modern player for the recovered Flash animations. All source archives on D: remained read-only. Selected files were copied into this repository on C:; temporary staging lives in ignored `.cache/` because the encrypted archive volume can disappear when its vault closes.

## Published additions

- Crack the Whip: all three original WAVs, native audio controls and downloads, plus a [standalone recreation](whip-app.md) with the original artwork and button. Its browser motion adaptation keeps the original ±30° thresholds and strict alternation, measured as the phone's side-to-side tilt within its screen plane, as the app's diagrams show. SHA-256 confirms the sounds match the released XAP.
- Early Experiments: five original SWFs with an on-demand Ruffle player, original downloads, surviving captions, missing-film notes and the conflicting historical website dates.
- CrossTxT: the original notification MP3.
- Ninja Cam, PicGen, Gathr, Purdue Menu, Zune Playlist Shuffler and Purdue Bus: recovered screenshots/artwork, source-supported details and selected original downloads. The Zune JAR's filename and internal version disagree; the page says so.
- Baconit: selected early screenshots and a separate eight-image local v2.5 gallery, preserving the distinction from the existing store gallery.
- Both full homepage archives: 51 separately labeled supplement pages each, original larger photos, links from former gaps, provenance manifests and refreshed verified ZIPs. See [website-archives.md](website-archives.md#october-21-local-backup-restoration).
- Completeness notes: Ninja Cam identifies its unfinished Windows 8 port; Thinking of You, Liquid Physics and TxTBack acknowledge recovered unpublished source; Early Experiments links the full school-video index.

The `local-recovery-*-2026-10-21.json` contributor manifests record source paths, output paths, byte counts and hashes. They may include staging-only files; they are not published. Public archive supplements use relative provenance paths and omit backend PHP, credentials and account endpoints. No historical executable or Java applet was run.

## Intentionally unselected material

- The image bundled with the CrossTxT extension is a small marketing-homepage capture, not an additional view of the extension's UI. It was inspected and omitted as redundant; the original notification audio is published.
- The 96.6 MB Liquid Physics AVI has approximately the same 4:35 duration as the existing hosted demo. A comparison is still needed before treating it as a second recording. No duplicate was uploaded.
- The 295 MB Minecraft recording is about 3:47 long and has a 2017-11-09 metadata timestamp. Its filename and sampled gameplay frame do not establish its purpose or connection to a documented project, so it is not presented as QWorld footage or published as a new project artifact.
- Libarae, Nielsen Digital Diary and GPSTagger need personal/coursework context before receiving project pages. Third-party tutorials and libraries are not claimed as original projects.
- Editable TxTBack design documents and private-looking conversations/tester material were not selected. Recovered source is acknowledged without publishing entire code trees, credentials, or old server endpoints.

These were conditional leads in the discovery review, not verified missing public media. The selected restoration above is complete without assigning them unsupported stories or release dates.

## Flash player maintenance

`docs/javascripts/recovered-media.js` is registered in `zensical.toml`. It initializes with Zensical's instant navigation, releases detached players, pauses media when leaving the page or hiding the tab, and allows only one of the recovered audio/player sources to play at a time. Native audio controls and original-file downloads remain usable without JavaScript. Flash does not autoplay: the emulator loads after an explicit Play action. The still images are browser captures of these same SWFs rendered in Ruffle, not original archival images or recreated artwork.

The self-hosted runtime is **Ruffle 0.7.1**, from the official release:

- Package: `https://github.com/ruffle-rs/ruffle/releases/download/v0.7.1/ruffle-0.7.1-web-selfhosted.zip`
- Package SHA-256: `ef12edbee135d581a9cd523837d746da30a07a64dbf1cf472d2e472c656f4b5e`
- Runtime directory: `docs/assets/vendor/ruffle/0.7.1/`
- API documentation: <https://github.com/ruffle-rs/ruffle/wiki/Using-Ruffle>

The MIT and Apache license files ship with the runtime. Both WebAssembly variants are retained as supplied; each is below Cloudflare Pages' 25 MB limit and is tracked in LFS. No third-party CDN is contacted. The runtime directory is immutable-cacheable; upgrade into a new versioned directory and update the JS URL and `_headers` rule together. The `allowScriptAccess: false`, `allowNetworking: 'none'` and `openUrlMode: 'deny'` settings prevent the historical movies from making external requests or interacting with the surrounding page. Do not loosen those settings to repair an animation.

SWFs, WAVs, WASM, JARs and archived Java class files have LFS patterns. Run `tools/check_lfs.py`, a clean Zensical build, and the two strict archive validators after changes. Validate play/pause/restart, movie selection, sound playback, instant navigation and phone-width controls in a real browser. The archived sites retain their separate sandbox rules.

## Validation

All five original SWFs rendered successfully in the browser using the pinned runtime. Playback, pause/resume, restart and movie selection were exercised. Navigating to Ninja Cam removed the player; browser Back and Play successfully reinitialized it. All three whip WAVs and the CrossTxT MP3 played with valid browser-reported durations, and starting another recovered sound paused the first. The media controls were checked at 1280px and 390px in dark/light themes, with no horizontal overflow. The independent finish review returned **ship**, with no material findings at the recovered-media component scope; contributor documentation review required no changes.

The clean site build and LFS check passed. Both archive validators reported zero errors and warnings, and the ZIP packager verified the saved bytes below the size limit. An independent file audit verified all 488 added/changed binaries have LFS filters, checked all 653 public supplement manifest entries, resolved local links, and confirmed there are no oversized files or published secrets. `git diff --check` passes outside the complete-archive trees; reconstructed archive HTML retains some original trailing whitespace under its byte-preservation policy. Local QA screenshots are in ignored `.impeccable/review/`.

Archive browser QA verified both wrapper sandboxes, recovered full-size photo links, gallery navigation and 390px containment. Crazy Horse and Thinking of You rendered successfully. The Fireworks frameset was converted to static section links, and 14 sibling pages were wrapped to keep the provenance notice above their original positioned content. After the final build, the catalog, Home and Sparklers pages were checked in the in-app browser: all images loaded, the original Home link worked, and each content wrapper began at the notice's lower edge with no overlap. Final ZIP sizes are 11,256,076 bytes (2011) and 21,574,134 bytes (2012).

This is a local repository update. It does not publish a deployment or change the archive drive.
