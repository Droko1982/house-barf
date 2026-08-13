# -*- coding: utf-8 -*-
"""Build en/index.html from index.html using the i18n string map."""
import re, sys, json, html as H, urllib.parse, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
from i18n import T, A, J

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'index.html')
OUTDIR = os.path.join(REPO, 'en')
OUT = os.path.join(OUTDIR, 'index.html')
BASE = 'https://www.housebarf.com/'

src = open(SRC, encoding='utf-8', newline='').read()

# ---------------------------------------------------------------- split head
head_end = src.index('</head>')
head, body = src[:head_end], src[head_end:]

# ============================================================ 1. TEXT NODES
unknown = []
def translate_text_nodes(chunk):
    parts = re.split(r'(<[^>]+>)', chunk)
    out = []
    for p in parts:
        if p.startswith('<') or not p.strip():
            out.append(p); continue
        stripped = p.strip()
        if not re.search(r'[A-Za-zÁÉÍÓÚáéíóúñÑ¿¡]', stripped):
            out.append(p); continue
        if stripped in T:
            lead = p[:len(p) - len(p.lstrip())]
            trail = p[len(p.rstrip()):]
            out.append(lead + T[stripped] + trail)
        else:
            unknown.append(stripped)
            out.append(p)
    return ''.join(out)

# don't touch <script>/<style> contents in the text pass
segments = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', body, flags=re.S)
body = ''.join(seg if seg.startswith(('<script', '<style')) else translate_text_nodes(seg)
               for seg in segments)

# ======================================================== 2. ATTRIBUTES
unknown_attr = []
def attr_sub(m):
    name, val = m.group(1), m.group(2)
    if val in A: return f'{name}="{A[val]}"'
    if val in T: return f'{name}="{T[val]}"'
    if re.search(r'[A-Za-zÁÉÍÓÚáéíóúñÑ]', val) and not val.startswith(('#', 'http', 'data:')):
        unknown_attr.append(f'{name}="{val}"')
    return m.group(0)
body = re.sub(r'\b(alt|aria-label|title|placeholder)="([^"]*)"', attr_sub, body)

# ==================================================== 3. WHATSAPP MESSAGES
WA = {
 "Hola House Barf! Quiero pedir alimento 🐶 (desde menú)": "Hi House Barf! I'd like to order dog food 🐶 (from the menu)",
 "Hola House Barf! Quiero pedir alimento 🐶 (ví la página web)": "Hi House Barf! I'd like to order dog food 🐶 (from your website)",
 "Hola House Barf! Quiero pedir alimento 🐶 (botón flotante)": "Hi House Barf! I'd like to order dog food 🐶 (floating button)",
 "Hola House Barf! Quiero pedir alimento 🐶 (desde celular)": "Hi House Barf! I'd like to order dog food 🐶 (from mobile)",
 "Hola House Barf! Quiero saber si hacen domicilio en mi zona del Eje Cafetero 🐶":
   "Hi House Barf! I'd like to know if you deliver to my area in the Coffee Region 🐶",
 "Hola House Barf! Quiero asesoría sobre la alimentación de mi perro 🐶":
   "Hi House Barf! I'd like some advice about feeding my dog 🐶",
 "Hola House Barf! Tengo un perro raza ____, ¿cuánto debe comer? 🐶":
   "Hi House Barf! I have a ____ breed dog, how much should it eat? 🐶",
 "Hola House Barf! Quiero ser distribuidor / trabajar con ustedes 🤝":
   "Hi House Barf! I'd like to become a distributor / work with you 🤝",
 "Mira House Barf! Comida para perros en Armenia Quindío a $4,500/lb con domicilio gratis desde 5kg 🐶":
   "Check out House Barf! Dog food in Armenia, Quindío at $4,500/lb with free delivery on 5kg+ 🐶",
}
unknown_wa = []
def wa_sub(m):
    raw = m.group(1)
    dec = urllib.parse.unquote(H.unescape(raw))
    if dec in WA:
        return 'wa.me/573126737317?text=' + urllib.parse.quote(WA[dec], safe='')
    if '${' in dec or '+' in raw:
        return m.group(0)            # template literal built in JS, handled separately
    unknown_wa.append(dec)
    return m.group(0)
body = re.sub(r'wa\.me/573126737317\?text=([^"\'\s>]+)', wa_sub, body)

# the "share with a friend" link has no phone number, so the regex above skips it.
# match on the decoded text so we never depend on a particular percent-encoding.
SHARE_EN = ("I recommend House Barf for your dog! Premium traditional chicken & vegetable dog food "
            "at $4,500/lb with free delivery in Armenia on 5kg+. Order at 318 587 5211 \U0001F43E")
def share_sub(m):
    dec = urllib.parse.unquote(m.group(1))
    if 'recomiendo House Barf' not in dec:
        unknown_wa.append(dec); return m.group(0)
    return 'wa.me/?text=' + urllib.parse.quote(SHARE_EN, safe='')
body = re.sub(r'wa\.me/\?text=([^"\'\s>]+)', share_sub, body)

# ================================================ 4. JS-EMBEDDED STRINGS
def js_translate(m):
    block = m.group(0)
    for es, en in sorted(J.items(), key=lambda kv: -len(kv[0])):
        block = block.replace(es, en)
    block = block.replace(
      "Hola House Barf! 🐶 Mi perro pesa ${w}kg (tamaño ${r.breed}). Quiero pedir ${monthlyLb} libras de Alimento Sabor Tradicional Pollo y Verduras por $${monthlyCost.toLocaleString('es-CO')}. (desde calculadora)",
      "Hi House Barf! 🐶 My dog weighs ${w}kg (${r.breed} size). I'd like to order ${monthlyLb} pounds of Traditional Chicken & Vegetable dog food for $${monthlyCost.toLocaleString('es-CO')}. (from the calculator)")
    block = block.replace(
      "Hola House Barf! \U0001F436 Quiero pedir ${qty} libra(s) de Alimento Sabor Tradicional Pollo y Verduras por $${priceStr}. (desde producto)",
      "Hi House Barf! \U0001F436 I'd like to order ${qty} pound(s) of Traditional Chicken & Vegetable dog food for $${priceStr}. (from the product section)")
    block = block.replace("'Como un ' + r.breed", "'About the size of a ' + r.breed")
    block = block.replace("Pedir ${monthlyLb} lb por WhatsApp", "Order ${monthlyLb} lb on WhatsApp")
    block = block.replace("Pedir ${qty} lb por WhatsApp", "Order ${qty} lb on WhatsApp")
    block = block.replace("hace ", "").replace(" min'", " min ago'")
    # nothing Spanish may survive in the shipped JS
    leftover = re.findall(r'(?:Hola|Quiero|libra|Concentrado|Pedir|domicilio|tamaño|porción|desde )', block)
    if leftover:
        print('WARNING untranslated JS tokens:', sorted(set(leftover)))
    return block
body = re.sub(r'<script(?![^>]*type="application/ld)(?![^>]*src=)[^>]*>.*?</script>', js_translate, body, flags=re.S)

# ==================================================== 5. RELATIVE ASSET PATHS
for a in ('hero.jpg', 'icon-192.png', 'privacidad.html'):
    body = body.replace(f'"{a}"', f'"../{a}"')
    head = head.replace(f'"{a}"', f'"../{a}"')
body = body.replace("register('sw.js')", "register('../sw.js')")
# /en/ has its own manifest (English name, English shortcuts, its own scope),
# so this one stays a sibling reference rather than being rewritten to ../
assert 'rel="manifest" href="manifest.json"' in head, 'manifest link not found'

# ============================================================== 6. HEAD
head = head.replace('<html lang="es">', '<html lang="en">')
head = re.sub(r'<title>.*?</title>',
  '<title>Dog Food in Armenia, Quindío &amp; the Coffee Region | House Barf</title>', head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="Premium chicken &amp; vegetable dog food at $4,500/lb with prebiotics and probiotics. Free delivery in Armenia on 5kg+ and shipping across Quindío and Colombia\'s Coffee Region.">', head)
head = re.sub(r'<meta name="keywords" content="[^"]*">',
  '<meta name="keywords" content="dog food Armenia Colombia, dog food Quindio, dog food Coffee Region Colombia, dog food delivery Armenia, buy dog food Colombia, English speaking pet food Quindio, dog food Pereira, dog food Manizales, dog food Salento, dog food Filandia, dog food Circasia, dog food Calarca, premium dog food Colombia, kibble Armenia Quindio, dog food with probiotics Colombia, expat dog food Colombia, pet supplies Armenia Quindio, large breed dog food Colombia, puppy food Armenia, dog nutrition Coffee Region">', head)
head = head.replace('<meta http-equiv="content-language" content="es-CO">',
                    '<meta http-equiv="content-language" content="en">')
head = head.replace('<meta name="language" content="es">', '<meta name="language" content="en">')
# hreflang: this page is the English alternate
head = re.sub(r'<link rel="alternate" hreflang="es-CO"[^>]*>\s*<link rel="alternate" hreflang="es"[^>]*>\s*<link rel="alternate" hreflang="x-default"[^>]*>',
  f'<link rel="alternate" hreflang="es-CO" href="{BASE}">\n    <link rel="alternate" hreflang="es" href="{BASE}">\n    <link rel="alternate" hreflang="en" href="{BASE}en/">\n    <link rel="alternate" hreflang="x-default" href="{BASE}">', head)
head = head.replace(f'<link rel="canonical" href="{BASE}">', f'<link rel="canonical" href="{BASE}en/">')
head = head.replace('<meta property="og:locale" content="es_CO">',
                    '<meta property="og:locale" content="en_US">\n    <meta property="og:locale:alternate" content="es_CO">')
head = head.replace(f'<meta property="og:url" content="{BASE}">', f'<meta property="og:url" content="{BASE}en/">')
head = re.sub(r'<meta property="og:title" content="[^"]*">',
  '<meta property="og:title" content="Dog Food in Armenia, Quindío &amp; the Coffee Region - House Barf $4,500/lb">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">',
  '<meta property="og:description" content="Premium chicken &amp; vegetable dog food at $4,500/lb. Free delivery in Armenia on 5kg+. We ship to Calarcá, Montenegro, Circasia, Pereira, Manizales and the whole Coffee Region. WhatsApp 312 673 7317.">', head)
head = re.sub(r'<meta name="twitter:title" content="[^"]*">',
  '<meta name="twitter:title" content="Dog Food in Armenia, Quindío &amp; the Coffee Region - House Barf">', head)
head = re.sub(r'<meta name="twitter:description" content="[^"]*">',
  '<meta name="twitter:description" content="Premium chicken &amp; vegetable dog food at $4,500/lb. Free delivery in Armenia on 5kg+. Shipping across Quindío and the Coffee Region. Nequi and cash accepted.">', head)
head = re.sub(r'<meta property="og:site_name" content="[^"]*">',
  '<meta property="og:site_name" content="House Barf - Dog Food Armenia Quindío">', head)
for a in ('og:image:alt', 'twitter:image:alt'):
    head = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % re.escape(a),
                  r'\1House Barf - premium dog food in Armenia, Quindío and the Coffee Region"', head)
head = head.replace('<meta name="apple-mobile-web-app-title" content="House Barf">',
                    '<meta name="apple-mobile-web-app-title" content="House Barf">')

# ------------------------------------------------------ 7. JSON-LD in English
m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', head, re.S)
data = json.loads(m.group(2))
EN = f'{BASE}en/'
for e in data:
    t = e.get('@type')
    e['url'] = EN if 'url' in e else e.get('url')
    if t == 'LocalBusiness':
        e['@id'] = EN + '#business'
        e['name'] = 'House Barf - Dog Food Armenia, Quindío & the Coffee Region'
        e['description'] = ("Dog food sold in Armenia, across Quindío and throughout Colombia's Coffee Region. "
            "Premium chicken and vegetable food at $4,500 per pound. Free delivery in Armenia on orders of 5kg or more, "
            "with shipping to Pereira, Manizales and other towns in the region. Orders via WhatsApp.")
        e['slogan'] = 'Full Bellies, Happy Tails'
        e['knowsLanguage'] = ['es', 'en']
    elif t == 'Product':
        e['name'] = 'House Barf Traditional Chicken & Vegetable Dog Food'
        e['description'] = ("Premium chicken and vegetable dry dog food for every breed and size. Sold by the pound. "
            "Free delivery in Armenia on 5kg+ and shipping across Quindío and the Coffee Region.")
        e['category'] = 'Dog Food'
        for prop in e.get('additionalProperty', []):
            prop['name'] = {'Sabor':'Flavour','Prebióticos':'Prebiotics','Probióticos':'Probiotics','Enriquecido':'Enriched'}.get(prop['name'], prop['name'])
            prop['value'] = {'Pollo y Verduras':'Chicken & Vegetables','Sí':'Yes'}.get(prop['value'], prop['value'])
        e['offers']['url'] = EN
    elif t == 'Organization':
        e['@id'] = EN + '#organization'
        e['slogan'] = 'Full Bellies, Happy Tails'
        e['knowsLanguage'] = ['es', 'en']
        e['contactPoint']['availableLanguage'] = ['Spanish', 'English']
    elif t == 'BreadcrumbList':
        e['itemListElement'] = [{"@type":"ListItem","position":1,"name":"Home","item":BASE},
                                {"@type":"ListItem","position":2,"name":"English","item":EN}]
    elif t == 'WebSite':
        e['url'] = BASE
        e['potentialAction']['target']['urlTemplate'] = 'https://wa.me/573126737317?text={search_term_string}'
    elif t == 'WebPage':
        e['name'] = 'Dog Food in Armenia, Quindío & the Coffee Region | House Barf'
        e['description'] = ("Premium chicken and vegetable dog food at $4,500/lb with free delivery in Armenia on 5kg+ "
            "and shipping across Quindío and the Coffee Region.")
        e['inLanguage'] = 'en'
        e['isPartOf'] = {"@type":"WebSite","name":"House Barf","url":BASE}
        e['about'] = {"@type":"Thing","name":"Dog food in Armenia, Quindío and the Coffee Region"}
        e['mentions'] = [{"@type":"Place","name":"Armenia, Quindío"},{"@type":"Place","name":"Pereira, Risaralda"},
                         {"@type":"Place","name":"Manizales, Caldas"},{"@type":"Place","name":"Coffee Region, Colombia"}]
    elif t == 'ItemList':
        e['name'] = 'Popular Dog Breeds in Armenia and the Coffee Region'
        e['description'] = 'House Barf suits every dog breed in Armenia and the Coffee Region'
        for it in e['itemListElement']:
            it['name'] = {'Pastor Alemán':'German Shepherd','Mestizo / Criollo':'Mixed Breed'}.get(it['name'], it['name'])
            it['description'] = re.sub(r'^.*? - ', '', it['description'])
            it['description'] = f"{it['name']} dog food in Armenia and the Coffee Region - House Barf premium nutrition"
# FAQ is rebuilt from the translated page below
head = head[:m.start(2)] + '\n    __LDJSON__\n    ' + head[m.end(2):]

full = head + body

# rebuild FAQPage from the *translated* visible FAQ so schema and page always match
items = re.findall(r'<button class="faq-q">(.*?)<svg.*?<div class="faq-a"><p>(.*?)</p></div>', full, re.S)
qa = [{"@type":"Question","name":H.unescape(re.sub(r'<[^>]+>','',q)).strip(),
       "acceptedAnswer":{"@type":"Answer","text":H.unescape(re.sub(r'<[^>]+>','',a)).strip()}} for q, a in items]
for e in data:
    if e.get('@type') == 'FAQPage':
        e['@id'] = EN + '#faq'; e['inLanguage'] = 'en'; e['mainEntity'] = qa
full = full.replace('__LDJSON__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))

# ------------------------------------------------- 8. language switcher in nav
# the Spanish source ships an ES->EN switcher; swap it for the EN->ES one rather
# than appending a second control (its CSS is inherited with the rest of the sheet)
SWITCH_ES = ('<a href="../" class="lang-switch" hreflang="es" lang="es" '
             'aria-label="Ver esta página en español" title="Ver en español">ES</a>')
inherited = re.search(r'<a href="en/" class="lang-switch"[^>]*>EN</a>', full)
if inherited:
    full = full.replace(inherited.group(0), SWITCH_ES, 1)
else:
    print('WARNING: source switcher not found; inserting one')
    full = full.replace('<button class="theme-toggle" id="themeToggle"',
                        SWITCH_ES + '\n                <button class="theme-toggle" id="themeToggle"', 1)
assert full.count('class="lang-switch"') == 1, 'expected exactly one language switcher'

os.makedirs(OUTDIR, exist_ok=True)
open(OUT, 'w', encoding='utf-8', newline='').write(full)

print('wrote', OUT, '%.0f KB' % (len(full.encode('utf-8'))/1024))

# the source's ES->EN switcher is replaced wholesale above, so it is not a translation gap
SWITCHER_NOISE = {'EN', 'aria-label="View this page in English"', 'title="View in English"'}
unknown = [u for u in unknown if u not in SWITCHER_NOISE]
unknown_attr = [u for u in unknown_attr if u not in SWITCHER_NOISE]

print('\nUNTRANSLATED text nodes :', len(set(unknown)))
for u in sorted(set(unknown)): print('   |', u[:100])
print('\nUNTRANSLATED attributes :', len(set(unknown_attr)))
for u in sorted(set(unknown_attr)): print('   |', u[:100])
print('\nUNMAPPED whatsapp msgs  :', len(set(unknown_wa)))
for u in sorted(set(unknown_wa)): print('   |', u[:100])
