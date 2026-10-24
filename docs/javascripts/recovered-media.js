(() => {
  const assets = new URL('../assets/', document.currentScript.src);
  const runtime = new URL('vendor/ruffle/0.7.1/', assets);
  const initialized = new WeakSet();
  let ruffleReady;
  let activeGallery;
  let activeAudio;

  const movies = {
    snowman: { file: 'snowman-snow-fight.swf', poster: 'snowman-poster.jpg', title: 'Snowman snow fight', description: 'My first animation. The old site says I looked back and laughed at how poorly it was made, but learned a lot.' },
    fight: { file: '3d-stick-fight.swf', poster: 'fight-poster.jpg', title: '3D stick fight', description: 'The second animation I made, according to the original movie index.' },
    badDay: { file: 'bad-day.swf', poster: 'bad-day-poster.jpg', title: 'Bad Day', description: 'A short film preserved as BadDay1.swf in the original movie folder.' },
    stick1: { file: 'stick-1.swf', poster: 'stick-1-poster.jpg', title: 'Stick figure 1', description: 'One of the tiny, 100 × 100 stick-figure animations from the original site.' },
    stick2: { file: 'stick-2.swf', poster: 'stick-2-poster.jpg', title: 'Stick figure 2', description: 'The second surviving 100 × 100 stick-figure loop.' },
  };

  function loadRuffle() {
    if (!ruffleReady) {
      ruffleReady = new Promise((resolve, reject) => {
        window.RufflePlayer = window.RufflePlayer || {};
        window.RufflePlayer.config = {
          ...window.RufflePlayer.config,
          publicPath: runtime.href,
          polyfills: false,
          allowScriptAccess: false,
          allowNetworking: 'none',
          openUrlMode: 'deny',
        };
        const script = document.createElement('script');
        script.src = new URL('ruffle.js', runtime).href;
        script.onload = () => {
          if (typeof window.RufflePlayer.newest === 'function') resolve(window.RufflePlayer.newest());
          else script.onerror();
        };
        script.onerror = () => {
          script.remove();
          ruffleReady = undefined;
          reject(new Error('The animation player could not be downloaded.'));
        };
        document.head.append(script);
      });
    }
    return ruffleReady;
  }

  function initializeGallery(root) {
    const select = root.querySelector('[data-flash-select]');
    const stage = root.querySelector('[data-flash-stage]');
    const play = root.querySelector('[data-flash-play]');
    const restart = root.querySelector('[data-flash-restart]');
    const status = root.querySelector('[data-flash-status]');
    const caption = root.querySelector('[data-flash-caption]');
    const download = root.querySelector('[data-flash-download]');
    const poster = root.querySelector('[data-flash-poster]');
    let player;
    let generation = 0;
    let loading = false;

    function suspend() {
      if (player) player.ruffle().suspend();
      if (!loading) play.textContent = player ? 'Resume animation' : 'Play animation';
      if (player && !loading) status.textContent = 'Paused.';
    }

    function destroy() {
      generation += 1;
      if (player) {
        player.ruffle().suspend();
        player.remove();
        player = undefined;
      }
      loading = false;
    }

    function selectedMovie() { return movies[select.value] || movies.snowman; }

    function showSelection() {
      destroy();
      const movie = selectedMovie();
      caption.textContent = movie.description;
      download.href = new URL(`early-experiments/animations/${movie.file}`, assets).href;
      download.textContent = `Download ${movie.title} (.swf)`;
      play.disabled = false;
      play.textContent = 'Play animation';
      restart.disabled = true;
      status.textContent = 'Ready when you are.';
      stage.setAttribute('aria-label', `${movie.title} animation player`);
      poster.src = new URL(`early-experiments/animations/${movie.poster}`, assets).href;
      poster.alt = `Still from ${movie.title}`;
      poster.hidden = false;
    }

    async function start() {
      if (loading) return;
      if (activeAudio) activeAudio.pause();
      const movie = selectedMovie();
      const attempt = ++generation;
      loading = true;
      play.disabled = true;
      restart.disabled = true;
      status.textContent = 'Loading the original animation…';
      try {
        const ruffle = await loadRuffle();
        if (attempt !== generation || !root.isConnected) return;
        if (player) player.remove();
        player = ruffle.createPlayer();
        player.setAttribute('aria-label', movie.title);
        stage.append(player);
        await player.ruffle().load({
          url: new URL(`early-experiments/animations/${movie.file}`, assets).href,
          autoplay: 'on',
          unmuteOverlay: 'visible',
          splashScreen: false,
          allowScriptAccess: false,
          allowNetworking: 'none',
          openUrlMode: 'deny',
          letterbox: 'on',
          contextMenu: 'rightClickOnly',
          backgroundExecutionMode: 'none',
          logLevel: 'error',
        });
        if (attempt !== generation || !root.isConnected) return;
        poster.hidden = true;
        play.textContent = 'Pause animation';
        restart.disabled = false;
        status.textContent = `Playing ${movie.title}.`;
      } catch (error) {
        if (attempt !== generation || !root.isConnected) return;
        if (player) { player.remove(); player = undefined; }
        poster.hidden = false;
        play.textContent = 'Try again';
        status.textContent = 'The animation could not play. Try again, or download the original file below.';
      } finally {
        if (attempt === generation && root.isConnected) {
          loading = false;
          play.disabled = false;
        }
      }
    }

    select.addEventListener('change', showSelection);
    play.addEventListener('click', () => {
      if (!player) { start(); return; }
      if (player.ruffle().suspended) {
        if (activeAudio) activeAudio.pause();
        player.ruffle().resume();
        play.textContent = 'Pause animation';
        status.textContent = `Playing ${selectedMovie().title}.`;
      } else {
        suspend();
        status.textContent = 'Paused.';
      }
    });
    restart.addEventListener('click', () => { destroy(); start(); });
    root.querySelector('[data-flash-controls]').hidden = false;
    showSelection();
    activeGallery = { root, suspend, destroy };
  }

  function initialize() {
    if (activeGallery && !activeGallery.root.isConnected) {
      activeGallery.destroy();
      activeGallery = undefined;
    }
    if (activeAudio && !activeAudio.isConnected) {
      activeAudio.pause();
      activeAudio = undefined;
    }
    document.querySelectorAll('[data-flash-gallery]').forEach(root => {
      if (initialized.has(root)) return;
      initialized.add(root);
      initializeGallery(root);
    });
    document.querySelectorAll('audio.qd-original-audio').forEach(audio => {
      if (initialized.has(audio)) return;
      initialized.add(audio);
      audio.addEventListener('play', () => {
        if (activeAudio && activeAudio !== audio) activeAudio.pause();
        if (activeGallery) activeGallery.suspend();
        activeAudio = audio;
      });
    });
    document.querySelectorAll('[data-play-audio]').forEach(button => {
      if (initialized.has(button)) return;
      initialized.add(button);
      const audio = document.getElementById(button.dataset.playAudio);
      if (!audio) return;
      button.hidden = false;
      button.addEventListener('click', async () => {
        const status = document.getElementById(button.getAttribute('aria-describedby'));
        try {
          audio.currentTime = 0;
          await audio.play();
          if (status) status.textContent = 'Whip cracked. Again?';
        } catch {
          if (status) status.textContent = 'Use the audio controls below, or download the original sound.';
        }
      });
    });
  }

  function suspendMedia() {
    if (activeGallery) activeGallery.suspend();
    if (activeAudio) activeAudio.pause();
  }
  window.addEventListener('pagehide', suspendMedia);
  document.addEventListener('visibilitychange', () => { if (document.hidden) suspendMedia(); });
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize);
  else initialize();
})();
