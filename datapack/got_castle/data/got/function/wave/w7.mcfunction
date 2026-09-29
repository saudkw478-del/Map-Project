title @a title {"text": "FINAL WAVE - The Night King", "color": "red", "bold": true}
title @a subtitle {"text": "The Night King has come. Hold the castle!", "color": "gray"}
playsound minecraft:entity.wither.spawn master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/w7_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
