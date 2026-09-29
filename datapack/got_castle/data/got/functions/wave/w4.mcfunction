title @a title {"text": "Wave 4 - The Ironborn", "color": "red", "bold": true}
title @a subtitle {"text": "Enemies are gathering outside the main gate!", "color": "gray"}
playsound minecraft:block.bell.use master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/w4_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
