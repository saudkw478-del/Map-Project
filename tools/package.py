"""Build everything and create the download zips in dist/."""
import os, shutil, subprocess, sys, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py = sys.executable
run = lambda *a: subprocess.check_call([py, os.path.join(ROOT, *a)])
run("tools", "world", "makeworld.py")          # world + npcs.json
run("tools", "villagers", "make_pack.py")      # villager resource pack
run("tools", "generate.py")                    # datapack (reads npcs.json)
dist = os.path.join(ROOT, "dist"); os.makedirs(dist, exist_ok=True)
world = os.path.join(ROOT, "world", "GoT_Westeros")

def add_tree(z, src, arc):
    for base, _, files in os.walk(src):
        for f in files:
            full = os.path.join(base, f)
            z.write(full, os.path.join(arc, os.path.relpath(full, src)))

rp_zip = os.path.join(dist, "GoT_Villagers_ResourcePack.zip")
with zipfile.ZipFile(rp_zip, "w", zipfile.ZIP_DEFLATED) as z:
    add_tree(z, os.path.join(ROOT, "resourcepack", "GoT_Villagers"), "")
dp = os.path.join(world, "datapacks", "got_castle")
if os.path.exists(dp):
    shutil.rmtree(dp)
shutil.copytree(os.path.join(ROOT, "datapack", "got_castle"), dp)
shutil.copy(rp_zip, os.path.join(world, "resources.zip"))   # auto-applied in single player

with zipfile.ZipFile(os.path.join(dist, "GoT_Westeros_Install.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    add_tree(z, world, "GoT_Westeros")
    z.write(rp_zip, "GoT_Villagers_ResourcePack.zip")
    z.write(os.path.join(ROOT, "install", "Install_Windows.bat"), "Install_Windows.bat")
    z.write(os.path.join(ROOT, "install", "install_mac_linux.sh"), "install_mac_linux.sh")
    z.write(os.path.join(ROOT, "README.md"), "README.md")
with zipfile.ZipFile(os.path.join(dist, "GoT_Westeros_Server_World.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    add_tree(z, world, "world")   # for hosts / Aternos: upload as the server's "world" folder
with zipfile.ZipFile(os.path.join(dist, "GoT_Westeros_Fallback.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    # for a normal Superflat world created in the game: replace its region folder + add datapack and resources
    add_tree(z, os.path.join(world, "region"), "region")
    add_tree(z, os.path.join(world, "datapacks"), "datapacks")
    z.write(os.path.join(world, "resources.zip"), "resources.zip")
print("dist:", {f: round(os.path.getsize(os.path.join(dist, f)) / 1048576, 1) for f in os.listdir(dist)}, "MB")
