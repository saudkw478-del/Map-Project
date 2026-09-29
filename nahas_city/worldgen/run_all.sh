#!/usr/bin/env bash
# Rebuild everything: world -> readback verification -> concept renders.  (~2-3 minutes, needs numpy/scipy/Pillow/nbtlib/numba)
set -euo pipefail
cd "$(dirname "$0")"
python3 build_world.py          # writes out/world/NahasCity, poi_manifest.json, terrain_raster.npy, world_map.png
python3 make_map_item.py     # in-game map item data -> world data/map_0.dat
python3 verify.py               # independent .mca / level.dat read-back checks (exit 1 on failure)
python3 previews.py             # out/previews/*.png  (concept renders by tools/render/voxrender.py, NOT in-game screenshots)
