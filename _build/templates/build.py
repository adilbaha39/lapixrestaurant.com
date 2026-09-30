#!/usr/bin/env python3
"""Static multilingual build for La Paix Restaurant (fr at root, /en/, /ar/).
Usage: python3 build.py [output_dir]   (default: parent folder of this script)"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(HERE)
DOMAIN = 'https://lapixrestaurant.com'
MAPS = 'https://maps.app.goo.gl/Wiap6Zg1k6W64BJZ8'
FB = 'https://www.facebook.com/imsouanelapaix'
PHONE_TXT, PHONE_TEL = '+212 6 36 74 56 93', '+212636745693'
OG_IMAGE = DOMAIN + '/images/hiro1.jpg'   # social preview image (home hero)
LANGS = ['fr', 'en', 'ar']
LOCALE = {'fr': 'fr_FR', 'en': 'en_US', 'ar': 'ar_AR'}
PAGES = {  # key: (file name, template, schema type)
    'index': ('index.html', 'index.html', 'WebPage'),
    'carte': ('la-paix-carte.html', 'la-paix-carte.html', 'WebPage'),
    'experience': ('la-paix-experience.html', 'la-paix-experience.html', 'WebPage'),
    'contact': ('la-paix-contact.html', 'la-paix-contact.html', 'ContactPage'),
}
TR = json.load(open(os.path.join(HERE, 'translations.json'), encoding='utf-8'))
MENU = json.load(open(os.path.join(HERE, 'menu.json'), encoding='utf-8'))['categories']
IMG = json.load(open(os.path.join(HERE, 'images.json'), encoding='utf-8'))
NEUTRAL_ALT = {'fr': 'Restaurant La Paix à Imsouane', 'en': 'La Paix Restaurant in Imsouane', 'ar': 'مطعم لا بي في إمسوان'}
CAT_ICON = {
 'couscous': '<path d="M3 12h18a9 9 0 01-9 9 9 9 0 01-9-9z"/><path d="M8 8V5M12 8V4M16 8V5"/>',
 'tagines': '<path d="M4 15c0 3 3.5 5 8 5s8-2 8-5"/><ellipse cx="12" cy="8" rx="8" ry="4"/><path d="M12 4V2"/>',
 'grills': '<path d="M6 21c4-6 8-6 12 0M6 3c4 6 8 6 12 0"/>',
 'boissons': '<path d="M5 8h12v6a5 5 0 01-5 5h-2a5 5 0 01-5-5V8zM17 10h2a2 2 0 010 4h-2M8 3v2M12 3v2"/>',
 'msemen': '<rect x="5" y="6" width="14" height="12" rx="2"/><path d="M5 12h14M9 6v12M15 6v12"/>',
 'salades': '<path d="M12 2C7 6 5 10 5 13a7 7 0 0014 0c0-3-2-7-7-11z"/>',
 'pates': '<path d="M4 4c4 4 4 12 0 16M20 4c-4 4-4 12 0 16M8 12h8"/>',
 'soupes': '<path d="M3 13h18a9 9 0 01-9 8 9 9 0 01-9-8z"/><path d="M12 3v7"/><circle cx="12" cy="3" r="1.3"/>',
 'sandwichs': '<path d="M3 10c1-3 4-5 9-5s8 2 9 5M2 10h20M4 10v3a2 2 0 002 2h12a2 2 0 002-2v-3"/>',
 'omelettes': '<circle cx="12" cy="12" r="9"/><path d="M8 12a4 4 0 108 0"/>',
}
TEAL_CATS = {'tagines', 'msemen', 'soupes'}
WIDE_CATS = {'boissons'}

def imgsrc(lang, fname):
    return ('' if lang == 'fr' else '../') + 'images/' + fname

UI = {
 'fr': dict(skip='Aller au contenu principal', menu='Ouvrir le menu', close='Fermer le menu', lang='Choisir la langue',
            catnav='Catégories de la carte', og_alt="Restaurant La Paix à Imsouane, terrasse face à l'océan",
            miss='Merci de choisir une date et une heure.', past='Vous ne pouvez pas choisir une date ou une heure déjà passée.',
            wa='Bonjour La Paix, je souhaite réserver une table pour le {date} à {time} ({guests}).'),
 'en': dict(skip='Skip to main content', menu='Open menu', close='Close menu', lang='Choose language',
            catnav='Menu categories', og_alt='La Paix Restaurant in Imsouane, terrace facing the ocean',
            miss='Please choose a date and time.', past='You cannot choose a past date or time.',
            wa='Hello La Paix, I would like to book a table for {date} at {time} ({guests}).'),
 'ar': dict(skip='انتقل إلى المحتوى الرئيسي', menu='فتح القائمة', close='إغلاق القائمة', lang='اختيار اللغة',
            catnav='أقسام القائمة', og_alt='مطعم لا بي في إمسوان، تراس مطل على المحيط',
            miss='يرجى اختيار تاريخ ووقت.', past='لا يمكن اختيار تاريخ أو وقت في الماضي.',
            wa='مرحبا لا بي، أرغب في حجز طاولة بتاريخ {date} على الساعة {time} ({guests}).'),
}
LANG_NAME = {'fr': 'Français', 'en': 'English', 'ar': 'العربية'}

ALT = {
 'Tajine aux légumes': ('Vegetable tagine', 'طاجين الخضر'), 'Poisson grillé': ('Grilled fish', 'سمك مشوي'),
 'Couscous': ('Couscous', 'كسكس'), 'Des chefs expérimentés': ('Experienced chefs', 'طهاة ذوو خبرة'),
 'Produits frais': ('Fresh ingredients', 'منتجات طازجة'), 'Cadre exceptionnel': ('Exceptional setting', 'إطار استثنائي'),
 'Recettes traditionnelles': ('Traditional recipes', 'وصفات تقليدية'), "Côte d'Imsouane": ('Imsouane coastline', 'ساحل إمسوان'),
 'Ambiance terrasse': ('Terrace atmosphere', 'أجواء التراس'), 'Fruits de mer': ('Seafood', 'مأكولات بحرية'),
 "Vue sur l'océan": ('Ocean view', 'إطلالة على المحيط'), 'Localisation Imsouane': ('Imsouane location', 'موقع إمسوان'),
 "Terrasse face à l'océan": ('Terrace facing the ocean', 'تراس مطل على المحيط'),
 'Arriver à La Paix': ('Arriving at La Paix', 'الوصول إلى لا بي'), "S'installer": ('Settling in', 'الجلوس'),
 'Déguster': ('Tasting', 'التذوق'), 'Profiter': ('Enjoying', 'الاستمتاع'), 'Tagines': ('Tagines', 'طواجن'),
 'Poissons': ('Fish', 'أسماك'), 'Grillades': ('Grills', 'مشاوي'), "Groupe d'amis": ('Group of friends', 'مجموعة أصدقاء'),
 'Entrée La Paix': ('La Paix entrance', 'مدخل لا بي'), 'Carte Imsouane': ('Map of Imsouane', 'خريطة إمسوان'),
 "Table face à l'océan": ('Table facing the ocean', 'طاولة مطلة على المحيط'), 'Détail plante': ('Plant detail', 'نبتة'),
 'Façade La Paix': ('La Paix facade', 'واجهة لا بي'),
 'Entrée du restaurant La Paix': ('La Paix restaurant entrance', 'مدخل مطعم لا بي'), 'Terrasse': ('Terrace', 'التراس'),
 'Amis à table': ('Friends at the table', 'أصدقاء على الطاولة'), 'Tajine': ('Tagine', 'طاجين'),
 'Msemen': ('Msemen', 'مسمن'),
}
HERO = {'index': (1600, 900), 'carte': (1600, 600), 'experience': (1600, 700), 'contact': (1600, 600)}
STICKY_CSS = {
 'index': '', 'experience': '',
 'carte': 'body{padding-top:96px;}\n  @media(max-width:480px){body{padding-top:84px;}}',
 'contact': 'body{padding-top:96px;}\n  @media(max-width:480px){body{padding-top:84px;}}',
}
HERO_CSS = {
 'index': """.hero{position:relative; min-height:640px; display:flex; align-items:flex-end; padding-top:150px; overflow:hidden;}
  .hero::before{background:linear-gradient(to bottom, rgba(10,25,28,.35), rgba(10,25,28,.55) 60%, rgba(10,25,28,.15));}""",
 'experience': """.hero{position:relative; min-height:400px; display:flex; align-items:center; padding-top:110px; overflow:hidden;}
  .hero::before{background:linear-gradient(to right, rgba(9,30,33,.85) 10%, rgba(9,30,33,.5) 45%, rgba(9,30,33,.05) 75%);}
  html[dir="rtl"] .hero::before{background:linear-gradient(to left, rgba(9,30,33,.85) 10%, rgba(9,30,33,.5) 45%, rgba(9,30,33,.05) 75%);}""",
 'carte': """.hero{position:relative; min-height:340px; display:flex; align-items:center; overflow:hidden;}
  .hero::before{background:linear-gradient(to right, rgba(9,30,33,.82) 15%, rgba(9,30,33,.4) 50%, rgba(9,30,33,.1) 80%);}
  html[dir="rtl"] .hero::before{background:linear-gradient(to left, rgba(9,30,33,.82) 15%, rgba(9,30,33,.4) 50%, rgba(9,30,33,.1) 80%);}""",
 'contact': """.hero{position:relative; min-height:320px; display:flex; align-items:center; overflow:hidden;}
  .hero::before{background:linear-gradient(to right, rgba(9,30,33,.82) 15%, rgba(9,30,33,.4) 45%, rgba(9,30,33,.05) 75%);}
  html[dir="rtl"] .hero::before{background:linear-gradient(to left, rgba(9,30,33,.82) 15%, rgba(9,30,33,.4) 45%, rgba(9,30,33,.05) 75%);}""",
}

def path_of(lang, page):
    f = PAGES[page][0]
    tail = '' if page == 'index' else f
    return '/' + tail if lang == 'fr' else f'/{lang}/{tail}'

def url_of(lang, page):
    return DOMAIN + path_of(lang, page)

def rel_link(frm, to, page):
    tail = '' if page == 'index' else PAGES[page][0]
    if frm == to:
        return tail or './'
    if frm == 'fr':
        return f'{to}/{tail}'
    if to == 'fr':
        return '../' + tail
    return f'../{to}/{tail}'

def head_block(lang, page):
    t = TR[page][lang]
    title, desc, kw = t['meta_title'], t['meta_desc'], t['meta_keywords']
    esc = lambda s: s.replace('&', '&amp;').replace('"', '&quot;')
    url = url_of(lang, page)
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{url_of(l, page)}">\n' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url_of("fr", page)}">\n'
    locs = ''.join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">\n' for l in LANGS if l != lang)
    home_desc = TR['index'][lang]['meta_desc']
    graph = {
     '@context': 'https://schema.org',
     '@graph': [
      {'@type': 'Restaurant', '@id': DOMAIN + '/#restaurant', 'name': 'La Paix Restaurant', 'url': DOMAIN + '/',
       'description': home_desc, 'image': OG_IMAGE, 'telephone': PHONE_TEL,
       'servesCuisine': ['Moroccan', 'Seafood'], 'acceptsReservations': True,
       'address': {'@type': 'PostalAddress', 'addressLocality': 'Imsouane', 'addressCountry': 'MA'},
       'hasMap': MAPS, 'hasMenu': url_of(lang, 'carte'), 'sameAs': [FB]},
      {'@type': 'WebSite', '@id': DOMAIN + '/#website', 'url': DOMAIN + '/', 'name': 'La Paix Restaurant',
       'inLanguage': LANGS, 'publisher': {'@id': DOMAIN + '/#restaurant'}},
      {'@type': PAGES[page][2], '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc,
       'inLanguage': lang, 'isPartOf': {'@id': DOMAIN + '/#website'}, 'about': {'@id': DOMAIN + '/#restaurant'}},
     ]}
    if page == 'carte':
        graph['@graph'].append({'@type': 'Menu', '@id': url + '#menu', 'name': title, 'url': url, 'inLanguage': lang,
          'hasMenuSection': [{'@type': 'MenuSection', 'name': c['name'][lang], 'hasMenuItem': [
            {'@type': 'MenuItem', 'name': it['n'][lang], 'offers': {'@type': 'Offer', 'price': str(it['p']), 'priceCurrency': 'MAD'}}
            for it in c['items']]} for c in MENU]})
    ld = json.dumps(graph, ensure_ascii=False, indent=2)
    return f'''<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(kw)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#173f42">
<link rel="canonical" href="{url}">
{alts}<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23173f42'/%3E%3Cpath d='M8 44 L22 24 L31 36 L41 16 L58 44' fill='none' stroke='white' stroke-width='3'/%3E%3C/svg%3E">
<!-- Open Graph / Facebook / WhatsApp -->
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:alt" content="{esc(UI[lang]['og_alt'])}">
<meta property="og:locale" content="{LOCALE[lang]}">
{locs}<meta property="og:site_name" content="La Paix Restaurant">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<!-- Analytics: paste the Google Analytics 4 snippet here once the measurement ID exists (clicks marked data-track are sent automatically when gtag is present) -->
<script type="application/ld+json">
{ld}
</script>
'''

def lang_switch(lang, page):
    opts = ''
    for l in LANGS:
        cur = ' active" aria-current="true' if l == lang else ''
        opts += f'          <a class="lang-option{cur}" href="{rel_link(lang, l, page)}" hreflang="{l}" lang="{l}">{LANG_NAME[l]}</a>\n'
    u = UI[lang]
    return f'''<div class="lang-switch" id="langSwitch">
        <button class="lang-current" id="langBtn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="{u['lang']}">
          <span>{lang.upper()}</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="lang-menu">
{opts}        </div>
      </div>
      <button type="button" class="burger" id="burger" aria-label="{u['menu']}" aria-expanded="false"><span></span><span></span><span></span></button>'''

def script_block(lang, page):
    u = UI[lang]
    scroll = ''
    if page == 'index':
        scroll = """
  var header=document.querySelector('header');
  window.addEventListener('scroll',function(){
    if(window.scrollY>80){header.style.background='#173f42';header.style.padding='16px 0';header.style.transition='.25s ease';}
    else{header.style.background='transparent';header.style.padding='26px 0';}
  });"""
    elif page == 'experience':
        scroll = """
  var header=document.querySelector('header');
  window.addEventListener('scroll',function(){
    if(window.scrollY>60){header.style.background='#173f42';header.style.transition='.25s ease';}
    else{header.style.background='transparent';}
  });"""
    if page == 'carte':
        scroll = """
  var pills=document.querySelectorAll('.cat-pill');
  if('IntersectionObserver' in window&&pills.length){
    var byId={}; pills.forEach(function(p){byId[p.getAttribute('href').slice(1)]=p;});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting)return;
      pills.forEach(function(p){p.classList.remove('active');});
      var p=byId[e.target.id]; if(p){p.classList.add('active');p.scrollIntoView({inline:'center',block:'nearest'});}
    });},{rootMargin:'-45% 0px -50% 0px'});
    document.querySelectorAll('.cat').forEach(function(sec){io.observe(sec);});
  }"""
    form = ''
    if page == 'contact':
        cfg = json.dumps({'miss': u['miss'], 'past': u['past'], 'wa': u['wa']}, ensure_ascii=False)
        form = f"""
  var pad=function(n){{return String(n).padStart(2,'0');}};
  var now=new Date();
  document.getElementById('resDate').min=now.getFullYear()+'-'+pad(now.getMonth()+1)+'-'+pad(now.getDate());
  var CFG={cfg};
  var RESTAURANT_WHATSAPP='{PHONE_TEL.lstrip('+')}';
  document.getElementById('reserveForm').addEventListener('submit',function(e){{
    e.preventDefault();
    var date=document.getElementById('resDate').value;
    var time=document.getElementById('resTime').value;
    var guests=document.getElementById('resGuests').selectedOptions[0].textContent;
    if(!date||!time){{alert(CFG.miss);return;}}
    if(new Date(date+'T'+time).getTime()<Date.now()){{alert(CFG.past);return;}}
    var msg=CFG.wa.replace('{{date}}',date).replace('{{time}}',time).replace('{{guests}}',guests);
    document.getElementById('formMsg').style.display='block';
    if(typeof window.gtag==='function'){{window.gtag('event','booking_whatsapp');}}
    window.open('https://wa.me/'+RESTAURANT_WHATSAPP+'?text='+encodeURIComponent(msg),'_blank','noopener');
  }});"""
    return f'''<script>
(function(){{
  var burger=document.getElementById('burger'), mobileNav=null;
  function closeNav(){{
    if(!mobileNav)return;
    mobileNav.remove(); mobileNav=null;
    burger.setAttribute('aria-expanded','false'); document.body.style.overflow='';
  }}
  burger.addEventListener('click',function(){{
    if(mobileNav){{closeNav();return;}}
    mobileNav=document.createElement('div');
    mobileNav.style.cssText='position:fixed;inset:0;background:#173f42;z-index:100;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;';
    document.querySelectorAll('.main-nav a').forEach(function(src){{
      var a=document.createElement('a');
      a.href=src.getAttribute('href'); a.textContent=src.textContent;
      a.style.cssText='color:#fff;font-size:20px;letter-spacing:1px;font-weight:500;';
      a.addEventListener('click',closeNav);
      mobileNav.appendChild(a);
    }});
    var x=document.createElement('button');
    x.type='button'; x.textContent='\\u00d7'; x.setAttribute('aria-label',{json.dumps(u['close'], ensure_ascii=False)});
    x.style.cssText='position:absolute;top:18px;inset-inline-end:22px;background:none;border:0;color:#fff;font-size:38px;line-height:1;cursor:pointer;';
    x.addEventListener('click',closeNav);
    mobileNav.appendChild(x);
    document.body.appendChild(mobileNav); document.body.style.overflow='hidden';
    burger.setAttribute('aria-expanded','true'); x.focus();
  }});
  var ls=document.getElementById('langSwitch'), lb=document.getElementById('langBtn');
  lb.addEventListener('click',function(e){{e.stopPropagation();lb.setAttribute('aria-expanded',ls.classList.toggle('open'));}});
  document.addEventListener('click',function(){{ls.classList.remove('open');lb.setAttribute('aria-expanded','false');}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'){{closeNav();ls.classList.remove('open');lb.setAttribute('aria-expanded','false');}}}});{scroll}
  document.addEventListener('click',function(e){{
    var el=e.target.closest('[data-track]'); if(!el)return;
    if(typeof window.gtag==='function'){{window.gtag('event',el.getAttribute('data-track'),{{link_url:el.href||''}});}}
  }});{form}
}})();
</script>
'''

CSS_ADD = """
  /* ---- a11y / SEO additions ---- */
  img{height:auto;}
  .menu-item-name{min-width:0; overflow-wrap:anywhere;}
  .moments-note{right:0;}
  html[dir="rtl"] .moments-note{right:auto; left:0;}
  .cat-inner>*,.cta-inner>*,.lieu-split>*,.meet-split>*,.find-wrap>*,.reserve-wrap>*,.moments-wrap>*,.gout-wrap>*,.instant-section>*,.instant-grid>*,.plates-top>*,.cards-grid>*,.split>*,.experience-section .wrap>*,.footer-top>*,.form-row>*,.feature-grid>*,.follow-grid>*{min-width:0;}
  .skip-link{position:absolute; top:-100px; left:16px; z-index:200; background:#fff; color:var(--teal-dark); padding:10px 16px; border-radius:6px; font-weight:600;}
  .skip-link:focus{top:12px;}
  :focus-visible{outline:2px solid #e3a06a; outline-offset:3px;}
  button.burger{background:none; border:0; padding:0; font:inherit;}
  a.lang-option{display:block;}
  h2.eyebrow{font-family:inherit; line-height:normal;}
  html[dir="rtl"] h2.eyebrow{font-family:'Cairo',sans-serif; font-weight:600;}
  .hero-bg{position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0;}
  .hero::before{content:''; position:absolute; inset:0; z-index:1;}
  .hero > .wrap{position:relative; z-index:2;}
  .map-thumb svg{display:block; width:100%; height:auto;}
  .map-thumb a[aria-hidden]{display:block; opacity:1;}
  header{position:fixed !important; top:0; left:0; width:100%; z-index:90;}
  STICKY_RULES

  HERO_RULES
"""

import html as _html

def menu_nav(lang):
    pills = ''.join('<a class="cat-pill" href="#%s"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">%s</svg>%s</a>'
                    % (c['id'], CAT_ICON[c['id']], _html.escape(c['name'][lang], quote=False)) for c in MENU)
    return '<nav class="cat-nav" aria-label="%s"><div class="wrap"><div class="cat-scroll">%s</div></div></nav>' % (UI[lang]['catnav'], pills)

def menu_sections(lang):
    out = ''
    for i, c in enumerate(MENU):
        cls = 'cat' + (' teal' if c['id'] in TEAL_CATS else '') + (' rev' if i % 2 else '') + (' wide' if c['id'] in WIDE_CATS else '')
        name = _html.escape(c['name'][lang], quote=False)
        items = ''.join('<li><span class="menu-item-name">%s</span><span class="menu-item-price" dir="ltr">%s DH</span></li>'
                        % (_html.escape(it['n'][lang], quote=False), it['p']) for it in c['items'])
        out += f'''<section class="{cls}" id="{c['id']}" aria-labelledby="h-{c['id']}">
  <div class="wrap cat-inner">
    <div class="cat-photo"><img src="{imgsrc(lang, c['img'])}" alt="{name}" width="1200" height="900" loading="lazy" decoding="async"></div>
    <div class="cat-body">
      <h2 class="cat-title" id="h-{c['id']}"><span class="cat-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">{CAT_ICON[c['id']]}</svg></span>{name}</h2>
      <ul class="menu-list">{items}</ul>
    </div>
  </div>
</section>
'''
    return out

def transform(page, lang):
    fname, tpl, _ = PAGES[page]
    src = open(os.path.join(HERE, 'templates', tpl), encoding='utf-8').read()
    t = {**TR['experience'][lang], **TR['contact'][lang], **TR[page][lang]}
    u = UI[lang]
    if page == 'carte':
        src = src.replace('<!--MENU_NAV-->', menu_nav(lang)).replace('<!--MENU_SECTIONS-->', menu_sections(lang))

    # 1) strip old OG/JSON-LD + main script, then rebuild head/script
    src = re.sub(r'<!-- Open Graph / Facebook / WhatsApp -->.*?</script>\n', '', src, flags=re.S)
    i = src.rfind('<script>\n'); assert i > 0
    src = src[:i] + script_block(lang, page) + '</body>\n</html>\n'
    src, n = re.subn(r'<title id="pageTitle">.*?</title>\n<meta id="metaDesc"[^>]*>\n<meta id="metaKeywords"[^>]*>\n', lambda m: head_block(lang, page), src, flags=re.S)
    assert n == 1, 'head block'
    dirn = 'rtl' if lang == 'ar' else 'ltr'
    src = src.replace('<html lang="fr">', f'<html lang="{lang}" dir="{dirn}">')
    src = src.replace('&family=Cairo:wght@400;500;600;700', '') if lang != 'ar' else src.replace('&family=Poppins:wght@300;400;500;600;700', '')

    # 2) hero: real <img> (LCP friendly) instead of a CSS background; remove old CSS rules
    hero_img = '  <img class="hero-bg" src="%s" alt="%s" width="%d" height="%d" fetchpriority="high" decoding="async">\n' % (
        imgsrc(lang, IMG['hero'][page]), NEUTRAL_ALT[lang], *HERO[page])
    if page == 'index':
        src, n = re.subn(r'  \.hero\{\n.*?\n  \}\n', '  HERO_PLACEHOLDER\n', src, count=1, flags=re.S)
        src = src.replace('<section class="hero" id="accueil">\n', '<section class="hero" id="accueil">\n' + hero_img, 1)
    elif page == 'carte':
        n = 1
        src = src.replace('<section class="hero">\n', '<section class="hero">\n' + hero_img, 1)
    else:
        src, n = re.subn(r'  \.hero\{position:relative;.*?\n  html\[dir="rtl"\] \.hero\{background:[^\n]*\n', '  HERO_PLACEHOLDER\n', src, count=1, flags=re.S)
        src = src.replace('<section class="hero">\n', '<section class="hero">\n' + hero_img, 1)
    assert n == 1, 'hero css'
    src = src.replace('  HERO_PLACEHOLDER\n', '')
    css = CSS_ADD.replace('HERO_RULES', HERO_CSS[page]).replace('STICKY_RULES', STICKY_CSS[page])
    src = src.replace('</style>', css + '</style>', 1)

    # 3) headings / semantics
    src = re.sub(r'<div class="eyebrow" data-i18n="steps_eyebrow">(.*?)</div>', r'<h2 class="eyebrow" data-i18n="steps_eyebrow">\1</h2>', src)
    src = re.sub(r'\bh4\b', 'h2' if page == 'contact' else 'h3', src)
    src = re.sub(r'\bh5\b', 'h3', src)
    src = re.sub(r'<h6\b', '<p class="footer-title"', src).replace('</h6>', '</p>')
    src = src.replace('.footer-col h6{', '.footer-col .footer-title{')
    src = src.replace('<body>\n', f'<body>\n<a class="skip-link" href="#main">{u["skip"]}</a>\n', 1)
    src = src.replace('</header>\n', '</header>\n<main id="main">\n', 1)
    assert src.count('<footer') == 1
    src = src.replace('<footer', '</main>\n<footer', 1)

    # 4) header lang switcher + burger
    src, n = re.subn(r'<div class="lang-switch" id="langSwitch">.*?<div class="burger"[^>]*>.*?</div>', lambda m: lang_switch(lang, page), src, count=1, flags=re.S)
    assert n == 1, 'lang switch'

    # 5) links
    src = src.replace('href="index.html"', 'href="./"')
    src = src.replace('<a href="#" class="logo">', '<a href="./" class="logo">')
    if page == 'index':
        src = src.replace('href="#reserver"', 'href="la-paix-contact.html#reserver"')
    if page == 'experience':
        src = src.replace('<section class="section" id="reserver">', '<section class="section" id="localisation">')
    selfkey = {'experience': 'nav_experience', 'contact': 'nav_contact', 'carte': 'nav_menu'}.get(page)
    if selfkey:
        src = re.sub(r'<a href="#"((?: class="active")? data-i18n="%s")' % selfkey, r'<a href="%s"\1' % fname, src)
    src = src.replace('<a href="#" data-i18n="footer_see_map">', f'<a href="{MAPS}" target="_blank" rel="noopener" data-i18n="footer_see_map">')
    src = re.sub(r'<a href="([^"]*)" class="active"', r'<a href="\1" class="active" aria-current="page"', src)
    src = re.sub(r'target="_blank"(?! rel)', 'target="_blank" rel="noopener"', src)
    src = re.sub(r'>\+212 6 65 33 06 69<', f'><a href="tel:{PHONE_TEL}" dir="ltr" data-track="phone_click">{PHONE_TXT}</a><', src)
    src = re.sub(r'<a href="tel:\+212665330669" class="btn btn-outline-white">',
                 f'<a href="tel:{PHONE_TEL}" class="btn btn-outline-white" data-track="phone_click">', src)
    src = src.replace(f'href="{MAPS}"', f'href="{MAPS}" data-track="map_click"')
    src = src.replace('<a href="https://www.facebook.com/imsouanelapaix" target="_blank" rel="noopener">', '<a href="https://www.facebook.com/imsouanelapaix" target="_blank" rel="noopener" aria-label="Facebook" data-track="social_click">')
    src = re.sub(r'\s*<a href="#"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/>.*?</svg></a>', '', src)
    if page == 'contact':
        for k, i_ in (('date', 'resDate'), ('time', 'resTime'), ('guests', 'resGuests')):
            src = re.sub(r'<label>(<svg[^>]*>.*?</svg><span data-i18n="field_%s">)' % k, r'<label for="%s">\1' % i_, src, flags=re.S)
        src = src.replace('id="formMsg"', 'id="formMsg" role="status"')

    # 6) images: placeholders -> real files from images.json (alt: dish category for food photos, neutral for venue photos)
    def img(m):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        if 'placehold.co' not in a['src']:
            return m.group(0)
        dims = re.search(r'placehold\.co/(\d+)x(\d+)', a['src'])
        slot = re.search(r'text=([^&"]+)', a['src']).group(1)
        assert slot in IMG['slots'][page], 'no image mapped for %s / %s' % (page, slot)
        fname, _, altkey = IMG['slots'][page][slot].partition('|')
        if altkey:
            alt = altkey if lang == 'fr' else ALT[altkey][0 if lang == 'en' else 1]
        else:
            alt = NEUTRAL_ALT[lang]
        out = '<img'
        if 'class' in a: out += f' class="{a["class"]}"'
        out += f' src="{imgsrc(lang, fname)}" alt="{alt}" width="{dims.group(1)}" height="{dims.group(2)}" loading="lazy" decoding="async">'
        return out
    src = re.sub(r'<img\b([^>]*?)\s*/?>', img, src)
    src = re.sub(r"url\('https://placehold\.co/1600x700/1f5257[^']*'\)", "url('%s')" % imgsrc(lang, IMG['ocean_banner']), src)
    assert 'placehold.co' not in src, 'placeholder image left over'

    # 7) static translations
    attr = r'(?:\s+[\w-]+(?:="[^"]*")?)*'
    pat = re.compile(r'<(\w+)(' + attr + r'?)\s+data-i18n="([^"]+)"(' + attr + r')\s*>(.*?)</\1>', re.S)
    def tr(m):
        assert m.group(3) in t, 'missing key ' + m.group(3)
        return f'<{m.group(1)}{m.group(2)}{m.group(4)}>{t[m.group(3)]}</{m.group(1)}>'
    src = pat.sub(tr, src)
    assert 'data-i18n' not in src, 'leftover data-i18n'
    return src

def main():
    for lang in LANGS:
        for page in PAGES:
            out = os.path.join(OUT, '' if lang == 'fr' else lang, PAGES[page][0])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(transform(page, lang))
    # sitemap with hreflang alternates
    rows = ''
    for page in PAGES:
        for lang in LANGS:
            alts = ''.join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{url_of(l, page)}"/>\n' for l in LANGS)
            alts += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_of("fr", page)}"/>\n'
            rows += f'  <url>\n    <loc>{url_of(lang, page)}</loc>\n{alts}  </url>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + rows + '</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(page404())
    print('built into', OUT)

def page404():
    return '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>404 | La Paix Restaurant</title>
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#173f42">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Poppins:wght@400;600&family=Cairo:wght@400;700&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Poppins',sans-serif;background:#f7f1e4;color:#1c2b2e;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:32px}
  main{max-width:640px;text-align:center}
  h1{font-family:'Playfair Display',serif;font-size:72px;color:#173f42;line-height:1}
  section{margin-top:28px}
  h2{font-family:'Playfair Display',serif;font-size:22px;color:#173f42;margin-bottom:8px}
  section[dir=rtl]{font-family:'Cairo',sans-serif}
  section[dir=rtl] h2{font-family:'Cairo',sans-serif}
  p{font-size:14px;color:#5b6a6c;margin-bottom:12px}
  a{display:inline-block;background:#173f42;color:#fff;text-decoration:none;padding:12px 22px;border-radius:6px;font-weight:600;font-size:13px}
  a:focus-visible{outline:2px solid #c8703f;outline-offset:3px}
</style>
</head>
<body>
<main>
  <h1>404</h1>
  <section lang="fr"><h2>Page introuvable</h2><p>La page demandée n'existe pas ou a été déplacée.</p><a href="/">Retour à l'accueil</a></section>
  <section lang="en"><h2>Page not found</h2><p>The page you requested does not exist or has been moved.</p><a href="/en/">Back to the homepage</a></section>
  <section lang="ar" dir="rtl"><h2>الصفحة غير موجودة</h2><p>الصفحة المطلوبة غير موجودة أو تم نقلها.</p><a href="/ar/">العودة إلى الرئيسية</a></section>
</main>
</body>
</html>
'''

if __name__ == '__main__':
    main()
