# Mixer Karl

A social bot that helped Mixer viewers find, message, and summon each other across channels.

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| 2019    | Retired      | [GitHub](https://github.com/QuinnDamerell/mixer-carl) |

## The story {#description}

Karl listened to Mixer.com's public firehose API, which streamed every chat message and presence update on the site. That meant he could keep track of users and help people find or summon each other across channels.

Some streamers loved Karl. Others, well, found him irritating. He was eventually disabled, and Mixer.com shut down not long afterward.

## Commands and Friends

<details class="qd-story-details" markdown="1">
<summary>Karl's commands, friends, and lurk mode</summary>

The bot introduced itself as “Karl” and credited `@Quinninator` and `@BoringNameHere`. You could send him caret-prefixed commands like `^find`, or talk to him in a private whisper. He could find people, relay messages across channels, and summon someone with a link to your channel. His help text, personality and all, is still in the [command code](https://github.com/QuinnDamerell/mixer-carl/blob/bbfa77bdece3726ad35ff0156e5fde11bed1f6c4/Carl/Dan/CommandDan.cs).

Friend lists let Karl tell you when friends were active and which channels they were watching. If you wanted to slip in quietly, `^lurk` stopped him from announcing your arrival. And before a regular user could summon someone, Karl checked the recipient's friend list first. It's all still in the [friend and presence code](https://github.com/QuinnDamerell/mixer-carl/blob/bbfa77bdece3726ad35ff0156e5fde11bed1f6c4/Carl/Dan/FriendlyDan.cs).

</details>

## Further Reading & Media

<details class="qd-story-details" markdown="1">
<summary>Karl's original commands and friend-list code</summary>

- [Karl's commands and introduction](https://github.com/QuinnDamerell/mixer-carl/blob/bbfa77bdece3726ad35ff0156e5fde11bed1f6c4/Carl/Dan/CommandDan.cs) — finding, whispering, summoning, and the original creator credits.
- [Friends and lurk mode](https://github.com/QuinnDamerell/mixer-carl/blob/bbfa77bdece3726ad35ff0156e5fde11bed1f6c4/Carl/Dan/FriendlyDan.cs) — friend-list controls and activity notifications.

</details>
