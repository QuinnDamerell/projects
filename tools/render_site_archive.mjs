#!/usr/bin/env node
// Render a local website archive to snapshot.png and snapshot.pdf without
// rebuilding, sanitizing, or deleting its HTML. Requires Node 22+ and Chrome/Edge.
// node tools/render_site_archive.mjs docs/assets/media/<slug>
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';

const root = path.resolve(process.argv[2] ?? '');
const paginated = process.argv.includes('--paginated');
if (!process.argv[2] || !fs.existsSync(path.join(root, 'manifest.json')) || !fs.existsSync(path.join(root, 'snapshot.html'))) {
  throw new Error('Usage: node tools/render_site_archive.mjs <local-archive-directory> [--paginated]');
}
const browserPath = [process.env.CHROME_PATH,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium',
].find(candidate => candidate && fs.existsSync(candidate));
if (!browserPath) throw new Error('Chrome or Edge not found; set CHROME_PATH.');

const types = {'.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.json':'application/json',
  '.png':'image/png', '.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.gif':'image/gif', '.svg':'image/svg+xml',
  '.webp':'image/webp', '.ico':'image/x-icon', '.ttf':'font/ttf', '.woff':'font/woff', '.woff2':'font/woff2'};
const server = http.createServer((request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    let file = path.resolve(root, '.' + pathname);
    const relative = path.relative(root, file);
    if (relative.startsWith('..') || path.isAbsolute(relative)) throw new Error('Invalid path');
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    response.setHeader('Content-Type', types[path.extname(file).toLowerCase()] ?? 'application/octet-stream');
    response.end(fs.readFileSync(file));
  } catch {
    response.writeHead(404); response.end('File not found');
  }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'site-archive-render-'));
const proc = spawn(browserPath, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`,
  '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--mute-audio',
  '--disable-background-networking', '--window-size=1280,900', 'about:blank'],
  {stdio:['ignore','ignore','pipe'], windowsHide:true});
const exited = new Promise(resolve => proc.once('exit', resolve));
let socket;
try {
  const wsUrl = await new Promise((resolve, reject) => {
    let log = '';
    const timer = setTimeout(() => reject(new Error('Browser startup timed out')), 30000);
    proc.stderr.on('data', chunk => {
      log += chunk;
      const match = log.match(/DevTools listening on (ws:\/\/\S+)/);
      if (match) { clearTimeout(timer); resolve(match[1]); }
    });
    proc.once('error', error => { clearTimeout(timer); reject(error); });
    exited.then(code => { clearTimeout(timer); reject(new Error(`Browser exited: ${code}`)); });
  });
  socket = new WebSocket(wsUrl);
  await new Promise((resolve, reject) => { socket.onopen=resolve; socket.onerror=reject; });
  let nextId=0;
  const pending=new Map(), events=[];
  const external=new Set();
  socket.onmessage=({data}) => {
    const message=JSON.parse(data);
    if (message.id) {
      const call=pending.get(message.id); if (!call) return;
      pending.delete(message.id); clearTimeout(call.timer);
      if (message.error) call.reject(new Error(`${call.method}: ${message.error.message}`));
      else call.resolve(message.result);
    } else {
      for (const listener of [...events]) listener(message);
      if (message.method==='Network.requestWillBeSent') {
        const url=message.params.request.url;
        if (/^https?:/.test(url) && !url.startsWith(origin + '/')) external.add(url);
      }
    }
  };
  const send=(method,params={},sessionId) => new Promise((resolve,reject) => {
    const id=++nextId;
    const timer=setTimeout(() => {pending.delete(id); reject(new Error(`${method} timed out`));},30000);
    pending.set(id,{method,resolve,reject,timer}); socket.send(JSON.stringify({id,method,params,sessionId}));
  });
  const {targetId}=await send('Target.createTarget',{url:'about:blank'});
  const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
  const page=(method,params={}) => send(method,params,sessionId);
  await page('Page.enable'); await page('Network.enable');
  await page('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  await page('Emulation.setDeviceMetricsOverride',{width:1280,height:900,deviceScaleFactor:1,mobile:false});
  let loadTimer;
  const loaded=new Promise((resolve,reject) => {
    loadTimer=setTimeout(() => reject(new Error('Local page load timed out')),15000);
    const listener=message => {
      if (message.method==='Page.loadEventFired' && message.sessionId===sessionId) {
        clearTimeout(loadTimer); events.splice(events.indexOf(listener),1); resolve();
      }
    };
    events.push(listener);
  });
  await page('Page.navigate',{url:origin+'/snapshot.html'});
  await loaded;
  const {result}=await page('Runtime.evaluate',{expression:`(async()=>{
    await Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,5000))]);
    await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));
    return {title:document.title,broken:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.getAttribute('src'))};
  })()`,awaitPromise:true,returnByValue:true});
  if (result.value?.broken.length) throw new Error('Broken images: '+JSON.stringify(result.value.broken));
  if (external.size) throw new Error('Unexpected remote resources: '+JSON.stringify([...external]));
  const {cssContentSize}=await page('Page.getLayoutMetrics');
  const height=Math.ceil(Math.max(900,cssContentSize.height));
  if (!paginated && height>19000) throw new Error('Homepage is too tall for a single-page reference PDF; use --paginated for a long article or transcript.');
  await page('Emulation.setDeviceMetricsOverride',{width:1280,height,deviceScaleFactor:1,mobile:false});
  const screenshot=await page('Page.captureScreenshot',{format:'png'});
  const pdf=await page('Page.printToPDF',{printBackground:true,generateTaggedPDF:true,
    ...(paginated
      ? {paperWidth:8.27,paperHeight:11.69,marginTop:.4,marginRight:.4,marginBottom:.4,marginLeft:.4}
      : {paperWidth:1280/96,paperHeight:(height+20)/96,marginTop:0,marginRight:0,marginBottom:0,marginLeft:0}),scale:1});
  fs.writeFileSync(path.join(root,'snapshot.png'),Buffer.from(screenshot.data,'base64'));
  fs.writeFileSync(path.join(root,'snapshot.pdf'),Buffer.from(pdf.data,'base64'));
  const metadataPath=path.join(root,'snapshot.json');
  const metadata=fs.existsSync(metadataPath)?JSON.parse(fs.readFileSync(metadataPath,'utf8')):{};
  metadata.screenshot={file:'snapshot.png',width:1280,height};
  metadata.pdf=paginated ? {file:'snapshot.pdf',layout:'A4 paginated'} : {file:'snapshot.pdf',pages:1};
  fs.writeFileSync(metadataPath,JSON.stringify(metadata,null,2)+'\n');
  console.log(JSON.stringify({root,...result.value,width:1280,height,external:[...external]},null,2));
} finally {
  socket?.close(); proc.kill();
  await Promise.race([exited,new Promise(resolve=>setTimeout(resolve,3000))]);
  server.closeAllConnections(); server.close();
  const resolvedProfile=path.resolve(profile), resolvedTemp=path.resolve(os.tmpdir());
  if (path.dirname(resolvedProfile)===resolvedTemp && path.basename(resolvedProfile).startsWith('site-archive-render-')) {
    try { fs.rmSync(resolvedProfile,{recursive:true,force:true,maxRetries:3,retryDelay:200}); } catch { /* Chrome may still be releasing its temporary profile. */ }
  }
}
