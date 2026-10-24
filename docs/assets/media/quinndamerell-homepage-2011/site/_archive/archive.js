/* Audited archive-only interactions. No network requests, storage, account actions, or eval. */
(() => {
  'use strict';
  document.querySelectorAll('img[data-rollover]').forEach(img => {
    const original=img.getAttribute('src'), hover=img.dataset.rollover, anchor=img.closest('a')||img;
    const enter=()=>{img.src=hover;},leave=()=>{img.src=original;};
    anchor.addEventListener('mouseenter',enter);anchor.addEventListener('mouseleave',leave);anchor.addEventListener('focus',enter);anchor.addEventListener('blur',leave);
  });
  document.querySelectorAll('.Accordion').forEach(accordion => {
    accordion.classList.add('archive-accordion');
    const panels=[...accordion.children].filter(el=>el.classList.contains('AccordionPanel'));
    const choose=index=>panels.forEach((panel,i)=>{const tab=panel.querySelector('[data-accordion-tab]'),content=panel.querySelector('.AccordionPanelContent');if(!tab||!content)return;content.hidden=i!==index;tab.setAttribute('aria-expanded',String(i===index));panel.classList.toggle('AccordionPanelOpen',i===index);});
    panels.forEach((panel,index)=>{const tab=panel.querySelector('[class^="AccordionPanelTab"]'),content=panel.querySelector('.AccordionPanelContent');if(!tab||!content)return;tab.dataset.accordionTab='';tab.tabIndex=0;tab.setAttribute('role','button');tab.addEventListener('click',()=>choose(index));tab.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(index);}if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();const j=(index+(e.key==='ArrowDown'?1:-1)+panels.length)%panels.length;choose(j);panels[j].querySelector('[data-accordion-tab]').focus();}});});choose(0);
  });
  document.querySelectorAll('[data-video-box]').forEach(link=>{link.addEventListener('click',e=>{e.preventDefault();document.querySelectorAll('#Content1 > div[id^="box"]').forEach(box=>{box.style.display=box.id===link.dataset.videoBox?'block':'none';});});});
  const links=[...document.querySelectorAll('a[data-gallery]')];if(!links.length)return;
  const overlay=document.createElement('div');overlay.className='archive-gallery';overlay.setAttribute('role','dialog');overlay.setAttribute('aria-modal','true');overlay.setAttribute('aria-label','Image gallery');
  const figure=document.createElement('figure'),img=document.createElement('img'),caption=document.createElement('figcaption'),controls=document.createElement('div');controls.className='gallery-controls';
  const button=(label,action)=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.addEventListener('click',action);controls.append(b);return b;};
  let current=0,group=[],opener=null;
  const show=index=>{current=(index+group.length)%group.length;const link=group[current];img.src=link.href;img.alt=link.title||link.querySelector('img')?.alt||'Archived photo';caption.textContent=(current+1)+' / '+group.length+(link.title?' — '+link.title:'');};
  const close=()=>{overlay.removeAttribute('data-open');opener?.focus();};
  button('Previous',()=>show(current-1));const closer=button('Close',close);button('Next',()=>show(current+1));figure.append(img,caption,controls);overlay.append(figure);document.body.append(overlay);
  links.forEach(link=>link.addEventListener('click',e=>{if(e.button!==0||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;e.preventDefault();opener=link;group=links.filter(other=>other.dataset.gallery===link.dataset.gallery);show(group.indexOf(link));overlay.setAttribute('data-open','');closer.focus();}));
  overlay.addEventListener('click',e=>{if(e.target===overlay)close();});document.addEventListener('keydown',e=>{if(!overlay.hasAttribute('data-open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft'){e.preventDefault();show(current-1);}if(e.key==='ArrowRight'){e.preventDefault();show(current+1);}if(e.key==='Tab'){const buttons=[...controls.querySelectorAll('button')];const i=buttons.indexOf(document.activeElement);e.preventDefault();buttons[(i+(e.shiftKey?-1:1)+buttons.length)%buttons.length].focus();}});
})();