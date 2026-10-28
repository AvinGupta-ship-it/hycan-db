#!/usr/bin/env python3
"""Series-isolated images of Figure 1 (HYC-0046, page 3), for digitize_figure.py.

Figure 1 is greyscale: the five isotherms differ only by marker shape, so the
colour mask of digitize_figure.py cannot separate them. This script splits the
plot's connected pixel groups by marker class and writes one image per series
(black marker pixels on white, same pixel grid as the page image, so the axis
calibration read off the page image applies unchanged). No pixel is moved or
rescaled; pixels are copied from the page image.

Marker classes (measured on isolated markers of the same figure):
  circle   (2550 m2/g)  bold black ring, 7-9 px wide and tall, 21-30 black px
  square   (2000 m2/g)  bold black ring, 5-6 px wide and tall, 18-20 black px
  triangle (3200 m2/g)  thin grey sides, black base bar >= 5 px, no top bar
  diamond  (1460 m2/g)  thin grey, no bar
  invtri   (330 m2/g)   thin grey sides, black top bar >= 6 px, no base bar
Bold classes use pixels with grey < 90; thin classes use pixels with grey < 235.
Groups that fuse two or more markers (overlap near the y axis) are not
assigned to any series and are listed as unassigned. One fused pair at
p ~ 36 bar (3200 triangle + 2550 circle) is split at pixel column 1055: the
ring's black pixels with x >= 1055 are the circle, the thin-mask pixels with
x <= 1054 and y <= 759 are the triangle.
"""
import json
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

PAGE = sys.argv[1]
OUT = sys.argv[2]

g = np.asarray(Image.open(PAGE).convert("L")).astype(int)
H, W = g.shape

# plot interior (frame lines excluded), minus tick marks and the legend block
X0, X1, Y0, Y1 = 731, 1091, 720, 972
inter = np.full(g.shape, 255)
inter[Y0:Y1 + 1, X0:X1 + 1] = g[Y0:Y1 + 1, X0:X1 + 1]
for r in (753, 797, 841, 885, 929):
    inter[r, 731:738] = 255
    inter[r, 1086:1092] = 255
for c in (821, 912, 1002):
    inter[966:973, c] = 255
inter[836:926, 948:1040] = 255          # legend swatches and legend text

S8 = np.ones((3, 3))


def longest_run(row):
    best = run = 0
    for v in row:
        run = run + 1 if v else 0
        best = max(best, run)
    return best


assigned = {k: np.zeros(g.shape, bool) for k in ("circle", "square", "triangle", "diamond", "invtri")}
log = {k: [] for k in assigned}
unassigned = []

# ---- bold classes (black-only mask) ---------------------------------------
blk = inter < 90
lab, n = ndimage.label(blk, structure=S8)
for i, sl in enumerate(ndimage.find_objects(lab), start=1):
    ys, xs = sl
    h = ys.stop - ys.start
    w = xs.stop - xs.start
    m = lab[sl] == i
    cnt = int(m.sum())
    if h <= 2 and w >= 5:
        continue                                  # base or top bar of a thin marker
    if cnt < 6:
        continue                                  # speckle / stray anti-aliasing core
    full = np.zeros(g.shape, bool)
    full[sl] = m
    cx = float(np.nonzero(full)[1].mean())
    cy = float(np.nonzero(full)[0].mean())
    if xs.start >= 1050 and ys.start >= 753 and ys.start < 765 and w >= 12:
        # fused triangle-bar + circle ring: keep the ring (x >= 1055)
        ring = full.copy()
        ring[:, :1055] = False
        assigned["circle"] |= ring
        log["circle"].append(("fused pair, ring split at x>=1055", cnt, float(np.nonzero(ring)[1].mean()), float(np.nonzero(ring)[0].mean())))
        continue
    if 7 <= w <= 9 and 7 <= h <= 9 and 21 <= cnt <= 30:
        assigned["circle"] |= full
        log["circle"].append(("single", cnt, cx, cy))
    elif 5 <= w <= 6 and 5 <= h <= 6 and 18 <= cnt <= 20:
        assigned["square"] |= full
        log["square"].append(("single", cnt, cx, cy))
    elif cnt >= 21:
        unassigned.append(("bold group not a single marker (overlap)", cnt, w, h, cx, cy))

# ---- thin classes (thr 235 mask) ------------------------------------------
thin = inter < 235
bold_assigned = assigned["circle"] | assigned["square"]
bold_dilated = ndimage.binary_dilation(bold_assigned, structure=S8)
lab2, n2 = ndimage.label(thin, structure=S8)
for i, sl in enumerate(ndimage.find_objects(lab2), start=1):
    ys, xs = sl
    h = ys.stop - ys.start
    w = xs.stop - xs.start
    m = lab2[sl] == i
    cnt = int(m.sum())
    if cnt < 6:
        continue
    if (m & bold_dilated[sl]).sum() >= 0.85 * cnt:
        continue                                  # a single bold marker, already assigned
    sub = g[sl]
    black = (sub < 90) & m
    nb = int(black.sum())
    runs = [longest_run(black[r]) for r in range(h)]
    top_bar = max(runs[:2]) if h >= 2 else 0
    bot_bar = max(runs[-2:]) if h >= 2 else 0
    full = np.zeros(g.shape, bool)
    full[sl] = m
    cx = float(np.nonzero(full)[1].mean())
    cy = float(np.nonzero(full)[0].mean())
    if xs.start >= 1050 and ys.start >= 753 and ys.start < 765 and w >= 12:
        tri = full.copy()
        tri[:, 1055:] = False
        tri[760:, :] = False
        assigned["triangle"] |= tri
        log["triangle"].append(("fused pair, triangle split at x<=1054,y<=759", int(tri.sum()), float(np.nonzero(tri)[1].mean()), float(np.nonzero(tri)[0].mean())))
        continue
    if w <= 8 and h <= 8 and nb <= 8 and cnt <= 30:
        if bot_bar >= 5 and top_bar <= 1:
            assigned["triangle"] |= full
            log["triangle"].append(("single", cnt, cx, cy))
        elif top_bar >= 6 and bot_bar <= 1:
            assigned["invtri"] |= full
            log["invtri"].append(("single", cnt, cx, cy))
        elif top_bar <= 1 and bot_bar <= 1:
            assigned["diamond"] |= full
            log["diamond"].append(("single", cnt, cx, cy))
        else:
            unassigned.append(("thin group of unclear class", cnt, w, h, cx, cy))
    elif nb < 21 or cnt > 30:
        unassigned.append(("thin group fusing several markers (overlap)", cnt, w, h, cx, cy))

NAMES = {"circle": "2550", "square": "2000", "triangle": "3200", "diamond": "1460", "invtri": "330"}
for k, mask in assigned.items():
    img = np.full((H, W, 3), 255, np.uint8)
    img[mask] = (0, 0, 0)
    Image.fromarray(img).save(f"{OUT}/fig1_series_{NAMES[k]}.png")

summary = {NAMES[k]: {"class": k, "n_groups": len(v), "groups": [list(x) for x in v]} for k, v in log.items()}
summary["unassigned"] = [list(u) for u in unassigned]
json.dump(summary, open(f"{OUT}/series_assignment.json", "w"), indent=1)
for k, v in log.items():
    print(f"{NAMES[k]:>5} m2/g  {k:<8} {len(v):2d} groups")
print("unassigned groups:")
for u in unassigned:
    print("  ", u)
