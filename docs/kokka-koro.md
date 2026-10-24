# Kokka Koro

A Machi Koro-style arena where Python and C# bots compete for the top spot.

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| 2019    | Retired      | [GitHub](https://github.com/QuinnDamerell/KokkaKoro) |

## The story {#description}

Players wrote bots with an SDK, uploaded them, and watched them battle it out over multiple rounds, with results tracked on a scoreboard. The whole thing ran on Azure App Service.

I built it during nap times while on leave with my infant twins, in the midst of the COVID lockdowns. There wasn't much else to do, so the bots got a board game.

## Building and Competing With Bots

<details class="qd-story-details" markdown="1">
<summary>Bot strategy, uploads, and tournaments</summary>

The [participant instructions](https://github.com/QuinnDamerell/KokkaKoro.TemplateBot) include a starter bot and working RandomBot example. Developers implement a strategy, compile it, and upload it with the Service Utility Tool.

Each move request includes the board state and available actions. A bot decides:

- How many dice to roll, and whether to accept the result.
- Which building to buy.
- Whom to collect a TV Station payout from.
- Which buildings to exchange through the Business Center.

The [annotated bot template](https://github.com/QuinnDamerell/KokkaKoro.TemplateBot/blob/928ef62037feb514d89493c27c2538fc07e029a6/KokkaKoroBotTemplate/LogicCore.cs) explains each decision and its helper methods.

The [original homepage source](https://github.com/QuinnDamerell/KokkaKoro/blob/22e0f266f3b689fc8391fafaf78265ad2297f32b/GameService/Pages/Index.cshtml) shows what the leaderboard tracked: wins, losses, and win percentages, plus recent games and official tournaments. Tournament progress and elapsed time helped everyone compare strategies across repeated matches.

</details>

## Further Reading & Media

<details class="qd-story-details" markdown="1">
<summary>Starter bot, strategy guide, and leaderboard source</summary>

- [Kokka Koro TemplateBot](https://github.com/QuinnDamerell/KokkaKoro.TemplateBot) — Quinn Damerell / GitHub, 2019. Original participant instructions and a separate starter repository for building, compiling, and uploading a bot, including a working RandomBot example.
- [Annotated bot strategy template](https://github.com/QuinnDamerell/KokkaKoro.TemplateBot/blob/928ef62037feb514d89493c27c2538fc07e029a6/KokkaKoroBotTemplate/LogicCore.cs) — the game's decision points, available actions, and board-state helpers.
- [Leaderboard and tournament homepage](https://github.com/QuinnDamerell/KokkaKoro/blob/22e0f266f3b689fc8391fafaf78265ad2297f32b/GameService/Pages/Index.cshtml) — original interface source preserving rankings and match statistics.

</details>
