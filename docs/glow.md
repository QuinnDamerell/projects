# Glow - Home Decor Ambient Lighting

Five paper lanterns that turn weather, time, and notifications into color.

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| 2015    | Active      | [GitHub](https://github.com/QuinnDamerell/Glow) |

## The story {#description}

Glow is part home art, part information display: an IoT project powered by a Raspberry Pi. Each of its five paper lanterns holds a multicolor LED, driven by a PWM controller and my custom software. The colors show weather conditions or notification alerts, and you can control it all through a local HTTP server.

No suitable C# library existed at the time, so I wrote an LED animation driver for full color control and smooth transitions.

## Lighting Modes

<details class="qd-story-details" markdown="1">
<summary>Weather, clocks, and Sleepy Time</summary>

The lanterns take on different jobs in each mode:

- **Weather:** one lantern each for the day's conditions, high temperature, low temperature, wind speed, and humidity. Sunny is yellow, rain blue, clouds white, and storms purple. Temperatures blend from blue to red.
- **Clock:** month, day of the month, hour, minute, and second, shown in color or grayscale.

You can see exactly how these work in the original [weather](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/GlowPi/Programs/Weather.cs) and [clock](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/GlowPi/Programs/Clock.cs) programs.

The companion app has a master brightness control and a “Sleepy Time” schedule: start time, end time, and nighttime brightness. Glow rotates through enabled programs and gradually dims for the night. The [original controls](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/Glow/PaneControls/GlowControlPane.xaml) and [controller code](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/GlowPi/Programs/GlowControl.cs) show how the settings and transitions work.

I also published [Windows IoT LED Driver](https://github.com/QuinnDamerell/WindowsIotLedDriver) separately. This Windows Runtime component supports the TLC5947 controller and provides LED control and timed color transitions for C++, C#, and JavaScript.

</details>

## Videos

### Glow Demo Video
<!-- These are hosted on CloudFlare's R2 object storage since Pages can only take up to 25MB -->
![type:video](https://projects-storage.quinn.space/glow-demo.mp4)

## Further Reading & Media

<details class="qd-story-details" markdown="1">
<summary>Tutorial, demonstration, community post, and source code</summary>

- [Glow — Hackster project listing](https://www.hackster.io/quinndamerell) — Hackster.io. Quinn's profile lists the [original Glow tutorial](media/hackster-glow-2015.md), credits Quinn Damerell and Marilyn Welniak, and retains the [original cover photograph](https://hackster.imgix.net/uploads/cover_image/file/68239/WP_20150617_05_14_19_Pro__highres.jpg). I couldn't get to the full tutorial on Hackster when I last checked.
- [Glow — A Windows Universal IOT Raspberry Pi Maker Project!](https://www.youtube.com/watch?v=cmgteH09jJQ) — Quinn Damerell, September 1, 2015 · 16:04. The original YouTube project demonstration, whose description links to the Hackster tutorial.
- [Glow! A Home Decor(ish), Ambient Lighting(ish), Real-time World System!](https://www.reddit.com/r/DIY/comments/3ja145/glow_a_home_decorish_ambient_lightingish_realtime/) — r/DIY, September 1, 2015. Quinn's original Reddit announcement, linking to the Hackster project.
- [Weather mode](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/GlowPi/Programs/Weather.cs) and [color clock](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/GlowPi/Programs/Clock.cs) — original source code showing how information becomes lantern colors.
- [Brightness and Sleepy Time controls](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/Glow/PaneControls/GlowControlPane.xaml) and [program controller](https://github.com/QuinnDamerell/Glow/blob/dabeba4fd0ddfad58bfde7464fb3eeb661dc9e13/GlowPi/Programs/GlowControl.cs) — original app interface and lighting schedule.
- [Windows IoT LED Driver](https://github.com/QuinnDamerell/WindowsIotLedDriver) — Quinn's separately published driver library, with an animation example and controller documentation.

</details>
