tag @s add got_me
effect give @s minecraft:strength 12 2 true
effect give @s minecraft:resistance 12 1 true
particle minecraft:angry_villager ~ ~1.5 ~ 0.5 0.5 0.5 0.05 15 force
playsound minecraft:entity.ravager.roar master @a[distance=..30]
title @s actionbar {"text": "\u0644\u0646\u0627 \u0627\u0644\u063a\u0636\u0628!", "color": "yellow"}
scoreboard players set @s got_pcd 45
tag @s remove got_me
