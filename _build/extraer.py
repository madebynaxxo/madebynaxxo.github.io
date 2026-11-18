# -*- coding: utf-8 -*-
"""Lee las tarjetas que hay hoy en las paginas de seccion y guarda _build/proyectos.json.
Solo se ejecuta una vez: a partir de ahi la fuente de verdad es el JSON."""
import re, json, io, os

SLUGS = {
 "identidad": ["yahba","kala","dandelion","j1-advertising-team","la-canada","mamamoo","crew-coffee"],
 "social":    ["fine-line-social","gif-dia-de-la-madre"],
 "creativo":  ["vale-madre","fine-line-catalogo","toltecayotl","ayers","copy-de-poster",
               "buddystay","vizabridge","jobbridgekorea"],
}
PAGES = [("es","identidad.html","identidad"),("es","social.html","social"),("es","creativo.html","creativo"),
         ("en","en/identity.html","identidad"),("en","en/social.html","social"),("en","en/creative.html","creativo")]

# imagenes que existen en el repo y que la tarjeta no estaba mostrando
EXTRA = {
 "crew-coffee": ["crew 1.png","crew 2.png","crew 3.png","crew 4.png","crew 5.png","crew 6.png","crew 7.png"],
 "jobbridgekorea": ["jbk mock up ig.png"],
}

card_re = re.compile(r'<div class="card([^"]*)">(.*?)\n    </div>', re.S)
def grab(pat, s, d=""):
    m = re.search(pat, s, re.S); return m.group(1).strip() if m else d
def norm(p):  # toda ruta queda relativa a la raiz del sitio
    return re.sub(r'^(\.\./)+', '', p)
def enc(p):
    return p.replace(" ", "%20")
def plain(h):
    return re.sub(r'\s+',' ', re.sub(r'<[^>]+>','',h)).strip()

def teaser(body, limit=135):
    t = plain(body)
    out = ""
    for part in re.split(r'(?<=[.!?])\s+', t):
        if out and len(out)+len(part)+1 > limit: break
        out = (out+" "+part).strip()
        if len(out) >= 70: break
    return out if out else t[:limit]

data = {}
for lang, path, section in PAGES:
    html = io.open(path, encoding="utf-8").read()
    body = html.split('<div class="band">',1)[1]
    i = 0
    for cls, c in card_re.findall(body):
        title = grab(r'<div class="c-title">(.*?)</div>', c)
        if not title: continue
        slug = SLUGS[section][i]; i += 1
        raw_pills = re.findall(r'<span class="mpill">(.*?)</span>', c, re.S)
        pills, links = [], []
        for p in raw_pills:
            a = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>', p, re.S)
            if a: links.append({"href": norm(a.group(1)), "label": plain(a.group(2))})
            else: pills.append(plain(p))
        gal = [{"src": norm(s), "alt": al}
               for s, al in re.findall(r'<a href="([^"]+)"[^>]*><img src="[^"]+" alt="([^"]*)"', c)]
        hero = norm(grab(r'<div class="c-ph[^"]*"[^>]*><img src="([^"]+)"', c))
        seen = {hero} | {g["src"] for g in gal}
        for x in EXTRA.get(slug, []):
            s = "images/"+enc(x)
            if s not in seen: gal.append({"src": s, "alt": title}); seen.add(s)
        yr = grab(r'<span class="c-yr">(.*?)</span>', c)
        rec = {
          "slug": slug, "section": section, "fit": "c-ph fit" in c,
          "hero": hero, "heroalt": grab(r'<div class="c-ph[^"]*"[^>]*><img src="[^"]+" alt="([^"]*)"', c),
          "year": (re.findall(r'(19|20)\d{2}', yr) and re.search(r'((?:19|20)\d{2})', yr).group(1)) or "",
          "tag": grab(r'<span class="c-tag">(.*?)</span>', c),
          "meta": yr, "title": title,
          "body": grab(r'<p class="c-body">(.*?)</p>', c),
          "pills": pills, "links": links, "gallery": gal,
        }
        rec["teaser"] = teaser(rec["body"])
        data.setdefault(slug, {})[lang] = rec

os.makedirs("_build", exist_ok=True)
json.dump(data, io.open("_build/proyectos.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(data)} proyectos\n")
for s, v in data.items():
    e = v["es"]
    print(f"  {s:22} {e['section']:10} {e['year'] or '----'}  imgs={1+len(e['gallery']):2}  idiomas={''.join(sorted(v))}")
