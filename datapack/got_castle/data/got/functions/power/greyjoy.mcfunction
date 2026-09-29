tag @s add got_me
execute as @e[tag=got_enemy,distance=..8] run effect give @s minecraft:levitation 3 3 true
effect give @s minecraft:speed 12 1 true
particle minecraft:splash ~ ~1 ~ 2 0.5 2 0.1 80 force
playsound minecraft:entity.elder_guardian.curse master @a[distance=..20]
title @s actionbar {"text": "\u0627\u0644\u0645\u062f\u0651 \u0648\u0627\u0644\u062c\u0632\u0631!", "color": "dark_aqua"}
scoreboard players set @s got_pcd 40
tag @s remove got_me
