tag @s add got_me
execute as @e[tag=got_enemy,distance=..10] run effect give @s minecraft:poison 8 1 true
execute as @e[tag=got_enemy,distance=..10] run effect give @s minecraft:slowness 8 1 true
effect give @s minecraft:speed 12 2 true
particle minecraft:witch ~ ~1 ~ 1 0.5 1 0.05 40 force
playsound minecraft:entity.spider.ambient master @a[distance=..20]
title @s actionbar {"text": "\u0644\u062f\u063a\u0629 \u0627\u0644\u0623\u0641\u0639\u0649!", "color": "red"}
scoreboard players set @s got_pcd 40
tag @s remove got_me
