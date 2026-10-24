"""Resume a Wayback mirror from its manifest; preserve raw bytes, never execute JS.

Requires Python 3.10+, beautifulsoup4 and curl. Downloads use bounded retries,
Memento headers and MIME checks. Output rewriting is a separate audited step.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, urljoin, quote, unquote, parse_qsl, urlencode
import argparse, concurrent.futures, datetime as dt, email.utils, hashlib, html, json, re, shutil, subprocess
from bs4 import BeautifulSoup

P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--output',type=Path,required=True)
P.add_argument('--cache',type=Path,required=True)
P.add_argument('--reuse',type=Path,action='append',default=[])
P.add_argument('--reuse-state',type=Path,action='append',default=[])
P.add_argument('--retry-missing',action='store_true')
P.add_argument('--retry-url',action='append',default=[])
P.add_argument('--inventory',type=Path)
P.add_argument('--reuse-only',action='store_true',help='Import matching preserved successes; make no network requests.')
P.add_argument('--max-resources',type=int,default=500)
A=P.parse_args();OUT=A.output.resolve();A.cache.mkdir(parents=True,exist_ok=True)
CURL=shutil.which('curl.exe') or shutil.which('curl')
if not CURL and not A.reuse_only:raise RuntimeError('curl was not found on PATH')
M=json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
TARGET=M['requested_timestamp'];ROOT='http://www.quinndamerell.com/'
records={r['original_url']:r for r in M['files']};sha=lambda b:hashlib.sha256(b).hexdigest()
STAMP=lambda s:dt.datetime.strptime(s,'%Y%m%d%H%M%S')
def normal(v,base):
    v=html.unescape(v.strip())
    if not v or v.startswith(('#','data:','mailto:','tel:','javascript:')):return None
    v=re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z]+_)?/','',v)
    p=urlsplit(urljoin(base,v));host=(p.hostname or '').lower()
    if p.scheme not in ('http','https'):return None
    if host in ('quinndamerell.com','www.quinndamerell.com'):host='www.quinndamerell.com'
    query=urlencode([(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if k.lower()!='phpsessid']) if 'phpsessid' in p.query.lower() else p.query
    return urlunsplit(('http' if host=='www.quinndamerell.com' else p.scheme,host,p.path or '/',query,''))
def kind(url):
    ext=Path(urlsplit(url).path).suffix.lower()
    return 'script' if ext=='.js' else ('page' if ext in ('','.php','.html','.htm','.asp','.aspx') else 'asset')
inventory=json.loads(A.inventory.read_text(encoding='utf8')) if A.inventory else []
def references(r):
    if r['status']!='saved':return []
    data=(OUT/r['raw_path']).read_bytes();url=r['original_url'];refs=[]
    if r['kind']=='page':
        soup=BeautifulSoup(data,'html.parser')
        for el in soup.find_all(True):
            for attr in ('href','src','poster','background'):
                if el.get(attr):
                    u=normal(el[attr],url)
                    if u and (attr!='href' or el.name=='link' or u.startswith(ROOT)):refs.append((u,'script' if el.name=='script' else kind(u)))
            if el.get('onclick'):
                for value in re.findall(r'(?:location(?:\.href)?\s*=|(?:window\.)?open\()\s*[\'"]([^\'"]+)',el['onclick']):
                    u=normal(value,url)
                    if u and u.startswith(ROOT):refs.append((u,kind(u)))
            if el.get('srcset'):
                for value in el['srcset'].split(','):
                    u=normal(value.strip().split()[0],url)
                    if u:refs.append((u,'asset'))
        text='\n'.join(el.get('style','') for el in soup.find_all(True))+'\n'+'\n'.join(el.get_text() for el in soup.find_all('style'))
        for script in soup.find_all('script'):
            for value in re.findall(r'[\'"]([^\'"\s]+\.(?:png|jpe?g|gif|css))[\'"]',script.get_text(),re.I):
                u=normal(value,url)
                if u:refs.append((u,'asset'))
    elif 'css' in r.get('content_type',''):text=data.decode('utf8',errors='replace')
    elif r['kind']=='script':
        # Preserve dependencies named in original scripts, including hover art;
        # original code remains inert and is never evaluated.
        text=data.decode('utf8',errors='replace')
        for value in re.findall(r'[\'"]([^\'"\s]+\.(?:png|jpe?g|gif|css))[\'"]',text,re.I):
            u=normal(value,url)
            if u:refs.append((u,'asset'))
    else:return []
    for value in re.findall(r'url\(\s*[\'"]?([^\)\'\"]+)',text,re.I)+re.findall(r'@import\s+[\'"]([^\'\"]+)',text,re.I):
        u=normal(value,url)
        if u:refs.append((u,'asset'))
    return refs
def reuse(url):
    choices=[]
    for root in A.reuse:
        path=root/'manifest.json'
        if path.exists():
            for r in json.loads(path.read_text(encoding='utf8'))['files']:
                if r['status']=='saved' and r['original_url']==url:choices.append((r,root/r['raw_path']))
    for path in A.reuse_state:
        if path.exists():
            for r in json.loads(path.read_text(encoding='utf8'))['records']:
                if r['status']=='saved' and r['original_url']==url and Path(r.get('source_file','')).is_file():choices.append((r,Path(r['source_file'])))
    if not choices:return None
    r,path=min(choices,key=lambda rp:abs((STAMP(rp[0]['actual_timestamp'])-STAMP(TARGET)).total_seconds()))
    result=dict(r);result.update(source_file=str(path),reused_preserved_source=True,requested_timestamp=TARGET,requested_wayback_url=f'https://web.archive.org/web/{TARGET}id_/{url}')
    result.pop('local_path',None);result.pop('raw_path',None)
    return result
def download(item):
    url,k=item
    cached=reuse(url)
    if cached:return cached
    key=sha(url.encode());dest=A.cache/(key+'.bin');headers=A.cache/(key+'.headers');attempts=[]
    image=bool(re.search(r'\.(png|jpe?g|gif|ico)(?:\?|$)',url,re.I))
    modes=[(TARGET,'im_',url),(TARGET,'id_',url)] if image else [(TARGET,'id_',url),(TARGET,'id_',url)]
    candidates=[row for row in inventory if len(row)>2 and str(row[0]).isdigit() and normal(row[1],ROOT)==url]
    if candidates:
        closest=min(candidates,key=lambda row:abs((STAMP(row[0])-STAMP(TARGET)).total_seconds()))
        modes.insert(0,(closest[0],'id_',closest[1]))
    for timestamp,mode,source_url in modes:
        encoded=quote(source_url,safe=':/?=&;%+,@!$()*[]~')
        requested=f'https://web.archive.org/web/{timestamp}{mode}/{encoded}'
        got=subprocess.run([CURL,'-sS','-L','--retry','1','--retry-delay','1','--connect-timeout','8','--max-time','22','--max-filesize','24000000','-D',str(headers),'-o',str(dest),'-w','%{http_code}\n%{url_effective}',requested],capture_output=True,text=True)
        hdr=headers.read_text(encoding='utf8',errors='replace') if headers.exists() else '';lines=got.stdout.splitlines();status=lines[0] if lines else '000'
        stamps=re.findall(r'^memento-datetime:\s*(.+)$',hdr,re.I|re.M);types=re.findall(r'^content-type:\s*([^;\r\n]+)',hdr,re.I|re.M);mime=types[-1].strip() if types else ''
        valid=got.returncode==0 and status=='200' and bool(stamps) and ((k=='page' and 'html' in mime) or (k!='page' and 'html' not in mime))
        attempts.append(dict(requested_wayback_url=requested,http_status=status,curl_exit_code=got.returncode,content_type=mime,accepted=valid,error=got.stderr.strip()))
        if valid:
            data=dest.read_bytes();actual=email.utils.parsedate_to_datetime(stamps[-1]).strftime('%Y%m%d%H%M%S')
            return dict(original_url=url,kind=k,status='saved',requested_timestamp=TARGET,requested_wayback_url=f'https://web.archive.org/web/{TARGET}id_/{url}',actual_timestamp=actual,resolved_wayback_url=lines[-1],content_type=mime,bytes=len(data),sha256=sha(data),http_status='200',recovery_attempts=attempts,source_file=str(dest))
        if status=='404':break
    return dict(original_url=url,kind=k,status='unavailable',requested_timestamp=TARGET,requested_wayback_url=f'https://web.archive.org/web/{TARGET}id_/{url}',http_status=status,recovery_attempts=attempts,reason='No valid archived resource recovered after bounded replay attempts; see recorded status/MIME evidence. This does not prove no capture exists.')
def local_path(r):
    url=r['original_url'];p=urlsplit(url)
    s='/'.join(re.sub(r'[^a-zA-Z0-9._-]','_',unquote(x)) for x in p.path.lstrip('/').split('/') if x not in ('.','..')).lower()
    if not s or s.endswith('/'):s+='index.html'
    if r['kind']=='page' and not s.endswith(('.html','.htm')):s+='.html'
    if p.query:s+='--'+sha(p.query.encode())[:10]
    if 'css' in r.get('content_type','') and not s.endswith('.css'):s+='.css'
    if p.hostname!='www.quinndamerell.com':s='_external/'+p.hostname+'/'+s
    used={r.get('local_path'):r['original_url'] for r in records.values() if r['status']=='saved'}
    if s in used and used[s]!=url:
        q=Path(s);s=str(q.with_name(q.stem+'--'+sha(url.encode())[:8]+q.suffix)).replace('\\','/')
    return s
def merge(r):
    url=r['original_url'];prior=records.get(url,{})
    if r['status']=='saved':
        data=Path(r.pop('source_file')).read_bytes();local=prior.get('local_path') or local_path(r)
        r['local_path']=local;r['raw_path']=prior.get('raw_path') or 'raw/'+local+('.txt' if r['kind'] in ('page','script') or 'css' in r['content_type'] or 'svg' in r['content_type'] else '')
        r['bytes']=len(data);r['sha256']=sha(data)
        offset=(STAMP(r['actual_timestamp'])-STAMP(TARGET)).total_seconds()/86400
        r['capture_offset_days']=round(offset,3);r['supplemental_capture']=r['kind']=='page' and abs(offset)>366
        dest=OUT/r['raw_path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        prior.pop('reason',None);prior.pop('placeholder_path',None)
    prior.update(r);records[url]=prior
    print(r['status'],r.get('actual_timestamp',''),url,flush=True)
def save():
    M['files']=sorted(records.values(),key=lambda r:r['original_url']);M['scope']='All same-site links reachable from the requested homepage and recovered pages, including legacy menu targets, and referenced assets. External navigational sites are not crawled. Sources are never executed. Every actual capture date is disclosed; later captures are restorations, not evidence that their bytes existed at the requested date.'
    M['url_aliases']=[{'original_url':ROOT,'target_url':ROOT+'index.html','reason':'Root navigation intentionally returns to the exact requested April 2012 homepage in this archive.'}]
    (OUT/'manifest.json').write_text(json.dumps(M,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
pending=[(r['original_url'],r['kind']) for r in records.values() if A.retry_missing and r['status']!='saved']
pending.extend((url,records.get(url,{}).get('kind',kind(url))) for url in A.retry_url)
processed=set();expanded=set()
while True:
    for r in list(records.values()):
        if r['status']=='saved' and r['original_url'] not in expanded:
            expanded.add(r['original_url'])
            pending.extend((u,k) for u,k in references(r) if u!=ROOT and u not in records)
    pending=list(dict(pending).items());pending=[x for x in pending if x[0] not in processed]
    if not pending:break
    if len(records)+len(pending)>A.max_resources:raise RuntimeError('Resource cap exceeded; inspect crawl graph before continuing')
    processed.update(u for u,k in pending)
    if A.reuse_only:
        for url,k in pending:
            result=reuse(url)
            if result:merge(result);save()
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            for result in pool.map(download,pending):merge(result);save()
    pending=[]
save();print('DONE',len(records),'records',len(processed),'retrieval/reuse attempts')
