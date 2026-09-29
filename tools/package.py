"""Build everything and create the download zips in dist/."""
import os, shutil, subprocess, sys, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py = sys.executable
subprocess.check_call([py, os.path.join(ROOT, "tools", "generate.py")])
subprocess.check_call([py, os.path.join(ROOT, "tools", "world", "makeworld.py")])
dist = os.path.join(ROOT, "dist"); os.makedirs(dist, exist_ok=True)
world = os.path.join(ROOT, "world", "GoT_Westeros")

def add_tree(z, src, arc):
    for base, _, files in os.walk(src):
        for f in files:
            full = os.path.join(base, f)
            z.write(full, os.path.join(arc, os.path.relpath(full, src)))

with zipfile.ZipFile(os.path.join(dist, "GoT_Westeros_Install.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    add_tree(z, world, "GoT_Westeros")
    z.write(os.path.join(ROOT, "install", "Install_Windows.bat"), "Install_Windows.bat")
    z.write(os.path.join(ROOT, "install", "install_mac_linux.sh"), "install_mac_linux.sh")
    z.write(os.path.join(ROOT, "README.md"), "README.md")
with zipfile.ZipFile(os.path.join(dist, "GoT_Westeros_Server_World.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    add_tree(z, world, "world")   # for hosts / Aternos: upload as the server's "world" folder
print("dist:", {f: os.path.getsize(os.path.join(dist, f)) // 1024 // 1024 for f in os.listdir(dist)}, "MB")
