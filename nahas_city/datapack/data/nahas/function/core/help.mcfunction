scoreboard players operation @s nh_tmp = @s nh_help
scoreboard players set @s nh_help 0
execute if score @s nh_tmp matches 2 run function nahas:core/kids_on
execute if score @s nh_tmp matches 3 run function nahas:core/kids_off
execute if score @s nh_tmp matches 4 run function nahas:core/help_cmds
execute if score @s nh_tmp matches 5 run function nahas:quest/main
execute if score @s nh_tmp matches 6 run function nahas:core/help_kit
execute if score @s nh_tmp matches 7 run function nahas:core/help_unstuck
execute if score @s nh_tmp matches 8 if entity @s[tag=nh_admin] run function nahas:selftest
execute unless score @s nh_tmp matches 2..8 run function nahas:core/help_menu
