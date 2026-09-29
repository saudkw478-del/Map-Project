tag @s remove role_1
tag @s remove role_2
tag @s remove role_3
tag @s remove role_4
scoreboard players operation @s nh_prole = @s nh_role
execute if score @s nh_role matches 1 run tag @s add role_1
execute if score @s nh_role matches 1 run tellraw @s ["",{"text":"دورك الآن: ","color":"yellow"},{"text":"المستكشف","color":"green","bold":true},{"text":"  (اكتب /trigger nh_power set 1 لاستخدام قوتك)","color":"gray"}]
execute if score @s nh_role matches 2 run tag @s add role_2
execute if score @s nh_role matches 2 run tellraw @s ["",{"text":"دورك الآن: ","color":"yellow"},{"text":"الفارس","color":"red","bold":true},{"text":"  (اكتب /trigger nh_power set 1 لاستخدام قوتك)","color":"gray"}]
execute if score @s nh_role matches 3 run tag @s add role_3
execute if score @s nh_role matches 3 run tellraw @s ["",{"text":"دورك الآن: ","color":"yellow"},{"text":"الحكيم","color":"aqua","bold":true},{"text":"  (اكتب /trigger nh_power set 1 لاستخدام قوتك)","color":"gray"}]
execute if score @s nh_role matches 4 run tag @s add role_4
execute if score @s nh_role matches 4 run tellraw @s ["",{"text":"دورك الآن: ","color":"yellow"},{"text":"الظل","color":"dark_purple","bold":true},{"text":"  (اكتب /trigger nh_power set 1 لاستخدام قوتك)","color":"gray"}]
advancement grant @s only nahas:role
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1.2
particle minecraft:enchant ~ ~1 ~ 0.5 0.8 0.5 0.3 40
