bossbar set nahas:boss2 visible false
bossbar set nahas:boss2 players
scoreboard players set #b2_ph nh_g 0
kill @e[tag=nh_bm,distance=..150]
loot spawn ~ ~1 ~ loot nahas:chests/boss
execute as @a[distance=..100] run scoreboard players add @s nh_gold 100
title @a[distance=..100] times 10 70 20
title @a[distance=..100] subtitle {"text":"قائد الرياح هُزم","color":"yellow"}
title @a[distance=..100] title {"text":"انتصرتم!","color":"green"}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..100] ~ ~ ~ 1 1
particle minecraft:totem_of_undying ~ ~2 ~ 3 2 3 0.3 100
function nahas:trial/complete_4
