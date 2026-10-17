"""日本語サイト（site/ja/index.html と site/ja/homes/<番号>/index.html）を生成する。
文言はこのファイル、物件の日本語情報は data/homes_ja.py。
実行: python3 tools/build_ja.py （英語版は tools/build.py）
"""
import html
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data"))
sys.path.insert(0, str(ROOT / "tools"))
from homes import HOMES, FEE_RATE  # noqa: E402
from homes_ja import JA  # noqa: E402
from build import MARK, EMAIL, SOURCE, img, fee  # noqa: E402

SITE = ROOT / "site"
OUT = SITE / "ja"
BRAND = "Hidden Iga"
PARTNER = "伊賀市公認パートナー"   # 【要確認】伊賀市との協定・登録の正式名称に合わせる
OPERATOR = "【要確認：運営会社名】"
AREA = {"rural": "農村部エリア", "mountain": "山間部エリア"}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=Shippori+Mincho:wght@500;600&family=Noto+Sans+JP:wght@400;500;700&display=swap">')
e = html.escape


def man(v):
    """万円表記（例：250万円、1,680万円）"""
    return f"{v:,}万円"


def head(title, desc, pre, alt):
    return f'''<!doctype html>
<html lang="ja" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#F3EEE5">
  {FONTS}
  <link rel="icon" href="{pre}img/brand/{MARK}" type="image/svg+xml">
  <link rel="stylesheet" href="{pre}css/style.css">
</head>
<body>
  <a class="skip" href="#main">本文へスキップ</a>
  <header class="hd">
    <div class="wrap hd-in">
      <a class="logo" href="{pre}ja/index.html"><img class="logo-mark" src="{pre}img/brand/{MARK}" alt="" width="36" height="36"><span class="logo-wm">Hidden <em>Iga</em></span></a>
      <nav class="nav" id="nav" aria-label="メニュー">
        <a href="{pre}ja/index.html#homes">物件一覧</a>
        <a href="{pre}ja/index.html#iga">伊賀について</a>
        <a href="{pre}ja/index.html#how">購入の流れ</a>
        <a href="{pre}ja/index.html#care">管理サービス</a>
        <a href="{pre}ja/index.html#faq">よくある質問</a>
        <a class="lang-link" href="{alt}" hreflang="en" lang="en">English</a>
        <a class="btn btn-ink" href="{pre}ja/index.html#contact">お問い合わせ</a>
      </nav>
      <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="メニューを開く"><span></span><span></span></button>
    </div>
  </header>
'''


def foot(pre):
    return f'''
  <footer class="ft">
    <div class="wrap ft-in">
      <div>
        <a class="logo" href="{pre}ja/index.html"><img class="logo-mark" src="{pre}img/brand/{MARK}" alt="" width="36" height="36"><span class="logo-wm">Hidden <em>Iga</em></span></a>
        <p>忍者の里・伊賀の、田舎の家。日本の田舎に、あなただけの隠れ家を。</p>
      </div>
      <div class="ft-small">
        <p>物件情報は、伊賀市役所が運営する「伊賀流空き家バンク」の掲載内容をもとにしています。{BRAND} は伊賀市のバックアップを受けた正式なエージェントとして活動しています。【要確認】 掲載内容は変わることがあります。最新の情報は元の掲載ページでご確認ください。</p>
        <p>運営：{OPERATOR}</p>
        <p class="tbc">【要確認】確認用の下書きです（未公開）。</p>
      </div>
    </div>
  </footer>
  <script src="{pre}js/main.js"></script>
</body>
</html>
'''


def card(h, pre):
    j = JA[h["no"]]
    tags = "".join(f"<li>{e(t)}</li>" for t in j["tags"][:3])
    return f'''
        <li class="card rv" data-area="{h['area']}" data-price="{h['price']}">
          <a href="{pre}ja/homes/{h['no']}/index.html">
            <div class="card-img"><img src="{pre}{img(h['no'],1)}" alt="" loading="lazy"><span class="card-area">{AREA[h['area']]}</span>{'<span class="card-360">360°内覧</span>' if h.get('tour') else ''}</div>
            <div class="card-body">
              <p class="card-place">伊賀市{e(j['place'])} <span>No. {h['no']}</span></p>
              <h3>{e(j['title'])}</h3>
              <ul class="card-facts"><li>{h['layout']}</li><li>建物 {h['floor']:,.0f}㎡</li><li>土地 {h['land']:,.0f}㎡</li></ul>
              <ul class="card-tags">{tags}</ul>
              <p class="card-price"><strong>{man(h['price'])}</strong></p>
            </div>
          </a>
        </li>'''


def index():
    pre = "../"
    homes = sorted(HOMES, key=lambda h: h["price"])
    cards = "".join(card(h, pre) for h in homes)
    n_r = sum(h["area"] == "rural" for h in HOMES)
    n_m = sum(h["area"] == "mountain" for h in HOMES)
    lo, hi = homes[0]["price"], homes[-1]["price"]
    ex = 500
    pct = f"{FEE_RATE*100:.0f}%"
    return head(f"{BRAND}｜日本の田舎に、あなただけの隠れ家を — 伊賀の古民家・空き家",
                "忍者の里・伊賀（三重県）の農村部・山間部にある古民家や田舎の家を紹介。セカンドハウスとして日本の田舎に家を持ちたい方の購入を、内覧から鍵の受け渡し、購入後の管理までサポートします。",
                pre, "../index.html") + f'''
  <main id="main" class="ja">
    <section class="hero">
      <div class="hero-img"><img src="{pre}{img(614,1)}" alt="伊賀市甲野の古民家"></div>
      <div class="wrap hero-in">
        <p class="kicker">忍者の里・伊賀の、田舎の家</p>
        <h1>日本の田舎に、<br><em>あなただけの隠れ家を。</em></h1>
        <p class="lead">田んぼの広がる谷あいや、山に抱かれた集落に残る、庭や畑、蔵のある古い家。{man(lo)}から。週末を過ごす場所に、夏を過ごす家に、ゆっくり暮らすための住まいに。伊賀市の空き家バンクの物件を、最初の内覧から鍵の受け渡しまでご案内します。</p>
        <div class="hero-cta"><a class="btn btn-ink" href="#homes">{len(HOMES)}件の物件を見る</a><a class="btn btn-line" href="#how">購入の流れ</a></div>
        <p class="official"><span class="official-ico" aria-hidden="true">✓</span>{PARTNER} <span>· 伊賀市役所の空き家バンクと連携</span></p>
      </div>
    </section>

    <section class="strip">
      <div class="wrap strip-in">
        <div><strong>{len(HOMES)}件</strong><span>販売中の物件</span></div>
        <div><strong>{lo:,}〜{hi:,}万円</strong><span>売り出し価格</span></div>
        <div><strong>{n_r}件・{n_m}件</strong><span>農村部・山間部</span></div>
        <div><strong>{sum(1 for h in HOMES if h.get('tour'))}件</strong><span>360°内覧つき</span></div>
      </div>
    </section>

    <section class="sec an" id="an">
      <div class="wrap an-in">
        <img class="an-seal rv" src="{pre}img/brand/{MARK}" alt="庵" width="160" height="160">
        <div class="rv">
          <p class="kicker">庵 · いおり</p>
          <h2>隠れ家には、<em>名前がある。</em></h2>
          <p>「庵（いおり）」とは、山里に結ぶ小さな住まいのこと。都会を離れて、休み、読み、お茶を楽しむための隠れ家です。昔から歌人や茶人が庵を持ちました。伊賀が生んだ俳人・松尾芭蕉の名前も、自らの庵「芭蕉庵」に由来します。</p>
          <p>Hidden Iga は、あなたの庵探しをお手伝いします。腰を下ろしたくなる庭、野菜を育てる畑、物語の詰まった蔵。そして、家にまた明かりがともるのを喜んでくれる村があります。</p>
        </div>
      </div>
    </section>

    <section class="sec" id="homes">
      <div class="wrap">
        <div class="sec-head">
          <div><p class="kicker">物件一覧</p><h2>伊賀の、<em>田舎の家。</em></h2></div>
          <p>伊賀市の「伊賀流空き家バンク」に掲載されている、農村部・山間部の売却物件です。価格は売主の売り出し価格です。</p>
        </div>
        <div class="filters" role="group" aria-label="物件の絞り込み">
          <div class="seg" data-filter="area">
            <button type="button" class="on" data-v="all">すべて <span>{len(HOMES)}</span></button>
            <button type="button" data-v="rural">農村部 <span>{n_r}</span></button>
            <button type="button" data-v="mountain">山間部 <span>{n_m}</span></button>
          </div>
          <label class="sort">並び順 <select data-sort><option value="asc">価格の安い順</option><option value="desc">価格の高い順</option></select></label>
        </div>
        <ul class="cards">{cards}
        </ul>
        <p class="note">間取りの「8DK」は、8部屋＋ダイニングキッチンの意味です。</p>
      </div>
    </section>

    <section class="sec sec-tint" id="iga">
      <div class="wrap iga-in">
        <div class="iga-img rv"><img src="{pre}{img(581,1)}" alt="" loading="lazy"></div>
        <div class="rv">
          <p class="kicker">伊賀について</p>
          <h2>静かな谷あい、<em>でも都市に近い。</em></h2>
          <p>伊賀市は三重県の北西部、大阪・京都・奈良に囲まれた山あいのまちです。伊賀忍者の里、俳人・松尾芭蕉のふるさととして知られ、米どころ、お茶、酒、伊賀焼の産地でもあります。</p>
          <p>市の周りの農村部・山間部には、住む人のいなくなった大きな古い家が数多く残っています。伊賀市は独自の空き家バンクで新しい住み手を探しており、物件ごとに状態の調査メモ、間取り図、動画を公開しています。</p>
          <ul class="ticks"><li>大阪・名古屋・京都へ鉄道でつながる</li><li>庭・畑・蔵のある、広い敷地の家が多い</li><li>市の調査による、正直な状態の説明</li></ul>
          <p class="tbc">【要確認】大阪・京都・関西空港からの所要時間</p>
        </div>
      </div>
    </section>

    <section class="sec" id="how">
      <div class="wrap">
        <div class="sec-head"><div><p class="kicker">購入の流れ</p><h2>探すところから、<em>住むところまで。</em></h2></div></div>
        <ol class="steps">
          <li class="rv"><span>01</span><h3>物件を選ぶ</h3><p>物件情報、状態の調査メモ、間取り図をご説明します。気になることは何でもご相談ください。</p></li>
          <li class="rv"><span>02</span><h3>登録・内覧</h3><p>内覧の予約には、伊賀流空き家バンクへの利用者登録が必要です。登録の準備から内覧の手配まで、現地でもオンラインでもお手伝いします。</p></li>
          <li class="rv"><span>03</span><h3>申込み・契約</h3><p>売買の仲介は、日本の宅地建物取引業者が行います。私たちは書類の説明や、業者・売主とのやりとりを支えます。</p></li>
          <li class="rv"><span>04</span><h3>決済・登記</h3><p>代金の支払い、司法書士による所有権の登記、購入時にかかる税金まで、手順をご案内します。</p></li>
          <li class="rv"><span>05</span><h3>入居・管理</h3><p>鍵、電気・水道、地元の職人の手配。留守の間は、現地の管理人が家を見守ります。</p></li>
        </ol>
        <div class="partner rv">
          <img src="{pre}img/brand/{MARK}" alt="" width="64" height="64">
          <div>
            <p class="kicker">{PARTNER}</p>
            <h3>伊賀市と二人三脚で</h3>
            <p>{BRAND} は、伊賀流空き家バンクを運営する伊賀市役所のバックアップを受けた、正式なエージェントです。物件情報、調査メモ、内覧はすべて市から直接。自治体が後ろについている安心感の中で、購入を進められます。</p>
            <p class="tbc">【要確認】伊賀市との協定・登録の正式名称と、サイトに記載することへの市の了承</p>
          </div>
        </div>
      </div>
    </section>

    <section class="sec care" id="care">
      <div class="wrap care-in">
        <div class="care-img rv"><img src="{pre}img/homes/564-02.jpg" alt="" loading="lazy"><span class="care-badge">留守の間も見守ります</span></div>
        <div class="rv">
          <p class="kicker">管理サービス</p>
          <h2>あなたの家を、<em>現地の管理人が。</em></h2>
          <p>セカンドハウスは、留守の間も安心できてこそ楽しめるもの。伊賀では、地元の管理人があなたに代わって家を見守ります。いつ訪れても、風が通り、手入れの行き届いた家でお迎えします。</p>
          <ul class="care-list">
            <li><strong>定期的な見回り</strong><span>窓を開けて風を通し、水を流して、木造の古い家を傷ませないようにします。</span></li>
            <li><strong>嵐のあとに</strong><span>大雨や台風のあとに、屋根・雨どい・庭を点検し、写真でご報告します。</span></li>
            <li><strong>庭と敷地</strong><span>草刈りと手入れで、ご近所にも気持ちよく。</span></li>
            <li><strong>修理の手配</strong><span>地元の職人を手配し、作業を見守り、見積もりをご説明します。</span></li>
            <li><strong>到着の準備</strong><span>鍵の管理、郵便物の受け取り、到着前の準備まで。</span></li>
          </ul>
          <p class="tbc">【要確認】管理サービスの内容・頻度・料金</p>
        </div>
      </div>
    </section>

    <section class="sec" id="faq">
      <div class="wrap faq-in">
        <div><p class="kicker">よくある質問</p><h2>よくある<em>ご質問</em></h2></div>
        <div class="faq">
          <details class="rv"><summary>外国籍の人や海外在住の人でも買えますか？</summary><p>日本では、外国籍の方や海外にお住まいの方でも住宅を所有できます。購入にビザは必要ありません。ただし、家を持っても日本に住む権利が得られるわけではなく、滞在はビザによります。【要確認】</p></details>
          <details class="rv"><summary>家についている畑も買えますか？</summary><p>農地は別の扱いです。農地の売買には農地法の許可が必要で、原則として耕作する人にしか許可が出ません。掲載物件の中にもこの注意書きがあるものがあり、物件ごとに市と業者に確認します。</p></details>
          <details class="rv"><summary>家の状態はどうですか？</summary><p>古く、手入れの必要な家が多くあります。市は雨漏りからトイレの不具合まで、わかっている点をすべて公開しています。ご購入の前に、点検や改修の見積もりも手配できます。</p></details>
          <details class="rv"><summary>現地に行く必要はありますか？</summary><p>少なくとも一度は現地をご覧いただくことをおすすめします。内覧は動画からでも始められ、多くの手続きは遠隔でも進められますが、契約や決済でご本人か代理人が必要になる場合があります。</p></details>
          <details class="rv"><summary>留守の間、家は誰が見てくれますか？</summary><p>伊賀の地元の管理人です。定期的に風を通して点検し、嵐のあとには屋根や庭を確認、鍵を預かって到着前に準備を整え、写真とともにご報告します。【要確認】</p></details>
          <details class="rv"><summary>売主は誰ですか？</summary><p>個人の所有者です。物件は伊賀流空き家バンクで公開され、売買は宅地建物取引業者が仲介します。私たちはその全体をご案内します。</p></details>
        </div>
      </div>
    </section>

    <section class="sec sec-tint" id="contact">
      <div class="wrap contact-in rv">
        <p class="kicker">お問い合わせ</p>
        <h2>気になる家は、<em>見つかりましたか。</em></h2>
        <p>物件番号と、ご予定やご希望をひとことお送りください。2営業日以内にご返信します。【要確認】</p>
        <a class="btn btn-ink" href="mailto:{EMAIL}?subject=%E4%BC%8A%E8%B3%80%E3%81%AE%E7%89%A9%E4%BB%B6%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6">メールで問い合わせる</a>
      </div>
    </section>
  </main>
''' + foot(pre)


def detail(h):
    pre = "../../../"
    j = JA[h["no"]]
    n = h["photos"]
    thumbs = "".join(f'<button type="button" data-src="{pre}{img(h["no"],k)}"{" class=on" if k==1 else ""}><img src="{pre}{img(h["no"],k)}" alt="写真{k}" loading="lazy"></button>' for k in range(1, n + 1))
    from PIL import Image as _I
    _o = ROOT / "data" / "img-orig" / f"{h['no']}-01.jpg"
    lowres = " lowres" if _o.exists() and _I.open(_o).width < 1000 else ""
    tour_img = pre + img(h["no"], min(2, n))
    tour = (f'<section class="d-sec"><h2>360°バーチャル内覧</h2><a class="tour" href="{h["tour"]}" rel="noopener" target="_blank" style="background-image:url({tour_img})">'
            f'<span class="tour-in"><span class="tour-ico" aria-hidden="true">360°</span><strong>家の中を歩いてみる</strong><span>すべての部屋を360°で見られます。伊賀市のバーチャル内覧が新しいタブで開きます ↗</span></span></a></section>') if h.get("tour") else ""
    video = f'<section class="d-sec"><h2>動画</h2><div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{h["video"]}" title="物件No.{h["no"]}の動画" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div></section>' if h["video"] else ""
    rows = [("所在地", f"伊賀市{j['place']}"), ("エリア", AREA[h["area"]]), ("間取り", h["layout"]), ("構造", j["structure"]), ("建築年", j["built"]),
            ("土地面積", f"{h['land']:,.2f}㎡"), ("延床面積", f"{h['floor']:,.2f}㎡"), ("水道", j["water"]), ("排水", j["drainage"]),
            ("トイレ", j["toilet"]), ("風呂", j["bath"]), ("ガス", j["gas"]), ("交通", j["access"]), ("学校", j["schools"]),
            ("買い物", j["shops"]), ("その他", j["notes"])]
    table = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in rows)
    others = [x for x in sorted(HOMES, key=lambda x: abs(x["price"] - h["price"])) if x["no"] != h["no"]][:3]
    more = "".join(card(x, pre) for x in others)
    return head(f"{j['title']}｜伊賀市{j['place']}｜{BRAND}", f"伊賀市{j['place']}の{h['layout']}の家。{man(h['price'])}。", pre, f"{pre}homes/{h['no']}/index.html") + f'''
  <main id="main" class="detail ja">
    <div class="wrap">
      <nav class="crumb" aria-label="パンくずリスト"><a href="{pre}ja/index.html#homes">物件一覧</a> / <span>No. {h['no']}</span></nav>
      <div class="d-head">
        <div>
          <p class="kicker">{AREA[h['area']]} · 伊賀市{e(j['place'])}</p>
          <h1>{e(j['title'])}</h1>
          <ul class="card-tags">{"".join(f"<li>{e(t)}</li>" for t in j["tags"])}</ul>
        </div>
        <div class="d-price"><strong>{man(h['price'])}</strong></div>
      </div>
      <div class="gallery{lowres}">
        <div class="g-main"><img src="{pre}{img(h['no'],1)}" alt="物件の写真"></div>
        {f'<div class="g-thumbs">{thumbs}</div>' if n > 1 else ''}
      </div>
      <div class="d-grid">
        <div>
          <section class="d-sec"><h2>建物の状態</h2><p class="cond">{e(j['condition'])}</p><p class="small">伊賀流空き家バンクの調査より。</p></section>
          <section class="d-sec"><h2>物件概要</h2><dl class="facts">{table}</dl></section>
          {tour}
          {video}
          <section class="d-sec"><h2>間取り図</h2><figure class="plan"><img src="{pre}img/homes/{h['no']}-plan.jpg" alt="間取り図" loading="lazy"></figure></section>
          <section class="d-sec"><h2>場所</h2><p class="small">詳しい住所は利用者登録の後にお知らせします。地図は地区を示しています。</p><div class="map"><iframe title="伊賀市{e(j['place'])}の地図" src="https://www.google.com/maps?q={h['lat']},{h['lng']}&amp;z=13&amp;output=embed" loading="lazy"></iframe></div></section>
        </div>
        <aside class="d-side">
          <div class="side-box">
            <p class="kicker">No. {h['no']}</p>
            <dl>
              <div><dt>売り出し価格</dt><dd>{man(h['price'])}</dd></div>
            </dl>
            <p class="small">別途、宅地建物取引業者の仲介手数料・税金・登記費用などがかかります。【要確認】</p>
            <a class="btn btn-ink" href="mailto:{EMAIL}?subject=No.{h['no']}%20(%E4%BC%8A%E8%B3%80%E5%B8%82{j['place'].split('（')[0]})">この物件について問い合わせる</a>
            {f'<a class="btn btn-line side-tour" href="{h["tour"]}" rel="noopener" target="_blank">360°バーチャル内覧 ↗</a>' if h.get('tour') else ''}
            <p class="side-official"><span aria-hidden="true">✓</span> {PARTNER}</p>
            <a class="src" href="{SOURCE}{h['no']}" rel="noopener" target="_blank">伊賀流空き家バンクの掲載ページ ↗</a>
          </div>
        </aside>
      </div>
      <section class="d-more"><h2>似た物件</h2><ul class="cards">{more}</ul></section>
    </div>
  </main>
''' + foot(pre)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(index(), encoding="utf-8")
    for h in HOMES:
        d = OUT / "homes" / str(h["no"])
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(detail(h), encoding="utf-8")
    print("built ja:", 1 + len(HOMES), "pages")
