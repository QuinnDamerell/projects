# Gathr

Drop a meetup on a map, invite friends, and find the organizer.

## Facts

**Created By: Quinn Damerell, Tyler Reid & Bryan Ehrlich**

| Documented by | Platform | Code |
| ------------- | -------- | --------- |
| February 2012 | Android and a server back-end | Recovered from my backup; unpublished |

## The story {#description}

Tyler, Bryan, and I built Gathr's Android app and server back-end over three months. Friends could place an event on a map, send meetup invitations, and see the organizer's current location. It was made for spontaneous plans, as Bryan recalls in his [project portfolio](media/bryanehrlich-project-portfolio-2026.md).

Gathr won first place in an ACM Google coding competition! My old portfolio site mentions the award, but not what year the competition was or when the app was released.

Both the Android and server code turned up in my project backup. Digging through it, the app let you set a meetup's start and end time, invite friends, change your RSVP, and post to the event's message board.

## Original Artwork

The original banner and architecture diagram survived too. The diagram shows the Android app talking to a Java/MySQL server over SSL, with separate notification and cleanup components.

![Original Gathr banner with blue figures gathered around the name](./assets/gathr/original-banner.png){: style="max-width:728px; width:100%;" loading="lazy"}

<details class="qd-story-details" markdown="1">
<summary>The original system diagram</summary>

![Gathr architecture diagram showing Android, its service helper, SSL, the Java and MySQL server, notifications, and a thread cleaner](./assets/gathr/system-diagram.png){: style="max-width:720px; width:100%; background:white;" loading="lazy"}

</details>

## Original Record

You can see Gathr and its award on my [February 2012 portfolio](assets/media/quinndamerell-homepage-2012/site/_captures/20120213160132-X47AU36R.html), and the rest of that old site lives on in the [full website archive](media/quinndamerell-homepage-2012.md).

## Further Reading & Media

- [Bryan Ehrlich's portfolio](media/bryanehrlich-project-portfolio-2026.md) — A co-creator's account of Gathr's map, meetup invitations, location sharing, and ACM Google competition win, alongside CrossTxT and PurdueBus.
