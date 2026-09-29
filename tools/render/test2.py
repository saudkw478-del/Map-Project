import sys, time
sys.path.insert(0, '.')
import voxrender as vr, entities as E
S = vr.Scene(270, 350, 170)
ents = []
for i, (dx, dz) in enumerate([(-6, -14), (4, -10), (-2, -22), (8, -18), (-9, -8)]):
    ents.append(dict(x=270 + dx + .5, y=64, z=380 + dz + .5, yaw=(i * 40) % 360, parts=E.humanoid_parts(arms_forward=True, **E.ZOMBIE)))
ents.append(dict(x=274.5, y=64, z=372.5, yaw=200, parts=E.humanoid_parts(**E.SKELETON)))
t = time.time()
im = S.shot(270.5, 64, 384.5, 180, 8, w=1280, h=720, ents=ents)
print("render", time.time() - t)
im.save("/tmp/claude-0/prev/shots/test2.png")
