(() => {
  const initialized = new WeakSet();
  // Keep selections while following an entry and returning via instant navigation.
  // A fresh page load always starts with every category enabled.
  const disabledCategories = new Set();

  function initializeMediaFilters() {
    const media = document.querySelector('.qd-media');
    if (!media || initialized.has(media)) return;

    const filters = media.querySelector('.qd-media-filters');
    const buttons = [...media.querySelectorAll('[data-media-filter]')];
    const entries = [...media.querySelectorAll('.qd-entry')];
    const years = [...media.querySelectorAll('.qd-year')];
    const groups = [...media.querySelectorAll('[data-media-group]')];
    const stories = entries.filter(entry => entry.closest('[data-media-group="stories"]'));
    const capsules = entries.filter(entry => entry.closest('[data-media-group="capsules"]'));
    const status = media.querySelector('.qd-media-filters__status');
    const empty = media.querySelector('.qd-media-empty');
    const reset = media.querySelector('[data-media-reset]');
    if (!filters || !buttons.length || !status || !empty || !reset) return;

    function update() {
      buttons.forEach(button => {
        button.setAttribute('aria-pressed', String(!disabledCategories.has(button.dataset.mediaFilter)));
      });
      entries.forEach(entry => {
        entry.hidden = disabledCategories.has(entry.dataset.mediaCategory);
      });
      years.forEach(year => {
        year.hidden = !year.querySelector('.qd-entry:not([hidden])');
      });
      groups.forEach(group => {
        group.hidden = !group.querySelector('.qd-entry:not([hidden])');
      });
      const visible = entries.filter(entry => !entry.hidden).length;
      const visibleStories = stories.filter(entry => !entry.hidden).length;
      const visibleCapsules = capsules.filter(entry => !entry.hidden).length;
      status.textContent = `${visibleStories} of ${stories.length} stories · ${visibleCapsules} of ${capsules.length} time capsules`;
      empty.hidden = visible > 0;
    }

    buttons.forEach(button => {
      button.addEventListener('click', () => {
        const category = button.dataset.mediaFilter;
        if (disabledCategories.has(category)) disabledCategories.delete(category);
        else disabledCategories.add(category);
        update();
      });
    });
    reset.addEventListener('click', () => {
      disabledCategories.clear();
      update();
      buttons[0].focus();
    });

    initialized.add(media);
    update();
    filters.hidden = false;
  }

  // Zensical replaces page content during instant navigation.
  if (typeof document$ !== 'undefined') document$.subscribe(initializeMediaFilters);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initializeMediaFilters);
  else initializeMediaFilters();
})();
