scoreboard players operation @s nh_tmp = @s nh_kills
scoreboard players operation @s nh_tmp -= @s nh_lastk
scoreboard players operation @s nh_lastk = @s nh_kills
execute if score @s nh_tmp matches 1.. run function nahas:core/gold_kills
execute if score @s nh_cd matches 1.. run scoreboard players remove @s nh_cd 1
execute if score @s nh_cd2 matches 1.. run scoreboard players remove @s nh_cd2 1
execute if score @s nh_gocd matches 1.. run scoreboard players remove @s nh_gocd 1
execute if score @s nh_pcd matches 1.. run scoreboard players remove @s nh_pcd 1
function nahas:core/seal_sync
function nahas:role/second
function nahas:items/second
execute if score #kids nh_g matches 1 run effect give @s minecraft:resistance 3 0 true
execute if score @s nh_gold matches 500.. run advancement grant @s only nahas:rich
