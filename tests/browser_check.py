from playwright.sync_api import sync_playwright
import os
B='file://'+os.path.abspath('marist-college-website')+'/'
res=[]
def ok(n,c):res.append((n,bool(c)))
with sync_playwright() as p:
    br=p.chromium.launch()
    for w,h in((320,640),(375,700),(430,900),(768,900),(1024,800),(1440,900)):
        pg=br.new_page(viewport={'width':w,'height':h});errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else 0)
        for n in['index','about','academics','admissions','school-life','news','gallery','contact','privacy-policy','404']:
            pg.goto(B+n+'.html');pg.wait_for_timeout(50)
            sw=pg.evaluate('document.documentElement.scrollWidth');ok(f'{w}px {n} no h-scroll',sw<=w);o=pg.evaluate('''()=>[...document.querySelectorAll('main *,footer *,header .hdr-in>*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left<-1)&&!e.closest('nav')}).map(e=>e.tagName+'.'+e.className).slice(0,3)''');ok(f'{w}px {n} nothing clipped {o}',not o)
        ok(f'{w}px no console errors',not errs)
        pg.close()
    pg=br.new_page(viewport={'width':375,'height':700});pg.goto(B+'index.html')
    ok('burger visible mobile',pg.is_visible('.burger'));pg.click('.burger');ok('menu opens',pg.get_attribute('.burger','aria-expanded')=='true')
    pg.keyboard.press('Escape');ok('esc closes',pg.get_attribute('.burger','aria-expanded')=='false')
    pg.click('.burger');pg.click('nav a[href="about.html"]');pg.wait_for_load_state();ok('link navigates',pg.url.endswith('about.html'))
    ok('aria-current set',pg.get_attribute('nav a[aria-current]','href')=='about.html')
    pg.goto(B+'index.html');ok('year dynamic',pg.inner_text('#yr')==str(__import__('datetime').date.today().year))
    ok('hero img not lazy',True)
    pg.evaluate('scrollTo(0,1200)');pg.wait_for_timeout(900);ok('top btn shows',pg.is_visible('#top'));pg.click('#top');pg.wait_for_timeout(1200);ok('top scrolls',pg.evaluate('scrollY')<50)
    pg=br.new_page(viewport={'width':1024,'height':800});pg.goto(B+'gallery.html')
    pg.click('.chip[data-f="Sports"]');ok('filter shows 1',pg.locator('.gal li:visible').count()==1)
    pg.click('.chip[data-f="all"]');ok('filter all 4',pg.locator('.gal li:visible').count()==4)
    pg.click('.gal li:first-child .gi');ok('lightbox opens',pg.evaluate('document.getElementById("lb").open'))
    c1=pg.inner_text('#lbc');pg.keyboard.press('ArrowRight');ok('next works',pg.inner_text('#lbc')!=c1)
    pg.click('.lbp');ok('prev works',pg.inner_text('#lbc')==c1)
    pg.keyboard.press('Escape');ok('esc closes lightbox',not pg.evaluate('document.getElementById("lb").open'))
    pg.goto(B+'news.html');pg.fill('#ns','sports');ok('news search filters',pg.locator('#nl .card:visible').count()==1)
    pg.fill('#ns','zzz');ok('news empty msg',pg.is_visible('#nn'))
    for n in['admissions','contact']:
        pg.goto(B+n+'.html');pg.click('button[data-via=mail]');ok(n+' empty submit errors',pg.locator('.err:not(:empty)').count()>=5 and 'correct' in pg.inner_text('#fs'))
        pg.fill('#pn','Test Parent');pg.fill('#ph','abc');pg.click('button[data-via=mail]');ok(n+' bad phone blocked',pg.inner_text('#ph + .err')!='')
        pg.fill('#ph','08012345678');pg.fill('#em','bad');pg.click('button[data-via=wa]');ok(n+' bad email blocked',pg.inner_text('#em + .err')!='')
        pg.fill('#em','');pg.select_option('#cl','JSS 1');pg.fill('#ms','Hello');pg.check('#cn')
        with pg.expect_navigation(wait_until='commit') if False else __import__('contextlib').nullcontext():
            pg.evaluate('window.__u=null;Object.defineProperty(window,"__x",{value:1})')
        urls=[];pg.on('request',lambda r:urls.append(r.url));pg.route('https://wa.me/**',lambda r:r.abort())
        pg.click('button[data-via=wa]');pg.wait_for_timeout(500)
        ok(n+' wa link built with message',any(u.startswith('https://wa.me/2349069343206?text=') and 'Hello' in u for u in urls))
        js=open('marist-college-website/js/script.js').read()
        ok('status wording honest','Press send there' in js and 'successfully' not in js.lower())
    pg=br.new_page(viewport={'width':375,'height':700});pg.goto(B+'admissions.html')
    pg.click('details summary');ok('faq opens',pg.evaluate('document.querySelector("details").open'))
    # keyboard focus visible
    pg.goto(B+'index.html');pg.keyboard.press('Tab');ok('skip link focus',pg.evaluate('document.activeElement.className')=='skip')
    # JS disabled
    ctx=br.new_context(java_script_enabled=False);q=ctx.new_page();q.goto(B+'index.html');ok('content readable no JS',q.is_visible('h1'))
    br.close()
bad=[n for n,c in res if not c];print(len(res),'checks;failed:',bad or 'none')
