execute unless entity @s[tag=nh_d_starsea] run tellraw @s {"text":"لم تكتشف هذا المكان بعد.","color":"red"}
execute if entity @s[tag=nh_d_starsea] run scoreboard players set @s nh_gocd 45
execute if entity @s[tag=nh_d_starsea] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute if entity @s[tag=nh_d_starsea] run execute in nahas:star_sea run tp @s 600.5 101 605.5
execute if entity @s[tag=nh_d_starsea] run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute if entity @s[tag=nh_d_starsea] run tellraw @s {"text":"وصلت إلى بحر النجوم","color":"aqua"}
execute if entity @s[tag=nh_d_starsea] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
