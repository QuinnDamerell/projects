from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,urljoin,unquote,quote,parse_qsl,urlencode
from bs4 import BeautifulSoup
import subprocess,concurrent.futures,json,hashlib,re,html,datetime,email.utils,gzip,os,collections,argparse,tempfile,shutil
# The recovery is reproducible with Python 3 and beautifulsoup4. See recovery-README.txt.
parser=argparse.ArgumentParser(description='Recover the linked QuinnDamerell.com historical site, preserving exact capture provenance.')
parser.add_argument('--repo-root',type=Path,default=Path.cwd())
parser.add_argument('--output',type=Path)
parser.add_argument('--cache',type=Path,default=Path(tempfile.gettempdir())/'codex-wayback-recovery/2011')
parser.add_argument('--target',default='20110116181801')
parser.add_argument('--home',default='http://www.quinndamerell.com/index.php')
parser.add_argument('--fallback-archive',type=Path)
parser.add_argument('--workers',type=int,default=2)
parser.add_argument('--alternate-timestamp',help='Optional alternate capture date for the bounded retry pass.')
args,unknown_args=parser.parse_known_args()
ROOT=args.repo_root.resolve();OUT=(args.output or ROOT/'docs/assets/media/quinndamerell-homepage-2011').resolve()
TEMP=args.cache.resolve();TEMP.mkdir(parents=True,exist_ok=True);CACHE=TEMP/'requests';CACHE.mkdir(parents=True,exist_ok=True)
TARGET=args.target;HOME=args.home;HOST=urlsplit(HOME).hostname
CURL=str(Path(os.environ.get('SystemRoot','C:/Windows'))/'System32/curl.exe') if os.name=='nt' else (shutil.which('curl') or 'curl')
sha=lambda b:hashlib.sha256(b).hexdigest()
targetdt=datetime.datetime.strptime(TARGET,'%Y%m%d%H%M%S')
CSSURL=re.compile(r'url\(\s*[\'"]?([^\)\'\"]+)[\'"]?\s*\)',re.I)
CSSIMPORT=re.compile(r'@import\s+[\'"]([^\'\"]+)[\'"]',re.I)
SCRIPTURL=re.compile(r'\.src\s*=\s*[\'"]([^\'\"]+)[\'"]',re.I)
NAVJS=re.compile(r'(?:window\.)?(?:document\.)?location(?:\.href)?\s*=\s*[\'"]([^\'\"]+)',re.I)
IGNORED=[];EXTERNAL=set()

def normal(value,base=HOME):
 value=html.unescape(str(value).strip())
 if not value or value.startswith(('#','data:','mailto:','tel:','javascript:','market:')):return None
 value=re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z]+_)?/','',value)
 p=urlsplit(urljoin(base,value));host=(p.hostname or '').lower()
 if p.scheme not in ('http','https'):return None
 if host in ('quinndamerell.com','www.quinndamerell.com'):host=HOST
 # The archive's PHP session identifiers have no content semantics.
 query=urlencode([(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if k.lower()!='phpsessid'])
 return urlunsplit(('http' if host==HOST else p.scheme,host,p.path or '/',query,''))
def key(url):
 p=urlsplit(url);return urlunsplit((p.scheme,p.netloc,p.path.lower(),p.query,''))
def same(url):return urlsplit(url).hostname==HOST
def local(url,kind):
 p=urlsplit(url);path=unquote(p.path);parts=[re.sub(r'[^a-z0-9._-]','_',x.lower()) for x in path.split('/') if x and x not in ('.','..')]
 if not same(url):parts=['_external',re.sub(r'[^a-z0-9._-]','_',p.netloc.lower())]+parts
 if not parts:parts=['root-index.html']
 elif path.endswith('/'):parts+=['index.html']
 elif kind=='page':
  name=parts[-1]
  if name=='index.php' and len(parts)==1:parts[-1]='index.html'
  elif name in ('index.html','index.htm','index.php'):parts[-1]=name.split('.')[0]+'-explicit.html'
  else:parts[-1]=re.sub(r'\.(?:php|asp|aspx|htm|html)$','',name)+'.html'
 if p.query:
  stem,ext=os.path.splitext(parts[-1]);parts[-1]=stem+'--'+sha(p.query.encode())[:10]+(ext or ('.html' if kind=='page' else ''))
 return '/'.join(parts)
def guess(url,context='link'):
 path=urlsplit(url).path.lower()
 if context=='script' or path.endswith('.js'):return 'script'
 if context!='link':return 'asset'
 if re.search(r'\.(?:png|jpe?g|gif|ico|svg|webp|bmp|css|js|pdf|zip|rar|jar|class|exe|swf|mp3|mp4|wmv|avi|mov|m4v|ogg|wav|ttf|woff2?)$',path):return 'asset'
 return 'page'
def textbody(data):
 if data[:2]==bytes([31,139]):data=gzip.decompress(data)
 return data

def parse_headers(path):
 text=path.read_text(encoding='utf-8',errors='replace') if path.exists() else ''
 stamps=re.findall(r'^memento-datetime:\s*(.+)$',text,re.M|re.I);types=re.findall(r'^Content-Type:\s*([^;\r\n]+)',text,re.M|re.I)
 stamp=email.utils.parsedate_to_datetime(stamps[-1].strip()).strftime('%Y%m%d%H%M%S') if stamps else None
 return stamp,(types[-1].strip() if types else '')
def request(url,kind,ts=TARGET,modifier='id_',force=False):
 identifier=sha((ts+modifier+url).encode());dest=CACHE/(identifier+'.bin');headers=CACHE/(identifier+'.headers');meta=CACHE/(identifier+'.json')
 if meta.exists() and not force:return json.loads(meta.read_text(encoding='utf8'))
 replay=f'https://web.archive.org/web/{ts}{modifier}/'+quote(url,safe=':/?=&%+@!;,$()\'~*')
 p=subprocess.run([CURL,'-sS','-L','--connect-timeout','6','--max-time','22','--max-filesize','24900000','-D',str(headers),'-o',str(dest),'-w','%{http_code}\n%{url_effective}',replay],capture_output=True,text=True)
 lines=p.stdout.splitlines();status=lines[0] if lines else '000';effective=lines[1] if len(lines)>1 else replay;actual,mime=parse_headers(headers)
 result={'requested_wayback_url':replay,'requested_timestamp':ts,'http_status':status,'resolved_wayback_url':effective,'actual_timestamp':actual,'content_type':mime,'curl_exit_code':p.returncode,'error':p.stderr.strip()}
 if p.returncode==0 and status=='200' and actual and dest.exists():
  data=textbody(dest.read_bytes());head=data[:700].lstrip().lower();lookshtml=bool(re.search(br'<(?:!doctype\s+html|html|head|body|title)\b',head))
  effective_original=re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z]+_)?/','',effective)
  wrongtarget=key(normal(effective_original) or url)!=key(url)
  if kind!='page' and ('html' in mime or lookshtml):result['error']='HTML fallback instead of requested asset'
  elif kind=='page' and not ('html' in mime or lookshtml):result['error']='Non-HTML response for page'
  elif kind=='page' and wrongtarget:result['error']='Archive redirected to a different original page; not treated as recovered target'
  else:
   result.update(status='saved',source_file=str(dest),bytes=len(data),sha256=sha(data),transport_sha256=sha(dest.read_bytes()))
 result.setdefault('status','unavailable');meta.write_text(json.dumps(result,indent=2),encoding='utf8');return result

# Sources from the earlier recovery can supplement unavailable nearest replays.
fallbacks=collections.defaultdict(list)
old=(args.fallback_archive or ROOT/'docs/assets/media/quinndamerell-homepage-2012').resolve()
if (old/'manifest.json').exists():
 for r in json.loads((old/'manifest.json').read_text(encoding='utf8'))['files']:
  if r.get('status')=='saved' and r.get('actual_timestamp') and r.get('raw_path') and (old/r['raw_path']).exists():
   source=old/r['raw_path'];fallbacks[key(normal(r['original_url']))].append({**r,'source_file':str(source),'reused_from_archive':'quinndamerell-homepage-2012'})
if (old/'history/manifest.json').exists():
 for r in json.loads((old/'history/manifest.json').read_text(encoding='utf8'))['items']:
  fallbacks[key(normal(r['original']))].append({'original_url':normal(r['original']),'actual_timestamp':r['timestamp'],'content_type':'text/html','source_file':str(old/'history'/r['source']),'sha256':r['sha256_original_html'],'reused_from_archive':'quinndamerell-homepage-2012/history','resolved_wayback_url':r['wayback'].replace('/'+r['timestamp']+'/', '/'+r['timestamp']+'id_/')})
# Exact bootstrap fetched and verified before crawling.
if (TEMP/'home.raw').exists():
 stamp,mime=parse_headers(TEMP/'home.headers')
 if stamp==TARGET:fallbacks[key(HOME)].insert(0,{'original_url':HOME,'actual_timestamp':stamp,'content_type':mime,'source_file':str(TEMP/'home.raw'),'resolved_wayback_url':f'https://web.archive.org/web/{TARGET}id_/{HOME}','bootstrap_exact_fetch':True})
for items in fallbacks.values():items.sort(key=lambda r:abs((datetime.datetime.strptime(r['actual_timestamp'],'%Y%m%d%H%M%S')-targetdt).total_seconds()))

CDX=[]
for p in [TEMP/'cdx.json',old/'history/cdx-inventory.json']:
 if not p.exists():continue
 try:
  data=json.loads(p.read_text(encoding='utf8'));cols=data[0]
  CDX.extend(dict(zip(cols,row)) for row in data[1:])
 except Exception:pass

def fetch(task):
 url,kind=task;attempts=[];result=None
 if url==HOME and any(x.get('bootstrap_exact_fetch') for x in fallbacks[key(url)]):
  chosen=next(x for x in fallbacks[key(url)] if x.get('bootstrap_exact_fetch'));result={**chosen,'status':'saved','http_status':'200'};attempts=[{'requested_wayback_url':chosen['resolved_wayback_url'],'status':'saved','actual_timestamp':TARGET,'method':'Exact homepage bootstrap fetch'}]
 else:
  got=request(url,kind);attempts.append(got)
  if got['status']=='saved':result=got
  if not result:
   # Reuse verified bytes only after the requested date was attempted.
   prior=fallbacks.get(key(url),[])
   if prior:
    chosen=prior[0];result={**chosen,'status':'saved','http_status':'200','restoration_note':'Requested target-date replay failed; reused previously recovered raw bytes with exact capture provenance.'}
   else:
    choices=sorted([r for r in CDX if key(normal(r['original']))==key(url)],key=lambda r:abs((datetime.datetime.strptime(r['timestamp'],'%Y%m%d%H%M%S')-targetdt).total_seconds()))
    if choices:
     chosen=choices[0];got=request(normal(chosen['original']),kind,chosen['timestamp']);attempts.append(got)
     if got['status']=='saved':result=got
    if not result:
     got=request(url,kind,TARGET,'im_' if re.search(r'\.(png|jpe?g|gif|ico|bmp|webp)$',urlsplit(url).path,re.I) else 'id_');attempts.append(got)
     if got['status']=='saved':result=got
 if not result:result={'status':'unavailable','reason':attempts[-1].get('error') or ('HTTP '+attempts[-1].get('http_status','000'))}
 record={**result,'original_url':url,'kind':kind,'requested_timestamp':TARGET,'requested_wayback_url':f'https://web.archive.org/web/{TARGET}id_/{url}','attempts':attempts,'local_path':local(url,kind)}
 if record['status']=='saved':
  body=textbody(Path(record['source_file']).read_bytes());record.update(bytes=len(body),sha256=sha(body));record['raw_path']='raw/'+record['local_path']+('.txt' if kind in ('page','script') or any(t in record.get('content_type','') for t in ('text/','javascript','json','xml','svg')) else '')
  dest=OUT/record['raw_path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body);record['capture_offset_days']=round((datetime.datetime.strptime(record['actual_timestamp'],'%Y%m%d%H%M%S')-targetdt).total_seconds()/86400,3);record['supplemental_capture']=abs(record['capture_offset_days'])>366
 print(record['status'],record.get('actual_timestamp',''),url,flush=True)
 return record

def refs(r):
 if r['status']!='saved':return []
 body=(OUT/r['raw_path']).read_bytes();text=body.decode('utf-8',errors='replace');base=r['original_url'];out=[]
 def add(value,context='link'):
  u=normal(value,base)
  if not u:return
  if value in ('none','url('):return
  if not same(u) and (context=='link' or 'youtube.com' in u):EXTERNAL.add(u);return
  if any(x in u.lower() for x in ['google-analytics.com/','googletagmanager.com/','facebook.com/plugins/']):IGNORED.append({'url':u,'reason':'Tracking or third-party widget intentionally excluded'});return
  out.append((u,guess(u,context)))
 if r['kind']=='page':
  soup=BeautifulSoup(body,'html.parser')
  for tag in soup.find_all(True):
   if tag.get('href'):add(tag['href'],'link' if tag.name=='a' else 'asset')
   for attr in ['src','poster','background','data']:
    if tag.get(attr):add(tag[attr],'script' if tag.name=='script' else 'asset')
   if tag.get('srcset'):
    for entry in tag['srcset'].split(','):add(entry.strip().split()[0],'asset')
   if tag.get('style'):
    for value in CSSURL.findall(tag['style']):add(value,'asset')
   for attr in ['onclick','onmouseover','onmouseout']:
    if tag.get(attr):
     for value in NAVJS.findall(tag[attr]):add(value)
   if tag.name=='param' and tag.get('name','').lower() in ('movie','src') and tag.get('value'):add(tag['value'],'asset')
  for tag in soup.find_all('style'):
   for value in CSSURL.findall(tag.get_text())+CSSIMPORT.findall(tag.get_text()):add(value,'asset')
  for tag in soup.find_all('script'):
   script=tag.get_text()
   for value in SCRIPTURL.findall(script):add(value,'asset')
   # AC_FL_RunContent argument pairs refer to Flash movies.
   for value in re.findall(r'[\'"]movie[\'"]\s*,\s*[\'"]([^\'\"]+)',script):add(value if value.lower().endswith('.swf') else value+'.swf','asset')
 elif 'css' in r.get('content_type',''):
  for value in CSSURL.findall(text)+CSSIMPORT.findall(text):add(value,'asset')
 elif r['kind']=='script':
  # Preserve original scripts inert; inventory static image references without executing them.
  for value in SCRIPTURL.findall(text):add(value,'asset')
 return out

def crawl():
 OUT.mkdir(parents=True,exist_ok=True);records={};pending=[(HOME,'page')];queued={key(HOME)};wave=0
 if (TEMP/'crawl-state.json').exists() or (OUT/'manifest.json').exists():
  if (TEMP/'crawl-state.json').exists():oldstate=json.loads((TEMP/'crawl-state.json').read_text(encoding='utf8'))
  else:
   previous=json.loads((OUT/'manifest.json').read_text(encoding='utf8'));oldstate={'records':previous['files']}
  records={key(r['original_url']):r for r in oldstate['records']};queued=set(records);pending=[]
  for r in records.values():
   for u,k in refs(r):
    if key(u) not in queued:queued.add(key(u));pending.append((u,k))
 while pending:
  wave+=1;batch=pending;pending=[];print('WAVE',wave,'REQUESTS',len(batch),flush=True)
  with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,args.workers)) as pool:
   for r in pool.map(fetch,batch):records[key(r['original_url'])]=r
  for u,k in batch:
   for nxt,kind in refs(records[key(u)]):
    if key(nxt) not in queued:queued.add(key(nxt));pending.append((nxt,kind))
  (TEMP/'crawl-state.json').write_text(json.dumps({'records':list(records.values()),'external_links':sorted(EXTERNAL),'excluded':IGNORED,'frontier':pending},indent=2),encoding='utf8')
 return records

if __name__=='__main__':
 records=crawl();print('CRAWL_COMPLETE',len(records),'saved',sum(r['status']=='saved' for r in records.values()),flush=True)
