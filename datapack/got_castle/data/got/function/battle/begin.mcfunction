kill @e[tag=got_enemy]
scoreboard objectives add got_g dummy {"text": "Game of Thrones", "color": "gold"}
scoreboard players set #state got_g 2
scoreboard players set #cool got_g 12
scoreboard players set #wave got_g 0
scoreboard players set #t got_g 0
scoreboard players set Wave got_g 0
scoreboard players set Enemies got_g 0
scoreboard objectives setdisplay sidebar got_g
difficulty normal
weather clear
function got:util/rules
execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run spawnpoint @s ~ ~ ~4
execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run function got:battle/prepare
title @a title {"text": "To Arms!", "color": "dark_red", "bold": true}
title @a subtitle {"text": "Defend the castle. Grab weapons from the armory!", "color": "gray"}
