"""Render top-down and elevation previews of the castle from the generator's voxel model."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import castle

COL = {"stone_bricks": "#7a7a7a", "cobblestone": "#5f5f5f", "polished_andesite": "#8d8d8d", "dark_oak_planks": "#4a3520",
       "polished_blackstone_bricks": "#2b2b33", "deepslate_bricks": "#3c3c3c", "iron_bars": "#c0c0c0", "red_wool": "#c0202a",
       "birch_log": "#e8e0c8", "gravel": "#8a8580", "grass_block": "#4a8a3a", "water": "#3050c0", "red_carpet": "#a01818",
       "iron_block": "#d8d8d8", "chiseled_stone_bricks": "#909090", "gray_stained_glass": "#4a5a6a", "spruce_planks": "#7a5a30"}

def color(name):
    base = name.split("[")[0]
    if base in COL: return COL[base]
    if "banner" in base: return "#d02020" if "red" in base else "#202020"
    if "ladder" in base or "torch" in base or "lantern" in base: return "#ffc040"
    if "stairs" in base or "slab" in base: return "#6a6a6a"
    if "fence" in base or "wall" in base: return "#606060"
    return "#a040a0"

vox = {}
for name, fn in castle.STAGES[1:]:
    vox.update(fn().vox)
xs = [k[0] for k in vox]; ys = [k[1] for k in vox]; zs = [k[2] for k in vox]
print("blocks:", len(vox), "x", min(xs), max(xs), "y", min(ys), max(ys), "z", min(zs), max(zs))
fig, axes = plt.subplots(1, 3, figsize=(30, 10))
# top-down: highest block per column
W = 60
img = np.zeros((2 * W + 1, 2 * W + 1, 3))
top = {}
for (x, y, z), b in vox.items():
    if (x, z) not in top or top[(x, z)][0] < y: top[(x, z)] = (y, b)
for (x, z), (y, b) in top.items():
    c = matplotlib.colors.to_rgb(color(b)); f = 0.55 + 0.45 * min(y, 50) / 50
    img[z + W, x + W] = [v * f for v in c]
axes[0].imshow(img, origin="upper"); axes[0].set_title("top (north up, gate at bottom)")
# elevations: south view (x vs y) nearest z max, and east view
def elev(ax, key, axis, title):
    im = np.ones((52, 2 * W + 1, 3)) * np.array([0.7, 0.85, 1.0])
    best = {}
    for (x, y, z), b in vox.items():
        u = x if axis == "x" else z
        depth = z if axis == "x" else -x   # south view: larger z nearer; east view: larger x nearer
        k = (u, y)
        if k not in best or best[k][0] < depth: best[k] = (depth, b)
    for (u, y), (d, b) in best.items():
        if 0 <= y < 52: im[51 - y, u + W] = matplotlib.colors.to_rgb(color(b))
    ax.imshow(im); ax.set_title(title)
elev(axes[1], "s", "x", "south elevation")
elev(axes[2], "e", "z", "east elevation")
plt.tight_layout(); plt.savefig("/tmp/claude-0/prev/castle.png", dpi=60)
