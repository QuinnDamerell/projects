# PicGen

A Java experiment with an ambitious premise: generate every possible grayscale image of a given size.

## Facts

| Documented by | Language | Code |
| ------------- | -------- | --------- |
| May 2009 | Java | Recovered from my backup; unpublished |

## The story {#description}

PicGen was designed to step through every combination of pixel shades on a grid. In theory, every image of that size and palette would appear somewhere in the sequence. All it needed was an unreasonable amount of time.

According to the description I wrote for my original website, my first full-color (RGB) attempt took about eight seconds just to cycle one pixel through every color. So I switched to grayscale to make the problem smaller. It was a fun Java proof of concept, not a practical way to find any particular picture.

## Original Screenshot

This screenshot survived in my old website backup. The five-by-five grid and progress bar are a good reminder of how quickly the number of combinations grows.

![PicGen displaying a five-by-five grid of gray pixels and a statistics bar](./assets/picgen/original-screenshot.jpg){: style="max-width:817px; width:100%;" loading="lazy"}

<details class="qd-story-details" markdown="1">
<summary>What version 2.0 can do</summary>

In the version 2.0 code I found, you can set the width and height separately and pick anywhere from 2 to 255 shades of gray. There's also a random starting grid, an adjustable window size, pause and resume, speed controls, and a statistics window.

It defaults to **5 × 5 pixels and 90 shades**. Those are just this version's defaults, though, so I can't say which settings made the older screenshot, or how far any run ever got.

</details>

## Original Record

My [May 2009 homepage](assets/media/quinndamerell-homepage-2012/site/_captures/20090526070712-QVB4AXXJ.html) introduced PicGen as a recent experiment, and my [January 2011 project index](assets/media/quinndamerell-homepage-2011/site/projects.html) described the Java and pixel-combination details. Neither says exactly when I made it.
