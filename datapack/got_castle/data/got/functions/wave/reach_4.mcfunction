title @a title {"text": "The Tyrell Feast Ambush", "color": "red", "bold": true}
title @a subtitle {"text": "Final wave! Hold the castle!", "color": "gray"}
playsound minecraft:entity.wither.spawn master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/reach_4_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
