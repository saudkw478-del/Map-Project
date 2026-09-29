execute if score @s got_shop matches 1 run function got:shop/menu
execute if score @s got_shop matches 2 run function got:shop/buy_2
execute if score @s got_shop matches 3 run function got:shop/buy_3
execute if score @s got_shop matches 4 run function got:shop/buy_4
execute if score @s got_shop matches 5 run function got:shop/buy_5
execute if score @s got_shop matches 6 run function got:shop/buy_6
execute if score @s got_shop matches 7 run function got:shop/buy_7
execute if score @s got_shop matches 8 run function got:shop/buy_8
scoreboard players set @s got_shop 0
