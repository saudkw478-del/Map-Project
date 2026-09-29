from shots_common import *
S = vr.Scene(270, 400, 120)
for night in (0, 1):
    im = S.shot(272.5, 74, 391.5, 5, 10, night=night, maxd=170, fov=80, w=480, h=270)
    im.save(f"{OUT}/dbg_{night}.png")
    a = np.array(im).astype(float); print(night, a.mean())
L = S.light_for(1)
ex, ey, ez = 272.5 - S.ox, 74 + 1.62 - vr.Y0, 391.5 - S.oz
print("eye cell", S.g[int(ex), int(ey), int(ez)], S.G.names[S.g[int(ex), int(ey), int(ez)]], "light", L[int(ex), int(ey), int(ez)], "sky light", S.light_for(0)[int(ex), int(ey), int(ez)])
print("levels night:", np.unique(L)[:20])
