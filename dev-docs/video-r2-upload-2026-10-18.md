# Selected video upload handoff — October 18, 2026

Quinn selected ranks 1–17 from the video importance report. All 17 files are downloaded to `C:\Users\quinn\Desktop\YouTube-R2-Archive-2026-10-18\`, and Quinn has uploaded them to the existing R2 bucket. All 17 public objects passed verification on October 18, 2026. No site deployment was performed in this task.

The files total **2.28 GB (2.12 GiB)** and approximately **257 minutes**. They contain H.264 video and AAC audio in MP4, up to 1080p, with fast-start metadata. Every file was probed for audio/video streams and expected duration; samples from the beginning, middle and end decoded. These checks do not establish full playback or current R2 availability.

## Upload and activation

1. Upload only the 17 root-level .mp4 files into the root of the existing projects-storage R2 bucket.
2. Keep every filename exactly as written. Do not include the Desktop folder name as an R2 object prefix.
3. Serve the objects with Content-Type video/mp4. Archive pages already point at the public URL listed in each row.
4. Keep README.txt, upload-manifest.json, checksums.sha256 and _metadata locally; these are handoff records, not public video objects.
5. R2 playback and seeking are now verified for all 17 videos. After publishing the site changes, confirm the public archive pages load their embedded videos.

The Desktop folder includes a JSON manifest, SHA-256 checksums, sanitized source metadata and per-file verification evidence. Keep these as local provenance. The project pages now link to the individual video archives, including the two Homeway timestamp references. The Media index and sidebar were left unchanged. The Windows Central Xbox article wrapper links to its related video; the original captured HTML remains intact.

## Archive pages and exact R2 object keys

| Rank | Archive page | R2 object key | Size |
| --- | --- | --- | --- |
| 1 | [Made with Layers (Thomas Sanladerer)](../docs/media/youtube-thomas-sanladerer-octoprint-guide-2021.md) | `youtube-thomas-sanladerer-octoprint-guide-2021.mp4` | 204.6 MB |
| 2 | [Uncle Jessy](../docs/media/youtube-uncle-jessy-octoeverywhere-centauri-carbon-2025.md) | `youtube-uncle-jessy-octoeverywhere-centauri-carbon-2025.mp4` | 167.7 MB |
| 3 | [The Next Layer](../docs/media/youtube-next-layer-octoprint-plugins-2023.md) | `youtube-next-layer-octoprint-plugins-2023.mp4` | 97.6 MB |
| 4 | [The Next Layer](../docs/media/youtube-next-layer-octoeverywhere-remote-access-2022.md) | `youtube-next-layer-octoeverywhere-remote-access-2022.mp4` | 152.4 MB |
| 5 | [PrintsLeo3D](../docs/media/youtube-printsleo3d-octoeverywhere-klipper-2024.md) | `youtube-printsleo3d-octoeverywhere-klipper-2024.mp4` | 288.2 MB |
| 6 | [ModBot](../docs/media/youtube-modbot-octoeverywhere-2022.md) | `youtube-modbot-octoeverywhere-2022.mp4` | 123.3 MB |
| 7 | [Chris Riley](../docs/media/youtube-chris-riley-octoeverywhere-2021.md) | `youtube-chris-riley-octoeverywhere-2021.mp4` | 51.4 MB |
| 8 | [Home Assistant y Domótica Fácil](../docs/media/youtube-domotica-facil-homeway-comparison-2025.md) | `youtube-domotica-facil-homeway-comparison-2025.mp4` | 158.0 MB |
| 9 | [Windows Central](../docs/media/youtube-windows-central-baconit-xbox-one-2016.md) | `youtube-windows-central-baconit-xbox-one-2016.mp4` | 59.4 MB |
| 10 | [Figure Feedback](../docs/media/youtube-figure-feedback-octoeverywhere-2024.md) | `youtube-figure-feedback-octoeverywhere-2024.mp4` | 244.1 MB |
| 11 | [Chris Riley](../docs/media/youtube-chris-riley-octoeverywhere-klipper-2023.md) | `youtube-chris-riley-octoeverywhere-klipper-2023.mp4` | 50.0 MB |
| 12 | [Daniel Barczak](../docs/media/youtube-daniel-barczak-homeway-2025.md) | `youtube-daniel-barczak-homeway-2025.mp4` | 189.3 MB |
| 13 | [Crys' Livingroom Workbench](../docs/media/youtube-octoapp-octoeverywhere-2021.md) | `youtube-octoapp-octoeverywhere-2021.mp4` | 32.8 MB |
| 14 | [Chris Riley](../docs/media/youtube-chris-riley-octoeverywhere-revisit-2022.md) | `youtube-chris-riley-octoeverywhere-revisit-2022.mp4` | 39.9 MB |
| 15 | [This Smart House](../docs/media/youtube-this-smart-house-octoprint-plugins-2021.md) | `youtube-this-smart-house-octoprint-plugins-2021.mp4` | 217.9 MB |
| 16 | [Denie van Kleef](../docs/media/youtube-denie-van-kleef-homeway-comparison-2026.md) | `youtube-denie-van-kleef-homeway-comparison-2026.mp4` | 114.8 MB |
| 17 | [Stacking Layers](../docs/media/youtube-stacking-layers-octoeverywhere-2024.md) | `youtube-stacking-layers-octoeverywhere-2024.mp4` | 83.7 MB |

## R2 verification and remaining publication

Verified October 18, 2026, at 17:29 UTC: all 17 public R2 URLs returned the expected content lengths and `video/mp4` type. Three 64 KiB ranges from the beginning, middle and end of each object returned HTTP 206 and matched the local files byte-for-byte. This is sampled comparison, not a full remote SHA-256 check.

All 17 actual public R2 streams also passed browser checks for expected duration/resolution, initial playback, midpoint seeking and resumed playback. These checks used the unchanged archive-page HTML served locally, with no substitution of local video files.

The 17 public archive-page URLs still returned HTTP 404. Publish the prepared site changes, then confirm an embedded player on the live site. Upload verification does not establish that the archive pages themselves are published.
