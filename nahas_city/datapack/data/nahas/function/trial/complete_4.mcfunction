scoreboard players set #t4 nh_g 9
scoreboard players set #trial nh_g 4
scoreboard players set #s4 nh_g 1
function nahas:core/seal_recount
execute as @a at @s run function nahas:core/seal_sync
execute as @a at @s run function nahas:hook/trial_done
