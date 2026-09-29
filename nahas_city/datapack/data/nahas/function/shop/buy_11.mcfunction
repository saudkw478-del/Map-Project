scoreboard players set #ok nh_g 0
execute if score @s nh_gold matches 5.. run scoreboard players set #ok nh_g 1
execute if score #ok nh_g matches 1 run function nahas:shop/do_11
execute if score #ok nh_g matches 0 run tellraw @s ["",{"text":"ذهبك لا يكفي لشراء ","color":"red"},{"text":"فانوس جديد","color":"gold"}]
