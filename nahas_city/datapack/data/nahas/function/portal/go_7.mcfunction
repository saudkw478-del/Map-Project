execute unless entity @s[tag=nh_d_star] run tellraw @s {"text":"لم تكتشف هذا المكان بعد.","color":"red"}
execute if entity @s[tag=nh_d_star] run scoreboard players set @s nh_gocd 45
execute if entity @s[tag=nh_d_star] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute if entity @s[tag=nh_d_star] run execute in minecraft:overworld run tp @s 1000.5 71 356.5
execute if entity @s[tag=nh_d_star] run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute if entity @s[tag=nh_d_star] run tellraw @s {"text":"وصلت إلى بوابة النجوم","color":"aqua"}
execute if entity @s[tag=nh_d_star] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
