execute unless score @s got_gold matches 5.. run return run title @s actionbar {"text": "\u0630\u0647\u0628\u0643 \u0644\u0627 \u064a\u0643\u0641\u064a", "color": "red"}
scoreboard players remove @s got_gold 5
loot give @s loot got:shop/heal
title @s actionbar {"text": "\u0627\u0634\u062a\u0631\u064a\u062a: \u0639\u0644\u0627\u062c \u0648\u0637\u0639\u0627\u0645", "color": "green"}
playsound minecraft:entity.villager.trade master @s
