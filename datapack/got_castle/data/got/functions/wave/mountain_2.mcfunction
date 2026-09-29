title @a title {"text": "The Bloody Gate", "color": "red", "bold": true}
title @a subtitle {"text": "Wave 2 of 3", "color": "gray"}
playsound minecraft:block.bell.use master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/mountain_2_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
