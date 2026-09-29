kill @e[tag=got_enemy]
scoreboard players set #state got_g 2
scoreboard players set #cool got_g 12
scoreboard players set #wave got_g 0
scoreboard players set #t2 got_g 0
scoreboard players set #enemies got_g 0
difficulty normal
function got:util/weather_clear
function got:util/rules
scoreboard players set #d got_g 0
execute as @a run scoreboard players operation #d got_g += @s got_deaths
scoreboard players operation #d0 got_g = #d got_g
execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run spawnpoint @s ~ ~ ~4
execute at @e[tag=got_origin,limit=1] as @a[distance=..130] run function got:battle/prepare
title @a title {"text": "\u0625\u0644\u0649 \u0627\u0644\u0633\u0644\u0627\u062d!", "color": "dark_red", "bold": true}
title @a subtitle {"text": "\u0627\u062d\u0645\u0650 \u0627\u0644\u0642\u0644\u0639\u0629. \u062e\u0630 \u0627\u0644\u0623\u0633\u0644\u062d\u0629 \u0645\u0646 \u0627\u0644\u0645\u062e\u0632\u0646 \u0623\u0648\u0644\u064b\u0627!", "color": "gray"}
