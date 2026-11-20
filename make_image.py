import os, math
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/dejavu/"
PAPER, INK, RED, GREY, RULE = (247, 243, 232), (20, 18, 14), (163, 35, 28), (107, 99, 85), (185, 174, 149)
SERIF_B, SERIF, SANS, SANS_B = "DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf", "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"
CARDS = [
    ('BANGLADESH', "Yunus's ancestral home is burned in Chattogram", "Fresh violence before Sheikh Hasina's return in December."),
    ('MIDDLE EAST', "Houthi missiles hit Riyadh's financial district", 'The Public Investment Fund tower was damaged; nobody was hurt.'),
    ('LAW', 'The ICJ finds Myanmar committed genocide', 'Judges ruled on the Rohingya case brought by The Gambia.'),
    ('AFRICA', 'Somalia expels the Emirati ambassador', 'Mogadishu accuses Abu Dhabi of undermining its sovereignty.'),
    ('EUROPE', 'A pay equity ruling is welcomed in New Zealand', 'The court set a framework for comparing female-led work.'),
    ('TRADE', 'Manila and Santiago sign a free trade deal', "The Philippines' first such pact with a Latin American state."),
    ('ASIA', "Mongolia's president resigns; a chairman steps up", 'Sandagiin Byambatsogt holds the post until a vote in four months.'),
    ('ENERGY', 'Saudi oil exports reach a nine-month high', 'JODI data show September shipments above their pre-war level.'),
    ('SPORT', 'Gukesh defends his title in Geneva on 24 November', "The champion meets Uzbekistan's Javokhir Sindarov."),
    ('SPORT', 'Carlsen forfeits two rapid games in a row', 'The Norwegian skipped the fast classic rounds without comment.'),
    ('CRICKET', 'New Zealand reach 317 for six at lunch', "India's attack lost Phillips late on the first day of the Test."),
    ('INDIA', 'A deep-tech hub is approved at IIT Kanpur', 'The Uttar Pradesh cabinet released Rs 281 crore for Noida.'),
]
_fonts = {}

def F(name, size):
    k = (name, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(FD + name, size)
    return _fonts[k]

def tw(d, t, f):
    return d.textlength(t, font=f)

def fit(d, t, f, w):
    name, size = os.path.basename(f.path), f.size
    while size > 6 and d.textlength(t, font=F(name, size)) > w:
        size -= 1
    return size

def wrap(d, t, f, w):
    lines, cur = [], ""
    for word in t.split():
        cand = (cur + " " + word).strip()
        if not cur or d.textlength(cand, font=f) <= w:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def clip(d, t, f, w, n):
    ls = wrap(d, t, f, w)
    if len(ls) <= n:
        return ls
    ls = ls[:n]
    last = ls[-1]
    while last and d.textlength(last + "…", font=f) > w:
        last = last[:-1]
    if " " in last:
        last = last.rsplit(" ", 1)[0]
    ls[-1] = last.rstrip() + "…"
    return ls

def rule(d, y, x0=8, x1=1016):
    d.line([(x0, y), (x1, y)], fill=RULE, width=1)

def star(d, cx, cy, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)

def illo1(d, bx, by):
    d.rectangle([bx, by, bx + 299, by + 95], fill=(30, 58, 107))
    for cx, kind in zip((bx + 40, bx + 150, bx + 260), ("us", "cn", "ru")):
        x0, y0 = cx - 18, by + 15
        if kind == "us":
            d.rectangle([x0, y0, x0 + 35, y0 + 21], fill=(255, 255, 255))
            for k in range(4):
                d.rectangle([x0, y0 + k * 6, x0 + 35, y0 + k * 6 + 3], fill=(178, 34, 52))
            d.rectangle([x0, y0, x0 + 15, y0 + 12], fill=(30, 58, 138))
        elif kind == "cn":
            d.rectangle([x0, y0, x0 + 35, y0 + 21], fill=(200, 16, 46))
            star(d, x0 + 9, y0 + 8, 4, (255, 222, 89))
        else:
            d.rectangle([x0, y0, x0 + 35, y0 + 21], fill=(255, 255, 255))
            d.rectangle([x0, y0 + 7, x0 + 35, y0 + 14], fill=(0, 57, 166))
            d.rectangle([x0, y0 + 14, x0 + 35, y0 + 21], fill=(213, 43, 30))
    for cx in (bx + 40, bx + 150, bx + 260):
        d.polygon([(cx - 22, by + 95), (cx + 22, by + 95), (cx + 13, by + 63), (cx - 13, by + 63)], fill=(14, 18, 22))
        d.ellipse([cx - 9, by + 42, cx + 9, by + 60], fill=(14, 18, 22))

def illo2(d, bx, by):
    d.rectangle([bx, by, bx + 299, by + 95], fill=(239, 231, 210))
    stone, dark = (122, 108, 82), (74, 62, 42)
    d.polygon([(bx + 30, by + 36), (bx + 127, by + 9), (bx + 224, by + 36)], fill=dark)
    d.rectangle([bx + 26, by + 36, bx + 228, by + 43], fill=stone)
    for k in range(6):
        cx = bx + 42 + k * 32
        d.rectangle([cx, by + 45, cx + 6, by + 80], fill=stone)
        d.rectangle([cx - 3, by + 43, cx + 9, by + 46], fill=dark)
        d.rectangle([cx - 3, by + 79, cx + 9, by + 82], fill=dark)
    d.rectangle([bx + 22, by + 82, bx + 232, by + 87], fill=stone)
    d.rectangle([bx + 16, by + 87, bx + 238, by + 91], fill=stone)
    d.rectangle([bx + 10, by + 91, bx + 244, by + 95], fill=stone)
    g, gx = (176, 138, 42), bx + 268
    d.line([(gx, by + 26), (gx, by + 75)], fill=g, width=2)
    d.line([(gx - 19, by + 36), (gx + 19, by + 36)], fill=g, width=2)
    d.line([(gx - 19, by + 36), (gx - 19, by + 46)], fill=g)
    d.line([(gx + 19, by + 36), (gx + 19, by + 46)], fill=g)
    d.arc([gx - 28, by + 40, gx - 10, by + 52], 0, 180, fill=g)
    d.arc([gx + 10, by + 40, gx + 28, by + 52], 0, 180, fill=g)
    d.line([(gx - 16, by + 75), (gx + 16, by + 75)], fill=g, width=2)

def illo3(d, bx, by):
    d.rectangle([bx, by, bx + 299, by + 95], fill=(30, 75, 58))
    pale, cx, cy = (196, 222, 204), bx + 62, by + 48
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(41, 98, 78), outline=pale)
    d.ellipse([cx - 12, cy - 28, cx + 12, cy + 28], outline=pale)
    d.line([(cx - 28, cy), (cx + 28, cy)], fill=pale)
    d.arc([cx - 27, cy - 20, cx + 27, cy + 20], 20, 160, fill=pale)
    d.arc([cx - 27, cy - 20, cx + 27, cy + 20], 200, 340, fill=pale)
    tx = bx + 180
    d.line([(tx, by + 20), (tx, by + 64)], fill=(232, 238, 230), width=11)
    d.ellipse([tx - 9, by + 58, tx + 9, by + 78], fill=(232, 238, 230))
    d.line([(tx, by + 42), (tx, by + 66)], fill=(203, 58, 46), width=5)
    d.ellipse([tx - 5, by + 62, tx + 5, by + 74], fill=(203, 58, 46))
    lx, ly = bx + 244, by + 44
    d.polygon([(lx - 22, ly + 26), (lx - 24, ly - 2), (lx - 6, ly - 24), (lx + 16, ly - 22), (lx + 24, ly + 2), (lx + 8, ly + 24)], fill=(124, 178, 122))
    d.line([(lx - 20, ly + 24), (lx + 18, ly - 20)], fill=(214, 236, 202), width=2)
    d.line([(lx + 2, ly + 12), (lx + 2, ly - 12)], fill=(214, 236, 202))

def band(d, bx, by, i):
    (illo1, illo2, illo3)[i](d, bx, by)

def main():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, 1015, 1015], outline=RULE)

    d.text((12, 12), "THE WORLD IN ONE DAY", font=F(SANS_B, 8), fill=INK)
    r = "DAY 324 OF 2026 · ONE-PAGE EDITION"
    d.text((1012 - tw(d, r, F(SANS, 8)), 12), r, font=F(SANS, 8), fill=GREY)
    rule(d, 26)

    t = "Friday 20 November 2026"
    d.text((12, 30), t, font=F(SERIF_B, fit(d, t, F(SERIF_B, 44), 900)), fill=INK)

    t = "Three presidents sign a peace declaration in Shenzhen · Cyclone Akvan bears down on Odisha · Anthropic raises $81.3bn"
    d.text((12, 78), t, font=F(SANS_B, fit(d, t, F(SANS_B, 12), 940)), fill=RED)

    tabs = ["ASIA 7", "AFRICA 2", "AMERICAS 3", "EUROPE 3", "MIDEAST 5", "ECONOMY 4", "SPORT 3"]
    for i, t in enumerate(tabs):
        x = 8 + i * 138
        d.rectangle([x, 96, x + 131, 113], outline=RULE)
        d.text((x + 4, 105), t, font=F(SANS_B, 9), fill=INK, anchor="lm")

    stats = [('3', 'presidents at one table'), ('110', 'kmph gusts off Odisha'),
             ('$81.3bn', 'raised in the largest IPO of 2026'), ('$1.5tn', "Anthropic's value at the bell"),
             ('10', 'train services already cancelled')]
    for i, (n, lab) in enumerate(stats):
        x = 8 + i * 200
        d.text((x, 120), n, font=F(SERIF_B, 20), fill=RED)
        d.text((x, 140), lab, font=F(SANS, 8), fill=GREY)

    data = [
        ("SHENZHEN · APEC", "Three presidents sign a peace declaration in Shenzhen",
         "Trump, Xi and Putin met as a trio for the first time, agreeing on nuclear talks, oil supply and a reformed Security Council.",
         "Reuters · AP"),
        ("ODISHA · CYCLONE AKVAN", "A cyclone turns for the coast and India clears the beaches",
         "Akvan should land between Narsapur and Puri with 100 kmph winds; ten trains are cancelled and flights are suspended.",
         "IMD · Indian Express"),
        ("NEW YORK · MARKETS", "Anthropic raises $81.3bn and passes SpaceX's record debut",
         "The AI lab opened above a $1.5 trillion valuation, the twelfth-largest company in the world on its first morning.",
         "Nasdaq · Bloomberg"),
    ]
    for i, (tag, hl, body, src) in enumerate(data):
        x = 8 + i * 351
        d.rectangle([x, 156, x + 305, 349], outline=RULE)
        band(d, x + 3, 159, i)
        n, f14 = str(i + 1), F(SANS_B, 14)
        nw = tw(d, n, f14)
        d.rectangle([x + 6, 162, x + 12 + nw, 181], fill=(255, 255, 255))
        d.text((x + 9, 164), n, font=f14, fill=RED)
        d.text((x + 6, 256), tag, font=F(SANS_B, 8), fill=RED)
        f17 = F(SERIF_B, 17)
        for j, ln in enumerate(clip(d, hl, f17, 294, 2)):
            d.text((x + 6, 267 + j * 18), ln, font=f17, fill=INK)
        f9 = F(SANS, 9)
        for j, ln in enumerate(clip(d, body, f9, 294, 3)):
            d.text((x + 6, 307 + j * 11), ln, font=f9, fill=GREY)
        d.text((x + 6, 347), src, font=F(SANS, 7), fill=GREY, anchor="ld")

    rule(d, 360)
    d.text((12, 366), "MORE STORIES INSIDE", font=F(SANS_B, 8), fill=INK)
    d.text((12, 382), "Twelve more dispatches from four continents, the day hour by hour, and the numbers that moved.", font=F(SANS, 8), fill=GREY)

    draw_lower(d)
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out)
    print(os.path.getsize(out))

def draw_lower(d):
    for i, (cat, hl, body) in enumerate(CARDS):
        x = 8 + (i % 4) * 248
        y = 392 + (i // 4) * 84
        d.rectangle([x, y, x + 240, y + 76], outline=RULE)
        d.text((x + 4, y + 3), str(i + 1), font=F(SANS_B, 8), fill=RED)
        d.text((x + 4, y + 13), cat, font=F(SANS_B, 7), fill=RED)
        fh = F(SERIF_B, 11)
        if len(wrap(d, hl, fh, 228)) > 2:
            fh = F(SERIF_B, fit(d, hl, fh, 200))
        for j, ln in enumerate(clip(d, hl, fh, 228, 2)):
            d.text((x + 4, y + 24 + j * 12), ln, font=fh, fill=INK)
        fb = F(SANS, 7)
        for j, ln in enumerate(clip(d, body, fb, 228, 2)):
            d.text((x + 4, y + 52 + j * 9), ln, font=fb, fill=GREY)

    d.rectangle([8, 656, 688, 900], outline=RULE, width=1)
    d.text((16, 662), "THE DAY BY THE HOUR", font=F(SANS_B, 9), fill=INK)
    hours = [
        ('00:00', 'Anthropic prices its listing at $81.3bn, above the range.'),
        ('03:00', "The IMD moves Cyclone Akvan's landfall south of Gopalpur."),
        ('05:00', 'Railways cancel ten trains along the Odisha and Andhra coast.'),
        ('06:00', "Chattogram police report Yunus's ancestral house set on fire."),
        ('08:00', 'Three capitals publish the Shenzhen declaration in full.'),
        ('10:00', 'The ICJ reads its genocide ruling against Myanmar.'),
        ('13:00', 'Nasdaq opens and Anthropic trades above $1.5 trillion.'),
        ('16:00', 'New Zealand close day one of the second Test on 317 for six.'),
    ]
    for i, (t, ev) in enumerate(hours):
        cx = 16 + (i % 4) * 168
        cy = 686 + (i // 4) * 108
        d.text((cx, cy), t, font=F(SERIF_B, 14), fill=RED)
        d.line([(cx, cy + 18), (cx + 164, cy + 18)], fill=RULE, width=1)
        fe = F(SANS, 7)
        for j, ln in enumerate(clip(d, ev, fe, 158, 3)):
            d.text((cx, cy + 24 + j * 9), ln, font=fe, fill=GREY)
    d.rectangle([700, 656, 1016, 900], outline=RULE, width=1)
    d.text((708, 662), "ALSO ON THIS DAY", font=F(SANS_B, 9), fill=INK)
    also = [
        'Houthi missiles damaged the Public Investment Fund tower in Riyadh.',
        'Somalia gave the Emirati ambassador a week to leave the country.',
        'Israel struck a Hezbollah bunker in the Bekaa valley overnight.',
        "Gaza's health ministry reported two dead and two dead of wounds.",
        'A tanker burned after a mine strike east of the Strait of Hormuz.',
        "Yemen's army claimed 144 Houthi casualties in Taiz and Marib.",
        "Mongolia's parliament accepted the president's resignation.",
        'Pakistan and Qatar signed a police cooperation memorandum.',
        'Manila and Santiago signed their first Latin American trade pact.',
        'The Philippine Senate apologised for a broadcast feed glitch.',
        'Gukesh and Sindarov play the first game in Geneva on 24 November.',
        'Rakshitha Sree Ramraj beat a Chinese seed at the Hong Kong Open.',
    ]
    fo = F(SANS, 7)
    for c in range(2):
        x = 708 if c == 0 else 866
        cw = min(150, 1014 - x)
        y = 686
        for k in range(6):
            n = c * 6 + k + 1
            for ln in wrap(d, "%d. %s" % (n, also[n - 1]), fo, cw):
                if y + 7 > 900:
                    break
                d.text((x, y), ln, font=fo, fill=GREY)
                y += 10
    d.text((16, 906), "Times UTC · numbers match the stories on this page.", font=F(SANS, 7), fill=GREY)

    rule(d, 918)
    d.text((8, 924), "MARKETS AT THE CLOSE", font=F(SANS_B, 9), fill=INK)
    mk = [
        ('$1.5tn', "Anthropic's value at the first close"),
        ('$81.3bn', 'raised, the largest listing of the year'),
        ('12th', 'largest company in the world by value'),
        ('9-mo high', 'Saudi crude exports in September'),
        ('Rs 281cr', 'cleared for the Kanpur deep-tech hub'),
    ]
    f7 = F(SANS, 7)
    for i, (v, lab) in enumerate(mk):
        x = 8 + i * 200
        d.text((x, 942), v, font=F(SERIF_B, 12), fill=INK)
        d.text((x, 958), lab, font=f7, fill=GREY)
    rule(d, 980)
    note = "DATE CHECK Every story here happened, or was first reported, on Friday 20 November 2026. Sources: Reuters, AP, AFP, Al Jazeera, UN News, ICJ, JODI."
    for j, ln in enumerate(wrap(d, note, f7, 780)):
        d.text((8, 986 + j * 9), ln, font=f7, fill=GREY)
    d.text((1016, 986), "make.fun · news-image-news-image-20261120", font=f7, fill=GREY, anchor="ra")

main()
