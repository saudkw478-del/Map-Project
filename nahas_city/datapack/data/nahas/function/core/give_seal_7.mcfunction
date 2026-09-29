tag @s add nh_got7
scoreboard players set @s nh_lastseal 7
loot give @s loot nahas:items/seal_7
advancement grant @s only nahas:seal_7
title @s times 10 70 20
title @s subtitle {"text":"7 من ٧","color":"yellow"}
title @s title {"text":"ختم النحاس السابع","color":"gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0 30
function nahas:hook/seal_gained
