scoreboard players set #t got_g 0
execute store result score #players got_g if entity @a
execute store result score #enemies got_g if entity @e[tag=got_enemy]
execute as @a at @s run function got:region/one
scoreboard players remove @a[scores={got_talkcd=1..}] got_talkcd 1
scoreboard players remove @a[scores={got_gift=1..}] got_gift 1
scoreboard players remove @a[scores={got_pcd=1..}] got_pcd 1
scoreboard players remove @a[scores={got_scd=1..}] got_scd 1
scoreboard players remove @a[scores={got_scoutt=1..}] got_scoutt 1
execute as @a[tag=got_scouting,scores={got_scoutt=..0}] run function got:scout/end
scoreboard players add #s5 got_g 1
execute if score #s5 got_g matches 5.. run function got:house/passives
scoreboard players add #s10 got_g 1
execute if score #s10 got_g matches 10.. run function got:cold/tick
execute if score #camp got_g matches 1 run function got:camp/second
execute if score #state got_g matches 1 run function got:game/running
execute if score #state got_g matches 2 run function got:game/intermission
execute if score #camp got_g matches 1 run function got:hud/update
execute if score #camp got_g matches 0 if score #state got_g matches 1..2 run function got:hud/update
function got:rank/check
