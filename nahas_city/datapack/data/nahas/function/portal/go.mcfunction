scoreboard players operation @s nh_tmp = @s nh_go
scoreboard players set @s nh_go 0
execute unless score @s nh_tmp matches 2..13 run function nahas:portal/go_menu
execute if score @s nh_tmp matches 2..13 if score @s nh_gocd matches 1.. run tellraw @s ["",{"text":"انتظر ","color":"red"},{"score":{"name":"@s","objective":"nh_gocd"},"color":"yellow"},{"text":" ثانية قبل السفر مرة أخرى.","color":"red"}]
execute if score @s nh_tmp matches 2 if score @s nh_gocd matches ..0 run function nahas:portal/go_1
execute if score @s nh_tmp matches 3 if score @s nh_gocd matches ..0 run function nahas:portal/go_2
execute if score @s nh_tmp matches 4 if score @s nh_gocd matches ..0 run function nahas:portal/go_3
execute if score @s nh_tmp matches 5 if score @s nh_gocd matches ..0 run function nahas:portal/go_4
execute if score @s nh_tmp matches 6 if score @s nh_gocd matches ..0 run function nahas:portal/go_5
execute if score @s nh_tmp matches 7 if score @s nh_gocd matches ..0 run function nahas:portal/go_6
execute if score @s nh_tmp matches 8 if score @s nh_gocd matches ..0 run function nahas:portal/go_7
execute if score @s nh_tmp matches 9 if score @s nh_gocd matches ..0 run function nahas:portal/go_8
execute if score @s nh_tmp matches 10 if score @s nh_gocd matches ..0 run function nahas:portal/go_9
execute if score @s nh_tmp matches 11 if score @s nh_gocd matches ..0 run function nahas:portal/go_10
execute if score @s nh_tmp matches 12 if score @s nh_gocd matches ..0 run function nahas:portal/go_11
execute if score @s nh_tmp matches 13 if score @s nh_gocd matches ..0 run function nahas:portal/go_12
