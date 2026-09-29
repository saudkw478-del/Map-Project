scoreboard players set #t6 nh_g 50
scoreboard players set #boss nh_g 4
scoreboard players set #b4_ph nh_g 0
scoreboard players set #b4_t nh_g 0
scoreboard players set #b4_miss nh_g 0
scoreboard players set #bmax4 nh_g 450
execute if score #kids nh_g matches 1 run scoreboard players set #bmax4 nh_g 225
execute in nahas:ember run summon minecraft:wither_skeleton 500 65 496 {Tags:["nh_boss","nh_b4"],PersistenceRequired:1b}
execute in nahas:ember positioned 500 65 496 as @e[tag=nh_b4,distance=..6,limit=1] run function nahas:boss/b4/init
bossbar set nahas:boss4 name {"text":"عملاق الجمر","color":"red"}
bossbar set nahas:boss4 color red
bossbar set nahas:boss4 style notched_10
execute store result bossbar nahas:boss4 max run scoreboard players get #bmax4 nh_g
execute store result bossbar nahas:boss4 value run scoreboard players get #bmax4 nh_g
bossbar set nahas:boss4 visible true
title @a[distance=..100] times 10 60 20
title @a[distance=..100] subtitle {"text":"المعركة بدأت!","color":"yellow"}
title @a[distance=..100] title {"text":"عملاق الجمر","color":"red"}
execute as @a[distance=..100] at @s run function nahas:hook/boss_start
