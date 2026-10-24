from mirror import *
import mimetypes,base64,copy
requested_full=targetdt.strftime('%B %d, %Y').replace(' 0',' ')
requested_month=targetdt.strftime('%B %Y')
requested_time=targetdt.strftime('%H:%M:%S UTC')
STYLE=""".archive-notice{box-sizing:border-box;display:block;width:100%;padding:8px 12px;margin:0 0 14px;background:#111214;color:#eee;font:13px/1.5 system-ui,sans-serif;text-align:center;position:relative;z-index:1000}.archive-notice a{color:#aecbfa}.archive-embed-gap{box-sizing:border-box;display:flex;min-height:180px;max-width:425px;padding:24px;align-items:center;justify-content:center;flex-direction:column;background:#eee;color:#222;font:15px/1.5 system-ui,sans-serif;text-align:center}.archive-embed-gap a{color:#165a9a}.archive-gallery{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.86);display:none;align-items:center;justify-content:center;padding:15px;box-sizing:border-box}.archive-gallery[data-open]{display:flex}.archive-gallery figure{position:relative;max-width:90vw;margin:0;background:#fff;padding:10px;border-radius:3px;text-align:center}.archive-gallery img{display:block;max-width:85vw;max-height:78vh;width:auto;height:auto;margin:auto}.archive-gallery figcaption{font:14px/1.4 Arial,sans-serif;padding:8px;max-width:75ch}.archive-gallery button{font:18px Arial,sans-serif;cursor:pointer;padding:6px 12px;border:1px solid #777;border-radius:3px;background:#fff;color:#111}.archive-gallery .gallery-controls{display:flex;gap:10px;justify-content:center;padding-top:8px}.archive-accordion .AccordionPanelContent{height:auto!important;overflow:visible!important}.archive-accordion .AccordionPanelContent[hidden]{display:none!important}.archive-accordion [role=button]{cursor:pointer}.archive-accordion [role=button]:focus{outline:2px solid #0099ff;outline-offset:2px}.archive-video-select{cursor:pointer;text-decoration:underline}.archive-nav-link{display:block;cursor:pointer;color:inherit;text-decoration:inherit}.archive-form-note{font:14px/1.4 system-ui,sans-serif;padding:8px;background:#fff4cc;color:#333}.archive-missing-inline{display:block;font:12px/1.4 system-ui,sans-serif;color:#555}.archive-legacy-download{font:14px/1.5 system-ui,sans-serif;background:#eee;padding:12px;color:#222}.archive-small-icon-fallback{display:inline-block}.archive-notice details{display:inline}.archive-notice summary{display:inline;cursor:pointer;text-decoration:underline}"""
JS="""/* Audited archive-only interactions. No network requests, storage, account actions, or eval. */
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
})();"""
MISSING='''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200"><rect width="320" height="200" fill="#eeeeec"/><rect x="2" y="2" width="316" height="196" fill="none" stroke="#aaa" stroke-dasharray="5 5"/><text x="160" y="92" text-anchor="middle" font-family="Arial" font-size="15" fill="#555">Image not recovered</text><text x="160" y="115" text-anchor="middle" font-family="Arial" font-size="12" fill="#666">from the Internet Archive</text></svg>'''
PAGECSS='body{font:16px/1.6 system-ui,sans-serif;background:#f4f3ef;color:#222;margin:0}main{max-width:1000px;margin:auto;padding:35px 22px}a{color:#175b85}table{border-collapse:collapse;width:100%;font-size:13px}td,th{text-align:left;vertical-align:top;border-bottom:1px solid #ccc;padding:7px;overflow-wrap:anywhere}code{overflow-wrap:anywhere}h1{line-height:1.2}'

def shell(title,content):return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>'+html.escape(title)+'</title><style>'+PAGECSS+'</style></head><body><main>'+content+'</main></body></html>'
def relative(target,current):return os.path.relpath(OUT/target,(OUT/current).parent).replace('\\','/')

def publish():
 statepath=TEMP/'crawl-state.json'
 if statepath.exists():state=json.loads(statepath.read_text(encoding='utf8'))
 else:
  previous=json.loads((OUT/'manifest.json').read_text(encoding='utf8'));state={'records':previous['files'],'external_links':previous.get('external_links',[]),'excluded':previous.get('excluded',[])}
 records={key(r['original_url']):r for r in state['records']};external=set(state.get('external_links',[]));substitutions=[];inactive_links=[]
 for r in records.values():
  r.pop('source_file',None)
  if r['status']!='saved' and r['kind']=='page':r['served_path']='site/'+r['local_path'];r['placeholder_path']=r['served_path']
  elif r['status']!='saved' and r['kind']=='asset':r['placeholder_path']='site/_missing/'+sha(r['original_url'].encode())[:14]+'.html'
 def mapping(value,base,current,resource=False,css=False):
  u=normal(value,base)
  if not u:return '#' if str(value).lower().startswith(('javascript:','market:')) else value
  r=records.get(key(u));fragment=urlsplit(str(value)).fragment
  if r and r['status']=='saved' and r['kind']!='script':return relative('site/'+r['local_path'],current)+('#'+fragment if fragment else '')
  if resource:
   return 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22/%3E' if css else relative('missing-asset.svg',current)
  if r and r.get('placeholder_path'):return relative(r['placeholder_path'],current)
  if not same(u):return u
  return 'https://web.archive.org/web/'+TARGET+'/'+u
 def css(text,base,current):
  def replace(m):
   u=normal(m.group(1),base);r=records.get(key(u)) if u else None
   if r and r['status']=='saved' and re.search(r'\.(ttf|otf|woff2?)(?:\?|$)',u,re.I):
    mime=mimetypes.guess_type(u)[0] or 'font/woff2';return 'url("data:'+mime+';base64,'+base64.b64encode((OUT/r['raw_path']).read_bytes()).decode()+'")'
   return 'url("'+mapping(m.group(1),base,current,True,True)+'")' if u else m.group(0)
  text=CSSURL.sub(replace,text);return CSSIMPORT.sub(lambda m:'@import "'+mapping(m.group(1),base,current,True)+'"',text)
 def gap(r,current):
  return shell('Archived resource unavailable','<p><a href="'+relative('snapshot.html',current)+'">Archive homepage</a> · <a href="'+relative('archive-index.html',current)+'">Recovery inventory</a></p><h1>This resource was not recovered</h1><p>This archived page collection referenced <code>'+html.escape(r['original_url'])+'</code>, but the attempted Internet Archive replays did not return a usable copy.</p><p>Its original server features are not reproduced. The file inventory records the attempts and any redirects.</p><p><a target="_blank" rel="noopener noreferrer" href="'+html.escape(r['requested_wayback_url'].replace(TARGET+'id_',TARGET))+'">Check the Wayback Machine</a></p>')
 def page(r,current):
  body=(OUT/r['raw_path']).read_bytes();soup=BeautifulSoup(body,'html.parser');base=r['original_url'];rollovers={}
  for s in soup.find_all('script'):
   rollovers.update(re.findall(r'(\w+)\.src\s*=\s*[\'"]([^\'\"]+)[\'"]',s.get_text()))
  # Use a surviving counterpart only when the source gallery links them.
  for a in soup.find_all('a',href=True):
   thumb=a.find('img',src=True)
   if not thumb:continue
   full_url=normal(a['href'],base);thumb_url=normal(thumb['src'],base)
   full=records.get(key(full_url)) if full_url else None;small=records.get(key(thumb_url)) if thumb_url else None
   if full and small and re.search(r'\.(png|jpe?g|gif)$',urlsplit(full_url).path,re.I):
    if full['status']!='saved' and small['status']=='saved':
     a['href']=thumb_url;a['title']='Only the archived thumbnail was recovered. '+a.get('title','')
     note=soup.new_tag('a',href=full_url,attrs={'class':'archive-missing-inline'});note.string='Full image unavailable';a.insert_after(note)
     substitutions.append({'page':base,'original_image':full_url,'displayed_image':thumb_url,'reason':'Full image unavailable; its original linked thumbnail is displayed.'})
    elif full['status']=='saved' and small['status']!='saved':
     thumb['src']=full_url;thumb['title']='Recovered full image displayed in place of its unavailable thumbnail.'
     substitutions.append({'page':base,'original_image':thumb_url,'displayed_image':full_url,'reason':'Thumbnail unavailable; its original linked full image is displayed at thumbnail size.'})
  if urlsplit(base).path.lower()=='/projects.php' and not soup.find(id='TxtBack'):
   label=soup.find('a',href='http://www.txtback.mobi')
   if label:label['id']='TxtBack'
  # Inline navigation and content-selection handlers are transcribed to inert data.
  for el in soup.find_all(True):
   onclick=el.get('onclick','');nav=NAVJS.search(onclick);select=re.search(r'showbox\([\'"]([^\'\"]+)',onclick)
   if nav:
    if el.name!='a':el.name='a';el['class']=list(el.get('class',[]))+['archive-nav-link']
    el['href']=nav.group(1)
   if select:el['href']='#'+select.group(1);el['data-video-box']=select.group(1);el['class']=list(el.get('class',[]))+['archive-video-select']
   hover=re.search(r'\.src\s*=\s*(\w+)\.src',el.get('onmouseover',''))
   if hover and hover.group(1) in rollovers:
    target=normal(rollovers[hover.group(1)],base);rec=records.get(key(target));img=el.find('img')
    if img and rec and rec['status']=='saved':img['data-rollover']=mapping(target,base,current,True)
  # Legacy external Flash video containers become explicit source links in their existing tabs.
  for object_ in list(soup.find_all(['object','embed','iframe','applet'])):
   if object_.parent is None:continue
   source=object_.get('data') or object_.get('src') or object_.get('archive') or ''
   movie=object_.find('param',attrs={'name':re.compile('movie',re.I)})
   if movie:source=movie.get('value','')
   box=soup.new_tag('div',attrs={'class':'archive-embed-gap'});youtube=re.search(r'(?:youtube\.com/(?:v/|embed/)|youtu\.be/)([a-zA-Z0-9_-]{11})',source)
   if youtube:
    box.append('The original embedded player used Flash. ');a=soup.new_tag('a',href='https://www.youtube.com/watch?v='+youtube.group(1),target='_blank',rel='noopener noreferrer');a.string='Open the original video on YouTube';box.append(a)
   else:
    box.append('Original embedded content is preserved as a reference. Flash and Java applets are not run in this archive. ')
    if source:
     a=soup.new_tag('a',href=mapping(source,base,current));a.string='View recovered file or archive source';box.append(a)
   object_.replace_with(box)
  for el in soup.select('script,noscript,base,meta[http-equiv="refresh" i],meta[http-equiv="content-security-policy" i]'):el.decompose()
  for el in soup.find_all('link',href=True):
   if 'stylesheet' in el.get('rel',[]):
    original=normal(el['href'],base);stylesheet=records.get(key(original)) if original else None
    if not stylesheet or stylesheet['status']!='saved':el.decompose()
  for el in soup.find_all(True):
   for attr in list(el.attrs):
    if attr.lower().startswith('on') or attr in ('integrity','crossorigin','srcdoc','codebase'):del el[attr]
   if el.name=='form':
    note=soup.new_tag('p',attrs={'class':'archive-form-note'});note.string='Historical form. Submission and account features are disabled in this static copy.';el.insert_before(note);el.name='div'
    for attr in ['action','method','target']:el.attrs.pop(attr,None)
   if el.name in ('input','button','select','textarea'):el['disabled']='disabled'
   if el.name=='a' and el.get('href','').lower().startswith('market:'):
    original=el['href'];el.name='span';el['class']=list(el.get('class',[]))+['archive-unavailable-link'];el['data-original-url']=original;el['title']='Historical Android Market link; this retired application action is not available in the static archive.';del el['href']
    el.append(' (historical Market link)');inactive_links.append({'page':base,'url':original,'reason':'Retired Android Market action displayed as non-interactive historical text.'})
   if el.name=='a' and el.get('href') and el.find('img') and not el.get_text(strip=True):
    navnames={'index.php':'Home','about_me.php':'About Me','projects.php':'Projects','websites.php':'Websites','pictures.php':'Photos','videos.php':'Videos'}
    label=navnames.get(urlsplit(el['href']).path.rsplit('/',1)[-1].lower())
    if label:el['aria-label']=label;el.find('img')['alt']=label
   if el.get('href'):
    original=normal(el['href'],base);el['href']=mapping(el['href'],base,current)
    if el.name=='a':
     if original and not same(original):el['target']='_blank';el['rel']='noopener noreferrer'
     else:el['target']='_self'
   for attr in ['src','poster','background']:
    if el.get(attr):el[attr]=mapping(el[attr],base,current,True)
   if el.get('srcset'):
    el['srcset']=', '.join(mapping(t.strip().split()[0],base,current,True)+(' '+' '.join(t.strip().split()[1:]) if len(t.strip().split())>1 else '') for t in el['srcset'].split(','))
   if el.get('style'):el['style']=css(el['style'],base,current)
   if el.name=='a' and any('lightbox' in value.lower() for value in (el.get('rel') or [])) and '_missing/' not in el['href'] and not el['href'].startswith('https:'):
    # Original rel may be replaced only for external links; local galleries retain it.
    el['data-gallery']=' '.join(el.get('rel',[]))
  for el in soup.find_all('style'):el.string=css(el.get_text(),base,current)
  # Preserve gallery group names before adding external rel attributes if necessary.
  for el in soup.select('a[rel]'):
   if any('lightbox' in x.lower() for x in el.get('rel',[])) and '_missing/' not in el['href'] and not el['href'].startswith('https:'):el['data-gallery']=' '.join(el['rel'])
  if not soup.html:
   wrapper=BeautifulSoup('<html><head></head><body></body></html>','html.parser');wrapper.body.append(soup);soup=wrapper
  if not soup.head:soup.html.insert(0,soup.new_tag('head'))
  if not soup.body:soup.html.append(soup.new_tag('body'))
  for meta in soup.find_all('meta',attrs={'http-equiv':re.compile('content-type',re.I)}):meta.decompose()
  for meta in soup.find_all('meta',charset=True):meta.decompose()
  soup.head.insert(0,soup.new_tag('meta',charset='utf-8'));soup.head.insert(1,soup.new_tag('meta',attrs={'name':'robots','content':'noindex'}))
  csp="default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src data:; media-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'"
  soup.head.insert(2,soup.new_tag('meta',attrs={'http-equiv':'Content-Security-Policy','content':csp}));soup.head.append(soup.new_tag('link',rel='stylesheet',href=relative('site/_archive/archive.css',current)))
  script=soup.new_tag('script',src=relative('site/_archive/archive.js',current),defer='defer');soup.head.append(script)
  stamp=r['actual_timestamp'];date=stamp[:4]+'-'+stamp[4:6]+'-'+stamp[6:8]
  notice=soup.new_tag('aside',attrs={'class':'archive-notice','role':'note'});notice.append('Archived website · requested '+requested_full+' · this page captured '+date+'. ')
  if r.get('supplemental_capture'):notice.append('This linked page survives only as a supplemental capture from another year. ')
  notice.append('Images may have different capture dates. ')
  for label,target in [('Archive home','snapshot.html'),('Files and capture dates','archive-index.html')]:
   a=soup.new_tag('a',href=relative(target,current),target='_self');a.string=label;notice.append(a);notice.append(' · ')
  notice.append('Forms are inactive; navigation and galleries work locally.');soup.body.insert(0,notice)
  return str(soup)
 # Write all resources; recovered scripts remain inert, only the audited helper executes.
 (OUT/'missing-asset.svg').write_text(MISSING,encoding='utf8');helper=OUT/'site/_archive';helper.mkdir(parents=True,exist_ok=True);(helper/'archive.css').write_text(STYLE,encoding='utf8');(helper/'archive.js').write_text(JS,encoding='utf8')
 for r in records.values():
  if r['status']=='saved' and r['kind']=='script':continue
  if r['status']!='saved' and r['kind']!='page':
   if r.get('placeholder_path'):
    dest=OUT/r['placeholder_path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(gap(r,r['placeholder_path']),encoding='utf8');r.update(served_path=r['placeholder_path'],served_bytes=dest.stat().st_size,served_sha256=sha(dest.read_bytes()))
   continue
  current='site/'+r['local_path'];dest=OUT/current;dest.parent.mkdir(parents=True,exist_ok=True)
  if r['status']!='saved':dest.write_text(gap(r,current),encoding='utf8')
  elif r['kind']=='page':dest.write_text(page(r,current),encoding='utf8')
  elif 'css' in r.get('content_type',''):dest.write_text(css((OUT/r['raw_path']).read_text(encoding='utf8',errors='replace'),r['original_url'],current),encoding='utf8')
  else:dest.write_bytes((OUT/r['raw_path']).read_bytes())
  r.update(served_path=current,served_bytes=dest.stat().st_size,served_sha256=sha(dest.read_bytes()))
 for stale in (OUT/'site/_missing').glob('*.html'):
  if stale.resolve() not in {(OUT/r['placeholder_path']).resolve() for r in records.values() if r.get('placeholder_path')}:stale.unlink()
 (OUT/'snapshot.html').write_text(page(records[key(HOME)],'snapshot.html'),encoding='utf8')
 saved=sum(r['status']=='saved' for r in records.values());pages=sum(r['status']=='saved' and r['kind']=='page' for r in records.values());missing=len(records)-saved
 changes=['Rewrote same-site links and resource paths to lowercase local files; distinct content-query variants use a stable hash in the filename.','Removed tracking and original executable scripts; preserved their raw source as inert text. Reimplemented photo accordion/gallery and video-tab selection with an audited local helper; hover artwork could not be recovered, so navigation uses its original normal-state images.','Converted handler-only navigation into real local links; labeled image navigation for accessibility and repaired the existing TxtBack fragment link to its matching project paragraph.','Disabled forms and account/server actions. Flash/Java embeds are source links, not emulated; external videos open at their original publisher.','Gallery thumbnails/full images substitute for their own missing counterpart only when paired in the original source, with an explicit note and per-image provenance. Replaced unavailable images with an explicit placeholder; missing background assets are transparent. Unavailable site pages have a local notice.','Preserved original source bytes with exact capture provenance and SHA-256; the served copies are separately hashed.']
 manifest={'title':"Quinn Damerell's original website — "+requested_month,'requested_timestamp':TARGET,'requested_url':f'https://web.archive.org/web/{TARGET}/{HOME}','copied_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Same-site pages reachable from the exact requested homepage, plus referenced image, CSS, script, and downloadable resources. External navigation destinations are not recursively crawled. Every discovered resource is recorded as recovered or unavailable with bounded retrieval evidence. Every resource records its actual capture date; copies more than one year from the target are labeled supplements.','static_changes':changes,'files':sorted([{k:v for k,v in r.items() if k!='source_file'} for r in records.values()],key=lambda r:r['original_url']),'external_links':sorted(external),'excluded':state.get('excluded',[]),'helper_script':{'path':'site/_archive/archive.js','sha256':sha((helper/'archive.js').read_bytes()),'purpose':'Local rollovers, photo accordion/gallery, and video selection; no network requests or storage'},'inactive_links':list({json.dumps(x,sort_keys=True):x for x in inactive_links}.values()),'display_substitutions':list({json.dumps(x,sort_keys=True):x for x in substitutions}.values()),'counts':{'total':len(records),'saved':saved,'pages':pages,'unavailable':missing},'integrity':'sha256 and bytes describe raw recovered bytes. served_sha256 and served_bytes describe rewritten local copies. Original PHP server programs and databases were not captured.'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 summary={'title':manifest['title'],'url':HOME,'wayback_url':manifest['requested_url'],'requested_timestamp':TARGET,'homepage_actual_timestamp':records[key(HOME)]['actual_timestamp'],'pages':pages,'saved_resources':saved,'unavailable_resources':missing,'snapshot_sha256':sha((OUT/'snapshot.html').read_bytes()),'snapshot_bytes':(OUT/'snapshot.html').stat().st_size,'scope':manifest['scope'],'static_changes':changes}
 (OUT/'snapshot.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 rows=[]
 for r in manifest['files']:
  target=r.get('served_path') or r.get('raw_path') or r['requested_wayback_url'];status=r['status']+(' (supplemental capture)' if r.get('supplemental_capture') else '')
  rows.append('<tr><td><a href="'+html.escape(target,quote=True)+'">'+html.escape(r['original_url'])+'</a></td><td>'+r['kind']+'</td><td>'+r.get('actual_timestamp','—')+'</td><td>'+status+'</td><td>'+str(r.get('bytes','—'))+'</td></tr>')
 intro='<p><a href="snapshot.html">Explore the archived site</a> · <a href="manifest.json">Machine-readable manifest</a></p><h1>QuinnDamerell.com — '+requested_month+' archive</h1><p>The homepage was captured '+requested_full+' at '+requested_time+'. Linked pages and resources have independent dates; later copies are labeled supplements.</p><p>This copy contains '+str(pages)+' recovered pages and '+str(saved)+' recovered resources. '+str(missing)+' discovered resources were unavailable after the recorded retrieval attempts.</p><p>Original navigation and gallery interactions have local replacements; hover-state artwork was not recovered. Forms, accounts, Java applets, and Flash players are inactive. Original scripts remain available as inert source files. Missing images have visible placeholders.</p><table><thead><tr><th>Original URL / local copy</th><th>Kind</th><th>Actual capture (UTC)</th><th>Status</th><th>Raw bytes</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
 (OUT/'archive-index.html').write_text(shell(requested_month+' site recovery inventory',intro),encoding='utf8')
 (OUT/'README.txt').write_text('QuinnDamerell.com — '+requested_month+'\n\nOpen snapshot.html to browse the archive.\nExact requested homepage: '+manifest['requested_url']+'\n\n'+manifest['scope']+'\n\n'+'\n'.join(changes)+'\n\nSee archive-index.html and manifest.json for all capture dates, source URLs, hashes, supplements, and unavailable resources.\n',encoding='utf8')
 print(json.dumps(summary,indent=2),flush=True)
 return manifest
if __name__=='__main__':publish()
