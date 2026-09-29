scoreboard players set #t2 nh_g 50
scoreboard players set #boss nh_g 1
scoreboard players set #b1_ph nh_g 0
scoreboard players set #b1_t nh_g 0
scoreboard players set #b1_miss nh_g 0
scoreboard players set #bmax1 nh_g 400
execute if score #kids nh_g matches 1 run scoreboard players set #bmax1 nh_g 200
execute in minecraft:overworld run summon minecraft:spider 1800 71 1850 {Tags:["nh_boss","nh_b1"],PersistenceRequired:1b}
execute in minecraft:overworld positioned 1800 71 1850 as @e[tag=nh_b1,distance=..6,limit=1] run function nahas:boss/b1/init
bossbar set nahas:boss1 name {"text":"ملكة العقارب","color":"yellow"}
bossbar set nahas:boss1 color red
bossbar set nahas:boss1 style notched_10
execute store result bossbar nahas:boss1 max run scoreboard players get #bmax1 nh_g
execute store result bossbar nahas:boss1 value run scoreboard players get #bmax1 nh_g
bossbar set nahas:boss1 visible true
title @a[distance=..100] times 10 60 20
title @a[distance=..100] subtitle {"text":"المعركة بدأت!","color":"yellow"}
title @a[distance=..100] title {"text":"ملكة العقارب","color":"yellow"}
execute as @a[distance=..100] at @s run function nahas:hook/boss_start
