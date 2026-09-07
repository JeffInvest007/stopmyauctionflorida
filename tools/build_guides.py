#!/usr/bin/env python3
"""Builds the situation guide pages for stopmyauctionflorida.com from the homepage's own
CSS, nav, footer, form and scripts, so every guide is visually identical to index.html.
Run from the repo root:  python3 tools/build_guides.py
"""
import re, json, html, pathlib, importlib.util, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")

def between(start, end, text=SRC):
    i = text.index(start); j = text.index(end, i) + len(end)
    return text[i:j]

# ---------- pieces lifted verbatim from index.html ----------
CSS        = between("<style>", "</style>")
FONTS      = between('<link rel="preload" as="font"', 'inter-var.woff2" />')
GTAG       = between('<!-- Google tag (gtag.js) -->', "gtag('config','G-7VK9SGKW97');</script>")
TRACK      = between('<!-- Lead event tracking:', "</script>")
NAV        = between('<header class="nav">', "</header>")
NAV        = re.sub(r'\s*<div class="langsel".*?</div>', '', NAV, flags=re.S)   # guides are English-only
NAV        = NAV.replace('href="#top"', 'href="index.html"')
SPARKS     = "\n".join(l for l in between('<section class="hero" id="top" style="padding:0">', '<div class="hero-grid wrap">').splitlines() if 'class="spark' in l)
MEET       = between('<section class="meet reveal">', "</section>")
CTA        = between('<section class="cta" id="offer">', "</section>")
FOOTER     = between('<footer class="site">', "</footer>")
ACTIONBAR  = between('<nav class="actionbar"', "</nav>")
SCRIPTS    = between("<script>\n  // current year", "</script>")
NOSCRIPT   = between("<noscript>", "</noscript>")

EXTRA_CSS = """
  /* ===================== GUIDE PAGES ===================== */
  .guide{padding:72px 0 60px}
  .guide-grid{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:56px;align-items:start}
  .prose{max-width:720px;font-size:1.08rem;line-height:1.75;color:var(--ink)}
  .prose h2{font-size:clamp(1.6rem,2.8vw,2.05rem);color:var(--green);margin:46px 0 14px}
  .prose h2:first-child{margin-top:0}
  .prose h3{font-size:1.22rem;color:var(--green);margin:28px 0 10px}
  .prose p{margin:0 0 18px}
  .prose ul,.prose ol{margin:0 0 20px 1.3em}
  .prose li{margin-bottom:9px}
  .prose li::marker{color:var(--gold);font-weight:700}
  .prose a{color:var(--terra);font-weight:600;text-decoration:underline;text-decoration-color:rgba(188,74,46,.35);text-underline-offset:3px}
  .prose a:hover{text-decoration-color:var(--terra)}
  .prose strong{color:var(--green-700)}
  .callout{background:var(--sand);border-left:4px solid var(--gold);border-radius:12px;padding:18px 22px;margin:26px 0;color:var(--green-700)}
  .callout strong{display:block;font-family:'Fraunces';font-size:1.08rem;margin-bottom:4px;color:var(--green)}
  .callout p{margin:0;font-size:1rem}
  .callout.warn{background:#FBEFEA;border-left-color:var(--terra)}
  .callout.warn strong{color:var(--terra-700)}
  .keyfacts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:30px 0 34px}
  .keyfact{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius-sm);padding:18px 18px 16px;box-shadow:var(--shadow-sm)}
  .keyfact b{display:block;font-family:'Fraunces';font-weight:700;font-size:1.65rem;color:var(--terra);line-height:1.1;margin-bottom:6px}
  .keyfact span{font-size:.9rem;color:var(--muted);line-height:1.4;display:block}
  @media(max-width:640px){.keyfacts{grid-template-columns:1fr 1fr}}
  .week{counter-reset:wk;list-style:none;margin:8px 0 26px 0 !important;padding:0}
  .week li{counter-increment:wk;position:relative;padding:14px 16px 14px 62px;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius-sm);margin-bottom:10px;box-shadow:var(--shadow-sm);font-size:1rem}
  .week li::before{content:counter(wk);position:absolute;left:16px;top:12px;width:32px;height:32px;border-radius:50%;background:var(--green);color:var(--gold-soft);font-family:'Fraunces';font-weight:700;display:grid;place-items:center;font-size:1rem}
  .week li b{color:var(--green)}
  .rail{position:sticky;top:96px;display:grid;gap:18px}
  .rail-card{background:linear-gradient(160deg,var(--green-900),var(--green));color:#EAF1ED;border-radius:var(--radius);padding:28px 26px;box-shadow:var(--shadow)}
  .rail-card h3{color:#fff;font-size:1.35rem;margin:8px 0 8px}
  .rail-card p{color:#C9D6CE;font-size:.96rem;margin-bottom:18px}
  .rail-card .btn{width:100%;margin-bottom:10px}
  .rail-card .btn-outline-light{border-color:rgba(255,255,255,.45)}
  .rail-card small{display:block;color:#9FB6AD;font-size:.82rem;margin-top:6px;text-align:center}
  .rail-links{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:22px 24px;box-shadow:var(--shadow-sm)}
  .rail-links h4{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-family:'Inter';font-weight:700;margin-bottom:12px}
  .rail-links a{display:block;padding:10px 0;border-top:1px solid var(--line);font-weight:600;color:var(--green);font-size:.96rem;transition:color .15s ease,padding-left .15s ease}
  .rail-links a:hover{color:var(--terra);padding-left:6px}
  @media(max-width:980px){.guide-grid{grid-template-columns:1fr;gap:34px}.rail{position:static}.prose{max-width:none}}
"""
CSS = CSS.replace("</style>", EXTRA_CSS + "</style>")

GUIDES = [
  dict(slug="sell-before-foreclosure-auction-florida.html", tag="Mortgage foreclosure",
       card="Sell before the foreclosure auction", blurb="A judge set your sale date. Here is how the last few weeks work in Florida, and how to walk away with cash instead of nothing."),
  dict(slug="tax-deed-sale-florida.html", tag="Tax deed sale",
       card="Behind on property taxes", blurb="Tax certificate, tax deed application, clerk's sale. What each notice means and how to redeem or sell before the county auctions your home."),
  dict(slug="inherited-house-foreclosure-florida.html", tag="Probate and inherited property",
       card="Inherited a house with a sale date", blurb="A parent's home, a mortgage nobody is paying, taxes piling up. How heirs sell a house that is still in probate before it is lost."),
  dict(slug="miami-dade-broward-foreclosure-help.html", tag="South Florida",
       card="Miami-Dade and Broward help", blurb="Where the sales happen, how to find your date, and why a buyer ten minutes away matters when the clock is short."),
]

def guide_cards(exclude_slug):
    out = []
    for g in GUIDES:
        if g["slug"] == exclude_slug: continue
        out.append(f'''      <a class="guide-card reveal" href="{g['slug']}">
        <span class="tag">{g['tag']}</span>
        <h3>{g['card']}</h3>
        <p>{g['blurb']}</p>
        <span class="more">Read the guide <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="M13 6l6 6-6 6"/></svg></span>
      </a>''')
    return "\n".join(out)

def rail_links(exclude_slug):
    out = []
    for g in GUIDES:
        if g["slug"] == exclude_slug: continue
        out.append(f'      <a href="{g["slug"]}">{g["card"]}</a>')
    out.append('      <a href="index.html">Back to the homepage</a>')
    return "\n".join(out)

CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#E7C77E" stroke-width="2.4"><path d="M20 6L9 17l-5-5"/></svg>'

def faq_html(faqs):
    return "\n".join(
        f'      <details class="faq reveal"><summary>{html.escape(q)} <span class="plus">+</span></summary><div class="ans">{a}</div></details>'
        for q, a in faqs)

def faq_schema(faqs):
    ents = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r"<[^>]+>","",a)}} for q,a in faqs]
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":ents}, ensure_ascii=False, indent=1)

def article_schema(p):
    d = {"@context":"https://schema.org","@type":"Article","headline":p["h1_plain"],"description":p["meta"],
         "inLanguage":"en-US","url":f"https://stopmyauctionflorida.com/{p['slug']}",
         "mainEntityOfPage":f"https://stopmyauctionflorida.com/{p['slug']}",
         "image":f"https://stopmyauctionflorida.com/{p['hero_img']}",
         "author":{"@type":"Person","name":"Coach Jeff","jobTitle":"Founder, Stop My Auction Florida"},
         "publisher":{"@type":"Organization","name":"Probate Assets Elite, LLC","logo":{"@type":"ImageObject","url":"https://stopmyauctionflorida.com/assets/logo.png"}},
         "about":{"@type":"Thing","name":p["about"]},"areaServed":{"@type":"State","name":"Florida"}}
    return json.dumps(d, ensure_ascii=False, indent=1)

def build(p):
    cta = CTA
    # pre-select the matching situation and stamp the page into the lead so Jeff knows which guide produced it
    cta = cta.replace(f'<option>{p["situation"]}</option>', f'<option selected>{p["situation"]}</option>')
    cta = cta.replace('value="direct visit"', f'value="{p["lead_source"]}"')
    cta = cta.replace('value="NEW AUCTION LEAD - stopmyauctionflorida.com"', f'value="NEW AUCTION LEAD - {p["lead_source"]}"')
    footer = FOOTER.replace('href="#how-time"', 'href="index.html#how-time"').replace('href="#top"', 'href="index.html"')
    page = f"""<!DOCTYPE html>
<!--
  Stop My Auction Florida  |  stopmyauctionflorida.com
  Probate Assets Elite, LLC  |  (786) 920-7419
  Situation guide: {p['h1_plain']}
  Built from the homepage template by tools/build_guides.py. Edit the content in tools/guide_*.py, not here.
-->
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(p['title'])}</title>
<meta name="description" content="{html.escape(p['meta'])}" />
<link rel="canonical" href="https://stopmyauctionflorida.com/{p['slug']}" />
<meta name="theme-color" content="#123F38" />

{GTAG}

<!-- Social preview -->
<meta property="og:type" content="article" />
<meta property="og:url" content="https://stopmyauctionflorida.com/{p['slug']}" />
<meta property="og:site_name" content="Stop My Auction Florida" />
<meta property="og:title" content="{html.escape(p['og_title'])}" />
<meta property="og:description" content="{html.escape(p['meta'])}" />
<meta property="og:image" content="https://stopmyauctionflorida.com/assets/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:locale" content="en_US" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{html.escape(p['og_title'])}" />
<meta name="twitter:description" content="{html.escape(p['meta'])}" />
<meta name="twitter:image" content="https://stopmyauctionflorida.com/assets/og-image.jpg" />

<!-- Icons -->
<link rel="icon" href="/favicon.ico" sizes="48x48" />
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />

<link rel="preload" as="image" href="{p['hero_img']}" />
{FONTS}

{CSS}
{NOSCRIPT}

<script type="application/ld+json">
{article_schema(p)}
</script>
<script type="application/ld+json">
{faq_schema(p['faqs'])}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Stop My Auction Florida","item":"https://stopmyauctionflorida.com/"}},
 {{"@type":"ListItem","position":2,"name":"{html.escape(p['crumb'])}","item":"https://stopmyauctionflorida.com/{p['slug']}"}}]}}
</script>
{TRACK}
</head>
<body>

<!-- ===================== NAV ===================== -->
{NAV}

<!-- ===================== HERO ===================== -->
<section class="hero" id="top" style="padding:0">
{SPARKS}
  <div class="hero-grid wrap">
    <div class="reveal in">
      <span class="eyebrow">{p['eyebrow']}</span>
      <h1>{p['h1']}</h1>
      <p class="lede">{p['lede']}</p>
      <div class="hero-promise">
        <span class="hp-icon"><svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 15h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 17"/><path d="m7 21 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 16 6 6"/><circle cx="16" cy="9" r="2.9"/></svg></span>
        <p><strong>{p['promise_lead']}</strong> {p['promise']}</p>
      </div>
      <div class="hero-cta">
        <a href="#offer" class="btn btn-primary">Get My Free Cash Offer</a>
        <a href="tel:+17869207419" class="btn btn-outline-light">Call (786) 920-7419</a>
        <a href="sms:+17869207419?body={p['sms']}" class="btn btn-outline-light">Text Us</a>
      </div>
      <div class="hero-trust">
        <div>{CHECK} {p['trust'][0]}</div>
        <div>{CHECK} {p['trust'][1]}</div>
        <div>{CHECK} No fees, no repairs, no commissions</div>
        <div>{CHECK} Nou pale krey&ograve;l &middot; Hablamos espa&ntilde;ol</div>
      </div>
    </div>
    <div class="hero-photo reveal in" style="overflow:visible">
      <span class="ribbon" style="z-index:3">{p['ribbon']}</span>
      <span style="position:absolute;inset:0;overflow:hidden;border-radius:var(--radius);z-index:1"><img src="{p['hero_img']}" alt="{html.escape(p['hero_alt'])}" width="{p['hero_w']}" height="{p['hero_h']}" fetchpriority="high" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{p.get('hero_pos','center')};{p.get('hero_zoom','')}"></span>
      <span class="gavel-badge" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/><path d="m16 16 6-6"/><path d="m8 8 6-6"/><path d="m9 7 8 8"/><path d="m21 11-8-8"/></svg></span>
    </div>
  </div>
</section>

<!-- ===================== URGENCY BAND ===================== -->
<div class="urgency">
  <div class="wrap">
    <span class="pill">{p['urgency_pill']}</span>
    <strong>{p['urgency']}</strong>
    <span>{p['urgency_sub']}</span>
  </div>
</div>

<!-- ===================== GUIDE ===================== -->
<section class="guide">
  <div class="wrap guide-grid">
    <article class="prose reveal">
{p['body']}
    </article>
    <aside class="rail">
      <div class="rail-card reveal">
        <span class="eyebrow" style="color:var(--gold-soft)">Talk to a real person</span>
        <h3>Call or text Coach Jeff</h3>
        <p>{p['rail_text']}</p>
        <a href="tel:+17869207419" class="btn btn-primary">Call (786) 920-7419</a>
        <a href="sms:+17869207419?body={p['sms']}" class="btn btn-outline-light">Text (786) 920-7419</a>
        <a href="https://wa.me/17869207419?text={p['sms']}" target="_blank" rel="noopener" class="btn btn-outline-light">WhatsApp</a>
        <small>An answer in less than 24 hours. No fees, ever.</small>
      </div>
      <div class="rail-links reveal">
        <h4>Other situations</h4>
{rail_links(p['slug'])}
      </div>
    </aside>
  </div>
</section>

<!-- ===================== MEET COACH JEFF ===================== -->
{MEET}

<!-- ===================== FAQ ===================== -->
<section>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Straight answers</span>
      <h2>{p['faq_title']}</h2>
    </div>
    <div class="faq-wrap">
{faq_html(p['faqs'])}
    </div>
  </div>
</section>

<!-- ===================== MORE GUIDES ===================== -->
<section class="guides">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Help by situation</span>
      <h2>Not quite your situation?</h2>
      <p>Every auction has its own clock. Pick the guide that matches yours.</p>
    </div>
    <div class="guide-cards">
{guide_cards(p['slug'])}
    </div>
  </div>
</section>

<!-- ===================== CTA / FORM ===================== -->
{cta}

<!-- ===================== FOOTER ===================== -->
{footer}

<!-- Mobile quick-action bar: on phones, call and offer are always one thumb away -->
{ACTIONBAR}

{SCRIPTS}
</body>
</html>
"""
    return page

if __name__ == "__main__":
    tools = ROOT / "tools"
    built = []
    for f in sorted(tools.glob("guide_*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        p = m.PAGE
        out = ROOT / p["slug"]
        out.write_text(build(p), encoding="utf-8")
        words = len(re.sub(r"<[^>]+>", " ", p["body"]).split())
        built.append((p["slug"], words, len(p["title"]), len(p["meta"])))
    for b in built: print("built %-48s body words=%4d title=%2d chars meta=%3d chars" % b)
