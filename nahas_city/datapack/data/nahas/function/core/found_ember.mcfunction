tag @s add nh_d_ember
scoreboard players add @s nh_disc 1
scoreboard players add @s nh_gold 15
title @s times 10 50 20
title @s subtitle {"text":"اكتشفت مكاناً جديداً","color":"gray"}
title @s title {"text":"بوابة الجمر","color":"yellow"}
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1
advancement grant @s only nahas:disc_ember
