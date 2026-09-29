tag @s add nh_got6
scoreboard players set @s nh_lastseal 6
loot give @s loot nahas:items/seal_6
loot give @s loot nahas:gift/seal_reward
advancement grant @s only nahas:seal_6
title @s times 10 70 20
title @s subtitle {"text":"6 من ٧","color":"yellow"}
title @s title {"text":"ختم النحاس السادس","color":"gold"}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0 30
function nahas:hook/seal_gained
