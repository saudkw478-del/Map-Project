scoreboard players set #trial nh_g 3
title @a[distance=..70] times 10 90 20
title @a[distance=..70] subtitle {"text":"اجمع ثلاث صفحات مفقودة من حراس الأعماق!","color":"yellow"}
title @a[distance=..70] title {"text":"المكتبة الغارقة","color":"gold"}
playsound minecraft:block.bell.use master @a[distance=..70] ~ ~ ~ 1 0.6
execute as @a[distance=..70] at @s run function nahas:hook/trial_start
