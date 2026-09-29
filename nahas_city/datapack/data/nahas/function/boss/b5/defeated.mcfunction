bossbar set nahas:boss5 visible false
bossbar set nahas:boss5 players
scoreboard players set #b5_ph nh_g 0
kill @e[tag=nh_bm,distance=..150]
loot spawn ~ ~1 ~ loot nahas:chests/boss
execute as @a[distance=..100] run scoreboard players add @s nh_gold 100
title @a[distance=..100] times 10 70 20
title @a[distance=..100] subtitle {"text":"الحارس النحاسي هُزم","color":"yellow"}
title @a[distance=..100] title {"text":"انتصرتم!","color":"green"}
playsound minecraft:ui.toast.challenge_complete master @a[distance=..100] ~ ~ ~ 1 1
particle minecraft:totem_of_undying ~ ~2 ~ 3 2 3 0.3 100
function nahas:trial/complete_7
execute as @a at @s run function nahas:hook/boss_defeated
advancement grant @a only nahas:final
execute as @a run loot give @s loot nahas:gift/final_reward
tellraw @a ["",{"text":"هُزم الحارس النحاسي! استيقظت المدينة وتحرر أهلها. شكراً لكم أيها الأبطال!","color":"gold","bold":true}]
