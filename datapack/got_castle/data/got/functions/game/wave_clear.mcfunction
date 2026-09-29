execute if score #wave got_g >= #total got_g run return run function got:game/victory
scoreboard players set #state got_g 2
scoreboard players set #cool got_g 15
title @a title {"text": "\u0627\u0646\u062a\u0647\u062a \u0627\u0644\u0645\u0648\u062c\u0629!", "color": "green", "bold": true}
effect give @a minecraft:regeneration 10 1 true
effect give @a minecraft:instant_health 1 2 true
loot give @a loot got:reward/supplies
scoreboard players add @a got_gold 8
scoreboard players add @a[tag=got_h_lannister] got_gold 4
scoreboard players add @a got_renown 2
playsound minecraft:entity.player.levelup master @a
