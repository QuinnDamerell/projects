# Prism

An acrylic desktop sculpture that turns a grid of LEDs into colorful 3-D patterns.

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| 2016    | Active      | [GitHub](https://github.com/QuinnDamerell/Prism) |

## The story {#description}

Inspired by Glow, Prism trades individual LEDs for a 10 × 10 Adafruit NeoPixel grid. Acrylic columns of different heights and cut angles refract its light into vivid patterns. I cut the acrylic with Microsoft Garage's laser cutter.

A cardboard base holds a Raspberry Pi Zero W and the LED matrix, so the finished unit only needs power. My custom software (it's on GitHub) handles pattern selection, cross-fades, on/off schedules, and control through an HTTP server and web interface.

## Animation Patterns

<details class="qd-story-details" markdown="1">
<summary>Six animated “gems” and the code behind them</summary>

Prism calls its animations “gems”: random colors, color peaks, color swipes, a running pixel, expanding drops, and moving rows. Each pattern keeps moving as it cross-fades into the next one over three seconds. The [animation controller](https://github.com/QuinnDamerell/Prism/blob/a54c1978693ee7c6c464a06e7da0c0fb5e49a930/Prism/src/Prism.cpp) has the selection and transition logic.

My separate [LightFX library](https://github.com/QuinnDamerell/LightFX) supplies layered drawing and fading. The [expanding-drops pattern](https://github.com/QuinnDamerell/Prism/blob/a54c1978693ee7c6c464a06e7da0c0fb5e49a930/Prism/src/Gems/ExpandingDropsGem.cpp), for example, creates colored drops at random positions and changes their arrival rate over time.

</details>

## Videos

<!-- These are hosted on CloudFlare's R2 object storage since Pages can only take up to 25MB -->
### Finished Demo Video
![type:video](https://projects-storage.quinn.space/prism-final.mp4)

### Prototype Demo Video
![type:video](https://projects-storage.quinn.space/prism-prototype.mp4)

## Further Reading & Media

<details class="qd-story-details" markdown="1">
<summary>Animation source and LightFX library</summary>

- [Prism animation controller](https://github.com/QuinnDamerell/Prism/blob/a54c1978693ee7c6c464a06e7da0c0fb5e49a930/Prism/src/Prism.cpp) — the six animated patterns and their cross-fades.
- [Expanding drops](https://github.com/QuinnDamerell/Prism/blob/a54c1978693ee7c6c464a06e7da0c0fb5e49a930/Prism/src/Gems/ExpandingDropsGem.cpp) — one complete animation, showing how layered colored drops are generated.
- [LightFX](https://github.com/QuinnDamerell/LightFX) — the separate drawing and animation library used by Prism.

</details>
