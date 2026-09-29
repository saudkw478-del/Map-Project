tag @s add got_me
execute unless score @s got_gold matches 30.. run return run title @s actionbar {"text": "\u062a\u062d\u062a\u0627\u062c 30 \u0630\u0647\u0628\u064b\u0627", "color": "red"}
scoreboard players remove @s got_gold 30
execute at @s run summon minecraft:iron_golem ~2 ~ ~ {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute at @s run summon minecraft:iron_golem ~-2 ~ ~ {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute at @s run summon minecraft:iron_golem ~ ~ ~2 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
playsound minecraft:entity.iron_golem.repair master @a[distance=..30]
title @s actionbar {"text": "\u0627\u0644\u062f\u064e\u0651\u064a\u0646 \u0633\u064f\u062f\u0650\u0651\u062f: 3 \u062d\u0631\u0627\u0633!", "color": "gold"}
scoreboard players set @s got_pcd 90
tag @s remove got_me
