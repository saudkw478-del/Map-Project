execute unless entity @s[tag=nh_d_t1] run tellraw @s {"text":"لم تكتشف هذا المكان بعد.","color":"red"}
execute if entity @s[tag=nh_d_t1] run scoreboard players set @s nh_gocd 45
execute if entity @s[tag=nh_d_t1] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute if entity @s[tag=nh_d_t1] run execute in minecraft:overworld run tp @s 1000.5 71 1900.5
execute if entity @s[tag=nh_d_t1] run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute if entity @s[tag=nh_d_t1] run tellraw @s {"text":"وصلت إلى معبد الواحة","color":"aqua"}
execute if entity @s[tag=nh_d_t1] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
