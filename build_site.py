import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "data", "months.json"), encoding="utf-8") as f:
    DATA = json.load(f)

MONTHS = DATA["months"]
COVER_NOTES = DATA["cover"]["notes"]

FONT_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Archivo:wght@400;500;600;700&display=swap">'

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{font_link}
<link rel="stylesheet" href="{root}assets/styles.css">
</head>
<body>
<div class="wrap">
<header class="site-header">
  <a class="wordmark" href="{root}index.html">Midwest <em>Deadpan</em></a>
  <nav><a href="{root}index.html">The year</a> &nbsp;·&nbsp; <a href="{root}cover.html">Cover</a></nav>
</header>
"""

FOOT = """
<footer class="site-footer">Midwest Deadpan — Dad Jokes &times; Kansas City, 2027. One illustration, one joke, one real Kansas City place. &nbsp;&middot;&nbsp; <a href="{root}assets/Midwest_Deadpan_2027_Calendar.pdf">Print-ready PDF</a></footer>
</div>
<script src="{root}assets/site.js"></script>
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

    prev_link = f'<a href="{prev_m["key"]}.html"><span>&larr; Previous</span>{prev_m["name"]}</a>' if prev_m else '<span></span>'
    next_link = f'<a href="{next_m["key"]}.html"><span>Next &rarr;</span>{next_m["name"]}</a>' if next_m else '<span></span>'

    html = HEAD.format(
        title=f'{m["name"]} 2027 — {m["location"]} | Midwest Deadpan',
        description=f'{m["setup"]} {m["punch"]} — {m["name"]} at {m["location"]}, Kansas City.',
        font_link=FONT_LINK,
        root="",
    )
    html += f"""
<div class="stage" style="--accent:{m['season']};">
  <div class="page-card">
    <div class="illus">
      <img src="assets/images/{m['key']}_hero.jpg" alt="{m['name']} 2027 illustration — {m['location']}">
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
  <a class="to-year" href="index.html">All 12 months</a>
  {next_link}
</div>
"""
    html += FOOT.format(root="")
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
        root="",
    )
    html += f"""
<div class="stage">
  <div class="page-card">
    <div class="illus">
      <img src="assets/images/cover_hero.jpg" alt="Cover illustration — the ensemble cast on Union Station's steps">
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
  <a class="to-year" href="index.html">All 12 months</a>
  <span></span>
</div>
"""
    html += FOOT.format(root="")
    with open(os.path.join(BASE, "cover.html"), "w", encoding="utf-8") as f:
        f.write(html)


def render_index():
    cards = ""
    for m in MONTHS:
        cards += f"""
    <a class="month-card" href="{m['key']}.html">
      <img src="assets/images/{m['key']}_thumb.jpg" alt="{m['name']} thumbnail">
      <div class="mc-body">
        <div class="mc-name"><span class="mc-dot" style="background:{m['season']};"></span>{m['name']}</div>
        <div class="mc-punch">{m['punch']}</div>
      </div>
    </a>"""

    html = HEAD.format(
        title="Midwest Deadpan",
        description="A 2027 Kansas City dad-joke calendar — twelve illustrated scenes where the joke leads and Kansas City completes it.",
        font_link=FONT_LINK,
        root="",
    )
    html += f"""
<div class="hero">
  <a href="cover.html"><img src="assets/images/cover_hero.jpg" alt="Cover illustration — the ensemble cast"></a>
  <div>
    <h1>The joke leads. Kansas City completes it.</h1>
    <p>Twelve illustrated scenes of ordinary Midwestern life in a slightly illogical Kansas City, where dad-joke logic occasionally becomes physically true. Beautiful first, funny second — every page rewards a second look.</p>
    <a class="cta" href="{MONTHS[0]['key']}.html">Start with January &rarr;</a>
    <a class="cta secondary" href="assets/Midwest_Deadpan_2027_Calendar.pdf">Download the print-ready PDF</a>
  </div>
</div>
<p class="year-label">The year</p>
<div class="month-grid">{cards}
</div>
"""
    html += FOOT.format(root="")
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    for i, m in enumerate(MONTHS):
        prev_m = MONTHS[i - 1] if i > 0 else None
        next_m = MONTHS[i + 1] if i < len(MONTHS) - 1 else None
        render_month(m, prev_m, next_m)
    render_cover()
    render_index()
    print(f"Built {len(MONTHS)} month pages + cover + index.")


if __name__ == "__main__":
    main()
