scoreboard players set #trial nh_g 6
title @a[distance=..400] times 10 90 20
title @a[distance=..400] subtitle {"text":"اهزموا حراس الجمر ثم عملاق الجمر!","color":"yellow"}
title @a[distance=..400] title {"text":"أرض الجمر","color":"gold"}
playsound minecraft:block.bell.use master @a[distance=..400] ~ ~ ~ 1 0.6
execute as @a[distance=..400] at @s run function nahas:hook/trial_start
