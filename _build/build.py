# -*- coding: utf-8 -*-
"""Genera una pagina por proyecto y reescribe las rejillas de Identidad / Social /
Creatividad con tarjetas tipo producto. Fuente de verdad: _build/proyectos.json."""
import json, io, os, re, html as H

D = json.load(io.open("_build/proyectos.json", encoding="utf-8"))

T = {
 "es": {
  "lang":"es", "dir":"proyectos", "other":"en/projects", "otherlabel":"ENGLISH",
  "nav":[("identidad.html","Identidad"),("social.html","Social"),
         ("creativo.html","Creatividad"),("academico.html","Vida Académica")],
  "cta":"Contacto", "ctahref":"index.html#contacto",
  "sec":{"identidad":("identidad.html","Identidad"),
         "social":("social.html","Social"),
         "creativo":("creativo.html","Creatividad")},
  "back":"Volver a", "verproy":"Ver proyecto", "piezas":"piezas", "pieza":"pieza",
  "galtitle":"Galería", "galsub":"Toca cualquier imagen para verla en grande.",
  "home":"Volver al inicio", "locs":"México · Corea del Sur · España",
  "rights":"Todos los derechos reservados", "menu":"Menú",
 },
 "en": {
  "lang":"en", "dir":"en/projects", "other":"proyectos", "otherlabel":"ESPAÑOL",
  "nav":[("identity.html","Identity"),("social.html","Social"),
         ("creative.html","Creativity"),("academic.html","Academic Life")],
  "cta":"Contact", "ctahref":"index.html#contact",
  "sec":{"identidad":("identity.html","Identity"),
         "social":("social.html","Social"),
         "creativo":("creative.html","Creativity")},
  "back":"Back to", "verproy":"View project", "piezas":"pieces", "pieza":"piece",
  "galtitle":"Gallery", "galsub":"Tap any image to see it full size.",
  "home":"Back to home", "locs":"Mexico · South Korea · Spain",
  "rights":"All rights reserved", "menu":"Menu",
 },
}
HEAD_LINKS = """  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />"""
SITE = "https://madebynaxxo.github.io"

def esc(s): return H.escape(s, quote=True)

def nav(t, root, sec_root, lang_href, active=None):
    items = "".join(
        f'\n    <li><a href="{sec_root}{h}"{" style=\"color:var(--red)\"" if h==active else ""}>{l}</a></li>'
        for h, l in t["nav"])
    return f"""<nav>
  <a href="{sec_root}index.html" class="nav-logo"><span class="nav-dot"></span>Made by NAXXO</a>
  <button class="nav-ham" id="nav-ham" aria-label="{t['menu']}"><span></span><span></span><span></span></button>
  <ul class="nav-links" id="nav-links">{items}
    <li><a href="{lang_href}" class="lang-btn">{t['otherlabel']}</a></li>
    <li><a href="{sec_root}{t['ctahref']}" class="btn btn-red nav-cta">{t['cta']}</a></li>
  </ul>
</nav>"""

def footer(t, sec_root, back_href, back_label):
    return f"""<footer>
  <div>
    <div class="f-brand">Made by<br><span>NAXXO</span></div>
    <p class="f-sub">{t['locs']}</p>
  </div>
  <div>
    <a href="{back_href}" class="btn btn-out" style="margin-bottom:1rem;display:inline-flex;">← {back_label}</a>
    <p class="f-copy">© 2026 Made by NAXXO — {t['rights']}</p>
  </div>
</footer>"""

# ─────────────────────────────── paginas de proyecto ───────────────────────────────
def project_page(slug, lang):
    t = T[lang]; r = D[slug][lang]
    root = "../" if lang == "es" else "../../"          # hacia la raiz del sitio
    secr = "../" if lang == "es" else "../"             # hacia las paginas del idioma
    if lang == "en": secr = "../"
    lang_href = f"{root}{T['en' if lang=='es' else 'es']['dir']}/{slug}.html"
    sfile, slabel = t["sec"][r["section"]]

    pills = "".join(f'<span class="mpill">{p}</span>' for p in r["pills"])
    links = "".join(
        f'<a class="btn {"btn-red" if i==0 else "btn-out"}" href="{l["href"] if l["href"].startswith("http") else root+l["href"]}"'
        f' target="_blank" rel="noopener">{l["label"]}</a>' for i, l in enumerate(r["links"]))
    links = f'\n      <div class="proj-links">{links}</div>' if links else ""

    hero = f'''<div class="proj-cover reveal{" fit" if r["fit"] else ""}">
    <img src="{root}{r["hero"]}" alt="{esc(r["heroalt"] or r["title"])}" />
  </div>'''

    gal = r["gallery"]
    if gal:
        items = "\n      ".join(
            f'<a href="{root}{g["src"]}"><img src="{root}{g["src"]}" alt="{esc(g["alt"] or r["title"])}" loading="lazy" /></a>'
            for g in gal)
        gallery = f'''
<div class="band band-gal">
  <div class="gal-head reveal">
    <h2 class="gal-title">{t["galtitle"]}</h2>
    <p class="gal-sub">{t["galsub"]}</p>
  </div>
  <div class="masonry">
      {items}
  </div>
</div>'''
    else:
        gallery = ""

    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(r['title'])} — Made by NAXXO</title>
  <meta name="description" content="{esc(r['teaser'])}" />
  <link rel="alternate" hreflang="es" href="{SITE}/proyectos/{slug}.html" />
  <link rel="alternate" hreflang="en" href="{SITE}/en/projects/{slug}.html" />
{HEAD_LINKS}
  <link rel="stylesheet" href="{root}shared.css" />
</head>
<body>
<div class="grain"></div>
<div class="cursor" id="cur"></div>
<div class="cursor-ring" id="ring"></div>

{nav(t, root, secr, lang_href)}

<section class="proj-hero">
  <a class="proj-back reveal" href="{secr}{sfile}">← {t['back']} {slabel}</a>
  <div class="proj-grid">
    <div class="proj-left reveal d1">
      <span class="proj-tag">{r['tag']}</span>
      <h1 class="proj-title">{r['title']}</h1>
      <p class="proj-meta">{r['meta']}</p>
    </div>
    <div class="proj-right reveal d2">
      <p class="proj-body">{r['body']}</p>
      <div class="proj-pills">{pills}</div>{links}
    </div>
  </div>
  {hero}
</section>
{gallery}

{footer(t, secr, secr+sfile, t['back']+' '+slabel)}

<script src="{root}shared.js"></script>
</body>
</html>
"""

# ─────────────────────────────── tarjetas de seccion ───────────────────────────────
BREAK = {"es":"Diseño Web — JobBridgeKorea · Seúl 2025","en":"Web Design — JobBridgeKorea · Seoul 2025"}

def pcard(slug, lang, inside_en):
    t = T[lang]; r = D[slug][lang]
    root = "../" if inside_en else ""
    href = f'{"../" if inside_en else ""}{t["dir"].split("/")[-1] if inside_en else t["dir"]}/{slug}.html'
    href = f'projects/{slug}.html' if inside_en else f'proyectos/{slug}.html'
    n = 1 + len(r["gallery"])
    count = f'{n} {t["piezas"] if n != 1 else t["pieza"]}'
    pills = "".join(f'<span>{p}</span>' for p in r["pills"][:2]) + f'<span class="pc-n">{count}</span>'
    return f"""      <a class="pcard reveal" href="{href}">
        <div class="pcard-media{' fit' if r['fit'] else ''}">
          <img src="{root}{r['hero']}" alt="{esc(r['heroalt'] or r['title'])}" loading="lazy" />
          <span class="pcard-badge">{r['tag']}</span>
        </div>
        <div class="pcard-body">
          <div class="pcard-head">
            <h3 class="pcard-title">{r['title']}</h3>
            <span class="pcard-yr">{r['year']}</span>
          </div>
          <p class="pcard-desc">{esc(r['teaser'])}</p>
          <div class="pcard-pills">{pills}</div>
          <span class="pcard-cta">{t['verproy']}</span>
        </div>
      </a>
"""

SECTION_FILES = {("es","identidad"):"identidad.html", ("es","social"):"social.html",
                 ("es","creativo"):"creativo.html",   ("en","identidad"):"en/identity.html",
                 ("en","social"):"en/social.html",    ("en","creativo"):"en/creative.html"}
ORDER = {}
for s, v in D.items(): ORDER.setdefault(v["es"]["section"], []).append(s)

# acepta la rejilla vieja y la nueva, para poder volver a generar sin romper nada
band_re = re.compile(r'<div class="band">\s*<div class="(?:pgrid|pcards)[^"]*">.*?\n\s*</div>\n</div>', re.S)

def rewrite_section(lang, section):
    path = SECTION_FILES[(lang, section)]
    inside_en = (lang == "en")
    html = io.open(path, encoding="utf-8").read()
    cards = ""
    for slug in ORDER[section]:
        if section == "creativo" and slug == "buddystay":
            cards += f'      <div class="pcards-label reveal"><span>{BREAK[lang]}</span></div>\n'
        cards += pcard(slug, lang, inside_en)
    block = f'<div class="band">\n  <div class="pcards">\n{cards}  </div>\n</div>'
    new, n = band_re.subn(block, html, count=1)
    assert n == 1, f"{path}: no se encontro la rejilla"
    io.open(path, "w", encoding="utf-8").write(new)
    return path, len(ORDER[section])

if __name__ == "__main__":
    made = 0
    for lang in ("es", "en"):
        d = T[lang]["dir"]; os.makedirs(d, exist_ok=True)
        for slug in D:
            io.open(f"{d}/{slug}.html", "w", encoding="utf-8").write(project_page(slug, lang))
            made += 1
        print(f"{d}/ → {len(D)} páginas")
    for lang in ("es", "en"):
        for section in ("identidad", "social", "creativo"):
            p, k = rewrite_section(lang, section)
            print(f"{p:22} → {k} tarjetas")
    print(f"\n{made} páginas de proyecto generadas")
