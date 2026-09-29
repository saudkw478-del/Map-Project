execute if score #wave got_g >= #total got_g run return run function got:game/victory
scoreboard players set #state got_g 2
scoreboard players set #cool got_g 15
title @a title {"text": "Wave cleared!", "color": "green", "bold": true}
effect give @a minecraft:regeneration 10 1 true
effect give @a minecraft:instant_health 1 2 true
loot give @a loot got:reward/supplies
playsound minecraft:entity.player.levelup master @a
