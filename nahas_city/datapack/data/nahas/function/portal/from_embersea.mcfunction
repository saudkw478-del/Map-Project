scoreboard players set @s nh_pcd 6
particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60
playsound minecraft:block.portal.travel master @s ~ ~ ~ 0.5 1.2
execute in minecraft:overworld run tp @s 300 71 906
tellraw @s {"text":"عدت إلى عالمك الأول.","color":"light_purple"}
particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60
