scoreboard players set #d got_g 0
execute as @a run scoreboard players operation #d got_g += @s got_deaths
scoreboard players operation #dd got_g = #d got_g
scoreboard players operation #dd got_g -= #d0 got_g
execute if score #dd got_g matches 7.. run function got:camp/battle_lost
