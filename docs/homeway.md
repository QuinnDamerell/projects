# Homeway

Free, private cloud tools for Home Assistant, from secure remote access to an AI assistant with a little personality.

[Visit Homeway :material-arrow-top-right:](https://homeway.io/?source=projects_hw){ .md-button .md-button--primary }

## Facts

| Created | Status | Code | Community |
| ------- | ------- | --------- | --------- |
| 2024    | Active  | [GitHub](https://github.com/homewayio/AddOn) | 78k+ members |

## The story {#description}

I built Homeway because reaching Home Assistant remotely always seemed to come with a catch: an exposed server, a VPN on every device, or ongoing setup and maintenance. After six months of development and a beta with more than 500 testers, it launched in April 2024. Setup takes about 20 seconds, and you get free, secure, and private remote access with zero maintenance. My [April 9 launch post](https://blog.homeway.io/welcome-to-homeway/) tells that early story.

Homeway now includes Sage AI, Alexa and Google Home integrations, a remote MCP server for AI agents, and WebRTC camera streaming. Like OctoEverywhere, it's a small, independent Seattle project with no investors, funded entirely through community Supporter Perks. It runs in seven server locations, has served more than 100 TB of traffic, and holds a 4.9 Trustpilot rating.

<figure class="product-capture">
  <a href="assets/heroes/homeway-website.webp"><img class="no-lightbox" src="assets/heroes/homeway-website.webp" alt="The Homeway website introducing its remote access and AI tools for Home Assistant" width="1269" height="714" loading="lazy" decoding="async"></a>
  <figcaption>A capture of the <a href="https://homeway.io/">Homeway website</a>, October 2026.</figcaption>
</figure>

## Community

I built Homeway as part of the Home Assistant community, and I want everyone to be able to use it, so every major feature is in the free tier. Supporter Perks fund the service and add higher limits, priority MCP routing, and advanced Sage models, and as support grows, the free limits go up for everyone. Our Discord is where we share ideas, help each other, and decide what comes next.

<details class="qd-story-details" markdown="1">
<summary>The timeline &amp; early community</summary>

## Timeline

| Year | Milestones |
| ---- | ---------- |
| 2023 | Development begins |
| 2024 | Launch with remote access, Alexa, Google Home, and Home Assistant app support; Docker container; Local Access |
| 2025 | Sage AI; DeepSeek R1, ChatGPT 5, and Gemini 3 models; Sage AI 2.0 |
| 2026 | WebRTC camera streaming; remote MCP server; passkeys |

## Early Development

Public testing started well before launch. When I [introduced Homeway on Reddit in early January 2024](media/reddit-homeway-introduction-2024.md), I answered questions about voice-assistant authentication, funding, and installation compatibility. At first, Homeway needed add-on support, so Docker users asked for another option. The [standalone Docker release](https://blog.homeway.io/homeway-docker-container-setup-guide/) followed in August, alongside the existing Linux CLI.

By [February 26, 2024](media/reddit-homeway-companion-2024.md), more than 150 community members were helping find bugs and polish the service. They also pointed out gaps in the security documentation, especially around mobile-app and voice-assistant authentication, which I answered in the discussion.

</details>

<details class="qd-story-details" markdown="1">
<summary>Remote access, apps &amp; cameras</summary>

## Remote Access

### Secure Remote Access

Homeway opens the full Home Assistant dashboard in any browser without exposing the server to the public internet. Every request passes two logins: Homeway's and Home Assistant's. Home Assistant credentials and session data are never stored, and a worldwide server mesh keeps the connection close to home.

### Home Assistant App Support

The official iPhone and Android apps work remotely, including location-based automations, push notifications, and widgets.

### Local Access

Launched in December 2024, Local Access extends secure remote access to other home-network services, including Node-RED, Unraid, AdGuard, Pi-hole, and Bitwarden.

### Shared Connections

Share access with a unique link and choose when it expires.

### WebRTC Camera Streaming

Since January 2026, Homeway’s free STUN and TURN servers have enabled end-to-end encrypted WebRTC camera streaming in the Home Assistant dashboard. STUN is unlimited, and TURN relays, which cost more to run, have a free allowance with higher limits for supporters. The add-on sets it all up automatically.

</details>

<details class="qd-story-details" markdown="1">
<summary>Sage, voices &amp; AI agents</summary>

## AI & Voice

### Sage AI

Sage is a free AI conversation agent for Home Assistant Assist, using models such as ChatGPT, Claude, and Gemini. It understands the whole home, controls devices, searches the web, checks weather, sets timers, and remembers preferences. It connects through the Wyoming protocol, with no API keys needed. When it launched in January 2025, it was the first fully integrated Assist pipeline. DeepSeek R1, ChatGPT 5, and Gemini 3 joined as they were released, and Sage AI 2.0 followed in October 2025.

The [Sage launch guide](https://blog.homeway.io/homeway-sage-free-private-intelligent-chatgpt-for-home-assistant-assist-voice/) walks through combining conversation, speech recognition, and speech synthesis in one Assist profile. It recommends handling supported commands locally and sending everything else to Sage. You can also ask Sage to create, list, or delete memories, so its personalization stays visible and editable.

The [October 30, 2025 Sage AI 2.0 announcement](https://blog.homeway.io/sage-ai-the-most-advanced-ai-home-assistant-integration/) celebrated the bigger voice and AI features with 60 days of free Supporter Perks and a raffle for 20 lifetime memberships. (Those were one-time launch promotions.)

### Lifelike Voices

Sage offers more than 80 lifelike, multilingual voices from ElevenLabs, Azure, Google, and OpenAI. Custom prompts shape how it thinks and speaks: friendly helper, strict space ranger, humble house elf. Your home, your cast of characters.

### Speech-To-Text

Sage provides low-latency, multilingual speech recognition for Home Assistant Voice devices, reaching a 5.7% word error rate in version 2.0. Speech-to-text, text-to-speech, and the AI model also work independently in scripts and automations.

### Google Home & Alexa

One-click integrations link Google Home and Amazon Alexa through Homeway’s low-latency network. The Assistant Device Control page lets you choose which devices each assistant can see.

In his [February 2025 hands-on review](media/neil-turner-homeway-review-2025.md), Neil Turner kept his Nginx Proxy Manager remote-access setup but found Homeway’s Google Assistant connection most useful. He reported faster responses and fewer offline-device problems than with his manual integration.

### Remote MCP Server

The remote MCP server launched in March 2026, connecting Claude, ChatGPT, Gemini, Cursor, VS Code, and other AI assistants and agents to Home Assistant. They can read the home’s layout and live device states, control devices, and help build dashboards, scripts, and automations. Server-enforced permissions apply to each tool, including a read-only option the AI cannot bypass.

</details>

<details class="qd-story-details" markdown="1">
<summary>Setup, security &amp; privacy</summary>

## Setup

### Home Assistant Add-on

The add-on, now called an app in Home Assistant, installs in about 20 seconds, links to a Homeway account, and updates automatically.

### Standalone CLI & Docker

Setups without add-on support can use a standalone Linux command line install or, since August 2024, a Docker container on Windows, Mac, or Linux.

## Security & Privacy

### Secure By Design

I build every feature around security. If it can't be built securely, it doesn't ship. The add-on opens an outbound TLS WebSocket, so your ports stay closed. The server signs a random handshake challenge with its private key, blocking impostors even if they hold a valid homeway.io certificate. Servers use TLS 1.3, per-server certificates, and HSTS preloading, with an A+ SSL Labs rating.

### Account Protection

Accounts support Google and Apple sign-in, time-based two-factor codes, and emailed codes for new-IP logins. Passkeys arrived in May 2026.

### Privacy Commitment

Homeway never stores or sells your Home Assistant data. Tunneled data is relayed, then deleted. Third-party AI providers receive only the minimum anonymized data Sage needs, which is deleted after processing.

</details>

<details class="qd-story-details" markdown="1">
<summary>Reviews, videos &amp; source notes</summary>

## Further Reading & Media

Reviews, walkthroughs, community discussions, and historical images from around the web.

### Articles & Reviews

- [Homeway – easy remote access to Home Assistant](media/neil-turner-homeway-review-2025.md) — Neil Turner, February 23, 2025. A hands-on account of remote access and Google Assistant setup, with a contemporary homepage screenshot.
- [Ist Homeway.io eine günstigere Alternative zu Nabu Casa, wenn es um Home Assistant geht?](media/fricklr-homeway-review-2025.md) — fricklr, formerly nachbelichtet, May 6, 2025. German hands-on review with setup screenshots and discussion of the connection to OctoEverywhere; an [English translation](media/fricklr-homeway-review-2025.md#english) is also available. The article incorrectly credits Quinn with creating Mainsail, Fluidd, and Moonraker.
- [Homeway vs Nabu Casa (Home Assistant Cloud)](https://programarfacil.com/domotica/homeway-vs-nabu-casa-home-assistant-cloud/) — Maxi / ProgramarFácil, December 18, 2025. Spanish comparison with a section about Quinn's story and an accompanying video. Includes a referral link.
- [Remplacer Nabu Casa : Tailscale vs Cloudflare vs WireGuard](https://domocraft.fr/infrastructure/remplacer-nabu-casa-tailscale-cloudflare-tunnel-wireguard/) — Tom DEHAME / Domocraft, April 22, 2026; updated July 16, 2026. French remote-access comparison with a short, critical Homeway subsection.
- [A Nabu Casa alternative for integrators? Why that is the wrong question](https://ha-fleet-manager.com/en/blog/nabu-casa-alternative-integratoren/) — Denny Ovčar / HA Fleet Manager, June 19, 2026. Vendor-written comparison with a Homeway paragraph and table entry.

### Videos

- [The best Home assistant FREE remote access 2024 Homeway working with mobile App](https://www.youtube.com/watch?v=dpO8RzE5ldE) — Ensferi, January 14, 2024 · 4:02. An early remote-access and mobile-app walkthrough.
- [Homeway HA Addon: Get FREE Remote Access, AI, & Alexa in SECONDS](media/youtube-daniel-barczak-homeway-2025.md) — Daniel Barczak, March 16, 2025 · 19:19. Installation, Alexa, and Sage walkthrough; Sage setup begins at 8:32 and testing at 12:24. Includes a referral link.
- [Is LOCAL AI the ULTIMATE Winner Over CLOUD AI for Home Assistant?](https://www.youtube.com/watch?v=cbktGbxv43Y&t=140s) — Daniel Barczak, July 28, 2025 · 14:30. A brief Homeway mention at 2:20 within a broader local-versus-cloud AI discussion.
- [Remote Home Assistant using smartphone with Homeway](https://www.youtube.com/watch?v=dOV3cbCpcdw) — Obengplus com, August 10, 2025 (Pacific time) · 6:36. An Indonesian creator's add-on installation and Android setup tutorial. Includes a referral link.
- [Nabu Casa vs Homeway: La alternativa que nadie te había contado](media/youtube-domotica-facil-homeway-comparison-2025.md) — Home Assistant y Domótica Fácil, December 18, 2025 · 12:34. Spanish comparison with [Quinn's story at 2:46](media/youtube-domotica-facil-homeway-comparison-2025.md#quinn-story) and a “Reto QUINN” segment at 11:55. Includes a referral link.
- [Home Assistant Toegang: Tailscale, Cloudflare, Nabu Casa en Homeway Vergeleken](media/youtube-denie-van-kleef-homeway-comparison-2026.md) — Denie van Kleef, March 15, 2026 · 22:09. Dutch comparison; the [Homeway section begins at 14:38](media/youtube-denie-van-kleef-homeway-comparison-2026.md#homeway).

Short companion clips from Home Assistant y Domótica Fácil (I don't have exact publication dates for these):

- [HomeWay vs Nabu Casa: ¡La Batalla de Asistentes de Voz!](https://www.youtube.com/shorts/oBdGLDnZyLw) — Voice assistants.
- [HomeWay vs Nabu Casa: Seguridad Domótica Superior](https://www.youtube.com/shorts/yTX2s8g0k0g) — Security.
- [Home Assistant: Nabu Casa vs HomeWay - ¿Cuál elegir?](https://www.youtube.com/shorts/JIWA84EY8YA) — Choosing between the services.
- [Home Assistant Cloud vs. HomeWay: Acceso Remoto Sin Sufrir](https://www.youtube.com/shorts/KV7LfbGQTIo) — Remote access.
- [HomeWay vs Nabu Casa: ¡Tu Red Local Sin Límites!](https://www.youtube.com/shorts/H9MwrV1d2N4) — Local network access.

### Community Discussions

- [Introducing Homeway — A free secure tunnel for self-hosted Home Assistants](media/reddit-homeway-introduction-2024.md) — Reddit / r/selfhosted, January 3, 2024 Pacific time (January 4 UTC). Early creator introduction and Q&A about installation support, authentication, funding, and alternatives. The original post was removed by moderators; the surviving comments include creator replies and critical feedback.
- [Companion app question](media/reddit-homeway-companion-2024.md) — Reddit / r/homeassistant, February 26, 2024. An early discussion in which Quinn describes the service and its community of more than 150 members.
- [Acesso externo no HA pelo Homeway é bom?](https://homeassistantbrasil.com.br/t/acesso-externo-no-ha-pelo-homeway-e-bom/11756) — Fórum Home Assistant Brasil, October 27, 2024. Portuguese-language setup and Alexa experiences.
- [Wer hat Erfahrungen mit homeway.io](https://community.simon42.com/t/wer-hat-erfahrungen-mit-homeway-io/50532) — Simon42 community, March 2025 onward. German user experiences, including Sage; the [discussion continues on page 2](https://community.simon42.com/t/wer-hat-erfahrungen-mit-homeway-io/50532?page=2).

### Launch Announcement & Historical Images

- [Homeway Launches New Remote Access Solution for Home Assistant Enthusiasts](media/newsfile-homeway-launch-2024.md) — Newsfile, April 25, 2024. Company press release with an [original promotional image](https://images.newsfilecorp.com/files/9100/200359_28570b48649fc828_001full.jpg). The [April 27 ZEX PR Wire publication](https://zexprwire.com/homeway-launches-new-remote-access-solution-for-home-assistant-enthusiasts/) is a syndication of the same release.
- [Homeway homepage screenshot](https://neilturner.me.uk/wp-content/uploads/2025/02/homeway-screenshot.png) — Neil Turner, February 2025.
- [Homeway page image](https://media.fricklr.com/ist-homeway-io-eine-guenstigere-alternative-zu-nabu-casa-wenn-es-um-home-assistant-geht/homeway-io.webp) and [setup screenshot](https://media.fricklr.com/ist-homeway-io-eine-guenstigere-alternative-zu-nabu-casa-wenn-es-um-home-assistant-geht/homeway-io-setup-nachbelichtet.webp) — fricklr / nachbelichtet, May 2025.
- [Homeway directory listing and screenshots](https://www.saashub.com/homeway-io) — SaaSHub. Homepage and Sage images labeled October 17, 2025; directory material rather than an independent review.

### Original Announcements & Guides

My own posts on the Homeway blog. Some guides have been updated since they were first published, so their model lists and setup steps may not match launch day.

- [Welcome To Homeway](https://blog.homeway.io/welcome-to-homeway/) — April 9, 2024. Six months of development, more than 500 beta testers, and the original launch goals.
- [Google Home Assistant Integration — A Quick Setup Guide](https://blog.homeway.io/google-home-assistant-integration-a-quick-setup-guide/) — April 12, 2024. Early account-linking walkthrough, device assignment, and automatic discovery of newly added devices.
- [Homeway Docker Container Setup Guide](https://blog.homeway.io/homeway-docker-container-setup-guide/) — August 13, 2024. Announcement of the standalone Docker option and a comparison with the add-on and Linux CLI.
- [Supporter Perks Updates](https://blog.homeway.io/supporter-perks-updates/) — page dated December 6, 2024; its current text describes pricing changes effective October 1, 2025. A record of the evolving funding model and the addition of Elite perks and ElevenLabs voices.
- [Node-RED, Unraid, AdGuard, & More — Free & Secure Remote Access](https://blog.homeway.io/node-red-unraid-adguard-more-free-secure-remote-access/) — December 16, 2024. Local Access launch, extending Homeway to other web services on the home network.
- [Homeway Sage — Free, Private, & Intelligent ChatGPT for Home Assistant Assist & Voice](https://blog.homeway.io/homeway-sage-free-private-intelligent-chatgpt-for-home-assistant-assist-voice/) — January 12, 2025. Sage introduction and illustrated Assist setup guide, including memory controls and voice-device configuration.
- [Sage AI 2.0 — The Most Advanced AI Home Assistant Integration](https://blog.homeway.io/sage-ai-the-most-advanced-ai-home-assistant-integration/) — October 30, 2025. The second major Sage release, customization examples, and the community celebration.
- [Free WebRTC Video Streaming For Home Assistant](https://blog.homeway.io/free-webrtc-video-streaming-for-home-assistant/) — January 22, 2026. Camera-streaming announcement and explanation of Homeway's STUN and TURN services.
- [Remote MCP Server For Home Assistant](https://blog.homeway.io/remote-mcp-server-for-home-assistant/) — March 12, 2026. Launch of Homeway's remote connection for AI assistants and agents.
- [Passkeys For Home Assistant](https://blog.homeway.io/passkeys-for-home-assistant/) — May 29, 2026. Passkey-support announcement and account setup guide.

</details>
