"""Post-process canvases so fences / walls / glass panes / iron bars get proper connection properties
(chunks written directly are NOT neighbour-updated by the game on load, so unconnected posts would show)."""
import re
import numpy as np
from wg_core import R, B, SKIP
from anvil import parse_block

NOT_SOLID = re.compile(r"slab|stairs|_wall|fence|pane|door|trapdoor|button|plate|sign|lantern|campfire|chest|barrel|bed$|_bed|carpet|torch|ladder|rod|cluster|"
                       r"skull|cobweb|bars|lectern|brewing|water|lava|chain|banner|cactus|leaves|end_rod|dead_bush|flower|sugar|frame|melon|air")
SOLID_HINT = re.compile(r"planks|_log|_wood|stone|bricks|sandstone|terracotta|wool|_block|blackstone|basalt|deepslate|concrete|cobblestone|andesite|diorite|"
                        r"granite|prismarine|calcite|bookshelf|copper|dirt|sand$|gravel|quartz|purpur|obsidian|glass$|smooth_|cut_|chiseled|polished|bedrock|tuff|clay|mud|hay|barrel")


def family(name):
    n = name.replace("minecraft:", "")
    if n.endswith("_fence") or n == "nether_brick_fence":
        return "fence"
    if n.endswith("glass_pane") or n == "iron_bars":
        return "pane"
    if n.endswith("_wall") and "sign" not in n and "torch" not in n and "banner" not in n:
        return "wall"
    return None


def link(canvases):
    """Modify canvases in place."""
    names = list(R.names)   # snapshot of ids that exist so far
    fam = {}
    solid = np.zeros(len(names) + 4096, bool)
    for i, nm in enumerate(names):
        base = nm.split("[")[0]
        f = family(base)
        if f and "[" not in nm:
            fam[i] = (f, base)
        short = base.replace("minecraft:", "")
        if i and not NOT_SOLID.search(short) and SOLID_HINT.search(short):
            solid[i] = True
    # variant tables
    var = {}
    for i, (f, base) in fam.items():
        tab = np.zeros(16, np.uint16)
        for m in range(16):
            n, e, s, w = (m & 1) > 0, (m & 2) > 0, (m & 4) > 0, (m & 8) > 0
            if f == "wall":
                def c(v): return "low" if v else "none"
                up = not ((n and s and not e and not w) or (e and w and not n and not s))
                st = f"{base}[east={c(e)},north={c(n)},south={c(s)},up={'true' if up else 'false'},west={c(w)}]"
            else:
                st = f"{base}[east={str(e).lower()},north={str(n).lower()},south={str(s).lower()},west={str(w).lower()}]"
            tab[m] = B(st)
        var[i] = tab
    solid = np.concatenate([solid, np.zeros(max(0, len(R.names) + 8 - len(solid)), bool)])
    total = 0
    for cv in canvases:
        a = cv.arr
        uniq = np.unique(a)
        present = [int(u) for u in uniq if int(u) in fam]
        if not present:
            continue
        sol = solid[np.minimum(a, len(solid) - 1)] & (a != SKIP)
        for fid in present:
            f = fam[fid][0]
            isf = a == fid
            allf = np.zeros(a.shape, bool)
            for j, (ff, _) in fam.items():
                if ff == f or (f == "pane" and ff == "pane"):
                    pass
            # neighbours may be any block of the same family, or solid blocks
            famany = np.isin(a, [k for k, v in fam.items() if v[0] == f])
            ok = famany | sol
            m = np.zeros(a.shape, np.uint8)
            # north = -z, south = +z, west = -x, east = +x   (axes: y,z,x)
            m[:, 1:, :] |= np.where(ok[:, :-1, :], 1, 0).astype(np.uint8)      # north neighbour at z-1
            m[:, :-1, :] |= np.where(ok[:, 1:, :], 4, 0).astype(np.uint8)      # south neighbour at z+1
            m[:, :, :-1] |= np.where(ok[:, :, 1:], 2, 0).astype(np.uint8)      # east neighbour at x+1
            m[:, :, 1:] |= np.where(ok[:, :, :-1], 8, 0).astype(np.uint8)      # west neighbour at x-1
            idx = np.nonzero(isf)
            a[idx] = var[fid][m[idx]]
            total += len(idx[0])
    return total
