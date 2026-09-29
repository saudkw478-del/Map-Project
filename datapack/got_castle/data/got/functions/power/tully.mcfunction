tag @s add got_me
effect give @a[distance=..15] minecraft:instant_health 1 1 true
effect give @a[distance=..15] minecraft:absorption 20 2 true
particle minecraft:falling_water ~ ~2 ~ 3 0.5 3 0.1 60 force
playsound minecraft:entity.dolphin.splash master @a[distance=..15]
title @a[distance=..15] actionbar {"text": "\u0627\u0644\u0641\u064a\u0636\u0627\u0646!", "color": "blue"}
scoreboard players set @s got_pcd 45
tag @s remove got_me
