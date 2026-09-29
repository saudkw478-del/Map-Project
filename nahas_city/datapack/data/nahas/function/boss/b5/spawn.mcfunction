scoreboard players set #t7 nh_g 50
scoreboard players set #boss nh_g 5
scoreboard players set #b5_ph nh_g 0
scoreboard players set #b5_t nh_g 0
scoreboard players set #b5_miss nh_g 0
scoreboard players set #bmax5 nh_g 800
execute if score #kids nh_g matches 1 run scoreboard players set #bmax5 nh_g 400
execute in minecraft:overworld run summon minecraft:iron_golem 1200 71 1200 {Tags:["nh_boss","nh_b5"],PersistenceRequired:1b}
execute in minecraft:overworld positioned 1200 71 1200 as @e[tag=nh_b5,distance=..6,limit=1] run function nahas:boss/b5/init
bossbar set nahas:boss5 name {"text":"الحارس النحاسي","color":"gold"}
bossbar set nahas:boss5 color red
bossbar set nahas:boss5 style notched_10
execute store result bossbar nahas:boss5 max run scoreboard players get #bmax5 nh_g
execute store result bossbar nahas:boss5 value run scoreboard players get #bmax5 nh_g
bossbar set nahas:boss5 visible true
title @a[distance=..100] times 10 60 20
title @a[distance=..100] subtitle {"text":"المعركة بدأت!","color":"yellow"}
title @a[distance=..100] title {"text":"الحارس النحاسي","color":"gold"}
execute as @a[distance=..100] at @s run function nahas:hook/boss_start
