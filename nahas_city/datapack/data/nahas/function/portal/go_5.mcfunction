execute unless entity @s[tag=nh_d_t3] run tellraw @s {"text":"لم تكتشف هذا المكان بعد.","color":"red"}
execute if entity @s[tag=nh_d_t3] run scoreboard players set @s nh_gocd 45
execute if entity @s[tag=nh_d_t3] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute if entity @s[tag=nh_d_t3] run execute in minecraft:overworld run tp @s 2100.5 71 1300.5
execute if entity @s[tag=nh_d_t3] run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute if entity @s[tag=nh_d_t3] run tellraw @s {"text":"وصلت إلى المكتبة الغارقة","color":"aqua"}
execute if entity @s[tag=nh_d_t3] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
