scoreboard players operation @s nh_tmp = @s nh_shop
scoreboard players set @s nh_shop 0
execute if score @s nh_tmp matches 2 run function nahas:shop/buy_1
execute if score @s nh_tmp matches 3 run function nahas:shop/buy_2
execute if score @s nh_tmp matches 4 run function nahas:shop/buy_3
execute if score @s nh_tmp matches 5 run function nahas:shop/buy_4
execute if score @s nh_tmp matches 6 run function nahas:shop/buy_5
execute if score @s nh_tmp matches 7 run function nahas:shop/buy_6
execute if score @s nh_tmp matches 8 run function nahas:shop/buy_7
execute if score @s nh_tmp matches 9 run function nahas:shop/buy_8
execute if score @s nh_tmp matches 10 run function nahas:shop/buy_9
execute if score @s nh_tmp matches 11 run function nahas:shop/buy_10
execute if score @s nh_tmp matches 12 run function nahas:shop/buy_11
execute if score @s nh_tmp matches 13 run function nahas:shop/buy_12
execute if score @s nh_tmp matches 20 run function nahas:shop/sell_ingots
execute if score @s nh_tmp matches 21 run function nahas:shop/sell_nuggets
execute unless score @s nh_tmp matches 2..13 unless score @s nh_tmp matches 20..21 run function nahas:shop/menu
