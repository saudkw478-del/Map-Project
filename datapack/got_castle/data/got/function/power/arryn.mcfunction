tag @s add got_me
effect give @s minecraft:levitation 2 9 true
effect give @s minecraft:slow_falling 15 0 true
particle minecraft:cloud ~ ~ ~ 0.5 0.1 0.5 0.1 30 force
playsound minecraft:entity.phantom.flap master @a[distance=..20]
title @s actionbar {"text": "\u0642\u0641\u0632\u0629 \u0627\u0644\u0635\u0642\u0631!", "color": "aqua"}
scoreboard players set @s got_pcd 15
tag @s remove got_me
