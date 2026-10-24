# CrossTxT

Your phone’s text messages, with a full-size keyboard. An early adventure in browser-based texting.

## Facts

**Created By: Quinn Damerell & Bryan Ehrlich**

| Created | Status | Domain |
| ------- | ------- | --------- |
| 2010    | Retired | CrossTxT.com |

## The story {#description}

Bryan Ehrlich and I built CrossTxT to move Android texting into the browser. It sent messages from your own phone number, kept the phone and web inboxes in sync, and backed up messages automatically. And it worked from any computer with an internet connection.

New texts triggered a desktop pop-up within seconds, and you could reply right in the notification. The website let you start and browse conversations just like you would on the phone.

Under the hood, it was PHP and MySQL on the server and Java on Android.

## The original notification sound

This little alert used to announce a new text in the browser. The original MP3 survived in my backup, along with the web page that played it.

<audio class="qd-original-audio" controls preload="none" aria-label="Original CrossTxT message notification">
  <source src="assets/crosstxt/alert.mp3" type="audio/mpeg">
  <a href="assets/crosstxt/alert.mp3">Download the notification sound</a>.
</audio>

[Download the original alert](assets/crosstxt/alert.mp3){: download="crosstxt-alert.mp3"}

## Sale

At the end of 2011, Bryan and I sold CrossTxT (the app, back-end, website, and domain) to Spider Web Design for $5,000. As I remember it, the buyer was a developer from Chicago. According to my [original portfolio](media/quinndamerell-homepage-2012.md), we both kept working on the website and Android app after the sale.

## Screenshots

![Main Menu](./assets/crosstxt/texting_large.png){: style="height:200px;"}
![Main Menu](./assets/crosstxt/main_large.png){: style="height:200px;"}
![Main Menu](./assets/crosstxt/Settings_large.png){: style="height:200px;"}
![Main Menu](./assets/crosstxt/Signin_large.png){: style="height:200px;"}

<details class="qd-story-details" markdown="1">
<summary>Inside the beta &amp; what happened next</summary>

## Features & Beta Experience

To join the closed beta in May 2011, you needed Android 2.2 or newer. The [signup page](https://web.archive.org/web/20110515070859/http://www.crosstxt.com:80/betasignup.php) asked for your phone model, Android version, and roughly how many texts you sent a month, and selected testers got an email invitation.

Setup imported your contacts and let you choose how many existing text messages to sync. The website worked in any browser, with no desktop program to install and no need to be on the same Wi-Fi. Chrome was optional; you only needed it for pop-up notifications. El Androide Libre’s [May 2011 walkthrough](media/elandroidelibre-crosstxt-2011.md) mentions a then-recent fix for accented characters, and Android Police’s [hands-on review](media/androidpolice-crosstxt-review-2011.md) shows off contact autocomplete and a conversation list beside the active thread.

The [original tutorial](https://web.archive.org/web/20110518025523/http://crosstxt.com:80/newuser/tutorial.php) explained the message statuses: waiting for the phone, sent, received, or failed. If a message failed, you just clicked it to try again. An old Android settings screenshot also shows options for starting after a reboot, automatic or manual contact sync, and a stop-service button.

Our [May 2011 privacy page](https://web.archive.org/web/20110516043705/http://www.crosstxt.com:80/privacy.php) described encrypting contacts and messages with AES-128, unlocked with your password. That's how we described the security design back then.

In Android Police’s developer Q&A, we talked about a paid Gold edition with multipart SMS and MMS to help cover server costs. Message search was in the works, and we were considering requests for a desktop client and contact photos. Those were our plans during the beta, and I can't confirm which ones actually shipped. [Read the Q&A](media/androidpolice-crosstxt-review-2011.md#app-feedback).

## Early Reception & App History

The original store description mentioned hundreds of beta requests, and Android Police and El Androide Libre each gave away 50 invitations in May 2011. [AppBrain’s store record](https://www.appbrain.com/app/crosstxt-sms-from-computer/com.lozingo.crosstxt) lists version 0.2.2 on May 29 and 0.2.5 on June 8, 2011, then, after the sale, 5,000 installs in May 2012 and 10,000 in February 2013. The app was removed from Google Play on October 13, 2013.

The old user reviews praise its reliability and how nice it was to type on a computer, alongside complaints about getting into the beta and, later, missing updates. In February 2012, one user even made [a custom Firefox theme](https://userstyles.org/styles/61576/gir-s-platinum-crosstxt-theme) to restyle the website’s gradients and shadows.

</details>

<details class="qd-story-details" markdown="1">
<summary>Reviews, original websites &amp; source notes</summary>

## Further Reading & Media

### Articles & Research

- [CrossTxT Bridges the Gap Between Phone and Computer for Easy Texting — Regardless of Browser](media/androidpolice-crosstxt-review-2011.md) — Android Police, May 22, 2011. Abhiroop Basu's review includes setup screenshots, a Texty comparison, and a developer Q&A.
- [Tu ordenador y tu Android conectados para tus SMS con CrossTxT](media/elandroidelibre-crosstxt-2011.md) — El Androide Libre, May 23, 2011, in Spanish. A hands-on introduction with phone and browser screenshots; the publication also offered readers 50 beta invitations supplied by the CrossTxT team.
- [CrossTxT voor Android: sms’en vanaf je computer](https://www.androidplanet.nl/apps/crosstxt-voor-android-smsen-vanaf-je-computer/) — Android Planet, May 23, 2011, in Dutch. Launch coverage of browser texting, synchronization, and the Chrome extension, with an original promotional image.
- [An energy-efficient framework for ubiquitous phone access](https://onlinelibrary.wiley.com/doi/10.1002/dac.3150) — Yantao Li, Gang Zhou, and Daniel Leong, International Journal of Communication Systems, first published May 11, 2016. The paper's bibliography cites the original CrossTxT Android app as reference 4.

### Community Discussions & Creations

- [CrossTxT discussion in a DeskDroid thread](media/reddit-crosstxt-beta-2011.md#comment-c1pwip5) — Reddit, April 17, 2011. A comment compares CrossTxT's closed beta with DeskDroid, describing desktop alerts, the Chrome extension, and control over synchronized messages and contacts.
- [Using the computer to write SMSs](https://www.howardforums.com/threads/using-the-computer-to-write-smss.1755866/) — HowardForums, February 21, 2012. A community comparison lists CrossTxT among browser-based SMS tools. The text shows up in search results, though the forum page itself may not load.
- [Gir's Platinum CrossTxT theme](https://userstyles.org/styles/61576/gir-s-platinum-crosstxt-theme) — InvaderGir on Userstyles.org, February 27, 2012; updated March 2, 2012. A fan-made Firefox theme for the CrossTxT website, with a preview image of the redesigned interface.

### Original Websites & App History

- [Original closed-beta signup page](https://web.archive.org/web/20110515070859/http://www.crosstxt.com:80/betasignup.php) — CrossTxT, Internet Archive capture dated May 15, 2011. Preserves the Android requirements and questions asked of prospective testers.
- [Lozingo Software](https://web.archive.org/web/20110516184237/http://www.lozingo.com:80/) — Original company website, Internet Archive capture dated May 16, 2011. The homepage credits Quinn Damerell and Bryan Ehrlich and links their CrossTxT and PurdueBus projects.
- [Original privacy page](https://web.archive.org/web/20110516043705/http://www.crosstxt.com:80/privacy.php) — CrossTxT, Internet Archive capture dated May 16, 2011. The team's contemporary explanation of contact and message encryption.
- [The unfinished beta FAQ](https://web.archive.org/web/20110516043648/http://www.crosstxt.com:80/faq.php) — CrossTxT, Internet Archive capture dated May 16, 2011. A brief, playful placeholder explains that Quinn and Bryan were still busy building the service.
- [CrossTxT new-user tutorial](https://web.archive.org/web/20110518025523/http://crosstxt.com:80/newuser/tutorial.php) — Original CrossTxT website, Internet Archive capture dated May 18, 2011. The original onboarding instructions explain the Chrome extension, starting conversations, and message-status indicators.
- [CrossTxT on Facebook](https://www.facebook.com/CrossTxT/) — Official project page, 2011. Our beta-era development updates show up in search results, though Facebook may ask you to sign in to see the page.
- [MightyText's contemporary compatibility list](https://mightytext-sms-from-computer.soft112.com/) — MightyText publisher description preserved by Soft112, version 0.72 dated August 31, 2011. Lists CrossTxT among apps tested alongside MightyText on a Nexus One running Android 2.3.
- [CrossTxT: Welcome to the Texting Revolution](media/crosstxt-homepage-2011.md) - Original CrossTxT website, Internet Archive capture dated October 28, 2011. The original landing page presents inbox synchronization, SMS backup, and desktop texting.
- [CrossTxT – SMS from Computer](https://www.appbrain.com/app/crosstxt-sms-from-computer/com.lozingo.crosstxt) — AppBrain, 2011–2013 store history. Preserves the original app description and developer credits, release milestones, and user reviews. The record spans the original team's work and the period after the sale.
- [CrossTxT on Quinn's original portfolio](assets/media/quinndamerell-homepage-2012/site/crosstxt/index.html) — Quinn Damerell, Internet Archive capture dated July 3, 2015. A preserved first-party description of the architecture, desktop notifications, and original Android screenshots.
- [Bryan Ehrlich's project portfolio](media/bryanehrlich-project-portfolio-2026.md) — Bryan Ehrlich, undated. The co-creator's account of CrossTxT includes a link to the original website's 2011 archive.

### Historical Images

- Android Police's original [Android setup screenshot 1](https://static0.anpoimages.com/wordpress/wp-content/uploads/2011/05/screenshot_1.png), [screenshot 2](https://static0.anpoimages.com/wordpress/wp-content/uploads/2011/05/screenshot_3.png), [screenshot 3](https://static0.anpoimages.com/wordpress/wp-content/uploads/2011/05/screenshot_8.png), and [settings screenshot](https://static0.anpoimages.com/wordpress/wp-content/uploads/2011/05/screenshot_11.png) — May 22, 2011.
- Android Police's [web conversation screenshot](https://static0.anpoimages.com/wordpress/wp-content/uploads/2011/05/testing-message.png), [desktop notification](https://static0.anpoimages.com/wordpress/wp-content/uploads/2011/05/notification.png), and [review header image](https://static0.anpoimages.com/wordpress/wp-content/uploads/2011/05/images_thumb1.jpg) — May 22, 2011.
- [Android Planet's CrossTxT image](https://www.androidplanet.nl/wp-content/uploads/2011/05/crosstxt-android1.jpg) — Illustration accompanying its May 23, 2011 article.
- [El Androide Libre's article image](https://s2.elespanol.com/2015/03/15/elandroidelibre/el_androide_libre_18258649_179328925_1706x960.jpg) — Image accompanying its May 23, 2011 article, preserved on the publication's current image host.
- [Gir's Platinum theme preview](https://userstyles.org/style_screenshots/61576_after.png) — InvaderGir, 2012. The full-size preview linked from the fan-made theme's listing.

</details>
