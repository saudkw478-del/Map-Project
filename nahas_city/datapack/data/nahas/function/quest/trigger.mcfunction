scoreboard players operation @s nh_tmp = @s nh_quest
scoreboard players set @s nh_quest 0
execute if score @s nh_tmp matches 1 run function nahas:quest/main
execute if score @s nh_tmp matches 2 run function nahas:quest/side
execute if score @s nh_tmp matches 11 run function nahas:quest/claim_1
execute if score @s nh_tmp matches 12 run function nahas:quest/claim_2
execute if score @s nh_tmp matches 13 run function nahas:quest/claim_3
execute if score @s nh_tmp matches 14 run function nahas:quest/claim_4
execute if score @s nh_tmp matches 15 run function nahas:quest/claim_5
execute unless score @s nh_tmp matches 1..2 unless score @s nh_tmp matches 11..15 run function nahas:quest/menu
