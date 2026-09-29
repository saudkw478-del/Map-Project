execute unless entity @e[tag=got_origin] run return run tellraw @s {"text": "Build the castle first: /function got:build", "color": "red"}
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
time set night
weather clear
function got:util/rules
execute at @e[tag=got_origin,limit=1] run spawnpoint @a ~ ~ ~4
function got:tp/hall
execute as @a run function got:kit/give
title @a title {"text": "The Long Night Begins", "color": "dark_red", "bold": true}
title @a subtitle {"text": "Hold the castle through 7 waves. Slay the Night King!", "color": "gray"}
playsound minecraft:ambient.cave master @a
