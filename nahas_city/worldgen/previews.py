#!/usr/bin/env python3
"""First-person CONCEPT renders (own voxel renderer, tools/render/voxrender.py -- NOT in-game screenshots)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.environ["GOT_WORLD"] = os.path.join(OUT, "world", "NahasCity", "region")
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "render"))
import numpy as np
import voxrender as vr

vr.Y0, vr.Y1 = 44, 196
extra_rules = [
    ("waxed_oxidized_cut_copper", (70, 160, 130), vr.ROOF, 0), ("oxidized", (70, 160, 130), vr.ROOF, 0),
    ("waxed_weathered_cut_copper", (100, 150, 110), vr.BRICKS, 0), ("weathered", (100, 150, 110), vr.BRICKS, 0),
    ("waxed_exposed_cut_copper", (190, 140, 100), vr.BRICKS, 0), ("waxed_cut_copper", (200, 120, 70), vr.BRICKS, 0),
    ("waxed_copper_block", (200, 120, 70), vr.PLAIN, 0), ("copper", (200, 120, 70), vr.PLAIN, 0),
    ("calcite", (235, 235, 228), vr.STONE, 0), ("smooth_basalt", (50, 50, 56), vr.STONE, 0), ("basalt", (60, 60, 66), vr.STONE, 0),
    ("end_stone", (222, 224, 160), vr.STONE, 0), ("amethyst", (150, 100, 200), vr.PLAIN, 0), ("purpur", (170, 120, 170), vr.PLAIN, 0),
    ("prismarine", (80, 150, 140), vr.BRICKS, 0), ("bookshelf", (130, 95, 55), vr.PLANKS, 0), ("bone_block", (225, 221, 199), vr.PLAIN, 0),
    ("netherrack", (110, 40, 40), vr.STONE, 0), ("lava", (240, 110, 20), vr.PLAIN, 14), ("red_concrete", (200, 40, 40), vr.PLAIN, 0),
    ("white_concrete", (235, 235, 235), vr.PLAIN, 0), ("glowstone", (250, 210, 120), vr.PLAIN, 15), ("sea_lantern", (172, 199, 190), vr.PLAIN, 15),
    ("terracotta", (152, 94, 67), vr.ROOF, 0), ("dirt_path", (150, 120, 70), vr.PLAIN, 0), ("tinted_glass", (60, 50, 70), vr.GLASS, 0),
    ("quartz", (236, 230, 223), vr.PLAIN, 0), ("concrete", (120, 80, 160), vr.PLAIN, 0), ("wool", (200, 60, 60), vr.PLAIN, 0),
    ("end_portal_frame", (60, 120, 100), vr.PLAIN, 0), ("clay", (160, 166, 180), vr.PLAIN, 0), ("sandstone", (216, 203, 155), vr.SAND, 0),
]
thin = [("fence", (110, 80, 45), vr.BARS, 0), ("_wall", (150, 140, 120), vr.BARS, 0), ("chain", (60, 60, 70), vr.BARS, 0),
        ("lightning_rod", (200, 120, 70), vr.BARS, 0), ("end_rod", (240, 240, 230), vr.BARS, 12), ("cobweb", (230, 230, 230), vr.BARS, 0),
        ("amethyst_cluster", (170, 120, 220), vr.BARS, 4), ("skull", (225, 221, 199), vr.SMALLLIGHT, 0), ("bed", (170, 40, 40), vr.PLAIN, 0),
        ("soul_lantern", (90, 200, 220), vr.SMALLLIGHT, 12), ("soul_campfire", (90, 200, 220), vr.SMALLLIGHT, 12)]
vr.RULES[0:0] = thin + extra_rules

SHOTS = [  # name, scene centre cx,cz, eye x,z, yaw, pitch, night, world-subdir
    ("01_spawn_camp_dusk", 300, 2050, 322, 2084, 150, -3, 2, "region"),
    ("02_hub_oasis_village", 600, 1650, 618, 1700, 172, -6, 0, "region"),
    ("03_oasis_temple", 1000, 1900, 1000, 1950, 180, 0, 0, "region"),
    ("04_scorpion_canyon_arena", 1800, 1850, 1800, 1878, 180, -6, 0, "region"),
    ("05_lake_library_bridge", 2100, 1300, 2100, 1385, 180, -5, 0, "region"),
    ("06_wind_fortress", 1700, 450, 1748, 522, 149, -18, 0, "region"),
    ("07_star_gate_night", 1000, 350, 1020, 400, 190, -4, 1, "region"),
    ("08_brass_city_gate", 1200, 1300, 1200, 1395, 180, -5, 0, "region"),
    ("09_city_palace_courtyard", 1200, 1200, 1200, 1236, 180, -10, 0, "region"),
    ("10_ember_gate", 300, 900, 300, 940, 180, -4, 1, "region"),
    ("11_star_sea_arrival", 600, 600, 600, 620, 180, -3, 1, "dimensions/nahas/star_sea/region"),
    ("12_ember_arrival", 500, 500, 500, 535, 180, -4, 1, "dimensions/nahas/ember/region"),
    ("13_sunken_library_main_hall", 2100, 1360, 2100, 1373, 180, 2, 0, "region", 43, 30),
    ("14_star_sea_island_hopping", 560, 590, 572, 596, 90, -6, 1, "dimensions/nahas/star_sea/region", 101, 44),
]


def main():
    from PIL import Image
    os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
    man = json.load(open(os.path.join(OUT, "poi_manifest.json"), encoding="utf-8"))
    only = sys.argv[1:]
    for shot in SHOTS:
        (name, cx, cz, ex, ez, yaw, pitch, night, sub) = shot[:9]
        fixed_y = shot[9] if len(shot) > 9 else None
        vr.Y0 = shot[10] if len(shot) > 10 else 44
        if only and not any(o in name for o in only):
            continue
        vr.WORLD = os.path.join(OUT, 'world', 'NahasCity', sub)
        vr._chunk_cache.clear()
        sc = vr.Scene(cx, cz, radius=150)
        # face the POI: yaw 180 => looking north (-z)... MC yaw 0 = south(+z), 180 = north
        try:
            if fixed_y is not None:
                x, y, z = ex + 0.5, fixed_y, ez + 0.5
            else:
                x, y, z = sc.clear_spot(ex, ez, yaw)
        except Exception:
            x, z = ex + 0.5, ez + 0.5
            y = 101 if 'star' in sub else (65 if 'ember' in sub else sc.ground(ex, ez))
        # stand a bit above ground for a nicer view
        im = sc.shot(x, y, z, yaw, pitch, w=1280, h=720, night=night, maxd=190.0)
        im.save(os.path.join(OUT, "previews", name + ".png"))
        print("saved", name, (x, y, z))


if __name__ == "__main__":
    main()
