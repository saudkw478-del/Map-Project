tag @s add nh_got3
scoreboard players set @s nh_lastseal 3
loot give @s loot nahas:items/seal_3
loot give @s loot nahas:gift/seal_reward
advancement grant @s only nahas:seal_3
title @s times 10 70 20
title @s subtitle {"text":"3 من ٧","color":"yellow"}
title @s title {"text":"ختم النحاس الثالث","color":"gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0 30
function nahas:hook/seal_gained
