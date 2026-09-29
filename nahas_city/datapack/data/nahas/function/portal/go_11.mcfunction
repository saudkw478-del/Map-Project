execute unless entity @s[tag=nh_d_embersea] run tellraw @s {"text":"لم تكتشف هذا المكان بعد.","color":"red"}
execute if entity @s[tag=nh_d_embersea] run scoreboard players set @s nh_gocd 45
execute if entity @s[tag=nh_d_embersea] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute if entity @s[tag=nh_d_embersea] run execute in nahas:ember run tp @s 500.5 65 505.5
execute if entity @s[tag=nh_d_embersea] run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute if entity @s[tag=nh_d_embersea] run tellraw @s {"text":"وصلت إلى أرض الجمر","color":"aqua"}
execute if entity @s[tag=nh_d_embersea] run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
