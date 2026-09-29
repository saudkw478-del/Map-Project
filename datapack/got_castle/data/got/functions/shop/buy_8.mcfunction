execute unless score @s got_gold matches 20.. run return run title @s actionbar {"text": "\u0630\u0647\u0628\u0643 \u0644\u0627 \u064a\u0643\u0641\u064a", "color": "red"}
scoreboard players remove @s got_gold 20
execute at @s run summon minecraft:iron_golem ~2 ~ ~ {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute at @s run summon minecraft:iron_golem ~-2 ~ ~ {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
title @s actionbar {"text": "\u0627\u0634\u062a\u0631\u064a\u062a: \u062d\u0631\u0633 \u0627\u0644\u0642\u0644\u0639\u0629", "color": "green"}
playsound minecraft:entity.villager.trade master @s
