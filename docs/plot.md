# Plot

Story games, mysteries, and escape rooms where every friend's browser holds a piece of the adventure.

[Visit Plot :material-arrow-top-right:](https://plot.game/){ .md-button .md-button--primary }

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| 2026    | Active      | None      |

## The story {#description}

I built Plot for game nights, whether friends are in the same room or across the world. The host picks a game and shares a link. Everyone joins in their browser, with nothing to install.

Games take 2 to 30 minutes. Many give each player a different piece of the puzzle, so talking it through is part of winning.

## How It Works

### One Link To Play

The host chooses a game from their library and creates a party. Friends join through one link, with no app or account required.

### Realtime Parties

Moves, guesses, and story beats stay in sync across devices. Games support 2 to 64 players, depending on the game.

### Player Profiles

Each player gets an anonymous profile with a name, icon, and color. They can claim it with an email magic link, and Plot tracks achievements along the way.

## Games

### Game Library

The library has 11 games in four categories: escape rooms, mysteries, story games, and quick play. A taste:

- **The Missing Minute:** a free four-player mystery. Each stranger remembers part of a lost minute; the truth emerges when they compare notes.
- **Thereabouts:** free realtime guessing for up to 64 players. One player gives a one-word clue, and everyone watches the guesses move live.
- **Exit Interview:** a co-op escape room set on your final day at Halcyon Labs.
- **Signal Lost:** a voice-optional mystery about an abandoned radio tower broadcasting four versions of the same warning.

Some games can use your microphone or camera, but Plot always asks for permission first.

### Buy Once, Replay Anytime

Some games are free; others are a one-time purchase with unlimited replays. Only the host needs to own the game. Friends always join free.

## Building Games for Plot

<details class="qd-story-details" markdown="1">
<summary>How the platform and SDK work</summary>

A Plot game is a browser app built with HTML, CSS, and JavaScript or TypeScript. Creators can use a web framework or a game engine that exports to the browser. Plot runs a copy on each device, letting players see different roles, clues, or controls while sharing progress. The [creator guide](https://docs.plot.game/manual/how-plot-games-work.html) explains what the game handles and what the platform takes care of.

The SDK provides player identities, shared game state, individual player data, live messages, and a common clock. Its [recovery system](https://docs.plot.game/manual/lifecycle-and-recovery.html) restores session state after ordinary reconnects and reloads.

The optional [synchronized-audio toolkit](https://docs.plot.game/toolkit/synced-audio.html) coordinates sound cues and looping ambience across devices. It can also catch a late-loading player up to the current point in a track.

</details>

## Further Reading & Media

<details class="qd-story-details" markdown="1">
<summary>Developer guides, SDK, and examples</summary>

- [Build Games Where Everyone Has A Part](https://docs.plot.game/) — Plot developer documentation. Guides and examples covering multiplayer game design, shared state, players, realtime events, and synchronized audio.
- [Plot browser SDK](https://www.npmjs.com/package/@plot.game/sdk) — npm, first published September 2026. The official `@plot.game/sdk` package, maintained by Quinn Damerell, with its release history.
- [How Plot games work](https://docs.plot.game/manual/how-plot-games-work.html) — the creator format, individual player views, and shared session state.
- [Lifecycle and recovery](https://docs.plot.game/manual/lifecycle-and-recovery.html) — how games recover from reloads and connection interruptions.
- [Synced audio](https://docs.plot.game/toolkit/synced-audio.html) — shared sound cues, looping ambience, and playback recovery.

</details>
