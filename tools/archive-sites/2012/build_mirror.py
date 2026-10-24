"""Build a contained, browsable mirror from preserved source bytes and manifest.

Python 3.10+ and beautifulsoup4. Only the small audited helper below executes;
historical scripts remain inert. No network access is used by this builder.
"""
from pathlib import Path
from urllib.parse import urlsplit,urljoin,urlunsplit,parse_qsl,urlencode
import argparse,base64,hashlib,html,json,os,re
from bs4 import BeautifulSoup
from bs4.element import Stylesheet
P=argparse.ArgumentParser(description=__doc__);P.add_argument('--output',required=True,type=Path)
P.add_argument('--historical-only',action='store_true',help='Build explicit historical_pages without rewriting the ordinary mirror.')
P.add_argument('--add-historical',action='append',default=[],metavar='CAPTURE.html',help='Register an existing history reader/source capture by its reader filename.')
A=P.parse_args()
OUT=A.output.resolve();M=json.loads((OUT/'manifest.json').read_text(encoding='utf8'));TARGET=M['requested_timestamp']
records={r['original_url']:r for r in M['files']};sha=lambda b:hashlib.sha256(b).hexdigest()
ROOT='http://www.quinndamerell.com/';HOME=ROOT+'index.html'
aliases={a['original_url']:a['target_url'] for a in M.get('url_aliases',[])}
fragment_targets={};missing_previews={}
capture_context={}
def normal(value,base):
    value=html.unescape(value.strip())
    if not value or value.startswith(('#','data:','mailto:','tel:','javascript:')):return None
    value=re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z]+_)?/','',value)
    p=urlsplit(urljoin(base,value));host=(p.hostname or '').lower()
    if p.scheme not in ('http','https'):return None
    if host in ('quinndamerell.com','www.quinndamerell.com'):host='www.quinndamerell.com'
    query=urlencode([(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if k.lower()!='phpsessid']) if 'phpsessid' in p.query.lower() else p.query
    u=urlunsplit(('http' if host=='www.quinndamerell.com' else p.scheme,host,p.path or '/',query,''))
    return aliases.get(u,u)
def relative(target,current):return os.path.relpath(OUT/target,(OUT/current).parent).replace('\\','/')
def find(url):
    if url in records:return records[url]
    matches=[r for u,r in records.items() if u.lower()==url.lower() and r['status']=='saved']
    return matches[0] if len(matches)==1 else None
def mapping(value,base,current,resource=False):
    url=normal(value,base)
    if not url:return '#' if value.lower().startswith('javascript:') else value
    capture=capture_context.get(current)
    if capture:
        if not resource and url==normal(capture['original_url'],capture['original_url']):
            fragment=urlsplit(value).fragment
            return relative(current,current)+('#'+fragment if fragment else '')
        url=capture.get('resource_aliases',{}).get(url,url) if resource else url
        gap=next((g for g in capture.get('capture_gaps',[]) if g['original_url']==url),None)
        if gap and not resource:return relative(gap['served_path'],current)
    r=find(url)
    if r and r['status']=='saved' and r['kind']!='script':
        frag=urlsplit(value).fragment
        return relative('site/'+r['local_path'],current)+('#'+frag if frag else '')
    if r and r.get('placeholder_path') and not resource:return relative(r['placeholder_path'],current)
    if resource:return relative('missing-asset.svg',current)
    if r and r['kind']=='asset' and re.search(r'\.(png|jpe?g|gif|ico)$',url,re.I):return relative('missing-asset.svg',current)
    return f'https://web.archive.org/web/{capture["actual_timestamp"] if capture else TARGET}/{url}'
cssurl=re.compile(r'url\(\s*[\'"]?([^\)\'\"]+)[\'"]?\s*\)',re.I)
cssimport=re.compile(r'@import\s+[\'"]([^\'\"]+)[\'"]',re.I)
def css(text,base,current):
    def replace(m):
        url=normal(m.group(1),base)
        if not url:return m.group(0)
        r=find(url)
        if r and r['status']=='saved' and (re.search(r'\.(ttf|otf|woff2?|eot)$',url,re.I) or r.get('content_type','').startswith('font/')):
            return 'url("data:'+r.get('content_type','font/ttf')+';base64,'+base64.b64encode((OUT/r['raw_path']).read_bytes()).decode()+'")'
        return 'url("'+mapping(m.group(1),base,current,True)+'")'
    text=cssurl.sub(replace,text)
    return cssimport.sub(lambda m:'@import "'+mapping(m.group(1),base,current,True)+'"',text)

HELPER_JS=r'''/* Audited archive replacement: DOM-only gallery and original header flip.
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
'''
HELPER_CSS='''/* Modern equivalents for preserved navigation and local image gallery. */
html {scroll-behavior:smooth}
.archive-menu-link {display:block;color:inherit;text-decoration:inherit;min-height:inherit}
.archive-form-note {padding:12px;border:1px solid #888;background:#fff;color:#333;font:14px/1.5 system-ui,sans-serif}
.archive-accordion {margin:8px 0;border:1px solid #bbb}
.archive-accordion>summary {cursor:pointer;background:#ddd;color:#222;padding:8px;font-weight:bold;min-height:24px}
.archive-accordion>div {height:auto!important;overflow:visible!important;padding:8px}
.archive-gallery {padding:16px;background:#161616;color:white;border:1px solid #777;max-width:94vw;max-height:94vh;box-sizing:border-box;text-align:center}
.archive-gallery::backdrop {background:rgba(0,0,0,.85)}
.archive-gallery>img {display:block;max-width:85vw;max-height:72vh;width:auto;height:auto;margin:12px auto}
.archive-gallery-controls {display:flex;justify-content:center;gap:12px}
.archive-gallery-controls button {font:16px system-ui,sans-serif;padding:8px 16px;cursor:pointer}
.archive-gallery-caption {font:14px/1.5 system-ui,sans-serif;margin:6px;color:#fff}
#livetile {transform-style:preserve-3d;transition:transform .8s;cursor:pointer}
#livetile .face {backface-visibility:hidden}
#livetile .back {transform:rotateX(-180deg)}
#livetile:focus-visible {outline:3px solid #e68e25;outline-offset:5px}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}#livetile{transition:none}}
'''
def page(r,current):
    soup=BeautifulSoup((OUT/r['raw_path']).read_bytes(),'html.parser');base=r['original_url']
    for adjustment in r.get('presentation_adjustments',[]):
        if adjustment['type']=='decorative_background':
            for style in soup.find_all('style'):
                style.string=Stylesheet(cssurl.sub(lambda match:'none' if normal(match.group(1),base)==adjustment['original_url'] else match.group(0),style.get_text()))
            for element in soup.select(adjustment['selector']):
                element['style']=element.get('style','')+';background-color:'+adjustment['fallback_color']+';'
        elif adjustment['type']=='decorative_bullet':
            for image in soup.find_all('img'):
                if normal(image.get('src',''),base)==adjustment['original_url']:
                    bullet=soup.new_tag('span',attrs={'aria-hidden':'true','style':'display:inline-block;width:11px;text-align:center;font-size:11px;line-height:11px;'})
                    bullet.string='•';image.replace_with(bullet)
    script_text='\n'.join(el.get_text() for el in soup.find_all('script'))
    hover_sources=dict(re.findall(r'(\w+)\.src\s*=\s*[\'"]([^\'"]+)[\'"]',script_text))
    if not soup.html:
        doc=BeautifulSoup('<!doctype html><html><head></head><body></body></html>','html.parser')
        doc.body.extend(list(soup.contents));soup=doc
    if not soup.head:soup.html.insert(0,soup.new_tag('head'))
    if not soup.body:
        body=soup.new_tag('body');body.extend([x.extract() for x in list(soup.html.contents) if x!=soup.head]);soup.html.append(body)
    if r.get('historical_capture'):
        # Preserve fallback multimedia notices after the original player is removed.
        for el in soup.find_all('noscript'):el.unwrap()
    for el in list(soup.select('object,embed')):
        if not el.parent:continue
        value=el.get('data') or el.get('src')
        if not value:
            param=el.find('param',attrs={'name':re.compile(r'^(movie|src)$',re.I)})
            if param:value=param.get('value')
        note=soup.new_tag('p',attrs={'class':'archive-form-note'});note.append('Original embedded multimedia required an unavailable player or service. ')
        if value:
            a=soup.new_tag('a',href=mapping(value,base,current));a.string='Original archived destination';note.append(a)
        el.replace_with(note)
    for el in soup.select('script,noscript,base,meta[http-equiv="refresh" i],meta[http-equiv="content-security-policy" i]'):el.decompose()
    for panel in soup.select('.AccordionPanel'):
        tab=panel.select_one('.AccordionPanelTab,.AccordionPanelTab_new');content=panel.select_one('.AccordionPanelContent')
        if tab and content:
            panel.name='details';panel['class']=['archive-accordion'];tab.name='summary';tab.attrs={};content['style']='height:auto;overflow:visible'
    for accordion in soup.select('.Accordion'):
        first=accordion.select_one('details')
        if first:first['open']='open'
    for el in soup.find_all('iframe'):
        a=soup.new_tag('a',href=mapping(el.get('src',''),base,current));a.string='View original embedded content (external archive link)';el.replace_with(a)
    for el in list(soup.find_all(True)):
        if not el.name:continue
        handler=el.get('onclick','');scroll=re.search(r'goToByScroll\(\s*[\'"]([^\'"]+)',handler)
        video=re.search(r'showbox\(\s*[\'"]([^\'"]+)',handler)
        if video:
            el['href']='#'+video.group(1);el['data-archive-video']=video.group(1);el['aria-controls']=video.group(1)
        nav=re.search(r'(?:window\.)?location(?:\.href)?\s*=\s*[\'"]([^\'"]+)',handler)
        hover=re.search(r'document\.(\w+)\.src\s*=\s*(\w+)\.src',el.get('onmouseover',''))
        if hover and hover.group(2) in hover_sources:
            image=soup.find('img',attrs={'name':hover.group(1)});u=normal(hover_sources[hover.group(2)],base)
            source=find(u) if u else None
            if image and source and source['status']=='saved':image['data-archive-hover']=mapping(hover_sources[hover.group(2)],base,current,True)
        if scroll:el['href']='#'+scroll.group(1)
        if nav:
            if el.name=='a':el['href']=nav.group(1)
            else:
                a=soup.new_tag('a',href=nav.group(1),attrs={'class':'archive-menu-link'});a.extend([x.extract() for x in list(el.contents)]);el.append(a)
        for attr in list(el.attrs):
            if attr.lower().startswith('on') or attr in ('srcdoc','integrity','crossorigin'):del el[attr]
        if el.name=='form':
            el.name='div';el.attrs.pop('action',None);el.attrs.pop('method',None)
            note=soup.new_tag('p',attrs={'class':'archive-form-note'});note.string='Historical form: submission required the original server and is unavailable in this offline archive.';el.insert(0,note)
        if el.name in ('button','input','select','textarea'):el['disabled']='disabled'
        if el.name=='a':
            rel=' '.join(el.get('rel',[])).lower()
            source=find(normal(el.get('href',''),base) or '')
            if el.get('href') and source and source['status']=='saved' and ('screenshots' in rel or 'lightbox' in rel) and re.search(r'\.(png|jpe?g|gif)(?:[?#]|$)',el['href'],re.I):el['data-archive-gallery']=rel
        if el.get('href'):
            resource=el.name=='link' and 'canonical' not in el.get('rel',[])
            if resource and 'icon' in ' '.join(el.get('rel',[])).lower():
                fr=find(normal(el['href'],base) or '')
                if not fr or fr['status']!='saved':el['href']=ROOT+'favicon.ico'
            el['href']=mapping(el['href'],base,current,resource)
        for attr in ('src','poster','background'):
            if el.get(attr):el[attr]=mapping(el[attr],base,current,True)
        if el.get('srcset'):
            el['srcset']=', '.join(mapping(piece.strip().split()[0],base,current,True)+(' '+piece.strip().split(maxsplit=1)[1] if len(piece.strip().split(maxsplit=1))>1 else '') for piece in el['srcset'].split(','))
        if el.get('style'):el['style']=css(el['style'],base,current)
    # Handle newly created anchors as well as original links.
    for a in soup.find_all('a'):
        if a.get('href') and a.get('class')==['archive-menu-link']:a['href']=mapping(a['href'],base,current)
        if a.get('href','').startswith(('http:','https:','mailto:','tel:')):a['target']='_blank';a['rel']=['noopener','noreferrer']
        else:a['target']='_self'
    for el in soup.find_all('style'):el.string=css(el.get_text(),base,current)
    if soup.select('a[data-archive-video]'):
        for box in soup.find_all(id=re.compile(r'^box\d+$')):
            box['data-archive-video-panel']='';box['style']='display:block;position:relative;max-width:100%'
            if box['id']=='box10':
                box.clear();note=soup.new_tag('p',attrs={'class':'archive-form-note'});note.string='Choose a video title to view its original archived destination. The original Flash video player cannot run in this offline copy.';box.append(note)
    r['restored_fragment_targets']=[]
    for fragment in sorted(r.get('required_fragments',[]) if r.get('historical_capture') else fragment_targets.get(base,set())):
        if soup.find(id=fragment) or soup.find('a',attrs={'name':fragment}):continue
        # The source project paragraph exists; the old homepage omitted its ID.
        paragraph=next((p for p in soup.find_all('p') if fragment=='TxtBack' and p.get_text(' ',strip=True).startswith('TxtBack')),None)
        if paragraph:
            paragraph['id']=fragment;reason='Attached missing original fragment to the existing matching project paragraph.'
        else:
            note=soup.new_tag('p',id=fragment,attrs={'class':'archive-form-note'});note.string=f'Original section unavailable: {fragment}. The source linked to this section, but its content or target was absent from the recovered page.';soup.body.append(note);reason='Visible archive gap notice; no original section text invented.'
        r['restored_fragment_targets'].append({'fragment':fragment,'reason':reason})
    soup.head.insert(0,soup.new_tag('meta',charset='utf-8'))
    soup.head.insert(1,soup.new_tag('meta',attrs={'name':'robots','content':'noindex'}))
    soup.head.insert(2,soup.new_tag('meta',attrs={'http-equiv':'Content-Security-Policy','content':"default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src data:; script-src 'self'; media-src 'self'; form-action 'none'; base-uri 'none'"}))
    soup.head.append(soup.new_tag('link',rel='canonical',href=base))
    soup.head.append(soup.new_tag('link',rel='stylesheet',href=relative('archive-ui.css',current)))
    soup.head.append(soup.new_tag('script',src=relative('archive-ui.js',current),defer='defer'))
    banner=soup.new_tag('aside',attrs={'role':'note','class':'archive-notice','style':'display:block;box-sizing:border-box;width:100%;margin:0 0 14px;padding:10px 16px;background:#111114;color:#ededf2;font:14px/1.5 system-ui,sans-serif;text-align:center;position:relative;z-index:2147483647;'})
    stamp=r['actual_timestamp'];date=f'{stamp[:4]}-{stamp[4:6]}-{stamp[6:8]}'
    if r.get('historical_capture'):
        banner.append(f'Historical website capture · original HTML captured {date} at {stamp[8:10]}:{stamp[10:12]}:{stamp[12:14]} UTC. ')
        banner.append('Original layout restored using locally recovered assets from other dates. Links continue into the wider archived site. ')
    else:banner.append(f'Archived website · requested April 16, 2012 · this page captured {date}. ')
    if r.get('supplemental_capture'):banner.append('Supplemental capture: a closer usable copy of this linked page was not recovered. ')
    banner.append('Images may use later captures. Local navigation and galleries restored; server features unavailable. ')
    for label,target in [('Archive home','snapshot.html'),('Files and capture dates','archive-index.html')]:
        a=soup.new_tag('a',href=relative(target,current),target='_self',style='color:#b9b2ff;text-decoration:underline');a.string=label;banner.append(a);banner.append(' · ')
    soup.body.insert(0,banner)
    return str(soup)

def build_historical_pages():
    """Render selected immutable source variants using the existing mirror only."""
    historical=M.setdefault('historical_pages',[])
    if A.add_historical:
        inventory=json.loads((OUT/'history/manifest.json').read_text(encoding='utf8'))
        for name in A.add_historical:
            item=next((x for x in inventory['items'] if x['reader']==name),None)
            if not item:raise ValueError('Unknown history reader: '+name)
            capture_id=Path(name).stem
            if any(x['capture_id']==capture_id for x in historical):continue
            source=OUT/'history'/item['source'];data=source.read_bytes()
            assert sha(data)==item['sha256_original_html'],name
            timestamp=item['timestamp'];wayback=f'https://web.archive.org/web/{timestamp}id_/{item["original"]}'
            historical.append(dict(capture_id=capture_id,title=item['title'],original_url=item['original'],kind='page',status='saved',historical_capture=True,actual_timestamp=timestamp,requested_timestamp=timestamp,requested_wayback_url=wayback,resolved_wayback_url=wayback,source_inventory='history/manifest.json',source_digest=item['digest'],raw_path='history/'+item['source'],bytes=len(data),sha256=sha(data),local_path='_captures/'+name,served_path='site/_captures/'+name,content_type='text/html'))
    for r in historical:
        data=(OUT/r['raw_path']).read_bytes();assert len(data)==r['bytes'] and sha(data)==r['sha256'],r['capture_id']
        current=r['served_path'];capture_context[current]=r
        r['resource_aliases']={};r['references']=[];r['capture_gaps']=[];r['required_fragments']=[]
        r.pop('presentation_adjustments',None)
        if r['capture_id']=='20090526070712-QVB4AXXJ':
            r['presentation_adjustments']=[]
            for adjustment in [
                {'original_url':ROOT+'images/stripe.png','type':'decorative_background','selector':'.links','fallback_color':'#444444','reason':'The original decorative stripe image is unavailable. A solid dark neutral background preserves readability of the original white sidebar text.'},
                {'original_url':ROOT+'images/bullet.png','type':'decorative_bullet','reason':'The original 11-pixel decorative bullet image is unavailable. A small text bullet replaces it; no original image bytes are claimed.'}]:
                source=find(adjustment['original_url'])
                if not source or source['status']!='saved':r['presentation_adjustments'].append(adjustment)
        soup=BeautifulSoup(data,'html.parser');refs=[];multimedia=set();favicons=set()
        for el in soup.find_all(True):
            if el.name in ('script','noscript'):continue
            for attr in ('href','src','poster','background'):
                value=el.get(attr)
                if value:refs.append((value,el.name=='a' and attr=='href'))
            for value in cssurl.findall(el.get('style','')):refs.append((value,False))
            if el.name=='style':refs.extend((value,False) for value in cssurl.findall(el.get_text()))
            scroll=re.search(r'goToByScroll\(\s*[\'"]([^\'"]+)',el.get('onclick',''))
            if scroll:r['required_fragments'].append(scroll.group(1))
            if el.name in ('object','embed'):
                value=el.get('src') or el.get('data')
                if value:multimedia.add(normal(value,r['original_url']))
            if el.name=='link' and 'icon' in ' '.join(el.get('rel',[])).lower():favicons.add(normal(el.get('href',''),r['original_url']))
        seen=set()
        for value,navigation in refs:
            url=normal(value,r['original_url'])
            if not url or (url,navigation) in seen:continue
            seen.add((url,navigation));entry={'original_url':url,'kind':'navigation' if navigation else 'resource'}
            adjustment=next((a for a in r.get('presentation_adjustments',[]) if a['original_url']==url),None)
            if adjustment and not navigation:
                entry.update(status='decorative_fallback',reason=adjustment['reason']);r['references'].append(entry);continue
            if url in multimedia:
                entry.update(status='disabled_multimedia',reason='Original multimedia player removed; the served page shows an explicit unavailable-player notice and archived destination link.');r['references'].append(entry);continue
            if navigation and url==normal(r['original_url'],r['original_url']):
                entry.update(status='current_capture',served_path=current);r['references'].append(entry);continue
            source=find(url)
            if url in favicons and (not source or source['status']!='saved'):
                source=find(ROOT+'favicon.ico')
                if source and source['status']=='saved':
                    r['resource_aliases'][url]=ROOT+'favicon.ico';entry['restored_from_url']=ROOT+'favicon.ico';entry['restoration_note']='Unavailable page-relative favicon replaced with the preserved site-root icon.'
            if not source and not navigation and '.pagespeed.' in url:
                prefix=url.split('.pagespeed.',1)[0];p=urlsplit(prefix);parts=p.path.rsplit('/',1);basename=parts[-1]
                names=[basename,re.sub(r'^\d+x\d+x','',basename),basename[1:] if basename.startswith('x') else basename]
                for name in dict.fromkeys(names):
                    candidate=urlunsplit((p.scheme,p.netloc,(parts[0]+'/' if len(parts)>1 else '')+name,p.query,''));found=find(candidate)
                    if found and found['status']=='saved':
                        source=found;r['resource_aliases'][url]=candidate
                        entry['restoration_note']='Recovered original asset reused for an unavailable PageSpeed derivative; derivative bytes are not claimed.'
                        entry['restored_from_url']=candidate;break
            if source and source['status']=='saved' and source['kind']!='script':
                entry.update(status='reused_local_capture',served_path=source.get('served_path','site/'+source['local_path']),source_actual_timestamp=source.get('actual_timestamp'),source_sha256=source['sha256'])
            elif navigation and source and source.get('placeholder_path'):
                entry.update(status='existing_gap',served_path=source['placeholder_path'])
            elif navigation and urlsplit(url).hostname=='www.quinndamerell.com':
                gap_path='site/_captures/gaps/'+sha((r['capture_id']+' '+url).encode())[:16]+'.html'
                gap={'original_url':url,'kind':'page','status':'unavailable','served_path':gap_path,'reason':'This historical source links to a destination absent from the recovered local archive. No network retrieval was performed for this additional capture.'}
                r['capture_gaps'].append(gap);entry.update(status='local_gap',served_path=gap_path)
            elif navigation:entry.update(status='external_navigation')
            else:entry.update(status='local_placeholder',served_path='missing-asset.svg',reason='Referenced asset is unavailable in the preserved local files; no new network retrieval was performed.')
            r['references'].append(entry)
        for gap in r['capture_gaps']:
            path=gap['served_path'];text='<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Historical archive gap</title><style>body{max-width:48em;margin:4em auto;padding:1em;font:18px/1.6 system-ui}a{color:#5144aa}</style></head><body><h1>Historical destination unavailable</h1><p>This source linked to <code>'+html.escape(gap['original_url'])+'</code>. Its content is not present in the recovered local files. No original page content is invented here.</p><p><a target="_self" href="'+relative(current,path)+'">Return to the '+r['actual_timestamp'][:4]+' capture</a> · <a target="_self" href="'+relative('archive-index.html',path)+'">Files and capture dates</a></p><p><a target="_blank" rel="noopener noreferrer" href="https://web.archive.org/web/'+r['actual_timestamp']+'/'+html.escape(gap['original_url'])+'">Check the destination on Wayback</a></p></body></html>'
            dest=OUT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,encoding='utf8');gap.update(served_bytes=dest.stat().st_size,served_sha256=sha(dest.read_bytes()))
        dest=OUT/current;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page(r,current),encoding='utf8');r.update(served_bytes=dest.stat().st_size,served_sha256=sha(dest.read_bytes()))
    M['historical_pages']=sorted(historical,key=lambda r:r['capture_id'])
    return historical

def historical_inventory_section():
    items=[]
    for r in M.get('historical_pages',[]):
        stamp=r['actual_timestamp'];date=f'{stamp[:4]}-{stamp[4:6]}-{stamp[6:8]} {stamp[8:10]}:{stamp[10:12]}:{stamp[12:14]} UTC'
        items.append('<li><a href="'+html.escape(r['served_path'])+'">'+html.escape(date+' — '+r['title'])+'</a> · <a href="'+html.escape(r['raw_path'])+'">exact preserved HTML source</a></li>')
    if not items:return ''
    return '<!--historical-captures:start--><section id="historical-captures"><h2>Additional historical captures</h2><p>These pages retain the HTML of the stated captures and restore their original layouts with recovered local assets. They do not replace the April 2012 homepage or its linked-page variants. Asset substitutions and local gaps are recorded under historical_pages in the manifest.</p><ul>'+''.join(items)+'</ul></section><!--historical-captures:end-->'

if A.historical_only:
    captures=build_historical_pages()
    (OUT/'manifest.json').write_text(json.dumps(M,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    inventory=(OUT/'archive-index.html').read_text(encoding='utf8')
    inventory=re.sub(r'<!--historical-captures:start-->.*?<!--historical-captures:end-->','',inventory,flags=re.S)
    (OUT/'archive-index.html').write_text(inventory.replace('</body>',historical_inventory_section()+'</body>'),encoding='utf8')
    print(json.dumps({'historical_pages':len(captures),'served_paths':[r['served_path'] for r in captures]},indent=2))
    raise SystemExit(0)

# Discover fragment destinations and missing linked resources from source HTML.
for source in list(records.values()):
    if source['status']!='saved' or source['kind']!='page':continue
    soup=BeautifulSoup((OUT/source['raw_path']).read_bytes(),'html.parser')
    for el in soup.find_all(True):
        values=[el.get('href','')]
        scroll=re.search(r'goToByScroll\(\s*[\'"]([^\'"]+)',el.get('onclick',''))
        if scroll:values.append('#'+scroll.group(1))
        for value in values:
            if not value:continue
            url=normal(value,source['original_url']) or source['original_url'];r=find(url);fragment=urlsplit(value).fragment
            if r and r['kind']=='page' and fragment:fragment_targets.setdefault(url,set()).add(fragment)
            if el.name=='a' and r and r['status']!='saved':
                r.setdefault('placeholder_path','gaps/'+sha(r['original_url'].encode())[:12]+'.html')
                img=el.find('img')
                if img:
                    preview=find(normal(img.get('src',''),source['original_url']) or '')
                    if preview and preview['status']=='saved':missing_previews[url]=preview
# Local notices keep unrecovered pages and downloads within the browsing graph.
for r in records.values():
    if r['status']=='saved':continue
    if r.get('placeholder_path') or r['kind']=='page' or (r['kind']=='asset' and re.search(r'\.(xpi|zip|exe|pdf|jar)$',r['original_url'],re.I)):
        path=r.get('placeholder_path') or 'gaps/'+sha(r['original_url'].encode())[:12]+'.html';r['placeholder_path']=path
        text='<!doctype html><html><head><meta charset="utf-8"><title>Archive gap</title><meta name="robots" content="noindex"><style>body{max-width:50em;margin:4em auto;font:18px/1.6 system-ui;padding:1em}a{color:#5144aa}</style></head><body><h1>Archived destination unavailable</h1><p>The original site linked to <code>'+html.escape(r['original_url'])+'</code>. A usable archived copy was not recovered. This notice does not reproduce or invent its original content.</p><p><a target="_blank" rel="noopener noreferrer" href="'+html.escape(r['requested_wayback_url'])+'">Check the original destination on Wayback</a></p><p><a target="_self" href="'+relative('snapshot.html',path)+'">Archive home</a> · <a target="_self" href="'+relative('archive-index.html',path)+'">Files and capture dates</a></p></body></html>'
        preview=missing_previews.get(r['original_url'])
        if preview:
            text=text.replace('</body>','<h2>Preserved thumbnail</h2><p>The original thumbnail was recovered. The linked full-size image remains unavailable.</p><img style="max-width:100%" alt="Preserved original thumbnail" src="'+relative('site/'+preview['local_path'],path)+'"></body>')
            r['available_thumbnail_url']=preview['original_url']
        dest=OUT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,encoding='utf8');r.update(served_path=path,served_bytes=dest.stat().st_size,served_sha256=sha(dest.read_bytes()))
for name,content in [('archive-ui.js',HELPER_JS),('archive-ui.css',HELPER_CSS)]:
    (OUT/name).write_text(content,encoding='utf8')
for r in records.values():
    if r['status']!='saved':continue
    data=(OUT/r['raw_path']).read_bytes();assert sha(data)==r['sha256'],r['original_url']
    if r['kind']=='script':continue
    current='site/'+r['local_path'];dest=OUT/current;dest.parent.mkdir(parents=True,exist_ok=True)
    if r['kind']=='page':dest.write_text(page(r,current),encoding='utf8')
    elif 'css' in r.get('content_type',''):dest.write_text(css(data.decode('utf8',errors='replace'),r.get('source_original_url',r['original_url']),current),encoding='utf8')
    else:dest.write_bytes(data)
    r.update(served_path=current,served_bytes=dest.stat().st_size,served_sha256=sha(dest.read_bytes()))
    if r['original_url']==HOME:(OUT/'snapshot.html').write_text(page(r,'snapshot.html'),encoding='utf8')
M['files']=sorted(records.values(),key=lambda r:r['original_url'])
M['static_changes']=['Preserved exact recovered raw bytes; historical HTML, CSS, JavaScript and SVG sources use inert .txt extensions.','Replaced historical scripts with an audited, local DOM-only gallery and header-tile helper. Original analytics, embeds, event handlers and server forms do not execute.','Restored onclick menu links and section links as ordinary anchors; local navigation stays in the iframe. External navigation opens a separate tab.','Embedded recovered font bytes in served CSS for opaque-origin iframe compatibility.','Unavailable internal pages/downloads have local explanatory notices; unavailable image assets have a visible placeholder. Every failed retrieval remains in the manifest.']
M['reconstructed_files']=[{'path':name,'bytes':(OUT/name).stat().st_size,'sha256':sha((OUT/name).read_bytes()),'purpose':'Audited local DOM gallery/header interactions; no original script execution.' if name.endswith('.js') else 'Contained gallery presentation and modern equivalents for header CSS transforms.'} for name in ('archive-ui.js','archive-ui.css')]
(OUT/'manifest.json').write_text(json.dumps(M,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
S=json.loads((OUT/'snapshot.json').read_text(encoding='utf8'))
S.update(pages=sum(r['status']=='saved' and r['kind']=='page' for r in records.values()),supplemental_pages=sum(r['status']=='saved' and r['kind']=='page' and r.get('supplemental_capture',False) for r in records.values()),saved_resources=sum(r['status']=='saved' for r in records.values()),unavailable_resources=sum(r['status']!='saved' for r in records.values()),snapshot_sha256=sha((OUT/'snapshot.html').read_bytes()),snapshot_bytes=(OUT/'snapshot.html').stat().st_size,client_functionality='Local image galleries, section links, legacy navigation and header tile restored; forms/server services unavailable.')
(OUT/'snapshot.json').write_text(json.dumps(S,indent=2)+'\n',encoding='utf8')
rows=[]
for r in M['files']:
    dest=r.get('served_path') or r.get('raw_path') or r['requested_wayback_url'];status=r['status']+(' (supplemental capture)' if r.get('supplemental_capture') else '')
    values=['<a href="'+html.escape(dest)+'">'+html.escape(r['original_url'])+'</a>',r['kind'],r.get('actual_timestamp') or ('Local restoration' if r.get('restored_from') else '—'),status,str(r.get('bytes','—'))]
    rows.append('<tr>'+''.join('<td>'+v+'</td>' for v in values)+'</tr>')
inventory='<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Archived site inventory</title><style>body{font:15px/1.5 system-ui;margin:24px;color:#222}table{border-collapse:collapse;width:100%}th,td{text-align:left;border:1px solid #ccc;padding:8px;overflow-wrap:anywhere}td:first-child{max-width:55vw}a{color:#5144aa}</style></head><body><h1>April 2012 website archive</h1><p><a href="snapshot.html">Browse the archived homepage</a> · <a href="history/index.html">Historical versions</a> · <a href="manifest.json">Full provenance manifest</a></p><p>This copy contains '+str(S['pages'])+' recovered pages and '+str(S['saved_resources'])+' recovered resources. '+str(S['unavailable_resources'])+' resources remain unavailable. The homepage HTML is the exact April 16, 2012 capture. Referenced pages and images use the closest recovered captures, sometimes years later; capture dates are shown here and on every page. Original scripts remain inert. A small local replacement restores galleries, navigation and the header flip. Original server forms and services are unavailable.</p><table><thead><tr><th>Original URL / local copy</th><th>Kind</th><th>Actual capture</th><th>Status</th><th>Original bytes</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></body></html>'
build_historical_pages()
(OUT/'manifest.json').write_text(json.dumps(M,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
(OUT/'archive-index.html').write_text(inventory.replace('</body>',historical_inventory_section()+'</body>'),encoding='utf8');print(json.dumps(S,indent=2))
