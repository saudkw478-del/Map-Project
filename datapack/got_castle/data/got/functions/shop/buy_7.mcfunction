execute unless score @s got_gold matches 40.. run return run title @s actionbar {"text": "\u0630\u0647\u0628\u0643 \u0644\u0627 \u064a\u0643\u0641\u064a", "color": "red"}
scoreboard players remove @s got_gold 40
loot give @s loot got:shop/totem
title @s actionbar {"text": "\u0627\u0634\u062a\u0631\u064a\u062a: \u062a\u0645\u064a\u0645\u0629 \u0627\u0644\u062e\u0644\u0648\u062f", "color": "green"}
playsound minecraft:entity.villager.trade master @s
