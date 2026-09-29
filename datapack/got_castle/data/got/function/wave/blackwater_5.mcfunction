title @a title {"text": "The Mountain Rides", "color": "red", "bold": true}
title @a subtitle {"text": "Final wave! Hold the castle!", "color": "gray"}
playsound minecraft:entity.wither.spawn master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/blackwater_5_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
