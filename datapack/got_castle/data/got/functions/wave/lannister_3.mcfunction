title @a title {"text": "Ghosts of the Rock", "color": "red", "bold": true}
title @a subtitle {"text": "Wave 3 of 4", "color": "gray"}
playsound minecraft:block.bell.use master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/lannister_3_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
