scoreboard players operation #b4_ph nh_g = #np nh_g
scoreboard players operation #phase nh_g = #np nh_g
scoreboard players set #boss nh_g 4
execute if score #np nh_g matches 1 run function nahas:boss/b4/p1
execute if score #np nh_g matches 2 run function nahas:boss/b4/p2
execute if score #np nh_g matches 3 run function nahas:boss/b4/p3
execute as @a[distance=..100] at @s run function nahas:hook/boss_phase
