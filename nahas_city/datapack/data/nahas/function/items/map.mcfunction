scoreboard players operation @s nh_tmp = @s nh_map
scoreboard players set @s nh_map 0
execute if score @s nh_tmp matches 2 run function nahas:items/coords
execute if score @s nh_tmp matches 3 run function nahas:items/list_places
execute if score @s nh_tmp matches 4 unless items entity @s container.* minecraft:filled_map run loot give @s loot nahas:items/world_map
execute unless score @s nh_tmp matches 2..4 run function nahas:items/map_next
