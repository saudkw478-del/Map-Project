scoreboard players set #trial nh_g 1
title @a[distance=..70] times 10 90 20
title @a[distance=..70] subtitle {"text":"اهزم موجات حراس المعبد!","color":"yellow"}
title @a[distance=..70] title {"text":"معبد الواحة","color":"gold"}
playsound minecraft:block.bell.use master @a[distance=..70] ~ ~ ~ 1 0.6
execute as @a[distance=..70] at @s run function nahas:hook/trial_start
