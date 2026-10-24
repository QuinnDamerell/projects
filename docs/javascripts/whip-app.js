// MainPage.xaml.cs started in Back, whipped once the roll passed -30 degrees,
// then cracked once it passed +30, strictly alternating.
export const SWING_DEGREES = 30;
const FLAT = Math.sin(20 * Math.PI / 180);

// How far the phone is turned within its own screen plane, like a steering
// wheel, as in the app's Whip and Crack diagrams: 0 is upright, negative turns
// the top toward the screen's left edge, positive toward its right edge.
// Only gravity matters, so the heading (alpha) is not needed. Raw gamma folds
// and jumps as an upright phone swings, so the angle comes from the bottom row
// of the full W3C Z-X'-Y'' rotation instead: the right edge's and top's
// upward components.
// https://www.w3.org/TR/orientation-event/#deviceorientation
export function screenTilt({ beta, gamma }) {
  if (![beta, gamma].every(Number.isFinite) || Math.abs(beta) > 180 || Math.abs(gamma) > 90) return null;
  const [b, g] = [beta, gamma].map(angle => angle * Math.PI / 180);
  const rightUp = -Math.cos(b) * Math.sin(g);
  const topUp = Math.sin(b);
  const upright = Math.hypot(rightUp, topUp);
  // How far the screen leans from upright, toward or away from you: 0 to 90.
  const lean = Math.acos(Math.min(1, upright)) * 180 / Math.PI;
  // Within 20 degrees of lying flat, gravity barely touches the screen plane,
  // so the angle is noise. Tilting toward or away from you never changes it.
  if (upright < FLAT) return { tilt: null, lean };
  return { tilt: Math.atan2(-rightUp, topUp) * 180 / Math.PI, lean };
}

export function createGestureTracker() {
  let expected;

  function reset() {
    expected = 'whip';
  }
  reset();

  return {
    reset,
    get next() { return expected; },
    sample(event) {
      const reading = screenTilt(event);
      if (!reading) return { valid: false, sound: null, tilt: null };
      const { tilt } = reading;
      if (tilt === null) return { valid: true, sound: null, tilt };
      // Within 30 degrees of upright or upside down is neither, so turning
      // past upside down cannot wrap from one side straight into the other.
      const zone = tilt < -SWING_DEGREES && tilt > SWING_DEGREES - 180 ? 'whip'
        : tilt > SWING_DEGREES && tilt < 180 - SWING_DEGREES ? 'crack' : null;
      if (zone !== expected) return { valid: true, sound: null, tilt };
      expected = zone === 'whip' ? 'crack' : 'whip';
      return { valid: true, sound: zone, tilt };
    },
  };
}

const SOUND_FILES = {
  whip: 'Whip1.wav',
  crack: 'Crack1.wav',
  combined: 'WhipAndCrack.wav',
};
const ASSETS = new URL('../assets/crack-the-whip/', import.meta.url);

// Half a second of 44.1 kHz, 16-bit mono silence as a WAV file.
function silentWav() {
  const samples = 22050;
  const view = new DataView(new ArrayBuffer(44 + samples * 2));
  const text = (offset, value) => [...value].forEach((letter, index) =>
    view.setUint8(offset + index, letter.charCodeAt(0)));
  text(0, 'RIFF');
  view.setUint32(4, 36 + samples * 2, true);
  text(8, 'WAVEfmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM
  view.setUint16(22, 1, true); // mono
  view.setUint32(24, 44100, true);
  view.setUint32(28, 44100 * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  text(36, 'data');
  view.setUint32(40, samples * 2, true);
  return new Blob([view.buffer], { type: 'audio/wav' });
}

function createSoundBank(doc) {
  const win = doc.defaultView;
  let context;
  let downloads;
  let loading;
  let buffers;
  let mediaChannel;
  const playing = new Set();
  const agent = win.navigator?.userAgent || '';
  // iPadOS reports a Mac user agent, but Macs have no multi-touch screen.
  const iOS = /iPhone|iPad|iPod/.test(agent) || (/Macintosh/.test(agent) && win.navigator?.maxTouchPoints > 1);

  // iOS plays Web Audio as ambient sound, which Silent Mode mutes, but plays
  // <audio> elements as media, which it does not. While any element plays, the
  // whole page's sound uses the media channel, so a looping silent clip keeps
  // the whip audible in Silent Mode. navigator.audioSession.type = 'playback'
  // is meant to do this, but did not on Quinn's iPhone.
  // https://bugs.webkit.org/show_bug.cgi?id=237322
  function holdMediaChannel() {
    if (!iOS) return;
    if (!mediaChannel) {
      mediaChannel = doc.createElement('audio');
      mediaChannel.setAttribute('x-webkit-airplay', 'deny');
      mediaChannel.disableRemotePlayback = true;
      mediaChannel.loop = true;
      mediaChannel.preload = 'auto';
      mediaChannel.src = URL.createObjectURL(silentWav());
    }
    // Must start inside the tap. If it is refused, only Silent Mode still mutes.
    const started = mediaChannel.play();
    started?.catch?.(() => {});
  }

  function releaseMediaChannel() {
    // Paused whenever the page is hidden, so iOS shows no lock screen player.
    mediaChannel?.pause();
  }

  function download() {
    downloads ||= Promise.all(Object.entries(SOUND_FILES).map(async ([key, file]) => {
      const response = await win.fetch(new URL(file, ASSETS));
      if (!response.ok) throw new Error(`Sound download failed (${response.status}).`);
      return [key, await response.arrayBuffer()];
    })).catch(error => {
      downloads = undefined;
      throw error;
    });
    return downloads;
  }

  // Download the original WAVs as the page opens, so the first tap only has to
  // decode them. Browsers only allow sound after a tap, so no AudioContext is
  // created here; a failed download is retried by that tap.
  function preload() {
    if (win.AudioContext || win.webkitAudioContext) download().catch(() => {});
  }

  function decode(data) {
    // Older WebKit reports decoding only through callbacks; newer browsers
    // also return a promise. Either settles this one.
    return new Promise((resolve, reject) => {
      const result = context.decodeAudioData(data, resolve, reject);
      if (result?.then) result.then(resolve, reject);
    });
  }

  function prepare() {
    const AudioContext = win.AudioContext || win.webkitAudioContext;
    if (!AudioContext) {
      return Promise.reject(new Error('This browser cannot use the sound button. Use the original audio player below.'));
    }
    try {
      holdMediaChannel();
      context ||= new AudioContext({ latencyHint: 'interactive' });
      // Called directly in the button's click handler, before any await/fetch.
      // iOS needs this user gesture to unlock sound for later sensor events.
      const resumed = context.state === 'running' ? Promise.resolve() : context.resume();
      if (!loading) {
        loading = download().then(files => Promise.all(files.map(([key, data]) =>
          decode(data).then(buffer => [key, buffer])))).then(entries => {
          buffers = Object.fromEntries(entries);
        }).catch(error => {
          // Decoding takes over the downloaded bytes, so a retry downloads again.
          loading = undefined;
          downloads = undefined;
          throw error;
        });
      }
      // All three original effects are decoded before motion is switched on.
      return Promise.all([resumed, loading]).then(() => {
        if (context.state !== 'running') {
          throw new Error('Sound is paused by your browser. Tap the button again to enable it.');
        }
      });
    } catch (error) {
      return Promise.reject(error);
    }
  }

  function play(key) {
    if (!buffers?.[key] || context?.state !== 'running') return false;
    const source = context.createBufferSource();
    source.buffer = buffers[key];
    source.loop = false;
    source.connect(context.destination);
    source.onended = () => {
      playing.delete(source);
      source.disconnect();
    };
    playing.add(source);
    try {
      source.start();
      return true;
    } catch (error) {
      playing.delete(source);
      source.disconnect();
      throw error;
    }
  }

  function stop() {
    for (const source of playing) {
      try { source.stop(); } catch { /* A source may have just ended. */ }
      source.disconnect();
    }
    playing.clear();
  }

  function suspend() {
    stop();
    releaseMediaChannel();
    if (context && context.state !== 'closed') context.suspend().catch(() => {});
  }

  function describe() {
    const clip = !iOS ? 'not used' : !mediaChannel ? 'not started' : mediaChannel.paused ? 'paused' : 'playing';
    return `${context?.state ?? 'not started'}, iOS silent clip ${clip}`;
  }

  return { preload, prepare, play, stop, suspend, describe };
}

// Add ?debug to the page URL (/crack-the-whip/crack-it/?debug) to show the
// live orientation and the tracker's state on top of the app while swinging.
function createDebugDisplay(doc, root, gesture, sounds) {
  const win = doc.defaultView;
  if (!new URLSearchParams(win.location?.search || '').has('debug')) return null;
  const panel = doc.createElement('pre');
  panel.className = 'debug-display';
  doc.body.append(panel);
  const times = [];
  const fired = [];
  let last;
  let strokeMin;
  let strokeMax;

  const number = value => (Number.isFinite(value) ? value.toFixed(1) : 'none').padStart(6);
  function zone(tilt) {
    if (!Number.isFinite(tilt)) return 'flat: ignored';
    if (Math.abs(tilt) >= 180 - SWING_DEGREES) return 'upside down: neither';
    if (tilt < -SWING_DEGREES) return 'whip side';
    if (tilt > SWING_DEGREES) return 'crack side';
    return 'middle: neither';
  }
  // -180 to +180 in 10-degree steps; | marks the 30-degree thresholds.
  function gauge(tilt) {
    const cells = [...'------------------:------------------'];
    cells[15] = cells[21] = '|';
    if (Number.isFinite(tilt)) cells[Math.round(tilt / 10) + 18] = 'O';
    return `L ${cells.join('')} R`;
  }

  function record(event, result) {
    const now = Date.now();
    times.push(now);
    while (now - times[0] > 1000) times.shift();
    last = { event, reading: screenTilt(event), result };
    const { tilt, sound } = result;
    if (Number.isFinite(tilt)) {
      strokeMin = Math.min(strokeMin ?? tilt, tilt);
      strokeMax = Math.max(strokeMax ?? tilt, tilt);
    }
    if (sound) {
      fired.unshift(`${sound} ${tilt.toFixed(0)}`);
      fired.length = Math.min(fired.length, 5);
      strokeMin = strokeMax = tilt;
    }
  }

  function render() {
    const event = last?.event || {};
    const tilt = last?.result.tilt;
    const next = gesture.next === 'whip' ? 'whip: tilt left past -30' : 'crack: tilt right past +30';
    panel.textContent = [
      `motion : ${root.dataset.motion || 'off'}, ${times.length}/s readings`,
      `alpha ${number(event.alpha)} beta ${number(event.beta)} gamma ${number(event.gamma)}`,
      `lean   : ${number(last?.reading?.lean)} from upright (flat past 70)`,
      `tilt   : ${number(tilt)} ${!last ? 'no reading yet' : !last.result.valid ? 'unusable reading' : zone(tilt)}`,
      gauge(tilt),
      `next   : ${next}`,
      `stroke : ${number(strokeMin)} to ${number(strokeMax)} since last sound`,
      `sounds : ${fired.join(', ') || 'none yet'}`,
      `audio  : ${sounds.describe()}`,
    ].join('\n');
  }

  const timer = win.setInterval(render, 100);
  render();
  return {
    record,
    destroy() {
      win.clearInterval(timer);
      panel.remove();
    },
  };
}

export function mountWhipApp(root) {
  const doc = root.ownerDocument;
  const win = doc.defaultView;
  const button = doc.querySelector('#crack-button');
  const motionButton = doc.querySelector('#motion-button');
  const soundStatus = doc.querySelector('#sound-status');
  const motionStatus = doc.querySelector('#motion-status');
  const motionNotice = doc.querySelector('#motion-notice');
  const audioFallback = doc.querySelector('#audio-fallback');
  const welcome = doc.querySelector('#welcome-dialog');
  const welcomeOK = doc.querySelector('#welcome-ok');
  const nativeAudio = [...doc.querySelectorAll('audio')];
  const whipStep = root.querySelector('#whip-step');
  const crackStep = root.querySelector('#crack-step');
  if (!button || !motionButton || !soundStatus || !motionStatus) return null;

  const sounds = createSoundBank(doc);
  const gesture = createGestureTracker();
  const debug = createDebugDisplay(doc, root, gesture, sounds);
  let motionEnabled = false;
  let motionStarting = false;
  let hasReading = false;
  let motionGeneration = 0;
  let clickGeneration = 0;
  let buttonBusy = false;
  let sensorTimer;
  let feedbackTimer;
  let destroyed = false;

  function pauseNativeAudio() {
    for (const audio of nativeAudio) audio.pause();
  }

  function clearFeedback() {
    win.clearTimeout(feedbackTimer);
    if (whipStep) whipStep.dataset.active = 'false';
    if (crackStep) crackStep.dataset.active = 'false';
    root.dataset.sound = '';
  }

  function showSound(key) {
    clearFeedback();
    root.dataset.sound = key;
    if (whipStep) whipStep.dataset.active = String(key !== 'crack');
    if (crackStep) crackStep.dataset.active = String(key !== 'whip');
    soundStatus.textContent = key === 'whip' ? 'Whip.' : key === 'crack' ? 'Crack!' : 'Whip… crack!';
    soundStatus.dataset.error = 'false';
    feedbackTimer = win.setTimeout(clearFeedback, 450);
  }

  function soundFailure(error) {
    soundStatus.dataset.error = 'true';
    if (audioFallback) audioFallback.hidden = false;
    soundStatus.textContent = error?.message?.startsWith('This browser cannot')
      || error?.message?.startsWith('Sound is paused')
      ? error.message
      : 'The sounds could not be loaded or played. Try again, or use the original audio player below.';
  }

  function stopMotion(message) {
    motionGeneration += 1;
    motionEnabled = false;
    motionStarting = false;
    hasReading = false;
    gesture.reset();
    win.removeEventListener('deviceorientation', onOrientation);
    win.clearTimeout(sensorTimer);
    motionButton.disabled = false;
    motionButton.textContent = 'enable motion';
    motionButton.setAttribute('aria-pressed', 'false');
    root.dataset.motion = 'off';
    if (message) {
      motionStatus.textContent = message;
      if (motionNotice) motionNotice.hidden = false;
    }
  }

  function onOrientation(event) {
    if (!motionEnabled || destroyed || doc.hidden) return;
    const next = gesture.sample(event);
    debug?.record(event, next);
    if (!next.valid) return;
    if (!hasReading) {
      hasReading = true;
      win.clearTimeout(sensorTimer);
      root.dataset.motion = 'on';
      motionStatus.textContent = 'Motion is on.';
      if (motionNotice) motionNotice.hidden = true;
    }
    if (!next.sound) return;
    try {
      // A long crack must not keep ringing over the next, much shorter whoosh.
      sounds.stop();
      if (!sounds.play(next.sound)) {
        stopMotion('Sound was paused by your browser. Tap Enable motion to continue, or use the button.');
        return;
      }
      showSound(next.sound);
    } catch (error) {
      stopMotion('Motion is off. Use the button to try sound again.');
      soundFailure(error);
    }
  }

  function onCrack() {
    if (destroyed || doc.hidden || buttonBusy) return;
    pauseNativeAudio();
    buttonBusy = true;
    button.disabled = true;
    const attempt = ++clickGeneration;
    soundStatus.textContent = 'Getting the original sounds ready…';
    // prepare() starts AudioContext.resume synchronously within this gesture.
    sounds.prepare().then(() => {
      if (destroyed || doc.hidden || attempt !== clickGeneration) {
        if (doc.hidden) sounds.suspend();
        return;
      }
      sounds.stop();
      if (!sounds.play('combined')) throw new Error('Sound is paused by your browser. Tap the button again to enable it.');
      showSound('combined');
    }).catch(error => {
      if (!destroyed && !doc.hidden && attempt === clickGeneration) soundFailure(error);
    }).finally(() => {
      if (attempt === clickGeneration) {
        buttonBusy = false;
        button.disabled = false;
      }
    });
  }

  function onMotionToggle() {
    if (destroyed || doc.hidden || motionStarting) return;
    if (motionEnabled) {
      stopMotion('Motion is off. The button still works.');
      sounds.stop();
      clearFeedback();
      return;
    }
    if (!win.isSecureContext) {
      stopMotion('Motion needs HTTPS. You can still use the button.');
      return;
    }
    const Orientation = win.DeviceOrientationEvent;
    if (!Orientation) {
      stopMotion('This browser does not provide motion controls. Use the button instead.');
      return;
    }

    const attempt = ++motionGeneration;
    pauseNativeAudio();
    motionStarting = true;
    motionButton.disabled = true;
    motionButton.textContent = 'Enabling motion…';
    root.dataset.motion = 'starting';
    if (motionNotice) motionNotice.hidden = true;
    motionStatus.textContent = 'Allow motion if your browser asks. Getting the sounds ready…';

    let permission;
    try {
      // Do not place an await before this call: Safari requires user activation.
      // https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent/requestPermission_static
      permission = typeof Orientation.requestPermission === 'function'
        ? Orientation.requestPermission()
        : Promise.resolve('granted');
    } catch (error) {
      permission = Promise.reject(error);
    }
    const permissionCheck = Promise.resolve(permission).then(result => {
      if (result !== 'granted') {
        throw new Error('Motion permission was not granted. The button still works.');
      }
    }, () => {
      throw new Error('Motion permission could not be requested. Try Enable motion again, or use the button.');
    });

    // Both permission and audio unlock begin in the click handler. Sensor events
    // never request permission, fetch/decode audio, or try to unlock audio.
    Promise.all([permissionCheck, sounds.prepare()]).then(() => {
      if (destroyed || doc.hidden || attempt !== motionGeneration) {
        if (doc.hidden) sounds.suspend();
        return;
      }
      motionStarting = false;
      motionEnabled = true;
      gesture.reset();
      motionButton.disabled = false;
      motionButton.textContent = 'Disable motion';
      motionButton.setAttribute('aria-pressed', 'true');
      root.dataset.motion = 'waiting';
      motionStatus.textContent = 'Waiting for your phone’s motion sensor…';
      win.addEventListener('deviceorientation', onOrientation);
      sensorTimer = win.setTimeout(() => {
        if (motionEnabled && !hasReading) {
          stopMotion('No motion readings arrived. Your browser or device may not support them. Use the button, or try Enable motion again.');
        }
      }, 7000);
    }).catch(error => {
      if (destroyed || doc.hidden || attempt !== motionGeneration) return;
      const permissionError = error?.message?.startsWith('Motion permission');
      stopMotion(permissionError ? error.message : 'Motion could not start because sound is unavailable. Try again, or use the original audio player below.');
      if (!permissionError) soundFailure(error);
    });
  }

  function onWelcomeOK() {
    // Every arrival's OK click starts the permission request in this gesture;
    // never defer it until after dialog closing, audio loading, or an await.
    onMotionToggle();
    welcome?.close();
    root.focus();
  }

  function onWelcomeCancel() {
    stopMotion('Motion is off. You can enable it or use the button.');
  }

  function pause() {
    const wasEnabled = motionEnabled || motionStarting;
    clickGeneration += 1;
    buttonBusy = false;
    button.disabled = false;
    stopMotion(wasEnabled ? 'Motion paused while you were away.' : undefined);
    sounds.suspend();
    pauseNativeAudio();
    clearFeedback();
    soundStatus.textContent = 'Sound paused. Tap the button when you’re ready.';
  }

  function onVisibilityChange() {
    if (doc.hidden) pause();
  }

  function onFirstKey() {
    // Lets the ok button's focus ring show for keyboard users (whip-app.css).
    if (doc.documentElement) doc.documentElement.dataset.keyboard = 'true';
  }

  function onNativePlay() {
    // The preserved audio player is another way to listen, not a second mixer.
    clickGeneration += 1;
    buttonBusy = false;
    button.disabled = false;
    stopMotion('Motion is off while the original audio player is playing.');
    sounds.suspend();
    clearFeedback();
    soundStatus.textContent = 'Playing the original sound in the audio player.';
  }

  button.addEventListener('click', onCrack);
  motionButton.addEventListener('click', onMotionToggle);
  welcomeOK?.addEventListener('click', onWelcomeOK);
  welcome?.addEventListener('cancel', onWelcomeCancel);
  doc.addEventListener('visibilitychange', onVisibilityChange);
  doc.addEventListener('keydown', onFirstKey, { once: true });
  win.addEventListener('pagehide', pause);
  for (const audio of nativeAudio) audio.addEventListener('play', onNativePlay);
  stopMotion();
  sounds.preload();
  button.disabled = false;
  button.hidden = false;
  motionButton.hidden = false;
  if (welcome && typeof welcome.showModal === 'function') welcome.showModal();

  return {
    destroy() {
      if (destroyed) return;
      destroyed = true;
      pause();
      debug?.destroy();
      button.removeEventListener('click', onCrack);
      motionButton.removeEventListener('click', onMotionToggle);
      welcomeOK?.removeEventListener('click', onWelcomeOK);
      welcome?.removeEventListener('cancel', onWelcomeCancel);
      if (welcome?.open) welcome.close();
      doc.removeEventListener('visibilitychange', onVisibilityChange);
      doc.removeEventListener('keydown', onFirstKey);
      win.removeEventListener('pagehide', pause);
      for (const audio of nativeAudio) audio.removeEventListener('play', onNativePlay);
    },
  };
}

if (typeof document !== 'undefined') {
  const root = document.querySelector('#whip-app');
  if (root) mountWhipApp(root);
}
