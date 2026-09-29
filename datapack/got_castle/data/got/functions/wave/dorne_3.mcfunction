title @a title {"text": "The Red Viper", "color": "red", "bold": true}
title @a subtitle {"text": "Wave 3 of 4", "color": "gray"}
playsound minecraft:block.bell.use master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/dorne_3_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
