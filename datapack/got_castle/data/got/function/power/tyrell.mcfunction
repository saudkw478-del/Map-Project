tag @s add got_me
effect give @a[distance=..15] minecraft:instant_health 1 2 true
effect give @a[distance=..15] minecraft:regeneration 12 1 true
particle minecraft:heart ~ ~1.5 ~ 2 0.7 2 0.05 25 force
playsound minecraft:entity.player.levelup master @a[distance=..15]
title @a[distance=..15] actionbar {"text": "\u0648\u0631\u062f \u0627\u0644\u0634\u0641\u0627\u0621!", "color": "green"}
scoreboard players set @s got_pcd 45
tag @s remove got_me
