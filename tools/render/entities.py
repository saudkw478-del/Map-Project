"""Entity models (villagers, zombies, skeletons ...) as textured boxes for the concept renderer."""
import numpy as np

SC = 0.9375 / 16.0   # px -> blocks (Minecraft's living-entity scale)


def uvs(U, V, w, h, d):
    """Cube unwrap: faces in order +x(left), -x(right), top, bottom, front(+z), back(-z) -> (u0, v0, du, dv)."""
    return [(U + d + w, V + d, d, h), (U, V + d, d, h), (U + d, V, w, d), (U + d + w, V, w, d),
            (U + d, V + d, w, h), (U + 2 * d + w, V + d, w, h)]


def box(x0, y0, z0, x1, y1, z1, uv=None, color=None, grow=0.0):
    return dict(b=(x0 - grow, y0 - grow, z0 - grow, x1 + grow, y1 + grow, z1 + grow), uv=uv, color=color)


def villager_parts(overlay_hat=True):
    P = []
    P.append(box(-4, 0, -2, 0, 12, 2, uvs(0, 22, 4, 12, 4)))                 # legs
    P.append(box(0, 0, -2, 4, 12, 2, uvs(0, 22, 4, 12, 4)))
    P.append(box(-4, 12, -3, 4, 24, 3, uvs(16, 20, 8, 12, 6)))               # body
    P.append(box(-4, 6, -3, 4, 24, 3, uvs(0, 38, 8, 18, 6), grow=0.5))       # robe / jacket
    P.append(box(-4, 24, -4, 4, 34, 4, uvs(0, 0, 8, 10, 8)))                 # head
    P.append(box(-1, 23, 4, 1, 27, 6, uvs(24, 0, 2, 4, 2)))                  # nose
    P.append(box(-8, 18, 1, -4, 26, 5, uvs(44, 22, 4, 8, 4)))                # crossed arms
    P.append(box(4, 18, 1, 8, 26, 5, uvs(44, 22, 4, 8, 4)))
    P.append(box(-4, 18, 1, 4, 22, 5, uvs(40, 38, 8, 4, 4)))
    if overlay_hat:
        P.append(box(-4, 24, -4, 4, 34, 4, uvs(32, 0, 8, 10, 8), grow=0.5))  # hat layer
    return P


def humanoid_parts(skin, shirt, pants, arms_forward=False, helmet=None, chest=None):
    """Colour-only humanoid (zombie / skeleton / raider). Local +z = front."""
    P = []
    P.append(box(-4, 0, -2, 0, 12, 2, color=pants)); P.append(box(0, 0, -2, 4, 12, 2, color=pants))
    P.append(box(-4, 12, -2, 4, 24, 2, color=shirt))
    P.append(box(-4, 24, -4, 4, 32, 4, color=skin))
    if arms_forward:
        P.append(box(-8, 20, -2, -4, 24, 12, color=skin)); P.append(box(4, 20, -2, 8, 24, 12, color=skin))
    else:
        P.append(box(-8, 12, -2, -4, 24, 2, color=skin)); P.append(box(4, 12, -2, 8, 24, 2, color=skin))
    if helmet:
        P.append(box(-4, 24, -4, 4, 32, 4, color=helmet, grow=0.6))
    if chest:
        P.append(box(-4, 12, -2, 4, 24, 2, color=chest, grow=0.5))
    return P


ZOMBIE = dict(skin=(75, 140, 70), shirt=(0, 150, 175), pants=(70, 55, 150))
SKELETON = dict(skin=(205, 205, 195), shirt=(190, 190, 180), pants=(180, 180, 172))
HUSK = dict(skin=(150, 130, 90), shirt=(120, 100, 70), pants=(90, 75, 55))
VINDICATOR = dict(skin=(150, 160, 140), shirt=(50, 90, 90), pants=(60, 60, 60))
WIGHT = dict(skin=(120, 170, 200), shirt=(60, 90, 120), pants=(50, 70, 100))       # ice-blue undead
WITHER_SKEL = dict(skin=(40, 40, 42), shirt=(35, 35, 38), pants=(35, 35, 38))


def assemble(ents, textures, ground_light=None):
    """ents: list of dict(x, y, z, yaw, parts, tex=index-or--1, scale=1.0). Returns kernel arrays."""
    boxes, pos, cs, col, tex, uv = [], [], [], [], [], []
    for e in ents:
        yaw = np.radians(e.get("yaw", 0.0))
        s = e.get("scale", 1.0) * SC
        for p in e["parts"]:
            b = np.array(p["b"], dtype=np.float64) * s
            boxes.append(b)
            pos.append([e["x"], e["y"], e["z"]])
            cs.append([np.cos(yaw), np.sin(yaw)])
            col.append(p["color"] if p["color"] is not None else (0, 0, 0))
            if p["uv"] is not None and e.get("tex", -1) >= 0:
                tex.append(e["tex"]); uv.append(np.array(p["uv"], dtype=np.float64))
            else:
                tex.append(-1); uv.append(np.zeros((6, 4)))
    n = len(boxes)
    T = np.zeros((max(1, len(textures)), 64, 64, 4), dtype=np.float32)
    for i, t in enumerate(textures):
        T[i] = t
    if n == 0:
        return (np.zeros((0, 6)), np.zeros((0, 3)), np.zeros((0, 2)), np.zeros((0, 3)), np.zeros(0, dtype=np.int32),
                np.zeros((0, 6, 4)), T)
    return (np.array(boxes), np.array(pos, dtype=np.float64), np.array(cs), np.array(col, dtype=np.float64),
            np.array(tex, dtype=np.int32), np.array(uv), T)
