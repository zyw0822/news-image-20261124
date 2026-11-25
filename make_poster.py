#!/usr/bin/env python3
"""Build the 1024x1024 news poster for make.fun news-image-20261124 (v2).

34 stories from Tuesday 24 November 2026, grouped by region.
Deterministic: same input -> same PNG bytes (fixed palette, fixed fonts,
no timestamps, no randomness, no network).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
NAVY = (11, 31, 58)
RED = (178, 34, 34)
INK = (17, 17, 17)
GREY = (90, 90, 90)
BODY = (55, 55, 55)
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

def fit(draw, text, fnt, max_w):
    """Truncate to one line with an ellipsis if too wide (deterministic)."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "…"
    while text and draw.textlength(text + ell, font=fnt) > max_w:
        text = text[:-1]
    return text + ell

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 112], fill=NAVY)
d.text((36, 18), "WORLD NEWS", font=font(SERIF_B, 58), fill="white")
d.text((36, 82), "THE DAY IN ONE PAGE", font=font(SANS_B, 15), fill=(180, 195, 220))
d.text((1024 - 36 - d.textlength("TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 19)), 26),
       "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 19), fill="white")
d.text((1024 - 36 - d.textlength("34 STORIES  •  8 REGIONS", font=font(SANS, 14)), 56),
       "34 STORIES  •  8 REGIONS", font=font(SANS, 14), fill=(180, 195, 220))
d.rectangle([0, 112, W, 118], fill=GOLD)

# Lead story
y = 134
d.text((36, y), "LEAD  •  TECHNOLOGY / MARKETS", font=font(SANS_B, 16), fill=RED)
y += 26
d.text((36, y), "HUANG IS BACK", font=font(SERIF_B, 58), fill=INK)
y += 70
y = para(d, 36, y,
         "Nvidia's board unanimously reinstates Jensen Huang as CEO and president, "
         "effective immediately, after US officials say the move poses no national-security "
         "risk. Shares soar 31%; Nasdaq jumps 6.5%.",
         font(SANS_B, 20), 952, 26)
y += 2
y = para(d, 36, y,
         "Investigations continue: SEC accounting probe, Congress hearings 1–3 Dec, California AG probe, export-control inquiry.",
         font(SANS, 15), 952, 20, color=(60, 60, 60))
d.line([36, y + 10, 988, y + 10], fill=LIGHT, width=2)

# Region grid: 2 columns
LEFT = [
    ("NORTH AMERICA", [
        ("CROWDSTRIKE TO BUY ZSCALER",
         "$44bn all-stock deal to build a cybersecurity giant as AI security spending surges."),
        ("SANOFI TO BUY INSMED FOR $41BN",
         "All-cash offer of $175 a share for the biotech, Sanofi's biggest deal in years."),
        ("US BLACKLISTS MEGASPEED",
         "The Singapore AI firm at the heart of the Nvidia chip scandal is blacklisted."),
        ("TRUMP HONOURS GIULIANI",
         "Medal of Freedom for the ex-New York mayor, in a private Oval Office ceremony."),
        ("TRUMP PARDONS THE TURKEYS",
         "Thanksgiving tradition at the White House, two days before the holiday."),
        ("SENATE PROBES VANCE OIL TIES",
         "A Senate panel examines the vice-president's links to a Venezuelan oil contract."),
    ]),
    ("EUROPE", [
        ("RUSSIA LAUNCHES NUCLEAR SATELLITE",
         "Moscow puts a nuclear-powered satellite in orbit, drawing close Western scrutiny."),
        ("UKRAINE SINKS WARSHIP OFF LIBYA",
         "Kyiv says its drones sank the Russian corvette Merkury off Benghazi."),
        ("PUTIN VOWS RETALIATION",
         "Vows 'inevitable' retaliation; refinery output down 45% since late October."),
        ("RUSSIAN DRONE ENTERS POLAND",
         "A surveillance drone briefly crosses into Polish airspace before turning back."),
        ("STRIKE ON ZAPORIZHZHIA KILLS 2",
         "Overnight Russian strike hits an apartment block; 40 wounded, including four children."),
        ("UK WARNS FIRMS OF SABOTAGE",
         "British officials tell companies backing Ukraine to brace for Russian sabotage."),
        ("GERMANY GETS DELTA ACCESS",
         "First country given access to Ukraine's Delta battlefield system; missile deal in the works."),
        ("BREAK-IN AT PRINCE WILLIAM'S HOME",
         "Two men arrested after a break-in at Anmer Hall, the prince's Norfolk home."),
    ]),
    ("AFRICA", [
        ("FIGHTING TRAPS EBOLA TEAMS",
         "Heavy clashes in Ituri, DR Congo, cut off Ebola responders."),
        ("KENYA BORDER CLASHES KILL 9",
         "Fighting erupts on the Isiolo-Garissa border."),
        ("LANDMINE DEATHS HIT 5-YEAR HIGH",
         "7,000 casualties worldwide in 2025, worst in Myanmar and Syria."),
    ]),
]

RIGHT = [
    ("ASIA", [
        ("CHINA PROBES SHANGHAI CHIEF",
         "Graft probe opens into Politburo member Chen Jining, the fourth such case in a year."),
        ("PAKISTANI ASTRONAUT FOR TIANGONG",
         "Set to be the first non-Chinese national aboard China's Tiangong station."),
        ("HANOI BLAST KILLS AT LEAST 6",
         "Restaurant explosion, suspected cooking gas, injures 10 in the Vietnamese capital."),
        ("SEOUL SCRAMBLES JETS",
         "Jets scrambled and air-raid alerts sounded as Russian jets enter its defence zone."),
        ("INDIA NOW ASIA'S NO. 3 POWER",
         "Lowy Index puts India past Russia and Japan, behind only the US and China."),
        ("JAPAN'S FIRST EBOLA DRILL",
         "Tokyo rehearses a response as an outbreak spreads in Congo."),
        ("INDONESIA CHARGES EX-POLICE CHIEF",
         "Treason charges over alleged spying aimed at undermining President Prabowo."),
    ]),
    ("MIDDLE EAST", [
        ("TANKERS HIT BY MINES IN HORMUZ",
         "Tankers are struck in the Strait of Hormuz; Iran and the US trade blame as tensions rise."),
        ("HAMAS SECURITY CHIEF KILLED",
         "Naeem Abu Nahel dies in an Israeli airstrike on Gaza City; six others also killed."),
        ("HOUTHIS HIT RIYADH TOWER",
         "Attack strikes the PIF tower, the capital's tallest skyscraper; 11 people injured."),
        ("IRAN VOWS TO FIGHT US BLOCKADE",
         "Tehran says it will use 'all tools' against the US naval blockade."),
        ("IRAQ TAKES OVER KURDISH OILFIELDS",
         "Prime minister orders the oil ministry to manage fields in Kurdish-controlled areas."),
    ]),
    ("LATIN AMERICA", [
        ("MEXICO CAPTURES 'EL CHAPO ISIDRO'",
         "Sinaloa kingpin seized in a bloody raid; 11 dead, four of them soldiers."),
        ("WHO CHIEF VISITS CUBA",
         "Tedros pledges $2m for vaccination during a visit to Havana."),
    ]),
    ("OCEANIA", [
        ("FIJI SHUTS SCHOOLS OVER DROUGHT",
         "All schools close for five days from 30 Nov as the El Niño drought deepens."),
    ]),
    ("SCIENCE", [
        ("MERCURY PROBE BURN CUT SHORT",
         "Burn ends early after a software glitch; ESA says the mission is safe."),
    ]),
]

ITEM_H = 33
SEC_H = 21
COL_W = 464
gy = y + 22

def draw_column(x, sections):
    yy = gy
    for title, items in sections:
        d.text((x, yy), title, font=font(SANS_B, 13), fill=RED)
        d.line([x, yy + 17, x + COL_W, yy + 17], fill=LIGHT, width=1)
        yy += SEC_H
        for head, body in items:
            d.text((x, yy), fit(d, head, font(SERIF_B, 13), COL_W),
                   font=font(SERIF_B, 13), fill=INK)
            d.text((x, yy + 16), fit(d, body, font(SANS, 10), COL_W),
                   font=font(SANS, 10), fill=BODY)
            yy += ITEM_H
        yy += 2
    return yy

end_left = draw_column(36, LEFT)
end_right = draw_column(524, RIGHT)

# Footer
fy = max(end_left, end_right) + 4
d.text((36, fy),
       "WORLD NEWS — TUESDAY 24 NOVEMBER 2026  •  Sources: Reuters, AP, BBC, SCMP, Al Jazeera, Ukrinform, Japan Times — 24 Nov 2026.",
       font=font(SANS, 11), fill=GREY)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
