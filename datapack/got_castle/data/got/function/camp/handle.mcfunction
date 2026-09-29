execute if score @s got_start matches 1 run function got:camp/menu
execute if score @s got_start matches 2 run function got:camp/start_short
execute if score @s got_start matches 3 run function got:camp/start_long
execute if score @s got_start matches 4 run function got:camp/stop
scoreboard players set @s got_start 0
