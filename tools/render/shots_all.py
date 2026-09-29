import sys, time
from shots_common import *
import random
which = set(sys.argv[1:])
def want(*n): return not which or bool(which & set(n))
tex = textures()
rnd = random.Random(4)
T0 = time.time()
def save(im, name):
    im.save(f"{OUT}/{name}.png"); print(f"[{time.time()-T0:6.1f}s] {name}", flush=True)

def army(x0, x1, z0, z1, rows, per, yaw, kinds, rnd):
    ents = []
    for r in range(rows):
        for i in range(per):
            x = x0 + (x1 - x0) * (i + 0.5) / per + rnd.uniform(-1.2, 1.2) + (r % 2) * 1.5
            z = z0 + (z1 - z0) * r / max(1, rows - 1) + rnd.uniform(-1.2, 1.2)
            k = rnd.choice(kinds)
            helm = rnd.choice([None, None, (190, 190, 195)])
            ents.append(zombie(x, 64, z, yaw + rnd.uniform(-20, 20), k, helmet=helm))
    return ents

# ---------------------------------------------------------------- Winterfell
if want("01_winterfell_spawn", "02_winterfell_gate", "03_night_battle", "11_godswood", "12_armory"):
    S = vr.Scene(270, 400, 190)
    if want("01_winterfell_spawn"):
        ents = [villager(264.5, 64, 379.5, 80, "snow"), villager(277.5, 64, 384.5, 250, "snow"), villager(273.5, 64, 372.5, 20, "taiga")]
        save(S.shot(270.5, 64, 392.5, 180, 4, ents=ents, textures=tex, maxd=200, fov=75), "01_winterfell_spawn")
    if want("02_winterfell_gate"):
        x, y, z = S.clear_spot(270, 480, 180)
        save(S.shot(x, y, z, 180, 3, maxd=300, fov=75), "02_winterfell_gate")
    if want("03_night_battle"):
        ents = army(262, 318, 402, 418, 3, 11, 180, [E.ZOMBIE, E.ZOMBIE, E.HUSK, E.WIGHT], rnd)
        for i in range(7):
            ents.append(dict(x=260 + i * 9, y=64, z=432 + rnd.uniform(-1, 1), yaw=180, parts=E.humanoid_parts(**E.SKELETON, helmet=(120, 120, 125))))
        ents.append(villager(285.5, 74, 393.5, 0, "snow"))
        save(S.shot(291.5, 75, 394.5, 4, 19, night=2, ents=ents, textures=tex, maxd=170, fov=85), "03_night_battle")
    if want("11_godswood"):
        y, p = look_at(290.5, 64, 378.5, 303.5, 68, 369)
        save(S.shot(290.5, 64, 378.5, y, p, maxd=160, fov=75), "11_godswood_weirwood")
    if want("12_armory"):
        save(S.shot(239.5, 64, 364.5, 0, 12, maxd=100, fov=80), "12_armory_interior")

# ---------------------------------------------------------------- Castle Black & the Wall
if want("05_wall_from_below", "06_atop_wall", "07_castle_black", "15_beyond_wall"):
    S = vr.Scene(250, 200, 190)
    if want("05_wall_from_below"):
        save(S.shot(250.5, 84, 216.5, 180, -13, maxd=260, fov=90), "05_wall_from_castle_black")
    if want("06_atop_wall"):
        save(S.shot(196.5, 136, 173.5, 270, 4, maxd=330, fov=85), "06_atop_the_wall")
    if want("07_castle_black"):
        x, y, z = S.clear_spot(250, 300, 180)
        ents = [villager(x + 3, y, z - 12, 180, "taiga"), villager(x - 4, y, z - 14, 160, "taiga")]
        save(S.shot(x, y, z, 180, 12, maxd=300, fov=80, ents=ents, textures=tex), "07_castle_black")
    if want("15_beyond_wall"):
        ents = army(228, 274, 132, 158, 3, 8, 0, [E.WIGHT, E.WIGHT, E.ZOMBIE], rnd)
        for e in ents:
            e["y"] = S.ground(e["x"], e["z"])
        x, y, z = S.clear_spot(250, 112, 0)
        y += 3
        save(S.shot(x, y + 6, z, 0, -3, maxd=260, fov=95), "15_beyond_the_wall")

# ---------------------------------------------------------------- King's Landing
if want("04_throne_room", "08_kings_landing", "10_iron_throne"):
    S = vr.Scene(405, 900, 190)
    if want("04_throne_room"):
        ents = [villager(400.5, 64, 872.5, 0, "jungle"), villager(410.5, 64, 868.5, 20, "jungle")]
        save(S.shot(405.5, 64, 890.5, 180, 3, ents=ents, textures=tex, maxd=90, fov=80), "04_throne_room")
    if want("10_iron_throne"):
        save(S.shot(405.5, 66, 868.0, 180, -6, maxd=60, fov=70), "10_iron_throne")
    if want("08_kings_landing"):
        x, y, z = S.clear_spot(388, 1000, 176)
        save(S.shot(x, y, z, 176, 4, maxd=300, fov=75), "08_kings_landing")

# ---------------------------------------------------------------- landmarks / other castles
if want("09_eyrie"):
    S = vr.Scene(480, 700, 190)
    x, y, z = S.clear_spot(395, 745, 300)
    yw, pt = look_at(x, y, z, 500, 128, 690)
    print("eyrie cam", x, y, z, yw, pt)
    save(S.shot(x, y, z, yw, pt, maxd=330, fov=85), "09_eyrie")
if want("13_harrenhal"):
    S = vr.Scene(340, 800, 190)
    x, y, z = S.clear_spot(340, 738, 0)
    save(S.shot(x, y, z, 0, 6, maxd=300, fov=80), "13_harrenhal")
if want("14_haunted_forest"):
    S = vr.Scene(250, 130, 190)
    x, y, z = S.clear_spot(250, 150, 200)
    save(S.shot(x, y, z, 200, 3, maxd=200, fov=80), "14_haunted_forest")
if want("16_highgarden"):
    S = vr.Scene(215, 1040, 190)
    x, y, z = S.clear_spot(215, 1110, 180)
    ents = [villager(x + 2, y, z - 8, 180, "savanna"), villager(x - 3, y, z - 10, 150, "savanna")]
    save(S.shot(x, y, z, 180, 6, maxd=300, fov=80, ents=ents, textures=tex), "16_highgarden")
if want("17_sunspear"):
    S = vr.Scene(470, 1235, 190)
    x, y, z = S.clear_spot(470, 1298, 180)
    ents = [villager(x + 2, y, z - 8, 180, "desert"), villager(x - 3, y, z - 10, 150, "desert")]
    save(S.shot(x, y, z, 180, 6, maxd=300, fov=80, ents=ents, textures=tex), "17_sunspear")
if want("18_casterly_rock"):
    S = vr.Scene(140, 800, 190)
    x, y, z = S.clear_spot(140, 885, 180)
    ents = [villager(x + 2, y, z - 8, 180, "jungle"), villager(x - 3, y, z - 10, 150, "jungle")]
    save(S.shot(x, y, z, 180, 6, maxd=300, fov=80, ents=ents, textures=tex), "18_casterly_rock")
