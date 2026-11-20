#!/usr/bin/env python3
"""Builds the Diamant redesign pitch into ./site from ./source (crawled copy)."""
import os, re, html, time
V = str(int(time.time()))
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'source'); OUT = os.path.join(ROOT, 'site')
E = html.escape

# ---------------------------------------------------------------- data
DENTAL = [
  ('konzervativno-in-estetsko-zobozdravstvo','Konzervativno in estetsko zobozdravstvo','Širok razpon preventivnega in estetskega zobozdravstva s poudarkom na estetiki.','s-konzervativa','zobozdravstvene-storitve__konzervativno-in-estetsko-zobozdravstvo'),
  ('implantati','Implantati','Manjkajoče zobe nadomestimo z zobnimi vsadki, implantati.','s-implantati','zobozdravstvene-storitve__implantati'),
  ('all-on-4','All-on-4','Če ste ali boste v kratkem izgubili vse zobe, vam jih metoda All-on-4 povrne v enem dnevu.','s-all-on-4','zobozdravstvene-storitve__all-on-4'),
  ('beljenje-zob','Beljenje zob','Sedaj si lahko posvetlite zobe že s samo enim obiskom v naši ordinaciji.','s-beljenje','zobozdravstvene-storitve__beljenje-zob'),
  ('zobna-protetika','Zobna protetika','Snemna in fiksna protetika. CAD-CAM polnokeramične prevleke, estetske luske, delne in totalne proteze.','s-protetika','zobozdravstvene-storitve__zobna-protetika'),
  ('ortodontski-aparati','Ortodontski aparati','Snemni in fiksni neopazni ortodontski aparati.','s-ortodontija','zobozdravstvene-storitve__ortodontski-aparati'),
  ('zdravljenje-koreninskih-kanalov','Zdravljenje koreninskih kanalov','Mikroskopsko endodontsko zdravljenje koreninskih kanalov in granulomov.','s-endodontija','zobozdravstvene-storitve__zdravljenje-koreninskih-kanalov'),
  ('oralna-kirurgija','Oralna kirurgija','Oralnokirurški posegi, zdiranje zob, apikotomije.','s-kirurgija','zobozdravstvene-storitve__oralna-kirurgija'),
  ('parodontologija','Parodontologija','Zdravljenje dlesni in obzobnih tkiv.','s-parodontologija','zobozdravstvene-storitve__parodontologija'),
  ('ustna-higiena','Ustna higiena','Čiščenje zobnega kamna, peskanje in poliranje zob.','s-higiena','zobozdravstvene-storitve__ustna-higiena'),
  ('sedacija','Sedacija','Sedacija z varnim in učinkovitim sredstvom, didušikovim oksidom.','s-sedacija','zobozdravstvene-storitve__sedacija'),
  ('zobni-rentgen','Zobni rentgen CBCT in ortopan','Ortopan in CBCT 3D slikanje v Celju in Ljubljani, brez čakalnih dob.','s-rentgen','storitve-rentgena'),
]
AESTH = [
  ('glajenje-gubic-obraza','Glajenje gubic obraza','Preparati, ki učinkovito gladijo gubice in preprečujejo nastanek novih.','s-gubice','estetske-storitve__glajenje-gubic-obraza'),
  ('dermalna-polnila-filerji','Dermalna polnila','Oblikovanje ustnic in obraza z vrhunskimi švicarskimi polnili TEOSYAL.','s-filerji','estetske-storitve__dermalna-polnila-filerji'),
  ('injekcijska-lipoliza','Injekcijska lipoliza','Minimalno invazivno raztapljanje maščobnih oblog na področju podbradka.','s-lipoliza','estetske-storitve__injekcijska-lipoliza'),
]
ALL = DENTAL + AESTH

QUOTES = [
  ('Pri 50-ih se tudi na zobeh pozna starost, imela sem rjavkaste zobe, sedaj po beljenju pa so občutno svetlejši. Nisem želela belih kot WC školjka in dr. Robič je to upošteval!','Anica','Žalec'),
  ('Še nikoli si ni noben zobozdravnik vzel toliko časa zame in mi vse razložil ter tudi pokazal na monitorju. Vedno me je bilo strah zobozdravnika, zdaj pa grem brez odpora.','Alojz','Šentjur'),
  ('Vsi hvalijo, kako lepe in naravne zobe ste mi naredili! Takoj sem jih vzel za svoje, čisto nič me ne moti ali žuli, vse lahko jem brez problemov.','Rudi','Proseniško'),
  ('Vrnili ste mi nasmeh na usta. Vaš pristop je bil strokoven, topel, prijazen, skratka profesionalen.','Andreja','Sevnica'),
  ('Poseg je bil neboleč, pa tudi kasnejših zapletov ni bilo. Tako sem našla zobozdravnike, katerim zaupam vse posege.','Emilija Brišar',''),
]

DENTISTS = [
  ('t-jure','Jure Robič, dr. dent. med., MSc.','Implantologija, oralna kirurgija in All-on-4',False),
  ('t-tina','Tina Robič, dr. dent. med.','Zobozdravnica',True),
  ('t-zupan','Jurij Zupan, dr. dent. med., MSc.','Konzervativa, protetika, implantologija v Ljubljani',True),
  ('t-eva','Eva Hren Krajnc, dr. dent. med.','Konzervativa, endodontija, protetika',True),
  ('t-luka','Luka Tepeš, dr. dent. med.','Protetika, implantologija, estetsko zobozdravstvo',True),
  ('t-nina','Nina Posilovič, dr. dent. med.','Konzervativa, endodontija, protetika',True),
  ('t-alja','Alja Stubičar, dr. dent. med.','Konzervativa, endodontija, protetika',True),
  ('t-plut','Jan Plut, dr. dent. med.','Konzervativa, endodontija, implantologija',True),
]
STAFF = [
  ('p-isel','Mišel Kekec','Zobotehnik, CAD-CAM laboratorij'),('p-aljar','Alja Robič, dipl. m.s.','Direktorica'),
  ('p-zan','Žan Rimc','Dipl. ustni higienik'),('p-lea-c','Lea Cizej','Dipl. ustni higienik'),('p-aljaz','Aljaž Pajenk','Dipl. ustni higienik'),
  ('p-maja','Maja Berk','Dipl. ustni higienik, Ljubljana'),('p-larisa','Larisa Mijatović, tzn','Vodja asistentk'),('p-sandra','Sandra Lakić','Asistentka dr. Robiča'),
  ('p-tinkara','Tinkara Žerovnik','Asistentka'),('p-tjasa','Tjaša Strojanšek Korošec','Asistentka'),('p-kiara','Kiara T. Šeligo','Asistentka dr. Robiča'),
  ('p-ira','Ira Lončar','Dipl. laboratorijski zobni protetik'),('p-lea','Lea Hriberšek, tzn','Asistentka'),('p-anja','Anja Zdolšek, dipl. m.s.','Medicinska sestra'),
]
AESTH_TEAM = [('t-eva-sajovic','Eva Sajovic Kuprivec, dr. med.','Glajenje gubic obraza, dermalna polnila'),('t-tea','Tea Jedlovčnik, dr. med.','Specialistka plastične, rekonstrukcijske in estetske kirurgije'),('t-eva','Eva Hren Krajnc, dr. dent. med.','Glajenje gubic obraza, dermalna polnila')]

# ---------------------------------------------------------------- service parsing
END = ['#2 Možnost obročnega plačila','#2 Imamo izkušnje','#2 TU SMO ZA VAS','#2 Podobne storitve','Preberite še članke','#2 Posvet z našimi','#2 Posvetujte se z nami']
DROP = re.compile(r'^(Naroči se na pregled|Naročite se.*|PREBERITE VEČ|Preberi več|NAROČITE SE.*|Več o [^.]{0,40})$', re.I)
def tidy(s):
    s = re.sub(r'\s+([.,;:!?)])', r'\1', s.strip()); s = re.sub(r'\(\s+', '(', s)
    s = s.replace(' – ', ', ').replace('–', '-') if False else s
    return re.sub(r'\s{2,}', ' ', s)
def sentence(s):
    if s.isupper() and len(s) > 3: s = s[0] + s[1:].lower()
    return s
def parse(name):
    t = open(os.path.join(SRC, name + '.txt'), encoding='utf8').read().split('IMAGES:')[0]
    i = t.find('#2 Storitve rentgena'); i = t.find('#2', i + 5)
    body = t[i:]
    faq = []
    fi = body.find('#2 Pogosta vprašanja')
    if fi >= 0:
        fe = body.find('\n#2', fi + 5); fe = len(body) if fe < 0 else fe
        q = None
        for ln in body[fi:fe].split('\n')[1:]:
            ln = tidy(ln)
            if not ln: continue
            if ln.startswith('#3'): q = [ln[2:].strip(), '']; faq.append(q)
            elif q: q[1] = (q[1] + ' ' + ln).strip()
        body = body[:fi] + body[fe:]
    ends = [body.find(m) for m in END if body.find(m) > 0]
    body = body[:min(ends)] if ends else body
    blocks = []; cur = None
    for ln in body.split('\n'):
        ln = tidy(ln)
        if not ln or DROP.match(ln): continue
        if ln.startswith('#2'):
            h = ln[2:].strip()
            if not h: continue
            cur = {'h': sentence(h), 'items': []}; blocks.append(cur)
        elif cur is None: continue
        elif ln.startswith('#3'): cur['items'].append(('h3', sentence(ln[2:].strip())))
        elif ln.isupper() and len(ln) < 70: cur['items'].append(('h3', sentence(ln)))
        else: cur['items'].append(('p', ln))
    title = blocks[0]['h'] if blocks else ''
    lede = ''
    if blocks and not blocks[0]['items'] and len(blocks) > 1 and not blocks[1]['items'] and len(blocks[1]['h']) > 60:
        lede = blocks[1]['h']; blocks = blocks[2:]
    elif blocks:
        b0 = blocks[0]
        if b0['items'] and b0['items'][0][0] == 'p': lede = b0['items'][0][1]; b0['items'] = b0['items'][1:]
        b0['h'] = 'O storitvi' if b0['items'] else b0['h']
        if not b0['items']: blocks = blocks[1:]
    out = []
    for b in blocks:
        if b['h'].lower().startswith('primerjava'): continue
        if not b['items']:
            # heading-only block: lede-like statement, keep as a standalone line
            if len(b['h']) > 60 and out: out[-1]['items'].append(('p', b['h']))
            continue
        out.append(b)
    return title, lede, out, faq

def render_items(items):
    h = []; buf = []
    def flush():
        if not buf: return
        if len(buf) >= 2 and all(len(x) < 120 and not x.endswith('.') for x in buf) or all(x.startswith(('– ','- ')) for x in buf):
            h.append('<ul>' + ''.join(f'<li>{E(x.lstrip("–- ").strip())}</li>' for x in buf) + '</ul>')
        else:
            h.extend(f'<p>{E(x)}</p>' for x in buf)
        buf.clear()
    for kind, txt in items:
        if kind == 'h3': flush(); h.append(f'<h3>{E(txt)}</h3>')
        else:
            short = len(txt) < 120 and not txt.endswith(('.', ':', '!', '?'))
            if short or txt.startswith(('– ', '- ')): buf.append(txt)
            else:
                if buf and len(buf) == 1 and not buf[0].startswith(('– ','- ')): h.append(f'<h3>{E(buf[0])}</h3>'); buf.clear()
                flush(); h.append(f'<p>{E(txt)}</p>')
    flush()
    return '\n'.join(h)

# ---------------------------------------------------------------- partials
def lines(text):
    return ''.join(f'<span class="line"><span>{E(l)}</span></span>' for l in text.split('|'))

TRACK = '''<script>
(function () {
  if (!/[?&]r=/.test(location.search)) return;
  var s = document.createElement('script');
  s.async = true;
  s.referrerPolicy = 'no-referrer';
  s.setAttribute('data-landing', location.href);
  s.src = 'https://phplaravel-758037-6569212.cloudwaysapps.com/v/script.js';
  document.head.appendChild(s);
})();
</script>'''

def head(title, desc, P):
    return f'''<!doctype html>
<html lang="sl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex">
<link rel="icon" href="{P}assets/img/logo-mark.png">
<link rel="preload" href="{P}assets/fonts/avantt-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{P}assets/fonts/avantt-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}assets/css/style.css?v={V}">
{TRACK}
</head>
<body>
'''

def svc_links(lst, P):
    return ''.join(f'<li><a href="{P}storitve/{s}.html">{E(n)}</a></li>' for s, n, *_ in lst)

def nav(P, light=False, cur=''):
    c = lambda k: ' class="is-current"' if cur == k else ''
    return f'''<div class="loader" aria-hidden="true"><div class="loader__mark"><img src="{P}assets/img/logo-mark.png" alt=""></div><div class="loader__bar"><span></span></div></div>
<header class="nav{' is-light' if light else ''}">
  <a class="nav__logo" href="{P}index.html" aria-label="Zobozdravstveni center Diamant, domov">
    <img class="l-white" src="{P}assets/img/logo-white.webp" alt="Zobozdravstveni center Diamant">
    <img class="l-blue" src="{P}assets/img/logo-blue.webp" alt="">
  </a>
  <nav class="nav__links" aria-label="Glavna navigacija">
    <button data-mega aria-expanded="false"{c('storitve')}>Storitve</button>
    <a href="{P}o-nas.html"{c('o-nas')}>O nas</a>
    <a href="{P}cenik.html"{c('cenik')}>Cenik</a>
    <a href="{P}darilni-boni.html"{c('boni')}>Darilni boni</a>
    <a href="{P}kontakt.html"{c('kontakt')}>Kontakt</a>
  </nav>
  <div class="nav__right">
    <div class="nav__phone"><a href="tel:+38630202020">030 20 20 20</a><small>Celje</small></div>
    <div class="nav__phone"><a href="tel:+38671212121">071 21 21 21</a><small>Ljubljana</small></div>
    <a class="btn" href="#" data-book>Naročite se <span class="arr">→</span></a>
    <button class="burger" aria-label="Meni" aria-expanded="false"><span></span><span></span></button>
  </div>
</header>
<div class="mega" aria-label="Storitve">
  <div><h4>Zobozdravstvo</h4><ul>{svc_links(DENTAL[:6], P)}</ul></div>
  <div><h4>&nbsp;</h4><ul>{svc_links(DENTAL[6:], P)}</ul></div>
  <div><h4>Estetika</h4><ul>{svc_links(AESTH, P)}</ul>
    <h4 style="margin-top:36px">Za paciente</h4><ul><li><a href="{P}cenik.html">Cenik</a></li><li><a href="{P}o-nas.html#ekipa">Ekipa</a></li><li><a href="{P}o-nas.html#izjave">Izjave strank</a></li><li><a href="{P}darilni-boni.html">Darilni boni</a></li></ul></div>
  <a class="mega__feat" href="{P}storitve/all-on-4.html"><img src="{P}assets/img/all-on-4-namestitev.webp" alt=""><div><strong>Fiksni zobje v 24 urah</strong><span>Metoda All-on-4 →</span></div></a>
</div>
<div class="mmenu">
  <details><summary>Zobozdravstvo</summary><div>{''.join(f'<a href="{P}storitve/{s}.html">{E(n)}</a>' for s,n,*_ in DENTAL)}</div></details>
  <details><summary>Estetika</summary><div>{''.join(f'<a href="{P}storitve/{s}.html">{E(n)}</a>' for s,n,*_ in AESTH)}</div></details>
  <a href="{P}o-nas.html">O nas</a><a href="{P}cenik.html">Cenik</a><a href="{P}darilni-boni.html">Darilni boni</a><a href="{P}kontakt.html">Kontakt</a>
  <a class="btn" href="#" data-book>Naročite se na termin</a>
</div>
<div class="scrim"></div>
<aside class="drawer" aria-label="Naročanje">
  <button class="drawer__close" aria-label="Zapri">×</button>
  <img src="{P}assets/img/logo-blue.webp" alt="" style="width:190px">
  <h2>Naročite se na termin</h2>
  <p class="muted">Pokličemo vas v najkrajšem možnem času in skupaj najdemo termin, ki vam ustreza.</p>
  {form('d')}
</aside>
'''

def form(px, dark=False):
    return f'''<form class="form" novalidate>
    <div class="field"><input id="{px}n" name="ime" placeholder=" " required><label for="{px}n">Ime in priimek</label></div>
    <div class="row2"><div class="field"><input id="{px}t" name="tel" type="tel" placeholder=" " required><label for="{px}t">Telefonska številka</label></div>
    <div class="field"><input id="{px}e" name="email" type="email" placeholder=" " required><label for="{px}e">E-pošta</label></div></div>
    <div class="seg"><div class="seg__t">Lokacija</div><input type="radio" name="lok" id="{px}l1" checked><label for="{px}l1">Celje, Opekarniška c. 1</label><input type="radio" name="lok" id="{px}l2"><label for="{px}l2">Ljubljana, Dunajska c. 154</label></div>
    <div class="seg"><div class="seg__t">Termin</div><input type="radio" name="ter" id="{px}t1"><label for="{px}t1">Dopoldan</label><input type="radio" name="ter" id="{px}t2"><label for="{px}t2">Popoldan</label><input type="radio" name="ter" id="{px}t3" checked><label for="{px}t3">Kadarkoli</label></div>
    <div class="field"><textarea id="{px}m" name="msg" placeholder=" "></textarea><label for="{px}m">S čim vam lahko pomagamo?</label></div>
    <p class="note">Cena prvega pregleda in osnovne RTG analize (ortopan) je <b>40 EUR</b>.</p>
    <label class="check"><input type="checkbox" required> Strinjam se, da se moji osebni podatki uporabijo za odgovor na to sporočilo.</label>
    <button class="btn" type="submit">Pošljite povpraševanje <span class="arr">→</span></button>
    <div class="thanks"><h3>Hvala, prejeli smo vaše sporočilo.</h3><p class="muted">Kmalu vas pokličemo in uskladimo termin.</p></div>
  </form>'''

def footer(P):
    return f'''<footer class="foot">
  <div class="foot__top">
    <div class="foot__cta"><h3>Posvetujte se z nami.</h3><a class="btn" href="#" data-book>Naročite se na termin <span class="arr">→</span></a>
      <div class="foot__social"><a class="link" href="https://www.facebook.com/ZC.diamant/" target="_blank" rel="noopener">Facebook</a><a class="link" href="https://www.instagram.com/zcdiamant/" target="_blank" rel="noopener">Instagram</a><a class="link" href="https://www.youtube.com/channel/UCg3XoaiOanpri--0khzK8Zg" target="_blank" rel="noopener">YouTube</a><a class="link" href="https://www.tiktok.com/@zc.diamant" target="_blank" rel="noopener">TikTok</a></div></div>
    <div><h4>Ordinacija Celje</h4><ul><li>Opekarniška c. 1, 3000 Celje</li><li><a href="tel:+38630202020">030 20 20 20</a></li><li><a href="mailto:info@zobozdravstvo-diamant.si">info@zobozdravstvo-diamant.si</a></li><li class="muted">Pon–sre 7.00–20.00<br>Čet–pet 7.00–15.00</li></ul></div>
    <div><h4>Ordinacija Ljubljana</h4><ul><li>Dunajska c. 154, 1000 Ljubljana</li><li><a href="tel:+38671212121">071 21 21 21</a></li><li><a href="mailto:info-lj@zobozdravstvo-diamant.si">info-lj@zobozdravstvo-diamant.si</a></li><li class="muted">Pon 12.00–20.00<br>Tor–pet 7.00–15.00</li></ul></div>
    <div><h4>Diamant</h4><ul><li><a href="{P}storitve.html">Storitve</a></li><li><a href="{P}o-nas.html">O nas</a></li><li><a href="{P}o-nas.html#ekipa">Ekipa</a></li><li><a href="{P}cenik.html">Cenik</a></li><li><a href="{P}darilni-boni.html">Darilni boni</a></li><li><a href="{P}kontakt.html">Kontakt in lokacija</a></li></ul></div>
  </div>
  <div class="foot__mark"><img src="{P}assets/img/logo-wordmark.png" alt="Diamant"></div>
  <div class="foot__legal">
    <p>© 2026 Zobozdravstvo Diamant, implantologija in estetsko zobozdravstvo d.o.o. Naložbo VAVČER ZA DIGITALNI MARKETING sofinancirata Republika Slovenija in Evropska unija iz Evropskega sklada za regionalni razvoj.</p>
    <div class="foot__eu"><img src="{P}assets/img/f-sps.webp" alt="Slovenski podjetniški sklad"><img src="{P}assets/img/f-rs.webp" alt="Republika Slovenija"><img src="{P}assets/img/f-eu.webp" alt="Evropska unija"></div>
  </div>
</footer>
<div class="mbar"><a class="call" href="tel:+38630202020">Pokličite</a><button class="bk" data-book>Naročite se</button></div>
<script src="{P}assets/vendor/gsap.min.js"></script>
<script src="{P}assets/vendor/ScrollTrigger.min.js"></script>
<script src="{P}assets/vendor/lenis.min.js"></script>
<script src="{P}assets/js/main.js?v={V}"></script>
</body></html>'''

def page(path, title, desc, content, light=False, cur=''):
    depth = path.count('/'); P = '../' * depth
    full = head(title, desc, P) + nav(P, light, cur) + '<main>' + content(P) + '</main>' + footer(P)
    dst = os.path.join(OUT, path); os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf8').write(full)

def cta_band(P, h='Imamo izkušnje, lahko vam pomagamo.', p='Za informativno ponudbo se naročite na neobvezujoč pregled.'):
    return f'''<section class="sec--tight"><div class="cta-band rv"><h2>{E(h)}</h2><div><p>{E(p)}</p><a class="btn" href="#" data-book>Naročite se na pregled <span class="arr">→</span></a></div></div></section>'''

# ---------------------------------------------------------------- home
def home(P):
    I = P + 'assets/img/'
    svc_rows = lambda lst: ''.join(f'''<li><a href="{P}storitve/{s}.html" data-img="{I}{img}.webp"><span class="n">{E(n)}</span><span class="d">{E(d)}</span><span class="a">→</span><span class="thumb"><img src="{I}{img}.webp" alt="" loading="lazy"></span></a></li>''' for s, n, d, img, _ in lst)
    team = ''.join(f'''<article class="member"><div class="member__img{' cut' if cut else ''}"><img src="{I}{img}.webp" alt="{E(n)}" loading="lazy"></div><h3>{E(n)}</h3><p>{E(r)}</p></article>''' for img, n, r, cut in DENTISTS)
    quotes = ''.join(f'''<div class="q"><blockquote>{E(q)}</blockquote><cite><b>{E(n)}</b>{(' <span>· ' + E(c) + '</span>') if c else ''}</cite></div>''' for q, n, c in QUOTES)
    return f'''
<section class="hero">
  <div class="hero__media" aria-hidden="true">
    <img class="is-on" src="{I}hodnik.webp" alt="" fetchpriority="high">
    <img src="{I}cakalnica.webp" alt="">
    <img src="{I}ordinacija-01.webp" alt="">
    <img src="{I}zunaj.webp" alt="">
  </div>
  <div class="hero__inner">
    <h1>{lines('Ohranimo|vaš nasmeh,|preden je|prepozno.')}</h1>
    <div class="hero__side">
      <p>Zobozdravstveni center za zobozdravstvo, estetiko in implantologijo. V Celju in Ljubljani, brez čakalnih dob.</p>
      <div class="hero__btns"><a class="btn" href="#" data-book>Naročite se na termin <span class="arr">→</span></a><a class="btn btn--ghost" href="#storitve">Storitve</a></div>
      <div class="hero__dots"><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i></div>
    </div>
  </div>
</section>

<section class="statement sec wrap">
  <p class="big">Namen sodobnega zobozdravstva ni nadomeščanje vaših zob z umetnimi. Edina prava pot je, da ohranite svoje zobe do pozne starosti.</p>
  <div class="stats">
    <div class="stat rv"><b data-count="29000">0<sup>+</sup></b><span>pacientov se ne more motiti</span></div>
    <div class="stat rv"><b data-count="36">0<sup>×</sup></b><span>povečava mikroskopa pri vsakem natančnem posegu</span></div>
    <div class="stat rv"><b data-count="84">0</b><span>obrokov za plačilo z Leanpay, brez obiska banke</span></div>
    <div class="stat rv"><b data-count="2">0</b><span>ordinaciji, v Celju in v Ljubljani</span></div>
  </div>
</section>

<section class="svc sec" id="storitve">
  <div class="wrap">
    <div class="sec-head"><h2 class="h2" data-split>{lines('Vse na|enem mestu.')}</h2>
      <div class="rv"><p>Od rentgenskega slikanja do operativnih posegov. Načrtujemo daljše termine, da lahko v enem obisku naredimo več.</p>
      <div class="tabs" style="margin-top:28px"><button class="is-on" data-tab="z">Zobozdravstvo<sup>{len(DENTAL)}</sup></button><button data-tab="e">Estetika<sup>{len(AESTH)}</sup></button></div></div>
    </div>
    <ul class="svc-list" data-list="z">{svc_rows(DENTAL)}</ul>
    <ul class="svc-list" data-list="e" hidden>{svc_rows(AESTH)}</ul>
  </div>
  <div class="float-img"><img src="{I}s-implantati.webp" alt=""></div>
</section>

<section class="story">
  <div class="story__grid wrap">
    <div class="story__left">
      <h2 class="h2" data-split>{lines('Fiksni zobje|v 24 urah.')}</h2>
      <p class="lead rv" style="margin-top:28px;color:rgba(255,255,255,.72);max-width:30ch">Metoda All-on-4 obnovi celotno zobovje na le štirih vsadkih na čeljust. Brez dodajanja umetne kosti.</p>
      <div class="story__price rv"><div><b>7.490 €</b><span>skupaj s cirkonijevimi zobmi</span></div><div><b>1 ura</b><span>poseg na eno čeljust</span></div></div>
      <div class="steps">
        <div class="step"><i>01</i><div><h3>3D diagnostika</h3><p>Na podlagi CBCT slikanja dobimo natančen vpogled v stanje čeljusti in kostnine.</p><img class="m-img" src="{I}implant-prerez.webp" alt="" loading="lazy"></div></div>
        <div class="step"><i>02</i><div><h3>Štirje vsadki</h3><p>Sprednja dva postavimo ravno, zadnja dva pod kotom, da se izognemo sinusu ali živcu. Poseg poteka v lokalni anesteziji.</p><img class="m-img" src="{I}implant-razstavljen.webp" alt="" loading="lazy"></div></div>
        <div class="step"><i>03</i><div><h3>Začasni mostiček isti dan</h3><p>Ob koncu posega namestimo začasen mostiček za takojšnjo funkcijo in estetski videz.</p><img class="m-img" src="{I}implant-sestavljen.webp" alt="" loading="lazy"></div></div>
        <div class="step"><i>04</i><div><h3>Končni mostiček iz cirkona</h3><p>Po 4 do 6 mesecih, ko se vsadki vrastejo in dlesen dozori, namestimo končno fiksno protezo.</p><img class="m-img" src="{I}all-on-4-namestitev.webp" alt="" loading="lazy" style="border-radius:14px"></div></div>
      </div>
      <a class="btn btn--white" href="{P}storitve/all-on-4.html" style="margin-top:48px">Več o metodi All-on-4 <span class="arr">→</span></a>
    </div>
    <div class="story__right"><div class="story__stage">
      <div class="story__glow"></div>
      <figure><img src="{I}implant-prerez.webp" alt="Prerez zobnega vsadka"></figure>
      <figure><img src="{I}implant-razstavljen.webp" alt="Sestavni deli zobnega vsadka"></figure>
      <figure><img src="{I}implant-sestavljen.webp" alt="Sestavljen zobni vsadek s krono"></figure>
      <figure><img class="wide" src="{I}all-on-4-namestitev.webp" alt="All-on-4 mostiček na štirih vsadkih"></figure>
    </div></div>
  </div>
</section>

<section class="sec wrap">
  <div class="sec-head"><h2 class="h2" data-split>{lines('Vrnili ste mi|nasmeh.')}</h2><p class="rv">Primeri iz naše ordinacije. Povlecite drsnik in primerjajte stanje pred posegom in po njem.</p></div>
  <div class="ba-grid">
    <div><div class="ba rv"><img src="{I}ba1-pred.webp" alt="Pred posegom"><img class="after" src="{I}ba1-po.webp" alt="Po posegu"><span class="tag l">Pred</span><span class="tag r">Po</span><span class="handle"></span></div><p class="ba-cap">Estetska obnova sprednjih zob</p></div>
    <div><div class="ba rv"><img src="{I}ba2-pred.webp" alt="Pred posegom"><img class="after" src="{I}ba2-po.webp" alt="Po posegu"><span class="tag l">Pred</span><span class="tag r">Po</span><span class="handle"></span></div><p class="ba-cap">Celostna rehabilitacija zgornje in spodnje čeljusti</p></div>
  </div>
</section>

<section class="sec--tight wrap" style="padding-top:0">
  <div class="sec-head"><h2 class="h2" data-split>{lines('Vrhunska tehnologija|in umetnost.')}</h2><p class="rv">Dober zobozdravnik mora imeti izreden čut za estetiko. Šele kombinacija umetnika in perfekcionista, ki pozna vso tehnologijo, vodi do vrhunske kakovosti.</p></div>
  <div class="bento">
    <div class="tile t1" data-par><img src="{I}mikroskop.webp" alt="Delo pod mikroskopom" loading="lazy"><div><h3>Pod 36× povečavo</h3><p>Vse storitve opravimo vsaj pod 3× povečavo z lupami ali celo pod 36× povečavo z mikroskopom, zato držijo dlje.</p></div></div>
    <div class="tile t2" data-par><img src="{I}skener.webp" alt="Intraoralni skener" loading="lazy"><div><h3>Digitalni odtis</h3><p>Zob ne odtiskujemo klasično, ampak jih digitalno poskeniramo. Brez neprijetnega okusa in siljenja na bruhanje.</p></div></div>
    <div class="tile t3" data-par><img src="{I}cad-cam.webp" alt="CAD-CAM" loading="lazy"><div><h3>Lasten CAD-CAM laboratorij</h3><p>Večino protetičnih izdelkov izdelamo v našem digitaliziranem laboratoriju v Celju.</p></div></div>
    <div class="tile t4 tile--stat"><div><b>0</b><p>čakalnih dob za rentgensko slikanje</p></div></div>
    <div class="tile t5" data-par><img src="{I}cbct.webp" alt="CBCT 3D rentgen" loading="lazy"><div><h3>CBCT 3D rentgen</h3><p>Ortopan in 3D slikanje na obeh lokacijah, z mnogokrat nižjo dozo sevanja.</p></div></div>
  </div>
</section>

<section class="sec wrap" style="background:var(--paper)">
  <div class="why">
    <div class="why__l"><div class="why__sticky">
      <h2 class="h2" data-split>{lines('Zasebna|ambulanta brez|koncesije.')}</h2>
      <p class="rv">Opravljamo nadstandardne storitve, ki jih ZZZS žal ne plača. Čas in denar, ki ga prihranimo pri administraciji, raje posvečamo vam in izobraževanju osebja. Zato naše cene bistveno ne odstopajo od doplačil pri koncesionarju.</p>
      <div class="why__img rv" data-par><img src="{I}sprejem.webp" alt="Sprejem v centru Diamant" loading="lazy"></div>
    </div></div>
    <div class="why__list">
      <div class="why__item rv"><h3>Enostavno naročanje</h3><p>Naročite se preko aplikacije ali po telefonu 030 20 20 20 v Celju oziroma 071 21 21 21 v Ljubljani.</p></div>
      <div class="why__item rv"><h3>Vse na enem mestu</h3><p>Od rentgenskega slikanja do operativnih posegov. Za preglede, kontrole in vzdrževanja omogočamo termine tudi v poznih popoldanskih urah.</p></div>
      <div class="why__item rv"><h3>Brez strahu</h3><p>Posebej obravnavamo paciente s strahom, sladkorne bolnike, študente in mladostnike. Na voljo je tudi inhalacijska sedacija.</p></div>
      <div class="why__item rv"><h3>Vrednost glede na ceno</h3><p>Z razumnimi cenami in pametnim načrtovanjem zagotovimo čudovit nasmeh in uporabne zobe tudi vam. Če imate željo, bomo skupaj našli pot.</p></div>
      <div class="why__item rv"><a class="btn btn--ink" href="{P}o-nas.html">Več o nas <span class="arr">→</span></a></div>
    </div>
  </div>
</section>

<section class="team sec" id="ekipa">
  <div class="wrap"><div class="sec-head"><h2 class="h2" data-split>{lines('Perfekcionisti,|ki jim zaupate.')}</h2><p class="rv">Ekipa zobozdravnikov, ustnih higienikov, asistentk in zobotehnikov, ki dela s strastjo in veseljem.</p></div></div>
  <div class="team__track">{team}</div>
  <div class="team__foot"><div class="team__bar"><span></span></div><a class="link" href="{P}o-nas.html#ekipa">Spoznajte celotno ekipo →</a></div>
</section>

<section class="sec wrap" id="izjave">
  <div class="quotes">
    <div><h2 class="h2" data-split>{lines('Kaj pravijo|pacienti.')}</h2>
      <div class="quotes__nav"><button data-q="prev" aria-label="Prejšnja">←</button><button data-q="next" aria-label="Naslednja">→</button></div>
      <p class="q-count"></p></div>
    <div class="q-stage">{quotes}</div>
  </div>
</section>

<section class="band sec--tight">
  <div class="band__grid wrap">
    <div class="band__num">84</div>
    <div><h2>Obrokov za vaš novi nasmeh.</h2><p>V sodelovanju s partnerjem Leanpay. Celoten postopek uredite na mobilnem telefonu ob obisku ordinacije, brez obiska banke in odvečne dokumentacije.</p></div>
    <a class="btn btn--white" href="https://pre-qualify.leanpay.si/check-limit" target="_blank" rel="noopener">Preverite svoj limit <span class="arr">→</span></a>
  </div>
</section>

<section class="sec wrap" id="lokacije">
  <div class="sec-head"><h2 class="h2" data-split>{lines('Celje|in Ljubljana.')}</h2><p class="rv">Dve sodobni ordinaciji z isto ekipo, istimi standardi in vedno dovolj parkirnih mest.</p></div>
  <div class="locs">
    <article class="loc rv"><div class="loc__img" data-par><img src="{I}zunaj.webp" alt="Center Diamant v Celju" loading="lazy"></div>
      <div class="loc__body"><h3>Celje</h3><div><h4>Naslov</h4><p>Opekarniška c. 1<br>3000 Celje</p></div><div><h4>Delovni čas</h4><p>Pon–sre 7.00–20.00<br>Čet–pet 7.00–15.00</p></div><div><h4>Telefon</h4><p><a href="tel:+38630202020">030 20 20 20</a></p></div><div><h4>E-pošta</h4><p><a href="mailto:info@zobozdravstvo-diamant.si">info@zobozdravstvo-diamant.si</a></p></div>
      <div class="acts"><a class="btn" href="#" data-book>Naročite se</a><a class="btn btn--ink" href="https://maps.google.com/?q=Opekarniška+cesta+1,+3000+Celje" target="_blank" rel="noopener">Navodila za pot</a></div></div></article>
    <article class="loc rv"><div class="loc__img" data-par><img src="{I}hotel-lj.webp" alt="Ordinacija Diamant v Ljubljani" loading="lazy"></div>
      <div class="loc__body"><h3>Ljubljana</h3><div><h4>Naslov</h4><p>Dunajska c. 154, pritličje hotela DoubleTree by Hilton</p></div><div><h4>Delovni čas</h4><p>Pon 12.00–20.00<br>Tor–pet 7.00–15.00</p></div><div><h4>Telefon</h4><p><a href="tel:+38671212121">071 21 21 21</a></p></div><div><h4>E-pošta</h4><p><a href="mailto:info-lj@zobozdravstvo-diamant.si">info-lj@zobozdravstvo-diamant.si</a></p></div>
      <div class="acts"><a class="btn" href="#" data-book>Naročite se</a><a class="btn btn--ink" href="https://maps.google.com/?q=Dunajska+cesta+154,+1000+Ljubljana" target="_blank" rel="noopener">Navodila za pot</a></div></div></article>
  </div>
</section>

<section class="sec--tight wrap" style="padding-top:0">
  <div class="sec-head"><h2 class="h2" data-split>{lines('Koristne|informacije.')}</h2><a class="link rv" href="#" style="justify-self:start">Vsi članki →</a></div>
  <div class="arts">
    <a class="art rv" href="#"><div class="art__img"><img src="{I}a-RiO6Zf.webp" alt="" loading="lazy"></div><time>17. 11. 2026</time><h3>Kaj krije zavarovalnica pri vsadku in kdaj se doplača</h3></a>
    <a class="art rv" href="#"><div class="art__img"><img src="{I}a-8x4lu9.webp" alt="" loading="lazy"></div><time>15. 11. 2026</time><h3>Kaj se zgodi, ko All-on-4 popusti in kaj je treba storiti</h3></a>
    <a class="art rv" href="#"><div class="art__img"><img src="{I}a-szfP9k.webp" alt="" loading="lazy"></div><time>13. 11. 2026</time><h3>Delna zobna proteza: kdaj zdrži in kdaj obremeni sosede</h3></a>
  </div>
</section>

<section class="book sec dark" id="narocanje">
  <div class="book__grid wrap">
    <div class="book__l"><h2 class="h1" data-split>{lines('Naročite se|na termin.')}</h2>
      <p class="rv">Izpolnite obrazec in pokličemo vas nazaj. Če imate strah pred zobozdravnikom, nam to zaupajte. Skupaj ga bomo pregnali.</p>
      <div class="book__contacts rv"><div><small>Celje</small><a href="tel:+38630202020">030 20 20 20</a></div><div><small>Ljubljana</small><a href="tel:+38671212121">071 21 21 21</a></div></div></div>
    <div class="rv">{form('h', True)}</div>
  </div>
</section>
'''

# ---------------------------------------------------------------- service pages
def service_page(item, cat):
    slug, name, desc, img, src = item
    title, lede, blocks, faq = parse(src)
    lede = lede or desc
    peers = [x for x in (DENTAL if cat == 'z' else AESTH) if x[0] != slug][:4]
    if len(peers) < 4: peers += [x for x in DENTAL if x[0] != slug][:4 - len(peers)]
    def content(P):
        I = P + 'assets/img/'
        secs = ''.join(f'<div class="prose-sec"><h2>{E(b["h"])}</h2><div class="prose rv">{render_items(b["items"])}</div></div>' for b in blocks)
        fq = ''
        if faq:
            fq = '<section class="sec--tight wrap"><h2 class="h2" style="margin-bottom:48px" data-split>' + lines('Pogosta vprašanja') + '</h2><div class="faq">' + ''.join(f'<details><summary>{E(q)}<span>+</span></summary><p>{E(a)}</p></details>' for q, a in faq) + '</div></section>'
        rel = ''.join(f'<a class="card rv" href="{P}storitve/{s}.html"><div class="card__img"><img src="{I}{im}.webp" alt="" loading="lazy"></div><h3>{E(n)}</h3><p>{E(d)}</p></a>' for s, n, d, im, _ in peers)
        bc = 'Estetika' if cat == 'e' else 'Zobozdravstvo'
        return f'''
<section class="phero">
  <div class="crumbs"><a href="{P}index.html">Domov</a><span>/</span><a href="{P}storitve.html">{bc}</a><span>/</span><span>{E(name)}</span></div>
  <div class="phero__grid"><h1>{lines(name)}</h1><div><p class="lead">{E(lede)}</p><a class="btn" href="#" data-book style="margin-top:28px">Naročite se na pregled <span class="arr">→</span></a></div></div>
  <div class="phero__img" data-par><img src="{I}{img}.webp" alt="{E(name)}"></div>
</section>
<section class="wrap" style="padding-top:clamp(40px,4vw,80px)">{secs}</section>
{fq}
{cta_band(P)}
<section class="sec--tight wrap"><div class="sec-head" style="margin-bottom:40px"><h2 class="h2" data-split>{lines('Podobne storitve')}</h2><a class="link" href="{P}storitve.html" style="justify-self:start">Vse storitve →</a></div><div class="cards">{rel}</div></section>
'''
    page(f'storitve/{slug}.html', f'{name} | Zobozdravstveni center Diamant', lede[:155], content, light=True, cur='storitve')
    return len(blocks), len(faq)

def storitve(P):
    I = P + 'assets/img/'
    card = lambda lst: ''.join(f'<a class="card rv" href="{P}storitve/{s}.html"><div class="card__img"><img src="{I}{im}.webp" alt="" loading="lazy"></div><h3>{E(n)}</h3><p>{E(d)}</p></a>' for s, n, d, im, _ in lst)
    return f'''
<section class="phero"><div class="crumbs"><a href="{P}index.html">Domov</a><span>/</span><span>Storitve</span></div>
  <div class="phero__grid"><h1>{lines('Storitve')}</h1><p class="lead">Vse od rentgenskega slikanja do operativnih posegov, pod isto streho. Brez bolečin in vsaj pod 3× povečavo.</p></div>
  <div class="phero__img" data-par><img src="{I}banner-zobo.webp" alt=""></div></section>
<section class="sec wrap"><div class="sec-head"><h2 class="h2" data-split>{lines('Zobozdravstvo')}</h2><p class="rv">Preventiva, estetika, protetika, implantologija in kirurgija.</p></div><div class="cards">{card(DENTAL)}</div></section>
<section class="sec wrap" style="padding-top:0"><div class="sec-head"><h2 class="h2" data-split>{lines('Estetika')}</h2><p class="rv">Za vsa vprašanja se pred terapijo pogovorite z usposobljenim strokovnjakom, ki bo svetoval primernost terapije.</p></div><div class="cards">{card(AESTH)}</div></section>
{cta_band(P, 'Bi želeli posvet z našim strokovnjakom?')}
'''

def onas(P):
    I = P + 'assets/img/'
    dent = ''.join(f'<article class="member rv"><div class="member__img{" cut" if cut else ""}"><img src="{I}{img}.webp" alt="{E(n)}" loading="lazy"></div><h3>{E(n)}</h3><p>{E(r)}</p></article>' for img, n, r, cut in DENTISTS)
    staff = ''.join(f'<article class="member rv"><div class="member__img"><img src="{I}{img}.webp" alt="{E(n)}" loading="lazy"></div><h3>{E(n)}</h3><p>{E(r)}</p></article>' for img, n, r in STAFF)
    aest = ''.join(f'<article class="member rv"><div class="member__img{" cut" if img=="t-eva" else ""}"><img src="{I}{img}.webp" alt="{E(n)}" loading="lazy"></div><h3>{E(n)}</h3><p>{E(r)}</p></article>' for img, n, r in AESTH_TEAM)
    quotes = ''.join(f'''<div class="q"><blockquote>{E(q)}</blockquote><cite><b>{E(n)}</b>{(' <span>· ' + E(c) + '</span>') if c else ''}</cite></div>''' for q, n, c in QUOTES)
    return f'''
<section class="phero"><div class="crumbs"><a href="{P}index.html">Domov</a><span>/</span><span>O nas</span></div>
  <div class="phero__grid"><h1>{lines('Smo perfekcionisti.')}</h1><p class="lead">Da smo drugačni, boste spoznali že ob vstopu v našo čakalnico. Težimo k estetiki in popolnosti.</p></div>
  <div class="phero__img" data-par><img src="{I}cakalnica.webp" alt="Čakalnica centra Diamant"></div></section>
<section class="wrap" style="padding-top:clamp(40px,4vw,80px)">
  <div class="prose-sec"><h2>Funkcionalno in estetsko hkrati</h2><div class="prose rv"><p>Storitve brez bolečin po dostopnih cenah želimo po kvaliteti približati specialističnem nivoju. V našem centru delamo po principu vse na enem mestu, tako prihranite pot in čas, pod isto streho pa je tudi mnogo lažje uskladiti termine.</p><p>Večino protetičnih del ne odtiskujemo klasično, ampak zobe digitalno poskeniramo. Protetični izdelki se tako perfektno prilegajo, večino pa jih izdelamo v našem digitaliziranem zobotehničnem laboratoriju v Celju.</p><p>Zobozdravstvo je drago, vendar se vedno prilagodimo pacientovim zmožnostim in poskrbimo, da je sama izvedba in uporabna vrednost visoka.</p></div></div>
  <div class="prose-sec"><h2>Zasebna ambulanta brez koncesije</h2><div class="prose rv"><p>V naših ordinacijah opravljamo nadstandardne in visokokakovostne storitve, ki jih ZZZS žal ne plača. Koncesije nismo pridobili, da lahko pacientom ponudimo največ za relativno ugodno ceno.</p><p>Tako prihranimo ogromno administrativnega dela, čas in denar pa raje posvečamo vam oziroma ga vlagamo v izobraževanje osebja. Pacientom omogočamo prijazen delovni čas, storitve brez čakalnih dob in, upamo si trditi, bistveno boljšo kvaliteto.</p></div></div>
</section>
<section class="sec--tight wrap"><div class="bento">
  <div class="tile t2" data-par><img src="{I}ekipa-skupaj.webp" alt="" loading="lazy"><div><h3>Ekipa s timskim duhom</h3><p>Sproščeno vzdušje, kjer imate občutek, da ste prišli na obisk k prijatelju.</p></div></div>
  <div class="tile t3" data-par><img src="{I}logo-stena.webp" alt="" loading="lazy"><div><h3>Celje</h3><p>Objekt PSO Diamant nasproti Celjskega sejma.</p></div></div>
  <div class="tile t4 tile--stat"><div><b>29.000+</b><p>zadovoljnih pacientov</p></div></div>
</div></section>
<section class="sec wrap" id="ekipa"><div class="sec-head"><h2 class="h2" data-split>{lines('Zobozdravniki')}</h2><p class="rv">Splošno zobozdravstvo, protetika, endodontija, implantologija in oralna kirurgija.</p></div><div class="tgrid">{dent}</div></section>
<section class="sec--tight wrap" style="padding-top:0"><div class="sec-head"><h2 class="h2" data-split>{lines('Higieniki, asistentke|in laboratorij')}</h2><p class="rv">Skrbijo za vašo ustno higieno, sterilizacijo, pripravo in udobje med vsakim obiskom.</p></div><div class="tgrid tgrid--small">{staff}</div></section>
<section class="sec--tight wrap"><div class="sec-head"><h2 class="h2" data-split>{lines('Ekipa za estetiko')}</h2><p class="rv">Pred vsako terapijo se pogovorite s strokovnjakom, ki svetuje glede na vaše stanje, starost in želje.</p></div><div class="tgrid">{aest}</div></section>
<section class="sec wrap" id="izjave"><div class="quotes"><div><h2 class="h2" data-split>{lines('Kaj pravijo|pacienti.')}</h2><div class="quotes__nav"><button data-q="prev" aria-label="Prejšnja">←</button><button data-q="next" aria-label="Naslednja">→</button></div><p class="q-count"></p></div><div class="q-stage">{quotes}</div></div></section>
{cta_band(P, 'V naših prostorih se boste sprostili tudi vi.', 'Skupaj bomo pregnali strah pred zobozdravnikom.')}
'''

PRICES = [
 ('pregledi','Pregledi in diagnostika',[('Pregled z anamnezo in analiza RTG','40 €'),('Kratek stomatološki pregled','20 €'),('Ortopantomografsko slikanje zob','30 €'),('CBCT 3D slikanje zob, segment 5×5 cm','50 €'),('CBCT 3D slikanje zob, segment 8×5 cm','70 €'),('CBCT 3D slikanje zob, segment 8×8 cm','90 €')]),
 ('implantologija','Implantologija',[('Implantat, zobni vsadek','750 €'),('Polnokeramična prevleka Zircon z nadgradnjo na implantatu','700 €'),('All-on-4, privijačen mostiček na 4 implantatih s takojšnjo obremenitvijo','4.990 €'),('All-on-4, končni mostiček iz cirkon oksidne keramike','2.500 €'),('2 implantata in spodnja proteza na 2 Locator polzilih','2.900 €'),('4 implantati in proteza na 4 Locator polzilih','5.200 €'),('Provizorična prevleka na implantatu','50 €')]),
 ('prevleke','Protetika, prevleke',[('Polnokeramična prevleka Zircon','410 €'),('Polnokeramični člen Zircon','410 €'),('Estetska keramična luska eMax','450 €'),('Polnokeramična endo prevleka','450 €'),('Onlay ali inlay','450 €'),('Provizorična prevleka','20–50 €')]),
 ('proteze','Protetika, proteze',[('Začasna delna proteza (1 zob)','100 €'),('Začasna delna proteza (2 do 3 zobje)','200 €'),('Začasna delna proteza (4 ali več zob)','320 €'),('Totalna zobna proteza','750 €'),('Delna proteza z ulito bazo Wissil','950 €'),('Polzilo, anker za nevidno zapono proteze','170 €'),('Podložitev proteze','100 €'),('Reparatura proteze','60–100 €')]),
 ('kirurgija','Oralna kirurgija',[('Kirurški izkles zoba','270 €'),('Izkles korenine','150 €'),('Reženjska operacija (kvadrant)','160 €'),('Apikotomija z retrogradno polnitvijo','250 €'),('Cistektomija','50–250 €'),('Enostavna ekstrakcija zoba','60 €'),('Komplicirana ekstrakcija zoba','90 €'),('Serijska ekstrakcija vseh zob v čeljusti','100 €'),('Augmentacija kosti ob implantatu','150–300 €'),('Sinus lift, odprti veliki','800 €'),('Sinus lift, zaprti mali','400 €'),('Šivanje','5 €')]),
 ('endodontija','Koreninsko zdravljenje',[('Endodontsko zdravljenje zoba s strojnim širjenjem kanalov, ultrazvokom in gumijasto opno (odvisno od števila kanalov)','200–800 €')]),
 ('konzervativa','Konzervativno zdravljenje',[('Kompozitna zalivka na 1 ploskvi','75 €'),('Kompozitna zalivka na 2 ploskvah','95 €'),('Kompozitna zalivka na 3 ali več ploskvah','120 €'),('Kompozitna zalivka na zobnem vratu','40 €'),('Kompozitna zalivka pod nivojem dlesni','40 €'),('Estetska dograditev sprednjega zoba','130 €'),('Povezava majavih zob s kompozitom','25 €'),('Zatiček in dograditev zoba (Fiberpost, Rebilda)','100 €'),('Gingivektomija','40 €')]),
 ('ortodontija','Ortodontski aparati',[('Ortodontski aparat','2.000–4.200 €'),('Retencijska opornica Essix','100 €'),('Retainer, pletena žička','100 €')]),
 ('higiena','Ustna higiena',[('Čiščenje zobnega kamna ter poliranje zob','60 €'),('Mali higienski paket (kamen, poliranje in peskanje)','70 €'),('Obsežno čiščenje zobnega kamna','80 €'),('Peskanje zob s poliranjem','35 €'),('Meritve obzobnih žepkov in ocena tveganja za parodontitis','60 €'),('Luščenje in glajenje korenin enega zoba','15 €'),('Luščenje in glajenje korenin po zobnem loku','150 €'),('Demontaža hibridne proteze in čiščenje pod njo','50–70 €')]),
 ('beljenje','Beljenje zob',[('Beljenje preko noči z opornicami in belilom Opalescence','300 €'),('Beljenje zob z lučko Fläsh v ordinaciji','350 €'),('Notranje beljenje avitalnega zoba','30 €')]),
 ('ostalo','Ostalo',[('Lokalna anestezija','5 €'),('Dodatek za delo pod mikroskopom','20 €'),('Gumijasta opna (koferdam)','10 €'),('Zobni nakit, kristal Swarovski','60 €'),('Michiganska razbremenilna opornica pri bruksizmu','300 €'),('Neopravičen izostanek, na uro','50 €')]),
 ('estetika','Estetske storitve',[('#Lipoliza',''),('Injekcijska lipoliza (podbradek), tretma','170 €'),('#Oblikovanje in povečava ustnic, polnila TEOSYAL',''),('0,5 ml','190 €'),('0,8 ml','250 €'),('1,0 ml','290 €'),('1,3 ml','377 €'),('1,5 ml','435 €'),('1,7 ml','493 €'),('2,0 ml','580 €'),('#Ostali predeli obraza (nazolabialne gubice …)',''),('0,5 ml','210 €'),('0,7 ml','250 €'),('1,0 ml','310 €'),('1,3 ml','403 €'),('1,5 ml','465 €'),('1,7 ml','527 €'),('2,0 ml','620 €'),('Raztapljanje starega polnila','140 €'),('Oblikovanje obraza z Allergan HArmonyCa 1,2 ml','900 €'),('#Glajenje gub (VISTABEL, Allergan, 8 € na enoto)',''),('Celoten obraz','od 256 €'),('Na čelu','od 80 €'),('Okrog oči','od 96 €'),('Med obrvmi','od 80 €'),('Nefertiti lift (regija vratu)','280 €'),('Gummy smile','80 €'),('Masseter (bruksizem, ožanje obraza)','300 €')]),
]
def cenik(P):
    navs = ''.join(f'<a href="#{k}">{E(t)}</a>' for k, t, _ in PRICES)
    tabs = ''.join(f'<div class="ptable" id="{k}"><h2>{E(t)}</h2><ul>' + ''.join((f'<li class="sub">{E(a[1:])}</li>' if a.startswith('#') else f'<li><span>{E(a)}</span><b>{E(b)}</b></li>') for a, b in rows) + '</ul></div>' for k, t, rows in PRICES)
    return f'''
<section class="phero"><div class="crumbs"><a href="{P}index.html">Domov</a><span>/</span><span>Cenik</span></div>
  <div class="phero__grid"><h1>{lines('Cenik')}</h1><p class="lead">Jasne cene brez presenečenj. Za informativno ponudbo se naročite na neobvezujoč pregled.</p></div></section>
<section class="sec--tight wrap"><div class="offers">
  <div class="offer rv"><h3>Mali higienski paket</h3><p>Čiščenje zobnih oblog in kamna ter peskanje in poliranje zob. Redno vzdrževanje, da noben problem ne ostane spregledan.</p><b>70 €</b><small>približno 40 minut</small></div>
  <div class="offer rv"><h3>Prevleke in mostički</h3><p>Brezkovinske estetske prevleke iz cirkona in polne keramike. Brez nadležnega odtiskovanja, narejene digitalno.</p><b>410 €</b><small>na člen, cena glede na količino</small></div>
  <div class="offer rv"><h3>Beljenje zob</h3><p>Beljenje spet poudari vaš nasmeh in ga posvetli. Priporočimo najprimernejšo metodo za vaše zobe.</p><b>300–350 €</b><small>120 minut</small></div>
</div></section>
<section class="wrap"><nav class="price-nav" aria-label="Kategorije">{navs}</nav>{tabs}</section>
{cta_band(P, 'Prepustite se našim strokovnjakom.')}
'''

def kontakt(P):
    I = P + 'assets/img/'
    return f'''
<section class="phero"><div class="crumbs"><a href="{P}index.html">Domov</a><span>/</span><span>Kontakt</span></div>
  <div class="phero__grid"><h1>{lines('Kontakt|in lokacija')}</h1><p class="lead">Vedno dovolj brezplačnih parkirnih mest pred stavbo. Gibalno oviranim je na voljo parkirišče pred zgornjim vhodom.</p></div></section>
<section class="sec--tight wrap"><div class="locs">
  <article class="loc rv"><div class="loc__img" data-par><img src="{I}vhod-01.webp" alt="" loading="lazy"></div><div class="loc__body"><h3>Celje</h3>
    <div><h4>Naslov</h4><p>Opekarniška c. 1, 3000 Celje</p></div><div><h4>Kontakt</h4><p><a href="tel:+38630202020">030 20 20 20</a><br><a href="mailto:info@zobozdravstvo-diamant.si">info@zobozdravstvo-diamant.si</a></p></div>
    <div style="grid-column:1/-1"><h4>Kako do nas</h4><p>Nahajamo se v objektu PSO Diamant nasproti Celjskega sejma in Tehnične trgovine Inpos. Avtocesto zapustite na izvozu Celje center. V križišču pri City Centru in Gostilni Amerika zavijte desno in iz krožišča zapeljite proti naši stavbi. Parkirate lahko na zgornjem ali spodnjem parkirišču.</p></div>
    <div class="acts"><a class="btn btn--ink" href="https://maps.google.com/?q=Opekarniška+cesta+1,+3000+Celje" target="_blank" rel="noopener">Odpri zemljevid</a></div></div></article>
  <article class="loc rv"><div class="loc__img" data-par><img src="{I}ordinacija-lj.webp" alt="" loading="lazy"></div><div class="loc__body"><h3>Ljubljana</h3>
    <div><h4>Naslov</h4><p>Dunajska c. 154, 1000 Ljubljana</p></div><div><h4>Kontakt</h4><p><a href="tel:+38671212121">071 21 21 21</a><br><a href="mailto:info-lj@zobozdravstvo-diamant.si">info-lj@zobozdravstvo-diamant.si</a></p></div>
    <div style="grid-column:1/-1"><h4>Kako do nas</h4><p>Center se nahaja v pritličju hotela DoubleTree by Hilton, desno od glavnega vhoda zraven restavracije Winners Lounge. Parkirate v garažni hiši Smelt pod hotelom, od koder je možen direkten vhod v center.</p></div>
    <div class="acts"><a class="btn btn--ink" href="https://maps.google.com/?q=Dunajska+cesta+154,+1000+Ljubljana" target="_blank" rel="noopener">Odpri zemljevid</a></div></div></article>
</div></section>
<section class="book sec dark"><div class="book__grid wrap"><div class="book__l"><h2 class="h1" data-split>{lines('Vrhunska oprema,|znanje in|poštenost.')}</h2><p class="rv">To je naš recept za zadovoljne paciente. Jure Robič, dr. dent. med., MSc.</p>
  <div class="book__contacts rv"><div><small>Podjetje</small><p style="font-size:18px;color:rgba(255,255,255,.75)">Zobozdravstvo Diamant, implantologija in estetsko zobozdravstvo d.o.o.<br>Opekarniška cesta 1, 3000 Celje<br>DŠ: 56599587 · Matična št.: 8097941000</p></div></div></div>
  <div class="rv">{form('k', True)}</div></div></section>
'''

BONI = [('b-pregled','Celosten pregled zob z rentgenskim posnetkom','40 €'),('b-swarovski','Swarovski kristal na zobu','60 €'),('b-higiena','Mali higienski paket','70 €'),('b-beljenje','Beljenje zob','300 €'),('b-gubice','Glajenje gubic obraza','175–525 €'),('b-poljub','Diamantov poljub, oblikovanje ustnic','190–870 €'),('b-50','Darilni bon 50 €','50 €'),('b-100','Darilni bon 100 €','100 €'),('b-150','Darilni bon 150 €','150 €'),('b-200','Darilni bon 200 €','200 €')]
def boni(P):
    I = P + 'assets/img/'
    cards = ''.join(f'<a class="card rv" href="#" data-book><div class="card__img" style="aspect-ratio:1"><img src="{I}{im}.webp" alt="{E(n)}" loading="lazy"></div><h3>{E(n)}</h3><p>{E(p)} · brezplačna dostava</p></a>' for im, n, p in BONI)
    return f'''
<section class="phero"><div class="crumbs"><a href="{P}index.html">Domov</a><span>/</span><span>Darilni boni</span></div>
  <div class="phero__grid"><h1>{lines('Nasmeh je|dragocen.')}</h1><p class="lead">Če iščete darilo za vaše najdražje, smo pripravili darilne bone za posamezne storitve ali poljubno vrednost.</p></div>
  <div class="phero__img" data-par><img src="{I}darilni-bon.webp" alt="Darilni bon Diamant"></div></section>
<section class="sec wrap"><div class="sec-head"><h2 class="h2" data-split>{lines('Izberite darilo')}</h2><p class="rv">Bon vam pošljemo na dom ali ga prevzamete na Opekarniški cesti 1 v Celju ali Dunajski cesti 154 v Ljubljani.</p></div><div class="cards">{cards}</div></section>
'''

# ---------------------------------------------------------------- build
if __name__ == '__main__':
    page('index.html', 'Zobozdravstveni center Diamant | Celje in Ljubljana', 'Zobozdravstvo, estetika in implantologija v Celju in Ljubljani. Več kot 29.000 zadovoljnih pacientov.', home)
    page('storitve.html', 'Storitve | Zobozdravstveni center Diamant', 'Zobozdravstvene in estetske storitve centra Diamant.', storitve, light=True, cur='storitve')
    page('o-nas.html', 'O nas | Zobozdravstveni center Diamant', 'Spoznajte ekipo centra Diamant.', onas, light=True, cur='o-nas')
    page('cenik.html', 'Cenik | Zobozdravstveni center Diamant', 'Cenik storitev centra Diamant.', cenik, light=True, cur='cenik')
    page('kontakt.html', 'Kontakt in lokacija | Zobozdravstveni center Diamant', 'Ordinaciji v Celju in Ljubljani.', kontakt, light=True, cur='kontakt')
    page('darilni-boni.html', 'Darilni boni | Zobozdravstveni center Diamant', 'Darilni boni centra Diamant.', boni, light=True, cur='boni')
    for it in DENTAL: print(it[0], service_page(it, 'z'))
    for it in AESTH: print(it[0], service_page(it, 'e'))
