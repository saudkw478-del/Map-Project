title @a title {"text": "The Wildlings Climb the Wall", "color": "red", "bold": true}
title @a subtitle {"text": "Wave 1 of 4", "color": "gray"}
playsound minecraft:block.bell.use master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/wildlings_1_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
