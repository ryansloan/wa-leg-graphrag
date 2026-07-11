"""Render the blog hero image: every final-passage vote as a faint thread,
with the case study's signal edges (sponsorships, caucus-breaking Nays) glowing
through the fog. 1200x630 (og:image), dark ground.

Output: assets/hero.png
"""

import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "hero.png"

GROUND, FOG = "#121211", "#6a6862"
SPON, NAY = "#199e70", "#d95926"  # dark-mode accent pair (validated on dark)
FOG_SAMPLE = 26000  # sample the context layer; the 30 signal edges are always complete
rng = np.random.default_rng(7)


def curve(p0, p1, n=24):
    """Vertical S-bezier from p0 (bottom) to p1 (top), sampled as a polyline."""
    (x0, y0), (x1, y1) = p0, p1
    t = np.linspace(0, 1, n)
    # cubic bezier with vertical control points -> threads hang rather than shoot
    bx_ = ((1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * x0
           + 3 * (1 - t) * t ** 2 * x1 + t ** 3 * x1)
    by_ = ((1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * (y0 + 0.42)
           + 3 * (1 - t) * t ** 2 * (y1 - 0.42) + t ** 3 * y1)
    return np.column_stack([bx_, by_])

MANDATE = ["HB 2081", "SB 5786", "SB 5525", "HB 1524"]
RELIEF = ["HB 2309", "HB 2575"]

d = json.loads((ROOT / "data" / "dataset.json").read_text())
members = {m["member_id"]: m for m in d["members"]}
name2num = {b["bill_id"]: b["bill_number"] for b in d["bills"]}

# positions: members along the bottom (sorted by party then district), bills along the top
mem_ids = sorted({v["member_id"] for v in d["votes"]},
                 key=lambda mid: (members[mid]["party"], members[mid]["district"], mid))
mx = {mid: i / (len(mem_ids) - 1) for i, mid in enumerate(mem_ids)}
bill_nums = sorted({b["bill_number"] for b in d["bills"]})
bx = {bn: i / (len(bill_nums) - 1) for i, bn in enumerate(bill_nums)}

# fog: a sample of all final-passage votes (member -> bill), hair-thin curved threads
all_fp = [(mx[v["member_id"]], bx[v["bill_number"]])
          for v in d["votes"] if "Final Passage" in v["motion"]]
if FOG_SAMPLE:
    idx = rng.choice(len(all_fp), size=min(FOG_SAMPLE, len(all_fp)), replace=False)
    all_fp = [all_fp[i] for i in idx]
fog = [curve((x0, 0.0), (x1, 1.0)) for x0, x1 in all_fp]

# signal: case-study edges (decisive-final Nay by Democrats on mandate bills + primary sponsorships)
def decisive(bid):
    bn = name2num[bid]
    last = defaultdict(int)
    for v in d["votes"]:
        if v["bill_number"] == bn and "Final Passage" in v["motion"]:
            last[v["chamber"]] = max(last[v["chamber"]], v["sequence_number"])
    return {(v["member_id"]): v["vote"] for v in d["votes"]
            if v["bill_number"] == bn and "Final Passage" in v["motion"]
            and v["sequence_number"] == last[v["chamber"]]}

signal_nay, signal_spon = [], []
for bid in MANDATE:
    for mid, vote in decisive(bid).items():
        if vote == "Nay" and members[mid]["party"] == "D":
            signal_nay.append(curve((mx[mid], 0.0), (bx[name2num[bid]], 1.0)))
for bid in MANDATE + RELIEF:
    for s in d["sponsorships"]:
        if s["bill_number"] == name2num[bid] and s["role"] == "primary":
            signal_spon.append(curve((mx[s["member_id"]], 0.0), (bx[name2num[bid]], 1.0)))

fig = plt.figure(figsize=(12, 6.3), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(GROUND)
fig.patch.set_facecolor(GROUND)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.04, 1.04)
ax.axis("off")

ax.add_collection(LineCollection(fog, colors=FOG, linewidths=0.3, alpha=0.09))

def glow(segs, color):
    for lw, a in [(5.0, 0.10), (2.6, 0.22), (1.3, 0.95)]:
        ax.add_collection(LineCollection(segs, colors=color, linewidths=lw, alpha=a,
                                         capstyle="round"))

glow(signal_nay, NAY)
glow(signal_spon, SPON)

fig.savefig(OUT, facecolor=GROUND)
print(f"wrote {OUT} | fog threads={len(fog)} | signal: {len(signal_nay)} nay, {len(signal_spon)} sponsored")
