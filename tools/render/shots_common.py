import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "villagers"))
import numpy as np
from PIL import Image
import voxrender as vr, entities as E
import make_pack as mp

OUT = "/tmp/claude-0/prev/shots"
os.makedirs(OUT, exist_ok=True)
TYPES = ["snow", "taiga", "plains", "desert", "savanna", "swamp", "jungle"]


def textures():
    base, outs = mp.build()
    return [np.array(mp.composite(base, outs[t])).astype(np.float32) for t in TYPES]


def villager(x, y, z, yaw, typ):
    return dict(x=x, y=y, z=z, yaw=yaw, parts=E.villager_parts(), tex=TYPES.index(typ))


def zombie(x, y, z, yaw, kind=E.ZOMBIE, **kw):
    return dict(x=x, y=y, z=z, yaw=yaw, parts=E.humanoid_parts(arms_forward=True, **kind, **kw))


def look_at(px, py, pz, tx, ty, tz):
    """MC yaw/pitch to look from (px,py+1.62,pz) at (tx,ty,tz)."""
    dx, dy, dz = tx - px, ty - (py + 1.62), tz - pz
    yaw = np.degrees(np.arctan2(-dx, dz))
    pitch = np.degrees(-np.arctan2(dy, np.hypot(dx, dz)))
    return yaw, pitch
