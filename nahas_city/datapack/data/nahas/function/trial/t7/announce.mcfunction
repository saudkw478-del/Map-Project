scoreboard players set #trial nh_g 7
title @a[distance=..60] times 10 90 20
title @a[distance=..60] subtitle {"text":"واجهوا الحارس النحاسي!","color":"yellow"}
title @a[distance=..60] title {"text":"قصر النحاس","color":"gold"}
playsound minecraft:block.bell.use master @a[distance=..60] ~ ~ ~ 1 0.6
execute as @a[distance=..60] at @s run function nahas:hook/trial_start
