execute if score @s nh_prole matches 1 run function nahas:role/p1
execute if score @s nh_prole matches 2 run function nahas:role/p2
execute if score @s nh_prole matches 3 run function nahas:role/p3
execute if score @s nh_prole matches 4 run function nahas:role/p4
execute if score @s nh_prole matches 1 run scoreboard players set @s nh_cd 30
execute if score @s nh_prole matches 2 run scoreboard players set @s nh_cd 45
execute if score @s nh_prole matches 3 run scoreboard players set @s nh_cd 40
execute if score @s nh_prole matches 4 run scoreboard players set @s nh_cd 30
execute if score #kids nh_g matches 1 run scoreboard players operation @s nh_cd /= #2 nh_g
