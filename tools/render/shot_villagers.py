from shots_common import *
S = vr.Scene(270, 350, 120)
tex = textures()
xs = [250.5 + 1.95 * i for i in range(7)]
ents = [villager(xs[i], 64, 382.5, 180, t) for i, t in enumerate(TYPES)]
im = S.shot(256.5, 64, 372.5, 0, 4, w=1280, h=720, fov=70, ents=ents, textures=tex, maxd=150)
im.save(f"{OUT}/villagers_lineup.png")
for name, idx in (("north", 0), ("nightwatch", 1), ("dorne", 3), ("lannister", 6)):
    x = xs[idx]
    px, pz = x + 0.3, 378.0
    y, p = look_at(px, 64, pz, x, 64 + 1.6, 382.5)
    S.shot(px, 64, pz, y, p, w=1280, h=720, fov=50, ents=ents, textures=tex, maxd=150).save(f"{OUT}/villager_{name}.png")
