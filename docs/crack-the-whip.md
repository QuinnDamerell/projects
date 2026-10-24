# Crack The Whip

A Windows Phone app that turned a tap or a well-timed swing into a whip crack.

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| By June 2012 | Retired | Recovered from my backup; not published |

## The story {#description}

Crack the Whip was world-famous—or at least friend-group-famous. Tap a button or swing your phone to hear a whip crack. Pulling the phone behind your head played the swish; snapping it forward delivered the crack. Two sounds, one satisfying illusion.

On June 5, 2012, in a [Reddit thread about my Windows Phone apps](media/reddit-crack-the-whip-2012.md#comment-c4wkt3k), I mentioned that it worked great on the HTC Titan but less reliably on other phones. So it was already out by then, though I don't know exactly when I first made it.

## Crack the whip

Do you have what it takes to crack the whip? My friends and I still joke about this app, so I rebuilt it for the web using the original sounds and artwork from my backup. The screen, the button, and the swing-to-crack motion controls are all there, so you can try it right now.

<a class="md-button md-button--primary" href="crack-the-whip/crack-it/index.html" target="_self">Experience The Original App Now</a>

For the full experience, open it on your phone and turn on motion. Or just press the button to hear the exact 1.76-second whip crack the original app played.

<audio class="qd-original-audio" id="whip-original" controls preload="none" aria-label="Original Crack the Whip button sound">
  <source src="assets/crack-the-whip/WhipAndCrack.wav" type="audio/wav">
  <a href="assets/crack-the-whip/WhipAndCrack.wav">Download the original sound</a>.
</audio>

[Download the original sound](assets/crack-the-whip/WhipAndCrack.wav){: download="WhipAndCrack.wav"}

<details class="qd-story-details" markdown="1">
<summary>The two sounds behind the swing</summary>

The motion controls played these two sounds separately. In the original code, the app switches between them as the phone rolls past −30° and +30°. Phones without the Motion API just used the button.

**The whoosh**

<audio class="qd-original-audio" controls preload="none" aria-label="Original whip whoosh">
  <source src="assets/crack-the-whip/Whip1.wav" type="audio/wav">
  <a href="assets/crack-the-whip/Whip1.wav">Download the whoosh</a>.
</audio>

**The crack**

<audio class="qd-original-audio" controls preload="none" aria-label="Original whip crack">
  <source src="assets/crack-the-whip/Crack1.wav" type="audio/wav">
  <a href="assets/crack-the-whip/Crack1.wav">Download the crack</a>.
</audio>

All three files are the exact sounds from the original release package, byte for byte.

</details>

## Images

### App Icon

![Crack the Whip app icon](./assets/crack-the-whip/LargeMobileTile.png){: style="height:150px;"}

### Screenshots

![Crack the Whip app screen](./assets/crack-the-whip/ScreenShot.png){: style="height:200px;"}

## Further Reading & Media

- [Quinn discusses Crack the Whip's device compatibility](media/reddit-crack-the-whip-2012.md#comment-c4wkt3k) — r/windowsphone, June 5, 2012. My notes on which phones it worked best on, from a thread about my apps.
