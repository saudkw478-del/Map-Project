scoreboard players set @s nh_pcd 6
particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60
playsound minecraft:block.portal.travel master @s ~ ~ ~ 0.5 1.2
execute in nahas:ember run tp @s 500 65 505
tag @s add nh_d_embersea
advancement grant @s only nahas:portal
tellraw @s {"text":"عبرت البوابة إلى أرض الجمر...","color":"light_purple"}
particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60
