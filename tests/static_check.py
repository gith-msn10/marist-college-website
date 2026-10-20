import os,re,sys,glob,html.parser as hp
R='marist-college-website';errs=[];warn=[]
pages=sorted(glob.glob(R+'/*.html'))
class P(hp.HTMLParser):
    def __init__(s):super().__init__();s.ids=[];s.links=[];s.stack=[];s.imgs=[];s.h=[];s.lab=[];s.forid=[];s.title=0;s.t='';s.meta=set();s.inputs=[];s.btn=[];s.cur=None
    def handle_starttag(s,t,a):
        a=dict(a)
        if t not in('meta','link','img','input','br','hr','source'):s.stack.append(t)
        if 'id' in a:s.ids.append(a['id'])
        if t in('a','link','script','img') :
            for k in('href','src'):
                if k in a:s.links.append((t,a[k]))
        if t=='img':s.imgs.append(a)
        if re.fullmatch('h[1-6]',t):s.h.append(int(t[1]))
        if t=='meta':s.meta.add(a.get('name') or a.get('property'))
        if t=='label' and 'for' in a:s.forid.append(a['for'])
        if t in('input','select','textarea'):s.inputs.append(a)
        if t=='title':s.title=1
        if t=='button':s.cur=a;s.bt=''
        if t=='a' and a.get('href')=='#':errs.append('href=#')
    def handle_endtag(s,t):
        if t=='title':s.title=0
        if t=='button' and s.cur is not None:
            if not (s.bt.strip() or s.cur.get('aria-label') or s.cur.get('data-full')):errs.append('unnamed button')
            s.cur=None
        if s.stack and s.stack[-1]==t:s.stack.pop()
        elif t in s.stack:errs.append(f'mismatched </{t}>');
    def handle_data(s,d):
        if s.title:s.t+=d
        if s.cur is not None:s.bt+=d
titles={}
for p in pages:
    n=os.path.basename(p);x=open(p,encoding='utf-8').read();q=P();q.feed(x)
    if q.stack:errs.append(f'{n}: unclosed {q.stack}')
    d=[i for i in set(q.ids) if q.ids.count(i)>1]
    if d:errs.append(f'{n}: dup ids {d}')
    if q.h.count(1)!=1:errs.append(f'{n}: h1 count {q.h.count(1)}')
    for a,b in zip(q.h,q.h[1:]):
        if b-a>1:warn.append(f'{n}: heading jump h{a}->h{b}')
    for i in q.imgs:
        for k in('alt','width','height'):
            if k not in i:errs.append(f'{n}: img missing {k} {i.get("src")}')
    for need in('description','og:title','og:image','og:url'):
        if need not in q.meta:errs.append(f'{n}: meta {need} missing')
    titles.setdefault(q.t,[]).append(n)
    for i in q.inputs:
        if i.get('type')!='submit' and i.get('id') and i['id'] not in q.forid:errs.append(f'{n}: input {i["id"]} lacks label')
    for t,l in q.links:
        if re.match(r'(https?:|mailto:|tel:|#|data:)',l):
            if l.startswith('#') and len(l)>1 and l[1:] not in q.ids:errs.append(f'{n}: broken anchor {l}')
            continue
        f=os.path.join(R,l.split('#')[0].split('?')[0])
        if not os.path.exists(f):errs.append(f'{n}: broken {t} {l}')
    for m in re.findall(r'srcset="([^"]+)"',x):
        for u in [c.strip().split()[0] for c in m.split(',')]:
            if not os.path.exists(os.path.join(R,u)):errs.append(f'{n}: srcset missing {u}')
    if 'deplaymaker19@gmail.com' not in x:errs.append(f'{n}: email missing')
    if 'tel:+2349069343206' not in x:errs.append(f'{n}: tel missing')
    if not re.search(r'<footer',x) or 'id="yr"' not in x:errs.append(f'{n}: footer/year')
for t,v in titles.items():
    if len(v)>1:errs.append(f'dup title {v}')
css=open(R+'/css/style.css').read()
for u in re.findall(r'url\(([^)]+)\)',css):
    if not os.path.exists(os.path.join(R,'css',u)):errs.append('css missing '+u)
if css.count('{')!=css.count('}'):errs.append('css braces')
sm=open(R+'/sitemap.xml').read()
for p in pages:
    n=os.path.basename(p)
    if n not in('404.html',) and n not in sm:errs.append('sitemap lacks '+n)
print('pages',len(pages));print('ERRORS',errs or 'none');print('WARN',warn or 'none')
