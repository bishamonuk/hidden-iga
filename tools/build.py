"""Build the English site (site/index.html + site/homes/<no>/index.html) from data/homes.py.
Run: python3 tools/build.py
"""
import html
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data"))
from homes import HOMES, EUR_RATE, FEE_RATE  # noqa: E402

SITE = ROOT / "site"
BRAND = "Iga Akiya"            # 【要確認】working name
OPERATOR = "[TBC: operating company]"   # 【要確認】
EMAIL = "hello@example.com"   # 【要確認】placeholder
SOURCE = "https://iga-akiyabank.com/bukken/detail.php?no="
AREA = {"rural": ("Rural farmland", "農村部"), "mountain": ("Mountain foothills", "山間部")}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&family=Inter:wght@400;500;600&display=swap">')
e = html.escape


def yen(man):
    return f"¥{man * 10000:,}"


def eur(man):
    v = man * 10000 / EUR_RATE
    return f"€{round(v, -2):,.0f}"


def fee(man):
    return man * FEE_RATE


def img(no, k):
    return f"img/homes/{no}-{k:02d}.jpg"


def head(title, desc, pre):
    return f'''<!doctype html>
<html lang="en-GB" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#F3EEE5">
  {FONTS}
  <link rel="stylesheet" href="{pre}css/style.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="hd">
    <div class="wrap hd-in">
      <a class="logo" href="{pre}index.html"><span class="logo-mark" aria-hidden="true">伊</span><span>{BRAND}</span></a>
      <nav class="nav" id="nav" aria-label="Main">
        <a href="{pre}index.html#homes">Homes</a>
        <a href="{pre}index.html#iga">Why Iga</a>
        <a href="{pre}index.html#how">How it works</a>
        <a href="{pre}index.html#fees">Fees</a>
        <a href="{pre}index.html#faq">FAQ</a>
        <a class="btn btn-ink" href="{pre}index.html#contact">Enquire</a>
      </nav>
      <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span><span></span></button>
    </div>
  </header>
'''


def foot(pre):
    return f'''
  <footer class="ft">
    <div class="wrap ft-in">
      <div>
        <a class="logo" href="{pre}index.html"><span class="logo-mark" aria-hidden="true">伊</span><span>{BRAND}</span></a>
        <p>Country homes in Iga, Japan — explained in English, for buyers in Europe.</p>
      </div>
      <div class="ft-small">
        <p>Listing information is taken from the Iga City Akiya Bank (伊賀流空き家バンク), run by Iga City Hall. Details can change — always check the original listing.</p>
        <p>Operated by {OPERATOR}.</p>
        <p class="tbc">【要確認】Draft for review — not yet published.</p>
      </div>
    </div>
  </footer>
  <script src="{pre}js/main.js"></script>
</body>
</html>
'''


def card(h, pre=""):
    a_en, a_ja = AREA[h["area"]]
    tags = "".join(f"<li>{e(t)}</li>" for t in h["tags"][:3])
    return f'''
        <li class="card rv" data-area="{h['area']}" data-price="{h['price']}">
          <a href="{pre}homes/{h['no']}/index.html">
            <div class="card-img"><img src="{pre}{img(h['no'],1)}" alt="" loading="lazy"><span class="card-area">{a_en}</span></div>
            <div class="card-body">
              <p class="card-place">{e(h['place'])}, Iga <span>No. {h['no']}</span></p>
              <h3>{e(h['title'])}</h3>
              <ul class="card-facts"><li>{h['layout']}</li><li>{h['floor']:,.0f} m² house</li><li>{h['land']:,.0f} m² land</li></ul>
              <ul class="card-tags">{tags}</ul>
              <p class="card-price"><strong>{yen(h['price'])}</strong><span>≈ {eur(h['price'])}</span></p>
            </div>
          </a>
        </li>'''


def index():
    homes = sorted(HOMES, key=lambda h: h["price"])
    cards = "".join(card(h) for h in homes)
    n_r = sum(h["area"] == "rural" for h in HOMES)
    n_m = sum(h["area"] == "mountain" for h in HOMES)
    lo, hi = homes[0]["price"], homes[-1]["price"]
    ex = 500
    return head(f"{BRAND} — Country houses for sale in Iga, Japan",
                "Traditional country houses (kominka) for sale in the rural and mountain areas of Iga, Japan. Explained in English, with support for buyers in Europe.", "") + f'''
  <main id="main">
    <section class="hero">
      <div class="hero-img"><img src="{img(614,1)}" alt="A traditional country house in Kōno, Iga"></div>
      <div class="wrap hero-in">
        <p class="kicker">Iga · Mie Prefecture · Japan</p>
        <h1>A house in the Japanese countryside,<br><em>from {yen(lo)}.</em></h1>
        <p class="lead">Old farmhouses with gardens, fields and storehouses, in the rice-growing valleys and wooded hills of Iga. We bring the listings of the Iga City Akiya Bank into English, and help buyers in Europe through every step — from the first viewing to the keys.</p>
        <div class="hero-cta"><a class="btn btn-ink" href="#homes">See the {len(HOMES)} homes</a><a class="btn btn-line" href="#how">How buying works</a></div>
      </div>
    </section>

    <section class="strip">
      <div class="wrap strip-in">
        <div><strong>{len(HOMES)}</strong><span>homes for sale</span></div>
        <div><strong>{yen(lo)}–{yen(hi)}</strong><span>asking prices</span></div>
        <div><strong>{n_r} · {n_m}</strong><span>rural · mountain</span></div>
        <div><strong>{FEE_RATE*100:.0f}%</strong><span>buyer support fee</span></div>
      </div>
    </section>

    <section class="sec" id="homes">
      <div class="wrap">
        <div class="sec-head">
          <div><p class="kicker">The homes</p><h2>Country houses for sale <em>in Iga</em></h2></div>
          <p>All listings come from the Iga City Akiya Bank (vacant house bank) and are in the city's rural and mountain areas. Prices are the sellers' asking prices.</p>
        </div>
        <div class="filters" role="group" aria-label="Filter homes">
          <div class="seg" data-filter="area">
            <button type="button" class="on" data-v="all">All <span>{len(HOMES)}</span></button>
            <button type="button" data-v="rural">Rural <span>{n_r}</span></button>
            <button type="button" data-v="mountain">Mountain <span>{n_m}</span></button>
          </div>
          <label class="sort">Sort <select data-sort><option value="asc">Price: low to high</option><option value="desc">Price: high to low</option></select></label>
        </div>
        <ul class="cards">{cards}
        </ul>
        <p class="note">Euro prices are approximate (¥{EUR_RATE} = €1). Kominka = a traditional Japanese house, usually timber-framed and built before the 1980s. Layout codes: “8DK” = 8 rooms plus a dining-kitchen.</p>
      </div>
    </section>

    <section class="sec sec-tint" id="iga">
      <div class="wrap iga-in">
        <div class="iga-img rv"><img src="{img(581,1)}" alt="" loading="lazy"></div>
        <div class="rv">
          <p class="kicker">Why Iga</p>
          <h2>Quiet valleys, <em>close to everything.</em></h2>
          <p>Iga sits in Mie Prefecture, in the hills between Osaka, Kyoto and Nara. It is best known as the home of the Iga ninja and the birthplace of the haiku poet Bashō — and for rice fields, tea, sake and Iga-yaki pottery.</p>
          <p>The rural and mountain districts around the city are full of large old houses that families no longer live in. Iga City runs its own Akiya Bank to find them new owners, and publishes inspection notes, floor plans and video tours for each home.</p>
          <ul class="ticks"><li>Railway lines into Osaka, Nagoya and Kyoto</li><li>Large plots — often with a garden, field or storehouse</li><li>Honest condition notes from the city's own survey</li></ul>
          <p class="tbc">【要確認】Travel times to Osaka / Kyoto / Kansai Airport to be checked before publishing.</p>
        </div>
      </div>
    </section>

    <section class="sec" id="how">
      <div class="wrap">
        <div class="sec-head"><div><p class="kicker">How it works</p><h2>From Europe to <em>your own front door</em></h2></div></div>
        <ol class="steps">
          <li class="rv"><span>01</span><h3>Choose</h3><p>Browse the homes in English. Ask us anything — we translate the full listing, inspection notes and floor plan.</p></li>
          <li class="rv"><span>02</span><h3>Register &amp; view</h3><p>Viewings are booked through the Iga City Akiya Bank, which asks buyers to register first. We prepare the registration with you and arrange a viewing — in person or by video.</p></li>
          <li class="rv"><span>03</span><h3>Offer &amp; contract</h3><p>The sale is handled by a licensed Japanese real estate agent. We interpret, explain every document in English, and coordinate with the agent and the seller.</p></li>
          <li class="rv"><span>04</span><h3>Pay &amp; register</h3><p>We guide you through the international payment, the judicial scrivener who registers your title, and the taxes due on purchase.</p></li>
          <li class="rv"><span>05</span><h3>Move in</h3><p>Keys, utilities, local contractors for repairs and renovation, and help settling into the community.</p></li>
        </ol>
      </div>
    </section>

    <section class="sec sec-ink" id="fees">
      <div class="wrap fees-in">
        <div class="rv">
          <p class="kicker">Fees</p>
          <h2>One clear fee: <em>{FEE_RATE*100:.0f}% of the price.</em></h2>
          <p>Our buyer support fee is {FEE_RATE*100:.0f}% of the purchase price, payable on completion. It covers English support from your first enquiry to moving in.</p>
          <p class="small">Other costs paid directly by the buyer: the licensed agent's brokerage fee (capped by Japanese law), registration and scrivener fees, real estate acquisition tax, stamp duty and fixed asset tax. We give you an estimate before you make an offer.</p>
          <p class="tbc">【要確認】Fee structure and wording to be confirmed by a Japanese real-estate specialist before publishing (see brief).</p>
        </div>
        <div class="calc rv" data-rate="{EUR_RATE}" data-fee="{FEE_RATE}">
          <label for="calc-price">Example: house price (¥)</label>
          <input id="calc-price" type="range" min="1000000" max="20000000" step="100000" value="{ex*10000}">
          <dl>
            <div><dt>House price</dt><dd data-o="price">{yen(ex)}</dd></div>
            <div><dt>Buyer support fee ({FEE_RATE*100:.0f}%)</dt><dd data-o="fee">{yen(int(fee(ex)))}</dd></div>
            <div class="total"><dt>Total</dt><dd data-o="total">{yen(int(ex + fee(ex)))}</dd></div>
            <div class="eur"><dt>≈ in euros</dt><dd data-o="eur">{eur(ex + fee(ex))}</dd></div>
          </dl>
        </div>
      </div>
    </section>

    <section class="sec" id="faq">
      <div class="wrap faq-in">
        <div><p class="kicker">FAQ</p><h2>Good <em>questions</em></h2></div>
        <div class="faq">
          <details class="rv"><summary>Can a foreigner buy a house in Japan?</summary><p>Yes. Japan does not restrict foreign nationals or non-residents from owning residential property, and you do not need a visa to buy. Owning a house does not give you the right to live in Japan — residence depends on your visa. 【要確認】</p></details>
          <details class="rv"><summary>Can I buy the fields that come with a house?</summary><p>Farmland is different. Buying or transferring it needs permission under Japan's Agricultural Land Act, which is usually given only to people who will farm it. Several listings note this — we check each case with the city and the agent.</p></details>
          <details class="rv"><summary>What condition are the houses in?</summary><p>Many are old and need work — the city lists every known issue, from roof leaks to unusable toilets. We translate these notes in full, and can arrange an inspection and renovation quotes before you commit.</p></details>
          <details class="rv"><summary>Do I need to travel to Japan?</summary><p>We recommend at least one visit. Viewings can start by video, and much of the paperwork can be done remotely, but signing and payment may need you or a representative in Japan.</p></details>
          <details class="rv"><summary>Who is the seller?</summary><p>Private owners. The Iga City Akiya Bank publishes the homes, and a licensed real estate agent handles each sale. We are your English-speaking guide through the process.</p></details>
        </div>
      </div>
    </section>

    <section class="sec sec-tint" id="contact">
      <div class="wrap contact-in rv">
        <p class="kicker">Enquire</p>
        <h2>Tell us which home <em>caught your eye.</em></h2>
        <p>Send us the listing number and a few lines about your plans. We reply in English within two working days. 【要確認】</p>
        <a class="btn btn-ink" href="mailto:{EMAIL}?subject=Enquiry%20about%20a%20home%20in%20Iga">Email us</a>
      </div>
    </section>
  </main>
''' + foot("")


def detail(h):
    pre = "../../"
    a_en, a_ja = AREA[h["area"]]
    n = h["photos"]
    thumbs = "".join(f'<button type="button" data-src="{pre}{img(h["no"],k)}"{" class=on" if k==1 else ""}><img src="{pre}{img(h["no"],k)}" alt="Photo {k}" loading="lazy"></button>' for k in range(1, n + 1))
    plan = f'<figure class="plan"><img src="{pre}img/homes/{h["no"]}-plan.jpg" alt="Floor plan (Japanese)" loading="lazy"><figcaption>Floor plan (in Japanese — we translate it on request)</figcaption></figure>'
    video = f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{h["video"]}" title="Video tour of No. {h["no"]}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>' if h["video"] else ""
    rows = [("Location", f'{h["place"]}, Iga, Mie <span class="ja">{h["place_ja"]}</span>'), ("Area", f"{a_en} <span class='ja'>{a_ja}エリア</span>"),
            ("Layout", h["layout"]), ("Structure", h["structure"]), ("Built", h["built"]),
            ("Land", f'{h["land"]:,.2f} m²'), ("Floor area", f'{h["floor"]:,.2f} m²'),
            ("Water", h["water"]), ("Drainage", h["drainage"]), ("Toilet", h["toilet"]), ("Bath", h["bath"]), ("Gas", h["gas"]),
            ("Access", h["access"]), ("Schools", h["schools"]), ("Shops", h["shops"]), ("Other", h["notes"])]
    table = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    others = [x for x in sorted(HOMES, key=lambda x: abs(x["price"] - h["price"])) if x["no"] != h["no"]][:3]
    more = "".join(card(x, pre) for x in others)
    total = h["price"] + fee(h["price"])
    return head(f"{h['title']} — {h['place']}, Iga | {BRAND}", f"{h['layout']} house for sale in {h['place']}, Iga, Japan. {yen(h['price'])}.", pre) + f'''
  <main id="main" class="detail">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="{pre}index.html#homes">Homes</a> / <span>No. {h['no']}</span></nav>
      <div class="d-head">
        <div>
          <p class="kicker">{a_en} · {e(h['place'])}, Iga</p>
          <h1>{e(h['title'])}</h1>
          <ul class="card-tags">{"".join(f"<li>{e(t)}</li>" for t in h["tags"])}</ul>
        </div>
        <div class="d-price"><strong>{yen(h['price'])}</strong><span>≈ {eur(h['price'])}</span></div>
      </div>
      <div class="gallery">
        <div class="g-main"><img src="{pre}{img(h['no'],1)}" alt="Photo of the house"></div>
        {f'<div class="g-thumbs">{thumbs}</div>' if n > 1 else ''}
      </div>
      <div class="d-grid">
        <div>
          <section class="d-sec"><h2>Condition</h2><p class="cond">{e(h['condition'])}</p><p class="small">From the Iga City Akiya Bank survey. We translate the full inspection notes on request.</p></section>
          <section class="d-sec"><h2>Key facts</h2><dl class="facts">{table}</dl></section>
          {f'<section class="d-sec"><h2>Video tour</h2>{video}</section>' if video else ''}
          <section class="d-sec"><h2>Floor plan</h2>{plan}</section>
          <section class="d-sec"><h2>Location</h2><p class="small">The exact address is shared after registration — the map shows the district.</p><div class="map"><iframe title="Map of {e(h['place'])}, Iga" src="https://www.google.com/maps?q={h['lat']},{h['lng']}&amp;z=13&amp;output=embed" loading="lazy"></iframe></div></section>
        </div>
        <aside class="d-side">
          <div class="side-box">
            <p class="kicker">No. {h['no']}</p>
            <dl>
              <div><dt>Asking price</dt><dd>{yen(h['price'])}</dd></div>
              <div><dt>Buyer support fee ({FEE_RATE*100:.0f}%)</dt><dd>{yen(int(fee(h['price'])))}</dd></div>
              <div class="total"><dt>Total</dt><dd>{yen(int(total))}</dd></div>
              <div class="eur"><dt>≈ in euros</dt><dd>{eur(total)}</dd></div>
            </dl>
            <p class="small">Plus the agent's fee, taxes and registration costs. 【要確認】</p>
            <a class="btn btn-ink" href="mailto:{EMAIL}?subject=Home%20No.%20{h['no']}%20({h['place']})">Enquire about this home</a>
            <a class="src" href="{SOURCE}{h['no']}" rel="noopener" target="_blank">Original listing (Japanese) ↗</a>
          </div>
        </aside>
      </div>
      <section class="d-more"><h2>Similar homes</h2><ul class="cards">{more}</ul></section>
    </div>
  </main>
''' + foot(pre)


if __name__ == "__main__":
    (SITE / "index.html").write_text(index(), encoding="utf-8")
    for h in HOMES:
        d = SITE / "homes" / str(h["no"])
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(detail(h), encoding="utf-8")
    print("built", 1 + len(HOMES), "pages")
