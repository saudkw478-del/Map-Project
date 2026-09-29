scoreboard players set #trial nh_g 5
title @a[distance=..700] times 10 90 20
title @a[distance=..700] subtitle {"text":"قاوموا أرواح النجوم ثم واجهوا ملكة النجوم!","color":"yellow"}
title @a[distance=..700] title {"text":"بحر النجوم","color":"gold"}
playsound minecraft:block.bell.use master @a[distance=..700] ~ ~ ~ 1 0.6
execute as @a[distance=..700] at @s run function nahas:hook/trial_start
