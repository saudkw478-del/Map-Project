function nahas:core/next
clear @s minecraft:compass[minecraft:custom_data={nh:"astrolabe"}]
execute if score #next nh_g matches 0 run loot give @s loot nahas:items/astrolabe_0
execute if score #next nh_g matches 1 run loot give @s loot nahas:items/astrolabe_1
execute if score #next nh_g matches 2 run loot give @s loot nahas:items/astrolabe_2
execute if score #next nh_g matches 3 run loot give @s loot nahas:items/astrolabe_3
execute if score #next nh_g matches 4 run loot give @s loot nahas:items/astrolabe_4
execute if score #next nh_g matches 5 run loot give @s loot nahas:items/astrolabe_5
execute if score #next nh_g matches 6 run loot give @s loot nahas:items/astrolabe_6
execute if score #next nh_g matches 7 run loot give @s loot nahas:items/astrolabe_7
