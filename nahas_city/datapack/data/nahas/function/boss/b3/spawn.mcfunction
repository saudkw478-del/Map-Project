scoreboard players set #t5 nh_g 50
scoreboard players set #boss nh_g 3
scoreboard players set #b3_ph nh_g 0
scoreboard players set #b3_t nh_g 0
scoreboard players set #b3_miss nh_g 0
scoreboard players set #bmax3 nh_g 350
execute if score #kids nh_g matches 1 run scoreboard players set #bmax3 nh_g 175
execute in nahas:star_sea run summon minecraft:evoker 560 97 921 {Tags:["nh_boss","nh_b3"],PersistenceRequired:1b}
execute in nahas:star_sea positioned 560 97 921 as @e[tag=nh_b3,distance=..6,limit=1] run function nahas:boss/b3/init
bossbar set nahas:boss3 name {"text":"ملكة النجوم","color":"light_purple"}
bossbar set nahas:boss3 color purple
bossbar set nahas:boss3 style notched_10
execute store result bossbar nahas:boss3 max run scoreboard players get #bmax3 nh_g
execute store result bossbar nahas:boss3 value run scoreboard players get #bmax3 nh_g
bossbar set nahas:boss3 visible true
title @a[distance=..100] times 10 60 20
title @a[distance=..100] subtitle {"text":"المعركة بدأت!","color":"yellow"}
title @a[distance=..100] title {"text":"ملكة النجوم","color":"light_purple"}
execute as @a[distance=..100] at @s run function nahas:hook/boss_start
