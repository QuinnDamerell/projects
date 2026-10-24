# Crack the Whip recreation

`docs/crack-the-whip/crack-it/index.html` (served at `/crack-the-whip/crack-it/`) is a standalone easter egg linked by **Experience The Original App Now** on the existing project story. Zensical copies the HTML unchanged. It does not add another project to navigation, the project count or search. The parent link uses `target="_self"` to keep normal document navigation into the standalone app. Styles and behavior live in `docs/stylesheets/whip-app.css` and `docs/javascripts/whip-app.js`.

## Search and link previews

The page's title is the original app's name, **Crack the Whip for Windows Phone**, and search engines may index it (it had `noindex` until October 22, 2026). Its head carries a meta description, a canonical URL, Open Graph tags and an X `summary` card. The share image is the original 300 × 300 live tile, `docs/assets/crack-the-whip/LargeMobileTile.png`, referenced by absolute URL because link-preview crawlers do not resolve relative paths. X reads the title, description and image from the Open Graph tags; only the card type and image alt text are separate. Zensical's `sitemap.xml` lists only Markdown pages, so crawlers find this page through the project story's link. If the page moves, update `og:url`, the canonical link and the image URL together.

## Original source and appearance

The reference is `D:\Project Archive\Projects\WhipCrack\WhipCrack\WhipCrack\MainPage.xaml` and its `.xaml.cs` code-behind, together with the already published `docs/assets/crack-the-whip/ScreenShot.png`. The archive drive was only read. No old executable or project was run.

The recreation preserves the black background, Segoe-style type, instruction copy, two original phone diagrams, Whip / Crack labels, outlined lowercase button and original credit. The app fills the viewport vertically, with content capped at 480px and scaled down on phones. There is no top toolbar or About disclosure. The historical domain remains visible in the credit, but the link goes to Quinn's current site. OS battery/time chrome is omitted; this is a browser layout, not a request for the browser's Fullscreen API.

The diagrams were copied unchanged from the source project's `Images` directory into `docs/assets/crack-the-whip/`. SHA-256 values match the originals:

| File | SHA-256 |
| --- | --- |
| `WhipForward.png` | `8f2159bf35937ad92580e2fa0a916846c77c6c36dde85d5669da8d9ee7d43081` |
| `CrackBack.png` | `1de47ac0fe057ec5c5067f583d71e2cd1afd9b2f339efcd536dcd4655eae6dbe` |

PNG and WAV files already have LFS patterns. The three original WAVs are reused from the earlier recovery; no sound is synthesized or edited.

## Motion and sound

The active C# handler starts in `Back`, switches to `Forward` (whip) only below −30° roll, then back to `Back` (crack) only above +30°. The source's smoothed `MotionMonitor` code is not called by the app and is not ported.

**What is measured.** The browser controller uses the motion the app's two diagrams show: the phone turned within its own screen plane, like a steering wheel. The tilt is 0° upright, negative when the top turns toward the screen's left edge (the Whip diagram) and positive toward its right edge (the Crack diagram). It is computed from `beta` and `gamma` as the angle of the right edge's and top's upward components, which is the bottom row of the full W3C Z–X′–Y″ rotation. So the tilt stays smooth as an upright phone swings, where raw `gamma` folds at ±90° and jumps. Only gravity matters, so the heading (`alpha`) is not needed, can be missing, and cannot drift. Tilting toward or away from you, or turning to face another way, never changes the tilt. Within 20° of lying flat, gravity barely touches the screen plane, so those readings count as working motion but are ignored.

**Sounds.** The cycle starts at whip: turning the top more than 30° to the left plays `Whip1.wav`. After that, only turning more than 30° to the right can play `Crack1.wav`, then only left again, in strict alternation. Holding a pose, continuing the same stroke, or moving within one side never repeats a sound. Within 30° of upright or upside down is neither side, so turning past upside down cannot wrap from one side straight into the other. With the screen facing out from your right hand, as when holding the phone like a whip handle, pulling it back over your shoulder turns the top toward the screen's left, so it whips, and snapping it forward cracks.

**History.** The first recreation used raw `gamma`, which played the wrong sound mid-swing. A second attempt measured twist about the phone's long axis, which a whip swing barely produces, so real swings were silent. A third measured the top leaning back and forward toward the player, which responded to tilting the phone toward or away from you rather than side to side, unlike the diagrams. On October 22, 2026, Quinn asked for the side-to-side axis the original used.

Each new sound stops the previous sound's tail. The separate button plays the original `WhipAndCrack.wav`; no sensor permission is needed for button playback. The browser controls sample delivery, so the original requested 10ms update period cannot be promised.

**Preloading.** All three WAVs download as soon as the page opens, while the welcome dialog is still showing, so the first tap only has to decode them. Browsers allow sound only after a tap, so no `AudioContext` exists before then. A failed preload is downloaded again by the first tap. Decoding takes over the downloaded bytes, so a failed decode also downloads again on the next tap. Decoding accepts both the callback form (older WebKit, through `webkitAudioContext`) and the promise form. All three sounds decode before motion listening starts, so sensor events do not fetch, decode or unlock audio.

**Silent Mode on iPhone and iPad.** iOS plays Web Audio as ambient sound, which Silent Mode mutes, but plays `<audio>` elements as media, which it does not. While any media element plays, the page's Web Audio also uses the media channel ([WebKit bug 237322](https://bugs.webkit.org/show_bug.cgi?id=237322)). On iOS only, the first tap that unlocks sound also starts a looping, unmuted `<audio>` element. Its source is half a second of 44.1 kHz, 16-bit mono silence generated in memory as a WAV blob, so there is no extra asset. It has `x-webkit-airplay="deny"` and `disableRemotePlayback`, starts before the `AudioContext` in the same tap, and is never added to the page, so it is not mistaken for the native fallback player. It pauses whenever the page is hidden, left or the native player starts, and the next tap restarts it. If iOS refuses it, the sounds still play, and only Silent Mode still mutes them. iOS is detected from the user agent: iPhone, iPad or iPod, or a Mac user agent with a multi-touch screen for iPadOS. Android and desktop browsers never create the element, so they show no media controls.

Side effects on iOS: starting the page's sound pauses music from other apps, as any media playback does, and Safari shows its speaker icon while the page is open.

`navigator.audioSession.type = 'playback'` from the [Audio Session API](https://www.w3.org/TR/audio-session/) is meant to do the same job, and the page does not set it. On Quinn's iPhone on October 22, 2026, a version that set it played only with Silent Mode off. The silence first blamed on that line was Silent Mode. The line neither helped nor hurt, and it was removed.

## Debug display

Add `?debug` to the URL (`/crack-the-whip/crack-it/?debug`) to show a fixed, tap-through panel above the app. It refreshes ten times a second from the latest reading and has no effect without the parameter: no element, no timer.

| Line | Shows |
| --- | --- |
| `motion` | Motion state (`off`, `starting`, `waiting`, `on`) and readings received in the last second |
| `alpha beta gamma` | The raw `deviceorientation` angles, or `none` |
| `lean` | How far the screen leans from upright toward or away from you; readings past 70° count as flat and are ignored |
| `tilt` | The side-to-side tilt the tracker uses, and its zone: whip side, crack side, middle, upside down, flat, unusable reading or no reading yet |
| gauge | −180° (L) to +180° (R) in 10° steps; `|` marks ±30°, `:` upright, `O` the current tilt |
| `next` | The only sound that can play next and what it needs |
| `stroke` | The furthest left and right tilts since the last sound, which shows whether a missed swing fell short of 30° |
| `sounds` | The last five sounds, newest first, with the tilt each fired at |
| `audio` | `AudioContext` state and, on iOS, whether the silent clip is playing |

## iOS and Android

| | iOS (Safari, and Chrome on iOS) | Android (Chrome, Samsung Internet, Firefox) |
| --- | --- | --- |
| Motion permission | `DeviceOrientationEvent.requestPermission()` runs in the **ok** or **Enable motion** tap. Safari may remember the answer, so later visits might not prompt. | No prompt; the API has no `requestPermission`. A site setting that blocks motion sensors shows the no-readings notice after seven seconds. |
| Orientation source | Fused gyroscope attitude. Only its gravity part (`beta`, `gamma`) is used. | Chrome derives `deviceorientation` from Android's game rotation vector (gyroscope fusion). Only `beta` and `gamma` are used. Phones without a gyroscope may be less reliable during fast swings. |
| Sound unlock | `AudioContext.resume()` in the same tap, plus the looping silent clip so Silent Mode does not mute the sounds. | `AudioContext.resume()` in the same tap. |

Both need HTTPS. Angles are in the device frame, so the screen auto-rotating mid-swing does not change the measurement, though the layout may rotate. The page disables double-tap zoom with `touch-action: manipulation` on the root (pinch zoom still works), and the app turns off text selection and the iOS long-press menu so a tight grip does not select text or open an image menu.

## Arrival and recovery

A native modal dialog explains the emulation, and asks players to turn their sound up, on every new document mount, including reloads; there is no remembered skip. Its **ok** button receives initial focus, so Enter dismisses it. Safari treats that arrival focus as keyboard focus and drew the page's dashed focus ring around **ok** on Quinn's iPhone, so the ring on **ok** stays hidden until the first key press anywhere on the page, which sets `data-keyboard` on `<html>`. Keyboard users still see it once they press Tab or any other key; phones and mice never do. Activating it starts `DeviceOrientationEvent.requestPermission()` when available and Web Audio resume synchronously in the same click, before any await, then closes the dialog and focuses the app. The browser may remember its permission decision; calling the API again cannot force another OS prompt. Dismissing the dialog leaves motion off and exposes the retry control.

Motion needs HTTPS or a browser-recognized local secure context; a LAN HTTP preview normally cannot enable it. Unsupported devices, denied permission, sound failures, or seven seconds without a valid reading reveal a compact recovery notice and **Enable motion** button. During normal operation those controls are hidden. Sound errors reveal the native audio player; a separate `<noscript>` player remains available without JavaScript. The project story retains the original audio downloads.

Motion and sound stop when the page is hidden or left. Returning to a retained page requires explicit re-enabling of motion, which starts again at whip. Permission/loading completion cannot restart an abandoned session. The native player and app sounds take turns: native playback stops motion and Web Audio and cancels pending app playback; pressing the app button or enabling motion pauses the native player. The page uses no external scripts, sensors never send readings anywhere, and audio files are hosted with the site.

API references used for the port:

- [Microsoft's Windows Phone attitude axes](https://learn.microsoft.com/en-us/archive/msdn-magazine/2012/june/touch-and-go-getting-oriented-with-the-windows-phone-compass)
- [W3C Device Orientation](https://www.w3.org/TR/orientation-event/#deviceorientation)
- [MDN orientation permission](https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent/requestPermission_static)

## Verification

Run `node --test tools/tests/whip-app.test.mjs tools/tests/whip-motion.test.mjs` for the steering-wheel tilt at any heading or lean, tilting toward or away from you staying silent, real swings, threshold boundaries, the upright Euler singularity, turning past upside down, lying flat, permission ordering, audio preloading, retries and both decoding forms, the iOS silent clip (including iPadOS detection and a refused clip), the untouched audio session, unsupported/error paths and cleanup races. The motion tests build each browser reading from a physical pose, so they check what a phone in that pose would report. Build with `.venv\Scripts\zensical.exe build --clean` and run `tools/check_lfs.py`. In a browser, check the arrival dialog, click and keyboard activation, reload, repeated button playback, motion/audio fallbacks and page hiding. Check 390px and desktop layouts.

Validated on October 22, 2026, after switching to the side-to-side tilt: both suites passed all 35 tests. In the Chromium preview, after **ok**, tilting toward and away from you through ±80° played nothing. Side-to-side swings played the whip at 32° left and the crack at 32° right, alternating.

Validated on October 22, 2026, after adding the iOS silent clip: both suites passed all 35 tests. The generated clip parsed as a valid half-second 44.1 kHz, 16-bit mono WAV of zeros, and in Chromium it loaded, played and kept looping. Whether it lets the sounds play in Silent Mode needs Quinn's iPhone.

Validated on October 22, 2026, after the motion rewrite and audio preloading: both suites passed all 32 tests. Before the rewrite, the same simulated swings played nothing for two of three grips. In the Chromium preview at 375 × 812 with Android Chrome's API shape (no `requestPermission`), all three WAVs finished downloading about 0.3 seconds after load with the dialog still open. After **ok**, simulated swings played the whip at 32° back and the crack at 32° forward, alternating. The button played the 1.76-second file, and nothing was downloaded twice.

Earlier validation on October 22, 2026: both suites passed all 30 tests and the clean site build passed. Browser checks covered dialog autofocus, Enter/click dismissal and focus transfer to the app, the dialog returning on reload, the no-readings fallback and button playback. Layouts were inspected at 390px, 1206px and 1440px; the 390 × 844 viewport had no horizontal overflow or extra page height and retained a 44px main button target. The scoped design detector reported no findings. An independent visual/code review returned **ship**, with no material findings. Earlier audio checks also verified native playback through its 1.76-second duration and handoff to Web Audio.

Physical phone gesture feel, iOS permission prompts, silent mode and Android sensor quality still need a real-device check over HTTPS on an iPhone and an Android phone; desktop and mocked-event tests do not establish that hardware behavior. No WebKit engine was available locally, so Safari-specific behavior is checked against platform documentation only.
