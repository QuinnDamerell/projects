#!/usr/bin/env node
// Snapshots a web page for the Media section: a full-page screenshot, a PDF, and a
// self-contained HTML copy with the page's images and stylesheets saved next to it.
// It drives the locally installed Chrome or Edge over the DevTools protocol, so no
// packages are needed (Node 22 or newer).
//
//   node tools/snapshot.mjs <url> <slug> [--image <match>=<replacement>] [--remove <selector>] ...
//
// <url> can also be a Wayback Machine link (https://web.archive.org/web/<timestamp>/<url>)
// for pages that are already offline; the copy then records both addresses.
//
// Files are written to docs/assets/media/<slug>/. Use --image to swap a broken image for a
// copy found elsewhere, such as the Wayback Machine: <match> is any part of the original
// image URL and <replacement> is a URL or a local file. When images are swapped, the page
// exactly as it loaded is also kept as as-captured.png. Use --remove to leave out ads and
// unrelated page sections, such as endless "more stories" feeds, by CSS selector.
//
// Fonts and background images referenced by the page's CSS still load from the original
// site; if they disappear the copy falls back to system fonts. The screenshot and PDF are
// the faithful record.

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36';
const VIEWPORT = { width: 1280, height: 900 };
const EXTENSIONS = { 'image/jpeg': '.jpg', 'image/png': '.png', 'image/gif': '.gif', 'image/webp': '.webp', 'image/avif': '.avif', 'image/svg+xml': '.svg' };
const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

function parseArgs(argv) {
  const positional = [];
  const images = [];
  const removes = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--image') {
      const value = argv[++i] ?? '';
      const split = value.indexOf('=');
      if (split < 1) throw new Error(`--image expects <match>=<replacement>, got "${value}"`);
      images.push({ match: value.slice(0, split), source: value.slice(split + 1) });
    } else if (argv[i] === '--remove') {
      removes.push(argv[++i] ?? '');
    } else {
      positional.push(argv[i]);
    }
  }
  const [url, slug] = positional;
  if (!url || !slug) throw new Error('Usage: node tools/snapshot.mjs <url> <slug> [--image <match>=<replacement>] [--remove <selector>] ...');
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) throw new Error('The slug may only contain lowercase letters, digits, and dashes.');
  return { source: resolveSource(url), slug, images, removes, outDir: path.join(repoRoot, 'docs', 'assets', 'media', slug) };
}

// Wayback Machine links are loaded with the if_ flag, which serves the archived page with
// its links and assets pointing into the archive but without the Wayback toolbar.
function resolveSource(url) {
  const match = url.match(/^https?:\/\/web\.archive\.org\/web\/(\d{4,14})(?:[a-z]{2}_)?\/(.+)$/);
  if (!match) return { url, load: url };
  const [, timestamp, address] = match;
  const original = address.replace(/^(https?:\/\/[^/:]+):80\//, '$1/');
  const t = timestamp.padEnd(14, '0');
  return {
    url: original,
    load: `https://web.archive.org/web/${timestamp}if_/${original}`,
    archive: `https://web.archive.org/web/${timestamp}/${original}`,
    timestamp,
    archived: `${t.slice(0, 4)}-${t.slice(4, 6)}-${t.slice(6, 8)}T${t.slice(8, 10)}:${t.slice(10, 12)}:${t.slice(12, 14)}Z`,
  };
}

function findBrowser() {
  const candidates = [
    process.env.CHROME_PATH,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
  ];
  const found = candidates.find(candidate => candidate && fs.existsSync(candidate));
  if (!found) throw new Error('Chrome or Edge was not found. Set CHROME_PATH to the browser executable.');
  return found;
}

async function launchBrowser() {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'snapshot-'));
  const proc = spawn(findBrowser(), [
    '--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--mute-audio',
    `--user-agent=${USER_AGENT}`, `--window-size=${VIEWPORT.width},${VIEWPORT.height}`, 'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  const exited = new Promise(resolve => proc.once('exit', resolve));

  const wsUrl = await new Promise((resolve, reject) => {
    let log = '';
    const timer = setTimeout(() => reject(new Error(`The browser did not start:\n${log}`)), 30000);
    proc.stderr.on('data', chunk => {
      log += chunk;
      const match = log.match(/DevTools listening on (ws:\/\/\S+)/);
      if (match) { clearTimeout(timer); resolve(match[1]); }
    });
    exited.then(code => reject(new Error(`The browser exited with code ${code}:\n${log}`)));
  });

  const close = async () => {
    proc.kill();
    await Promise.race([exited, sleep(5000)]);
    try { fs.rmSync(profile, { recursive: true, force: true, maxRetries: 10, retryDelay: 300 }); } catch { /* temp profile; safe to leave */ }
  };
  return { wsUrl, close };
}

async function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = () => reject(new Error('Could not connect to the browser.'));
  });
  let nextId = 0;
  const pending = new Map();
  const waiters = new Set();
  const listeners = [];
  ws.onmessage = ({ data }) => {
    const message = JSON.parse(data);
    if (message.id) {
      const call = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) call.reject(new Error(`${call.method}: ${message.error.message}`));
      else call.resolve(message.result);
      return;
    }
    for (const listener of listeners) {
      if (listener.method === message.method) listener.handler(message.params, message.sessionId);
    }
    for (const waiter of waiters) {
      if (waiter.method === message.method && waiter.sessionId === message.sessionId) {
        waiters.delete(waiter);
        waiter.resolve(message.params);
      }
    }
  };
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const id = ++nextId;
    pending.set(id, { resolve, reject, method });
    ws.send(JSON.stringify({ id, method, params, sessionId }));
  });
  const once = (method, sessionId) => new Promise(resolve => waiters.add({ method, sessionId, resolve }));
  const on = (method, handler) => listeners.push({ method, handler });
  return { send, once, on, close: () => ws.close() };
}

async function openPage(cdp) {
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const send = (method, params) => cdp.send(method, params, sessionId);
  // An alert or confirm box would block the page, and every call into it, until answered.
  cdp.on('Page.javascriptDialogOpening', (params, from) => {
    if (from === sessionId) send('Page.handleJavaScriptDialog', { accept: true }).catch(() => {});
  });
  // Page code runs in an isolated world: it shares the page's DOM but not its JavaScript, so
  // scripts that patch built-ins can't interfere. The Wayback Machine's playback script
  // (wombat.js) does exactly that, making URLs and outerHTML report original addresses.
  let contextId;
  const isolate = async () => {
    const { frameTree } = await send('Page.getFrameTree');
    ({ executionContextId: contextId } = await send('Page.createIsolatedWorld', { frameId: frameTree.frame.id, worldName: 'snapshot' }));
  };
  // Runs fn inside the page. Arguments and the return value must be JSON-serializable.
  const evaluate = async (fn, ...args) => {
    const { result, exceptionDetails } = await Promise.race([
      send('Runtime.evaluate', { expression: `(${fn})(...${JSON.stringify(args)})`, contextId, awaitPromise: true, returnByValue: true }),
      sleep(90000).then(() => { throw new Error(`The page did not finish ${fn.name} within 90 seconds.`); }),
    ]);
    if (exceptionDetails) throw new Error(exceptionDetails.exception?.description ?? exceptionDetails.text);
    return result.value;
  };
  return { sessionId, send, evaluate, isolate, once: method => cdp.once(method, sessionId) };
}

// Wayback Machine links wrap files in its viewer; the id_ flag returns the original bytes.
const waybackRaw = url => url.replace(/^(https?:\/\/web\.archive\.org\/web\/\d+)(?:[a-z]{2}_)?\//, '$1id_/');

async function download(source, referer) {
  if (!/^https?:/i.test(source)) {
    const type = Object.keys(EXTENSIONS).find(key => EXTENSIONS[key] === path.extname(source).toLowerCase().replace('.jpeg', '.jpg')) ?? '';
    return { buffer: fs.readFileSync(source), type };
  }
  // The Wayback Machine sometimes stalls a request indefinitely, so give up after a while.
  // Some sites refuse image requests without a Referer, to stop hotlinking.
  const headers = { 'User-Agent': USER_AGENT, ...(referer && { Referer: referer }) };
  const response = await fetch(source, { headers, signal: AbortSignal.timeout(30000) });
  if (!response.ok) throw new Error(`HTTP ${response.status} for ${source}`);
  return { buffer: Buffer.from(await response.arrayBuffer()), type: response.headers.get('content-type')?.split(';')[0].trim() ?? '' };
}

function saveImage(outDir, url, { buffer, type }, used) {
  let base = decodeURIComponent(new URL(url).pathname.split('/').pop() || 'image').replace(/[^\w.-]+/g, '-');
  const ext = EXTENSIONS[type];
  if (ext && !base.toLowerCase().endsWith(ext) && !(ext === '.jpg' && /\.jpe?g$/i.test(base))) base += ext;
  let name = base;
  for (let n = 2; used.has(name.toLowerCase()); n++) name = base.replace(/(\.\w+)?$/, `-${n}$1`);
  used.add(name.toLowerCase());
  fs.writeFileSync(path.join(outDir, 'images', name), buffer);
  return `images/${name}`;
}

// Reads each linked stylesheet's text from the browser instead of downloading it again, and
// tags its <link> so the HTML copy can inline it. On archived pages the Wayback Machine's
// playback script makes the page report original addresses, and those servers are usually gone.
async function collectStylesheets(cdp, page) {
  const headers = [];
  cdp.on('CSS.styleSheetAdded', ({ header }, from) => { if (from === page.sessionId) headers.push(header); });
  await page.send('DOM.enable');
  await page.send('CSS.enable');
  await sleep(500);
  const css = [];
  for (const header of headers) {
    if (header.isInline || !header.ownerNode || !header.sourceURL || header.origin !== 'regular') continue;
    try {
      const { text } = await page.send('CSS.getStyleSheetText', { styleSheetId: header.styleSheetId });
      const { object } = await page.send('DOM.resolveNode', { backendNodeId: header.ownerNode });
      await page.send('Runtime.callFunctionOn', {
        objectId: object.objectId, arguments: [{ value: css.length }],
        functionDeclaration: 'function (i) { this.setAttribute("data-snapshot-sheet", i); }',
      });
      css.push({ text, base: header.sourceURL });
    } catch (error) { console.warn(`  Stylesheet not saved (${error.message})`); }
  }
  return css;
}

// Grows the viewport to the whole page before capturing; captureBeyondViewport leaves
// cross-origin iframes such as video embeds blank.
async function saveScreenshot(page, file) {
  const { cssContentSize } = await page.send('Page.getLayoutMetrics');
  await page.send('Emulation.setDeviceMetricsOverride', { width: VIEWPORT.width, height: Math.ceil(cssContentSize.height), deviceScaleFactor: 1, mobile: false });
  await sleep(2000);
  const { data } = await page.send('Page.captureScreenshot', { format: 'png' });
  await page.send('Emulation.setDeviceMetricsOverride', { ...VIEWPORT, deviceScaleFactor: 1, mobile: false });
  fs.writeFileSync(file, Buffer.from(data, 'base64'));
}

// ---- Functions below run inside the page. ----

async function settlePage() {
  const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
  // Scroll through once so lazy-loaded images load, then wait for them. The time limit stops
  // pages that keep growing as you scroll (infinite feeds, comment widgets).
  const stop = Date.now() + 20000;
  for (let y = 0; y < document.documentElement.scrollHeight && Date.now() < stop; y += innerHeight / 2) {
    scrollTo(0, y);
    await pause(150);
  }
  scrollTo(0, 0);
  await Promise.all([...document.images].map(img => img.complete ? null : new Promise(resolve => {
    img.addEventListener('load', resolve, { once: true });
    img.addEventListener('error', resolve, { once: true });
    setTimeout(resolve, 20000); // archived images can take several slow redirects

  })));
  await Promise.race([document.fonts.ready, pause(5000)]);
  await pause(1000);
}

function removeElements(selectors) {
  let count = 0;
  for (const selector of selectors) {
    document.querySelectorAll(selector).forEach(el => { el.remove(); count++; });
  }
  return count;
}

function readPage() {
  const meta = name => document.querySelector(`meta[property="${name}"], meta[name="${name}"]`)?.content || null;
  return {
    title: meta('og:title') || document.title,
    site: meta('og:site_name') || location.hostname,
    published: meta('article:published_time'),
    images: [...document.images].map(img => ({ src: img.currentSrc || img.src, ok: img.complete && img.naturalWidth > 0 })),
    youtube: [...document.querySelectorAll('iframe[src*="youtube.com/embed/"], iframe[src*="youtube-nocookie.com/embed/"]')]
      .map(frame => new URL(frame.src).pathname.split('/').pop()),
  };
}

async function swapImage(match, dataUrl, localPath) {
  const imgs = [...document.images].filter(img => (img.currentSrc || img.src).includes(match));
  for (const img of imgs) {
    img.closest('picture')?.querySelectorAll('source').forEach(source => source.remove());
    ['srcset', 'sizes', 'loading'].forEach(name => img.removeAttribute(name));
    img.src = dataUrl;
    img.dataset.snapshotSrc = localPath;
    await img.decode().catch(() => {});
  }
}

function serializeForArchive({ url, loadUrl, archive, archived, timestamp, captured, published, restored, trimmed, css, images, youtube }) {
  // Archived pages report original addresses, so anything not already in the archive is
  // pointed at its archived copy. Paths relative to the original site resolve against it.
  const resolve = value => {
    let address = new URL(value, loadUrl).href;
    if (!timestamp) return address;
    if (/^https?:\/\/web\.archive\.org\/(?!web\/)/i.test(address)) address = new URL(value, url).href;
    return /^https?:\/\/web\.archive\.org\//i.test(address) ? address : `https://web.archive.org/web/${timestamp}/${address}`;
  };

  // Custom elements never get defined without scripts, so styles that wait for :defined
  // would hide them forever; treat every element as defined.
  const absolutizeCss = (text, base) => text
    .replace(/:not\(\s*:defined\s*\)/g, ':not(*)')
    .replace(/:defined\b/g, ':is(*)')
    .replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g, (all, quote, ref) => {
      if (/^(data:|#)/i.test(ref)) return all;
      try { return `url("${new URL(ref, base).href}")`; } catch { return all; }
    })
    .replace(/@import\s+(['"])([^'"]+)\1/g, (all, quote, ref) => {
      try { return `@import "${new URL(ref, base).href}"`; } catch { return all; }
    });

  // Inline stylesheets so the copy keeps the page's look without the original server.
  for (const link of document.querySelectorAll('link[data-snapshot-sheet]')) {
    const sheet = css[link.getAttribute('data-snapshot-sheet')];
    const style = document.createElement('style');
    if (link.media) style.media = link.media;
    style.textContent = absolutizeCss(sheet.text, sheet.base);
    link.replaceWith(style);
  }
  document.querySelectorAll('style').forEach(style => { style.textContent = absolutizeCss(style.textContent, loadUrl); });
  document.querySelectorAll('[style*="url("]').forEach(el => el.setAttribute('style', absolutizeCss(el.getAttribute('style'), loadUrl)));

  // Point images at the saved copies; anything left falls back to its original address.
  for (const img of document.images) {
    const local = img.dataset.snapshotSrc || images[img.currentSrc || img.src];
    if (local) {
      img.closest('picture')?.querySelectorAll('source').forEach(source => source.remove());
      ['srcset', 'sizes', 'loading', 'data-snapshot-src'].forEach(name => img.removeAttribute(name));
      img.setAttribute('src', local);
    } else if (img.getAttribute('src')) {
      try { img.setAttribute('src', resolve(img.getAttribute('src'))); } catch { /* leave as-is */ }
    }
  }

  // YouTube embeds become a thumbnail that links to the video.
  for (const frame of document.querySelectorAll('iframe[src*="youtube.com/embed/"], iframe[src*="youtube-nocookie.com/embed/"]')) {
    const id = new URL(frame.src).pathname.split('/').pop();
    const link = document.createElement('a');
    link.href = `https://www.youtube.com/watch?v=${id}`;
    link.style.cssText = `display:block;position:relative;width:${Math.round(frame.getBoundingClientRect().width) || 480}px;max-width:100%;`;
    link.innerHTML = youtube[id]
      ? `<img src="${youtube[id]}" alt="YouTube video thumbnail" style="display:block;width:100%;height:auto;"><span style="position:absolute;left:12px;bottom:12px;padding:4px 10px;border-radius:4px;background:#000c;color:#fff;font:600 14px/1.4 system-ui,sans-serif;">&#9654; Watch on YouTube</span>`
      : 'Watch this video on YouTube';
    frame.replaceWith(link);
  }

  // A static copy runs no scripts, embeds, trackers, or redirects.
  document.querySelectorAll([
    'script', 'noscript', 'iframe', 'object', 'embed', 'base', 'meta[http-equiv="refresh" i]', 'meta[http-equiv="content-security-policy" i]',
    'link[rel~="preload"]', 'link[rel~="modulepreload"]', 'link[rel~="prefetch"]', 'link[rel~="preconnect"]', 'link[rel~="dns-prefetch"]', 'link[rel~="manifest"]',
  ].join(',')).forEach(el => el.remove());
  for (const el of document.querySelectorAll('*')) {
    for (const { name } of [...el.attributes]) if (/^on/i.test(name)) el.removeAttribute(name);
  }
  for (const el of document.querySelectorAll('a[href], area[href], link[href], source[src], video[src], audio[src], form[action]')) {
    const attr = el.hasAttribute('href') ? 'href' : el.hasAttribute('src') ? 'src' : 'action';
    const value = el.getAttribute(attr);
    if (value && !value.startsWith('#') && !/^(data|mailto|tel|javascript):/i.test(value)) {
      try { el.setAttribute(attr, resolve(value)); } catch { /* leave as-is */ }
    }
  }

  // Mark the copy as an archive: a notice at the top, and no search indexing of the duplicate.
  const head = document.head;
  head.querySelector('link[rel="canonical"]')?.remove();
  head.insertAdjacentHTML('afterbegin', `<meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="${url}">`);
  const day = (iso, timeZone) => new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone });
  const notice = document.createElement('div');
  notice.setAttribute('role', 'note');
  notice.style.cssText = 'display:block;box-sizing:border-box;width:100%;margin:0;padding:10px 16px;background:#111114;color:#ededf2;font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;text-align:center;position:relative;z-index:2147483647;';
  notice.innerHTML = `Archived copy of <a href="${url}" style="color:#a193ff;text-decoration:underline;">${new URL(url).hostname}</a>`
    + `${published ? `, originally published ${day(published, 'UTC')}` : ''}.`
    + (archive
      ? ` Saved by the <a href="${archive}" style="color:#a193ff;text-decoration:underline;">Internet Archive</a> on ${day(archived, 'UTC')} and copied here ${day(captured)}.`
      : ` Captured ${day(captured)}.`)
    + `${restored ? ' Images that were broken on the live page were restored from the Internet Archive.' : ''}`
    + `${trimmed ? ' Ads and unrelated sections of the page were left out.' : ''}`;
  document.body.prepend(notice);

  return `<!DOCTYPE html>\n${document.documentElement.outerHTML}`;
}

// ---- Main ----

async function main() {
  const { source, images: swaps, removes, outDir } = parseArgs(process.argv.slice(2));
  const { url, archive, archived, timestamp } = source;
  fs.rmSync(path.join(outDir, 'images'), { recursive: true, force: true });
  fs.mkdirSync(path.join(outDir, 'images'), { recursive: true });
  const captured = new Date().toISOString();
  const browser = await launchBrowser();
  try {
    const cdp = await connect(browser.wsUrl);
    const page = await openPage(cdp);
    await page.send('Page.enable');
    await page.send('Emulation.setDeviceMetricsOverride', { ...VIEWPORT, deviceScaleFactor: 1, mobile: false });

    console.log(`Loading ${source.load}`);
    const loaded = page.once('Page.loadEventFired');
    const { errorText } = await page.send('Page.navigate', { url: source.load });
    if (errorText) throw new Error(`Could not load the page: ${errorText}`);
    await Promise.race([loaded, sleep(45000)]);
    await page.isolate();
    // Remove before scrolling, so endless feeds don't load more, and again after, for
    // anything that loaded late.
    let removed = removes.length ? await page.evaluate(removeElements, removes) : 0;
    console.log('  Waiting for images and fonts');
    await page.evaluate(settlePage);
    if (removes.length) {
      removed += await page.evaluate(removeElements, removes);
      console.log(`  Removed ${removed} elements`);
    }
    const info = await page.evaluate(readPage);
    if (archive && info.site === 'web.archive.org') info.site = new URL(url).hostname;

    const broken = info.images.filter(img => !img.ok && /^https?:/.test(img.src));
    for (const img of broken) console.log(`  Broken image on the page: ${img.src}`);
    console.log('  Saving screenshot');
    await saveScreenshot(page, path.join(outDir, swaps.length ? 'as-captured.png' : 'snapshot.png'));

    const used = new Set();
    const restored = [];
    for (const { match, source } of swaps) {
      const original = info.images.find(img => img.src.includes(match));
      if (!original) { console.warn(`  No image on the page matches "${match}"; skipped.`); continue; }
      const file = await download(waybackRaw(source));
      const local = saveImage(outDir, original.src, file, used);
      await page.evaluate(swapImage, match, `data:${file.type};base64,${file.buffer.toString('base64')}`, local);
      restored.push({ original: original.src, source, file: local });
      console.log(`  Restored ${original.src} -> ${local}`);
    }
    if (restored.length) await saveScreenshot(page, path.join(outDir, 'snapshot.png'));

    console.log('  Saving PDF');
    const { data: pdf } = await page.send('Page.printToPDF', { printBackground: true, generateTaggedPDF: true });
    fs.writeFileSync(path.join(outDir, 'snapshot.pdf'), Buffer.from(pdf, 'base64'));

    // Collect what the HTML copy needs from outside the page: stylesheets, images, video thumbnails.
    console.log('  Saving stylesheets and images for the HTML copy');
    const css = await collectStylesheets(cdp, page);
    const images = {};
    for (const { src, ok } of info.images) {
      if (!ok || !/^https?:/.test(src) || src in images || restored.some(r => r.original === src)) continue;
      try {
        const viaArchive = timestamp && !/^https?:\/\/web\.archive\.org\//i.test(src);
        const file = await download(viaArchive ? `https://web.archive.org/web/${timestamp}im_/${src}` : src, source.load);
        if (!file.type.startsWith('image/')) throw new Error(`got ${file.type || 'an unknown type'} for ${src}`);
        images[src] = saveImage(outDir, src, file, used);
      } catch (error) { console.warn(`  Image not saved (${error.message})`); }
    }
    const youtube = {};
    for (const id of info.youtube) {
      try { youtube[id] = saveImage(outDir, `https://i.ytimg.com/youtube-${id}.jpg`, await download(`https://i.ytimg.com/vi/${id}/hqdefault.jpg`), used); } catch { /* falls back to a text link */ }
    }

    const html = await page.evaluate(serializeForArchive, { url, loadUrl: source.load, archive, archived, timestamp, captured, published: info.published, restored: restored.length > 0, trimmed: removes.length > 0, css, images, youtube });
    fs.writeFileSync(path.join(outDir, 'snapshot.html'), html);

    const record = {
      url, title: info.title, site: info.site, published: info.published, captured,
      ...(archive && { archive, archived }),
      restoredImages: restored,
      ...(removes.length && { removed: removes }),
      youtube: info.youtube.map(id => `https://www.youtube.com/watch?v=${id}`),
    };
    fs.writeFileSync(path.join(outDir, 'snapshot.json'), `${JSON.stringify(record, null, 2)}\n`);
    cdp.close();
    console.log(`Saved to ${path.relative(repoRoot, outDir)}${path.sep}`);
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error.message);
  process.exit(1);
});
