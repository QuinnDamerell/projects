(() => {
  const initialized = new WeakSet();
  let printState = [];

  function revealFragment() {
    let id;
    try {
      id = decodeURIComponent(window.location.hash.slice(1));
    } catch {
      return;
    }
    const target = id && document.getElementById(id);
    if (!target) return;

    let revealed = false;
    for (let parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS' && !parent.open) {
        parent.open = true;
        revealed = true;
      }
    }
    if (revealed) requestAnimationFrame(() => target.scrollIntoView({ behavior: 'instant', block: 'start' }));
  }

  function initializeStoryDetails() {
    const content = document.querySelector('.md-content__inner');
    if (content && !initialized.has(content)) {
      const details = [...content.querySelectorAll('details.qd-story-details')];
      if (details.length > 1) {
        const controls = document.createElement('div');
        controls.className = 'qd-story-controls';
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'md-button';
        function updateLabel() {
          button.textContent = details.every(detail => detail.open) ? 'Collapse all details' : 'Expand all details';
        }
        button.addEventListener('click', () => {
          const open = !details.every(detail => detail.open);
          details.forEach(detail => { detail.open = open; });
          updateLabel();
        });
        details.forEach(detail => detail.addEventListener('toggle', updateLabel));
        updateLabel();
        controls.append(button);
        details[0].before(controls);
      }
      initialized.add(content);
    }
    revealFragment();
  }

  // Preserve direct links into the archive, including instant-navigation arrivals.
  window.addEventListener('hashchange', revealFragment);
  if (typeof document$ !== 'undefined') document$.subscribe(initializeStoryDetails);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initializeStoryDetails);
  else initializeStoryDetails();

  // Printed copies include the complete record; restore the reading view afterward.
  window.addEventListener('beforeprint', () => {
    if (printState.length) return;
    printState = [...document.querySelectorAll('details.qd-story-details')].map(detail => [detail, detail.open]);
    printState.forEach(([detail]) => { detail.open = true; });
  });
  window.addEventListener('afterprint', () => {
    printState.forEach(([detail, open]) => { detail.open = open; });
    printState = [];
  });
})();
