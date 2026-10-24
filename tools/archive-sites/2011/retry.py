from mirror import *
if (TEMP/'crawl-state.json').exists():state=json.loads((TEMP/'crawl-state.json').read_text(encoding='utf8'))
else:
 previous=json.loads((OUT/'manifest.json').read_text(encoding='utf8'));state={'records':previous['files'],'external_links':previous.get('external_links',[]),'excluded':previous.get('excluded',[])}
rs=state['records'];out=[]
for r in rs:
 u=r['original_url']
 if urlsplit(u).path.endswith(('/none','/url(')):
  state.setdefault('excluded',[]).append({'url':u,'reason':'Rejected false URL parsed from an inline JavaScript CSS assignment.'});continue
 if 'youtube.com/v/' in u:
  state.setdefault('excluded',[]).append({'url':u,'reason':'External Flash video player. Original YouTube link preserved; external websites are outside the mirror scope.'});continue
 out.append(r)
state['records']=out
(TEMP/'crawl-state.json').write_text(json.dumps(state,indent=2),encoding='utf8')

def retry(r):
 if r['status']=='saved':return r
 url=r['original_url'];kind=r['kind'];prior=fallbacks.get(key(url),[])
 if prior:
  got=prior[0].copy();got['status']='saved';got['restoration_note']='Reused verified source bytes from simultaneous 2012 recovery, after requested January 2011 replay failed.'
 else:
  ts=args.alternate_timestamp or TARGET
  got=request(url,kind,ts,'im_' if re.search(r'\.(png|jpe?g|gif|ico|bmp|webp)$',urlsplit(url).path,re.I) else 'id_',force=True)
 r['attempts'].append({**got,'recovery_pass':'Final bounded retry after original date replay and applicable modifier/capture attempts.'})
 if got['status']=='saved':
  r.update(got);r['requested_timestamp']=TARGET;r['requested_wayback_url']=f'https://web.archive.org/web/{TARGET}id_/{url}'
  body=textbody(Path(got['source_file']).read_bytes());r.update(bytes=len(body),sha256=sha(body));r['raw_path']='raw/'+r['local_path']+('.txt' if kind in ('page','script') or any(t in r.get('content_type','') for t in ('text/','javascript','json','xml','svg')) else '')
  dest=OUT/r['raw_path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body);r['capture_offset_days']=round((datetime.datetime.strptime(r['actual_timestamp'],'%Y%m%d%H%M%S')-targetdt).total_seconds()/86400,3);r['supplemental_capture']=abs(r['capture_offset_days'])>366;r.pop('reason',None)
 print('RETRY',r['status'],url,flush=True)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,args.workers)) as pool:
 for i,r in enumerate(pool.map(retry,out)):
  state['records'][i]=r
  (TEMP/'crawl-state.json').write_text(json.dumps(state,indent=2),encoding='utf8')
print('RETRY_COMPLETE',sum(r['status']=='saved' for r in out),'/',len(out),flush=True)
