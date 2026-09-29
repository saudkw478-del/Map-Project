scoreboard players operation @s nh_tmp = @s nh_power
scoreboard players set @s nh_power 0
execute if score @s nh_tmp matches 2 run function nahas:role/flare
execute unless score @s nh_tmp matches 2 run function nahas:role/active
