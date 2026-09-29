scoreboard players set #t got_g 0
execute store result score #players got_g if entity @a
execute store result score #enemies got_g if entity @e[tag=got_enemy]
scoreboard players operation Enemies got_g = #enemies got_g
execute if score #state got_g matches 1 run function got:game/running
execute if score #state got_g matches 2 run function got:game/intermission
