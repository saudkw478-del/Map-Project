execute if score @s got_house matches 1 run function got:house/menu
execute if score @s got_house matches 2 run function got:house/pick_stark
execute if score @s got_house matches 3 run function got:house/pick_lannister
execute if score @s got_house matches 4 run function got:house/pick_targaryen
execute if score @s got_house matches 5 run function got:house/pick_martell
execute if score @s got_house matches 6 run function got:house/pick_tyrell
execute if score @s got_house matches 7 run function got:house/pick_baratheon
execute if score @s got_house matches 8 run function got:house/pick_greyjoy
execute if score @s got_house matches 9 run function got:house/pick_arryn
execute if score @s got_house matches 10 run function got:house/pick_tully
scoreboard players set @s got_house 0
