import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "data", "months.json"), encoding="utf-8") as f:
    DATA = json.load(f)

MONTHS = DATA["months"]
COVER_NOTES = DATA["cover"]["notes"]

# TODO: switch to https://dadjokes.ngengwe.com once its DNS record is added
# (Wrangler token can't write DNS -- see project notes). Keep this in sync
# with the live custom domain once that's resolved.
SITE_URL = "https://dad-jokes-calendar.pages.dev"

FONT_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Archivo:wght@400;500;600;700&display=swap">'

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site_url}/{slug}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.png" type="image/png">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{site_url}/{og_image}">
<meta property="og:url" content="{site_url}/{slug}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{site_url}/{og_image}">
{font_link}
<link rel="stylesheet" href="/assets/styles.css">
</head>
<body class="{body_class}">
<div class="wrap">
<header class="site-header">
  <a class="wordmark" href="{home_href}">Midwest <em>Deadpan</em></a>
  <nav><a href="{home_href}">The year</a> &nbsp;·&nbsp; <a href="/flipbook">Flipbook</a> &nbsp;·&nbsp; <a href="/cover">Cover</a></nav>
</header>
"""

FOOT = """
<footer class="site-footer">Midwest Deadpan — Dad Jokes &times; Kansas City, 2027. One illustration, one joke, one real Kansas City place. &nbsp;&middot;&nbsp; <a href="/assets/Midwest_Deadpan_2027_Calendar.pdf">Print-ready PDF</a></footer>
</div>
<script src="/assets/site.js"></script>
</body>
</html>
"""


def build_grid(days, first_weekday):
    cells = [None] * first_weekday + list(range(1, days + 1))
    while len(cells) % 7 != 0:
        cells.append(None)
    rows = []
    for r in range(0, len(cells), 7):
        week = cells[r:r + 7]
        cells_html = "".join(
            f"<td>{c}</td>" if c else '<td class="empty">&middot;</td>' for c in week
        )
        rows.append(f"<tr>{cells_html}</tr>")
    return "".join(rows)


def hotspots_html(hotspots):
    pins = "".join(
        f'<button class="pin" style="left:{h["x"]}%; top:{h["y"]}%;" '
        f'data-idx="{i}" aria-label="{h["title"]}">{i + 1}</button>'
        for i, h in enumerate(hotspots)
    )
    notes = "".join(
        f'<div class="note" data-idx="{i}"><div class="note-num">{i + 1}</div>'
        f'<div><span class="kind">{h["kind"]}</span><h3>{h["title"]}</h3><p>{h["text"]}</p></div></div>'
        for i, h in enumerate(hotspots)
    )
    return pins, notes


def chain_html(chain):
    parts = []
    for i, c in enumerate(chain):
        parts.append(f"<span>{c}</span>")
        if i < len(chain) - 1:
            parts.append("<i>&rarr;</i>")
    return "".join(parts)


def render_month(m, prev_m, next_m):
    pins, notes = hotspots_html(m["hotspots"])
    grid_rows = build_grid(m["days"], m["firstWeekday"])
    chain = chain_html(m["chain"])

    prev_link = f'<a href="/{prev_m["key"]}"><span>&larr; Previous</span>{prev_m["name"]}</a>' if prev_m else '<span></span>'
    next_link = f'<a href="/{next_m["key"]}"><span>Next &rarr;</span>{next_m["name"]}</a>' if next_m else '<span></span>'

    html = HEAD.format(
        title=f'{m["name"]} 2027 — {m["location"]} | Midwest Deadpan',
        description=f'{m["setup"]} {m["punch"]} — {m["name"]} at {m["location"]}, Kansas City.',
        font_link=FONT_LINK,
        site_url=SITE_URL,
        slug=m["key"],
        og_image=f"assets/images/{m['key']}_hero.jpg",
        body_class="",
        home_href=f"/#{m['key']}",
    )
    html += f"""
<div class="stage" style="--accent:{m['season']};">
  <div class="page-card">
    <div class="illus">
      <img src="/assets/images/{m['key']}_hero.jpg" alt="{m['name']} 2027 illustration — {m['location']}">
      {pins}
    </div>
    <div class="joke-band">
      <p class="joke-setup">{m['setup']}</p>
      <p class="joke-punch">{m['punch']}</p>
    </div>
    <div class="grid-band">
      <p class="grid-month"><b>{m['name']}</b> 2027</p>
      <table class="cal">
        <thead><tr><th>S</th><th>M</th><th>T</th><th>W</th><th>T</th><th>F</th><th>S</th></tr></thead>
        <tbody>{grid_rows}</tbody>
      </table>
    </div>
  </div>
  <div class="panel">
    <div class="panel-head">
      <h2>{m['location']}</h2>
      <span class="tag-badge">{m['tag']}</span>
    </div>
    <div class="chain">{chain}</div>
    <div class="note-list">{notes}</div>
  </div>
</div>
<div class="month-nav">
  {prev_link}
  <a class="to-year" href="/#{m['key']}">All 12 months</a>
  {next_link}
</div>
"""
    html += FOOT
    with open(os.path.join(BASE, f"{m['key']}.html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_cover():
    notes = "".join(
        f'<div class="note"><div class="note-num">{i + 1}</div>'
        f'<div><span class="kind">{n["kind"]}</span><h3>{n["title"]}</h3><p>{n["text"]}</p></div></div>'
        for i, n in enumerate(COVER_NOTES)
    )
    html = HEAD.format(
        title="The Cover | Midwest Deadpan",
        description="The ensemble cast of the 2027 Midwest Deadpan calendar, gathered on Union Station's steps.",
        font_link=FONT_LINK,
        site_url=SITE_URL,
        slug="cover",
        og_image="assets/images/cover_hero.jpg",
        body_class="",
        home_href="/",
    )
    html += f"""
<div class="stage">
  <div class="page-card">
    <div class="illus">
      <img src="/assets/images/cover_hero.jpg" alt="Cover illustration — the ensemble cast on Union Station's steps">
    </div>
  </div>
  <div class="panel">
    <div class="panel-head">
      <h2>The cover</h2>
      <span class="tag-badge">Not tied to a month</span>
    </div>
    <div class="chain"><span>Dad</span><i>&middot;</i><span>Turkey</span><i>&middot;</i><span>Skeleton</span><i>&middot;</i><span>Referee</span></div>
    <div class="note-list">{notes}</div>
  </div>
</div>
<div class="month-nav">
  <span></span>
  <a class="to-year" href="/">All 12 months</a>
  <span></span>
</div>
"""
    html += FOOT
    with open(os.path.join(BASE, "cover.html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_index():
    html = HEAD.format(
        title="Midwest Deadpan",
        description="A 2027 Kansas City dad-joke calendar — twelve illustrated scenes where the joke leads and Kansas City completes it.",
        font_link=FONT_LINK,
        site_url=SITE_URL,
        slug="",
        og_image="assets/images/cover_hero.jpg",
        body_class="feed-body",
        home_href="/",
    )

    cover_section = f"""
  <section class="feed-page feed-cover" id="cover" data-label="Cover" aria-label="Cover">
    <div class="feed-illus">
      <img src="/assets/images/cover_hero.jpg" alt="Cover illustration — the ensemble cast on Union Station's steps">
      <div class="feed-scrim"></div>
    </div>
    <div class="feed-cover-copy">
      <p class="feed-eyebrow">2027 &middot; Dad Jokes &times; Kansas City</p>
      <h1>The joke leads.<br>Kansas City completes it.</h1>
      <p class="feed-sub">Twelve illustrated scenes where dad-joke logic occasionally becomes physically true. Scroll to start the year.</p>
    </div>
    <div class="feed-scrolldown" aria-hidden="true">Scroll <span>&darr;</span></div>
  </section>"""

    month_sections = ""
    for m in MONTHS:
        month_sections += f"""
  <section class="feed-page" id="{m['key']}" data-label="{m['name'][:3]}" aria-label="{m['name']} 2027 — {m['location']}" style="--accent:{m['season']};">
    <div class="feed-illus">
      <img src="/assets/images/{m['key']}_hero.jpg" alt="{m['name']} 2027 illustration — {m['location']}" loading="lazy">
    </div>
    <div class="feed-info">
      <h2 class="feed-month-label">{m['name'].upper()} 2027</h2>
      <p class="joke-setup">{m['setup']}</p>
      <p class="joke-punch">{m['punch']}</p>
      <a class="feed-more" href="/{m['key']}">{m['location']} &rarr;</a>
    </div>
  </section>"""

    end_section = """
  <section class="feed-page feed-end" id="end" aria-label="End of the year">
    <div class="feed-end-copy">
      <p class="feed-eyebrow">That's the year</p>
      <h2>Twelve months, one Kansas City.</h2>
      <a class="cta" href="/assets/Midwest_Deadpan_2027_Calendar.pdf">Download the print-ready PDF</a>
      <a class="cta secondary" href="#cover">Back to the cover &uarr;</a>
    </div>
  </section>"""

    dots = "".join(
        f'<button data-target="{sid}" aria-label="Jump to {label}"></button>'
        for sid, label in [("cover", "cover")] + [(m["key"], m["name"]) for m in MONTHS] + [("end", "end")]
    )

    section_ids = ["cover"] + [m["key"] for m in MONTHS] + ["end"]

    html += f"""
<div class="feed-progress"><div class="feed-progress-fill" id="feedProgressFill"></div></div>
<div class="feed-scroller" tabindex="0" role="region" aria-label="2027 calendar, month by month, press Page Down to advance">{cover_section}{month_sections}{end_section}
</div>
<div class="feed-dots">{dots}</div>
<script>window.__FEED_SECTIONS__ = {json.dumps(section_ids)};</script>
<script src="/assets/feed.js"></script>
</div>
</body>
</html>
"""
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_flipbook():
    html = HEAD.format(
        title="The Flipbook | Midwest Deadpan",
        description="Flip through the 2027 Midwest Deadpan calendar one spread at a time — illustration on the left, the story on the right.",
        font_link=FONT_LINK,
        site_url=SITE_URL,
        slug="flipbook",
        og_image="assets/images/cover_hero.jpg",
        body_class="flip-body",
        home_href="/",
    )

    total = len(MONTHS) + 1  # cover + 12 months

    cover_leaf = f"""
    <div class="flip-page" data-index="0" style="z-index:{total};">
      <div class="book-cover">
        <img src="/assets/images/cover_hero.jpg" alt="Cover illustration — the ensemble cast on Union Station's steps">
        <div class="book-cover-scrim"></div>
        <div class="book-cover-copy">
          <p class="feed-eyebrow">2027 &middot; Dad Jokes &times; Kansas City</p>
          <h1>Midwest Deadpan</h1>
          <p class="book-cover-hint">Turn the page to begin &rarr;</p>
        </div>
      </div>
    </div>"""

    month_leaves = ""
    for i, m in enumerate(MONTHS):
        place = m["hotspots"][0]
        grid_rows = build_grid(m["days"], m["firstWeekday"])
        month_leaves += f"""
    <div class="flip-page" data-index="{i + 1}" style="z-index:{total - i - 1};">
      <div class="book-spread">
        <div class="book-left">
          <img src="/assets/images/{m['key']}_hero.jpg" alt="{m['name']} 2027 illustration — {m['location']}" loading="lazy">
        </div>
        <div class="book-right" style="--accent:{m['season']};">
          <p class="feed-month-label">{m['name'].upper()} 2027</p>
          <p class="joke-setup">{m['setup']}</p>
          <p class="joke-punch">{m['punch']}</p>
          <div class="book-explain">
            <h3>{place['title']}</h3>
            <p>{place['text']}</p>
          </div>
          <table class="book-mini-cal">
            <caption>{m['name']} 2027</caption>
            <thead><tr><th>S</th><th>M</th><th>T</th><th>W</th><th>T</th><th>F</th><th>S</th></tr></thead>
            <tbody>{grid_rows}</tbody>
          </table>
        </div>
      </div>
    </div>"""

    html += f"""
<div class="book-wrap">
  <div class="book-stage" id="bookStage">{cover_leaf}{month_leaves}
  </div>
  <button class="book-nav prev" id="bookPrev" aria-label="Previous page">&larr;</button>
  <button class="book-nav next" id="bookNext" aria-label="Next page">&rarr;</button>
</div>
<p class="book-progress"><span id="bookPageNum">1</span> / {total}</p>
<script src="/assets/flipbook.js"></script>
</div>
</body>
</html>
"""
    with open(os.path.join(BASE, "flipbook.html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_404():
    html = HEAD.format(
        title="Page Not Found | Midwest Deadpan",
        description="That page doesn't exist. Browse the 2027 Midwest Deadpan calendar instead.",
        font_link=FONT_LINK,
        site_url=SITE_URL,
        slug="404.html",
        og_image="assets/images/cover_hero.jpg",
        body_class="",
        home_href="/",
    )
    html += """
<div class="hero">
  <a href="/cover"><img src="/assets/images/cover_hero.jpg" alt="Cover illustration — the ensemble cast"></a>
  <div>
    <h1>That page took a wrong turn.</h1>
    <p>There's no month here. Head back to the year, or start with January.</p>
    <a class="cta" href="/">Back to the year &rarr;</a>
  </div>
</div>
"""
    html += FOOT
    with open(os.path.join(BASE, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_sitemap():
    urls = [""] + [m["key"] for m in MONTHS] + ["cover", "flipbook"]
    entries = "\n".join(f"  <url><loc>{SITE_URL}/{u}</loc></url>" for u in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'
    with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    for i, m in enumerate(MONTHS):
        prev_m = MONTHS[i - 1] if i > 0 else None
        next_m = MONTHS[i + 1] if i < len(MONTHS) - 1 else None
        render_month(m, prev_m, next_m)
    render_cover()
    render_index()
    render_flipbook()
    render_404()
    render_sitemap()
    print(f"Built {len(MONTHS)} month pages + cover + index + flipbook + 404 + sitemap.")


if __name__ == "__main__":
    main()
