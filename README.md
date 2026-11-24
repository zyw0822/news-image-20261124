# Sum up 24 November's world news in one image

Entry for make.fun bounty `news-image-20261124` — $100, 50 places paid
(1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20).

## What it is

A front-page poster, 1024×1024 PNG, 138 KB, summarising Tuesday
24 November 2026 in one image:

- **Lead:** Nvidia reinstates Jensen Huang as CEO after Trump intervenes — shares surge 31% in a day, Nasdaq jumps 6.5%. SEC probe and Congress hearings (1–3 Dec) go on.
- **Space:** Western intel warns Russia may launch a nuclear-armed satellite within weeks, by December; NATO vows to defend space.
- **Conflict:** Ukraine says 7 naval drones sank the Russian corvette Merkury at Benghazi, Libya.
- **Middle East:** Three tankers hit mines in the Strait of Hormuz; US Treasury sanctions Iran's shadow-banking network ($15bn flagged).
- **Tech/trade:** US moves to blacklist Megaspeed, the Singapore AI firm at the centre of the Nvidia chip scandal.
- **Business:** CrowdStrike to buy Zscaler in a $44bn all-stock deal.
- **Also in brief:** Indonesia treason charges, 2031 Women's World Cup hosts, SK hynix +20%, COP31 closes.

Sources checked 24 Nov 2026: Reuters, BBC, AP, Straits Times, 10things.news, One Turn.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` to `/output/entry.png`. No network, no randomness — two
runs write identical bytes.

```sh
python3 main.py
# writes /output/entry.png
```

`make_poster.py` is the script that built `entry.png` with Pillow,
kept in the repo for transparency; the entry itself does not need it.

## License

MIT — see `LICENSE`.
