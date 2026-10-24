# Local project and personal-site archive review

Reviewed October 21, 2026. This is a contributor research note, not published site content.

The strongest recovery is the original **Crack the Whip audio**, followed by **five early Flash animations**, **CrossTxT's notification sound**, **Ninja Cam screenshots**, **PicGen's screenshot and source**, and **Gathr's original artwork and source**. Several omitted apps and prototypes also deserve consideration.

## Scope and method

| Read-only archive root | Files, including hidden files | Bytes |
| --- | ---: | ---: |
| `D:\Project Archive\Projects` | 38,866 | 4,795,403,035 |
| `D:\Website Archive\Websites\Personal` | 1,864 | 596,590,172 |
| `D:\Website Archive\Websites\Backups\Personal\Personal` | 923 | 33,170,724 |
| **Total** | **41,653** | **5,425,163,931** |

All 78 project directories were inventoried. Review concentrated on first-party source, descriptions, screenshots, audio/video, and historical webpages. Generated output, dependencies, and version-control internals were not read line by line. The five top-level RAR archives were listed without extraction; the WhipCrack release XAP was inspected as a ZIP without running it. This is a discovery audit, not a certification that every archived file has been examined.

Compared with the current `personal-projects/docs` project pages, media inventories, and existing assets, plus the current `personal-site` homepage. Existing editorial exclusions in `media-archive.md` were honored. Selected images were visually inspected and/or compared by SHA-256; WAV headers, video metadata, and SWF headers were inspected without running archived applications.

During the initial audit, no files on D: were written or changed, and no archived application, PHP backend, Java applet, or Flash program was executed. Only this note and a temporary Minecraft video preview on C: were created. After the user approved the additions, selected media was copied to the C: projects repository and the site was updated. The five recovered SWFs were subsequently played through self-hosted Ruffle for verification. D: remained read-only throughout. See [local-recovery.md](local-recovery.md) for the implementation and validation record.

For compact paths below:

- **P** = `D:\Project Archive\Projects`
- **W** = `D:\Website Archive\Websites\Personal`
- **B** = `D:\Website Archive\Websites\Backups\Personal\Personal`

## First additions to make

### 1. Crack the Whip: the actual app sounds

These are the three files loaded by the original app. All three are byte-for-byte identical to the corresponding entries in `P\WhipCrack\Release\WhipCrack.xap`, verified by SHA-256.

| File | Duration | Bytes | Original use |
| --- | ---: | ---: | --- |
| [WhipAndCrack.wav](<D:/Project Archive/Projects/WhipCrack/WhipCrack/WhipCrack/sounds/WhipAndCrack.wav>) | 1.760 s | 310,568 | The **crack the whip** button |
| [Whip1.wav](<D:/Project Archive/Projects/WhipCrack/WhipCrack/WhipCrack/sounds/Whip1.wav>) | 0.351 s | 62,032 | First motion-triggered sound |
| [Crack1.wav](<D:/Project Archive/Projects/WhipCrack/WhipCrack/WhipCrack/sounds/Crack1.wav>) | 1.469 s | 259,248 | Second motion-triggered sound |

All are 44.1 kHz, 16-bit stereo PCM WAVs. The combined sound is the best default for a small player or button on the existing project page; the two components can sit below it as an optional detail.

Evidence: [MainPage.xaml.cs](<D:/Project Archive/Projects/WhipCrack/WhipCrack/WhipCrack/MainPage.xaml.cs>) loads the files at lines 49–59 and plays the combined effect in `Button_Tap` at lines 146–150. Motion readings alternate the individual sounds when roll crosses −30° / +30°. The source preserves a button-only fallback for devices lacking the Motion API. This supports a more concrete explanation of the old compatibility issue, without claiming to have reproduced it.

Original gesture artwork, store artwork, source, and release packages also survive. The two images currently displayed on the project page already exist in the current assets, so audio is the meaningful new addition. Source is recovered locally; that does not create a public source-code URL.

The `org` folder contains four sound-source candidates. One filename credits BLASTWAVEFX; their original licensing records were not established by this scan. Keep that provenance with the recovery rather than describing the effect as a recording Quinn personally made.

Checksums:

```text
WhipAndCrack.wav  aa30b935bf5c606ccbd6bfce1fa4f14b06fd0ef66e4ee665306a615ea912e4b7
Whip1.wav         3c3121a95570527cf21235fbb0750d885fde076ae3244f8c6f1dfd7a9ee7f439
Crack1.wav        1946717b9ab7fbaff8545cfcdf0e05e9258a43aac0e3d918f0868d9819aa49f6
```

### 2. Five early Flash animations

The oldest-looking website backup contains actual animation binaries, not just dead links. Corresponding copies also survive under `W\2023\old\websites\animations`.

| Recovered file | Canvas | Main timeline duration |
| --- | --- | ---: |
| [snowman_snow_fight.swf](<D:/Website Archive/Websites/Backups/Personal/Personal/websites/animations/movies/snowman_snow_fight.swf>) | 500 × 500 | 11.11 s |
| [3D.swf](<D:/Website Archive/Websites/Backups/Personal/Personal/websites/animations/movies/3D.swf>) | 320 × 240 | 21.60 s |
| [BadDay1.swf](<D:/Website Archive/Websites/Backups/Personal/Personal/websites/animations/movies/BadDay1.swf>) | 320 × 240 | 4.58 s |
| [stick1.swf](<D:/Website Archive/Websites/Backups/Personal/Personal/websites/animations/stick1.swf>) | 100 × 100 | 3.00 s |
| [stick 2.swf](<D:/Website Archive/Websites/Backups/Personal/Personal/websites/animations/stick%202.swf>) | 100 × 100 | 3.00 s |

All five have valid compressed SWF version-5 headers. Durations are calculated from main-timeline frame counts/rates, not verified playback lengths. The site calls itself **Quincy's Movie Index**. The old `others.htm` calls the snowman fight the first animation Quinn made; `sick_figures.htm` describes the 3D fight as the second. Preserve those original captions: they add more personality than a generic project description. Pages for BadDay2 and street survive, but their referenced SWF files were not found.

Recommended addition: an early-animation gallery on `early-experiments.md`, with modern video previews and the original SWFs retained as artifacts. Rendering/conversion and playback QA remain future work; this scan did not execute them. Some historical HTML points to misspelled or differently named movie paths, so restoration should use the files actually present.

### 3. CrossTxT's notification sound

[alert.mp3](<D:/Project Archive/Projects/crosstxt/alert.mp3>) is a valid 0.784-second stereo MP3, 12,564 bytes. `P\crosstxt\crosstxt.php` lines 2509–2512 embeds it with the OGG alternative, establishing that it was used by the web app.

Add an **Original notification sound** player to the CrossTxT page. `alert.ogg`, `alert.wav`, and `alert_org.wav` also survive, with copies in `CrossTxT Giving v1`. The two nonempty WAV versions have different hashes; `alert-old1.wav` is empty. Do not count each encoding or transfer-bundle copy as a separate lost sound.

A previously absent [Chrome extension screenshot](<D:/Project Archive/Projects/crosstxt extension/screenShot.png>) also survives. Review the visible conversation content before selecting it for a public gallery.

### 4. Ninja Cam screenshots and source

The current page says that the screenshot files and code have not been recovered. Both are now present:

- [Screen1.png](<D:/Project Archive/Projects/NinjaCam/Media/ScreenShots/Screen1.png>): original help screen.
- [Screen2.png](<D:/Project Archive/Projects/NinjaCam/Media/ScreenShots/Screen2.png>): imitation Wikipedia Ninja page, with **Image Captured** status.
- [Screen3.png](<D:/Project Archive/Projects/NinjaCam/Media/ScreenShots/Screen3.png>): third original screenshot.
- [MainPage.xaml.cs](<D:/Project Archive/Projects/NinjaCam/NinjaCam/SpyCam/MainPage.xaml.cs>): Windows Phone source.
- `P\NinjaCam\Release\NinjaCam 1.0.xap` and `NinjaCam 1.5.xap`: preserved packages.

Replace the screenshot-leads section with a real gallery and correct the local-source recovery status. A separate `NinjaCamWin8` prototype is incomplete: its capture method is a placeholder that writes text, so it should not be described as a released Windows 8 camera app.

### 5. PicGen: a screenshot and a more accurate story

The current description says black-and-white, an n × n grid, and no recovered code. The archive supplies an [817 × 657 original screenshot](<D:/Website Archive/Websites/Backups/Personal/Personal/PicGen/PicGen.jpg>), Java source, and JARs.

[PicGen.java](<D:/Project Archive/Projects/PicGen/src/PicGen/PicGen.java>) identifies **PicGen 2.0** and supports independent width/height, 2–255 grayscale levels, optional random starting pixels, and adjustable window dimensions. Its default inputs are **5 × 5 and 90 shades**. `MainWindow.java` preserves pause/resume, speed, and statistics controls. These are the surviving source version's defaults, not proof of the settings used in every historical run or in the screenshot.

`B\PicGen\index.php` preserves a better origin story: the initial RGB experiment reportedly took about eight seconds to cycle every color for just one pixel, prompting a move to grayscale. Add that creator account, the screenshot, and the recovered-source status. Avoid presenting the square black-and-white version as the only implementation.

### 6. Gathr's original illustration and source

The current page's **Code: Not recovered** can be updated to acknowledge a recovered local copy. Both halves survive:

- Android: `P\Gathr\Android\src\com\DamerellEhrlichReid\Gathr`
- Server: `P\Gathr\Server\src\com\DamerellEhrlichReid\server`

The [original architecture illustration](<D:/Project Archive/Projects/Gathr/GathrDiagram.png>) is particularly good period material: Android, a service helper, SSL, Java/MySQL, and notification components. `GathrBanner.png` and `Android\res\drawable\storeicon1.png` also survive. All three are absent by hash from the current image assets.

Recovered layouts substantiate scheduled start/end times, invitations, RSVP changes, and an event message board. Add selected details to the existing story, with the illustration rather than a large source dump.

## Other worthwhile additions

| Candidate | Recommendation and evidence |
| --- | --- |
| **Purdue Menu for Windows Phone** | Add a platform-history section to the existing Android-focused page. [Screenshot 1](<D:/Project Archive/Projects/PurdueMenuWP/Media/1.png>) through `4.png`, source, and packages survive. `PurdueMenu\Properties\WMAppManifest.xml` identifies Windows Phone 7.1 and app version 1.0.0.0. Existence is established; original launch date is not. |
| **Purdue Menu promotional artwork** | [Three-phone promotional image](<D:/Project Archive/Projects/PurdueMenuPrivate/Media/PurdueMenuFlyer/final.png>) is a good nostalgic addition beyond the current gallery. Editable flyer DOCX files and `Media\highres_promo.png` survive too. |
| **Baconit's early visual evolution** | Native 768 × 1280 screenshots survive under `P\Baconit\Media\ScreenShots\2.5\768X1280\1.png`–`8.png`, versus 329 × 548 store recoveries on the current site. Versions 1.2, 1.3, 1.4, 1.5, 1.8, 2.3, and 2.4 fill gallery gaps. [Version 1.3 main screen](<D:/Project Archive/Projects/Baconit/Media/ScreenShots/1.3/main_reddits.png>) and [version 2.5 screenshot 1](<D:/Project Archive/Projects/Baconit/Media/ScreenShots/2.5/768X1280/1.png>) are absent by hash from current assets. Select a small evolution gallery rather than publishing every duplicate. |
| **Zune Playlist Shuffler** | The original site download, `B\ZuneShuffler\Zune Playlist Shuffler 1.3.jar`, and `zuneplaylist.png` survive. Separately, `P\Zune Playlist Shuffler\src\zuneplaylistshuffler\GUI.java` identifies v2.0. Add a recovered-source/version note; do not assume v2.0 was publicly released. |
| **PurdueBus construction artifacts** | `P\PurdueBus\Media\Google Earth Routes` contains BasicLoop, GoldLoop, RossAde, SilverLoop, and Tower Acres KML files. Nice material for explaining the original route-building process. |

## Restoring the old homepages

The backup folder contains the older PHP-era site, while `W` contains `2023` and `2025` directories with later sites and an `old` subtree. Folder labels and copied filesystem dates are not reliable publication dates. The backup is valuable earlier content, but this scan does not establish it as the oldest copy that exists anywhere.

- **Full-sized photographs:** originals survive where the current Wayback-based gallery uses thumbnails. Examples under `B\images\picture_page` include `miss_indiana_2008\41.jpg` (427 × 640), `miss_indiana_2008\Miss Indiana 017.JPG` (779 × 350), `miss_indiana\opening_full.JPG` (796 × 556), `senior\1l.jpg` (764 × 594), and `Casey_computer1_full.jpg` (615 × 420). The 2009 and 2010 theater galleries also contain larger images. Restore selectively with local-backup provenance.
- **Early websites:** the animation site, Fireworks site (`websites\Friework Web`, original spelling), and Crazy Horse class project survive as fuller local website trees. These can extend the early-experiments collection beyond descriptions.
- **Actual applet/download binaries:** Pong, Shooter, and Freezer class files; PicGen JAR; and Zune Shuffler JAR survive. They can fill archive download gaps without executing applets in the restored website.
- **Next Bus and TxTBack pages:** both `2023` and `2025` copies contain their original `index.html` pages, but they say **This page is coming soon**. Useful to replace an unavailable-page notice, not to invent a fuller product story.
- **Thinking of You:** original landing page and image tree survive in the later sites. Its PHP backend remains source evidence, not part of a functional static restoration.
- **More school-video references:** `B\videos.php` records English Final 2008 parts 1/2/3 as `9CDAWBQSoYI`, `Zte3l6EuaIc`, and `a4cTdxaSgeo`, and English Final 2007 as `4zJcmMbN1gI`. The current early-experiments page retains only the first reference. These are local recovery leads, not verified playable videos; no local video copies were found.
- **Conflicting early dates:** `B\websites.php` dates Animation/Fireworks/Crazy Horse as 2002/2004/2005; the already archived index used by the current site says 2004/2006/2007. Preserve the discrepancy and ask Quinn before revising the timeline. Neither source automatically wins.

The website pass found local filename/path candidates for 99 of 116 unavailable 2011 manifest references and 101 of 122 unavailable 2012 references, including 60 photo-gallery references in each. These overlap and are **candidate matches**, not 200 distinct recoveries or proof of identical historical revisions. Each accepted replacement should record local provenance and retain the original Wayback record.

## Material to preserve, but not claim as newly discovered content yet

- **Liquid Physics original demo:** [LiquidWallpaper.avi](<D:/Project Archive/Projects/LiquidPhysicsFull/Media/LiquidWallpaper.avi>) is 96,568,232 bytes, 640 × 480, about 4:34.77, with MPEG-4 video and mono MP2 audio. The current site already embeds an R2 demo; compare the recordings before presenting this as an additional video. Original media/description documents also survive, but the DOCX contents were not examined in this pass.
- **Minecraft recording:** [minecraft.mp4](<D:/Website Archive/Websites/Personal/2025/QuinnDamerell.com/Images/minecraft.mp4>) is 295,337,355 bytes, 1920 × 1080 at 60 fps, about 3:47.06. Metadata says Minecraft and has a 2017-11-09 creation timestamp. A frame at 30 seconds shows Minecraft survival gameplay. No current-site reference was found, and its purpose/ownership cannot be established from the filename and one frame. Do not label it QWorld footage.
- **TxtBack original design files:** `P\TxtBack\Media\txtback1.xcf`, logo exports, and announcement-style DOCX files survive. Private-looking conversations/tester material was not included in recommendations.
- **Libarae, Nielsen Digital Diary, and GPSTagger:** substantial source survives, but personal/coursework context should be established before turning them into prominent portfolio entries.
- **Known duplicates:** sampled Instemote, Loyalty, Next Bus, PurdueBus, and Liquid Physics website images match existing assets exactly. A different hash alone can also reflect re-encoding rather than a new picture.
- **Libraries and tutorials:** AmbilWarna, NeHe OpenGL assets/sounds, DroidNova examples, and portions of CryptoCoinX are third-party material or require authorship clarification. They are not automatically Quinn-authored lost media.
- **Source publication:** some old projects contain embedded authentication values, account/transfer material, and private data. Recovered source status can be acknowledged without publishing the whole archive. Any later public source release needs a focused selection and review.

Large videos exceed the site's 25 MB per-file limit and belong in the existing R2 workflow if selected. No remote media was downloaded, uploaded, or compared during this local scan.

## Selected project-directory findings

This table records triage results for every immediate project directory. Names reflect the disk exactly.

| Directory | Result |
| --- | --- |
| 390Lang | Java crawler/search servlet coursework. |
| AI_HW1 | Tower of Hanoi coursework. |
| AI_HW2 | Hill-climbing and genetic-algorithm exercises. |
| AIHW4 | Eclipse metadata; no source found. |
| AmbilWarna | Upstream Android color-picker dependency. |
| AndroidPurdueMenu | Bare SVN repository; possible future history recovery. |
| AndroidTodoClient | Android to-do experiment. |
| AzureRedditTimeMachiene | Azure deployment solution/configuration. |
| Baconit | Source, artwork, rich early screenshot archive. |
| Baconit7.8 | Older branch; overlapping and additional screenshots. |
| BusParser | Transit routes/stops/shapes/trips parser. |
| BusReader | Bare SVN repository. |
| BusRouteEarthToArray | Route-conversion utility. |
| CedarPointWP | Earlier shell/build artifacts. |
| City Bus | Next Bus source; sampled screenshot already published. |
| CityBusLiveTime | Transit live-time reader/parser. |
| crosstxt | Web source and original notification audio. |
| crosstxt extension | Extension source and additional screenshot. |
| CrossTxT Giving v1 | Transfer bundle; overlapping code/audio and private material. |
| CrossTxTJavaPush | Bare SVN repository. |
| CryptoCoinX | CCXSharp/MtGox library and WPF UI; authorship needs separation. |
| CS 180 | Java coursework, word solver/trie and other assignments. |
| CS 240 | C exercises including Connect-X and semaphores. |
| CS 590G | Empty. |
| CS250 | Low-level/C exercises and benchmark plots. |
| CS251 | Search/crawler work and Purdue map editor/viewer. |
| CS334 | Graphics coursework; shaders, height maps, trees. |
| CS352 | Compiler/parser coursework. |
| CS390 | Servlet, file-server, Swing, and Racket exercises. |
| cs390-ds0 | Distributed chat/reliable/FIFO channels. |
| cs390-ds0-project-0 | Client/server chat and heartbeat project. |
| CS390C-Assignment4 | Small Java coursework. |
| CS422 | Networking labs, benchmarks, Windows Phone experiment. |
| CS448 | Database/query/optimizer coursework. |
| DistHW3 | Inverted-index project. |
| Fall | Android starter/surface-view experiment. |
| Gathr | Android/server source and original illustration/branding. |
| GPSTagger | Named GPS-point capture utility. |
| instemote | Source, geofence task, known images. |
| Insteon | Overlapping Instemote source copy. |
| libarae-client | Java library desktop app. |
| libarae-communication | Shared library-app protocol. |
| libarae-server | Library-app server/database code. |
| LiquidPhysicsFull | Android source, demo AVI, promotional assets. |
| LiquidWallpaper | Bare SVN repository. |
| Loyalty | Phone/cloud source; sampled image already published. |
| NielsenDigitalDiary | Android TV diary; context/ownership unconfirmed. |
| NinjaCam | Screenshots, source, and release packages recovered. |
| NinjaCamWin8 | Incomplete Windows 8 port. |
| OnMyWay | Windows Phone starter template. |
| OpenGL | NeHe tutorials and associated assets. |
| Part4 | Eclipse metadata; no substantive src content found. |
| PicGen | Java source, JAR, configurable grayscale implementation. |
| PurdueBus | Source/media plus Google Earth route files. |
| PurdueMenu | Existing Android app source. |
| PurdueMenuPrivate | Historical APKs, promotional art, flyers. |
| PurdueMenuWP | Omitted Windows Phone version and screenshots. |
| RedditTimeMachine | SVN repository storage rather than checked-out app. |
| RemoteSystemsTempFiles | Eclipse metadata. |
| StateFarm | Java competition/challenge exercises. |
| StateFarmLocal | Second competition exercise tree. |
| ThinkingOfYou | Existing app source and artwork variants. |
| TodoClient | Java system-tray to-do client experiment. |
| TxtBack | Existing project source, logos, design/announcement files. |
| vortex-part-vi | DroidNova Android/OpenGL tutorial material. |
| VsoBuildHud | Build-watching prototype with blank WPF main view. |
| VsoBuildHudWebsite | Adapted Visual Studio Online OAuth companion sample. |
| WhipCrack | Three release-identical sounds, source, artwork, packages. |
| WindowsIotLedDriver | LED/PWM/animation library and sample; already referenced by Glow. |
| Zune Playlist Shuffler | Source identifies v2.0. |
| ZunePlayListShuffler | Separate SVN repository storage. |

Top-level loose artifacts were inventoried separately: five RAR archives, two Gathr server JARs, a Baconit XAP, and a key file. The key's contents were not needed or included. RAR listings mostly overlap the directory trees; the Liquid Physics 1.9.1 archive also contains the demo AVI.

## Suggested implementation order

1. Add the three Whip sounds and CrossTxT notification audio to the existing pages.
2. Add Ninja Cam, PicGen, and Gathr images and correct their recovery status/history.
3. Recover viewable versions of the five childhood animations and selected early webpages.
4. Add the Purdue Menu Windows Phone section; curate the nostalgic promotional artwork.
5. Repair selected homepage archive gaps with explicitly labeled local-backup evidence, keeping historical date conflicts visible.
