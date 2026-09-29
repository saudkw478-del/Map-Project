execute if score @s got_scd matches 1.. run return run title @s actionbar {"text": "\u0627\u0644\u063a\u0631\u0627\u0628 \u0645\u062a\u0639\u0628... \u0627\u0646\u062a\u0638\u0631 \u0642\u0644\u064a\u0644\u064b\u0627", "color": "red"}
execute if entity @s[tag=got_scouting] run return 0
execute unless score @s got_id matches 1.. run function got:util/assign_id
scoreboard players set @s got_scoutt 30
scoreboard players set @s got_scd 120
tag @s add got_scouting
tag @s add got_me
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["got_back","got_new_back"]}
execute as @e[type=minecraft:marker,tag=got_new_back] run scoreboard players operation @s got_id = @a[tag=got_me,limit=1] got_id
tag @e[type=minecraft:marker,tag=got_new_back] remove got_new_back
execute if entity @e[tag=got_origin] at @e[tag=got_origin,limit=1] run summon minecraft:bat ~ ~40 ~ {Tags:["got_eye","got_new_eye"],NoAI:1b,NoGravity:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b}
execute unless entity @e[tag=got_origin] at @s run summon minecraft:bat ~ ~40 ~ {Tags:["got_eye","got_new_eye"],NoAI:1b,NoGravity:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b}
execute as @e[type=minecraft:bat,tag=got_new_eye] run scoreboard players operation @s got_id = @a[tag=got_me,limit=1] got_id
tag @e[type=minecraft:bat,tag=got_new_eye] remove got_new_eye
gamemode spectator @s
spectate @e[type=minecraft:bat,tag=got_eye,sort=nearest,limit=1] @s
title @s title {"text": "\u0639\u064a\u0646 \u0627\u0644\u063a\u0631\u0627\u0628", "color": "dark_gray", "bold": true}
title @s subtitle {"text": "\u062a\u0631\u0649 \u0633\u0627\u062d\u0629 \u0627\u0644\u0645\u0639\u0631\u0643\u0629 \u0645\u0646 \u0627\u0644\u0623\u0639\u0644\u0649 \u0644\u0645\u062f\u0629 30 \u062b\u0627\u0646\u064a\u0629", "color": "gray"}
tag @s remove got_me
