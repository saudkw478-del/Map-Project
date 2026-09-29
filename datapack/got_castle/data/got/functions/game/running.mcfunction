execute if score #enemies got_g matches 1..5 run effect give @e[tag=got_enemy] minecraft:glowing 3 0 true
execute as @e[tag=got_enemy,tag=!got_boss] at @s unless entity @a[distance=..30] run function got:game/march
execute if score #enemies got_g matches 0 run function got:game/wave_clear
