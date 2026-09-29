execute if score @s got_battle matches 2 run function got:game/stop
execute if score @s got_battle matches 1 run function got:battle/try
scoreboard players set @s got_battle 0
