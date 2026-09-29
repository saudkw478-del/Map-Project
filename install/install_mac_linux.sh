#!/bin/sh
# Copies the Westeros world into your Minecraft Java saves folder.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ "$(uname)" = "Darwin" ]; then SAVES="$HOME/Library/Application Support/minecraft/saves"; else SAVES="$HOME/.minecraft/saves"; fi
if [ ! -f "$HERE/GoT_Westeros/level.dat" ]; then echo "GoT_Westeros folder not found next to this script"; exit 1; fi
mkdir -p "$SAVES"
if [ -e "$SAVES/GoT_Westeros" ]; then echo "Already installed at $SAVES/GoT_Westeros (delete it to reinstall)"; exit 0; fi
cp -R "$HERE/GoT_Westeros" "$SAVES/GoT_Westeros"
echo "Done! Open Minecraft Java (1.21+): Singleplayer > Game of Thrones - Westeros"
