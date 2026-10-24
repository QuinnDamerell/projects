/* Audited archive replacement: DOM-only gallery and original header flip.
 * No requests, storage, dynamic evaluation, form submission or parent access.
 * Images keep ordinary href fallbacks when scripting is disabled. */
(() => {
  "use strict";
  const links = Array.from(document.querySelectorAll('a[data-archive-gallery]'));
  if (links.length && typeof HTMLDialogElement !== 'undefined') {
    const dialog = document.createElement('dialog'); dialog.className = 'archive-gallery';
    dialog.setAttribute('aria-label', 'Archived image gallery');
    const bar = document.createElement('div'); bar.className = 'archive-gallery-controls';
    const image = document.createElement('img'); const caption = document.createElement('p');
    caption.className = 'archive-gallery-caption'; caption.setAttribute('aria-live', 'polite');
    const button = (label, action) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = label; b.addEventListener('click', action); bar.append(b); return b; };
    let group = [], index = 0, origin;
    const show = delta => {
      index = (index + delta + group.length) % group.length;
      const anchor = group[index]; image.src = anchor.href;
      image.alt = anchor.title || anchor.querySelector('img')?.alt || 'Archived screenshot';
      caption.textContent = `${index + 1} / ${group.length}` + (anchor.title ? ` — ${anchor.title}` : '');
    };
    button('Previous', () => show(-1)); button('Next', () => show(1)); button('Close', () => dialog.close());
    dialog.append(bar, image, caption); document.body.append(dialog);
    links.forEach(anchor => anchor.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); origin = anchor;
      group = links.filter(a => a.dataset.archiveGallery === anchor.dataset.archiveGallery);
      index = group.indexOf(anchor); show(0); dialog.showModal();
    }));
    dialog.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') {e.preventDefault();show(-1);} if (e.key === 'ArrowRight') {e.preventDefault();show(1);} });
    dialog.addEventListener('click', e => {if (e.target === dialog) dialog.close();});
    dialog.addEventListener('close', () => origin?.focus());
  }
  const tile = document.getElementById('livetile');
  if (tile) {
    let flipped = false;
    const flip = () => {flipped = !flipped;tile.style.transform = flipped ? 'rotateX(-180deg)' : 'rotateX(0deg)';};
    tile.tabIndex = 0; tile.setAttribute('role', 'button'); tile.setAttribute('aria-label', 'Flip Quinn Damerell photo tile');
    tile.addEventListener('click', flip);
    tile.addEventListener('keydown', e => {if(e.key === 'Enter' || e.key === ' ') {e.preventDefault();flip();}});
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) setTimeout(() => {flip();setInterval(flip, 8000);}, 3000);
  }
  document.querySelectorAll('img[data-archive-hover]').forEach(image => {
    const link = image.closest('a'); if (!link) return;
    const original = image.src;
    const enter = () => {image.src = image.dataset.archiveHover;};
    const leave = () => {image.src = original;};
    link.addEventListener('mouseenter', enter); link.addEventListener('focus', enter);
    link.addEventListener('mouseleave', leave); link.addEventListener('blur', leave);
  });
  const selectors = Array.from(document.querySelectorAll('a[data-archive-video]'));
  if (selectors.length) {
    const panels = Array.from(document.querySelectorAll('[data-archive-video-panel]'));
    const show = id => {
      panels.forEach(panel => {panel.style.display = panel.id === id ? 'block' : 'none';});
      selectors.forEach(link => link.setAttribute('aria-expanded', String(link.dataset.archiveVideo === id)));
    };
    show('box10');
    selectors.forEach(link => link.addEventListener('click', event => {event.preventDefault();show(link.dataset.archiveVideo);}));
  }
})();
