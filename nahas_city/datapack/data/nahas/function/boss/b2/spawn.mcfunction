scoreboard players set #t4 nh_g 50
scoreboard players set #boss nh_g 2
scoreboard players set #b2_ph nh_g 0
scoreboard players set #b2_t nh_g 0
scoreboard players set #b2_miss nh_g 0
scoreboard players set #bmax2 nh_g 300
execute if score #kids nh_g matches 1 run scoreboard players set #bmax2 nh_g 150
execute in minecraft:overworld run summon minecraft:breeze 1700 152 436 {Tags:["nh_boss","nh_b2"],PersistenceRequired:1b}
execute in minecraft:overworld positioned 1700 152 436 as @e[tag=nh_b2,distance=..6,limit=1] run function nahas:boss/b2/init
bossbar set nahas:boss2 name {"text":"قائد الرياح","color":"white"}
bossbar set nahas:boss2 color purple
bossbar set nahas:boss2 style notched_10
execute store result bossbar nahas:boss2 max run scoreboard players get #bmax2 nh_g
execute store result bossbar nahas:boss2 value run scoreboard players get #bmax2 nh_g
bossbar set nahas:boss2 visible true
title @a[distance=..100] times 10 60 20
title @a[distance=..100] subtitle {"text":"المعركة بدأت!","color":"yellow"}
title @a[distance=..100] title {"text":"قائد الرياح","color":"white"}
execute as @a[distance=..100] at @s run function nahas:hook/boss_start
