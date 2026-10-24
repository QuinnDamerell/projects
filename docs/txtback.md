# TxTBack

An anonymous text-message conversation with a stranger, inspired by early Omegle.

## Facts

| Created | Status | Code |
| ------- | ------- | --------- |
| 2009    | Retired     | Recovered from my backup; unpublished |

## The story {#description}

Text one number, get matched with a stranger, and keep talking until one of you decides to switch. That was TxTBack, which my [old project index](assets/media/quinndamerell-homepage-2011/site/projects.html) calls my first major public project. Its Java server ran from my Purdue dorm room.

Reddit brought in a wave of users, but Google Voice rate limits eventually took it down. Back then, the other option was an expensive SMS API service.

## How It Worked

<details class="qd-story-details" markdown="1">
<summary>Matching, commands, and carrier quirks</summary>

When it relaunched in January 2010, TxTBack worked in the United States and was free, apart from your carrier's texting charges. Your first text got instructions back, and you joined the queue by sending `start`. When you were matched, you both got a connection notice, and your phone numbers stayed hidden from each other. I explained all this in the [Reddit discussion](media/reddit-txtback-relaunch-2010.md#comment-c0jbw70).

Here are the commands, from my [Reddit explanations](media/reddit-txtback-relaunch-2010.md#comment-c0jc4hf) and the [forum FAQ](https://web.archive.org/web/20100129212416/http://forum.txtback.mobi:80/feed.php):

| Command | What it did |
| ------- | ----------- |
| `start` | Joined the queue or connected with another participant. |
| `stop` | Left the queue or ended the conversation. |
| `status` | Returned service statistics. |
| `help` | Explained the commands. |
| `menu` | Returned instructions for Purdue dining-court menus for the next meal. |

There were plenty of carrier quirks. As I explained in an [MMS reply](media/reddit-txtback-relaunch-2010.md#comment-c0jc404), Verizon users could send longer texts by MMS, but pictures and videos weren't forwarded. The forum FAQ warned that messages over 160 characters might not arrive and messages could show up out of order, and it noted that the anti-spam limit had been loosened so you could send several short messages in a row. AT&T sometimes replied from changing numbers, which split the conversation on your phone. Every new carrier needed its own work and volunteer testing.

</details>

## Relaunch & Early Community

<details class="qd-story-details" markdown="1">
<summary>120 people, a relaunch, and “Down But Kicking”</summary>

In my [January 24, 2010 announcement](media/reddit-txtback-relaunch-2010.md), I mentioned that the previous week's attempt had pulled in more than 120 people in three hours before the service went down. The replies are a mix of successful chats and messages that went unanswered.

The [forum feed](https://web.archive.org/web/20100129212416/http://forum.txtback.mobi:80/feed.php) tells the rest: a January 23 overhaul announcement, the January 24 relaunch, and a January 25 outage update titled “Down But Kicking,” which blamed an outside service and mentioned a possible fix.

The relaunch thanked Jordan for web design, Ben for testing and moderation, Casey for ideas and help, and Reddit users `panguin` and `infinatespirals` for testing other carriers. By [January 27](https://web.archive.org/web/20100127181720/http://forum.txtback.mobi:80/), the forum had 10 registered members, eight topics, and 17 posts.

</details>

## Screenshots

![TxTBack website](./assets/txtback/TxTBack.png){: style="height:160px;"}

## Further Reading & Media

<details class="qd-story-details" markdown="1">
<summary>Launch threads, forum records, and original portfolio</summary>

### Launch & Community

- [Dear Reddit I give you TxtBack, like Omegle a free and fun text messaging service I made for you :)](media/reddit-txtback-relaunch-2010.md) — Quinn on Reddit, January 24, 2010. The relaunch announcement preserves early users' conversations, questions, and troubleshooting, along with Quinn's replies.
- Quinn's replies about [joining and leaving the queue](media/reddit-txtback-relaunch-2010.md#comment-c0jbw70), [status and help commands](media/reddit-txtback-relaunch-2010.md#comment-c0jc4hf), and [MMS limitations](media/reddit-txtback-relaunch-2010.md#comment-c0jc404) — Reddit, January 2010. Direct links to the original operational explanations.
- [How pairing worked](media/reddit-txtback-relaunch-2010.md#comment-c0jcd8b) — `tsujiku` on Reddit, January 2010. Explains the queue and the notification sent to both participants when matched.
- [TxtBack official forums](https://web.archive.org/web/20100127181720/http://forum.txtback.mobi:80/) — Internet Archive capture dated January 27, 2010. The original community homepage preserves the announcements, help, feedback, and general discussion boards.
- [Forum announcements, FAQ, and early replies](https://web.archive.org/web/20100129212416/http://forum.txtback.mobi:80/feed.php) — TxtBack forum feed, January 23–25, 2010; Internet Archive capture dated January 29, 2010. The archived XML feed preserves Quinn's relaunch and outage updates, acknowledgments to early helpers, user replies, and a FAQ describing a Purdue dining-menu feature.

### Project History

- [TxtBack on Quinn's original project portfolio](https://web.archive.org/web/20110116092658/http://www.quinndamerell.com:80/projects.php) — Quinn Damerell, Internet Archive capture dated January 16, 2011. A contemporary first-party description links the original txtback.mobi website and explains the Java server running from Quinn's dorm room.

</details>
