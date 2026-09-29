import time, sys
sys.path.insert(0, '.')
import voxrender as vr
t = time.time()
S = vr.Scene(270, 350, 170)
print("scene", time.time() - t, S.g.shape, len(S.G.names))
t = time.time()
im = S.shot(270, 64, 380, 180, 8, w=640, h=360)
print("render", time.time() - t)
im.save("/tmp/claude-0/prev/shots/test1.png")
t = time.time()
im = S.shot(270, 64, 380, 180, 8, w=1280, h=720)
print("render2", time.time() - t)
im.save("/tmp/claude-0/prev/shots/test1_hd.png")
