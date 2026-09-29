execute unless score @s got_gold matches 10.. run return run title @s actionbar {"text": "\u0630\u0647\u0628\u0643 \u0644\u0627 \u064a\u0643\u0641\u064a", "color": "red"}
scoreboard players remove @s got_gold 10
loot give @s loot got:shop/horse
title @s actionbar {"text": "\u0627\u0634\u062a\u0631\u064a\u062a: \u062d\u0635\u0627\u0646 \u0648\u0633\u0631\u062c", "color": "green"}
playsound minecraft:entity.villager.trade master @s
