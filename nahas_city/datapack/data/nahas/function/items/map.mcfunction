scoreboard players operation @s nh_tmp = @s nh_map
scoreboard players set @s nh_map 0
execute if score @s nh_tmp matches 2 run function nahas:items/coords
execute if score @s nh_tmp matches 3 run function nahas:items/list_places
execute unless score @s nh_tmp matches 2..3 run function nahas:items/map_next
