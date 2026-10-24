import assert from 'node:assert/strict';
import test from 'node:test';
import { mountWhipApp } from '../../docs/javascripts/whip-app.js';

class Target {
  listeners = new Map();
  dataset = {};
  attributes = new Map();
  textContent = '';
  disabled = false;
  hidden = false;
  addEventListener(name, callback) {
    if (!this.listeners.has(name)) this.listeners.set(name, new Set());
    this.listeners.get(name).add(callback);
  }
  removeEventListener(name, callback) { this.listeners.get(name)?.delete(callback); }
  emit(name, event = {}) {
    for (const listener of this.listeners.get(name) || []) listener(event);
  }
  count(name) { return this.listeners.get(name)?.size || 0; }
  setAttribute(name, value) { this.attributes.set(name, value); }
  showModal() { this.open = true; }
  close() { this.open = false; }
  focus() { this.focused = true; }
}

function fixture(options = {}) {
  const calls = [];
  const sources = [];
  const contexts = [];
  const timers = new Map();
  let timerId = 0;
  const win = new Target();
  const doc = new Target();
  const root = new Target();
  const ids = ['crack-button', 'motion-button', 'sound-status', 'motion-status', 'whip-step', 'crack-step',
    'welcome-dialog', 'welcome-ok', 'motion-notice', 'audio-fallback'];
  const elements = Object.fromEntries(ids.map(id => [id, new Target()]));
  elements['motion-notice'].hidden = true;
  elements['audio-fallback'].hidden = true;
  const nativeAudio = new Target();
  nativeAudio.paused = true;
  nativeAudio.pause = () => { nativeAudio.paused = true; };
  nativeAudio.play = () => { nativeAudio.paused = false; nativeAudio.emit('play'); };
  doc.querySelector = selector => elements[selector.slice(1)];
  doc.querySelectorAll = selector => selector === 'audio' ? [nativeAudio] : [];
  root.querySelector = selector => /#(?:whip|crack)-step$/.test(selector) ? elements[selector.slice(1)] : null;
  root.ownerDocument = doc;
  doc.documentElement = new Target();
  doc.defaultView = win;
  win.isSecureContext = options.secure !== false;
  win.navigator = {};
  win.location = { search: options.search || '' };
  doc.body = { children: [], append(element) { this.children.push(element); } };
  if (options.audioSession) win.navigator.audioSession = { type: 'auto' };
  if (options.userAgent) {
    win.navigator.userAgent = options.userAgent;
    win.navigator.maxTouchPoints = options.touchPoints ?? 5;
  }
  const media = [];
  doc.createElement = tag => {
    const element = new Target();
    Object.assign(element, { tag, paused: true });
    element.play = () => {
      calls.push('media-play');
      element.paused = false;
      return options.mediaRefused ? Promise.reject(new Error('NotAllowedError')) : Promise.resolve();
    };
    element.pause = () => { calls.push('media-pause'); element.paused = true; };
    element.remove = () => { element.removed = true; };
    media.push(element);
    return element;
  };
  if (options.orientation !== false) {
    win.DeviceOrientationEvent = {};
    if (options.permission !== false) {
      win.DeviceOrientationEvent.requestPermission = () => {
        calls.push('permission');
        return options.permission ? options.permission() : Promise.resolve('granted');
      };
    }
  }
  let fetchFailures = options.failFetches || 0;
  let decodeFailures = options.failDecodes || 0;
  win.fetch = async url => {
    const file = url.pathname.split('/').pop();
    calls.push(`fetch:${file}`);
    if (options.fetchError || fetchFailures-- > 0) throw new Error('Network failed');
    return { ok: true, arrayBuffer: async () => file };
  };
  win.setTimeout = (callback, delay) => {
    const id = ++timerId;
    timers.set(id, { callback, delay });
    return id;
  };
  win.clearTimeout = id => timers.delete(id);
  const intervals = new Map();
  win.setInterval = callback => {
    const id = ++timerId;
    intervals.set(id, callback);
    return id;
  };
  win.clearInterval = id => intervals.delete(id);
  if (options.audio !== false) {
    win.AudioContext = class {
      state = 'suspended';
      destination = {};
      constructor() { contexts.push(this); calls.push('context'); }
      resume() {
        calls.push('resume');
        this.state = 'running';
        return Promise.resolve();
      }
      suspend() { calls.push('suspend'); this.state = 'suspended'; return Promise.resolve(); }
      decodeAudioData(file, success) {
        calls.push('decode');
        if (decodeFailures-- > 0) return Promise.reject(new Error('Bad audio'));
        // Older WebKit: callbacks only, no promise.
        if (options.callbackDecode) { queueMicrotask(() => success({ file })); return undefined; }
        return Promise.resolve({ file });
      }
      createBufferSource() {
        const source = {
          loop: true,
          stopped: false,
          connect() {},
          disconnect() {},
          start() { calls.push('play'); sources.push(this); },
          stop() { this.stopped = true; },
        };
        return source;
      }
    };
  }
  const app = mountWhipApp(root);
  return { root, win, doc, app, elements, calls, sources, contexts, timers, nativeAudio, media,
    click(id) { elements[id].emit('click'); },
    // Everything except the sound downloads that start as the page opens.
    actions() { return calls.filter(call => !call.startsWith('fetch:')); },
    downloads() { return calls.filter(call => call.startsWith('fetch:')).length; },
    // The phone turned in its screen plane: negative toward the screen's left
    // edge (whip), positive toward its right (crack). The screen leans back 30
    // degrees, as when held up to look at it.
    tilt(degrees) {
      const [lean, turn] = [30 * Math.PI / 180, degrees * Math.PI / 180];
      win.emit('deviceorientation', {
        alpha: 0,
        beta: Math.asin(Math.cos(lean) * Math.cos(turn)) * 180 / Math.PI,
        gamma: Math.atan2(Math.cos(lean) * Math.sin(turn), Math.sin(lean)) * 180 / Math.PI,
      });
    },
    runIntervals() { for (const callback of intervals.values()) callback(); },
    intervalCount() { return intervals.size; },
    runSensorTimeout() {
      for (const [id, timer] of timers) {
        if (timer.delay === 7000) { timers.delete(id); timer.callback(); }
      }
    },
  };
}

const flush = () => new Promise(resolve => setImmediate(resolve));

test('startup and button playback never request sensor permission', async () => {
  const f = fixture();
  assert.deepEqual(f.calls, ['fetch:Whip1.wav', 'fetch:Crack1.wav', 'fetch:WhipAndCrack.wav'],
    'the sounds download as the page opens, with no AudioContext before a tap');
  assert.equal(f.win.count('deviceorientation'), 0);
  f.click('crack-button');
  assert.ok(f.calls.includes('resume'), 'audio unlock starts in click, before async loading');
  await flush();
  assert.equal(f.calls.filter(call => call === 'decode').length, 3);
  assert.equal(f.sources.length, 1);
  assert.equal(f.sources[0].loop, false);
  assert.equal(f.calls.includes('permission'), false);
  assert.equal(f.win.count('deviceorientation'), 0);
  f.click('crack-button');
  await flush();
  assert.equal(f.sources.length, 2);
  assert.equal(f.calls.filter(call => call === 'decode').length, 3, 'decoded sounds are reused');
  assert.equal(f.downloads(), 3, 'taps reuse the preloaded downloads');
  f.app.destroy();
});

test('sound leaves the iOS audio session at its default', async () => {
  // 'playback' did not get past Silent Mode on an iPhone; the silent clip does.
  const f = fixture({ audioSession: true });
  f.click('crack-button');
  assert.equal(f.win.navigator.audioSession.type, 'auto');
  await flush();
  assert.equal(f.sources.length, 1);
  f.app.destroy();
});

const IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const IPAD = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15';

test('on iPhone a looping silent clip starts inside the tap so Silent Mode does not mute', async () => {
  const f = fixture({ userAgent: IPHONE });
  assert.equal(f.media.length, 0, 'nothing plays before a tap');
  f.click('crack-button');
  assert.deepEqual(f.actions().slice(0, 3), ['media-play', 'context', 'resume'],
    'the media channel starts in the tap, before Web Audio');
  const [clip] = f.media;
  assert.equal(clip.tag, 'audio');
  assert.equal(clip.loop, true);
  assert.equal(clip.disableRemotePlayback, true);
  assert.equal(clip.attributes.get('x-webkit-airplay'), 'deny');
  assert.match(clip.src, /^blob:/);
  assert.equal(f.nativeAudio.count('play'), 1, 'the clip is not one of the page players');
  await flush();
  assert.equal(f.sources.length, 1);
  f.doc.hidden = true;
  f.doc.emit('visibilitychange');
  assert.equal(clip.paused, true, 'hidden pages show no lock screen player');
  f.doc.hidden = false;
  f.click('welcome-ok');
  await flush();
  assert.equal(f.media.length, 1, 'later taps reuse the same clip');
  assert.equal(clip.paused, false);
  assert.equal(f.win.count('deviceorientation'), 1, 'the clip playing does not count as the native player');
  for (const value of [45, -40, 40]) f.tilt(value);
  assert.deepEqual(f.sources.slice(1).map(source => source.buffer.file), ['Whip1.wav', 'Crack1.wav']);
  f.app.destroy();
  assert.equal(clip.paused, true);
});

test('iPadOS gets the silent clip; Macs, Android and desktop browsers do not', async () => {
  const cases = [
    [{ userAgent: IPAD, touchPoints: 5 }, 1],
    [{ userAgent: IPAD, touchPoints: 0 }, 0],
    [{ userAgent: 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Mobile Safari/537.36' }, 0],
    [{}, 0],
  ];
  for (const [options, clips] of cases) {
    const f = fixture(options);
    f.click('crack-button');
    await flush();
    assert.equal(f.media.length, clips, JSON.stringify(options));
    assert.equal(f.sources.length, 1);
    f.app.destroy();
  }
});

test('a refused silent clip still lets the tap play the sound', async () => {
  const f = fixture({ userAgent: IPHONE, mediaRefused: true });
  f.click('crack-button');
  await flush();
  assert.equal(f.sources.length, 1);
  assert.equal(f.elements['sound-status'].dataset.error, 'false');
  f.app.destroy();
});

test('a failed preload downloads again on the first tap', async () => {
  const f = fixture({ failFetches: 1 });
  await flush();
  assert.equal(f.downloads(), 3);
  f.click('crack-button');
  await flush();
  assert.equal(f.downloads(), 6);
  assert.equal(f.sources.length, 1);
  assert.equal(f.elements['audio-fallback'].hidden, true);
  f.app.destroy();
});

test('a failed decode downloads fresh bytes for the next tap', async () => {
  const f = fixture({ failDecodes: 1 });
  f.click('crack-button');
  await flush();
  assert.equal(f.sources.length, 0);
  assert.equal(f.elements['sound-status'].dataset.error, 'true');
  f.click('crack-button');
  await flush();
  assert.equal(f.downloads(), 6, 'decoding took over the first bytes');
  assert.equal(f.sources.length, 1);
  f.app.destroy();
});

test('older WebKit with callback-only decoding still plays', async () => {
  const f = fixture({ callbackDecode: true });
  f.click('welcome-ok');
  await flush();
  assert.equal(f.win.count('deviceorientation'), 1);
  for (const value of [45, -40, 40]) f.tilt(value);
  assert.deepEqual(f.sources.map(source => source.buffer.file), ['Whip1.wav', 'Crack1.wav']);
  f.app.destroy();
});

test('each arrival shows the welcome dialog and OK requests motion in its click', async () => {
  for (let arrival = 0; arrival < 2; arrival += 1) {
    const f = fixture();
    assert.equal(f.elements['welcome-dialog'].open, true);
    assert.deepEqual(f.actions(), []);
    f.click('welcome-ok');
    assert.deepEqual(f.actions().slice(0, 3), ['permission', 'context', 'resume']);
    assert.equal(f.elements['welcome-dialog'].open, false);
    assert.equal(f.root.focused, true);
    await flush();
    f.tilt(45);
    assert.equal(f.elements['motion-notice'].hidden, true);
    f.app.destroy();
  }
});

test('?debug shows the live orientation and why a swing did or did not sound', async () => {
  const f = fixture({ search: '?debug' });
  const panel = f.media.find(element => element.tag === 'pre');
  assert.ok(f.doc.body.children.includes(panel));
  assert.match(panel.textContent, /motion : off/);
  assert.match(panel.textContent, /tilt   :   none no reading yet/);
  f.click('welcome-ok');
  await flush();
  f.tilt(-25);
  f.runIntervals();
  assert.match(panel.textContent, /tilt   :  -25\.0 middle: neither/);
  assert.match(panel.textContent, /next   : whip: tilt left past -30/);
  assert.match(panel.textContent, /lean   :   30\.0 from upright/);
  assert.match(panel.textContent, /alpha    0\.0 beta /);
  f.tilt(-40);
  f.tilt(-70);
  f.runIntervals();
  assert.match(panel.textContent, /tilt   :  -70\.0 whip side/);
  assert.match(panel.textContent, /sounds : whip -40/);
  assert.match(panel.textContent, /stroke :  -70\.0 to  -40\.0 since last sound/);
  assert.match(panel.textContent, /next   : crack: tilt right past \+30/);
  assert.match(panel.textContent, /audio  : running, iOS silent clip not used/);
  assert.match(panel.textContent, /L -+O-+\|/, 'the gauge marks the tilt left of the whip threshold');
  f.win.emit('deviceorientation', { alpha: null, beta: null, gamma: null });
  f.runIntervals();
  assert.match(panel.textContent, /alpha   none beta   none gamma   none/);
  assert.match(panel.textContent, /tilt   :   none unusable reading/);
  f.app.destroy();
  assert.equal(panel.removed, true);
  assert.equal(f.intervalCount(), 0);
});

test('without ?debug there is no debug display or timer', () => {
  const f = fixture();
  assert.equal(f.media.length, 0);
  assert.equal(f.doc.body.children.length, 0);
  assert.equal(f.intervalCount(), 0);
  f.app.destroy();
});

test('the ok focus ring waits for the keyboard', () => {
  const f = fixture();
  assert.equal(f.doc.count('keydown'), 1);
  assert.equal(f.doc.documentElement.dataset.keyboard, undefined, 'no ring on arrival');
  f.doc.emit('keydown');
  assert.equal(f.doc.documentElement.dataset.keyboard, 'true');
  f.app.destroy();
  assert.equal(f.doc.count('keydown'), 0);
});

test('welcome OK closes on denied permission and exposes a working retry', async () => {
  let requests = 0;
  const f = fixture({ permission: () => Promise.resolve(++requests === 1 ? 'denied' : 'granted') });
  f.click('welcome-ok');
  await flush();
  assert.equal(f.elements['welcome-dialog'].open, false);
  assert.equal(f.elements['motion-notice'].hidden, false);
  assert.match(f.elements['motion-status'].textContent, /permission/);
  f.click('motion-button');
  await flush();
  f.tilt(45);
  assert.equal(requests, 2);
  assert.equal(f.elements['motion-notice'].hidden, true);
  f.app.destroy();
});

test('dismissing the dialog does not silently grant sensor access', () => {
  const f = fixture();
  f.elements['welcome-dialog'].emit('cancel');
  assert.equal(f.win.count('deviceorientation'), 0);
  assert.equal(f.elements['motion-notice'].hidden, false);
  assert.deepEqual(f.actions(), []);
  f.app.destroy();
});

test('permission and audio unlock start in gesture, then predecoded motion alternates', async () => {
  const f = fixture();
  f.click('motion-button');
  assert.deepEqual(f.actions().slice(0, 3), ['permission', 'context', 'resume']);
  assert.equal(f.win.count('deviceorientation'), 0, 'listen only after audio and permission are ready');
  await flush();
  assert.equal(f.win.count('deviceorientation'), 1);
  assert.equal(f.calls.filter(call => call === 'decode').length, 3);
  assert.equal(f.sources.length, 0);
  for (const value of [45, -29, -40, -50, 0, 29, 31]) f.tilt(value);
  assert.equal(f.sources.length, 2);
  assert.deepEqual(f.sources.map(source => source.buffer.file), ['Whip1.wav', 'Crack1.wav']);
  assert.equal(f.sources[0].stopped, true, 'a new stroke stops the previous sound tail');
  assert.equal(f.elements['motion-button'].attributes.get('aria-pressed'), 'true');
  f.click('motion-button');
  assert.equal(f.win.count('deviceorientation'), 0);
  assert.ok(f.sources.every(source => source.stopped));
  f.tilt(-40);
  assert.equal(f.sources.length, 2);
  f.app.destroy();
});

test('motion works on browsers without requestPermission after explicit opt-in', async () => {
  const f = fixture({ permission: false });
  f.tilt(-50);
  assert.equal(f.sources.length, 0);
  f.click('motion-button');
  await flush();
  f.tilt(45);
  f.tilt(-50);
  assert.equal(f.sources.length, 1);
  assert.equal(f.calls.includes('permission'), false);
  f.app.destroy();
});

test('repeated large swings keep the same sound direction and stop each previous tail', async () => {
  const f = fixture();
  f.click('welcome-ok');
  await flush();
  f.tilt(45);
  for (let cycle = 0; cycle < 5; cycle += 1) {
    // Past sideways, beta changes sign; the swing direction must not.
    for (const angle of [-40, -80, -100, -140, -100, -80, -70, -20, 40, 80, 100, 140, 100, 80, 79]) f.tilt(angle);
  }
  assert.deepEqual(f.sources.map(source => source.buffer.file),
    Array.from({ length: 5 }, () => ['Whip1.wav', 'Crack1.wav']).flat());
  assert.ok(f.sources.slice(0, -1).every(source => source.stopped));
  assert.equal(f.sources.at(-1).stopped, false);
  assert.equal(f.elements['motion-notice'].hidden, true);
  f.app.destroy();
});

test('insecure or missing motion APIs retain the button fallback', async () => {
  for (const options of [{ secure: false }, { orientation: false }]) {
    const f = fixture(options);
    f.click('motion-button');
    assert.deepEqual(f.actions(), []);
    assert.match(f.elements['motion-status'].textContent, /HTTPS|does not provide/);
    f.click('crack-button');
    await flush();
    assert.equal(f.sources.length, 1);
    f.app.destroy();
  }
});

test('denied or rejected permission leaves motion off and button usable', async () => {
  for (const permission of [() => Promise.resolve('denied'), () => Promise.reject(new Error('NotAllowedError'))]) {
    const f = fixture({ permission });
    f.click('motion-button');
    await flush();
    assert.equal(f.win.count('deviceorientation'), 0);
    assert.match(f.elements['motion-status'].textContent, /permission/);
    assert.equal(f.elements['motion-button'].disabled, false);
    f.click('crack-button');
    await flush();
    assert.equal(f.sources.length, 1);
    f.app.destroy();
  }
});

test('missing Web Audio and download failures explain the native audio fallback', async () => {
  for (const options of [{ audio: false }, { fetchError: true }]) {
    const f = fixture(options);
    f.click('crack-button');
    await flush();
    assert.match(f.elements['sound-status'].textContent, /original audio player/);
    assert.equal(f.elements['sound-status'].dataset.error, 'true');
    assert.equal(f.elements['audio-fallback'].hidden, false);
    assert.equal(f.elements['crack-button'].disabled, false);
    f.click('motion-button');
    await flush();
    assert.equal(f.win.count('deviceorientation'), 0);
    assert.equal(f.elements['motion-button'].disabled, false);
    f.app.destroy();
  }
});

test('an API with no valid readings times out without playing', async () => {
  const f = fixture();
  f.click('motion-button');
  await flush();
  f.win.emit('deviceorientation', { alpha: 0, beta: null, gamma: 0 });
  f.win.emit('deviceorientation', { alpha: 0, beta: NaN, gamma: 0 });
  f.runSensorTimeout();
  assert.equal(f.sources.length, 0);
  assert.equal(f.win.count('deviceorientation'), 0);
  assert.match(f.elements['motion-status'].textContent, /No motion readings/);
  assert.equal(f.elements['motion-button'].attributes.get('aria-pressed'), 'false');
  f.app.destroy();
});

test('hiding a page stops audio and sensors and never auto-resumes', async () => {
  const f = fixture();
  f.click('motion-button');
  await flush();
  f.tilt(45);
  f.tilt(-45);
  f.doc.hidden = true;
  f.doc.emit('visibilitychange');
  assert.equal(f.win.count('deviceorientation'), 0);
  assert.equal(f.contexts[0].state, 'suspended');
  assert.equal(f.sources[0].stopped, true);
  f.doc.hidden = false;
  f.doc.emit('visibilitychange');
  f.tilt(-45);
  assert.equal(f.sources.length, 1);
  assert.equal(f.win.count('deviceorientation'), 0);
  f.click('motion-button');
  await flush();
  f.tilt(45);
  assert.equal(f.sources.length, 1, 're-enabling starts again from a whip, so tilting right is silent');
  f.tilt(-45);
  assert.equal(f.sources.length, 2);
  assert.equal(f.sources[1].buffer.file, 'Whip1.wav');
  f.app.destroy();
  assert.equal(f.win.count('pagehide'), 0);
  assert.equal(f.doc.count('visibilitychange'), 0);
});

test('a pending permission response cannot restart motion after pagehide', async () => {
  let grant;
  const f = fixture({ permission: () => new Promise(resolve => { grant = resolve; }) });
  f.click('motion-button');
  f.win.emit('pagehide');
  grant('granted');
  await flush();
  assert.equal(f.win.count('deviceorientation'), 0);
  assert.equal(f.sources.length, 0);
  assert.equal(f.elements['motion-button'].attributes.get('aria-pressed'), 'false');
  f.app.destroy();
});

test('an interrupted audio context stops motion until the next gesture', async () => {
  const f = fixture();
  f.click('motion-button');
  await flush();
  f.tilt(45);
  f.contexts[0].state = 'suspended';
  f.tilt(-45);
  assert.equal(f.sources.length, 0);
  assert.equal(f.win.count('deviceorientation'), 0);
  assert.match(f.elements['motion-status'].textContent, /paused/);
  f.app.destroy();
});

test('native audio and Web Audio take turns and both stop when hidden', async () => {
  const f = fixture();
  f.nativeAudio.play();
  f.click('crack-button');
  assert.equal(f.nativeAudio.paused, true);
  await flush();
  assert.equal(f.sources.length, 1);
  f.nativeAudio.play();
  assert.equal(f.sources[0].stopped, true);
  f.click('motion-button');
  assert.equal(f.nativeAudio.paused, true);
  await flush();
  assert.equal(f.win.count('deviceorientation'), 1);
  f.nativeAudio.play();
  assert.equal(f.win.count('deviceorientation'), 0);
  f.doc.hidden = true;
  f.doc.emit('visibilitychange');
  assert.equal(f.nativeAudio.paused, true);
  f.app.destroy();
  assert.equal(f.nativeAudio.count('play'), 0);
});

test('native playback cancels a pending Web Audio playback request', async () => {
  const f = fixture();
  f.click('crack-button');
  f.nativeAudio.play();
  await flush();
  assert.equal(f.sources.length, 0);
  assert.equal(f.nativeAudio.paused, false);
  f.app.destroy();
});
