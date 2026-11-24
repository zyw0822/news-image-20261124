#!/usr/bin/env python3
"""Build the 1024x1024 news poster for make.fun news-image-20261124.
Deterministic: same input -> same PNG bytes (fixed palette, no timestamps).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
NAVY = (11, 31, 58)
RED = (178, 34, 34)
INK = (17, 17, 17)
GREY = (90, 90, 90)
LIGHT = (238, 240, 243)
GOLD = (201, 162, 39)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((36, 22), "WORLD NEWS", font=font(SERIF_B, 62), fill="white")
d.text((36, 88), "THE DAY IN ONE PAGE", font=font(SANS_B, 16), fill=(180, 195, 220))
d.text((1024 - 36 - d.textlength("TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 20)), 30),
       "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 20), fill="white")
d.text((1024 - 36 - d.textlength("10 STORIES  •  ONE IMAGE", font=font(SANS, 15)), 62),
       "10 STORIES  •  ONE IMAGE", font=font(SANS, 15), fill=(180, 195, 220))
d.rectangle([0, 118, W, 124], fill=GOLD)

# Lead story
y = 142
d.text((36, y), "LEAD  •  TECHNOLOGY / MARKETS", font=font(SANS_B, 17), fill=RED)
y += 28
d.text((36, y), "HUANG IS BACK", font=font(SERIF_B, 78), fill=INK)
y += 92
y = para(d, 36, y,
         "Nvidia's board reinstates Jensen Huang as CEO and president "
         "after President Trump intervenes — shares surge 31% in a day, "
         "Nasdaq jumps 6.5%.",
         font(SANS_B, 24), 952, 32)
y += 6
y = para(d, 36, y,
         "He resigned 11 days earlier over an affair with an alleged Chinese spy. "
         "The SEC accounting probe, Congress hearings on 1–3 Dec, and the export-control "
         "investigation all go on.",
         font(SANS, 19), 952, 26, color=(60, 60, 60))
d.line([36, y + 14, 988, y + 14], fill=LIGHT, width=2)

# Grid: 2 cols x 3 rows
stories = [
    ("SPACE / GEOPOLITICS", "A NUCLEAR WEAPON IN SPACE?",
     "Western intelligence warns Russia may launch a nuclear-armed satellite within weeks, by December. NATO vows to defend space."),
    ("CONFLICT", "UKRAINE SINKS WARSHIP OFF LIBYA",
     "Kyiv says 7 naval drones sank the Russian corvette Merkury at Benghazi. The war spreads beyond Europe."),
    ("MIDDLE EAST", "THREE TANKERS HIT MINES IN HORMUZ",
     "Iran says three tankers caught fire under US escort. US Treasury sanctions Iran's shadow-banking network; $15bn flagged."),
    ("TECH / TRADE", "US BLACKLISTS MEGASPEED",
     "Washington moves to blacklist the Singapore AI firm at the centre of the Nvidia chip scandal. An Alibaba unit is hit too."),
    ("BUSINESS", "CROWDSTRIKE TO BUY ZSCALER",
     "A $44bn all-stock deal to build a cybersecurity giant, as AI security spending surges."),
    ("EUROPE / ASIA", "RUSSIA WARNS ESTONIA",
     "Moscow says Tallinn's actions risk open war. Solomon Islands ends its security pact with China."),
]
gx, gy = 36, y + 30
col_w, row_h = 466, 148
for i, (kicker, head, body) in enumerate(stories):
    x = gx + (i % 2) * (col_w + 20)
    yy = gy + (i // 2) * row_h
    d.text((x, yy), kicker, font=font(SANS_B, 14), fill=RED)
    yy += 20
    yy = para(d, x, yy, head, font(SERIF_B, 21), col_w, 25)
    yy += 2
    para(d, x, yy, body, font(SANS, 16), col_w, 21, color=(50, 50, 50))
    if i % 2 == 0:
        d.line([x + col_w + 10, gy + (i // 2) * row_h, x + col_w + 10, gy + (i // 2) * row_h + row_h - 12],
               fill=LIGHT, width=2)

# Also in brief
by = gy + 3 * row_h + 8
d.rectangle([0, by, W, by + 96], fill=NAVY)
d.text((36, by + 10), "ALSO IN BRIEF", font=font(SANS_B, 16), fill=GOLD)
para(d, 36, by + 32,
     "Indonesia files treason charges over spying on President Prabowo  •  "
     "US, Mexico, Costa Rica and Jamaica to host the 2031 Women's World Cup; UK hosts 2035  •  "
     "SK hynix US shares surge 20% on the Nvidia rebound  •  COP31 climate talks close after a two-day delay.",
     font(SANS, 15), 952, 20, color="white")

# Footer
fy = by + 96 + 10
d.text((36, fy), "WORLD NEWS — 24 NOVEMBER 2026  •  Sources: Reuters, BBC, AP, Straits Times — 24 Nov 2026.",
       font=font(SANS, 14), fill=GREY)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
