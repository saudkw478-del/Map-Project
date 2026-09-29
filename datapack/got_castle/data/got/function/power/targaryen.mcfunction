tag @s add got_me
execute at @s anchored eyes positioned ^ ^ ^5 run particle minecraft:flame ~ ~ ~ 2 1 2 0.08 200 force
execute at @s anchored eyes positioned ^ ^ ^5 as @e[tag=got_enemy,distance=..6] run damage @s 14 minecraft:on_fire by @a[tag=got_me,limit=1]
execute at @s anchored eyes positioned ^ ^ ^5 as @e[tag=got_enemy,distance=..6] run data merge entity @s {Fire:120s}
playsound minecraft:entity.ender_dragon.growl master @a[distance=..40]
title @s actionbar {"text": "\u062f\u0631\u0627\u0643\u0627\u0631\u064a\u0633!", "color": "dark_red"}
scoreboard players set @s got_pcd 30
tag @s remove got_me
