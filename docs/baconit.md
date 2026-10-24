# Baconit

Reddit, with a Windows Phone twist. A swipe, a sync, and the occasional April Fools surprise.

## Facts

| Created | Status | Code | Subreddit |
| ------- | ------- | --------- | --------- |
| 2011    | Retired | [GitHub](https://github.com/QuinnDamerell/Baconit) | [Subreddit](https://www.reddit.com/r/baconit/) |

## The story {#description}

I built Baconit as a full-featured Reddit app for Windows Phone, and it held the Windows Phone Store’s top rating for a long time. It had a Metro interface, Flip View, BaconSync, and a fast Markdown renderer.

The original Windows, Windows Phone, and Xbox releases are no longer maintained, but community versions carry on. NLogDEV’s [Baconit Extended](https://store.live.net.co/app/121), for example, adds Reddit galleries, newer video and GIF playback, and fixes for older Windows Phone devices.

### Key Features

#### Flip View

Flip View made Baconit the first Reddit app with horizontal, one-post-at-a-time browsing. Open any subreddit, swipe through full-screen posts, and jump straight to the comments.

<figure class="product-capture product-capture--phone">
  <a href="assets/baconit/3.0/3.png"><img class="no-lightbox" src="assets/baconit/3.0/3.png" alt="Original Baconit 3.0 Flip View screenshot displaying a Reddit post about the Giant’s Causeway" width="768" height="1280" loading="lazy" decoding="async"></a>
  <figcaption>Flip View in Baconit 3.0. An original Windows Phone screenshot from the project archive.</figcaption>
</figure>

<details class="qd-story-details" markdown="1">
<summary>BaconSync, live tiles &amp; the Markdown engine</summary>

#### BaconSync

BaconSync kept visited Reddit links in sync across desktop browsers and phones, for free, so you could instantly see what you’d already read. It also sent a web page straight from the browser to Baconit.

I made the official Chrome extension, Pradeek J. made the Firefox one, and Ivan Kiselovs made the Opera one, as the [original BaconSync page](assets/media/quinndamerell-homepage-2012/site/baconit/baconsync/index.html) credits. Other extension and Reddit-app developers were invited to plug in through its API.

#### Smart Bar, Subscriptions & Live Tiles

The **Smart Bar** took a subreddit name, Reddit URL, or search term. Subscriptions could stay on the phone or sync to a Reddit account. You could pin the app, a subreddit, or a single story to Start, with custom tile images and info. First-use hints explained the touch targets and gestures. The [February 2012 review of version 1.5](media/allaboutwindowsphone-baconit-review-2012.md) covers all of these.

My [version 1.6 announcement](https://forums.windowscentral.com/threads/free-app-baconit-a-metro-reddit-app.187178/) also lists an auto-updating inbox, unread-message and karma tiles, endless subreddit scrolling, image submissions, saved and hidden stories, and live formatting previews for posts.

#### Microsoft Band

Version 4.3 brought Reddit to the Microsoft Band’s wallpaper, using pictures from a chosen subreddit. It also added profiles with karma, account anniversaries, Reddit Gold status, and sortable post and comment histories. [Windows Central’s December 2015 report](https://www.windowscentral.com/baconit-nabs-user-profiles-sorting-and-more-latest-update) has the full release notes.

#### Universal Markdown

When I built Baconit, XAML apps had no Markdown renderer. Reddit comments needed one, so I wrote Universal Markdown, an efficient parser and renderer. Every comment used its control inside a virtualized list, so performance really mattered.

The Windows Community Toolkit team later asked to include Universal Markdown. I was happy to contribute it.

[Universal Markdown on GitHub](https://github.com/QuinnDamerell/UniversalMarkdown)

[Markdown in the Windows Community Toolkit](https://github.com/CommunityToolkit/WindowsCommunityToolkit/tree/main/Microsoft.Toolkit.Uwp.UI.Controls.Markdown)

The Windows 10 rewrite added a full-screen editor, Markdown helpers, and live previews for posts, comments, and messages. In the [January 2016 version 4.7 announcement](media/reddit-baconit-editing-2016.md), I explained how previews adapted to device speed: slower phones waited for a typing pause so long posts would not slow the keyboard.

</details>

### April Fools
On April 1st, Baconit staged a convincing Windows Phone shutdown and reboot, complete with a “failed bootloader.” The fake screens matched the OS exactly. The app then revealed the joke on screen. A little mischief, with no actual reboot.

<figure class="product-capture">
  <a href="assets/baconit/april-fools-system-error.png"><img class="no-lightbox" src="assets/baconit/april-fools-system-error.png" alt="Nokia Windows Phone resting on autumn leaves and displaying Baconit's fake System Error message" width="682" height="583" loading="lazy" decoding="async"></a>
  <figcaption>The fake “System Error” message from Baconit’s April Fools’ prank.</figcaption>
</figure>

[The prank’s Reddit thread](media/reddit-baconit-april-fools-2013.md)

## Awards

Baconit won People’s Choice in Microsoft’s Big App on Campus competition for college students, sending Marilyn and me to South by Southwest in Austin, Texas. According to my [April 2012 portfolio](media/quinndamerell-homepage-2012.md), I spent about three months building it before entering, and it made it through three voting rounds to take the most votes in the free-app division. The prize included the SXSW Music 2012 trip and a cash award.

Baconit also won **2012 App of the Year** in the Community App Awards for Windows Phone, as my [November 2012 product page](assets/media/quinndamerell-homepage-2012/site/_captures/20121129203450-AMUY7X4S.html) notes.

<details class="qd-story-details" markdown="1">
<summary>Versions, community &amp; life on Xbox</summary>

### Major Versions

- 1.0 for Windows Phone 7.5: Original C# Silverlight version
- 2.0: A Windows Phone 7.5 (Mango) release, already shown on the [May 2012 product page](assets/media/quinndamerell-homepage-2012/site/_captures/20120501190612-D5LFX4OT.html)
- 2.5: Windows Phone 8 support, shown in the [November 2012 walkthrough](media/youtube-windows-central-baconit-wp8-2012.md)
- 3.0: A big update for Windows Phone 8
- 4.0 Windows 10 (Universal Windows Platform): Final rewrite as a Universal Windows App running on Windows 10, Windows Phone, HoloLens, and Xbox

### Community & Development

The free and donation editions started out with the same features. When version 3.0 arrived in April 2014, both stayed ad-free, and donation users also got an **Early Access** app to try upcoming changes. That release also added an option to hide stories you'd already read. [Windows Central’s version 3.0 coverage](https://www.windowscentral.com/baconit-updated-version-3) has the details.

On Xbox One, the PC interface gained a controller-operated pointer: left stick to move, right stick to scroll, triggers to zoom. Replies, system notifications, GIFs, YouTube, galleries, and the in-app browser all worked. By my count at the time, it took just three code changes and a few manifest changes, since 99% of the code was shared across phone, tablet, desktop, HoloLens, and Xbox. The [July 2016 hands-on](media/windowscentral-baconit-xbox-hands-on-2016.md) also points out the preview’s rough edges: the image-saving and clipboard commands showed up but didn't work on the console.

Baconit even made it to **Everest Base Camp**. In May 2012, Windows Central reported that student Minesh Mandalia used it on the Lumia 800 he took on the trip. The [article includes his photographs](https://www.windowscentral.com/skydiving-enthusiast-takes-lumia-800-mt-everest).

</details>

<details class="qd-story-details" markdown="1">
<summary>Press coverage &amp; video reviews</summary>

## Press

### Videos

**[Windows Central - Baconit Review](media/youtube-windows-central-baconit-windows-10-2015.md)**
![type:video](https://projects-storage.quinn.space/baconit-windows-central-review.mp4)
[YouTube Source](https://www.youtube.com/watch?v=dfo1W8beIXc)

**[WMPoweruser.com - WP7 App Review: Baconit](media/youtube-wmpoweruser-baconit-review-2012.md)**

![type:video](https://projects-storage.quinn.space/baconit-wp7-review.mp4)
[YouTube Source](https://www.youtube.com/watch?v=FIcTZlR4nNg)

**[Windows Central - Baconit for Windows Phone 8](media/youtube-windows-central-baconit-wp8-2012.md)**
![type:video](https://projects-storage.quinn.space/baconit-wp8-review.mp4)
[YouTube Source](https://www.youtube.com/watch?v=qAwL_fWz5wc)

### Articles
- Microsoft Student blog - [Meet Microsoft Developer Quinn Damerell](media/microsoft-student-blog-2012.md)
- Microsoft Devices Blog - [Quinn Damerell: App developer bringing home the Baconit](media/windows-blog-baconit-2012.md)
- WinSource - [WinSource Interview: Quinn Damerell of Baconit](media/winsource-baconit-2012.md)
- Windows Phone Blog - [Crowning the "Big App on Campus": Meet 4 fantastic student-made apps](media/windows-phone-blog-big-app-on-campus-2012.md)
- Windows Central - [Baconit for Reddit gets rewritten as a stunning universal Windows 10 app](media/windowscentral-baconit-windows-10-2015.md)
- Windows Central - [Baconit arrives on Xbox One Preview, bringing dank Reddit memes to your console](media/windowscentral-baconit-xbox-one-2016.md)
- On MSFT - [Baconit app gets a bunch of new features in major update](media/onmsft-baconit-update-2015.md)
- Windows Central - [Reddit users, your Baconit is here](media/windowscentral-baconit-launch-2011.md)

### Store Listing

- Microsoft — [Baconit on the Windows Phone Marketplace](media/windows-phone-marketplace-baconit-2012.md). The March 2, 2012 listing for version 1.7.0.0, with screenshot thumbnails, early reviews, and a history of other recovered captures.

</details>

<details class="qd-story-details" markdown="1">
<summary>Original demos &amp; release videos</summary>

## Videos

<!-- These are hosted on CloudFlare's R2 object storage since Pages can only take up to 25MB -->
### Baconit Update 4.2.0
![type:video](https://projects-storage.quinn.space/baconit-update-4-2-0.mp4)

### Baconit Update 4.1.12
![type:video](https://projects-storage.quinn.space/baconit-update-4-1-12.mp4)

### Baconit Update 2.1
![type:video](https://projects-storage.quinn.space/baconit-update-2-1.mp4)

### Baconit  Update 1.6
![type:video](https://projects-storage.quinn.space/baconit-update-1-6.mp4)

### BaconSync Announcement
![type:video](https://projects-storage.quinn.space/baconit-baconsync.mp4)

### April Fools Joke
![type:video](https://projects-storage.quinn.space/baconit-april-fools-joke.mp4)

</details>

<details class="qd-story-details" markdown="1">
<summary>Early screenshots from my project backup</summary>

## Early visual history

My old project backup filled in some fun gaps between the release galleries: the oversized home-screen title, a light theme, Smart Bar help, and early image and profile views. I've labeled these six originals with the version folder I found them in, which doesn't necessarily tell us exactly when they were taken or when each feature first appeared.

### Versions 1.2–1.4

The front page from 1.2, the subreddit home from 1.3, and the light theme from 1.4:

![Baconit 1.2 front page with large pivot headings, gray voting arrows, and blue comment links](./assets/baconit/local-backup/1.2-front-page.png){: style="height:200px;" loading="lazy"}
![Baconit 1.3 home screen with a textured Reddit mascot background and large subreddit names](./assets/baconit/local-backup/1.3-home.png){: style="height:200px;" loading="lazy"}
![Baconit 1.4 light theme with starred subreddit shortcuts on a pale background](./assets/baconit/local-backup/1.4-light-theme.png){: style="height:200px;" loading="lazy"}

### Versions 1.5–2.4

Smart Bar help from 1.5, the image viewer from 1.8, and my Reddit profile from the 2.3 and 2.4 folders. Those last two folders had identical screenshots, so the profile view only appears once.

![Baconit 1.5 Smart Bar help explaining instant subreddits, Reddit URL lookup, and search](./assets/baconit/local-backup/1.5-smart-bar.png){: style="height:200px;" loading="lazy"}
![Baconit 1.8 image viewer displaying a long-exposure photograph of Sacramento Tower Bridge](./assets/baconit/local-backup/1.8-image-viewer.png){: style="height:200px;" loading="lazy"}
![Baconit profile showing Quinn's karma, account anniversary, and cake-day countdown, shared by the 2.3 and 2.4 folders](./assets/baconit/local-backup/2.3-2.4-profile.png){: style="height:200px;" loading="lazy"}

</details>

<details class="qd-story-details" markdown="1">
<summary>Baconit 2.5: all eight original screenshots</summary>

## Original 2.5 screenshot set

The backup also had a complete **768 × 1280** set in the 2.5 folder. Red accents run through the front page, comments, profile, and live tiles, while Flip View shows a bird wallpaper and a Windows 8 news article. This is a different promotional set from the smaller [2.5 store gallery](#25-screenshots) below, so I've kept both.

![Baconit 2.5 Reddit front page with red voting arrows, comment links, and thumbnail borders](./assets/baconit/local-backup/2.5/1.png){: style="height:200px;" loading="lazy"}
![Windows Phone 8 Start screen with red wide Baconit live tiles, karma totals, and subreddit pictures](./assets/baconit/local-backup/2.5/2.png){: style="height:200px;" loading="lazy"}
![Bird wallpaper displayed in Baconit 2.5 Flip View with a red vote and comment bar](./assets/baconit/local-backup/2.5/3.png){: style="height:200px;" loading="lazy"}
![Baconit 2.5 nested comments with red usernames and reply-thread guides](./assets/baconit/local-backup/2.5/4.png){: style="height:200px;" loading="lazy"}
![The Next Web article about the Windows 8 Store displayed inside Baconit 2.5 Flip View](./assets/baconit/local-backup/2.5/5.png){: style="height:200px;" loading="lazy"}
![Quinn's Reddit profile in Baconit 2.5 with red karma totals and a cake-day countdown](./assets/baconit/local-backup/2.5/6.png){: style="height:200px;" loading="lazy"}
![Baconit 2.5 comment details with red up-vote, down-vote, share, profile, and reply buttons](./assets/baconit/local-backup/2.5/7.png){: style="height:200px;" loading="lazy"}
![Baconit 2.5 home screen with starred Baconit, front page, Purdue, and Windows Phone subreddit shortcuts](./assets/baconit/local-backup/2.5/8.png){: style="height:200px;" loading="lazy"}

</details>

<details class="qd-story-details" markdown="1">
<summary>Screenshots &amp; logos through the years</summary>

## Images

Alongside my original project images, some of the sets below came from old Windows Phone Marketplace listings; the [Marketplace archive and capture history](media/windows-phone-marketplace-baconit-2012.md#capture-history) has the details. They're labeled the way the store listed them, and the small store thumbnails are shown at their original size. The two galleries above are the extra originals from my local backup.

### App Logos

![Main Menu](./assets/baconit/logo.png){: style="height:150px;"}
![Main Menu](./assets/baconit/logo-new.jpg){: style="height:150px;"}

### 1.0 Screenshots

![Main Menu](./assets/baconit/1.0/home.png){: style="height:200px;"}
![Main Menu](./assets/baconit/1.0/live-tiles.png){: style="height:200px;"}
![Main Menu](./assets/baconit/1.0/subreddit.png){: style="height:200px;"}
![Main Menu](./assets/baconit/1.0/Comments.png){: style="height:200px;"}
![Main Menu](./assets/baconit/1.0/commentView.png){: style="height:200px;"}

### 1.6–1.7 Screenshots

From the store listings saved February 11 and March 2, 2012. These only survived as tiny 90 × 150 thumbnails.

![Reddit front page with voting controls and post thumbnails — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/48a7d574-5b3c-4a50-850b-c03d99dfb6fe.png){: style="height:150px;" loading="lazy"}
![Windows Phone Start screen with blue Baconit live tiles — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/155f2c3c-e2f4-4166-bacf-97323487cf59.png){: style="height:150px;" loading="lazy"}
![Baconit account menu with messages and karma totals — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/7cfb0ed5-ebf0-4058-aae1-edad24fba7af.png){: style="height:150px;" loading="lazy"}
![Reddit discussion in Baconit’s comments view — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/eb8cf4ab-b20a-49cd-baaf-f91be09ba619.png){: style="height:150px;" loading="lazy"}
![An Imgur photograph open in Baconit’s in-app browser — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/0c62ceaf-2922-45b0-8bdc-65c9b862a2ac.png){: style="height:150px;" loading="lazy"}
![Subreddit manager with account and home checkboxes — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/74f1cde2-239b-44d9-ad9a-6f2d78da5e67.png){: style="height:150px;" loading="lazy"}
![Comment details with voting, reply, and sharing buttons — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/0cd569d2-e99c-442b-bc56-f982fc43c449.png){: style="height:150px;" loading="lazy"}
![Baconit home screen listing subscribed subreddits — 1.6.0.0 and 1.7.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/da56dcb0-ad49-484e-b8ab-0ed6fd058722.png){: style="height:150px;" loading="lazy"}

### 1.9 Screenshots

From the store listings saved April 4 and April 20, 2012, also as 90 × 150 thumbnails.

![Reddit front page with voting controls and post thumbnails — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/48a7d574-5b3c-4a50-850b-c03d99dfb6fe.png){: style="height:150px;" loading="lazy"}
![Windows Phone Start screen with blue Baconit live tiles — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/155f2c3c-e2f4-4166-bacf-97323487cf59.png){: style="height:150px;" loading="lazy"}
![Sacramento Tower Bridge photograph in Baconit Flip View — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/5d9028e5-86d1-4025-a190-5551eaafda77.png){: style="height:150px;" loading="lazy"}
![Baconit account menu with messages and karma totals — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/7cfb0ed5-ebf0-4058-aae1-edad24fba7af.png){: style="height:150px;" loading="lazy"}
![Nested Reddit comments with a highlighted parent comment — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/eb8cf4ab-b20a-49cd-baaf-f91be09ba619.png){: style="height:150px;" loading="lazy"}
![An Imgur photograph open in Baconit’s in-app browser — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/0c62ceaf-2922-45b0-8bdc-65c9b862a2ac.png){: style="height:150px;" loading="lazy"}
![Subreddit manager with account and home checkboxes — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/74f1cde2-239b-44d9-ad9a-6f2d78da5e67.png){: style="height:150px;" loading="lazy"}
![Baconit home screen listing subscribed subreddits — 1.9.0.0](./assets/media/windows-phone-marketplace-baconit-2012/images/da56dcb0-ad49-484e-b8ab-0ed6fd058722.png){: style="height:150px;" loading="lazy"}

### 2.0 Screenshots

![Main Menu](./assets/baconit/2.0/8.png){: style="height:200px;"}
![Main Menu](./assets/baconit/2.0/1.png){: style="height:200px;"}
![Main Menu](./assets/baconit/2.0/3.png){: style="height:200px;"}
![Main Menu](./assets/baconit/2.0/4.png){: style="height:200px;"}
![Main Menu](./assets/baconit/2.0/7.png){: style="height:200px;"}
![Baconit Reddit front page with blue voting arrows and post thumbnails — 2.0.0.0, 2.1.0.0, and 2.2.0.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/13e71cdb-532f-48a1-a89c-a69cecbf0cc6.png){: style="height:200px;" loading="lazy"}

The last image comes from the 2.0.0.0, 2.1.0.0, and 2.2.0.0 Marketplace listings, saved May 6, June 8, and July 9, 2012. It's 432 × 720 pixels, and it's the only one of that listing’s eight screenshots that survived.

### 2.4.1 Screenshots

From the store listing saved November 24, 2012, at 329 × 548 pixels. The image files themselves were saved on October 13, 2015, so they might include changes made after that first listing.

![Baconit Reddit front page with blue voting arrows and post thumbnails — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/bf937da7-e26c-4699-a021-34bc3d63dbf5.png){: style="height:200px;" loading="lazy"}
![Windows Phone Start screen with Baconit and subreddit live tiles — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/0b02a2ed-98b5-4652-a9f2-3a5231043f89.png){: style="height:200px;" loading="lazy"}
![Sacramento Tower Bridge photograph in Baconit Flip View — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/a61c7f61-25a0-405d-871b-0cce408675b0.png){: style="height:200px;" loading="lazy"}
![Nested Reddit comments with a highlighted parent comment — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/ef629fb8-ddfa-4c9c-aa98-fbd0027ef227.png){: style="height:200px;" loading="lazy"}
![Scientific American article open inside Baconit Flip View — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/afd636e5-e1c1-432f-9dc5-c543c67d2472.png){: style="height:200px;" loading="lazy"}
![Quinn’s Reddit profile showing karma totals and account details — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/a1cc241a-5784-4816-a8e8-85e1dcf858cf.png){: style="height:200px;" loading="lazy"}
![Comment details with voting, reply, and sharing buttons — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/2275a1cc-2aaa-4aa3-85f7-49509b7f25c9.png){: style="height:200px;" loading="lazy"}
![Baconit home screen listing subscribed subreddits — 2.4.1.0](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/2d7e06ce-f409-4ce5-b88b-fcc137563c36.png){: style="height:200px;" loading="lazy"}

### 2.5 Screenshots

From store listings saved December 11, 2012, June 6, 2013, April 26, 2014, and July 6, 2015. The listings for 2.5.0.0, 2.6.4.2, 3.0.0.215, and 3.0.1.0 all used the same screenshots. Seven of them match the 2.4.1.0 set, but the Start screen now shows red, wide live tiles. The later listings kept using these older promotional screenshots, which were saved on January 21, 2013, at 329 × 548 pixels.

![Baconit Reddit front page with blue voting arrows and post thumbnails — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/9b51e87f-2277-409e-86f5-5a5cf2aecedc.png){: style="height:200px;" loading="lazy"}
![Windows Phone 8 Start screen with red wide Baconit tiles showing cake day and Reddit posts — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/e137d7a9-d65b-456e-b5e6-40272cb09973.png){: style="height:200px;" loading="lazy"}
![Sacramento Tower Bridge photograph in Baconit Flip View — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/946f5d8e-ede0-472d-911f-ce4c6ed655f6.png){: style="height:200px;" loading="lazy"}
![Nested Reddit comments with a highlighted parent comment — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/867ab857-1b9a-4bbf-93dd-0acdd218524f.png){: style="height:200px;" loading="lazy"}
![Scientific American article open inside Baconit Flip View — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/f1e609f4-c907-43d3-a3c9-d42e25d64b50.png){: style="height:200px;" loading="lazy"}
![Quinn’s Reddit profile showing karma totals and account details — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/f863cc5c-bbc2-41a2-8657-9c16d21d7106.png){: style="height:200px;" loading="lazy"}
![Comment details with voting, reply, and sharing buttons — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/c7b4e7e8-31c1-439c-b78e-fa05323c98bf.png){: style="height:200px;" loading="lazy"}
![Baconit home screen listing subscribed subreddits — 2.5–3.0 listings](./assets/media/windows-phone-marketplace-baconit-2012/recovered-screenshots/1e9eed81-76f0-4468-93b5-3ba69cda2235.png){: style="height:200px;" loading="lazy"}

### 3.0 Screenshots

![Main Menu](./assets/baconit/3.0/8.png){: style="height:200px;"}
![Main Menu](./assets/baconit/3.0/1.png){: style="height:200px;"}
![Main Menu](./assets/baconit/3.0/3.png){: style="height:200px;"}
![Main Menu](./assets/baconit/3.0/4.png){: style="height:200px;"}
![Main Menu](./assets/baconit/3.0/6.png){: style="height:200px;"}

### 4.0 Screenshots

![Main Menu](./assets/baconit/4.0/1.png){: style="height:190px;"}
![Main Menu](./assets/baconit/4.0/2.png){: style="height:190px;"}
![Main Menu](./assets/baconit/4.0/3.png){: style="height:190px;"}
![Main Menu](./assets/baconit/4.0/4.png){: style="height:190px;"}
![Main Menu](./assets/baconit/4.0/5.png){: style="height:190px;"}
![Main Menu](./assets/baconit/4.0/6.png){: style="height:190px;"}
![Main Menu](./assets/baconit/4.0/modern-release-img.png){: style="height:190px;"}

</details>

<details class="qd-story-details" markdown="1">
<summary>More coverage &amp; source notes</summary>

## Further Reading & Media

Coverage, reviews, demos, and historical records from the Windows Phone, Windows 10, and Xbox releases. Links go to the original publishers or to archived copies.

### Features & Reviews

- [Review: Baconit (Reddit Client)](media/allaboutwindowsphone-baconit-review-2012.md) — All About Windows Phone, February 7, 2012. Ewan Spence's review of version 1.5 awards 90% and includes ten early screenshots.
- [Microsoft's Windows Phone student developers: building an ecosystem](media/theverge-windows-phone-students-2012.md) — The Verge, March 29, 2012. Tom Warren's feature includes an interview with Quinn, a portrait, and the story behind Baconit.
- [Skydiving enthusiast takes Lumia 800 to Mt. Everest](https://www.windowscentral.com/skydiving-enthusiast-takes-lumia-800-mt-everest) — Windows Central, May 22, 2012. Photographs and a travel account of Baconit being used on a Lumia 800 at Everest Base Camp.
- [Baconit pays homage to the Blue Screen of Death for its WP8 April Fool's](media/phonearena-baconit-april-fools-2013.md) — PhoneArena, March 31, 2013. Coverage of the simulated shutdown and boot failure prank.
- [Baconit](https://sparetimecode.wordpress.com/2016/02/09/baconit/) — Spare Time Code, February 9, 2016. A developer's assessment of the open-source code becomes a reflection on shipping useful software.
- [Hands on with Baconit for Xbox One, one of Windows 10's best Reddit apps](media/windowscentral-baconit-xbox-hands-on-2016.md) — Windows Central, July 30, 2016. A console hands-on with images, video, and discussion of the shared Windows codebase.
- [Baconit For Windows](https://www.softpedia.com/get/Internet/Other-Internet-Related/Baconit.shtml) — Softpedia, updated May 4, 2018; original publication date unknown. An editorial review of version 4.9.1.0 with an eighteen-image screenshot gallery.

### News & Updates

- [Reddit app Baconit now available internationally](https://www.windowscentral.com/reddit-app-baconit-now-available-internationally) — Windows Central, January 1, 2012. Early coverage of availability outside the United States.
- [Microsoft crowns the winners of the "Big App on Campus" contest](https://www.phonearena.com/news/Microsoft-crowns-the-winners-of-the-Big-App-on-Campus-contest_id28389) — PhoneArena, March 23, 2012. Reports on Baconit's People's Choice award and the finalists' trip to SXSW.
- [Microsoft reveals winners of Windows Phone student app contest](https://www.neowin.net/news/microsoft-reveals-winners-of-windows-phone-student-app-contest/) — Neowin, March 23, 2012. More contest coverage. The text shows up in search results, but I haven't been able to open the article directly.
- [BaconSync Beta for Baconit (try saying it five times fast) in the works](media/windowscentral-baconsync-beta-2012.md) — Windows Central, June 28, 2012. Introduces browser-to-phone synchronization and send-to-phone features.
- [Reddit app Baconit updated to version 2.5 for Windows Phone](https://www.neowin.net/news/reddit-app-baconit-25-updated-for-windows-phone-8/) — Neowin, November 29, 2012. Covers Windows Phone 8 support, Live Tiles, lockscreen integration, NFC, and HD images.
- [Windows Phone 8 apps: BaconIt, Nokia Maps and PhotoBeamer](https://mobilesyrup.com/2012/11/30/windows-phone-8-apps-baconit-nokia-maps-and-photobeamer/) — MobileSyrup, November 30, 2012. Discusses the version 2.5 release. The text shows up in search results, but I haven't been able to open the article directly.
- [Baconit updated to version 3.0, introduces new start experience and more](https://www.windowscentral.com/baconit-updated-version-3) — Windows Central, April 22, 2014. Screenshots of the redesigned start experience and coverage of the Early Access edition.
- [Baconit recieves major update, taking the Reddit client to version 3](https://allaboutwindowsphone.com/flow/item/19705_Baconit_recieves_major_update_.php) — All About Windows Phone, April 22, 2014. Four screenshots accompany a discussion of the free, donation, and Early Access editions.
- [Popular Third-party Reddit Client 'Baconit' For Windows Phone Receives A Big Update](https://onmsft.com/news/popular-third-party-reddit-client-baconit-windows-phone-receives-big-update/) — OnMSFT, April 22, 2014. Additional coverage of version 3.0.0.208.
- [Big Baconit update brings ability to submit posts to any subreddit and much more](https://www.windowscentral.com/baconit-now-lets-you-submit-post-any-subreddit) — Windows Central, December 7, 2015. Version 4.2 release coverage.
- [Baconit nabs User Profiles, Sorting and more in latest update](https://www.windowscentral.com/baconit-nabs-user-profiles-sorting-and-more-latest-update) — Windows Central, December 24, 2015. Covers profiles, sorting, and Microsoft Band wallpaper support in version 4.3.
- [Big Baconit 4.6.5 update brings many changes to memory usage and design](https://www.windowscentral.com/big-baconit-60-update-brings-many-changes-memory-usage-and-design) — Windows Central, January 12, 2016. Performance and interface changes in version 4.6.5.
- [Baconit snags big editing improvements in latest update](https://www.windowscentral.com/baconit-snags-big-editing-improvements-latest-update) — Windows Central, January 14, 2016. Covers editing improvements and accompanying fixes.
- [3rd Party Reddit app wars continue on Windows 10 as Baconit grabs another hefty update](https://onmsft.com/news/3rd-party-reddit-app-wars-continue-windows-10-baconit-grabs-another-hefty-update/) — OnMSFT, January 14, 2016. Another account of the editing update.
- [Baconit snags a new minor update in Windows Store](https://nokiapoweruser.com/baconit-snags-a-new-minor-update-in-windows-store/) — NokiaPowerUser, January 26, 2016. A minor-release report I found through search, though I haven't been able to open the page directly.
- [Baconit, the highly-rated Reddit reader, gets updated with a list of fixes](https://onmsft.com/news/baconit-highly-rated-reddit-reader-gets-updated-list-fixes/) — OnMSFT, June 30, 2016. A maintenance-update report I found through search, though I haven't been able to open the page directly.
- [Baconit, third-party Reddit client, arrives on Xbox for Preview members](https://onmsft.com/news/baconit-third-party-reddit-client-arrives-xbox-preview-members/) — OnMSFT, July 29, 2016. Xbox launch coverage based on Quinn's announcement.

### App Roundups & Personal Impressions

- [What's up with Windows Phone 7's networking performance?](https://www.osnews.com/story/25903/whats-up-with-windows-phone-7s-networking-performance/) — OSnews, May 2, 2012. A positive Baconit mention within a broader platform critique (I confirmed the text through search results).
- [The 25 Best Smartphone Apps Developed By Students](https://www.gettingsmart.com/2012/06/06/the-25-best-smartphone-apps-developed-by-students/) — Getting Smart, June 6, 2012. Baconit appears at number 19 in this syndicated roundup.
- [Best Lumia apps - what's in the Spotlight?](https://blogs.windows.com/devices/2012/11/02/best-lumia-apps-whats-in-the-spotlight/) — Microsoft Devices Blog, November 2, 2012. Features Baconit with an app image and an embedded walkthrough by Quinn.
- [The 50 Best Apps of 2012](https://www.complex.com/pop-culture/a/damien-scott/the-50-best-apps-of-2012) — Complex, December 11, 2012. Baconit ranks 35th.
- [30 days with Windows Phone 8 — Perspective from an admitted iOS addict](https://thenextweb.com/news/30-days-with-windows-phone-8-perspective-from-an-admitted-ios-addict) — The Next Web, December 22, 2012. Baconit appears among the writer's everyday apps (I confirmed the text through search results).
- [Ewan's Windows Phone live tiles layout and applications](https://allaboutwindowsphone.com/features/item/16727_Ewans_Windows_Phone_live_tiles.php) — All About Windows Phone, January 28, 2013. Ewan Spence discusses Baconit within a tour of his own phone and app collection.
- [How does the Windows Phone 8 Kool-Aid Taste?](https://www.spkaa.com/blog/windows-phone-8-review) — SPK and Associates, March 5, 2013. A phone review highlights Baconit's interface and animations.
- [March Apps Madness 2013 – news and entertainment apps](https://blogs.windows.com/devices/2013/03/25/march-apps-madness-2013-news-and-entertainment-apps/) — Microsoft Devices Blog, March 25, 2013. Includes Baconit in an app bracket with an image. The text shows up in search results, but I haven't been able to open the page directly.
- [Digixav Awards 2013](https://digixav.com/2014/01/01/digixav-awards-2013/) — Digixav, January 1, 2014. Baconit is writer Rowan's individual Windows Phone app selection, rather than the site's overall winner.
- [Best social apps for your Windows Phone](https://betanews.com/commentary/best-social-apps-for-your-windows-phone/) — BetaNews, January 13, 2014; updated February 4, 2016. A dedicated Reddit section recommends Baconit and compares it with Readit.
- [10 Windows Phone apps for Design inspiration](https://superdevresources.com/10-windows-phone-apps-for-design-inspiration/) — Super Dev Resources, March 20, 2014; updated October 30, 2020. Selects Baconit as an interface design example and includes a screenshot.
- [4 Days With Windows Phone 8.1](https://bryansiegel.com/2014/04/4-days-windows-phone-8-1/) — Bryan Siegel, April 20, 2014. A personal account praises swiping between Reddit posts (I confirmed the text through search results).
- [50 best apps for Windows Phone](https://blogs.windows.com/devices/2014/10/08/50-best-apps-windows-phone/) — Microsoft Devices Blog, October 8, 2014. Includes a dedicated Baconit entry in an official app roundup.
- [Best Windows apps this week](https://betanews.com/series/best-windows-apps-this-week-41/) — BetaNews, November 20, 2015; updated February 4, 2016. The 155th installment selects Baconit as App of the Week and includes a screenshot.

### International Coverage

- ["Big App on Campus": 4 aplicaciones desarrolladas por estudiantes](https://blogs.windows.com/latam/2012/03/30/big-app-on-campus-4-aplicaciones-desarrolladas-por-estudiantes/) — Microsoft Windows Blog for Latin America, March 30, 2012, in Spanish. A translated contest report includes Quinn's answers about favorite apps and development advice.
- [WP7 生态系统下的主力开发者：学生？](https://www.ifanr.com/80997) — ifanr, April 8, 2012, in Chinese. A feature based on The Verge's reporting includes a dedicated section on Quinn and Baconit.
- [REVIEW HTC Windows Phone 8S, un „Prâslea“ mai ieftin şi cu o baterie la fel de slabă ca fratele mai mare](https://adevarul.ro/stil-de-viata/tehnologie/review-htc-windows-phone-8s-un-praslea-mai-1408812.html) — Adevărul, February 11, 2013, in Romanian. A hardware review discusses Baconit's interface, subreddit discovery, and in-app browsing.
- [Baconit y Adobe Creative Cloud se preparan para el lanzamiento de Windows 10](https://www.xatakawindows.com/actualidad-en-redmond/baconit-y-adobe-creative-cloud-se-preparan-para-el-lanzamiento-de-windows-10) — Xataka Windows, July 28, 2015, in Spanish. Covers the universal rewrite and plans to release the source code.
- [Лучшие программы недели для Windows Phone от 22.11.2015](https://trashbox.ru/topics/91587/luchshie-programmy-nedeli-dlya-windows-phone-ot-22.11.2015) — Trashbox.ru, November 23, 2015, in Russian. Baconit is one of five weekly app selections; the November 22 date in the title identifies the roundup.
- [Die besten Apps für Windows 10 Mobile](https://windowsarea.de/2018/08/die-besten-apps-fuer-windows-10-mobile/) — WindowsArea.de, August 26, 2018, in German. A dedicated section discusses Baconit's performance, navigation, and interface.

### Videos & Audio

- [Lumiappaday #48: Baconit demoed on the Nokia Lumia 800](https://www.youtube.com/watch?v=bl0ZXzLvcLo) — My Nokia Blog, January 1, 2012. An early hands-on demonstration, 3:13.
- [Hot Apps: Civilization Revolution, Baconit, Symmetry, Wikitude, Falling Birds](https://www.ivoox.com/en/hot-apps-civilization-revolution-baconit-symmetry-wikitude-falling-audios-mp3_rf_5431499_1.html) — Channel 9 / Hot Apps, May 2012. An iVoox listing for Laura Foy's episode featuring Baconit.
- [Podcast #21: CeBIT & Co.](https://www.ivoox.com/en/podcast-21-cebit-co-audios-mp3_rf_5094170_1.html) — smartphone7, March 10, 2013, in German. Tobias selects Baconit in this 26:38 episode.
- [Ireland Windows Apps of the Week April 28th](https://www.youtube.com/watch?v=SvgGdir5t9k) — WindowsAppsIreland, April 28, 2014. Baconit appears in a short weekly app showcase, 0:56.
- [Top 5 Continuum Apps Worth Checking Out!](https://www.youtube.com/watch?v=ecmx7t2hT5M) — MSPoweruser, April 5, 2016. Includes Baconit among the recommended Continuum apps, 3:32.
- [Hands On: Browsing Reddit with Baconit for Xbox One](media/youtube-windows-central-baconit-xbox-one-2016.md) — Windows Central, July 29, 2016. Console hands-on footage, 3:54.
- [Baconit beta Reddit XBOX ONE UWP App Latest Preview](https://www.youtube.com/watch?v=SXIgGOp1jgM) — keepitwarm, July 29, 2016. Another demonstration of the Xbox version, 4:04.
- [Free UWP APP: Baconit](https://www.youtube.com/watch?v=3LGoU8Jkekc) — XboxIssues, September 20, 2016. Console app footage, 3:26.
- [Baconit fan explainer](https://www.youtube.com/watch?v=qCsX8_1f-74) — Mike Ottenhoff, November 23, 2016. A fan-made explanation with original audio, 2:19.

### Historical Images

- [Quinn Damerell portrait](https://platform.theverge.com/wp-content/uploads/sites/2/chorus/assets/1029390/quinn-300.jpg) — The Verge, March 29, 2012. The photograph accompanying the feature on student Windows Phone developers.

### Original Announcements & Community Continuations

- [Baconit — A Metro Reddit App](https://forums.windowscentral.com/threads/baconit-a-metro-reddit-app.185868/) — Quinn / quinbd, Windows Central forum, January 13, 2012. Early feature list and reader feedback.
- [Free Reddit App](https://forums.windowscentral.com/threads/free-reddit-app.185869/) — Quinn / quinbd, Windows Central forum, January 13, 2012. Separate early introduction with a reader response.
- [Baconit 1.5 is now live](media/reddit-baconit-free-donation-2012.md) — Quinn / quinbd, r/wp7, February 2012. Release discussion with requests and Quinn's replies about version 1.6; includes the [discussion of the free and donation editions](media/reddit-baconit-free-donation-2012.md#comment-c3no50t).
- [Free app: Baconit — A Metro Reddit App](https://forums.windowscentral.com/threads/free-app-baconit-a-metro-reddit-app.187178/) — Quinn / quinbd, Windows Central forum, February 14, 2012. Version 1.6 feature list and an early milestone of more than 12,000 downloads.
- [Dev of Baconit looking for feedback](https://forums.windowscentral.com/threads/dev-of-baconit-looking-for-feedback.189309/) — Quinn / quinbd, Windows Central forum, April 5, 2012. Feedback request while preparing version 2.0.
- [Baconit Update 4.7 — The Editing Update](media/reddit-baconit-editing-2016.md) — Quinn / quinbd, r/baconit, January 2016. Original changelog, explanation of adaptive Markdown preview timing, and user reports.
- [Baconit Extended](https://store.live.net.co/app/121) — NLogDEV, Live Store. A community continuation of the Windows Phone app, listed since May 2025, with gallery/video improvements, screenshots, and user reviews. This is a later developer's version, separate from Quinn's original releases.

### Archive Leads

- [Hot Apps episode: archived WMV](https://web.archive.org/web/20220207110125/https://sec.ch9.ms/ch9/b3af/db27797c-3492-460c-adc9-d4e875c4b3af/HAciv.wmv) — Channel 9, May 2012; Internet Archive capture dated February 7, 2022. A capture of the episode's original video file was located; playback remains unverified.
- [Sample magazine PDF](https://appdevelopermagazine.com/sample/sample.pdf) — App Developer Magazine, issue date unknown. According to search results, it lists Baconit – Donate at number 5 among paid Windows apps. I haven't been able to confirm the page number or issue date, or open the PDF directly.

</details>
