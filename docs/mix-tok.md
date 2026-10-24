# MixTok

Mixer gameplay highlights, indexed and ranked in a TikTok-style swipeable feed.

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| 2019    | Retired      | [GitHub](https://github.com/QuinnDamerell/mixtok-service) |

## The story {#description}

MixTok was a short-lived experiment built on Mixer.com's clipping feature. Streamers were already saving and sharing their best gameplay moments, so MixTok indexed and ranked those clips into a familiar, TikTok-style feed you could swipe through.

## ClipMine

<details class="qd-story-details" markdown="1">
<summary>Clip search, filters, and ranking</summary>

The service also included **MixTok - ClipMine**, a browser-based clip explorer. Its [original interface](https://github.com/QuinnDamerell/mixtok-service/blob/56caa9e3b33c7b86ecfcc6bfbf4be59dc17fa799/MixTok/wwwroot/index.html) offered:

- **Sorting:** view count, recency, or MixTok Rank.
- **Filters:** game, channel, language, clip age, minimum views, live status, and partnered status.
- **HypeZone:** Apex, Fortnite, PUBG, Black Ops 4, and Rainbow Six.
- **Results:** thumbnails, playback, channel links, and share links, plus a count of indexed clips and channels.

There was also a documented REST API for the same search. You could combine filters, like recent clips from live, non-partnered channels, as shown in the [API examples](https://github.com/QuinnDamerell/mixtok-service/blob/56caa9e3b33c7b86ecfcc6bfbf4be59dc17fa799/MixTok/wwwroot/apidoc.html).

[MixTok Rank](https://github.com/QuinnDamerell/mixtok-service/blob/56caa9e3b33c7b86ecfcc6bfbf4be59dc17fa799/MixTok/Core/ClipMine.cs) balanced popularity with freshness: a clip's view-based score dropped as it aged. Every clip counted as at least ten minutes old, so brand-new clips couldn't rocket to the top with extreme scores.

</details>

## Further Reading & Media

<details class="qd-story-details" markdown="1">
<summary>Explorer, API guide, and ranking source</summary>

- [ClipMine explorer](https://github.com/QuinnDamerell/mixtok-service/blob/56caa9e3b33c7b86ecfcc6bfbf4be59dc17fa799/MixTok/wwwroot/index.html) — the original search interface, clip player, and index statistics.
- [ClipMine API documentation](https://github.com/QuinnDamerell/mixtok-service/blob/56caa9e3b33c7b86ecfcc6bfbf4be59dc17fa799/MixTok/wwwroot/apidoc.html) — filter descriptions and example searches.
- [MixTok ranking and filtering](https://github.com/QuinnDamerell/mixtok-service/blob/56caa9e3b33c7b86ecfcc6bfbf4be59dc17fa799/MixTok/Core/ClipMine.cs) — the age-adjusted popularity score and search implementation.

</details>
