scoreboard players set @s got_gift 2400
loot give @s loot got:reward/supplies
scoreboard players add @s got_gold 3
tellraw @s {"text": "\u0636\u063a\u0637 \u0627\u0644\u0642\u0631\u0648\u064a \u0641\u064a \u064a\u062f\u0643 \u0645\u0624\u0648\u0646\u0629 \u0648\u062b\u0644\u0627\u062b \u0642\u0637\u0639 \u0645\u0646 \u0627\u0644\u0630\u0647\u0628.", "color": "green"}
playsound minecraft:entity.villager.celebrate master @s
