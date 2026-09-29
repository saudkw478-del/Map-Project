#!/usr/bin/env python3
"""Integration/packaging: assemble the final world folder and the dist/*.zip files.
Run after worldgen/build_world.py (which writes worldgen/out/world/NahasCity).
  1. worldgen/make_map_item.py   -> world data/map_0.dat + idcounts.dat
  2. datapack/ -> world datapacks/nahas_city ; resourcepack/ -> world resources.zip (+ icon.png)
  3. worldgen/verify.py (read-back checks)
  4. dist/: Nahas_City_World.zip, _ResourcePack.zip, _Datapack.zip, _Fallback.zip, _AI_Bridge.zip
"""
import os, shutil, subprocess, sys, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
WG = os.path.join(ROOT, "worldgen")
WORLD = os.path.join(WG, "out", "world", "NahasCity")
DIST = os.path.join(ROOT, "dist")
STAMP = (2026, 1, 1, 0, 0, 0)
SKIP = ("__pycache__", ".pyc", ".DS_Store")


def files_under(base):
    for d, dn, fn in os.walk(base):
        dn[:] = sorted(x for x in dn if x not in SKIP)
        for f in sorted(fn):
            if not f.endswith(SKIP[1]) and f not in SKIP:
                yield os.path.join(d, f)


def zip_write(zf, src, arc):
    zi = zipfile.ZipInfo(arc.replace(os.sep, "/"), STAMP)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    with open(src, "rb") as f:
        zf.writestr(zi, f.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def make_zip(path, entries):
    """entries: list of (source file, archive name)"""
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w") as zf:
        for src, arc in entries:
            zip_write(zf, src, arc)
    return os.path.getsize(path)


def tree(base, prefix):
    return [(f, prefix + os.path.relpath(f, base)) for f in files_under(base)]


def main():
    assert os.path.isdir(WORLD), "run worldgen/build_world.py first"
    subprocess.check_call([sys.executable, os.path.join(WG, "make_map_item.py")])
    # datapack into the world
    dp = os.path.join(WORLD, "datapacks", "nahas_city")
    shutil.rmtree(dp, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "datapack"), dp, ignore=shutil.ignore_patterns("__pycache__"))
    # resource pack zip (pack.mcmeta at the zip root)
    rp_dir = os.path.join(ROOT, "resourcepack")
    rp_zip = os.path.join(DIST, "Nahas_City_ResourcePack.zip")
    os.makedirs(DIST, exist_ok=True)
    make_zip(rp_zip, tree(rp_dir, ""))
    shutil.copyfile(rp_zip, os.path.join(WORLD, "resources.zip"))
    try:
        from PIL import Image
        Image.open(os.path.join(rp_dir, "pack.png")).convert("RGB").resize((64, 64), Image.LANCZOS).save(os.path.join(WORLD, "icon.png"))
    except Exception as e:
        print("icon skipped:", e)
    subprocess.check_call([sys.executable, os.path.join(WG, "verify.py")])
    # world zip
    world_entries = tree(WORLD, "NahasCity/")
    sizes = {"Nahas_City_World.zip": make_zip(os.path.join(DIST, "Nahas_City_World.zip"), world_entries)}
    # datapack zip (pack.mcmeta at root)
    sizes["Nahas_City_Datapack.zip"] = make_zip(os.path.join(DIST, "Nahas_City_Datapack.zip"), tree(os.path.join(ROOT, "datapack"), ""))
    sizes["Nahas_City_ResourcePack.zip"] = os.path.getsize(rp_zip)
    # fallback: overlay on a fresh Superflat world folder (datapack + resources.zip + generated regions/dimensions + map)
    fb = [(f, a) for f, a in world_entries
          if a.split("/", 2)[1] in ("datapacks", "resources.zip", "region", "dimensions", "data")]
    fb = [(f, a.split("/", 1)[1]) for f, a in fb]          # drop the NahasCity/ prefix: extract INTO the new world's folder
    sizes["Nahas_City_Fallback.zip"] = make_zip(os.path.join(DIST, "Nahas_City_Fallback.zip"), fb)
    # AI bridge
    ai = os.path.join(ROOT, "ai")
    sizes["Nahas_City_AI_Bridge.zip"] = make_zip(os.path.join(DIST, "Nahas_City_AI_Bridge.zip"), tree(ai, "ai_bridge/"))
    for k, v in sizes.items():
        print(f"{k}: {v / 1e6:.1f} MB")
        assert v < 100 * 1024 * 1024, k + " too big for git"


if __name__ == "__main__":
    main()
